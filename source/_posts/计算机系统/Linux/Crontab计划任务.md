---
title: Crontab计划任务
date: 2015-06-12
tags: Crontab
id: 1
---

编辑 Crontab 文件： `crontab -e`

查看 Crontab 日志： `tail -100f /var/log/cron`

基本格式 :

![Crontab](/resource/img/crontab.png)

`*　　*　　*　　*　　*　　command`

分　时　日　月　周　命令

第1列表示分钟1～59 每分钟用*或者 */1表示
第2列表示小时1～23（0表示0点）
第3列表示日期1～31
第4列表示月份1～12
第5列标识号星期0～6（0表示星期天）
第6列要运行的命令

## Crontab文件的一些例子：

`30 21 * * * /usr/local/etc/rc.d/lighttpd restart`
上面的例子表示每晚的21:30重启apache

`45 4 1,10,22 * * /usr/local/etc/rc.d/lighttpd restart`
上面的例子表示每月1、10、22日的4 : 45重启apache

`10 1 * * 6,0 /usr/local/etc/rc.d/lighttpd restart`
上面的例子表示每周六、周日的1 : 10重启apache

`0,30 18-23 * * * /usr/local/etc/rc.d/lighttpd restart`
上面的例子表示在每天18 : 00至23 : 00之间每隔30分钟重启apache

`0 23 * * 6 /usr/local/etc/rc.d/lighttpd restart`
上面的例子表示每星期六的11 : 00 pm重启apache

`* */1 * * * /usr/local/etc/rc.d/lighttpd restart`
每一小时重启apache

`* 23-7/1 * * * /usr/local/etc/rc.d/lighttpd restart`
晚上11点到早上7点之间，每隔一小时重启apache

`0 11 4 * mon-wed /usr/local/etc/rc.d/lighttpd restart`
每月的4号与每周一到周三的11点重启apache

`0 4 1 jan * /usr/local/etc/rc.d/lighttpd restart`
一月一号的4点重启apache

## 遇到的坑

`* 1 * * *` 这样写的话会每天1点的每分钟执行一次，需要写成 `0 1 * * *` 这样的形式