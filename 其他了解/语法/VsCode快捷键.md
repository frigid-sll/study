VsCode自从诞生以来，以其各自优异的特性迅速走红。尤其是对于前端开发小伙伴来说，几乎成为必不可少的开发工具。所以，熟练掌握VsCode的各自使用技巧与调试技巧会让你的日常开发工作效率倍增。本文将会以大量图文的方式，从下面几个方面详细介绍VsCode的各种技巧：

- 第一部分主要介绍VsCode的基本技巧，比如常用快捷键、辅助标尺等。熟悉此部分的可以直接跳过。
- 第二部分主要各种断点（比如日志断点、内联断点、表达式断点等等）、数据面板等等
- 第三部分主要讲解各种项目的调试实战，比如Node程序、TS程序、Vue程序、Electron程序、Html等的调试实战
- 最后一部分将会讲解其他有用的技巧，比如代码片段、重构、Emmet等等



#### 基本技巧

##### 快速启动

VsCode安装后，会自动写入环境变量，终端输入`code`即可唤起VsCode应用程序。



##### 常用快捷键

- `ctrl + p`快速搜索文件并跳转，添加`:`可以跳转到指定行

![图片](https://mmbiz.qpic.cn/mmbiz/pfCCZhlbMQQEFUQlAswcpwFclVlpWXdS8ojNCKS5PP9PEHv6KLhFAt4lltJUzAx73LDkPVqeiaTZ4uQqs1KUatw/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1)image.png

- `ctrl + shift + p` 根据您当前的上下文访问所有可用命令。
- `ctrl + shift + c`在外部打开终端并定位到当前项目路径
- `ctrl + 按键1左边的符号`显示隐藏终端面板
- `Ctrl+B` 切换侧边栏
- `Ctrl+\` 快速拆分文件编辑
- `alt + 单机左键` 添加多处光标
- `alt + shift + 单击左键` 同一列所有位置添加光标
- `alt + shift + 鼠标选择` 选择相同开始和结束的区域

![图片](https://mmbiz.qpic.cn/mmbiz/pfCCZhlbMQQEFUQlAswcpwFclVlpWXdS4qvIsMByAeZGO8qnNYTTejLDvMbRKx5aZ7deTJMbbMLkJhEQYQeE0w/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1)image.png

- `alt + 上键或下键` 将当前行或者选中的区域上移/下移一行



##### 垂直标尺

在配置文件中添加如下配置，可以增加字符数标尺辅助线

```
"editor.rulers": [40, 80, 100]
复制代码
```

![图片](https://mmbiz.qpic.cn/mmbiz/pfCCZhlbMQQEFUQlAswcpwFclVlpWXdSASzXbXUvuuQCAkUuL7ic0xMmWbl4Y0yH0WdulStnibu4q8s3bwPZvmIQ/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1)image.png



#### 进阶技巧

##### 断点的基本使用

下面以在VsCode中快速调试一个Node项目为例，演示断点的基本使用。后文会继续结束各种高级断点。

- 创建一个基本的node项目为Nodejs
- 打开左侧调试面板，选择你要调试的node项目名称，添加调试配置

![图片](https://mmbiz.qpic.cn/mmbiz/pfCCZhlbMQQEFUQlAswcpwFclVlpWXdS3pej1obgyU3GmJlesv3YPuBzXlmdteqnjspJqIpkJkBAhsfdykJ8ZQ/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1)image.png

- 选择调试的项目类型为Node.js

![图片](https://mmbiz.qpic.cn/mmbiz/pfCCZhlbMQQEFUQlAswcpwFclVlpWXdSazicy9WBQbick8FiaOgbmywqgXKcjjyicPib6wtoRHkW9cdQK5Kjxv425Yg/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1)image.png

- 打开生成的.vscode/launch.json文件，指定程序入口文件

`program`字段用于指定你的程序入口文件，`${workspaceFolder}`表示当前项目根路径

![图片](https://mmbiz.qpic.cn/mmbiz/pfCCZhlbMQQEFUQlAswcpwFclVlpWXdSq1C9ZXkicsY0S9DdmiaSfww9z6wiaB8yB6qwMkvrYjlIxpTpF7EnwVt0A/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1)image.png

- 在程序中添加断点，只需要点击左侧的边栏即可添加断点

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)image.png

- 按`F5`开始调试，成功调试会有浮窗操作栏

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)image.png

浮窗的操作按钮功能依次为：

- 继续(`F5`)、
- 调试下一步(`F10`)、
- 单步跳入(`F11`)、
- 单步跳出(`Shift F11`)、
- 重新调试(`Ctrl + Shift + F5`)、
- 结束调试(`Shift + F5`)



##### 日志断点

日志断点是普通断点的一种变体，区别在于**不会中断调试**，而是可以把信息记录到控制台。日志断点对于调试无法暂停或停止的服务时特别有用。步骤如下:

- 添加日志断点的步骤

![图片](https://mmbiz.qpic.cn/mmbiz/pfCCZhlbMQQEFUQlAswcpwFclVlpWXdSzicgOHo93EWruHq4J0qy79mG7v31lDJ03ibh4gNpraWRrQgIib7f1YoeA/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1)image.png

- 输入要日志断点的信息，点击回车添加完成

可以使用`{}`使用变量，比如`在此处添加日志断点，b的值为${b}`

![图片](https://mmbiz.qpic.cn/mmbiz/pfCCZhlbMQQEFUQlAswcpwFclVlpWXdSVCTJHvkIanVJvVjojic8NyVMR1icErz5h9uLGnzHJnibI3eInMvfTxPXA/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1)image.png

- 日志断点添加成功后会有是一个菱形图标

![图片](https://mmbiz.qpic.cn/mmbiz/pfCCZhlbMQQEFUQlAswcpwFclVlpWXdSicIy5vSvgIV2AsLBrAtbUZQhMsA7Mjg4TlNntibAmxREiavFKpmFicNjNg/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1)image.png

- 按`F5`运行查看调试结果

![图片](https://mmbiz.qpic.cn/mmbiz/pfCCZhlbMQQEFUQlAswcpwFclVlpWXdSnJepiaAcI4rL6BdzxRDQ7lemum0MWnargicagcAPiaezsVS98myPn2S7A/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1)image.png



##### 表达式条件断点

条件断点是表达式结果为`true`时才会进行断点，步骤如下:

- 在代码行左侧右击，也可以添加断点，此处选择添加条件断点

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)image.png

- 填写表达式，按回车键

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)image.png

- 添加成功的小图标如下

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)image.png

- 按`F5`调试，条件成立所以进行了断点

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)image.png



##### 命中计数断点

只有该行代码命中了指定次数，才会进行断点。步骤如下:

- 选择条件断点，切换为命中次数选项，填写命中次数

![图片](https://mmbiz.qpic.cn/mmbiz/pfCCZhlbMQQEFUQlAswcpwFclVlpWXdSa7iasVvde0rEkGJicgicN51JJvZNNInjlV9mkEFPlw6phCJPwiaOCzgesg/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1)image.png

- 填写成功如下图所示

![图片](https://mmbiz.qpic.cn/mmbiz/pfCCZhlbMQQEFUQlAswcpwFclVlpWXdSzRyWAbibT8O2flPf7qZpsMVIMyXenrethbib2LdNyahbMVzgqmMzHf0g/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1)image.png

- 按`F5`调试，如图所示，index为9时才中断

![图片](https://mmbiz.qpic.cn/mmbiz/pfCCZhlbMQQEFUQlAswcpwFclVlpWXdSVPe0sbLOKbclRD4ygb8hoibvYXJrDYPL3faJj3xWnBJ6w1MYrbuy1kQ/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1)image.png



##### 内联断点

仅当执行到达与内联断点关联的列时，才会命中内联断点。这在调试在一行中包含多个语句的缩小代码时特别有用。比如for循环，短路运算符等一行代码包含多个表达式时会特别有用。步骤如下:

- 在指定位置按`Shift + F9`

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)image.png

- 调试之后，每次运行到该内联处的代码都会中断

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)image.png



##### 补充知识点：数据面板介绍

- 数据面板可以查看所有变量

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)image.png

- 在变量上点击右键，可以设置变量值、复制变量值等操作

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)image.png

- 聚焦于数据面板时，可以通过键入值来搜索过滤。点击下图所示按钮可以控制是否筛选。

![图片](https://mmbiz.qpic.cn/mmbiz/pfCCZhlbMQQEFUQlAswcpwFclVlpWXdSqOfhbNrMial45icpqaQXZG5Rl5ZqDU6ibj1xWKdX1usMxYdbLPrHqDR6g/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1)image.png

![图片](https://mmbiz.qpic.cn/mmbiz/pfCCZhlbMQQEFUQlAswcpwFclVlpWXdS1PiaVoicl0lDFJYknqm8qDneSDm7Z7VrZLWkfN5Skolb30dWW1dWgBMw/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1)image.png



##### 补充知识点：监听面板介绍

可以将变量添加到监听面板，实时观察变量的变化。

- 在变量面板通过右键选择“添加到监视”将变量添加到监听面板

![图片](https://mmbiz.qpic.cn/mmbiz/pfCCZhlbMQQEFUQlAswcpwFclVlpWXdSNdiaryh0BIoSU4YLoGlnwBh7lDg0grhn6jJfiaJE6p0qsSoyibeBiaLeqA/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1)image.png

- 也可以直接在监听面板选择添加按钮进行变量添加

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)image.png

- 添加变量后就可以实时监听变量的变化

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)image.png



##### 补充知识点：调试服务器时打开一个URI

开发 Web 程序通常需要在 Web 浏览器中打开特定 URL，以便在调试器中访问服务器代码。VS Code 有一个内置功能“ serverReadyAction ”来自动化这个任务。

- 一段简单的server代码

```
var express = require('express');
var app = express();

app.get('/', function(req, res) {
  res.send('Hello World!');
});

app.listen(3000, function() {
  console.log('Example app listening on port 3000!');
});
复制代码
```

- 配置launch.json，以支持打开URI

```
{
  "type": "node",
  "request": "launch",
  "name": "Launch Program",
  "program": "${workspaceFolder}/app.js",

  "serverReadyAction": {
    "pattern": "listening on port ([0-9]+)",
    "uriFormat": "http://localhost:%s",
    "action": "openExternally"
  }
}
复制代码
```

`pattern`是设置匹配的程度端口号，端口号放在小括号内，即作为一个正则的捕获组使用。`uriFormat`映射为URI，其中`%s`使用`pattern`中的第一个捕获组替换。最后使用该URI作为外部程序打开的URI。

- 按`F5`调试，会自动打开浏览器，且会在下图所示处中断，当继续执行后，浏览器才能看到输出了server的内容

![图片](https://mmbiz.qpic.cn/mmbiz/pfCCZhlbMQQEFUQlAswcpwFclVlpWXdSxAb9CVfg62vGEDu2Tzn8ql42TocnxuOtBfBibbdxM9w8pQ8kxiaorEnA/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1)image.png



#### 终局：各场景调试实战

##### 调试NodeJS项目

关于NodeJs项目的调试方法，已经在上述的**断点的基本使用**[1]部分做了介绍，可以网上滚动翻阅。



##### 调试Typescript项目

- 调试TS项目前，先创建一个TS项目

  ```
  # 终端运行
  tsc --init
  复制代码
  ```

  VS Code 内置了对 Ts 调试的支持。为了支持调试 Ts 与正在执行的 Js 代码相结合，VS Code 依赖于调试器的source map在 Ts 源代码和正在运行的 Js 之间进行映射，所以需要需要开启`sourceMap`选项。

  ```
  {
    "sourceMap": true,
    "outDir": "./out"
  }
  复制代码
  ```

  ```
  const num: number = 123;
  console.log(num);
  
  function fn(arg: string): void {
  console.log('fn', arg);
  }
  
  fn("Hello");
  复制代码
  ```

- - 新建index.ts文件，写一个基本的ts代码
  - 打开`tsconfig.json`文件，开启sourceMap选项和指定编译后输出的路径
  - 先初始化一个ts程序，生成默认的`tsconfig.json`文件

- 手动编译调试TS

  在上述的ts基本项目中：

  ![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)image.png

  ![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)image.png

  ![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)image.png

  ![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)image.png

- - 按`F5`或者`运行 -> 启动调试`，此时可以看到可以正常debug调试
  - 在index.ts中随意添加一个断点
  - 此时可以看到生成了out文件夹，里面包含一个`index.js`和一个`index.js.map`文件
  - 终端执行ts的编译命令`tsc`

- 通过构建任务构建调试TS

  ![图片](https://mmbiz.qpic.cn/mmbiz/pfCCZhlbMQQEFUQlAswcpwFclVlpWXdSsjVGOK23bnoIUriagxWFYIbGIz2Xa2b3SdEA9pcBTHksYH6iau8Zic0mg/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1)image.png

  ![图片](https://mmbiz.qpic.cn/mmbiz/pfCCZhlbMQQEFUQlAswcpwFclVlpWXdSyBFpbM1ErsmRK5d7xQwuv4YGuicV0eftibw42lO865iblViaicJQ859cjlQ/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1)image.png

  注意，如果你使用的是其他终端(比如`cmder`)的话，有可能会生成不了，如下图所示，使用默认的powershell即可：

  ![图片](https://mmbiz.qpic.cn/mmbiz/pfCCZhlbMQQEFUQlAswcpwFclVlpWXdSRvXWPBa6j716gzIzciaYiadcPDodOEnTCbicTWCibibMw4Q8rsxNnjh1ZUw/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1)image.png

- - 调试的话和上述步骤一样，在有了编译后的文件后，按`F5`即可
  - 选择`tsc构建选项`，此时可以看到自动生成了编译文件
  - 按`Ctrl+Shift+B`或选择`终端 -> 运行生成任务`，此时会弹出一个下拉菜单

- 监视改变并实时编译

  ![图片](https://mmbiz.qpic.cn/mmbiz/pfCCZhlbMQQEFUQlAswcpwFclVlpWXdSaM6ogSFOWCQ7GicruII7k2RwvMy8DXXEnuPnt7PC689wkoKeydfgPHg/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1)image.png

  ![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)image.png

- - 如下图所示，会实时编译
  - 按`Ctrl + Shift + B`选择监视选项，可以实时监视文件内容发生变化，重新编译



##### 补充知识点：tasks配置文件的创建方式

- 方法1：点击`终端 -> 配置任务 -> 选择任务`可以生成对应的tasks.json配置

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)image.png

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)image.png

- 方法2：点击`终端 -> 运行生成任务 -> 点击设置图标`也可以生成对应的tasks.json配置

![图片](https://mmbiz.qpic.cn/mmbiz/pfCCZhlbMQQEFUQlAswcpwFclVlpWXdS8lr5ba96Xpy9oIZ9rw2a17aiaeAMGRP6fR2h2TIqKH04ckPmCDSpISw/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1)image.png

![图片](https://mmbiz.qpic.cn/mmbiz/pfCCZhlbMQQEFUQlAswcpwFclVlpWXdStoXJFcZCIDNTgadI8Y78R2lvq4FP58YF21YjjmNl6CV6hmFmFqoUBw/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1)image.png



##### 补充知识点：每次调试时重新编译

- 按上述的操作已经生成了task.json配置文件

```
{
 "version": "2.0.0",
 "tasks": [
    {
      "type": "typescript",
      "tsconfig": "tsconfig.json",
      "problemMatcher": [
        "$tsc"
      ],
      "group": "build",
      "label": "tsc: 构建 - tsconfig.json"
    }
  ]
}
复制代码
```

- 点击`运行 -> 添加配置 -> 选择nodejs`

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)image.png

- 在生成的`launch.json`文件中，添加`preLaunchTask`字段，值是`tasks.json`的`label`值，一定要相同，注意大小写。该字段的作用是在执行命令前先执行改`task`任务。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)image.png

注意，如果编译后的js文件不在相应的位置，通过图中的`outFiles`字段可以指定`ts`编译后的`js`路径。

- 在`index.ts`文件中按`F5`启动调试，可以看到调试前已经生成了编译文件，而后就可以正常调试了。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)image.png



##### 补充知识点：VsCode的TS版本说明

- vscode本身内置了对ts的支持
- vscode内置的ts版本（即工作区版本），仅仅用于IntelliSense（代码提示），工作区ts版本与用于编译的ts版本无任何关系。

修改工作区ts版本的方法：

- 在状态栏选择typescript的图标，选择版本切换

![图片](https://mmbiz.qpic.cn/mmbiz/pfCCZhlbMQQEFUQlAswcpwFclVlpWXdSyT2PqqCKxTFO1FOqicffbeZrqTzjM6yRvAGuLRechpDQ4icZpSOMsJmQ/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1)image.png

- 选择你需要的版本即可

![图片](https://mmbiz.qpic.cn/mmbiz/pfCCZhlbMQQEFUQlAswcpwFclVlpWXdSoBlEQlYDkUhZTzOibulz5wwZNuskEswTOeMicHt8NwVor0ROpvTc49qg/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1)image.png

![图片](https://mmbiz.qpic.cn/mmbiz/pfCCZhlbMQQEFUQlAswcpwFclVlpWXdSia7bxGAr3LKTaGJCVOHcYNjONOPzejnSxkrPbFTvEsTS9ficX8zibT9GQ/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1)image.png



##### 调试html项目

学会了上述ts的调试后，我们尝试调试html文件，并且html文件中引入ts文件:

- 创建html，引入ts编译后的js文件

```
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document</title>
</head>
<body>
  <h3>Hello</h3>
  <script src="./out/index.js"></script>
</body>
</html>
复制代码
```

- ts源文件如下：

```
const num: number =  1221;
console.log(num);

function fn(arg: string): void {
  console.log('fn', arg);
}

document.body.append('World')

fn("he");
复制代码
```

- 打debug

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)image.png

- launch.json启动命令配置

```
{
  // 使用 IntelliSense 了解相关属性。 
  // 悬停以查看现有属性的描述。
  // 欲了解更多信息，请访问: https://go.microsoft.com/fwlink/?linkid=830387
  "version": "0.2.0",
  "configurations": [
    {
      "type": "pwa-chrome",
      "request": "launch",
      "name": "Launch Chrome",
      "url": "file:///E:/demo/vscode/debug/ts/index.html",
      "preLaunchTask": "tsc: 构建 - tsconfig.json",
      "webRoot": "${workspaceFolder}"
    }
  ]
}
复制代码
```

- 选择我们的启动命令

![图片](https://mmbiz.qpic.cn/mmbiz/pfCCZhlbMQQEFUQlAswcpwFclVlpWXdSvdCAdeRkUYxKLEgeRFVk8xFBpJmneiaAdEL3VUqiaIKEtZwFGfbjEVDQ/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1)image.png

- 按`F5`可以正常唤起chrome浏览器，并在vscode的ts源码处会有debug效果



#### 调试Vue项目的两种方式

下面介绍两种调试vue2项目的3种方法，其他框架的调试也类似：



##### 不使用vscode插件Debugger for chrome的方法

- 初始化vue项目，配置`vue.config.js`，指定要生成sourceMaps资源

```
module.exports = {
  configureWebpack: {
    // 生成sourceMaps
    devtool: "source-map"
  }
};
复制代码
```

- 根目录下创建`./vscode/launch.json文件` 或者选择`运行 -> 添加配置 -> Chrome`

![图片](https://mmbiz.qpic.cn/mmbiz/pfCCZhlbMQQEFUQlAswcpwFclVlpWXdSmQ3DWMmO132vcPksh9NCH5UTHq0ibbdXzvyBfRUxPZL57S29XstWtJQ/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1)image.png

```
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "chrome",
      "request": "launch",
      "name": "vuejs: chrome",
      "url": "http://localhost:8080",
      "webRoot": "${workspaceFolder}",
      "breakOnLoad": true,
      "pathMapping": {
        "/_karma_webpack_": "${workspaceFolder}"
      },
      "sourceMapPathOverrides": {
        "webpack:/*": "${webRoot}/*",
        "/./*": "${webRoot}/*",
        "/src/*": "${webRoot}/*",
        "/*": "*",
        "/./~/*": "${webRoot}/node_modules/*"
      },
      "preLaunchTask": "serve"
    }
  ]
}

