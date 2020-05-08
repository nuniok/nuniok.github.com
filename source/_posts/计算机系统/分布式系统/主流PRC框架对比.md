---
title: 主流PRC框架对比
date: 2017-07-25
tags: RPC
id: 1
---


PRC 是指远程过程调用。即不同服务之间通过网络来表达调用的语义和传达数据。

#### PRC 解决的问题

* 解决通讯问题，一般通过 TCP 、 HTTP 连接来实现传输。
* 解决寻址问题。
* 实现技术异构。

#### RPC 的调用过程
![RPC调用过程](/resource/img/rpc_call_process.png)

#### PRC 框架有哪些？

* Thrift (Fackbook开源)
* gRPC (Google开源)
* hsf/dubbo (阿里开源)
* finagle (Twitter开源)

我们如何选择一款合适的 RPC 框架。从实现技术异构的角度要支持夸语言的调用，并且在高并发的请求下能有很好的性能表现。



