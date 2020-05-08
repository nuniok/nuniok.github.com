---
title: Python的mixin模式
date: 2018-01-12
tags: Python
id: 1
---

Mixin 是利用语言特性来简洁的实现组合模式，Python 中通过一定规范的多继承实现的。

使用时需要注意一下几点：

* 类的单一职责
* 对宿主类一无所知
* 不存在对宿主类的方法调用，避免引入 MRO 查找顺序

如下例子，对于不同的 Mixin 类只负责实现自己的行为特征函数，然后 People 类继承这些特征，在自己的函数中使用这些特征。

```
#!/usr/bin/python
# coding: utf-8
"""
File: mixin_demo.py
Author: noogel <noogel@163.com>
Date: 2018-01-12 09:11
Description: mixin_demo
"""


class EatMixin(object):

    def eat(self):
        return "eat!"


class DrinkMixin(object):

    def drink(self):
        return "drink!"


class SleepMixin(object):

    def sleep(self):
        return "sleep!"


class People(EatMixin, DrinkMixin, SleepMixin):

    def __init__(self):
        print "People can ", self.eat()
        print "People can ", self.drink()
        print "People can ", self.sleep()


if __name__ == "__main__":
    print "Init people."
    people = People()

```

```text
➜  dev-demo python mixin_demo.py 
Init people.
People can  eat!
People can  drink!
People can  sleep!
```

> https://www.zhihu.com/question/20778853

