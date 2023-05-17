##### PEP8选项

使用linter可帮助显示语法及句法警告或错误。Odoo源代码尽力遵守Python标准，但其中有一些可予以忽略。

- E501: 行内容过长
- E301: 应有一个空行，但无空行
- E302: 应有两个空行，但仅有一个



##### 导入的顺序为

1. 外部库 (每行一个并在python stdlib中分离)
2.  `odoo`的导入
3. 来自Odoo模块的导入 (很少见，仅在需要时进行)

在以上3组中，导入的行按字母排序。

```python
# 1 : imports of python lib
import base64
import re
import time
from datetime import datetime
# 2 : imports of odoo
import odoo
from odoo import api, fields, models, _ # alphabetically ordered
from odoo.tools.safe_eval import safe_eval as eval
# 3 : imports from odoo addons
from odoo.addons.website.models.website import slug
from odoo.addons.web.controllers.main import login_redirect
```



##### 编程规范(Python)

- 每个python文件的第一行应带有`# -*- coding: utf-8 -*-` .

- **易读性**高于**简洁性**或使用语法或惯例。

- 不要使用 `.clone()`

  ```
  # 不妥
  new_dict = my_dict.clone()
  new_list = old_list.clone()
  # 妥
  new_dict = dict(my_dict)
  new_list = list(old_list)
  ```

- Python字典 : 创建及更新

  ```python
  # -- creation empty dict
  my_dict = {}
  my_dict2 = dict()
   
  # -- creation with values
  # 不妥
  my_dict = {}
  my_dict['foo'] = 3
  my_dict['bar'] = 4
  # 妥
  my_dict = {'foo': 3, 'bar': 4}
   
  # -- update dict
  # 不妥
  my_dict['foo'] = 3
  my_dict['bar'] = 4
  my_dict['baz'] = 5
  # 妥
  my_dict.update(foo=3, bar=4, baz=5)
  my_dict = dict(my_dict, **my_dict2)
  ```

  - 举例

    ```python
    my_dict = {'a' : 1, 'b' : 2}
    my_dict2 = {'a' : 11, 'b' : 22, 'c' : 33}
    my_dict3 = dict(my_dict2, **my_dict)
    print(my_dict3)
    {'a': 1, 'b': 2, 'c': 33}
    
    my_dict3.update(a=11)
    print(my_dict3)
    {'a': 11, 'b': 2, 'c': 33}
    ```

- 使用有意义的变量/类/方法名

- 无用变量 : 临时变量可通常为对象给定名称来让代码更清晰，但那并不表示应当总是创建临时变量：

  ```python
  # 无意义
  schema = kw['schema']
  params = {'schema': schema}
  # 更简化
  params = {'schema': kw['schema']}
  ```

- 多个返回点在更为简化时是OK的

  ```python
  # 有点复杂并带有冗余的临时变量
  def axes(self, axis):
    axes = []
    if type(axis) == type([]):
            axes.extend(axis)
    else:
            axes.append(axis)
    return axes
   
   # 更清晰
  def axes(self, axis):
    if type(axis) == type([]):
            return list(axis) # 克隆axis
    else:
            return [axis] # 单元素列表
  ```

