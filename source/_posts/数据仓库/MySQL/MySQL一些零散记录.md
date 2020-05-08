---
title: MySQL一些零散记录
date: 2017-12-17
tags: MySQL
id: 1
---

## MySQL 大小写区分问题
![](/resource/img/15135036470309.jpg)


## sql_mode 配置

Modes affect the SQL syntax MySQL supports and the data validation checks it performs. This makes it easier to use MySQL in different environments and to use MySQL together with other database servers.

### 查看当前sql_mode
```
SELECT @@GLOBAL.sql_mode;
SELECT @@SESSION.sql_mode;
```

### 设置当前sql_mode
```
SET GLOBAL sql_mode = 'modes...';
SET SESSION sql_mode = 'modes...';
```
### Full list of SQL Models

https://dev.mysql.com/doc/refman/5.7/en/sql-mode.html


## /*!40001 SQL_NO_CACHE */

`/*!  */` 这是 mysql 里的语法，并非注释，`!` 后面是版本号，如果本数据库等于或大于此版本号，那么注释内的代码也会执行。

关于这个条件的问答： https://lists.mysql.com/mysql/203373



