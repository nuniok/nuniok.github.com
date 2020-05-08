---
title: Python简单web服务
date: 2015-03-18
tags: [Python, web]
id: 1
---

利用Python自带的包可以建立简单的web服务器。在DOS里cd到准备做服务器根目录的路径下，输入命令：
python -m Web服务器模块 [端口号，默认8000]
例如：
python -m SimpleHTTPServer 8080
然后就可以在浏览器中输入
http://localhost:端口号/路径
来访问服务器资源。 
例如：
http://localhost:8080/index.htm（当然index.htm文件得自己创建）
其他机器也可以通过服务器的IP地址来访问。

这里的“Web服务器模块”有如下三种：
- BaseHTTPServer: 提供基本的Web服务和处理器类，分别是HTTPServer和BaseHTTPRequestHandler。
- SimpleHTTPServer: 包含执行GET和HEAD请求的SimpleHTTPRequestHandler类。
- CGIHTTPServer: 包含处理POST请求和执行CGIHTTPRequestHandler类。