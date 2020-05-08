---
title: Python 包管理
date: 2015-09-19
tags: [pip, easy_install]
id: 1
---

## pip

pip更新`python -m pip install -U pip`

### pipy国内镜像目前有：

https://pypi.douban.com/  豆瓣

https://mirrors.tuna.tsinghua.edu.cn/pypi/web/ 清华大学


### 指定源安装

pip可以通过指定源的方式安装 `pip install web.py -i https://pypi.douban.com/simple`

也可以通过修改配置文件，Linux的文件在`~/.pip/pip.conf`，Windows在`%HOMEPATH%\pip\pip.ini`。

```
[global]
index-url = https://pypi.douban.com/simple
```

---------

## easy_install

easy_install指定源安装 `easy_install -i https://pypi.douban.com/simple`

或者修改配置文件 `~/.pydistutils.cfg`：

```
[easy_install]
index_url = http://e.pypi.python.org/simple
```

easy_install查看包的版本

```
root@xyz-pc:~# easy_install tornado -v
Searching for tornado
Best match: tornado 4.0.2
tornado 4.0.2 is already the active version in easy-install.pth

Using /usr/lib/python2.7/dist-packages
Processing dependencies for tornado
Finished processing dependencies for tornado
Searching for -v
Reading https://pypi.python.org/simple/-v/
Couldn't find index page for '-v' (maybe misspelled?)
Scanning index of all packages (this may take a while)
Reading https://pypi.python.org/simple/
No local packages or download links found for -v
error: Could not find suitable distribution for Requirement.parse('-v')
```

-----------

## 安装Python安装包管理工具相关命令

安装easy_install：`apt-get install python-setuptools`

`sudo yum install python-setuptools-devel`

`esay_install pip`

pip指定版本：`pip install 'pymongo<2.8'`

升级版本：`pip install --upgrade pymongo`

查看已安装包：`pip show --files SomePackage`

查看需要更新的包：`pip list --outdated`

卸载包：`pip uninstall SomePackage`

帮助：`pip --help`

指定豆瓣源安装：`pip install -i https://pypi.douban.com/simple/ functools32`

查看已安装包：`pip list`

> http://www.cnblogs.com/taosim/articles/3288821.html

## pipenv


安装 `pip3 install pipenv`

安装虚拟环境 `pipenv install`

启动虚拟环境 `pipenv shell`

查看当前环境依赖 `pip3 list`

退出虚拟环境 `exit`

安装 `pipenv install ……`

卸载 `pipenv uninstall ……`

查看依赖关系 `pipenv graph`

查看虚拟环境路径 `pipenv --venv`

删除环境 `pipenv --rm`

创建 Python3 环境 `pipenv --three`