复制代码
```

- 添加任务脚本

```
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "serve",
      "type": "npm",
      "script": "serve",
      "isBackground": true,
      "problemMatcher": [
        {
          "base": "$tsc-watch",
          "background": {
            "activeOnStart": true,
            "beginsPattern": "Starting development server",
            "endsPattern": "Compiled successfully"
          }
        }
      ],
      "group": {
        "kind": "build",
        "isDefault": true
      }
    }
  ]
}
复制代码
```

该脚本的作用是运行`npm run serve`编译命令。

- 按`F5`启动调试即可

注意：此方式的主要点在于`launch.json`配置文件中，通过`preLaunchTask`字段指定调试前先运行一个任务脚本，`preLaunchTask`的值对应`tasks.json`文件中的`label`值。

更多详细内容，大家可以点击这里的**参考文档**[2]查阅。



##### 借助vscode插件Debugger for Chrome在Chrome中调试

- 第一步还是初始化vue项目，添加`vue.config.js`文件配置，指定要生成sourceMaps资源

```
module.exports = {
  configureWebpack: {
    // 生成sourceMaps
    devtool: "source-map"
  }
};
复制代码
```

- vscode中扩展中安装`Debugger for Chrome`插件，并确保没有禁用插件

![图片](https://mmbiz.qpic.cn/mmbiz/pfCCZhlbMQQEFUQlAswcpwFclVlpWXdSXIkx04qz8xdwaAZy5SJBMIkvfFAnOngB5kWRjTaPVtm3gpFTdJ1Hbg/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1)image.png

- 手动启动项目的运行, 此方式不需要配置`tasks.json`任务

```
# 终端执行命令，启动项目
npm run serve
复制代码
```

- 按`F5`启动调试即可

![图片](https://mmbiz.qpic.cn/mmbiz/pfCCZhlbMQQEFUQlAswcpwFclVlpWXdSdUySUiapY8mpiciceicCKBaUQEUTV9uWvKg8nPcHkvSx78elYfAUJSWhPQ/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1)image.png

更多详细内容，请点击这里的**参考文档**[3]查阅。



##### 借助vscode插件`Debugger for Firfox`在Firefox中调试

- 和`Debugger for Chrome`基本一样，区别在于安装`Debugger for Firfox`插件，并在launch.json配置中，增加调试Firefox的配置即可，配置如下

```
{
  "version": "0.2.0",
  "configurations": [
    // 省略Chrome的配置...
    // 下面添加的Firefox的配置
    {
      "type": "firefox",
      "request": "launch",
      "reAttach": true,
      "name": "vuejs: firefox",
      "url": "http://localhost:8080",
      "webRoot": "${workspaceFolder}/src",
      "pathMappings": [{ "url": "webpack:///src/", "path": "${webRoot}/" }]
    }
  ]
}
复制代码
```

- 调试时选择对应的调试命令即可

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)image.png

> Firefox初始启动时不会触发调试，需要刷新一次



##### 调试Electron项目

Electron很多人都使用过，主要用于开发跨平台的系统桌面应用。那么来看下`vue-cli-electron-builder`创建的`Electron`项目怎么调试。步骤如下：

- 在初始化项目后，首先修改`vue.config.js`文件配置，增加sourceMaps配置：

```
module.exports = {
  configureWebpack: {
    devtool: 'source-map'
  }
}
复制代码
```

- 创建调试配置`.vscode/launch.json`

```
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Electron: Main",
      "type": "node",
      "request": "launch",
      "protocol": "inspector",
      "preLaunchTask": "bootstarp-service",
      "runtimeExecutable": "${workspaceRoot}/node_modules/.bin/electron",
      "windows": {
        "runtimeExecutable": "${workspaceRoot}/node_modules/.bin/electron.cmd"
      },
      "args": ["--remote-debugging-port=9223", "./dist_electron"],
      "outFiles": ["${workspaceFolder}/dist_electron/**/*.js"]
    },
    {
      "name": "Electron: Renderer",
      "type": "chrome",
      "request": "attach",
      "port": 9223,
      "urlFilter": "http://localhost:*",
      "timeout": 0,
      "webRoot": "${workspaceFolder}/src",
      "sourceMapPathOverrides": {
        "webpack:///./src/*": "${webRoot}/*"
      }
    },
  ],
  "compounds": [
    {
      "name": "Electron: All",
      "configurations": ["Electron: Main", "Electron: Renderer"]
    }
  ]
}
复制代码
```

此处配置了两个调试命令: `Electron: Main`用于调试主进程，`Electron: Renderer`用于调试渲染进程；`compounds[].`选项用于定义复合调试选项; `configurations`定义的复合命令是**并行的**; `preLaunchTask`用于配置命令执行前先执行的任务脚本，其值对应`tasks.json`中的`label`字段; `preLaunchTask`用在`compounds`时，用于定义`configurations`复合任务执行前先执行的脚本。

- 创建任务脚本

```
{
  // See https://go.microsoft.com/fwlink/?LinkId=733558
  // for the documentation about the tasks.json format
  "version": "2.0.0",
  "tasks": [
    {
      "label": "bootstarp-service",
      "type": "process",
      "command": "./node_modules/.bin/vue-cli-service",
      "windows": {
        "command": "./node_modules/.bin/vue-cli-service.cmd",
        "options": {
          "env": {
            "VUE_APP_ENV": "dev",
            "VUE_APP_TYPE": "local"
          }
        }
      },
      "isBackground": true,
      "args": [
        "electron:serve", "--debug"
      ],
      "problemMatcher": {
        "owner": "custom",
        "pattern": {
          "regexp": ""
        },
        "background": {
          "beginsPattern": "Starting development server\\.\\.\\.",
          "endsPattern": "Not launching electron as debug argument was passed\\."
        }
      }
    }
  ]
}
复制代码
```

- 启动调试

在主进程相关代码上打上断点，然后启动调试主进程命令就可以调试主进程了

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)image.png

注意，这里的`options`参数是根据实际的情况，自定义添加我们运行项目时所需要的参数，比如我这里因为启动项目的npm命令是:

```
"serve-local:dev": "cross-env VUE_APP_TYPE=local VUE_APP_ENV=dev vue-cli-service electron:serve"
复制代码
```

- 主进程调试成功

![图片](https://mmbiz.qpic.cn/mmbiz/pfCCZhlbMQQEFUQlAswcpwFclVlpWXdSOmRQIVcR69E6fPanycfOMySSRkmLicdE2UAqsGccs5UbTtagMO9l05Q/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1)image.png

- 开始调试渲染进程

切换到渲染进程的调试选项，在渲染进程的代码处打上断点，点击调试。注意，此时并不会有断点终端，需要`ctrl+r`手动刷新软件进程才会看到渲染进程的断点。

![图片](https://mmbiz.qpic.cn/mmbiz/pfCCZhlbMQQEFUQlAswcpwFclVlpWXdSmiaDBByeKQI0ntGeDBmcR38r5ia9tszJzYdBDVDbCdibShTfx2ic1cep1w/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1)image.png

- 刷新渲染进程后的效果，如下图，已经进入了断点

![图片](https://mmbiz.qpic.cn/mmbiz/pfCCZhlbMQQEFUQlAswcpwFclVlpWXdSRicic2aEEzu84J50yvtiavFg5ADxicN2Y1mg2N7UnI1T5N0ANmXiaT9eOSw/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1)image.png

- 另一种方式

同时开启渲染进程和主进程的调试，只需要切换到调试全部的选项即可。注意，此种方式因为`compounds[].configurations`配置是并行执行的，并不一定能保证渲染进程调试一定能附加到主进程调试成功（估计是时机问题），有些时候会调试渲染进程不成功。所以，可以采取上面的方式进行调试。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)image.png

更多调试Electron的内容，可以点击**参考文档**[4]查阅。

##### 补充：更进一步

- **VS调试React app文档**[5]
- **VS调试Next.js文档**[6]
- **更多...**[7]



### 其他技巧

#### 技巧一：代码片段（snippets）

##### 从扩展商店中安装snippets

```
@category:"snippets"
复制代码
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)image.png



