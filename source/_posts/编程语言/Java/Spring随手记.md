---
title: Spring 随手记
date: 2018-04-20
tags: Java
id: 1
---
基本记录，没有系统性整理，只是作为一个重温知识点用，不具有阅读参考价值。

![](/resource/img/15618712316175.jpg)



### 注解（Inherited）
Spring注解方式减少了配置文件内容，更加便于管理。

### MVC模块注解
@Controller ：表明该类会作为与前端作交互的控制层组件，通过服务接口定义的提供访问应用程序的一种行为，解释用户的输入，将其转换成一个模型然后将试图呈献给用户。
@RequestMapping ： 这个注解用于将url映射到整个处理类或者特定的处理请求的方法。
@RequestParam ：将请求的参数绑定到方法中的参数上，有required参数，默认情况下，required=true。
@RequestParam ：将请求的参数绑定到方法中的参数上，有required参数，默认情况下，required=true。
@RequestBody ： @RequestBody是指方法参数应该被绑定到HTTP请求Body上。
@RestController ：控制器实现了REST的API，只为服务于JSON，XML或其它自定义的类型内容，@RestController用来创建REST类型的控制器，与@Controller类型。

### 组件类注解
@Component ：表示一个带注释的类是一个“组件”，成为Spring管理的Bean。当使用基于注解的配置和类路径扫描时，这些类被视为自动检测的候选对象。同时@Component还是一个元注解。
@ComponentScan：自动扫描指定包下所有使用@Service,@Component,@Controller,@Repository的类并注册。 
@Repository：标注一个DAO组件类。 
@Service：标注一个业务逻辑组件类。 
@Controller：标注一个控制器组件类。 
@Component 可以代替 @Repository、@Service、@Controller，因为这三个注解是被 @Component 标注的。

### 装配 Bean 时常用注解
@Autowired：属于Spring 的org.springframework.beans.factory.annotation包下,可用于为类的属性、构造器、方法进行注值。
@Resource：不属于spring的注解，而是来自于JSR-250位于java.annotation包下，使用该annotation为目标bean指定协作者Bean。
@PostConstruct 和 @PreDestroy 方法 实现初始化和销毁bean之前进行的操作。

### Configuration and @Bean
使用@Configuration 来注解类表示类可以被 Spring 的 IoC 容器所使用，作为 bean 定义的资源。

### IOC
控制反转（Inversion of Control，缩写为IoC），是面向对象编程中的一种设计原则，可以用来减低计算机代码之间的耦合度。其中最常见的方式叫做依赖注入（Dependency Injection，简称DI），还有一种方式叫“依赖查找”（Dependency Lookup）。通过控制反转，对象在被创建的时候，由一个调控系统内所有对象的外界实体，将其所依赖的对象的引用传递给它。也可以说，依赖被注入到对象中。
https://zh.wikipedia.org/wiki/%E6%8E%A7%E5%88%B6%E5%8F%8D%E8%BD%AC

## Spring 通过 calss 直接获取 Bean
```
SpringApplication app = new SpringApplication(THTTPMain.class);
ApplicationContext ctx = app.run(args);
ReportManager manager = ctx.getBean(ReportManager.class);
manager.run();
```

## Spring 标签管理
https://www.cnblogs.com/wuchanming/p/5426746.html
![](/resource/img/15618712485957.jpg)


## AOP 面向切面编程
![](/resource/img/15618712585422.jpg)

