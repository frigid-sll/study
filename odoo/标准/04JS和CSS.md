#### Javascript和CSS

##### 静态文件组织

Odoo插件具有架构各个文件的一些规范。我们这讲解如何组织网页资源的更多详情。

第一件事是要知道Odoo服务会对位于*static/*文件夹中的所有文件（静态地）提供服务， 但会使用插件名前缀。例如，如果文件位于 *addons/web/static/src/js/some_file.js*，那就可以通过 url *your-odoo-server.com/web/static/src/js/some_file.js*来静态获取

规范为根据如下结构组织代码：

- static： 通用的所有静态文件

  - *static/lib*: 这是js库应该处于的位置，位于子文件夹中。 因此，例如， *jquery* 库中的所有文件位于*addons/web/static/lib/jquery*中

  - static/src： 通用静态源代码文件夹

    - *static/src/css*: 所有css文件
    - *static/src/fonts*
    - *static/src/img*
    - static/src/js
      - *static/src/js/tours*: 终端用户导览文件 (教程，非测试)
    - *static/src/scss*: scss 文件
    - *static/src/xml*: 所有会在JS中渲染的qweb模板

  - static/tests

    : 这里放置所胡测试相关的文件。

    - *static/tests/tours*: 这里放置所有导览测试文件 (非教程)。



##### Javascript编码指南

- `use strict;` 推荐在所有javascript文件中使用
- 使用一种linter (jshint, …)
- 永远不要添加最小化混淆 Javascript库
- 对类声明使用驼峰名

更精确的JS指南在[github wiki](https://github.com/odoo/odoo/wiki/Javascript-coding-guidelines)中进行详细讲解。还可以通过查看Javascript手册来查看Javascript中已有的API。



##### CSS编码指南

- 对所有类添加 *o_<module_name>* 前缀，其中*module_name* 是模块的技术名称(‘sale’, ‘im_chat’, …) 或模块所保留的主路由(主要针对website模块，如‘o_forum’ 对应 *website_forum* 模块)。 这一规则的唯一例外是网页客户端：它仅使用*o_* 前缀。
- 避免使用*id* 标签
- 使用Bootstrap原生类
- 使用下划线小写字母标记来命名类