---
title: Peewee源码解读
date: 2017-02-05
tags: [Peewee, Python, 源码]
id: 2
---

## 通过select查询语句引入


```python
from model.db.tb1 import Tb1
query = Tb1.select().where(Tb1.id > 0)
print "select query:", query.sql()[0] % tuple(query.sql()[1])
print "query result:"
for item in query.dicts().execute():
    print item
```

    select query: SELECT `t1`.`id`, `t1`.`name`, `t1`.`age`, `t1`.`create_time` FROM `tb1` AS t1 WHERE (`t1`.`id` > 0)
    query result:
    {'age': 12, 'create_time': datetime.datetime(2017, 2, 5, 0, 14, 6), 'id': 1, 'name': u'test'}
    {'age': 20, 'create_time': datetime.datetime(2017, 2, 5, 0, 14, 55), 'id': 2, 'name': u'zhang'}


## 分析每一次调用

![peewee_select_query](/resource/img/peewee_select_query.png)
其中`Tb1`是我们定义的一个Model
```
class Tb1(XYZ_DB.Model):
    """
    """
    id = PrimaryKeyField()
    name = CharField()
    age = IntegerField()
    create_time = DateTimeField()

    class Meta(object):

        """表配置信息
        """
        db_table = "tb1"
```
peewee对`Model`类指定`BaseModel`元类
```
class Model(with_metaclass(BaseModel)):
```

未完待续

[Jupyter Markdown](http://daringfireball.net/)
