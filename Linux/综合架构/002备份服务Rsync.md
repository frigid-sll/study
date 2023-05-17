

##### 作用

- 数据备份的服务器

- 进行日志统一保存

  ```
  grep -r oldboy /backup/
  
  查找backup目录下所有文件内容里包含oldboy信息的文件
  ```



##### 如何部署搭建备份服务器：rsync服务



##### 什么是rsync服务？

Rsync是一款开源的、快速的、多功能的、可实现全量及增量的本地或远程数据同步备份的优秀工具 



##### Rsync软件使用方法：

rsync命令 1V4：cp、scp、rm、ls

- 本地备份数据

  - cp命令：

    ```
    cp /etc/hosts /tmp
    ```

  - rsync

    ```
    rsync /etc/hosts /tmp/host_rsync
    ```

- 远程备份数据

  - scp

    ```
    scp -rp /etc/hosts 172.16.1.41:/backup
    yes
    输入那台服务器用户的密码：
    
    当前登陆用户是root输入的就是那台服务器root用户的密码，如果是别的那输入的也是那台服务器别的用户的密码
    
    -r：递归，文件和文件夹都可以
    -p：保持文件的属性
    ```

  - rsync

    ```
    rsync -rp /etc/hosts 172.16.1.41:/backup
    yes
    输入那台服务器用户的密码：
    ```

  - rsync备份目录：**没有斜线，将目录也传过去**

    ```
    rsync -rp /etc 172.16.1.41:/backup
    yes
    输入那台服务器用户的密码：
    ```

  - rsync备份目录：**有斜线，只将里面的内容传过去**

    ```
    rsync -rp /etc/ 172.16.1.41:/backup
    yes
    输入那台服务器用户的密码：
    ```

- 实现无差异同步数据

  ```
  rsync -rp --delete /需要与哪个文件/夹内容同步/ 172.16.1.41:/要被同步的文件/夹
  
  --delete 实现无差异同步数据
  
  #backup里面内容跟null一样,相当于执行了rm
  rsync -rp --delete /null/ 172.16.1.41:/backup
  
  如何将目录中的数据快速删除：使用rsync
  ```

- 查看文件是否存在

  ```
  rsync /etc/hosts
  ```



##### rsync语法格式

- 本地备份数据

  ```
  rsync [option...] src ... [dest]
  本地备份数据
  src：要备份的数据信息
  dest：备份到什么路径中
  ```

- 远程备份数据

  - 拉取数据

    ```
    PULL:
    rsync [option...] [USER@]HOST:SRC... [DEST]
    
    rsync -rp root@172.16.1.41:/etc/hosts /backup
    ```

    

    | 参数    | 解释                                                         |
    | ------- | ------------------------------------------------------------ |
    | [USER@] | 以什么用户身份拉取数据（默认当前用户，最好用root，不然有些文件会报错，权限不足或者用户不存在） |
    | HOST    | 指定远程主机IP地址或主机名称<br/>主机名称要在/etc/hosts文件中有解析 |
    | SRC     | 要拉取的数据信息                                             |
    | DEST    | 保存到本地的路径信息                                         |

  - 推数据

    ```
    PUSH:
    rsync [option...] SRC... [USER@]HOST:DEST
    
    rsync -rp /etc/hosts root@172.16.1.41:/backup
    ```

    | 参数    | 解释                         |
    | ------- | ---------------------------- |
    | SRC     | 本地要进行远程传输备份的数据 |
    | [USER@] | 以什么用户身份推送数据       |
    | HOST    | 指定远程主机ip或主机名称     |
    | dest    | 保存到远程的路径信息         |

  - 守护进程方式备份数据（一直运行）

    - 可以进行一些配置管理
    - 可以进行安全策略管理
    - 可以实现自动传输备份数据

    

##### 服务部署安装过程

- 下载安装软件 yum
- 编写配置文件 
- 搭建服务环境 备份的目录/目录权限
- 启动服务程序 开机自动启动
- 测试服务功能



##### rsync守护进程服务端部署方式

- 下载安装

  ```
  rpm -qa | grep rsync
  yum install -y rsync
  ```

