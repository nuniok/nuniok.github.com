---
title: Tornado学习总结
date: 2015-05-28
tags: [Python, Tornado]
id: 1
---

## 框架
![原始图像](/resource/img/Tornado/tornado1.png)

## 四层
* WEB框架（处理器、模板、数据库连接、认证、本地化等）
* HTTP/HTTPS层（基于HTTP协议实现了HTTP服务器和客户端）
* TCP层（TCP服务器，负责数据传输）
* EVENT层（处理IO事件）

============================================================

## 基础用法学习

### 请求处理程序和请求参数

程序将URL映射到tornado.web.RequestHandler的子类上去。
```python
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("You requested the main page")
 
class StoryHandler(tornado.web.RequestHandler):
    def get(self, story_id):
        self.write("You requested the story " + story_id)
 
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/story/([0-9]+)", StoryHandler),
])
```
`get_argument()` 方法获取查询字符串参数。
`self.request.files` 可以访问上传文件。
![原始图像](/resource/img/Tornado/tornado2.png)

在继承类中通过 self.request.arguments.items() 方法获取所有返回对象。

### 重写RequestHandler的方法函数

程序调用 initialize() 函数，这个函数的参数是 Application 配置中的关键字 参数定义。initialize 方法一般只是把传入的参数存 到成员变量中，而不会产生一些输出或者调用像 send_error 之类的方法。
程序调用 prepare()。无论使用了哪种 HTTP 方法，prepare 都会被调用到，因此 这个方法通常会被定义在一个基类中，然后在子类中重用。prepare可以产生输出 信息。如果它调用了finish（或send_error` 等函数），那么整个处理流程 就此结束。
程序调用某个 HTTP 方法：例如 get()、post()、put() 等。如果 URL 的正则表达式模式中有分组匹配，那么相关匹配会作为参数传入方法，见下图：
![原始图像](/resource/img/Tornado/tornado3.png)

见 code 1，RequestHandler中一些方法函数需要在其子类中重新定义`handler\base.py`
![原始图像](/resource/img/Tornado/tornado4.png)

`get_current_user()` 处理获得当前用户

### 重定向
通过 `self.redirect` 或 `RedirectHandler `。
```python
application = tornado.wsgi.WSGIApplication([
    (r"/([a-z]*)", ContentHandler),
    (r"/static/tornado-0.2.tar.gz", tornado.web.RedirectHandler,
     dict(url="http://github.com/downloads/facebook/tornado/tornado-0.2.tar.gz")),
], **settings)
```

### 模板
模板支持 `{ % 控制语句 % }`、`{ { 表达式 } }`
可以通过 extends 和 block 实现模板继承。


### Cookie和Cookie安全
通过下面方式加强安全性
```python
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        if not self.get_secure_cookie("mycookie"):
            self.set_secure_cookie("mycookie", "myvalue")
            self.write("Your cookie was not set yet!")
        else:
            self.write("Your cookie was set!")
 
application = tornado.web.Application([
    (r"/", MainHandler),
], cookie_secret="61oaBcAaaXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=")
```
另一种配置写法：
```python
class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        name = tornado.escape.xhtml_escape(self.current_user)
        self.write("Hello, " + name)
 
settings = {
    "cookie_secret": "61oaBcAaaXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "login_url": "/login",
}
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/login", LoginHandler),
], **settings)
```
`@tornado.web.authenticated` 用于用户认证
`cookie_secret`用于加密cookie
`login_url` 记录重定向地址
`xsrf_cookies` 开关XSRF防范机制
![原始图像](/resource/img/Tornado/tornado5.png)

### 静态文件和主动式文件缓存
`"static_path": os.path.join(os.path.dirname(__file__), "static")`
static_url() 函数会将相对地址转成一个类似于 /static/images/logo.png?v=aae54 的 URI，v 参数是 logo.png 文件的散列值， Tornado 服务器会把它发给浏览器，并以此为依据让浏览器对相关内容做永久缓存。
由于 v 的值是基于文件的内容计算出来的，如果你更新了文件，或者重启了服务器 ，那么就会得到一个新的 v 值，这样浏览器就会请求服务器以获取新的文件内容。 如果文件的内容没有改变，浏览器就会一直使用本地缓存的文件，这样可以显著提高页 面的渲染速度。

### 本地化

### UI模块
```python
class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        entries = self.db.query("SELECT * FROM entries ORDER BY date DESC")
        self.render("home.html", entries=entries)
 
class EntryHandler(tornado.web.RequestHandler):
    def get(self, entry_id):
        entry = self.db.get("SELECT * FROM entries WHERE id = %s", entry_id)
        if not entry: raise tornado.web.HTTPError(404)
        self.render("entry.html", entry=entry)
 
settings = {
    "ui_modules": uimodules,
}
application = tornado.web.Application([
    (r"/", HomeHandler),
    (r"/entry/([0-9]+)", EntryHandler),
], **settings)
{% module Entry(entry, show_comments=True) %}
```

### 非阻塞式异步请求
Tornado 当中使用了 一种非阻塞式的 I/O 模型，所以你可以改变这种默认的处理行为——让一个请求一直保持 连接状态，而不是马上返回，直到一个主处理行为返回。要实现这种处理方式，只需要 使用 tornado.web.asynchronous 装饰器就可以了。

### 调试模式和自动重载
如果你将 debug=True 传递给 Application 构造器，该 app 将以调试模式 运行。在调试模式下，模板将不会被缓存，而这个 app 会监视代码文件的修改， 如果发现修改动作，这个 app 就会被重新加载。在开发过程中，这会大大减少 手动重启服务的次数。然而有些问题（例如 import 时的语法错误）还是会让服务器 下线，目前的 debug 模式还无法避免这些情况。

[参考地址](http://demo.pythoner.com/itt2zh/index.html)
