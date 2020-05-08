---
title: Asynchronous and non-Blocking I/O 翻译
date: 2016-08-04
tags: [Python, Tornado, 异步非阻塞]
id: 1
---

> http://www.tornadoweb.org/en/stable/guide/async.html

Real-time web features require a long-lived mostly-idle connection per user. In a traditional synchronous web server, this implies 
devoting one thread to each user, which can be very expensive.
*在同步状态下，实时的网络请求会一直占用着一个空的连接，这样每一个用户都会占用着一个线程，很浪费*
 
To minimize the cost of concurrent connections, Tornado uses a single-threaded event loop. This means that all application code should aim to be asynchronous and non-blocking because only one operation can be active at a time.
*为了最大限度的利用连接，Tornado使用单线程事件循环的方式。就是使应用采用异步和非阻塞的方式保持着当下只有一个活动的事件，同时又能接收多个应用请求。*
 
The terms asynchronous and non-blocking are closely related and are often used interchangeably, but they are not quite the same thing.
*异步和非阻塞这两个术语通常意思一样，但是他们也有不同的地方。*

## Blocking

A function blocks when it waits for something to happen before returning. A function may block for many reasons: network I/O, disk I/O, mutexes, etc. In fact, every function blocks, at least a little bit, while it is running and using the CPU (for an extreme example that demonstrates why CPU blocking must be taken as seriously as other kinds of blocking, consider password hashing functions like bcrypt, which by design use hundreds of milliseconds of CPU time, far more than a typical network or disk access).
*等待这个功能模块返回结果前，函数有很多阻塞的原因，比如：网络I/O、磁盘I/O、互斥操作等。事实上每个功能模块在它运行的时候都会使用一点CPU资源（CPU阻塞必须要当做其它类型的阻塞）*
 
A function can be blocking in some respects and non-blocking in others. For example, tornado.httpclient in the default configuration blocks on DNS resolution but not on other network access (to mitigate this use ThreadedResolver or a tornado.curl_httpclient with a properly-configured build of libcurl). In the context of Tornado we generally talk about blocking in the context of network I/O, although all kinds of blocking are to be minimized.
*函数能在一些方面阻塞，在另一些方面不阻塞，*******，在Tornado下我们一般讨论的是网络I/O阻塞，其它情况都是很小的。*
*Tornado里面讨论的阻塞都是指网络阻塞，其它的阻塞可以忽略。*

## Asynchronous

An asynchronous function returns before it is finished, and generally causes some work to happen in the background before triggering some future action in the application (as opposed to normal synchronous functions, which do everything they are going to do before returning). There are many styles of asynchronous interfaces:
*异步函数会在执行结束之前返回，在完成之后通常是一些后台程序去触发预先设定好的处理程序（不像同步程序，必须都做完了才返回）。下面列举了很多种风格的异步接口。*
 
* Callback argument *回调参数*
* Return a placeholder (Future, Promise, Deferred) *返回一个占位符*
* Deliver to a queue *交付到队列中*
* Callback registry (e.g. POSIX signals) *回调到注册表中*

Regardless of which type of interface is used, asynchronous functions by definition interact differently with their callers; there is no free way to make a synchronous function asynchronous in a way that is transparent to its callers (systems like gevent use lightweight threads to offer performance comparable to asynchronous systems, but they do not actually make things asynchronous).
*无论使用哪种接口，异步函数都会使用不同的方式与调用者交互；没有办法去定义一个同步函数却采用异步的方式调用，对于调用者来说都是透明的（就像采用gevent的轻量级线程系统去提供做到的性能堪比异步系统，但它实际上并不是异步）。*
*这句话的意思就是说同步的方法没法用异步的方式去调，虽然你写的代码看起来像是异步的，但其实并不是。*

## Examples

Here is a sample synchronous function:
*下面的例子是一个同步函数。*

```
from tornado.httpclient import HTTPClient
 
def synchronous_fetch(url):
    http_client = HTTPClient()
    response = http_client.fetch(url)
    return response.body
```

And here is the same function rewritten to be asynchronous with a callback argument:
*下面的例子被重写成异步的方式了，采用了回调参数的方式。*
 
```
from tornado.httpclient import AsyncHTTPClient
 
def asynchronous_fetch(url, callback):
    http_client = AsyncHTTPClient()
    def handle_response(response):
        callback(response.body)
    http_client.fetch(url, callback=handle_response)
```

And again with a Future instead of a callback:
*下面的例子通过返回一个展位符的方式实现异步回调的。*
 
```
from tornado.concurrent import Future
 
def async_fetch_future(url):
    http_client = AsyncHTTPClient()
    my_future = Future()
    fetch_future = http_client.fetch(url)
    fetch_future.add_done_callback(
        lambda f: my_future.set_result(f.result()))
    return my_future
```

The raw Future version is more complex, but Futures are nonetheless recommended practice in Tornado because they have two major advantages. Error handling is more consistent since the Future.result method can simply raise an exception (as opposed to the ad-hoc error handling common in callback-oriented interfaces), and Futures lend themselves well to use with coroutines. Coroutines will be discussed in depth in the next section of this guide. Here is the coroutine version of our sample function, which is very similar to the original synchronous version:
*通过`Future`的方式实现的更复杂，但是Tornado更建议这样去写，主要有两个原因。从`Future`返回的错误处理更一致，从`Future.result`方法可以返回一个简单的异常，`Future`能够更好的与协同程序一起使用。协同程序的具体讨论将会在下一节讨论，下面的例子给了一个协同程序的例子，写法很像同步的那个版本。*
 
```
from tornado import gen
 
@gen.coroutine
def fetch_coroutine(url):
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(url)
    raise gen.Return(response.body)
```

The statement raise gen.Return(response.body) is an artifact of Python 2, in which generators aren’t allowed to return values. To overcome this, Tornado coroutines raise a special kind of exception called a Return. The coroutine catches this exception and treats it like a returned value. In Python 3.3 and later, a return response.body achieves the same result.
*这个版本中返回一个`raise gen.Return(response.body)`，在Python2中的用法，因为生成器不允许返回一个值，所以Tornado做了特殊处理，通过跑出一个`Return`的异常，然后协同程序补货这个异常，就相当于返回值了。在Python3.3以后就可以直接返回这个值了。*

> Translated by zhangxu on 2016-08-05