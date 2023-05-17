- 在library.book中添加average_book_occupation() 方法：

  ```
  def average_book_occupation(self):
      self.flush()
      sql_query = """
          SELECT
              lb.name,
              avg((EXTRACT(epoch from age(return_date, rent_date)) / 86400))::int
          FROM
              library_book_rent AS lbr
          JOIN
              library_book as lb ON lb.id = lbr.book_id
          WHERE lbr.state = 'returned'
          GROUP BY lb.name;"""
      self.env.cr.execute(sql_query)
      result = self.env.cr.fetchall()
      _logger.info("Average book occupation: %s", result)
  ```

- 执行该查询

  ```
  self.env.cr.execute(sql_query)
  ```

- 获取结果并进行日志记录（注意应导入logger）

  ```
  result = self.env.cr.fetchall()
  logger.info("Average book occupation: %s", result)
  ```

- 在library.book模型的表单视图中添加一个按钮来触发我们的方法：

  ```
  <button name="average_book_occupation" string="Log Average Occ." type="object" />
  ```

  

第1步中，我们添加了average_book_occupation()方法，在用户点击Log Average Occ.按钮时会进行调用。

在第2步中，我们使用flush()方法。Odoo v13开始ORM中大量使用了缓存。ORM对每个事务使用一个全局缓存。这样数据库中的记录与ORM缓存中的记录数据可能会不同。在执行查询前使用flush()方法可以确保缓存中的所有修改被推送到数据库中。

第3步中，我们声明了一条SELECT查询SQL。这会返回用户持有某本书的平均天数。如果在PostgreSQL命令行运行这条查询，根据数据库中的图书数据会得到类似下面的结果：

第4步对存储在self.env.cr中的数据库游标调用execute(方法。这会发送查询到PostgreSQL并进行执行。

第5步使用游标的 fetchall()方法来获取由查询所得到的行的列表。该方法返回一个行的列表，本例中为 [(‘Odoo 12 Development Cookbook’, 33), (‘PostgreSQL 10 Administration Cookbook’, 81)]。通过我们执行的查询，可以知道每行有两个值，第一个为书名，另一个是用户持有这本书的平均天数。然后我们进行了日志记录。

第6步我们添加了按钮来处理用户动作。

> 📝**重要提示：**如果执行UPDATE查询，需要手动将缓存置为无效，因为Odoo ORM的缓存对UPDATE查询所做的改变是没有感知的。要将缓存置为无效，可使用self.invalidate_cache()。



##### 扩展知识…

self.env.cr中的对象是对psycopg2 游标的轻度封装。以下的方法是最常执行的一部分方法：

- execute(query, params)：通过params参数值元组替换查询中标记为%s的参数来执行SQL查询。

  > ⚠️**警告：**不要自行替换，保持使用%s这样的格式化选项，因为如果使用字符串拼接这类技术会带来SQL注入的风险。

- fetchone()：从数据库返回一行，以元组进行封装（即便是仅查询了一个字段）。

- fetchall()：以元组列表从数据库中返回所有行。

- dictfetchall()：以列名对值的映射字典列表返回数据库中的所有行。

在处理原生SQL查询时要非常小心：

- 你跳过了所有应用层面的权限。请确保调用search([(‘id’, ‘in’, tuple(ids)]) 时传递id 列表过滤掉所有用户无权访问的记录。
- 你所做的修改不受插件模块中所设置的约束限制，除在数据库层面所强制的NOT NULL, UNIQUE和FOREIGN KEY约束。对于计算字段的重新计算触发器也是如此，因而可能会导致数据库的崩溃。
- 避免使用INSERT/UPDATE语句，因为通过语句插入或更新记录不会执行create() 和 write()中重写的业务逻辑。它不会更新已存储的计算字段并且会跳过ORM约束。