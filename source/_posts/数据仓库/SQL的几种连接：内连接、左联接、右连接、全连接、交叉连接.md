---
title: SQL的几种连接：内连接、左联接、右连接、全连接、交叉连接
date: 2014-10-16
tags: SQL
id: 1
---

SQL连接可以分为内连接、外连接、交叉连接。
 
数据库数据：
![book表](/resource/img/sql/SQL01.png)
![stu表](/resource/img/sql/SQL02.png)
 
## 内连接

* 等值连接：在连接条件中使用等于号(=)运算符比较被连接列的列值，其查询结果中列出被连接表中的所有列，包括其中的重复列。
* 不等值连接：在连接条件使用除等于运算符以外的其它比较运算符比较被连接的列的列值。这些运算符包括>、>=、<=、<、!>、!<和<>。
* 自然连接：在连接条件中使用等于(=)运算符比较被连接列的列值，但它使用选择列表指出查询结果集合中所包括的列，并删除连接表中的重复列。

内连接：内连接查询操作列出与连接条件匹配的数据行，它使用比较运算符比较被连接列的列值。
`select * from book as a,stu as b where a.sutid = b.stuidselect * from book as a inner join stu as b on a.sutid = b.stuid`

内连接可以使用上面两种方式，其中第二种方式的inner可以省略。

![stu表](/resource/img/sql/SQL03.png)

其连接结果如上图，是按照a.stuid = b.stuid进行连接。

## 外连接

* 左联接：是以左表为基准，将a.stuid = b.stuid的数据进行连接，然后将左表没有的对应项显示，右表的列为NULL
`select * from book as a left join stu as b on a.sutid = b.stuid`

![stu表](/resource/img/sql/SQL04.png)

* 右连接：是以右表为基准，将a.stuid = b.stuid的数据进行连接，然以将右表没有的对应项显示，左表的列为NULL
`select * from book as a right join stu as b on a.sutid = b.stuid`

![stu表](/resource/img/sql/SQL05.png)

* 全连接：完整外部联接返回左表和右表中的所有行。当某行在另一个表中没有匹配行时，则另一个表的选择列表列包含空值。如果表之间有匹配行，则整个结果集行包含基表的数据值。
`select * from book as a full outer join stu as b on a.sutid = b.stuid`

![stu表](/resource/img/sql/SQL06.png)
 
## 交叉连接
交叉连接：交叉联接返回左表中的所有行，左表中的每一行与右表中的所有行组合。交叉联接也称作笛卡尔积。
`select * from book as a cross join stu as b order by a.id`

![stu表](/resource/img/sql/SQL07.png)