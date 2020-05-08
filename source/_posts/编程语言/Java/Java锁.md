---
title: Java 锁相关
date: 2020-04-26
tags: Java
id: 1
---

锁解决的问题是并发操作引起的脏读、数据不一致问题。

## 基本原理

### volatile

在Java中允许线程访问共享变量，为了确保共享变量能被准确和一致的更新，线程应该确保使用排它锁来单独获得这个变量，Java中提供了 volatile，使之在多处理器开发中保证变量的可见性，当一个线程改变了共享变量，另一个线程能够及时读到这个修改的值。恰当的使用它会比 synchronized 成本更低，因为不会引起上下文的切换和调度。

### synchronized

通过锁机制实现同步，在Java中每一个对象都可以作为锁，有以下三种形式：

* 对于普通同步方法，锁的是当前实例对象。
* 对于静态同步方法，所得是当前类 class 对象。
* 对于同步方法块，锁的是括号内指定的对象。

为了减少获得锁和释放锁带来的性能消耗，Java SE 1.6 引入了偏向锁和轻量级锁。**偏向锁**的核心思想是：如果一个线程获得了锁，就进入偏向模式，当这个线程再次请求锁时，如果没有其它线程获取过该锁，无需再做任何同步操作，可以节省大量锁申请的操作，来提高性能。如果偏向锁获取失败，会通过**轻量级锁**的方式获取，如果获取成功则进入临界区，如果失败则表示有其它线程争夺到锁，当前线程锁请求会膨胀为**重量级锁**。

![](/resource/img/2020-04-26-02-05-44.png)

**锁粗化** 是指在遇到一连串连续的对同一个锁不断的进行请求和释放的操作时，会把所有的锁操作整合成对锁的一次请求，减少锁请求的同步次数。

**锁消除** 是指在编译期，通过对上下文的扫描，去除不可能存在共享资源竞争的锁。

**自旋锁** 是指在锁膨胀后，避免线程真正的在操作系统层面被挂起，通过对线程做几个空循环，以期望在这之后能获取到锁，顺利的进入临界区，如果还获取不到，则会真正被操作系统层面挂起。

![](/resource/img/2020-04-26-02-14-59.png)

### CAS

指的是比较并交换，它是一个原子操作，比较一个内存位置的值并且只有相等时修改这个内存位置的值并更新值，保证新的值总是基于最新的信息计算的。在 JVM 中 CAS 操作是利用处理器提供的 CMPXCHS 指令实现。是实现我们平时所说的自旋锁或乐观锁的核心操作。

优点是竞争小的时候使用系统开销小；对应缺点是循环时间长开销大、ABA问题、只能保证一个变量的原子操作。

#### ABA 问题

问题产生原因是两个线程处理的时间差导致，具体如下图：

![](/resource/img/2020-04-26-01-21-06.png)

解决 ABA 问题可以增加一个版本号，在每次修改值的时候增加一个版本号。

产生：

```java
private static AtomicReference<Integer> atomicReference = new AtomicReference<Integer>(100);

public static void main(String[] args) {
    new Thread(() -> {
        atomicReference.compareAndSet(100, 101);
        atomicReference.compareAndSet(101, 100);
    },"t1").start();

    new Thread(() -> {
        try {
            TimeUnit.SECONDS.sleep(1);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        System.out.println(atomicReference.compareAndSet(100, 2019) + "\t修改后的值:" + atomicReference.get());
    },"t2").start();
}
```

解决：
```java
private static AtomicStampedReference<Integer> atomicStampedReference = new AtomicStampedReference<Integer>(100,1);

public static void main(String[] args) {
    new Thread(() -> {
        System.out.println("t1拿到的初始版本号:" + atomicStampedReference.getStamp());

        //睡眠1秒，是为了让t2线程也拿到同样的初始版本号
        try {
            TimeUnit.SECONDS.sleep(1);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        atomicStampedReference.compareAndSet(100, 101,atomicStampedReference.getStamp(),atomicStampedReference.getStamp()+1);
        atomicStampedReference.compareAndSet(101, 100,atomicStampedReference.getStamp(),atomicStampedReference.getStamp()+1);
    },"t1").start();

    new Thread(() -> {
        int stamp = atomicStampedReference.getStamp();
        System.out.println("t2拿到的初始版本号:" + stamp);

        //睡眠3秒，是为了让t1线程完成ABA操作
        try {
            TimeUnit.SECONDS.sleep(3);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        System.out.println("最新版本号:" + atomicStampedReference.getStamp());
        System.out.println(atomicStampedReference.compareAndSet(100, 2019,stamp,atomicStampedReference.getStamp() + 1) + "\t当前 值:" + atomicStampedReference.getReference());
    },"t2").start();
}
```
