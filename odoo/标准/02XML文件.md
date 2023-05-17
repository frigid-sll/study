#### XML文件

##### 格式

要在XML中声明记录，推荐使用 **record** 标记符 (使用 *<record>*) ：

- 在`model`前放置`id`属性
- 对于字段声明，首先为`name` 属性。然后将值要么放到 `field` 标签中，要么放到`eval` 属性中，最终其它属性 (widget, options, …)按重要性排序。
- 尝试通过模型对记录分组。在动作/菜单/视图之间依赖的情况下，可能无法应用这一惯例。
- 使用在下一点中定义的命名规范
- 标签*<data>*仅用于通过`noupdate=1`设置不可更新的数据。如果在文件中仅存在不可更新数据，可对`<odoo>`标签设置`noupdate=1`且不设置 `<data>` 标签。

```xml
<record id="view_id" model="ir.ui.view">
    <field name="name">view.name</field>
    <field name="model">object_name</field>
    <field name="priority" eval="16"/>
    <field name="arch" type="xml">
        <tree>
            <field name="my_field_1"/>
            <field name="my_field_2" string="My Label" widget="statusbar" statusbar_visible="draft,sent,progress,done" />
        </tree>
    </field>
</record>
```



Odoo支持自定义标签来作为语法糖：

- menuitem: 使用它来作为声明`ir.ui.menu`的快捷方式
- template: 使用它来声明仅要求视图中`arch`版块的 QWeb视图。
- report: 用于声明[报表动作](https://alanhou.org/odoo-13-actions/#reference-actions-report)
- act_window: 在record标记符无法实现时使用它

前4个标签的推荐度高于 *record* 标记。



#### XML ID和命名

##### 安全、视图和动作

使用如下模式：

- 对于菜单：`*<model_name>*_menu`, 或是什么子菜单用 `*<model_name>*_menu_*do_stuff*` 。
- 对于视图： `*<model_name>*_view_*<view_type>*`, 其中的*view_type* 为 `kanban`, `form`, `tree`, `search`, …
- 对于动作: 主动作为 `*<model_name>*_action`。其它使用`_*<detail>*`作为后缀，其中*detail* 为简洁地解释动作的小写字符串。仅用于多个动作对模型进行声明时。
- 对于窗口动作： 通过具体的视图信息如 `*<model_name>*_action_view_*<view_type>*`对动作名进行后缀。
- 对于组: `*<model_name>*_group_*<group_name>*` 其中 *group_name* 是组的名称，通常为‘user’, ‘manager’, …
- 对于规则: `*<model_name>*_rule_*<concerned_group>*` 其中*concerned_group* 是相关组的短名称 (‘user’对应‘model_name_group_user’, ‘public’对应公共用户, ‘company’ 对应多租户规则, …).

名称应与xml id相同，使用点号替换下划线。动作应有一个真实命名，因为它用作显示名。

```xml
<!-- views  -->
<record id="model_name_view_form" model="ir.ui.view">
    <field name="name">model.name.view.form</field>
    ...
</record>
 
<record id="model_name_view_kanban" model="ir.ui.view">
    <field name="name">model.name.view.kanban</field>
    ...
</record>
 
<!-- actions -->
<record id="model_name_action" model="ir.act.window">
    <field name="name">Model Main Action</field>
    ...
</record>
 
<record id="model_name_action_child_list" model="ir.actions.act_window">
    <field name="name">Model Access Childs</field>
</record>
 
<!-- menus and sub-menus -->
<menuitem
    id="model_name_menu_root"
    name="Main Menu"
    sequence="5"
/>
<menuitem
    id="model_name_menu_action"
    name="Sub Menu 1"
    parent="module_name.module_name_menu_root"
    action="model_name_action"
    sequence="10"
/>
 
<!-- security -->
<record id="module_name_group_user" model="res.groups">
    ...
</record>
 
<record id="model_name_rule_public" model="ir.rule">
    ...
</record>
 
<record id="model_name_rule_company" model="ir.rule">
    ...
</record>
```



##### 继承XML

继承视图的Xml Id应使用与原记录相同的ID。它有助于一眼看到所有的继承。因最终的 Xml Id会使用所创建的模块作为前缀，所以不会产生重叠。

命名应包含一个 `.inherit.{details}` 后缀来有且于在查看名称时理解重载的目的。

```xml
<record id="model_view_form" model="ir.ui.view">
    <field name="name">model.view.form.inherit.module2</field>
    <field name="inherit_id" ref="module1.model_view_form"/>
    ...
</record>
```



新的主要视图不要求继承后缀，因为它们是基于第一个的新记录。

```xml
<record id="module2.model_view_form" model="ir.ui.view">
    <field name="name">model.view.form.module2</field>
    <field name="inherit_id" ref="module1.model_view_form"/>
    <field name="mode">primary</field>
    ...
</record>
```