##### 创建全局代码片段

- 选择`文件 -> 首选项 -> 用户片段`
- 选择`新建全局代码片段文件`

![图片](https://mmbiz.qpic.cn/mmbiz/pfCCZhlbMQQEFUQlAswcpwFclVlpWXdSN7LuKYrUPJnvplHyNkq7ujcRx1j3bDMQ0r0XUeqStBAYrPIH7F5RHA/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1)image.png

- 添加代码片段文件的文件名称，会生成`.code-snippets`后缀的文件

- - 定义用户片段

```
{
  "自动补全console.log": {
    "scope": "javascript,typescript",
      "prefix": "log",
      "body": [
        "console.log('$1');",
        "$2"
      ],
    "description": "输出console.log('')"
  }
}
复制代码
```

| 关键词      | 类型       | 说明                                                         |
| :---------- | :--------- | :----------------------------------------------------------- |
| scope       | `string`   | 代码片段生效的作用域，可以是多个语言，比如`javascript,typescript`表示在js和ts生效，不加`scope`字段表示对所有文件类型生效 |
| prefix      | `string    | string[]`                                                    |
| body        | `string[]` | 代码片段内容，数组的每一项会是一行                           |
| description | `string`   | `IntelliSense` 显示的片段的可选描述                          |
| 1−1 - 1−n   | -          | 定义光标的位置，光标根据数字大小按tab依次跳转；注意`$0`是特殊值，表示光标退出的位置，是最后的光标位置。 |

- 在键盘输入`log`时效果如下

![图片](https://mmbiz.qpic.cn/mmbiz/pfCCZhlbMQQEFUQlAswcpwFclVlpWXdS2O7u0UlGDHsK1J7Po5lZ5I0N1lE8u4q1mdYRLyTk22Y5FonicvSs2ibA/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1)image.png

- 指定光标处的默认值并选中

```
"body": [
  "console.log('${1:abc}');"
],
复制代码
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)image.png

- 指定光标处的默认值有多个，并提供下拉选择

用两个竖线包含多个选择值，`|多个选择值直接用逗号隔开|`

```
"body": [
  "console.log('${1:abc}');",
  "${2|aaa,bbb,ccc|}"
],
复制代码
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)image.png



##### 新建当前工作区的代码片段

只需要选择`文件 \-> 首选项 \-> 用户片段 \-> 新建xxx文件夹的代码片段`, 新建后会在当前工作区生成`.vscode/xxx.code-snippets`文件

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)image.png



