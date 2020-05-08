---
title: Python元类
date: 2019-01-09
tags: Python
id: 1
---

<iframe frameborder="no" border="0" marginwidth="0" marginheight="0" width=330 height=86 src="//music.163.com/outchain/player?type=2&id=34125745&auto=1&height=66"></iframe>

```
class BaseMetaClass(type):
    ___sub_class = {}

    def __iter__(self):
        for item in BaseMetaClass.___sub_class.itervalues():
            yield item

    def __repr__(cls):
        return cls.__name__

    def __new__(mcs, name, bases, attrs):
        new_cls = super(BaseMetaClass, mcs).__new__(mcs, name, bases, attrs)
        if object not in bases:
            BaseMetaClass.___sub_class[new_cls.__name__] = new_cls
        print mcs, name, bases, attrs, new_cls
        return new_cls


class NotifyManager(object):
    __metaclass__ = BaseMetaClass

    def __iter__(self):
        yield self.__metaclass__


class TestA(NotifyManager):

    @classmethod
    def notify(cls):
        return cls.__name__


class TestB(NotifyManager):

    @classmethod
    def notify(cls):
        return cls.__name__
```

