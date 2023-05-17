Odoo的发展历史伴随着Python2到Python3的发展, 因此也不可避免了留下了历史的痕迹. 从最初的(cr,uid,ids,context) 到 api.one, api.mulit, api.model, 再到如今只剩5种装饰方法, API的历史演变体现了Python2到Python3的进程, 本章我们将了解Odoo中API的前世今生.



##### 8.0之前的API

当年那是Odoo还叫OpenERP的时代，OpenObject对象的方法通常都需要带着几个固定的参数：cr,uid,ids,context等等，写起来很繁琐，比如下面的例子：

```python
def btn_import(self,cr,uid,ids,context=None):
    ...
```

到了8.0，可能Odoo官方的开发人员也觉得这样写起来太繁琐了，于是乎，他们引入了新API，封装在api.py文件中，主要有一下几种类型：

- model
- multi
- one
- constrains
- depends
- onchange
- returns

而从13.0开始, 官方再次对API动刀, 这次仅保留了5种装饰方法:

- model
- constrains
- depends
- onchange
- returns

下面我们就这5种类型进行详细的介绍, 关于one和multi的介绍 我们放到附录中, 仅供需要维护旧版本Odoo的同学参考.



##### model

在Odoo中，`@model`是一个装饰器，用于将一个Python类与Odoo模型关联起来。具体用法如下：

首先，需要在Python文件中导入`@model`装饰器：

```python
from odoo import models, fields, api
```

接下来，定义一个Python类，并在类上使用`@model`装饰器：

```python
class ExampleModel(models.Model):
    _name = 'example.model'
    _description = 'Example Model'
    name = fields.Char(string='Name', required=True)
```

在这个例子中，`ExampleModel`是一个继承自`models.Model`的Python类，它代表了一个Odoo模型。使用`@model`装饰器，可以将这个Python类和Odoo模型关联起来。 `_name`属性指定了这个模型的名称，`_description`属性指定了这个模型的描述。`name`字段是这个模型的一个属性，它定义了一个Char类型的字段，在Odoo中它将被渲染为一个文本框。 3. 定义模型的方法 在Odoo模型中，可以定义各种方法来实现特定的功能。例如，可以定义一个读取模型数据的方法：

```python
class ExampleModel(models.Model):
    _name = 'example.model'
    _description = 'Example Model'
    name = fields.Char(string='Name', required=True)
    @api.model
    def get_all_names(self):
        return self.env['example.model'].search([]).mapped('name')
```

在这个例子中，定义了一个名为`get_all_names`的方法，它使用`self.env['example.model'].search([])`来搜索所有`example.model`记录，并使用`mapped('name')`将它们的`name`属性映射为一个列表。这个方法使用了`@api.model`装饰器，表示它是一个模型级别的方法，可以通过`ExampleModel.get_all_names()`来调用。 除了`@api.model`，还有其他的装饰器可以用于定义不同类型的方法，例如`@api.multi`用于定义可以一次处理多个记录的方法，`@api.one`用于定义只能处理单个记录的方法等等。这些装饰器可以根据实际需要选择使用。





##### contrains

作用：给某些字段添加限制条件, 如果是多个字段, 用逗号将其分开. 触发条件: 单声明的字段值发生变化时触发

constrains只接受简单的字段名称, 像对象属性obj.x形式的参数将会被忽略. 另外, 使用constrains限制的字段必须出现在视图中(如果没有出现,可以使用重载create的方法强制实现).

在我们book_store模块中, 我们可以给book对象设置一个名称限制, 限制其名称长度必须在10个字符以内,否则提示错误.

```python
@api.constrains("name")
def _check_name(self):
    """检查名称长度"""
    if len(self.name) > 10:
        raise ValidationError("图书名称必须限制在10个字符以内")
```

当输入错误时,便会提示:

