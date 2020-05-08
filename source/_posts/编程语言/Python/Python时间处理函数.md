---
title: Python时间处理函数
date: 2018-02-06
tags: Python
id: 2
---

## 常用时间表示方法

时间处理看似简单，不熟悉的话实则也有很多坑在里面，下面先介绍一下常用的时间系统。

### 格林尼治时间 GMT
格林尼治时间是指位于英国伦敦郊区的皇家格林尼治天文台当地的标准时间，因为本初子午线被定义为通过那里的经线。由于地球每天的自转是有些不规则的，而且正在缓慢减速，因此格林尼治时间基于天文观测本身的缺陷，已经不再被作为标准时间使用。现在的标准时间，是由原子钟报时的协调世界时（UTC）来决定。

> [格林尼治标准时间-维基百科](https://zh.wikipedia.org/wiki/%E6%A0%BC%E6%9E%97%E5%B0%BC%E6%B2%BB%E6%A8%99%E6%BA%96%E6%99%82%E9%96%93)

### 协调世界时 UTC
协调世界时是最主要的世界时间标准，其以原子时秒长为基础。它与0度经线的平太阳时相差不超过1秒，并不遵守夏令时。协调世界时是最接近格林威治标准时间的几个替代时间系统之一，也是我们系统中主要使用的一个时间系统。
理论时区上以被15整除的子午线为中心，向东西两侧延伸7.5°，每15°为一个时区，这是理论时区。所以每差一个时区理论相差一个小时。东边的时区比西边的时区早，所以引入了[国际日期变更线](https://zh.wikipedia.org/wiki/%E5%9B%BD%E9%99%85%E6%97%A5%E6%9C%9F%E5%8F%98%E6%9B%B4%E7%BA%BF)的概念。实际上为了避开国界线，时区的形状并不规则，又会以国家内部行政分界线划分，这是实际时区。在我国横跨四个理论时区，实际统一使用东八区（UTC+8）为实际时区。
![](/resource/img/15143912170273.jpg)
时区的具体表示方式请移步 [时区-维基百科](https://zh.wikipedia.org/wiki/%E6%97%B6%E5%8C%BA)

### UNIX时间
UNIX时间或称POSIX时间，是UNIX或类UNIX系统使用的时间表示方式：从协调世界时1970年1月1日0时0分0秒起至现在的总秒数，不考虑闰秒。
UNIX时间也就是我们常说的时间戳，也是系统中常用的一种时间表示方式。它全球唯一，当我们将时间戳转换成协调世界时的时候是零时区的时间加上对应时区的时差得出的协调世界时。

### 夏令时
先放维基百科解释 [夏时制-维基百科](https://zh.wikipedia.org/wiki/%E5%A4%8F%E6%97%B6%E5%88%B6)
是一种为了节约能源而认为规定的地方时间制度。

## Python 处理时间

说完了时间的一些表示方法，下面来说说 Python 有哪些处理时间的模块，以及整理了一些各异的时间处理函数。


### time 模块


### datetime 模块


### calendar 模块
```
import calendar

#返回指定年的某月
def get_month(year, month):
    return calendar.month(year, month)

#返回指定年的日历
def get_calendar(year):
    return calendar.calendar(year)

#判断某一年是否为闰年，如果是，返回True，如果不是，则返回False
def is_leap(year):
    return calendar.isleap(year)

#返回某个月的weekday的第一天和这个月的所有天数
def get_month_range(year, month):
    return calendar.monthrange(year, month)

#返回某个月以每一周为元素的序列
def get_month_calendar(year, month):
    return calendar.monthcalendar(year, month)
```

### arrow 库

pip 安装就好了，Python中最好用的时间处理库了。

[官方文档](http://arrow.readthedocs.io/en/latest/)

[crsmithdev_arrow_ Better dates & times for Python - github](https://github.com/crsmithdev/arrow/)

