---
title: k近邻法
date: 2016-12-28
tags: [分类算法, KNN, kd树]
id: 1
---

简单解释：采用测量不同特征值之间距离的方法进行分类的算法。
主要优点是精度高，缺点是计算和空间负责度高，适用于数值型和标称型。
已下是通过Python实现的k-近邻算法，大致思路是计算样本数据`data_set`中的点与待分类点的距离，按距离递增排序，然后取出前K个点，计算这些点所属标签的数量，计数最高的标签为分类结果。

``` python
#! /data/server/python/bin/python
# -*- coding:utf-8 -*-
"""
k-近邻算法
"""
import math
import operator
from collections import Counter


def knn(position, data_set, labels, k):
    """
    k-近邻算法
    :param position: 待分类点
    :param data_set: 数据样本
    :param labels: 标签集合
    :param k: 取值
    :return: 所属标签
    """
    distance_list = []
    for index, item in enumerate(data_set):
        distance_list.append((
            labels[index],
            math.sqrt(reduce(operator.add, [(v - position[i]) ** 2 for i, v in enumerate(item)]))
        ))
    distance_list = sorted(distance_list, key=lambda x: x, reverse=True)
    result = Counter([val[0] for val in distance_list[:k]])
    result_labels = sorted(result.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    return result_labels[0][0]


if __name__ == "__main__":
    point = [0.2, 0.3]
    data_set = [[1, 1.1], [1, 1], [0, 0], [0, 0.1]]
    labels = ['A', 'A', 'B', 'B']
    k = 3
    print knn(point, data_set, labels, k)
```

### k-d tree算法
> http://www.cnblogs.com/eyeszjwang/articles/2429382.html

--------

**k近邻法** 给定一个训练数据集，对新输入的实例，在训练的数据集中找到与该实例最近邻的k个实例，这k个实例的多数属于某个类，就把该输入实例分为这个类。

**kd树** 是一种对k维空间中的实例点进行存储以便对其进行快速检索的树形数据结构。

##### 算法：（构造平衡kd树）
输入：k维空间数据集
$$ T={x_1,x_2,...,x_N} $$,
$$ x_i=(x_i^{(1)},x_i^{(2)},...,x_i^{(k)})^T, i=1,2,...,N; $$

输出：kd树。

##### 生成：
从深度为0的结点开始。重复对深度为j的结点，选择`x(l)`为切分的坐标轴，`l=j(mode k) + 1`，以该结点的区域中所有实例的`x(l)`坐标的中位数为切分点，将该结点对应的超矩形区域切分为两个子区域。切分由通过切分点并与坐标轴`x(l)`垂直的超平面实现。由该结点生成深度为j+1的左、右子结点：左子节点对应坐标`x(l)`小于切分点的子区域，右子节点对应坐标`x(l)`大于切分点的子区域。

##### 实例：
对以下给定二维数据集构造一个平衡kd树
$$ T= \{(2,3)^T, (5,4)^T, (9,6)^T, (4,7)^T, (8,1)^T, (7,2)^T \} $$