![img](https://book.odoomommy.com/chapter1/images/4.png)

constrains的参数也可以是一个函数(当参数是函数时,只能接受一个参数), 该函数返回要限制的字段列表.

```python
def _get_constrains_fields(self):
        return ['name', 'date']

@api.constrains(_get_constrains_fields)
def _check_name(self):
    """检查名称长度"""
    if len(self.name) > 10:
        raise ValidationError("图书名称必须限制在10个字符以内")
    if self.date < date(2000,1,1):
        raise ValidationError("只能添加2000年以后的图书")
```



##### 另外一种constrains

odoo支持另外一种添加限制的方式，即通过sql约束的方式。方法是在odoo类对象中添加_sql_constraints属性，值是一个包含了元组的列表，元组的三个值分别是约束名，约束条件和警告信息，看一个例子：

```python
_sql_constraints = [
    ('name_description_check',
     'CHECK(name != description)',
     "The title of the course should not be the description"),
    ('name_unique',
     'UNIQUE(name)',
     "The course title must be unique"),
]
```

这样做的好处是，在数据库层面就限制了数据的校验，而不是在代码层面的校验，显然效率会更高。缺点是在添加限制之前，数据库中不能存在违反约束的数据，否则约束会添加失败。



##### depends

depends主要用于compute方法，v8当中已经取消了function字段，对于任何fields都可以通过添加compute属性动态赋值。depends就是用来标该方法依赖于哪些字段的装饰。

```python
@api.depends('date')
def _get_book_age(self):
    self.age = (datetime.now().date() - self.date).days
```

depends装饰器的参数可以是多个以逗号分割的字段, 也可以是一个返回字段列表的函数. depends装饰器不可用于id字段.

对于compute方法来说，加不加depends装饰的区别在于，加了depends的方法会在依赖的字段发生改变时重新计算本字段的值，而不加depends的方法只在触发的第一次调用，也就是说不会持续更新。



##### returns

returns的用法主要是用来指定返回值的格式，它接受三个参数，第一个为返回值的model，第二个为向下兼容的method，第三个为向上兼容的method。

第一个参数如果是对象本身，则写'self',如果是其他对象，则写其他对象名如：@api.returns('ir.ui.view')。

例如：

```python
@api.multi    
@api.returns('mail.message', lambda value: value.id)
def message_post(self, **kwargs):
    if self.env.context.get('mark_so_as_sent'):
        self.filtered(lambda o: o.state == 'draft').with_context(tracking_disable=True).write({'state': 'sent'})
        self.env.user.company_id.set_onboarding_step_done('sale_onboarding_sample_quotation_state')
    return super(SaleOrder, self.with_context(mail_post_autofollow=True)).message_post(**kwargs)
```

returns主要用于确保新旧API返回值的一致，并不常用。



##### onchange

onchange的适用场景是当某个字段发生变化时被调用，用来处理需要动态联动的字段。

onchange的参数是发生变化的字段名，例如：

```python
@api.onchange('amount', 'unit_price')
def _onchange_price(self):
   self.price = self.amount * self.unit_price
   return {
       'warning': {
           'title': "Something bad happened",
           'message': "It was very bad indeed",
       }
   }
```

onchange 可以有返回值可以没有返回值。返回值由一个字典组成，可选的值有 value和warning，value用来返回需要设置的字段值，warning用来返回一些警告信息。

```python
@api.onchange('field_name')
def onchange_field_name(self):
    value = self.field_name if self.field_name else 'Nothing'
    return {'value': {'field_name': value}}
```



#### CUID方法介绍

前面介绍了API的多种装饰器及其作用，下面介绍odoo ORM框架的标准CUID方法。所谓CURD即Create\Update\Read\Delete等操作的简称。



##### Browse

在odoo中如果我们想要读取某个对象的信息，最常用的方法是browse方法，browse方法接收一个参数ID，然后返回该对象对应的对象。

```python
order = self.env['sale.order'].browse(1)
print(order.name)
```

获取到对象以后，使用点号+属性名的方式即可获取该对象所有属性或者调用对应的方法。



##### Create

如果我们想要创建一个对象，那么我们就需要使用create方法。create方法接收一个参数vals，其值是包含需要创建的对象的各个字段的值。

```python
order = self.env['sale.order'].create({
    "name":"SO0001",
    "user_id":1
})
```



##### Write

write方法给我们提供了一个修改对象值的方法，接收一个参数vals，其值是包含需要修改字段的值。

```python
order = self.env['sale.order'].browse(1)
order.write（{
    "name":"SO002"
})
```

如果只是修改其中的一个字段的值，那么可以直接使用赋值的方法：

```python
order = self.env['sale.order'].browse(1)
order.name = "SO0002"
```

两种方法的作用是等效的，第二种方法跟面向对象一些，第一种方法的优势在于可以在一行代码中提交多个字段的修改。



##### Unlink

odoo ORM的删除并没使用delete作为删除方法，而是使用了unlink关键字。

```python
order = self.env['sale.order'].browse(1)
order.unlink()
```

> 这里只对CUID的各个方法做一个简单的示例, 关于其内部更多的详情,参见第五部分的模型一章.





##### search

在Odoo中，可以使用`self.env['partner'].search(domain, offset=0, limit=None, order=None, count=False)`方法来搜索partner模型中符合条件的记录。具体用法如下：

- domain：搜索条件，可以是一个由多个操作符和字段名、字段值组成的列表。例如，`[('name', '=', 'John'), ('is_company', '=', True)]`表示搜索所有is_company属性为True且name属性为John的partner记录。
- offset：搜索结果的偏移量，表示从第几条记录开始返回结果，默认为0。
- limit：搜索结果的最大数量，表示最多返回多少条记录，默认为None，表示返回所有符合条件的记录。
- order：搜索结果的排序方式，可以是一个由多个排序字段和排序方向组成的列表。例如，`'name asc, id desc'`表示先按name字段升序排序，再按id字段降序排序。
- count：是否返回搜索结果的数量而不是记录列表，默认为False，表示返回记录列表。 例如，如果需要搜索所有is_company属性为True且name属性为John的partner记录，并按id字段降序排序，可以使用以下代码：

```
partners = self.env['partner'].search([('name', '=', 'John'), ('is_company', '=', True)], order='id desc')
```

这个代码会返回一个partner记录列表，其中包含所有is_company属性为True且name属性为John的记录，并按id字段降序排序。 需要注意的是，domain参数是必须的，而其他参数都是可选的。在使用search方法时，可以根据实际需要选择要使用的参数。





##### mapped

在Odoo中，`mapped`是一个方法，可以用于将一个记录集中指定的字段映射为一个列表。具体用法如下：

```python
recordset.mapped(fieldname)
```

其中，`recordset`表示一个记录集，`fieldname`表示要映射的字段名。这个方法会返回一个包含所有记录中指定字段的值的列表。 例如，如果有一个名为`example.model`的模型，其中有一个名为`name`的Char类型的字段，可以使用下面的代码将`example.model`模型中所有记录的`name`字段映射为一个列表：

```python
names = self.env['example.model'].search([]).mapped('name')
```

这个代码会先使用`self.env['example.model'].search([])`搜索所有`example.model`记录，然后使用`mapped('name')`将它们的`name`属性映射为一个列表。

最终，`names`变量将包含所有记录的`name`字段值组成的列表。 

##### 需要注意的是

- `mapped`方法只能用于记录集，不能用于单个记录。
- 另外，如果记录集中有多条记录的指定字段值相同，那么这个值在列表中只会**出现一次**。





##### 在Odoo中，search()和browse()都是用于从数据库中检索记录的方法，它们之间的区别如下：

1. search()方法：用于根据指定的条件从数据库中检索记录。search()方法接受一个类似于SQL的WHERE子句的条件参数，返回一个符合条件的记录集合(models.RecordSet对象)。搜索结果可以在调用search()方法时通过limit、offset、order等参数进行排序、分页、筛选等操作。search()方法返回的结果是一个RecordSet对象，可以像列表一样进行遍历、切片、排序等操作。
2. browse()方法：用于从数据库中获取指定ID的记录。browse()方法接受一个或多个记录的ID参数，返回一个RecordSet对象，该对象包含指定ID的记录。如果传入的ID参数为一个列表或元组，返回的RecordSet对象包含对应的所有记录。browse()方法的返回结果是一个RecordSet对象，可以像列表一样进行遍历、切片、排序等操作。 需要注意的是，search()方法是一个懒加载(lazy load)的方法，只有在真正需要访问搜索结果时才会从数据库中获取数据。而browse()方法是一个即时加载(eager load)的方法，它会立即从数据库中获取指定ID的记录并返回。因此，当需要查询指定ID的记录时，建议使用browse()方法；当需要根据条件查询记录时，建议使用search()方法。