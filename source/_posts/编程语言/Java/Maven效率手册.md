---
title: Maven 效率手册
date: 2019-07-28
tags: Java
id: 2
---

> 基于 Ubuntu 18.04.2 系统做过尝试

## 安装

```
apt-get install maven
```

## 仓库概念

![](/resource/img/15720899449087.jpg)


`~/.m2` 目录下面是存放安装包的内容缓冲.

`settings.xml` 。。。


不要使用 IDE 内嵌 Maven


## 基本命令

`mvn compile` 编译源码
`mvn package` 打包
`mvn test` 测试
`mvn clean` 清除代码
`mvn deploy` 上传到私服
`mvn install` 上传到本地仓库

`mvn -X install` 开启调试日志
`mvn -U package` 清除缓存打包
`mvn cobertura:cobertura` 单元测试覆盖率
`mvn dependency:tree` 查看依赖关系


## Maven SNAPSHOT 版本和 RELEASE 版本的区别

https://www.cnblogs.com/EasonJim/p/6852840.html

https://www.jianshu.com/p/7e8e67205b97

## Maven 依赖冲突

https://www.jianshu.com/p/b08364ce234f



