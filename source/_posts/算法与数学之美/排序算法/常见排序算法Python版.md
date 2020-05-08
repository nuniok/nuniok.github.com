---
title: 常见排序算法Python版
date: 2015-03-08
tags: 排序算法
id: 1
---

平均时间复杂度均为O(n^2)的排序算法：

## 插入排序
```
# -*- coding:utf-8 -*-
# 插入排序，两层遍历，以一个位置为基准，不断向前遍历，将比基准位置大的数调整到基准位置。
def insertion_sort(sort_list):
    iter_len = len(sort_list)
    if iter_len < 2:
        return sort_list
    for i in range(1, iter_len):
        key = sort_list[i]
        j = i - 1
        while j>=0 and sort_list[j]>key:
            sort_list[j+1] = sort_list[j]
            j -= 1
        sort_list[j+1] = key
    return sort_list
if __name__ == "__main__":
    sort_list = [4,2,7,3,1,9,33,25,46,21,45,22]
    print sort_list
    print insertion_sort(sort_list)
```


## 冒泡排序
```
def bubble_sort(sort_list):
    iter_len = len(sort_list)
    if iter_len < 2:
        return sort_list
    for i in range(iter_len-1):
        for j in range(iter_len-i-1):
            if sort_list[j] > sort_list[j+1]:
                sort_list[j], sort_list[j+1] = sort_list[j+1], sort_list[j]
    return sort_list
if __name__ == "__main__":
    sort_list = [4,2,7,3,1,9,33,25,46,21,45,22]
    print sort_list
    print bubble_sort(sort_list)
```


## 选择排序
```
# -*- coding:utf-8 -*-
# 向后遍历，选择最小值进行交换。
def selection_sort(sort_list):
    iter_len = len(sort_list)
    if iter_len < 2:
        return sort_list
    for i in range(iter_len-1):
        smallest = sort_list[i]
        location = i
        for j in range(i, iter_len):
            if sort_list[j] < smallest:
                smallest = sort_list[j]
                location = j
        if i != location:
            sort_list[i], sort_list[location] = sort_list[location], sort_list[i]
    return sort_list
if __name__ == "__main__":
    sort_list = [4,2,7,3,1,9,33,25,46,21,45,22]
    print sort_list
    print selection_sort(sort_list)
```

## 归并排序
```
class Merge_sort(object):
    def _merge(self, alist, p, q, r):
        left = alist[p:q+1]
        right = alist[q+1:r+1]
        for i in range(p, r+1):
            if len(left)>0 and len(right)>0:
                if left[0]<=right[0]:
                    alist[i] = left.pop(0)
                else:
                    alist[i] = right.pop(0)
            elif len(right)==0:
                alist[i] = left.pop(0)
            elif len(left)==0:
                alist[i] = right.pop(0)
 
    def _merge_sort(self, alist, p, r):
        if p<r:
            q = int((p+r)/2)
            self._merge_sort(alist, p, q)
            self._merge_sort(alist, q+1, r)
            self._merge(alist, p, q, r)
 
    def __call__(self, sort_list):
        self._merge_sort(sort_list, 0, len(sort_list)-1)
        return sort_list
if __name__ == "__main__":
    sort_list = [4,2,7,3,1,9,33,25,46,21,45,22]
    print sort_list
    merge = Merge_sort()
    print merge(sort_list)
```

## 堆排序
堆排序，是建立在数据结构——堆上的。关于堆的基本概念、以及堆的存储方式这里不作介绍。这里用一个列表来存储堆（和用数组存储类似），对于处在i位置的元素，2*i+1位置上的是其左孩子，2*i+2是其右孩子，类似得可以得出该元素的父元素。 
首先我们写一个函数，对于某个子树，从根节点开始，如果其值小于子节点的值，就交换其值。用此方法来递归其子树。接着，我们对于堆的所有非叶节点，自下而上调用先前所述的函数，得到一个树，对于每个节点（非叶节点），它都大于其子节点。（其实这是建立最大堆的过程）在完成之后，将列表的头元素和尾元素调换顺序，这样列表的最后一位就是最大的数，接着在对列表的0到n-1部分再调用以上建立最大堆的过程。最后得到堆排序完成的列表。


