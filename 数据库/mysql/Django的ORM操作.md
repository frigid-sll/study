






```
# 基本条件查询

# 1.查询id为1的书籍	

BookInfo.objects.filter(id=1)



# 2.查询书名包含‘湖’的书籍 (like %湖%)	

BookInfo.objects.filter(btitle__contains='湖')



# 3.查询书名以‘部’结尾的书籍 （endswith 、startswith）（like %部）	

BookInfo.objects.filter(btitle__endswith='部')



# 4.查询书名不为空的书籍 (双重否定代表肯定)	

BookInfo.objects.filter(btitle__isnull=False)



# 5.查询编号为2或4的书籍 （选项，要么2要么4） （不是区间）	

BookInfo.objects.filter(id__in=[2,4])



# 6.查询编号大于2的书籍 (大于：gt)(小于：lt)(大于等于：gte)(小于等于：lte)	
BookInfo.objects.filter(id__gt=2)



# 7.查询id不等于3的书籍 (exclude查询满足条件以外的数据) （filter查询满足条件的数据）	
BookInfo.objects.exclude(id=3)



# 8.查询1980年发表的书籍	

BookInfo.objects.filter(bpub_date__year='1980')



# 9.查询1990年1月1日后发表的书籍	

BookInfo.objects.filter(bpub_date__gt=date(1990,1,1))



# 10.按照阅读量进行排序查询
正序(从小到大):

BookInfo.objects.all().order_by('bread')

倒序:
BookInfo.objects.all().order_by('-bread')
 


########################################################
# 

F对象
# 1.查询阅读量大于评论量的书籍	

BookInfo.objects.filter(bread__gt=F('bcomment'))

# 2.查询阅读量大于2倍评论量的书籍	

BookInfo.objects.filter(bread__gt=F('bcomment')*2)
 


########################################################
# 

Q对象
# 1.查询阅读量大于20，或编号小于3的图书	

BookInfo.objects.filter(Q(bread__gt=20) | Q(id__lt=3))

# 2.查询编号不等于3的书籍	

BookInfo.objects.filter(~Q(id=3))



########################################################
# 

聚合函数
# 1.统计总的阅读量	

BookInfo.objects.aggregate(Sum('bread'))



########################################################
# 

基础关联查询
# 1.一查多：查询编号为1的图书中所有人物信息	

book = BookInfo.objects.get(id=1)	

book.heroinfo_set.all()


# 2.多查一：查询编号为1的英雄出自的书籍	

hero = HeroInfo.objects.get(id=1)	
hero.hbook




########################################################
# 

关联过滤查询

# 1.多查一：查询书籍中人物的描述包含"降龙"的书籍	

BookInfo.objects.filter(heroinfo__hcomment__contains='降龙')

# 2.一查多：查询书名为"天龙八部"的所有人物信息	

HeroInfo.objects.filter(hbook__btitle='天龙八部')




from django.db.models import Q

def index(request):
    a=models.Company.objects.filter(Q(num__gt=20)|Q(name__contains='小')).order_by('-time')
    for x in a:
        print(x.name)
    return HttpResponse('123')

```





##### 执行manage.py migrate，报错： django.db.utils.OperationalError: (1050, “Table ‘表名’ already exists）

```
python manage.py migrate myapp --fake  
```





##### 添加

```
# 表.objects.create

# 方法一
a = User.objects.create(userNum=123, name='ABB', age=18, sex='男')

# 方法二
d = dict(userNum=123, name='ABB', age=18, sex='男')
a = User.objects.create(**d)

#方法三
a = User(userNum=123, name='ABB', age=18, sex='男')
a.save()

```



| 参数             | 解释                                                         |
| ---------------- | ------------------------------------------------------------ |
| get_or_create    | 只要有一个字段值与数据表中不相同（除主键），就会执行插入操作<br/>如果完全相同则不进行插入操作，而是返回这行数据的数据对象 |
| update_or_create | 判断当前数据在数据表中是否存在，若存在则进行更新，否则为新增表数据 |
| bulk_create      | 对数据进行批量操作<br/>v1 = User(userNum=123, name='ABB', age=18, sex='男')<br/>v2 = User(userNum=124, name='ABC', age=19, sex='女')<br/>info_list = [v1,v2]<br/>User.objects.bulk_create(info_list)<br/> |

- get_or_create

  ```
  >>> Class.objects.get_or_create(name='www',number=123,defaults={})
  (<Class: www>, True)
  >>> Class.objects.all()
  <QuerySet [<Class: 师玲珑>, <Class: 张雪>, <Class: www>]>
  >>> Class.objects.get_or_create(name='www',number=123,defaults={})
  (<Class: www>, False)
  >>> Class.objects.all()
  <QuerySet [<Class: 师玲珑>, <Class: 张雪>, <Class: www>]>
  ```

- update_or_create

  ```
  Django提供了update_or_create方法，执行数据修改时，判断要修改的数据是否已经存在：
  大致意思是创建或者更新，当过滤条件匹配到查询结果则将更新defaults字典中的字段，否则创建一条记录，字段内容为defaults字段中的内容。
  
  返回（对象，已创建）的元组，其中object是已创建或已更新的对象，created是一个布尔值，指定是否创建了新对象。
  
  >>> Class.objects.update_or_create(name='www',number=123,defaults={'name':'sss'})
  (<Class: sss>, False)
  >>> Class.objects.all()
  <QuerySet [<Class: 师玲珑>, <Class: 张雪>, <Class: sss>]>
  ```

  





##### 删除

```
# 表.objects.filter().delete()

# 方法一 删除全部内容
User.objects.all().delete()

#方法二 删除一条name为ABC的数据
User.objects.filter(name='ABC').delete()

#方法三 删除多条数据
User.objects.filter(age=18).delete()

```

