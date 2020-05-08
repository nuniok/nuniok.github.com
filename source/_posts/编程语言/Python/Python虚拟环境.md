---
title: Python 虚拟环境 virtualenv
date: 2017-12-12
tags: [Python, virtualenv]
id: 1
---

## 安装
`pip install virtualenv`

## 创建虚拟环境
```
root@kali:/recall/code# virtualenv test_env
New python executable in test_env/bin/python 
Installing setuptools, pip...done.
root@kali:/recall/code#
```
默认情况下，虚拟环境会依赖系统环境中的site packages，就是说系统中已经安装好的第三方package也会安装在虚拟环境中，
如果不想依赖这些package，那么可以加上参数 

--no-site-packages　
```
root@kali:/recall/code# virtualenv test_env --no-site-packages 
New python executable in test_env/bin/python 
Installing setuptools, pip...done.
root@kali:/recall/code#
```

或者进入到项目目录：`virtualenv .`，如果需要指定 Python3 则 `virtualenv -p python .`


## 启动虚拟环境
我们先进入到该目录下：`cd test_env/`
```
source bin/activate
```
启动成功后，会在前面多出 test_env 字样，如下所示
```
(test_env)root@kali:/recall/code/test_env#
```

## 退出虚拟环境
```
deactivate
```




