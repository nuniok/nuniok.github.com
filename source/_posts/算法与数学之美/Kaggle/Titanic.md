---
title: Kaggle Titanic问题
date: 2017-01-11
tags: [分类算法, 随机森林]
id: 1
---

# Kaggle Titanic问题

#### [技能get点]

- [x] Pandas基本操作
- [√] 随机森林算法 ——> 数学原理、算法思想
- [√] kaggle竞赛的一个项目完成参与流程
- [√] 特征功能 ——> 特征提取

#### 随机森林算法


#### kaggle竞赛参与流程


#### 特征提取



```python
#! /usr/bin/python
# -*- coding:utf-8 -*-
"""
@author: abc
@file: xyzforest.py
@date: 2017-01-06
"""
__author__ = "abc"

import numpy as np
import pandas as pd
import csv
from sklearn.ensemble import RandomForestClassifier


class Titanic(object):
    """
    Titanic
    """
    def __init__(self):
        """
        __init__
        """
        self.train_path = "/home/abc/Projects/kaggle/Titanic/train.csv"
        self.test_path = "/home/abc/Projects/kaggle/Titanic/test.csv"

    def load_data(self, path):
        """
        加载数据
        :param path:
        :return:
        """
        return pd.read_csv(path, header=0)

    def wash_train_data(self, train_data):
        """
        清洗训练数据
        :param train_data:
        :return:
        """
        # PassengerId,Survived,Pclass,Name,Sex,Age,SibSp,Parch,Ticket,Fare,Cabin,Embarked
        # 性别数值化
        train_data.Sex = train_data.Sex.map({'female': 0, 'male': 1}).astype(int)

        # Embarked 数值化, 补充众数
        if len(train_data.Embarked[train_data.Embarked.isnull()]) > 0:
            train_data.Embarked[train_data.Embarked.isnull()] = train_data.Embarked.dropna().mode().values
        ports_dict = {name: index for index, name in enumerate(set(train_data.Embarked))}
        train_data.Embarked = train_data.Embarked.map(ports_dict).astype(int)

        # 年龄补充平均数
        if len(train_data.Age[train_data.Age.isnull()]) > 0:
            train_data.Age[train_data.Age.isnull()] = train_data.Age.dropna().median()

        # 删除多余字段
        train_data = train_data.drop(self.drop_label(), axis=1)

        self.data_concat(train_data)

        return train_data.values

    def wash_test_data(self, test_data):
        """
        清洗测试数据
        :param test_data:
        :return:
        """
        # PassengerId,Pclass,Name,Sex,Age,SibSp,Parch,Ticket,Fare,Cabin,Embarked
        test_data.Sex = test_data.Sex.map({'female': 0, 'male': 1}).astype(int)

        if len(test_data.Embarked[test_data.Embarked.isnull()]) > 0:
            test_data.Embarked[test_data.Embarked.isnull()] = test_data.Embarked.dropna().mode().values
        ports_dict = {name: index for index, name in enumerate(np.unique(test_data.Embarked))}
        test_data.Embarked = test_data.Embarked.map(ports_dict).astype(int)

        if len(test_data.Age[test_data.Age.isnull()]) > 0:
            test_data.Age[test_data.Age.isnull()] = test_data.Age.dropna().median()

        if len(test_data.Fare[test_data.Fare.isnull()]) > 0:
            median_fare = np.zeros(3)
            for f in range(0, 3):  # loop 0 to 2
                median_fare[f] = test_data[test_data.Pclass == f + 1]['Fare'].dropna().median()
            for f in range(0, 3):  # loop 0 to 2
                test_data.loc[(test_data.Fare.isnull()) & (test_data.Pclass == f + 1), 'Fare'] = median_fare[f]

        test_data = test_data.drop(self.drop_label(), axis=1)

        self.data_concat(test_data)

        return test_data.values

    def drop_label(self):
        """
        drop_label
        :return:
        """
        return ['Name', 'Ticket', 'PassengerId']

    def data_concat(self, raw_data):
        """
        data_concat
        :param raw_data:
        :return:
        """
        # 根据年龄优化
        raw_data.loc[raw_data.Age < 18, "Age"] = 0
        raw_data.loc[raw_data.Age >= 18, "Age"][raw_data.Age < 45] = 1
        raw_data.loc[raw_data.Age >= 45, "Age"] = 2
        # 根据父母孩子数量优化
        raw_data.loc[raw_data.Parch > 0, "Parch"] = 1
        raw_data.loc[raw_data.Cabin.isnull(), "Cabin"] = 1
        raw_data.loc[raw_data.Cabin.notnull(), "Cabin"] = 0

    def rediction_model(self, train_data, label_data, test_data):
        """
        预测模型
        :param train_data:
        :param test_data:
        :return:
        """
        forest = RandomForestClassifier(n_estimators=2000)
        forest = forest.fit(train_data, label_data)
        return forest.predict(test_data).astype(int)

    def save_result(self, path, head, data):
        """
        save_result
        :param path:
        :param head:
        :param data:
        :return:
        """
        with open(path, "wb") as wbf:
            csv_obj = csv.writer(wbf)
            csv_obj.writerow(head)
            for item in data:
                csv_obj.writerow(list(item))

    def run(self):
        """
        运行
        :return:
        """
        # 加载数据
        train_data = self.load_data(self.train_path)
        test_data = self.load_data(self.test_path)
        passenger_id = test_data.PassengerId.values
        # 清洗数据
        train_data = self.wash_train_data(train_data)
        test_data = self.wash_test_data(test_data)
        train_data, label_data = train_data[0::, 1::], [val for val in train_data[0::, 0]]
        head = ["PassengerId", "Survived"]
        data = zip(passenger_id, self.rediction_model(train_data, label_data, test_data))
        self.save_result("xyzforest.csv", head, data)

if __name__ == "__main__":
    tt = Titanic()
    print tt.run()

```

#### 参考

[pandas documentation](http://pandas.pydata.org/pandas-docs/stable/index.html)

[【原】十分钟搞定pandas](http://www.cnblogs.com/chaosimple/p/4153083.html)

[机器学习系列(3)_逻辑回归应用之Kaggle泰坦尼克之灾](http://www.cnblogs.com/zhizhan/p/5238908.html)

[Kaggle系列——Titanic 80%＋精确度纪录](http://blog.csdn.net/yobobobo/article/details/48194021)