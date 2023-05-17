**一，利用标准数据库优化技术**

传统数据库优化技术博大精深，不同的数据库有不同的优化技巧，但重心还是有规则的。在这里算是题外话，挑两点通用的说说：

- 索引，给关键的字段添加索引，性能能更上一层楼，如给表的关联字段，搜索频率高的字段加上索引等。Django建立实体的时候，支持给字段添加索引，具体参考Django.db.models.Field.db_index。按照经验，Django建立实体之前应该早想好表的结构，尽量想到后面的扩展性，避免后面的表的结构变得面目全非。

- 使用适当字段类型，本来varchar就搞定的字段，就别要text类型，小细节别不关紧要，后头数据量一上去，愈来愈多的数据，小字段很可能是大问题。



##### **二 ，了解Django的QuerySets**

了解Django的QuerySets对象，对优化简单程序有至关重要的作用。QuerySets是有缓存的，一旦取出来，它就会在内存里呆上一段时间，尽量重用它。

```
# 了解缓存属性：
>>> entry = Entry.objects.get(id=1)
>>> entry.blog   # 博客实体第一次取出，是要访问数据库的
>>> entry.blog   # 第二次再用，那它就是缓存里的实体了，不再访问数据库
>>> entry = Entry.objects.get(id=1)
>>> entry.authors.all()   # 第一次all函数会查询数据库
>>> entry.authors.all()   # 第二次all函数还会查询数据库
```

- all，count exists是调用函数（需要连接数据库处理结果的），注意在模板template里的代码，模板里不允许括号，但如果使用此类的调用函数，一样去连接数据库的，能用缓存的数据就别连接到数据库去处理结果。还要注意的是，自定义的实体属性，如果调用函数的，记得自己加上缓存策略。

- 使用QuerySets的iterator()： 　　
  - 通常QuerySets先调用iterator再缓存起来，当获取大量的实体列表而仅使用一次时，缓存行为会耗费宝贵的内存，这时iterator()能帮到你，iterator()只调用iterator而省 去了缓存步骤，显著减少内存占用率，具体参考相关文档。



##### 三， 数据库的工作就交给数据库本身计算，别用Python处理

- 使用 filter and exclude 过滤不需要的记录，这两个是最常用语句，相当是SQL的where

- 同一实体里使用F()表达式过滤其他字段

- 使用annotate对数据库做聚合运算

- 不要用python语言对以上类型数据过滤筛选，同样的结果，python处理复杂度要高，而且效率不高， 白白浪费内存

- 使用QuerySet.extra() extra虽然扩展性不太好，但功能很强大，如果实体里需要需要增加额外属性，不得已时，通过extra来实现，也是个好办法

- 使用原生的SQL语句 如果发现Django的ORM已经实现不了你的需求，而extra也无济于事的时候，那就用原生SQL语句



##### 四，如果需要就一次性取出你所需要的数据

- 单一动作（如：同一个页面）需要多次连接数据库时，最好一次性取出所有需要的数据，减少连接数据库次数。

  - 此类需求推荐使用QuerySet.select_related() 和prefetch_related()

- 相反，别取出你不需要的东西，模版templates里往往只需要实体的某几个字段而不是全部
  - 这时QuerySet.values() 和 values_list()，对你有用
  - 它们只取你需要的字段，返回字典dict和列表list类型的东西，在模版里够用即可，这可减少内存损耗，提高性能

- 同样QuerySet.defer()和only()对提高性能也有很大的帮助
  - 一个实体里可能有不少的字段，有些字段包含很多元数据，比如博客的正文，很多字符组成，Django获取实体时（取出实体过程中会进行一些python类型转换工作），我们可以延迟大量元数据字段的处理，只处理需要的关键字段
  - 这时QuerySet.defer()就派上用场了，在函数里传入需要延时处理的字段即可；而only()和defer()是相反功能

- 使用QuerySet.count()代替len(queryset)
  - 虽然这两个处理得出的结果是一样的，但前者性能优秀很多。
- 同理判断记录存在时，QuerySet.exists()比if queryset实在强得太多了



