---
title: Python字符串编码
date: 2017-06-24
tags: Python
id: 1
---


说道Python字符串编码处理会让很人头疼，下面介绍一些 Python 处理字符串编码的方式。


## chardet 模块

chardet 主要用于编码识别

pip安装： `sudo pip install chardet`

官方地址： http://pypi.python.org/pypi/chardet

```
In [1]: import chardet

In [2]: import urllib

In [3]: test_data = urllib.urlopen('http://www.baidu.com/').read()

In [4]: chardet.detect(test_data)
Out[4]: {'confidence': 0.99, 'language': '', 'encoding': 'utf-8'}

In [5]: isinstance(test_data.decode('utf-8'), unicode)
Out[5]: True

In [6]: isinstance(test_data, unicode)
Out[6]: False

```

运行结果：
`{'confidence': 0.99, 'language': '', 'encoding': 'utf-8'}`
运行结果表示有 99% 的概率认为这段代码是 utf-8 编码方式。


对于大文件的编码识别，可以通过 UniversalDetector 部分读取进行检查。
```
In [1]: import urllib

In [2]: import chardet

In [3]: from chardet.universaldetector import UniversalDetector

In [4]: uso = urllib.urlopen('http://www.baidu.com/')
   ...: det = UniversalDetector()
   ...: for line in uso.readlines():
   ...:     det.feed(line)
   ...:     if det.done:
   ...:         break
   ...: det.close()
   ...: uso.close()
   ...: det.result
   ...:
Out[4]: {'confidence': 0.99, 'encoding': 'utf-8', 'language': ''}

```
运行结果：
`{'confidence': 0.99, 'encoding': 'utf-8', 'language': ''}`


## Python 模块之 codecs


> Mark未完

