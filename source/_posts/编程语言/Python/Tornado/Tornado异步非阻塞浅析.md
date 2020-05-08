---
title: Tornado 异步非阻塞浅析
date: 2017-11-17
tags: [Tornado]
id: 1
---

[以下代码基于 Tornado 3.2.1 版本讲解]
[主要目标：讲解 gen.coroutine、Future、Runner 之间的关系]


这里是示例运行代码
```
#!/usr/bin/python
# coding: utf-8
"""
File: demo.py
Author: noogel
Date: 2017-08-28 22:59
Description: demo
"""
import tornado

from tornado import gen, web


@gen.coroutine
def service_method():
    raise gen.Return("abc")


class NoBlockHandler(tornado.web.RequestHandler):

    @web.asynchronous
    @gen.coroutine
    def get(self):
        result = yield service_method()
        self.write(result)
        self.finish()


class Application(tornado.web.Application):

    def __init__(self):
        settings = {
            "xsrf_cookies": False,
        }
        handlers = [
            (r"/api/noblock", NoBlockHandler),
        ]
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    Application().listen(2345)
    tornado.ioloop.IOLoop.instance().start()

```

> 演示运行效果...

讲解从 coroutine 修饰器入手，这个函数实现了简单的异步，它通过 generator 中的 yield 语句使函数暂停执行，将中间结果临时保存，然后再通过 send() 函数将上一次的结果送入函数恢复函数执行。

```
def coroutine(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        future = TracebackFuture()
        if 'callback' in kwargs:
            print("gen.coroutine callback:{}".format(kwargs['callback']))
            callback = kwargs.pop('callback')
            IOLoop.current().add_future(
                future, lambda future: callback(future.result()))
        try:
            print("gen.coroutine run func:{}".format(func))
            result = func(*args, **kwargs)
        except (Return, StopIteration) as e:
            result = getattr(e, 'value', None)
        except Exception:
            future.set_exc_info(sys.exc_info())
            return future
        else:
            if isinstance(result, types.GeneratorType):
                def final_callback(value):
                    deactivate()
                    print("gen.coroutine final set_result:{}".format(value))
                    future.set_result(value)
                print("gen.coroutine will Runner.run() result:{}".format(result))
                runner = Runner(result, final_callback)
                runner.run()
                return future
        print("@@ gen.coroutine will set_result and return:{}".format(result))
        future.set_result(result)
        return future
    return wrapper
```

```flow
st=>start: create future object
rf=>operation: run function
ex=>condition: is not exception
gen=>condition: is generator
run=>operation: Runner.run()
fts=>operation: future.set_done()
rtnf=>operation: return future
ed=>end

st->rf->ex
ex(no)->rtnf
ex(yes)->gen
gen(yes)->run
gen(no)->rtnf
run->rtnf
rtnf->ed
```


首先创建一个Future实例，然后执行被修饰的函数，一般函数返回的是一个生成器对象，接下来交由 Runner 处理，如果函数返回的是 Return, StopIteration 那么表示函数执行完成将结果放入 future 中并 set_done() 返回。

下面是Future的简版：
```
class Future(object):

    def __init__(self):
        self._result = None
        self._callbacks = []

    def result(self, timeout=None):
        self._clear_tb_log()
        if self._result is not None:
            return self._result
        if self._exc_info is not None:
            raise_exc_info(self._exc_info)
        self._check_done()
        return self._result

    def add_done_callback(self, fn):
        if self._done:
            fn(self)
        else:
            self._callbacks.append(fn)

    def set_result(self, result):
        self._result = result
        self._set_done()

    def _set_done(self):
        self._done = True
        for cb in self._callbacks:
            try:
                cb(self)
            except Exception:
                app_log.exception('Exception in callback %r for %r', cb, self)
        self._callbacks = None
```
在tornado中大多数的异步操作返回一个Future对象，这里指的是 Runner 中处理的异步返回结果。我们可以将该对象抽象成一个占位对象，它包含很多属性和函数。一个 Future 对象一般对应这一个异步操作。当这个对象的异步操作完成后会通过 set_done() 函数去处理 _callbacks 中的回调函数，这个回调函数是在我们在做修饰定义的时候传入 coroutine 中的。

