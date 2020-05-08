---
title: 关于Java的最初了解
date: 2017-03-15
tags: Java
id: 1
---

## Apache Maven

Maven 是一个项目管理和构建自动化工具。但是对于我们程序员来说，我们最关心的是它的项目构建功能，它可以规定项目的文件结构，比如下面：


| 目录 | 目的 |
| --- | --- |
| ${basedir} | 存放 pom.xml和所有的子目录 |
| ${basedir}/src/main/java | 项目的 java源代码 |
| ${basedir}/src/main/resources | 项目的资源，比如说 property文件 |
| ${basedir}/src/test/java | 项目的测试类，比如说 JUnit代码 |
| ${basedir}/src/test/resources | 测试使用的资源 |

## Spring Boot

Spring Boot 是一个轻量级框架，Spring Boot 的目的是提供一组工具，以便快速构建容易配置的 Spring 应用程序。

## Apache Tomcat

Tomcat是由Apache软件基金会下属的Jakarta项目开发的一个Servlet容器，实现了对Servlet和JavaServer Page（JSP）的支持，并提供了作为Web服务器的一些特有功能，如Tomcat管理和控制平台、安全域管理和Tomcat阀等。由于Tomcat本身也内含了一个HTTP服务器，它也可以被视作一个单独的Web服务器。Apache Tomcat包含了一个配置管理工具，也可以通过编辑XML格式的配置文件来进行配置。


## Hibernate

是一种Java语言下的对象关系映射解决方案。Hibernate不仅负责从Java类到数据库表的映射（还包括从Java数据类型到SQL数据类型的映射），还提供了面向对象的数据查询检索机制，从而极大地缩短了手动处理SQL和JDBC上的开发时间。

## Spring web MVC

框架提供了模型-视图-控制的体系结构和可以用来开发灵活、松散耦合的 web 应用程序的组件。MVC 模式导致了应用程序的不同方面(输入逻辑、业务逻辑和 UI 逻辑)的分离，同时提供了在这些元素之间的松散耦合。

