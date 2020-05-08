---
title: Raft 算法摘要
date: 2020-04-14
tags: 分布式系统
id: 1
---


## 算法概述

Raft 算法是解决分布式系统一致性问题的，与 Paxos 实现的功能相同，相对来说更容易实现和理解。这些一致性协议可以保证在集群中大部分节点（半数以上节点）可用的情况下，集群依然可以工作并给出一个正确的结果。
Raft 将一致性问题分解为多个子模块解决：

* Leader 选举 Leader election
* 日志同步 log replication
* 安全性 safety
* 日志压缩 log compaction
* 成员变更 membership change

Raft 将系统中的角色分为：

* Leader 接受客户端请求，并且向 Follower 同步请求日志，当日志同步到大多数节点上后告诉 Follower 提交日志。
* Follower 接受并持久化 Leader 同步的日志，在 Leader 通知可以提交后提交日志。
* Candidate 是选举过程中的临时角色。

![](/resource/img/2020-04-23-00-00-46.png)


Raft 要求系统在任何一个时刻最多只有一个 Leader，正常工作期间只有 Leader 和 Follower。
Raft 算法角色状态转换如下：

![](/resource/img/2020-04-23-00-00-58.png)

Follower 只响应其它服务器的请求，如果 Flower 超时没有接受到 Leader 的消息，它会成为一个 Candidate 状态并开始一次 Leader 选举，收到大多数服务器投票的 Candidate 会成为新的 Leader，Leader 在宕机之前会一直保持 Leader 状态。

![](/resource/img/2020-04-23-00-01-09.png)

Raft 算法将时间分为一个个的任期 term，每一个 term 的开始都是 Leader 选举，在成功选举 Leader 之后，Leader 会在整个 term 内管理整个集群，如果 Leader 选举失败，这个 term 就会因为没有 Leader 而结束。

## Leader 选举(Leader election)

Raft 使用心跳触发 Leader 选举。当服务器启动时，初始化为 Follower。Leader 向所有 Follower 周期性发送 heartbeat。如果 Follower 选举超时，会等待一段随机时间后再发起一次 Leader选举。选举出 Leader 后，会定期向所有 Follower 发送 heartbeat 维持状态，如果 Follower 一段时间没有收到心跳则认为 Leader 已经挂了，再次发起Leader选举过程。

![](/resource/img/2020-04-23-00-01-17.png)

## 日志复制 (log replication)

Leader 选举出来后，就开始接收客户端的请求，把日志条目加入到日志处理中，然后并行的向其它服务器发起请求复制日志条目。当这条日志被复制到大多数服务器中，Leader会把这条日志状态改变向客户端返回执行结果。

![](/resource/img/2020-04-23-00-01-29.png)

如果某个Follower没有复制成功，则Leader会无限的重试直到Follower最终存储了所有的日志条目。日志由有序编号和日志条目组成，每条日志条目包含它被创建时的任期号 term，和用于状态机执行的命令。

![](/resource/img/2020-04-23-00-01-37.png)


## 安全性 (safety)

Raft增加两条极限值来保证安全性：
1. 拥有最新已提交的log entry 的 Follower 才有资格成为 Leader
2. Leader只能推进commit index 来提交当前term的已经复制到大多数节点上的日志，旧的term日志会跟随当前term的日志来间接提交。

![](/resource/img/2020-04-23-00-01-48.png)


## 日志压缩 (log compaction)

通过定期记录 snapshot 来解决，每个副本独立的对自己系统状态进行snapshot，并且是已提交的日志进行。snapshot 包含日志元数据，最后一条已提交的 log entry 的 log index 和 term。Leader会发送snapshot给最后日志太多的Follower，或者新加入的机器。
copy-on-write https://blog.csdn.net/u012501054/article/details/90241124
做一次snapshot可能耗时过长，会影响正常日志同步。可以通过使用copy-on-write技术避免snapshot过程影响正常日志同步。

## 成员变更 (membership change)

不同节点之间同步成员变更存在间隙，会导致一致性问题。Raft提出两阶段成员变更方法，集群从旧成员配置切换过度成员配置，叫做共同一致，是指旧成员配置和新成员配置组合，一旦共同一致被提交，系统再切换到新成员配置。

![](/resource/img/2020-04-23-00-02-00.png)

Raft与Multi-Paxos的不同：

![](/resource/img/2020-04-23-00-02-07.png)


## QA

![](/resource/img/如果.png)

![](/resource/img/2020-04-23-00-03-28.png)


> https://zhuanlan.zhihu.com/p/32052223