下面的代码是在 coroutine 中定义的，用来添加对异步操作完成后的回调处理。
```
if 'callback' in kwargs:
    print("gen.coroutine callback:{}".format(kwargs['callback']))
    callback = kwargs.pop('callback')
    IOLoop.current().add_future(
        future, lambda future: callback(future.result()))
```
这里是 IOLoop 中的 add_future 函数，它是来给 future 对象添加回调函数的。
```
def add_future(self, future, callback):
    assert isinstance(future, Future)
    callback = stack_context.wrap(callback)
    future.add_done_callback(
        lambda future: self.add_callback(callback, future))
```

然后说 Runner 都做了什么。在 3.2.1 版本中 Runner 的作用更重要一些。那么 Runner() 的作用是什么？
它主要用来控制生成器的执行与终止，将异步操作的结果 send() 至生成器暂停的地方恢复执行。在生成器嵌套的时候，当 A 中 yield B 的时候，先终止 A 的执行去执行 B，然后当 B 执行结束后将结果 send 至 A 终止的地方继续执行 A。
```
class Runner(object):
    def __init__(self, gen, final_callback):
        self.gen = gen
        self.final_callback = final_callback
        self.yield_point = _null_yield_point
        self.results = {}
        self.running = False
        self.finished = False

    def is_ready(self, key):
        if key not in self.pending_callbacks:
            raise UnknownKeyError("key %r is not pending" % (key,))
        return key in self.results

    def set_result(self, key, result):
        self.results[key] = result
        self.run()

    def pop_result(self, key):
        self.pending_callbacks.remove(key)
        return self.results.pop(key)

    def run(self):
        try:
            self.running = True
            while True:
                next = self.yield_point.get_result()
                self.yield_point = None
                try:
                    print("gen.Runner.run() will send(next)")
                    yielded = self.gen.send(next)
                    print("gen.Runner.run() send(next) done.")
                except (StopIteration, Return) as e:
                    print("gen.Runner.run() send(next) throw StopIteration or Return done.")
                    self.finished = True
                    self.yield_point = _null_yield_point
                    self.final_callback(getattr(e, 'value', None))
                    self.final_callback = None
                    return
                if isinstance(yielded, (list, dict)):
                    yielded = Multi(yielded)
                elif isinstance(yielded, Future):
                    yielded = YieldFuture(yielded)
                    self.yield_point = yielded
                    self.yield_point.start(self)
        finally:
            self.running = False

    def result_callback(self, key):
        def inner(*args, **kwargs):
            if kwargs or len(args) > 1:
                result = Arguments(args, kwargs)
            elif args:
                result = args[0]
            else:
                result = None
            self.set_result(key, result)
        return wrap(inner)

```

实例化 Runner() 的时候将生成器对象和生成器执行结束时的回调函数传入，然后通过 run() 函数去继续执行生成器对象。

run() 函数的处理首先包了一层 while 循环，因为在生成器对象中可能包含多个 yield 语句。

`yielded = self.gen.send(next)`，在第一次 send() 恢复执行的时候默认传入 None ,因为函数第一次执行并没有结果。然后将第二次执行的结果 yielded （返回的是一个 Future 对象），包装成一个 YieldFuture 对象，然后通过 start()  函数处理：

```
def start(self, runner):
    if not self.future.done():
        self.runner = runner
        self.key = object()
        self.io_loop.add_future(self.future, runner.result_callback(self.key))
    else:
        self.runner = None
        self.result = self.future.result()
```

首先判断 future 是否被 set_done()，如果没有则注册一系列回调函数，如果完成则保存结果，以供下一次恢复执行时将结果送入生成器。
在 Runner.run() 执行完成后此时的 coroutine 中的 future 对象已经是被 set_done 的，然后直接返回 future 对象，最后被 外层的 @web.asynchronous 修饰器消费。

------

参考：
> http://www.cnblogs.com/MnCu8261/p/6560502.html
> https://www.cnblogs.com/chenchao1990/p/5406245.html
> http://blog.csdn.net/u010168160/article/details/53019039
> https://www.cnblogs.com/yezuhui/p/6863781.html
> http://blog.csdn.net/zhaohongyan6/article/details/70888221
> https://www.zybuluo.com/noogel/note/952488