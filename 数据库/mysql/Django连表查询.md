##### ORM连表操作

在django学习orm的时候，我们可以把一对多和多对多分为两种方式：正向搜索和反向搜索。

正向查找：ForeignKey在UserInfo表中。如果从UserInfo表开始查询其他表，这是一个正向操作，而如果从UserType表开始查询其他表，这是一个反向操作。

- 一对多：模型。外键(其他表)
- 多对多：模型。ManyToManyField(其他表格)
- 一对一：模特。一对一字段(其他表)

##### 正向连表操作总结：

所谓的正向和反向连接表操作的标识仅由Foreign_Key字段位于哪个表来确定，

Foreign_Key字段可用于连接任何表中的表；否则，将使用与Foreign_Key字段关联的小写表名。

- 一对多：对象。外键。关联表字段，值(外键字段_ 关联表字段)

- 多对多：外键字段。全部()

##### 反向连表操作总结：

- 通过值、值列表和过滤器反转跨表：小写表名_ 关联的表字段

- 按对象反向跨表：小写surface _set.all()。

  - all()：获取全部

  - filter：再次筛选


  ```
 Class.objects.filter(id=1).first().stu_set.filter(name__startswith='o')
  ```



##### 字段关系：

- 字段关系是 django 维护表关系的方式；其中主要有一对一，多对一以及多对多， 

- 现在的一对一及多对一关系中需要设置 **on_delete** 属性用来描述当关联数据被删除时的操作，有如下一些
  - models.CASCADE：删除关联数据,与之关联也删除 
  - models.PROTECT：删除关联数据,引发错误ProtectedError
  - models.SET_NULL：与之关联的值设置为null（前提FK字段需要设置为可空） 
  - models.SET_DEFAULT： 删除关联数据,与之关联的值设置为默认值（前提FK字段需要设置默认值）
  -  models.DO_NOTHING：删除关联数据,什么也不做



##### 一对一关系:

比如当你拥有一个老师表时，紧接着你还需要一个教授表，那么教授表可能拥有老师表的一系列属性，那么你还不想把老师表中的字段直接复制到教授表，那么可以通过**OneToOneField**来实现教授表继承老师表

```
模型类使用OneToOneField用来定义一对一关系；

OneToOneField(to,on_delete,parent_link=False,options)

class Child(models.Model):
    name=models.CharField(max_length=100,verbose_name='姓名')
    age=models.CharField(max_length=100,verbose_name='年纪')
    def __str__(self):
        return self.name

class Man(models.Model):
    child=models.OneToOneField(to=Child,verbose_name='小孩',on_delete=models.CASCADE)
    Responsibility=models.BooleanField(verbose_name='责任',default=True)
    def __str__(self):
        return self.child.name

python .\manage.py shell
from myapp.models import *
c1=Child.objects.create(name='张三',age='18')  #添加一条数据到child表
m1=Man.objects.create(child=c1)
m1.child   --><Child: 张三>
m1.child.name   -->'张三'
c1.delete()   --> {'myapp.Man': 1, 'myapp.Child': 1})   删除被继承的表的数据  继承的表数据也同时被删除
```



##### 多对一关系

Django使用django.db.models.**ForeignKey**定义多对一关系
ForeignKey需要一个位置参数：与该模型关联的类
生活中的多对一关系：班主任，班级关系。一个班主任可以带很多班级，但是每个班级只能有一个班主任

```
class Headmaster(models.Model):
	name=models.CharField(max_length=50)
	def __str__(self):
		return self.name

class Class(models.Model):
	class_name=models.CharField(max_length=50)
	teacher=models.ForeignKey(Headmaster,null=True,on_delete=models.SET_NULL)
	def __str__(self):
		return self.class_name


>>> H1 = Headmaster(name='渔夫')
>>> H1.save()
>>> H1
<Headmaster: 渔夫>
>>> H2 = Headmaster(name='农夫')
>>> H2.save()
>>> Headmaster.objects.all() 
[<Headmaster: 渔夫>, <Headmaster: 农夫>]

以上创建了两条老师数据
由于我们设置外键关联可以为空 null=True ,所以此时在班级表创建时，可以直接保存，不需要提供老师数据

>>> C1 = Class(class_name='一班') 
>>> C2 = Class(class_name='二班') 
#如果外键设置不为空时，保存会引发以下错误 
# IntegrityError: NOT NULL constraint failed: bbs_class.teacher_id 
>>> C1.teacher = H1 
>>> C2.teacher = H2 
>>> C1.save() 
>>> C2.save()

将老师分配个班级之后，由于班级表关联了老师字段，我们可以通过班级找到对应老师
虽然老师表中没有关联班级字段，但是也可以通过老师找到他所带的班级，这种查询方式也叫作关联查询
通过模型类名称后追加一个'_set'，来实现反向查询
>>> H1.class_set.all() 
<QuerySet [<Class: 一班>]>

由于我们这是一个多对一的关系，也就说明我们的老师可以对应多个班级
我们可以继续给H1老师分配新的班级

>>> C3 = Class(class_name='三班') 
>>> C3.teacher = H1 
>>> C3.save() 
>>> H1.class_set.all() 
[<Class: 一班>, <Class: 三班>]
```

- 一个班级只能对应一个老师，外键是唯一的，那么你在继续给C1班级分配一个新的老师时，**会覆盖之前的老师 信息**，并不会保存一个新的老师



##### 多对多关系

多对多关系在模型中使用**ManyToManyField**字段定义

多对多关系可以是具有关联，也可以是没有关联，所以不需要明确指定on_delete属性
生活中，多对多关系：一个音乐家可以隶属多个乐队，一个乐队可以有多个音乐家

```
class Artist(models.Model):
	artist_name=models.CharField(max_length=50)
	def __str__(self):
		return self.artist_name

class Band(models.Model):
	band_name=models.CharField(max_length=50)
	artist=models.ManyToManyField(Artist)
	def __str__(self):
		return self.band_name

创建音乐家以及乐队
>>> from bbs.models import Artist,Band 
>>> A1 = Artist.objects.create(artist_name='Jack') 
>>> A2 = Artist.objects.create(artist_name='Bob') 
>>> B1 = Band.objects.create(band_name='FiveMonthDay') 
>>> B2 = Band.objects.create(band_name='SHE')

创建出两个乐队之后对其进行音乐家的添加
多对多字段添加时，可以使用 add 函数进行多值增加

>>> B1.artist.add(A1,A2) 
>>> B2.artist.add(A2)

B1 乐队含有 A1 , A2 两名成员
B2 乐队含有 A1 成员

>>> B1.artist.all() 
[<Artist: Bob>, <Artist: Jack>] 
>>> B2.artist.all() 
[<Artist: Jack>]

可以在音乐家表中查找某个乐家属于哪些乐队
>>> Band.objects.filter(artist=A1) # 这里使用的是我们模型类来进行查找。 
[<Band: SHE>, <Band: FiveMonthDay>] # A1乐家属于，SHE以及FiveMonthDay 
>>> Band.objects.filter(artist=A2) 
[<Band: SHE>]

也可以查找这音乐家在哪个乐队
>>> A1.band_set.all() # 直接通过具体数据对象进行查找 
[<Band: SHE>, <Band: FiveMonthDay>] 
>>> A2.band_set.all() 
[<Band: SHE>]

多对多关联字段的删除，要使用 remove 来进行关系的断开
而不是直接使用 delete ， remove 只会断开数据之间的联系，但是不会将数据删除
现在在B1乐队中删除A1乐家

>>> B1.artist.remove(A1) 
>>> B1.artist.all() 
<QuerySet [<Artist: Bob>]>

```



