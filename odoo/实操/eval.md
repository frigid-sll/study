##### eval是对关联字段进行操作，多关系字段的写入方法,0-6分别是什么含义?



##### One2many

- 使用
  - （0,0,{values}） 根据values里面的信息新建一个记录
  - （1，ID，{values}），这里的ID是指o2m中的m表的记录ID，更新id=ID的记录
  - （2，ID），删除id=ID的数据（相当于用了unlink，删除数据以及整个主从数据连接关系）

- One2many举例：

  ```
  create({‘order_line_ids’:[(0,0,{‘line表中的字段’:’值’})]})
  write（{‘order_line_ids’:[(1,10，{‘line表中的字段’:’值’})]}）
  Write（{’order_line_ids‘:[(2，10)]}），删除line表中id=10的记录
  ```



##### Many2many：

- 使用
  - （0,0,{values}） 根据values里面的信息新建一个记录
  - （1，ID，{values}），这里的ID是指o2m中的m表的记录ID，更新id=ID的记录
  - （2，ID），删除id=ID的数据（相当于用了unlink，删除数据以及整个主从数据连接关系）
  - （3,ID） 切断主从链接关系但不会删除这个记录
  - （4，ID） 为id=ID的数据添加主从链接关系
  - （5，），删除所有的从数据的链接关系，等价于向所有的从数据调用（3，ID）
  - （6，0，[IDs]）,用ID里面的记录替换原来的记录，等价于使用了(5,)后循环使用（4，id）

- Many2many举例：

  ```xml
  <record id="base.group_website_publisher" model="res.groups">
      <field name="name">Display Editor Bar on Website</field>
      <field name="category_id" ref="base.module_category_website"/>
  </record>
  <record id="base.group_website_designer" model="res.groups">
      <field name="name">Manage Website and qWeb view</field>
      <field name="users" eval="[(4, ref('base.user_root'))]"/>
      //当前权限组适用的用户：ref('base.user_root')里所有
      <field name="implied_ids" eval="[(4, ref('base.group_website_publisher'))]"/>
      //继承的权限：ref('base.group_website_publisher')里所有
      <field name="category_id" ref="base.module_category_website"/>
  </record>
  ```

  