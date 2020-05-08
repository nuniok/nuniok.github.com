---
title: Ubuntu配置SMB服务
date: 2018-01-06
tags: Ubuntu
id: 1
---

## 安装samba

`sudo apt-get install samba`

## 添加用户

添加 smb 服务的用户名密码

`sudo smbpasswd -a xyz`

## 配置

编辑/etc/samba/smb.conf文件，在最后加上如下内容

```
[xyz]
   comment = xyz's Home
   path = /home/Doucument
   browseable = yes
   read only = no
   guest ok = no
   create mask = 0600
```

## 重启服务

`sudo /etc/init.d/samba restart`
