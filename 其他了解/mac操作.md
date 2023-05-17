##### brew常用命令

```
* 查看brew版本：brew -v
* 更新brew版本：brew update
* 本地软件库列表：brew list
* 查看软件库版本：brew list --versions
* 查找软件包：brew search xxx （xxx为要查找软件的关键词）
* 安装软件包：brew install xxx （xxx为软件包名称）
* 卸载软件包：brew uninstall xxx
* 安装软件：brew cask install xxx（xxx为软件名称）
* 卸载软件：brew cask uninstall xxx
* 查找软件安装位置：which xxx （xxx为软件名称）
```



#### Mac权限问题，operation not permitted

##### 推荐方案：alias

其实还是尽量不要去关闭SIP，比较简单的办法是在zsh或bash的配置文件中添加`alias`，例如我们用brew安装了vim，然后我们需要用覆盖mac自带的vim，以zsh为例，我们可以在文件`~/.zshrc`中添加如下代码

```text
alias vim="/usr/local/bin/vim"
alias vimdiff="/usr/local/bin/vimdiff"
alias vi="/usr/local/bin/vi"
alias view="/usr/local/bin/view"
alias vimdiff="/usr/local/bin/vimdiff"
alias vimtutor="/usr/local/bin/vimtutor"
TEXT 复制 全屏
```

重新登陆，或执行下面命令，让alias生效，

```text
source ~/.zshrc
```



##### 显示隐藏文件

```
command + shift + .
```



##### 创建虚拟环境

```
python -m venv 虚拟环境名

启动
source 虚拟环境名/bin/activate

关闭
deactivate
```







`lsof -i -P`命令用于列出当前系统中打开的所有网络连接，包括TCP和UDP连接。其中，-i选项用于指定只显示网络连接信息，-P选项用于禁止将端口号转换为服务名称（即不解析/etc/services文件）。 使用该命令可以查看当前系统中哪些进程正在监听哪些端口，以及哪些进程正在与外部主机建立网络连接。输出结果中包含以下信息：

- COMMAND：进程名称。
- PID：进程ID。
- USER：进程的用户。
- FD：文件描述符。
- TYPE：网络连接类型，如TCP、UDP等。
- DEVICE：连接使用的设备。
- SIZE/OFF：连接的大小或偏移量。
- NODE：连接使用的节点。
- NAME：连接使用的地址和端口号。
- USER：连接的用户。
- INODE：连接的节点。 例如，以下是lsof -i -P命令的示例输出：

```
plaintextCopy code
COMMAND   PID     USER   FD   TYPE  DEVICE SIZE/OFF NODE NAME
Google    1000    user   48u  IPv4  0x0123456      0t0  TCP 192.168.1.100:56284->172.217.24.206:https (ESTABLISHED)
Dropbox   2000    user   23u  IPv4  0x0123456      0t0  TCP 192.168.1.100:53222->162.125.66.1:http (ESTABLISHED)
iTerm2    3000    user   25u  IPv4  0x0123456      0t0  TCP 192.168.1.100:50856->104.16.24.235:https (ESTABLISHED)
```

可以看到，该命令列出了三个进程的网络连接信息，包括进程名称、进程ID、连接类型、本地地址、本地端口、远程地址、远程端口和连接状态等信息。



##### 在Mac终端上，可以使用以下命令查看当前正在运行的服务和对应的端口：

```
plaintextCopy code
lsof -i -P | grep LISTEN
```

这个命令会列出所有正在监听的网络连接，包括服务的名称、进程ID和对应的端口。如果只想查看某个特定端口的连接，可以在命令中添加端口号，例如：

```
plaintextCopy code
lsof -i -P | grep LISTEN | grep 8080
```
