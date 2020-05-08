---
title: SHH打洞配置
date: 2018-01-07
tags: Ubuntu
id: 2
---

拿三台机器举例打洞配置讲解


| 机器 | 网络环境 | 用途 | SSH服务 |
| --- | --- | --- | --- |
| A机器 | 公网IP固定 | 中转机器 | 需要 |
| B机器 | NAT网络 | 被访问机器 | 需要 |
| C机器 | 任意网络环境 | 需要访问B机器 | 不需要 |


## 自动连接重试

需要B机器向A机器建立 SSH 反向隧道，命令如下：

`autossh -p 22 -M 6777 -NR '*:6766:127.0.0.1:22' usera@a.site`

通过 `autossh` 可以实现连接失败自动重连，`*:6766:127.0.0.1:22` 是将A机器的6766端口转发到B机器的22端口，`usera@a.site` 是请求B机器的用户名和地址。

## 打洞

开启端口转发功能，编辑 sshd 的配置文件 /etc/ssh/sshd_config，增加配置：
`GatewayPorts yes`

## 另一台机器连接

通过C机器对A机器的6766端口发起连接就会自动被转发到B机器。

`ssh -p 6766 userb@a.site`


## SSH 私钥认证

把请求机器的 ~/.ssh/id_rsa.pub 添加到被请求机器的 ~/.ssh/authorzied_keys 文件中

同时设置文件权限为 `chmod 600 ~/.ssh/authorzied_keys`

设置后在连接机器的时候就不需要密码了，可以走私钥认证。

## 守护进程

这里通过 supervisord 配置保证B机器重启后 autossh 能启动。

## 有固定公网IP的机器

这里我选用的是阿里云的机器，因为平时用的量不大，所以选择按量付费就可以了，看了下费用大概 80RMB/月。

## 参考：
> http://blog.csdn.net/lidongshengajz/article/details/73482908
> https://linux.cn/article-5975-1.html

