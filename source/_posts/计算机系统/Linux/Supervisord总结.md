---
title: Supervisord总结
date: 2015-08-07
tags: supervisord
id: 1
---

## 常用命令

一、添加好配置文件后
二、更新新的配置到supervisord
`supervisorctl update`
三、重新启动配置中的所有程序
`supervisorctl reload`
四、启动某个进程(program_name=你配置中写的程序名称)
`supervisorctl start program_name`
五、查看正在守候的进程
`supervisorctl`
六、停止某一进程 (program_name=你配置中写的程序名称)
`pervisorctl stop program_name`
七、重启某一进程 (program_name=你配置中写的程序名称)
`supervisorctl restart program_name`
八、停止全部进程
`supervisorctl stop all`
注意：显示用stop停止掉的进程，用reload或者update都不会自动重启。

supervisord : supervisor的服务器端部分，启动supervisor就是运行这个命令。
supervisorctl：启动supervisor的命令行窗口。

--------------------

需求：redis-server这个进程是运行redis的服务。我们要求这个服务能在意外停止后自动重启。

## 安装（Centos）

```
yum install python-setuptools
easy_install supervisor
```

测试是否安装成功： 
`echo_supervisord_conf`

创建配置文件：
`echo_supervisord_conf > /etc/supervisord.conf`

修改配置文件，在supervisord.conf最后增加：
```
[program:redis]
command = redis-server   //需要执行的命令
autostart=true    //supervisor启动的时候是否随着同时启动
autorestart=true   //当程序跑出exit的时候，这个program会自动重启
startsecs=3  //程序重启时候停留在runing状态的秒数
```

环境变量配置：

`environment=PATH="/usr/local/cuda-8.0/bin:/usr/local/cuda-8.0/lib64",LD_LIBRARY_PATH="/usr/local/cuda-8.0/lib64:$LD_LIBRARY_PATH"`

> 更多配置说明请参考：http://supervisord.org/configuration.html


运行命令：
```
supervisord    //启动supervisor
supervisorctl   //打开命令行
```

```
[root@vm14211 ~]# supervisorctl
redis                            RUNNING    pid 24068, uptime 3:41:55
```

```
ctl中： help   //查看命令 
ctl中： status  //查看状态
```

## 遇到的问题
 
1. redis出现的不是running而是FATAL 状态
应该要去查看log
log在/tmp/supervisord.log

2. 日志中显示： 
gave up: redis entered FATAL state, too many start retries too quickly
修改redis.conf的daemonize为no
> 具体说明：http://xingqiba.sinaapp.com/?p=240

事实证明webdis也有这个问题，webdis要修改的是webdis.json这个配置文件

## 参考
> http://www.cnblogs.com/yjf512/archive/2012/03/05/2380496.html