##### 技巧二：Emmet

vscode内置了对Emmet的支持，无需额外扩展。例如html的Emmet演示如下:

![图片](https://mmbiz.qpic.cn/mmbiz/pfCCZhlbMQQEFUQlAswcpwFclVlpWXdSiaTGXqSbXyVegUQQpj3V19jB6g5XB9MsqfMKbVEvZ6A5flaDOER11IQ/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1)emmet.gif



##### 技巧三：对光标处代码变量快速重命名

选中或者光标所处的位置，按`F2`可以对所有的变量重命名

![图片](https://mmbiz.qpic.cn/mmbiz/pfCCZhlbMQQEFUQlAswcpwFclVlpWXdSTow6pXXnWgX4811vgSsicPWdQodxMibO9GymZHQiacT6NQC5cwDJ8f1nw/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1)clipboard.png



##### 技巧四：代码重构建议

- 选中要重构的代码，点击出现的黄色小灯的图标

![图片](https://mmbiz.qpic.cn/mmbiz/pfCCZhlbMQQEFUQlAswcpwFclVlpWXdSvrR2Ztb1ShLtBUdQtzNRNyMajIyDGf4D2C5h11QkHvHvh1EJmKN4oQ/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1)clipboard.png

- 选中重构的类型

![图片](https://mmbiz.qpic.cn/mmbiz/pfCCZhlbMQQEFUQlAswcpwFclVlpWXdS1yAiaw0CM54otw5U8jAjQxWwWwiaczgkMIu4RV6pugEGicicNzKhTtcgwg/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1)clipboard.png

- 输入新的变量名

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)clipboard.png

- 还可以重构到函数

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)clipboard.png

- TS中还可以提取接口等等

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)clipboard.png



##### 补充：VsCode扩展插件开发

VsCode扩展插件可以做什么事情？

- 定制主题、文件图标
- 扩展工作台功能
- 创建webView
- 自定义新的语言提示
- 支持调试特定的runtime

基于`Yeoman`快速开发VsCode插件，步骤如下:

- 安装`Yeoman`和用于生成模板的插件**VS Code Extension Generator**[8]

```
# 终端运行，主要node版本需要12及以上，node10会安装报错
npm i -g yo generator-code
复制代码
```

- 运行`yo code`创建命令，选择要生成的项目模板。这里演示`New extension`

![图片](https://mmbiz.qpic.cn/mmbiz/pfCCZhlbMQQEFUQlAswcpwFclVlpWXdSEu6OhgHecnCE8waeoSAyN2Sn9sNfbAuxedZhV9yGE2eA5bvDBib1hZQ/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1)image.png

- 根据提示依次选择

![图片](https://mmbiz.qpic.cn/mmbiz/pfCCZhlbMQQEFUQlAswcpwFclVlpWXdSRKESthk8E5sNYKnvxD8N23iabsFLT7I0eEIzbOQG3fGJibygxiaUzHT4w/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1)image.png

- 生成的内容如下

![图片](https://mmbiz.qpic.cn/mmbiz/pfCCZhlbMQQEFUQlAswcpwFclVlpWXdSbib0ibSDQrW0oyP8C2dniathurqxdYBOabm2LSn1CHP5gGibgIvCqyJS5A/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1)image.png

- 按`F5`生成编译项目，此时会自动打开一个新窗口
- 在新窗口按`Ctrl+Shfit+P`,输入`Hello World`命令

![图片](https://mmbiz.qpic.cn/mmbiz/pfCCZhlbMQQEFUQlAswcpwFclVlpWXdSUPAhwKHZS1DBaPgkamwQzsM286wjicOlHYyicfhkRoUEHibXpyJ5uXhoA/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1)image.png

- 此时会弹出一个弹窗的效果

![图片](https://mmbiz.qpic.cn/mmbiz/pfCCZhlbMQQEFUQlAswcpwFclVlpWXdSfP7xFxNKCbkqdZLw9Z31oS0vsCj7BYu3f2pZKHvYl6kaJgzA1T1qWA/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1)image.png

- 至此，一个最简单的插件就完成了