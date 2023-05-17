##### 1) 使用背景

1. 使用Linux默认vim编辑器时，代码显示不美观，没有自动补全
2. 复制粘贴操作限制不方便，对于需要从其他地方转移过来调试的代码需要依赖第三方ssh软件，例：Xshell等



##### 2) 软件介绍

此时推荐一款跨平台开源编辑器软件：Visual Studio Code（简称“VS Code”）

```
Visual Studio Code是Microsoft在2015年4月30日Build开发者大会上正式宣布一个运行于 Mac OSX、Windows和 Linux 之上的，针对于编写现代Web和云应用的跨平台源代码编辑器，可在桌面上运行，并且可用于Windows，macOS和Linux。它具有对JavaScript，TypeScript和Node.js的内置支持，并具有丰富的其他语言（例如C++，C＃，Java，Python，PHP，Go）和运行时（例如.NET和Unity）扩展的生态系统。
```



##### 2.1) 主要功能

- 语法高亮（syntax high lighting）
- 可定制的热键绑定（customizable keyboard bindings）
- 括号匹配（bracket matching）
- 代码片段收集（snippets）
- 丰富的快捷键



***官网下载链接：https://code.visualstudio.com/Download***





#### 3）配置vscode软件语言为中文

##### 3.1 进入扩展中心（快捷键ctrl+shift+X）

##### 3.2 搜索chinese，安装语言包插件

##### 3.3 安装完成，重启软件使其生效







### 3.3）安装可以SSH到远程主机的Remote-SSH插件

##### 3.3.1 进入扩展中心，搜索Remote-SSH

##### 3.3.2 安装Remote-SSH插件

##### 3.3.3 插件安装完毕，左侧栏出现远程资源管理器入口

<img src='https://img-blog.csdnimg.cn/img_convert/a3bf0f940fc02679bf66c99778820003.png'>



##### 3.4）Vscode开启登陆终端（使用SSH插件远程时开启使用Linux主机的Bash功能）

##### 3.4.1 文件->首选项->设置->Show Login Terminal 打上勾

<img src='https://img-blog.csdnimg.cn/img_convert/0e04e4aa0cd9df048ef8fde27b9b56d8.png'>

##### 3.4.2 搜索Show Login Terminal，勾选开启该功能

<img src='https://img-blog.csdnimg.cn/img_convert/dd921d366968cf1ca0510543191a009a.png'>

##### vscode使用Remote-SSH插件连接远程主机





##### 点击+号添加创建SSH配置

<img src='https://img-blog.csdnimg.cn/img_convert/8eb0fd85e7b84e39c8e1e8dcd483ecf4.png'>



#####  填写远程目标主机账号名和IP地址（能解析到正确IP的域名也可）后，按Enter回车键

<img src='https://img-blog.csdnimg.cn/img_convert/cf7b69c9e3d8cc89415d5ddb9696830e.png'>

##### 选择将SSH配置信息保存到当前用户配置下，也可选择全局配置（第二个选项）

<img src='https://img-blog.csdnimg.cn/img_convert/eb6d6de7df7f3e90685ffe5089220d7c.png'>



##### 开始SSH访问远程主机

<img src='https://img-blog.csdnimg.cn/img_convert/63d88008b1ec998506bb55577957f411.png'> 



##### 选择目标主机类型>Linux

##### 如果出错：

<img src='https://img-blog.csdnimg.cn/302cf43306674a9dabde8f78db48005b.png#pic_center'>

<img src='https://img-blog.csdnimg.cn/8af8cbc9d80c476d8489145a98f270f0.png#pic_center'>

##### 下方终端窗口输入yes回车下一步

##### 输入远程主机密码按Enter回车下一步

#####  SSH访问成功！