- 编写配置文件

  ```
  vim /etc/rsyncd.conf
  
  dG内容全部删除，然后添加下面的内容
  
  #指定管理备份目录的用户，不管别人传来的是啥身份过来就都要是rsync，如果fake注释就会报错
  uid = rsync
  #指定管理备份目录的用户组
  gid = rsync		
  #定义rsync备份服务的端口号
  prot = 873 											
  #将rsync虚拟用户伪装超级管理员进行修改传输过来的数据的属主和属组，不管别人传来的是啥身份过来就都是rsync不会报错
  fake super = yes
  #和安全相关的配置
  use chroot = no 	
  #最大连接数
  max connections = 200 					
  #超时时间(秒)如果300s都没有数据传输，就会把链接强制去掉
  timeout = 300 			
  #记录rsync的进程号，让程序快速停止进程 kill `cat /var/run/rsyncd.pid`、如果文件存在就代表服务正在运行
  pid file = /var/run/rsyncd.pid	
  #锁文件，如果连接满了就控制不能有新连接
  lock file = /var/run/rsync.lock	
  #rsync日志文件 用于排错分析问题
  log file = /var/log/rsyncd.log	
  #忽略传输中的简单错误
  ignore errors
  #指定备份目录是可读可写的
  read only = false
  #客户端是否可以看服务端模块信息，为了避免安全一般要关闭
  list = false
  #允许传输备份数据的主机（白名单）
  hosts allow = 172.16.1.0/24
  #禁止传输备份数据的主机（黑名单）
  hosts deny = 0.0.0.0/32
  #指定认证用户，登陆需要认证
  auto users = rsync_backup
  #指定认证用户密码文件 用户名称:密码信息
  secrets file = /etc/rsync.password
  #模块信息
  [backup]
  #模块中的配置参数
  comment = "backup dir by oldboy"
  #指定备份目录，这个目录要存在
  path = /backup
  ```

- 服务环境准备

  - 创建rsync服务的虚拟用户

    ```
    useradd rsync -M -s /sbin/nologin
    ```

  - 创建密码认证文件

    ```
    echo "rsync_backup:oldboy123" >/etc/rsync.password
    
    认证用户：rsync_backup
    认证用户密码：oldboy123
    
    #进行查看
    ll /etc/rsync.password
    
    #修改权限,不让其他用户看
    chmod 600 /etc/rsync.password
    ```

  - 创建备份目录并修改属主属组信息

    ```
    mkdir /backup
    
    #修改属主属组为rsync（根据配置文件来），如果不修改权限，别人推送数据就推不进来，别人推送数据的时候身份是配置文件里面写的rsync
    chown rsync.rsync /backup/
    ```

- 启动备份服务

  ```
  systemctl start rsyncd
  systemctl enable rsyncd
  ```


- 需要熟悉rsync守护进程名称语法

  - PULL：恢复数据

    ```
    rsync [OPTION...] [USER@]HOST::SRC... [DEST]
    
    rsync -avz rsync_backup@172.16.1.41::backup/newboy /oldboy/
    
    将备份服务器中的backup模块路径下的newboy里的数据恢复到本地的/oldboy目录下
    ```
  
    - ::src：要恢复的数据
  
    - dest：本地恢复数据路径
  
  - PUSH：备份数据
  
    ```
    rsync [OPTION...] SRC... [USER@]HOST::DEST
    
    rsync -avz /etc/hosts rsync_backup@172.16.1.41::backup
    输入认证用户密码
    会有报错，但是数据已经传输过去了，172.16.1.41的/backup里面有hosts文件，将本地的/etc/hosts推送到172.16.1.41,推送过去的数据的属主和属组都变是rsync
    
    报错解决：
    需要在传输之前就把传输的数据的属主和属组都改为备份服务器设置的文件信息的属主和属组
    或
    将fake super=yes开启
    ```
  
    - SRC：要推送备份数据信息
    - [USER@]：指定认证用户信息
    - HOST：指定远程主机的IP地址或者主机名称
    - ::DEST：备份服务器的模块信息（backup）



##### Rsync服务常见问题

- 防火墙没关闭
  - 如果打开了需要开放873端口

- 命令语法格式有问题，后面写的是模块信息而不是路径信息
- 服务认证用户失败
  - 用户名或密码输入错误
  - 指定的密码文件和实际密码文件名称不一致
  - `/etc/rsync.password`文件权限不是600
  - `rsync_backup:123456` 密码配置文件后面注意不要有空格
  - rsync客户端密码文件中只输入密码信息即可，不要输入虚拟认证用户名称
- rsync服务位置模块错误
  - 配置文件的模块名称和在传输的时候写的模块名称要一致
- 权限问题
  - 备份目录的属主和属组不正确，不是rsync
  - 备份目录的权限不正确，不是755
- 服务端没有虚拟用户rsync



##### rsync客户端配置

- 创建一个秘密文件

  ```
  echo "oldboy123" >/etc/rsync.password
  chmod 600 /etc/rsync.password
  ```

- 进行免交互传输数据设置

  ```
  rsync -avz /etc/hosts rsync_backup@172.16.1.41::backup --password-file=/etc/rsync.password
  
  --password-file：指定认证用户密码文件
  ```

  

##### Rsync参数详解

