---
title: MySQL锁优化
date: 2017-12-14
tags: MySQL
id: 1
---

## MySQL 锁表种类
常见的有行锁和表锁。表锁会锁住整张表，并发能力弱，开发中要避免使用表级锁。行锁只将单行数据锁住，锁数据期间对其它行数据不影响，并发能力高，一般使用行锁来处理并发事务。MySQL是如何加不同类型的锁的？对于加锁数据的筛选条件，有其对应的索引建立，MySQL可以快速定位的数据进行行级加锁；而对于没有索引的情况，MySQL 的做法是会先锁住整张表，然后再去获取数据，然后将不满足条件的数据锁释放掉。

## 等待锁超时问题
*Lock wait timeout exceeded; try restarting transaction*一种情况是因为有操作语句对整个表加锁了，这里发现的例子是在开启事务做 UPDATE 更新时发现的，UPDATE 条件如果不是主键或者没有索引则会锁整张表，只有以主键为条件或完全匹配的唯一索引做更新才是行级锁。
还有就是另一个事务中持有锁时间过长导致。

```SELECT * FROM INNODB_TRX;  // 查看事务表锁状态
// 创建事务，更新语句，但是不提交SET SESSION AUTOCOMMIT=off;BEGIN;UPDATE tabl1 SET status=1 WHERE expired_at <123456 AND expired_at >= 12346 AND `status` = 0;
```这时候再去提交则会报等待锁超时问题。
> http://www.toniz.net/?p=556加行锁的注意事项：
> http://blog.csdn.net/u014453898/article/details/56068841
## 插入语句死锁问题在 INSERT 语句中出现 *Deadlock found when trying to get lock; try restarting transaction* 是因为范围匹配加锁是对索引页加锁了，导致其它事务插入数据时报死锁。处理办法是查询改成行锁，以 ID 或唯一索引加锁。

> 这里需要强调的是尽量避免使用范围加锁。最好是通过主键加行锁处理。


## 避免加锁失败和发生死锁的注意事项
1. 减少锁占用时间，避免拿锁时做过多耗时操作。2. 加锁条件需对应加索引，尽量为行级锁。3. 避免死锁需要再开启事务后一次将所需资源加锁，处理后及时 COMMIT 释放锁。4. 对于请求的网络资源，首先将所需外部资源准备好。* 对于开启事物后加锁，只有 COMMIT 后方可释放锁* 在捕获异常中的处理，在捕获异常后要记得 ROLLBACK* 等待锁超时时间一般设置在 1-2 秒时间 `SET innodb_lock_wait_timeout=1`。