##### 五，懂减少数据库的连接数

使用 QuerySet.update() 和 delete()，这两个函数是能批处理多条记录的，适当使用它们事半功倍；如果可以，别一条条数据去update delete处理。

对于一次性取出来的关联记录，获取外键的时候，直接取关联表的属性，而不是取关联属性

```
entry.blog.id
优于
entry.blog__id# 善于使用批量插入记录，如：Entry.objects.bulk_create([
    Entry(headline="Python 3.0 Released"),
    Entry(headline="Python 3.1 Planned")
])
优于
Entry.objects.create(headline="Python 3.0 Released")
Entry.objects.create(headline="Python 3.1 Planned")# 前者只连接一次数据库，而后者连接两次
# 还有相似的动作需要注意的，如：多对多的关系，my_band.members.add(me, my_friend)
优于
my_band.members.add(me)
my_band.members.add(my_friend)
```





##### 准备工作：

##### settings.py添加该配置参数:

```
# 只要操作数据库那么就会打印sql语句

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'propagate': True,
            'level':'DEBUG',
        },
    }
}

```



##### **惰性查询特点**

```
# 惰性查询：如果只是书写了orm语句，在后面根本没有用到该语句所查询出来的参数，那么orm会自动识别出来，直接不执行。

# 举例：
	res = models.Book.objects.all()  # 这时orm是不会走数据库的
    print(res)   # 只有当要用到的上述orm语句的结果时，才回去数据库查询。
```

```
# 我们下来做一个题目：
获取数据表中所有数的名字：
    res = models.Book.objects.values('name')
    print(res)   # 拿到的是列表套字典的形式
    for i in res:
        print(i.get('name'))   # for循环出字典，通过.get方法取出每个书的名字

```



##### # 那么如何实现获取到的是一个数据对象，然后点title就能够拿到书名，并且没有其他字段。

only用法

```
res = models.Book.objects.only('name') # 对象只有name属性
print(res)
for i in res:
    print(i.name)  # 如果点(.)only括号内有的字段，不走数据库
	print(i.price)  # 如果点(.)only括号内没有的字段，那么会反复走数据库去查询(查询一个返回一个)而all()不需要

```

defer用法

```
res = models.Book.objects.defer('name')  # 对象除了没有name属性之外其他的都有
for i in res:
    print(i.price)


"""
    defer与only刚好相反
        defer括号内放的字段不在查询出来的对象里面 查询该字段需要重新走数据
        而如果查询的是非括号内的字段 则不需要走数据库了
"""

```



**select_related联表操作**

```
# 跟跨表操作有关

示例：
# 查询每本书的出版社名字
    res = models.Book.objects.all()
    for i in res:
        print(i.publish.name)
# 使用all方法查询的时候，每一个对象都会去数据库查询数据



# 使用select_related()
    res = models.Book.objects.select_related()
    for i in res:
        print(i.publish.name) # 直走一次数据库 INNER JOIN链表操作
"""
    select_related内部直接先将book与publish连起来 然后一次性将大表里面的所有数据
    全部封装给查询出来的对象
        这个时候对象无论是点击book表的数据还是publish的数据都无需再走数据库查询了

    select_related括号内只能放外键字段    一对多 一对一
        多对多也不行

"""

# 这样就比all方法更加的优化一点，这样网络请求就少了，延迟就降低了，提高效率。

```



**prefetch_related子查询**

```
# 跟跨表操作有关

res = models.Book.objects.prefetch_related('publish')  # 子查询
for i in res:
    print(i.publish.name)
    
"""
    prefetch_related该方法内部其实就是子查询
        将子查询查询出来的所有结果也给你封装到对象中
        给你的感觉好像也是一次性搞定的
"""


```



##### 总结

```
# prefetch_related对比select_related少了一次查询

# 到底孰优孰劣呢？
各有优缺点：如果表特别特别大的时候使用prefetch_related品表阶段就要耗费很长的时间，而select_related子查询虽然查询两次，但是操作两个表的时间非常短效率就会胜于联表查询prefetch_related
```