| 参数                | 解释                                                         |
| ------------------- | ------------------------------------------------------------ |
| -v                  | 显示详细的传输信息                                           |
| -a                  | 命令的归档参数，包含rtopgDl                                  |
| -r                  | 递归参数                                                     |
| -t                  | 保持文件属性信息时间信息不变（修改时间）                     |
| -o                  | 保持文件的属主信息不变                                       |
| -g                  | 保持文件的属组信息不变                                       |
| -p                  | 保持文件的权限信息不变                                       |
| -D                  | 保持设备文件信息不变                                         |
| -l                  | 保持链接文件属性不变，但是看不到内容                         |
| -L                  | 保持链接文件数据信息不变（-vrtogpD -L），如果是软连接文件传过去内容还是有，-l传输过去软链接文件内容没有 |
| -P                  | 显示文件传输进度                                             |
| --exclude=PATTERN   | 排除指定数据不被传输（文件路径）                             |
| --exclude-from=file | 排除指定数据不被传输（批量排除，文件）                       |
| --bwlimit=RATE      | 显示传输的速率，并设置传输的速率，防止把服务器的带宽占满，导致别人无法访问 |
| --delete            | 同步数据，有的都有，没有的也没有                             |
| -z                  | 将会在传输过程中压缩。                                       |
| --port=xxx          | 指定传输的rsync服务端口                                      |

##### PS：如何让-o和-g参数生效：

- 需要将配置文件uid和gid为root
- 需要将配置文件的fake super参数进行注释
- 将备份服务器中的备份目录属主属组权限设置root.root



##### Rsync多模块

```
vim /etc/rsyncd.conf

#下面添加新的模块
#备份模块信息
[backup]
#模块中的配置参数
comment = "backup dir by oldboy"
#指定备份目录，这个目录要存在
path = /backup
#数据库模块信息
[dba]
#模块中的配置参数
comment = "backup dir by oldboy"
#指定备份目录，这个目录要存在
path = /dba
#开发模块信息
[dev]
#模块中的配置参数
comment = "backup dir by oldboy"
#指定备份目录，这个目录要存在
path = /dev_data
```

- 创建目录

  ```
  mkdir -p /{dba,dev_data}
  ```

- 修改权限

  ```
  chown rsync.rsync /{dba,dev_data}
  ```

- 检查

  ```
  ll -d /{dev_data,dba}
  ```

- 重启服务

  ```
  systemctl restart rsyncd
  ```

  

##### 守护进程的排除功能实践

- 准备环境

  ```
  mkdir -p /oldboy/{a..c}
  touch /oldboy/{1..2}.txt
  touch /oldboy/{a..c}/{1..3}.txt
  tree /oldboy
  /oldboy
  ├── 1.txt
  ├── 2.txt
  ├── a
  │   ├── 1.txt
  │   ├── 2.txt
  │   └── 3.txt
  ├── b
  │   ├── 1.txt
  │   ├── 2.txt
  │   └── 3.txt
  └── c
      ├── 1.txt
      ├── 2.txt
      └── 3.txt
  ```

- 需要将/oldboy目录下面a目录全部数据备份、b目录不要备份1.txt、c整个目录不做备份。使用`--exlcude`

  ```
  rsync -avz /oldboy --exclude=b/1.txt --exclude=c/ rsync_backup@172.16.1.41::backup --password_file=/etc/rsync.password
  ```

  **PS：使用相对路径，是相对于前面写的要备份的路径。排除的时候也可以使用绝对路径**

- 使用`--exclude-from=file`批量排除

  - 生成排除文件，可以用find命令查找要排除的文件然后写入

    ```
    vim /oldboy/exclude.txt
    b/1.txt
    c/1.txt
    c/3.txt
    exclude.txt
    
    #多行写，后面也不要有空格
    ```

  - 进行传输

    ```
    rsync -avz /oldboy --exclude-from=/oldboy/exclude.txt rsync_backup@172.16.1.41::backup --pasword-file=/etc/rsync.password
    ```

    

##### 守护进程创建备份目录

- 将要备份的文件/etc/hosts传输到backup模块设置的路径下的10.0.0.31子目录下。

  ```
  rsync -avz /etc/hosts rsync_backup@172.16.1.41::backup/10.0.0.31/ --password-file=/etc/rsync.password
  ```

- 注意
  - 如果没有会自动创建，但是如果写多级目录，前面的目录不存在则会报错
  - 记住后面要加上/，不然会被认为是文件



##### 守护进程的访问控制配置

- 白名单：`host allow`
- 黑名单：`host deny`

- 三种配置方法：
  - 只有白名单，没有黑名单
  - 只有黑名单，没有白名单
  - 白名单和黑名单都有
    - 先看白名单信息
    - 在看黑名单
    - 如果都没有匹配到就默认允许
    - 如果都匹配到了白名单优先于黑名单



##### 守护进程列表配置

```
vim /etc/rsyncd.conf

#true，客户端可以看服务端模块信息；false则不可以看
list = true
```



##### 客户端查看服务端rsync模块信息

```
rsync rsync_backup@172.16.1.41::
backup	"backup dir by oldboy"
dba			"backup dir by oldboy"
dev			"backup dir by oldboy"
```