## 快速排序
首先要用到的是分区工具函数（partition），对于给定的列表（数组），我们首先选择基准元素（这里我选择最后一个元素），通过比较，最后使得该元素的位置，使得这个运行结束的新列表（就地运行）所有在基准元素左边的数都小于基准元素，而右边的数都大于它。然后我们对于待排的列表，用分区函数求得位置，将列表分为左右两个列表（理想情况下），然后对其递归调用分区函数，直到子序列的长度小于等于1。
```
class Quick_sort(object):
    def _partition(self, alist, p, r):
        i = p-1
        x = alist[r]
        for j in range(p, r):
            if alist[j]<=x:
                i += 1
                alist[i], alist[j] = alist[j], alist[i]
        alist[i+1], alist[r] = alist[r], alist[i+1]
        return i+1
 
    def _quicksort(self, alist, p, r):
        if p<r:
            q = self._partition(alist, p, r)
            self._quicksort(alist, p, q-1)
            self._quicksort(alist, q+1, r)
 
    def __call__(self, sort_list):
        self._quicksort(sort_list, 0, len(sort_list)-1)
        return sort_list
if __name__ == "__main__":
    sort_list = [4,2,7,3,1,9,33,25,46,21,45,22]
    print sort_list
    quick = Quick_sort()
    print quick(sort_list)
```

Python对于递归深度做了限制，默认值为1000，可以通过设置修改深度。
```
import sys
sys.setrecursionlimit(99999)
```
另外一种是随机化分区函数。由于之前我们的选择都是子序列的最后一个数，因此对于特殊情况的健壮性就差了许多。现在我们随机从子序列选择基准元素，这样可以减少对特殊情况的差错率。
```
import random
class Random_quick_sort(object):
    
    def _randomized_partition(self, alist, p, r):
        i = random.randint(p, r)
        alist[i], alist[r] = alist[r], alist[i]
        return self._partition(alist, p, r)
    def _partition(self, alist, p, r):
        i = p-1
        x = alist[r]
        for j in range(p, r):
            if alist[j]<=x:
                i += 1
                alist[i], alist[j] = alist[j], alist[i]
        alist[i+1], alist[r] = alist[r], alist[i+1]
        return i+1
    def _quicksort(self, alist, p, r):
        if p<r:
            q = self._randomized_partition(alist, p, r)
            self._quicksort(alist, p, q-1)
            self._quicksort(alist, q+1, r)
 
    def __call__(self, sort_list):
        self._quicksort(sort_list, 0, len(sort_list)-1)
        return sort_list
if __name__ == "__main__":
    sort_list = [4,2,7,3,1,9,33,25,46,21,45,22]
    print sort_list
    random_quick = Random_quick_sort()
    print random_quick(sort_list)
```

## Python风格快速排序算法
```
def quick_sort_2(sort_list):
    if len(sort_list)<=1:
        return sort_list
    return quick_sort_2([lt for lt in sort_list[1:] if lt<sort_list[0]]) + \
           sort_list[0:1] + \
           quick_sort_2([ge for ge in sort_list[1:] if ge>=sort_list[0]])
if __name__ == "__main__":
    sort_list = [4,2,7,3,1,9,33,25,46,21,45,22]
    print sort_list
    print quick_sort_2(sort_list)
```

## 计数排序
计数排序的基本思想是对于给定的输入序列中的每一个元素x，确定该序列中值小于x的元素的个数。一旦有了这个信息，就可以将x直接存放到最终的输出序列的正确位置上。例如，如果输入序列中只有17个元素的值小于x的值，则x可以直接存放在输出序列的第18个位置上。当然，如果有多个元素具有相同的值时，我们不能将这些元素放在输出序列的同一个位置上，因此，上述方案还要作适当的修改。
假设输入的线性表L的长度为n，L=L1,L2,..,Ln；线性表的元素属于有限偏序集S，|S|=k且k=O(n)，S={S1,S2,..Sk}；则计数排序可以描述如下：
1、扫描整个集合S，对每一个Si∈S，找到在线性表L中小于等于Si的元素的个数T(Si)；
2、扫描整个线性表L，对L中的每一个元素Li，将Li放在输出线性表的第T(Li)个位置上，并将T(Li)减1。
```
class Counting_sort(object):
    def _counting_sort(self, alist, k):
        alist3 = [0 for i in range(k)]
        alist2 = [0 for i in range(len(alist))]
        for j in alist:
            alist3[j] += 1
        for i in range(1, k):
            alist3[i] = alist3[i-1] + alist3[i]
        for l in alist[::-1]:
            alist2[alist3[l]-1] = l
            alist3[l] -= 1
        return alist2
 
    def __call__(self, sort_list, k=None):
        if k is None:
            import heapq
            k = heapq.nlargest(1, sort_list)[0] + 1
        return self._counting_sort(sort_list, k)
if __name__ == "__main__":
    sort_list = [4,2,7,3,1,9,33,25,46,21,45,22]
    print sort_list
    counting = Counting_sort()
    print counting(sort_list)
```

排序算法用于研究其思想，具体的应用需要根据实际环境进行修改，但是要遵循以下规则。
当需要排序的时候，尽量设法使用内建Python列表的sort方法。
当需要搜索的时候，尽量设法使用内建的字典。





