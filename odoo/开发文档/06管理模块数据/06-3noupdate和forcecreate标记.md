##### 使用noupdate和forcecreate标记

大部分的插件模块拥有不同类型的数据。

- 有些数据只要存在模块就可正常运作
- 另一些数据不可由用户修改
- 大部分数据都可以供用户按需修改，仅出于方便目的予以提供。

本节会详细讲解这些不同类型的数据。首先，我们将在已有记录中写入一个字段，然后我们会创建一条在模块更新时会重新创建的记录。

##### 如何实现…

我们可以在加载数据时设置`<odoo>`元素或`<record>`元素自身的某些属性来对Odoo施加不同的行为，

-  添加在安装时会创建但后续升级中不更新的出版社。但在用户删除它时会被重新创建

  ```xml
  <odoo noupdate="1">
    <record id="res_partner_packt" model="res.partner">
      <field name="name">Packt publishing</field>
      <field name="city">Birmingham</field>
      <field name="country_id" ref="base.uk"/>
    </record>
  </odoo>
  ```

- 添加一个在插件更新时不会修改且用户删除后不会重建的图书分类(`forcecreate="False"`)

  ```xml
  <odoo noupdate="1">
    <record id="book_category_all"
      model="library.book.category"
      forcecreate="false">
      <field name="name">All books</field>
    </record>
  </odoo>
  ```

- 最后data.xml内容为

  ```xml
  <?xml version="1.0" encoding="UTF-8" ?>
  <odoo noupdate="1">
      <record id="res_partner_packt" model="res.partner">
          <field name="name">Packt Publishing</field>
          <field name="city">Birmingham</field>
          <field name="country_id" ref="base.uk"/>
      </record>
  
      <record id="book_category_all" model="library.book.category" forcecreate="False">
          <field name="name">All books</field>
      </record>
  </odoo>
  ```



##### 运行原理…

`<odoo>`元素可包含一个**noupdate属性**，在 ir.model.data记录中由第一次读取所包含的数据记录创建，因此成为数据表中的一个字段。

在Odoo安装插件时（称为 init 模式），不论noupdate为true或false都会写入所有记录。

在更新插件时（称为update模式），会查看已有的XML ID来确定是否设置了noupdate标记，如是，则会忽略准备写入到该XML ID 的元素。

在用户删除该记录时则并非如此，因此可以通过在update模式下设置记录的forcecreate标记为false来强制不重建noupdate记录。

> 📝**重要：**在老版本的插件中（版本8.0及以前），经常会发现<openerp>元素中包含一个<data>元素，其中又包含<record>及其它元素。这仍然可用，但已被弃用。现在，<odoo>, <openerp>和<data>的语法完全一致，它们作为XML数据的一个包裹。



##### 扩展知识…

如果在使用noupdate标记时依然想要加载记录，可以在运行Odoo服务时带上–init=your_addon或-i your_addon参数。这会强制Odoo重新加载记录。还会重建已删除的记录。注意如果模块绕过了XML ID机制的话这可能会导致重复记录以及关联安装出错，例如在用<function>标签调用Python代码来创建记录时。

通过这一代码，可以绕过noupdate标记，但首先请确保这确实是你所需要的。另一个解决这一场景的方案是编写一个迁移脚本，参见*插件更新和数据迁移*一节。



##### 其它内容

Odoo还使用XML ID来追踪插件升级后所删除的数据。如果记录在更新前通过模块命名空间获取到一个XML ID，但在更新时重置了该XML ID，记录会因被视作已过期而从数据库中删除。有关这一机制更深入的讨论，请见*插件更新和数据迁移*一节。