删除过程中数据设有外键字段，就会同时删除外键关联的数据，删除模式参考[models.py](https://blog.csdn.net/alittlehorse/article/details/118230241?spm=1001.2014.3001.5501)中设置的PROTECT、SET_NULL等



##### 修改

```
# 表.objects.filter().update()

# 方法一 修改name为ABC的性别为gay
User.objects.filter(name='ABC').update(sex='gay')

# 方法二 
a = dict(age='1')
User.objects.filter(name='ABC').update(**a)

# 方法三 使用F方法实现自增/自减
from djanto.db.models import F
User.objects.filter(name='ABC').update(age=F('age')+1)

```



##### 查询

```
# select * from user 全表查询
a = User.objects.all()
# 查第一条
a[0].name

# select * from user LIMIT3 查前3条
a = User.objects.all()[:3]

# filter 也可添加多个条件
User.objects.filter(name='ABC',age=18)

# SQL中or方法 select * from user where name='ABC' or age=18 ,需要引入 Q
from django.db.models import Q
User.objects.filter(Q(name='ABC') | Q(age=18))

# SQL中not方法 select * from user where not name='ABC' ,在Q前加~
User.objects.filter(~Q(name='ABC'))

# 统计数量
User.objects.filter(name='ABC').count()

# 去重 select DISTINCT name from user where name='ABC' ，distinct无需设置参数，去重方式根据values
a = User.objects.values('name').filter(name='ABC').distinct()

# 降序排序查询，降序在order_by里设置 '-'
User.objects.order_by('-age')

```



| **匹配符**  | **使用**                        | **说明**                               |
| ----------- | ------------------------------- | -------------------------------------- |
| __exact     | filter(name__exact=‘ABC’)       | 完全等于                               |
| __iexact    | filter(name__iexact =‘ABC’)     | 完全等于并忽略大小写                   |
| __contains  | filter(name__contains =‘ABC’)   | 模糊匹配，类似SQL中like %ABC%          |
| __icontains | filter(name__icontains =‘ABC’)  | 模糊匹配并忽略大小写                   |
| __gt        | filter(name__gt =1)             | 大于                                   |
| __gte       | filter(name__gte =1)            | 大于等于                               |
| __lt        | filter(name__lt=1)              | 小于                                   |
| __lte       | filter(name__lte=1)             | 小于等于                               |
| __isnull    | filter(name__isnull=True/False) | 判断是否为空                           |
| __in        | filter(createtime__in=need_del) | 判断createtime是否在这个need_del列表里 |





##### 关联表外键参数on_delete

```
(1)、on_delete = None：
删除关联表的数据时，当前表与关联表的filed的行为。
(2)、on_delete = models.CASCADE：
表示级联删除，当关联表（子表）中的数据删除时，与其相对应的外键（父表）中的数据也删除。
(3)、on_delete = models.DO_NOTHING:
你删你的，父亲（外键）不想管你
(4)、on_delete = models.PROTECT:
保护模式，如采用这个方法，在删除关联数据时会抛出ProtectError错误
(5)、on_delete = models.SET_DEFAULT:
设置默认值，删除子表字段时，外键字段设置为默认值，所以定义外键的时候注意加上一个默认值。
(6)、on_delete = models.SET（值）:
删除关联数据时，自定义一个值，该值只能是对应指定的实体
```



##### 数据库字段

- 字符串

  ```
  password=models.CharField(verbose_name='密码：',max_length=50)
  ```

- 设置主键

  ```
  account=models.CharField(verbose_name='账号：',max_length=50,primary_key=True,db_index=True)
  db_index:添加索引
  ```

- 设置关联外键

  ```
  account=models.ForeignKey(User_Account,on_delete = models.CASCADE)
  ```

- 整型

  ```
  group_id=models.IntegerField(verbose_name='群聊编号')
  ```

- 布尔类型

  ```
  models.BooleanField(verbose_name='是否可以增加文件',default=False)
  ```

- 单选

  ```
  #sex choices 设置单选，元组前面的值为真是存储值，后面的值为展示值sex=models.CharField(max_length=1,choices=[('男','男'),('女','女')])
  ```

- 时间

  ```
  DateTimeField(DateField)x
  日期+时间格式 YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]
  
  models.DateField(verbose_name='token更新时间',auto_now=True)
  日期格式 YYYY-MM-DD
  auto_now：每次修改都会自动更新
  auto_now_add：数据创建时值为添加时的时间，后续其他字段数据修改不会变
  
  TimeField(DateTimeCheckMixin, Field)
  时间格式 HH:MM[:ss[.uuuuuu]]
  ```

  



##### 清空数据库，重新建表

- 想要删除自己之前练习的数据库模型

  ```
  Order.objects.all().values().delete()
  ```

- 删除文件

  - 删除数据库内所有的表
  - 删除migrations文件夹中的所有 文件，除了`__init__.py `文件
  - 运行

  ```
  python manage.py makemigrations
  python manage.py migrate
  ```





##### `django` 解决`manage.py migrate`无效的问题

- **解决方案**

  ```
  python manage.py dbshell 进到数据库中，执行delete from django_migrations where app='your_appname';
  
  python manage.py makemigrations(若migrations文件未删除，可不执行这一步)
  
  python manage.py migrate 好啦，大功告成
  ```

- **原因**

  ```
  造成多次应用migrations失败的原因是，当前model是修改过的，原来的migrations已经被我删除，但是，重新生成的migrations使用递增整数记名，所以，在django_migrations表中0001，0002等前面几个数字的文件都已被记录，在Django看来，被记录了就相当于已应用，所以，会出现刚开始的No migrations to apply.
  ```

  