- 了解内置函数 : 至少应对所有的[Python内置函数](http://docs.python.org/library/functions.html)有一个基本的了解

  ```python
  value = my_dict.get('key', None) # very very redundant
  value = my_dict.get('key') # good
  ```

- 同时， `if 'key' in my_dict` 和 `if my_dict.get('key')` 的含义大相径庭，确保要正确使用。

- 学习列表推导式：使用列表推导式、字段解析式及使用 `map`, `filter`, `sum`, … 的基本操作。它们会让代码更易于阅读。

  ```python
  # 不太好
  cube = []
  for i in res:
          cube.append((i['id'],i['name']))
  # 更佳
  cube = [(i['id'], i['name']) for i in res]
  ```

- 集合也是布尔型：在python中，很多对象在布尔上下文（如if）中运行时具有“类布尔型”的值。其中有集合(列表、字典、集合…) ，在为空时为 “假”，在包含内容时为“真”：

  - 因此可以编写 `if some_collection:` 来代替 `if len(some_collection):`.

  ```python
  bool([]) is False
  bool([1]) is True
  bool([False]) is True
  ```

- 对可遍历内容进行遍历：

  ```python
  # 创建临时列表并查找bar
  for key in my_dict.keys():
          "do something..."
  # 更佳
  for key in my_dict:
          "do something..."
  # 访问键、值对
  for key, value in my_dict.items():
          "do something..."
  ```

- 使用 dict.setdefault

  ```python
  # 更长.. 更难以阅读
  values = {}
  for element in iterable:
      if element not in values:
          values[element] = []
      values[element].append(other_value)
   
  # 更好.. 使用 dict.setdefault 方法
  values = {}
  for element in iterable:
      values.setdefault(element, []).append(other_value)
  ```

- 作为一个优秀开发者，对代码添加文档 (方法中的docstring，复杂代码部分的简单注释)
- 这些指南以外，以下链接也会有帮助：http://python.net/~goodger/projects/pycon/2007/idiomatic/handout.html (有点老，但非常相关)



##### Odoo中的编程

- 避免创建生成器和装饰器：仅使用Odoo API所自带的
- 和在python中一样，使用 `filtered`, `mapped`, `sorted`, … 方法来改善可读性、优化性能。



##### 让方法批量生效

在添加函数时，确保其可通过遍历self的每条记录来处理多条记录。

```python
def my_method(self)
    for record in self:
        record.do_cool_stuff()
```



对于性能问题，（例如）在开发‘stat 按钮’时，不要在循环中执行 `search` 或 `search_count`。推荐使用 `read_group` 方法来在一个请求中计算所有值。

```python
def _compute_equipment_count(self):
""" Count the number of equipement per category """
    equipment_data = self.env['hr.equipment'].read_group([('category_id', 'in', self.ids)], ['category_id'], ['category_id'])
    mapped_data = dict([(m['category_id'][0], m['category_id_count']) for m in equipment_data])
    for category in self:
        category.equipment_count = mapped_data.get(category.id, 0)
```



##### 传送上下文

上下文是无法修改的 `frozendict` 。 要通过不同的上下文调用方法，应使用 `with_context` 方法：

```python
records.with_context(new_context).do_stuff() # 替换了所有的上下文
records.with_context(**additionnal_context).do_other_stuff() # additionnal_context的址覆盖原生上下文
```



##### ⚠️警告

- 在上下文中传递参数可能会伴随危险的副作用。

- 因为值是自动传送的，所以可能会出现一些预期外的行为。在上下文中通过*default_my_field*键调用 `create()`方法会对相应的模型设置*my_field*的默认值。但在创建期间，其它对象 (如创建sale.order时的sale.order.line)有一个*my_field* 字段名会创建，也会设置它们的默认值。

如需创建一个影响对象行为的关键上下文，选择一个好名称，并最终使用模块的名称作为前缀来隔离影响。一个好例子是`mail`模块的键：

- *mail_create_nosubscribe* 
- *mail_notrack*
-  *mail_notify_user_signature*, …



##### 不要跳过ORM

在ORM可完成相应任务时不应直接使用数据库游标！这样可以传递所有的ORM功能，可能是事务、访问权限等等。

并且很有可能会让代码更难以阅读、安全性更低。

```python
# 极其极其错误
self.env.cr.execute('SELECT id FROM auction_lots WHERE auction_id in (' + ','.join(map(str, ids))+') AND state=%s AND obj_price > 0', ('draft',))
auction_lots_ids = [x[0] for x in self.env.cr.fetchall()]
 
# 无注入，但仍错误
self.env.cr.execute('SELECT id FROM auction_lots WHERE auction_id in %s '\
           'AND state=%s AND obj_price > 0', (tuple(ids), 'draft',))
auction_lots_ids = [x[0] for x in self.env.cr.fetchall()]
 
# 更佳
auction_lots_ids = self.search([('auction_id','in',ids), ('state','=','draft'), ('obj_price','>',0)])
```





##### 禁止SQL注入！

在手动使用SQL查询时要注意不要引入SQL注入漏洞。在用户输入没有正确进行过滤或引用有问题时就会出现漏洞，让攻击者可以使用预期外的SQL查询语句y (如绕过过滤或执行 UPDATE或DELETE命令)。

最好的方式是永远永远不要使用Python字符串拼接 (+) 或字符串参数插值 (%) 来传递变量到SQL查询字符串中。

第二个原因，也同样重要，决定如何格式化查询参数是数据库抽象层(psycopg2)的任务，而不是你的任务！例如psycopg2知道在你传递值列表时需要将其格式化为逗号分隔列表，使用括号包裹！

```python
# 以下非常不妥：
#   - 它是一个SQL注入漏洞
#   - 可读性差
#   - 格式化id列表不是你的任务
self.env.cr.execute('SELECT distinct child_id FROM account_account_consol_rel ' +
           'WHERE parent_id IN ('+','.join(map(str, ids))+')')
 
# 更佳
self.env.cr.execute('SELECT DISTINCT child_id '\
           'FROM account_account_consol_rel '\
           'WHERE parent_id IN %s',
           (tuple(ids),))
```



这非常重要，请注意在重构时，最重要的是不要拷贝这些模式！

以下是一个易记忆的示例， 帮助我们记住问题所在 (但不要拷贝其中的代码)。在继续之前，请确保阅读pyscopg2的在线文档在学习正确的使用方式：

- 查询字符串的问题 (http://initd.org/psycopg/docs/usage.html#the-problem-with-the-query-parameters)
- 如何通过psycopg2传递参数 (http://initd.org/psycopg/docs/usage.html#passing-parameters-to-sql-queries)
- 高级参数类型 (http://initd.org/psycopg/docs/usage.html#adaptation-of-python-values-to-sql-types)



##### 考虑可扩展性

函数和方法不应包含太多逻辑： 更推荐使用一些简短简单的方式，而不是使用几个大而复杂的方法。一个黄金准则是在方法有一个以上任务时尽快进行分割(参见 http://en.wikipedia.org/wiki/Single_responsibility_principle).

应避免在方法中硬编码业务逻辑，因此妨碍了轻易地通过子模块进行继承：

```python
# 不要这么做
# 修改作用域或条件表示重载整个方法
def action(self):
    ...  # 长方法
    partners = self.env['res.partner'].search(complex_domain)
    emails = partners.filtered(lambda r: arbitrary_criteria).mapped('email')
 
# 更好但也不要这么做
# 修改逻辑强制复制一部分代码
def action(self):
    ...
    partners = self._get_partners()
    emails = partners._get_emails()
 
# 更佳
# 最小化重载
def action(self):
    ...
    partners = self.env['res.partner'].search(self._get_partner_domain())
    emails = partners.filtered(lambda r: r._filter_partners()).mapped('email')
```



以上代码是出于示例是对可扩展函数进行，但必须考虑可读性并进行权衡。

同样相应地对函数命名：简短、适当命名的函数是可读/可维护代码和紧致文档的起点。

这一推荐对类、文件、模块和包也同样适用。(还可参见http://en.wikipedia.org/wiki/Cyclomatic_complexity)



##### 不要执行事务

Odoo框架负责为所有的RPC调用提供事务性上下文。原则是新的数据库游标在每个RPC调用的开始时打开，并在调用返回时、传送RPC客户端回复前执行，大概是这样：

```python
def execute(self, db_name, uid, obj, method, *args, **kw):
    db, pool = pooler.get_db_and_pool(db_name)
    # 创建事务游标
    cr = db.cursor()
    try:
        res = pool.execute_cr(cr, uid, obj, method, *args, **kw)
        cr.commit() # 一切正常，执行
    except Exception:
        cr.rollback() # 错误，按原子性回滚所有内容
        raise
    finally:
        cr.close() # 保持关闭手动打开的游标
    return res
```



如果在RPC调用执行时发生任何错误，事务会自动进行原子级回滚，保留系统状态。

相似地，系统还在测试套装执行过程中提供独立的事务，因此它可以进行回滚或不依赖于服务端启动选项。

结果是如果手动在任何地方调用 `cr.commit()`，大机率会将系统分割成各种方式，因为你会产生部分提交，因而有部分和不利落的回滚，导致其它问题：

- 不连续的业务数据，通常会有数据丢失

- 工作流去同步，永久文档卡死

- 无法利落地回滚测试，并会开始污染数据库，以及导致错误 (即使在事务中未发生错误也会这样)



##### 以下是一些非常简单的规则：

应**永不**自己调用call `cr.commit()` ，**除非**你显式地创建了自己的数据库游标！并非需要这么做的场景非常罕见！顺便说一下如果你真的创建了自己的游标，那么需要处理错误用例及适当的回滚，以及在完成时恰当地关闭游标。

和通常认为的不同，你甚至不需要在以下场景中调用 `cr.commit()` ： – 在*models.Model* 对象的 `_auto_init()` 方法中：这由插件初始化方法处理，或者在创建自定义模型由ORM事务处理； – 在报表中: `commit()`也由框架处理，你甚至可以在报表中更新数据库 – 在*models.Transient*方法中：这些方法和*models.Model* ones的调用完全一致，在事务中及在结束处相应的`cr.commit()/rollback()` – 等等(如果存在疑虑查看通用规则 ！)

此后服务端框架之外的所有 `cr.commit()` 调用必须有**显式注释**说明它们绝对有必要，为什么它们确实正确，以及为什么它们没有毁坏事务。否则可以并应当删除它们！



##### 正确地使用翻译方法

Odoo使用了一个 GetText样式的方法，名为“下划线” `_( )` ，来代码中使用的静态字符串需要在运行时使用上下文的语言翻译。这种伪方法在代码中通过如下导入进行访问：

```python
from odoo import _
```



在使用时必须遵循一些非常重要的规则来让其生效并避免使用一些无用的垃圾填充翻译。

基本上，这一方法应公用在代码中手动编写的静态字符串，它不会翻译字段值，如商品名等。这时必须要在相应字段上使用翻译标记。

规则非常简单：调用下划线方法应总是以 `_('literal string')` 的形式而不能是其它形式：

```python
# 妥：普通字符串
error = _('This record is locked!')
 
# 妥：包含格式化模式的字符串
error = _('Record %s cannot be modified!') % record
 
# 也ok: 多行字面量字符串
error = _("""This is a bad multiline example
             about record %s!""") % record
error = _('Record %s cannot be modified' \
          'after being validated!') % record
 
# 不妥: 尝试在字符串格式化之后翻译
#      (注意括号!)
# 这<strong>不会</strong>起作用且会使翻译混乱!
error = _('Record %s cannot be modified!' % record)
 
# 不妥: 动态字符串、字符串拼接等禁止使用!
# 这不会起作用且会使翻译混乱!
error = _("'" + que_rec['question'] + "' \n")
 
# 不妥: 字段值会自动由框架翻译
# 这没有用且不会以你所认为的方式生效:
error = _("Product %s is out of stock!") % _(product.name)
# 并且以下当然不会生效，已进行过解释:
error = _("Product %s is out of stock!" % product.name)
 
# 不妥: 字段值自动由框架翻译
# 这没有用且不会按你所认为的方式生效：
error = _("Product %s is not available!") % _(product.name)
# 并且以下当然不会生效，已进行过解释:
error = _("Product %s is not available!" % product.name)
 
# 取而代之你可以使用如下，这样所有内容都会翻译，
# 包含产品名，如果其字段定义相应地设置了翻译标记：
error = _("Product %s is not available!") % product.name
```



同时，记住翻译器要具有传递给下划线函数的字面量值才能生效，因此请尽量让它们更容易理解并保持杂散字符和格式化最小化。翻译器必须知道%s 或 %d这样的格式化模式，新行等需要被保留，但以有意义和明显地方式使用它们很重要：

```python
# 不妥: 让翻译难以处理
error = "'" + question + _("' \nPlease enter an integer value ")
 
# 更佳 (还要注意括号的位置!)
error = _("Answer to question %s is not valid.\n" \
          "Please enter an integer value.") % question
```



通常在Odoo中， 在操作字符串时更推荐使用`%` 而非 `.format()` (在字符串中仅有一个变量供替换时)，且推荐使用 `%(varname)` 而非位置参数 (在有多个变量供替换时)。这会让社区翻译翻译者更易于翻译。



#### 符号和惯例

##### 模型名 (使用点号标记符，前缀模块名) :

- 在定义Odoo模型时：使用名称的单数形式 (*res.partner* 和 *sale.order* 来取代 *res.partnerS* 和 *saleS.orderS*)
- 在定义Odoo 临时模型 (向导)时： 使用 `<related_base_model>.<action>` ，其中 *related_base_model* 是与临时模型相关的基模型 (在 *models/*中定义) ，*action* 是临时模型所做内容的短名称。
  - 避免使用 *wizard* 一词。例如： `account.invoice.make`, `project.task.delegate.batch`, …
- 在定义*report* 模型(如SQL视图) 时: 按照临时模型规范使用 `<related_base_model>.report.<action>`。

- Odoo Python类 : 使用驼峰(面向对象样式)。

  ```
  class AccountInvoice(models.Model):
      ...
  ```

##### 变量名 :

- 对模型变量使用驼峰

- 对普通变量使用下划线小写字母标记

- 在包含记录id或id列表时对变量名使用后缀 *_id* 或 *_ids* 。不要使用 `partner_id` 来包含res.partner的记录

  ```python
  Partner = self.env['res.partner']
  partners = Partner.browse(ids)
  partner_id = partners[0].id
  ```

- `One2Many` 和 `Many2Many` 字段应总是带有 *_ids* 作为后缀 (例: sale_order_line_ids)

- `Many2One` 字段应带有 *_id* 作为后缀 (示例 : partner_id, user_id, …)

  

##### 方法规范

- 计算字段：计算方法的模式为 *_compute_<field_name>*
- 搜索方法：搜索方法的模式为 *_search_<field_name>*
- 默认方法：默认方法的模式为*_default_<field_name>*
- 选择方法：选择方法的模式为 *_selection_<field_name>*
- Onchange方法 : onchange方法的模式为 *_onchange_<field_name>*
- 约束方法：约束方法的模式为 *_check_<constraint_name>*
- 动作方法：对象动作方法的前缀为*action_*。因其仅使用一条记录，在方法的开始处添加`self.ensure_one()`。



##### 模型中属性排序应为

1. 私有属性 (`_name`, `_description`, `_inherit`, …)

2. 默认方法和 `_default_get`

3. 字段声明

4. 计算、后向和搜索方法的排序与声明顺序相同

5. 选择方法 (用于返回针对选择字段计算值的方法)

6. 约束方法 (`@api.constrains`) 和 onchange方法 (`@api.onchange`)

7. CRUD方法 (ORM 重载)

8. s动作方法

9. 最后是其它业务方法。

   ```python
   class Event(models.Model):
       # 私有属性
       _name = 'event.event'
       _description = 'Event'
    
       # 默认方法
       def _default_name(self):
           ...
    
       # 字段声明
       name = fields.Char(string='Name', default=_default_name)
       seats_reserved = fields.Integer(oldname='register_current', string='Reserved Seats',
           store=True, readonly=True, compute='_compute_seats')
       seats_available = fields.Integer(oldname='register_avail', string='Available Seats',
           store=True, readonly=True, compute='_compute_seats')
       price = fields.Integer(string='Price')
       event_type = fields.Selection(string="Type", selection='_selection_type')
    
       # 计算和搜索字段，和字段声明的顺序一样
       @api.depends('seats_max', 'registration_ids.state', 'registration_ids.nb_register')
       def _compute_seats(self):
           ...
    
       @api.model
       def _selection_type(self):
           return []
    
       # 约束和onchange
       @api.constrains('seats_max', 'seats_available')
       def _check_seats_limit(self):
           ...
    
       @api.onchange('date_begin')
       def _onchange_date_begin(self):
           ...
    
       # CRUD方法(和 name_get, name_search, ...) 重载
       def create(self, values):
           ...
    
       # 动作方法
       def action_validate(self):
           self.ensure_one()
           ...
    
       # 业务方法
       def mail_user_confirm(self):
           ...
   ```

   





