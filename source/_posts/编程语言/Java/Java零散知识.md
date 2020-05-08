---
title: Java 零散知识
date: 2018-02-21
tags: Java
id: 1
---
零散整理，复习知识点。


## HashMap 实现原理
![](/resource/img/15618701610818.jpg)

Java 8 中，HashMap 是由哈希数组+链表+红黑树组成的，也就是哈希数组、哈希表、链表散列，意思就是数组不是紧密排列的。每个数组元素对应一种不同的hash值，但是不同的hash值可能会映射到数组的同一下标（即哈希冲突）。因为
```
n = tab.length
tab[i = (n - 1) & hash]
```
put(K key,V value)方法：添加键值对key-value，如果存在键key，则value覆盖oldValue，并返回oldValue。先通过键key，利用哈希函数hashCode()等操作，获取hash值，然后根据hash值得到映射到数组的下标，再判断key键是不是存在此下标中。
两个对象的hashCode相同，equals不一定相同;两个对象equals相同，hashCode一定相同。所以，重写equals()方法，一定要重写hashCode()方法。

get(Object key)方法：返回键key对应的value值，如果不存在键key，返回null。
以上两个方法都是找key，然后就直接获得附加的value值了。

https://blog.csdn.net/laoxingyao/article/details/81252977

## Java clone
https://blog.csdn.net/zhangjg_blog/article/details/18369201

## 抽象类\抽象方法
https://blog.csdn.net/qq_33567641/article/details/80986235

## Optional 使用

```
Optional.ofNullable(entities)
                .orElse(Collections.emptyList())
                .stream()
                .map(this::copyValueFromEntity2Dto)
                .collect(Collectors.toList());
```

##IntStream迭代索引

```
 Map<String, Boolean> retMap = IntStream.range(0, skuList.size())
                .mapToObj(i -> Pair.of(skuList.get(i).getSkuId(), purchased.get(i)))
                .collect(Collectors.toMap(Pair::getLeft, Pair::getRight));
```

## POJO

POJO（Plain Ordinary Java Object）简单的Java对象，实际就是普通JavaBeans，是为了避免和EJB混淆所创造的简称。使用POJO名称是为了避免和EJB混淆起来, 而且简称比较直接. 其中有一些属性及其getter setter方法的类,没有业务逻辑，有时可以作为VO(value -object)或dto(Data Transform Object)来使用.当然,如果你有一个简单的运算属性也是可以的,但不允许有业务方法,也不能携带有connection之类的方法。

## 函数接口

```
import java.util.function.*;
BiConsumer<T, U>
Function<T, R>
BiFunctionM<T, R, U>
@FunctionalInterface
```
https://www.ibm.com/developerworks/cn/java/j-java8idioms7/index.html

Supplier<T> 接收一个函数，返回值类型为 T
```
public void abc(Supplier<T> fun){
    fun.get();
}
abc(Class1::func1);
```

##Jackson - Annotations

@JsonIgnore 注解用来忽略某些字段，可以用在Field或者Getter方法上，用在Setter方法时，和Filed效果一样。这个注解只能用在POJO存在的字段要忽略的情况，不能满足现在需要的情况。
@JsonIgnoreProperties(ignoreUnknown = true)，将这个注解写在类上之后，就会忽略类中不存在的字段，可以满足当前的需要。这个注解还可以指定要忽略的字段。
@JsonInclude 该注解也是放在类名上面，作用是忽略类中字段值为null的当接收的时候。

## Mock\Stub

Mock 测试就是在测试过程中，对于某些不容易构造或者不容易获取比较复杂的对象，用一个虚拟的对象来创建以便测试的测试方法。
Mock 与 Stub 的区别?
https://yanbin.blog/mockito-how-to-mock-void-method/#more-7748

## EventBus

EventBus 是Google.Guava提供的消息发布-订阅类库，它实现了观察者设计模式，消息通知负责人通过EventBus去注册/注销观察者，最后由消息通知负责人给观察者发布消息。由于EventBus是将消息队列放入到内存中的，listener消费这个消息队列，故系统重启之后，保存或者堆积在队列中的消息丢失。


## lombok

@Data ：注解在类上；提供类所有属性的 getting 和 setting 方法，此外还提供了equals、canEqual、hashCode、toString 方法。
@Setter：注解在属性上；为属性提供 setting 方法。
@Getter：注解在属性上；为属性提供 getting 方法。
@Builder：构造一个实例，属性不需要单独 Set。

```
import lombok.Data;
import lombok.Builder;
@Data
@Builder
public class ReportReqDto {
    private String id;
    private Integer age;
    private String name;
}
ReportReqDto.builder().id("1234312312313").age(12).name("test");
```
```
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AbelDeliveryRequestDto {
    private long memberId;
    private String skuId;
    private int quantity;
    private String extra;
    private boolean anonymous;
    private Map<String, String> params = new HashMap<>();
}
```

Maven 配置：

```
<dependency>
    <groupId>org.projectlombok</groupId>
    <artifactId>lombok</artifactId>
    <version>1.16.10</version>
</dependency>
```

