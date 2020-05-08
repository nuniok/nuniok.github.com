---
title: JVM 类加载机制
date: 2020-04-06
tags: JVM
id: 1
---

Java 类从源码到实例化对象需要经历几个过程

1. 编写Java源码（.java文件）
2. 编译成Java字节码（.class文件）
3. 类加载器读取字节码转换成java.lang.Class实例
4. JVM 通过 newInstance 等方法创建真正对象


ClassLoader 是 Java 最基本的类加载器，用来实例化不同的类对象。Java类的来源可以有内部自带的核心类`$JAVA_HOME/jre/lib/`，核心扩展类`$JAVA_HOME/jre/lib/ext`，动态远程加载的`.class`文件，分别由不同的 ClassLoader 来协作加载。

![](/resource/img/2020-04-05-23-58-25.png)

