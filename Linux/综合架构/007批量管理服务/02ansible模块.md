##### 命令模块的应用

```
ansible 主机名称/主机组名称/主机地址信息/all -m（指定应用的模块信息） 模块名称 -a（指定动作信息） "执行什么动作"
```

- command：在一个远程主机上执行一个命令,默认模块

  ```
  ansible ip -m command -a "hostname"
  ```

  - 有些符号无法识别：<、>、|、;、and、&

- shell：在节点上执行命令，没有无法识别的

  ```
  ansible -m shell -a "cd /tmp;pwd"
  ```

  - 利用shell执行脚本
    - 编写脚本
    - 脚本发送远程主机
    - 修改权限
    - 执行脚本

- script：万能模块

  - 编写一个脚本

  - 运行ansible命令执行脚本

    ```
    ansible -m script -a "./yum.sh"
    ```

- 扩展

  - chdir：执行命令之前切换目录

    ```
    ansible ip -m command -a "chdir=/tmp touch old.txt"
    默认创建在家目录，加上chdir就是在切换的目录下创建文件
    ```

  - creates：如果文件存在则不执行命令

    ```
    ansible ip -m command -a "creates=/tmp/hosts touch old.txt"
    ```

  - removes：如果文件存在则执行命令

    ```
    ansible ip -m command -a "removes=/tmp/hosts chdir=/tmp touch old.txt"
    ```

  - free_from：-a参数后面必须写上一个合法的linux命令



##### 文件类型的模块

- copy：将数据信息进行批量分发

  ```
  ansible ip -m copy -a "src=/etc/hosts dest=/etc/"
  或进行重命名
  ansible ip -m copy -a "src=/etc/hosts dest=/etc/hosts.bak"
  ```

  - owner、group设置文件传输过去后的属主、属组

    ```
    ansible ip -m copy -a "src=/etc/hosts dest=/etc/ owner=oldboy group=oldboy"
    ```

  - mode：设置文件传输过去的权限

    ```
    ansible ip -m copy -a "src=/etc/hosts dest=/etc/ mode=1777"
    ```

  - backup：对原文件进行备份，防止传输的文件覆盖原文件

    ```
    ansible ip -m copy -a "src=/etc/hosts dest=/etc/ backup=yes"
    ```

  - content：创建一个文件并直接编辑文件信息

    ```
    ansible ip -m copy -a "content='oldboy1234' dest=/etc/rsync.password"
    ```

  - remote_src:：把客户端下src的文件复制到客户端的dest路径下

    ```
    ansible ip -m copy -a "src='/tmp/old.txt' dest=/old remote_src=yes"
    ```

  - 复制目录信息的时候有斜线是将目录内容复制过去、没有斜线将目录本身也复制过去

- fetch：将被控端数据传到管理端

  ```
  #将172.16.1.31里/tmp/oldboy.txt拉取到本地tmp目录下
  ansible 172.16.1.31 -m fetch -a "src=/tmp/oldboy.txt dest=/tmp"
  ```

- file：设置文件属性信息

  - 基本用法

    ```
    ansible ip -m file -a "dest=/etc/hosts owner=oldboy group=oldboy mode=666"
    ```

  - state：创建数据信息（文件 目录 链接文件）

    - =absent：删除数据信息

      ```
      #文件
      ansible ip -m file -a "dest=/old.txt state=absent"
      
      #目录
      ansible ip -m file -a "dest=/old state=absent"
      ```

    - =directory：创建一个目录信息

      ```
      ansible ip -m file -a "dest=/old/old01/old02 state=directory"
      ```

    - =file：检测创建的数据是否存在，绿色存在，红色不存在

      ```
      ansible ip -m file -a "dest=/old/old.txt state=file"
      ```

    - =hard：创建一个硬链接文件

      ```
      ansible ip -m file -a "src=/old/1.txt dest=/old/old01/old_hard.txt state=hard"
      ```

    - =link：创建一个软链接文件

      ```
      ansible ip -m file -a "src=/old/1.txt dest=/old/old01/old_link.txt state=link"
      ```

    - touch：创建一个文件信息

      ```
      ansible ip -m file -a "dest=/old/1.txt state=touch"
      ```




##### 安装卸载软件yum

```
ansible all -m yum -a "name=iotop state=installed"
```

- name：指定安装软件名称
- state：指定是否安装软件
  - installed：安装软件
  - absent：卸载软件
  
  

##### 管理服务器的运行状态：service模块——停止、开启、重启

- name：指定管理的服务名称

- state：指定服务状态

  - started：启动
  - restarted：重启
  - stopped：停止

  - enable：指定服务是否开启自启动

```
ansible all -m service -a "name=nfs state=started enable=yes"
```



##### 批量设置多个主机的定时任务信息：cron模块

- minute：设置分钟信息（0-59）
- hour：设置小时信息（0-23）
- day：设置日期信息（1-31）
- month：设置月份信息（1-12）
- weekday：设置周信息（0-6）
- job：用于定义定时任务需要干的事情
- name：设置注释信息
- state：
  - absent：删除定时任务
  - disable：是否注释定时任务（yes/no）

基本用法

```
ansible all -m cron -a "minute=0 hour=2 job='/usr/sbin/ntpdate ntpl.aliyun.com &>/dev/null'"
```

扩展用法：设置的时候加上注释，如果存在就不再新建任务

```
ansible all -m cron -a "name='time sync' minute=0 hour=2 job='/usr/sbin/ntpdate ntpl.aliyun.com &>/dev/null'"
```

删除定时任务

```
ansible all -m cron -a "name='time sync' state=absent"
```

PS：ansible可以删除的定时任务，只能是ansible设置好的定时任务

批量注释定时任务

```
ansible all -m cron -a "name='time sync' minute=0 hour=2 job='/usr/sbin/ntpdate ntpl.aliyun.com &>/dev/null' disbale=yes"
```



##### 批量进行挂载服务：mount

- src：需要挂载的存储设备或文件信息

- path：指定目标挂载点目录

- fstype：指定挂载时的文件系统类型

- state

  - present/mounted：进行挂载
    - present：不会实现立即挂载，修改fstab文件，实现开机自动挂载
    - mounted：会实现立即挂载，并会修改fstab文件，开机自动挂载


  ```
  absible 172.16.1.7 -m mount -a "src=172.16.1.31:/data path=/mnt fstype=xfs state=mounted"
  ```

  - absent/unmounted：进行卸载
    - absent：会实现立即卸载，并且会删除fstab文件信息，禁止开机自动挂载
    - unmounted：会实现立即卸载，但是不会删除fstab文件信息


  ```
  absible 172.16.1.7 -m mount -a "src=172.16.1.31:/data path=/mnt fstype=xfs state=absent"
  ```




##### 批量创建用户：user

```
ansible all -m user -a "name=oldboy uid=666 group=old"
```

- 指定用户uid信息：uid

- 指定用户组信息：

  - group：同时指定属组和其他组
  - groups：只指定其他组

- 批量创建虚拟用户

  ```
  ansible all -m user -a "name=rsync create_home=no shell=/sbin/nologin"
  ```

- 创建用户并创建密码（或给已有的用户修改密码）

  ```
  ansible all -m user -a  "name=old passwd=123456"
  ```

  PS：利用ansible程序user模块设置用户密码信息，需要将密码明文信息转换为密文信息进行设置。上面的命令会报错

  ```
  #查看密码信息
  cat /etc/shadow
  ```
  
  - 生成密文密码信息方法
  
    ```
    ansible all -i localhost, -m debug -a "msg={{ 'mypassword' | password_hash('sha512','mysecretsalt') }}"
    
    mypassword：密码信息
    mysecretsalt：加密校验信息
    ```
    
  - 执行命令
  
    ```
    #设置密码为123456，加密校验信息为oldboy
    ansible all -i localhost, -m debug -a "msg={{ '123456' | password_hash('sha512','oldboy') }}"
    
    localhost | SUCCESS => {
        "msg": "$6$oldboy$MVd3DevkLcimrBLdMICrBY8HF82Wtau5cI8D2w4Zs6P1cCfMTcnnyAmmJc7mQaE9zuHxk8JFTRgYMGv9uKW7j1"
    }
    
    
    #将生成的加密密码去生成用户并设置密码，注意要用单引号，双引号会解析$，以为是变量
    ansible all -m user -a  ’name=old passwd=$6$oldboy$MVd3DevkLcimrBLdMICrBY8HF82Wtau5cI8D2w4Zs6P1cCfMTcnnyAmmJc7mQaE9zuHxk8JFTRgYMGv9uKW7j1‘
    
    #客户端测试
    su - old
    输入密码：123456
    ```
    
    






##### 获取内置变量模块：setup

- 获取全部内置变量

  ```
  ansible rsync -m setup
  ```

- 筛选进行查看

  ```
  ansible rsync -m setup -a "filter=ansible_hostname"
  ```

- 常见主机信息：

  | 参数                               | 解释                               |
  | ---------------------------------- | ---------------------------------- |
  | ansible_all_ipv4_addresses         | 仅显示ipv4的信息                   |
  | ansible_devices                    | 仅显示磁盘设备信息                 |
  | ansible_distribution               | 显示是什么系统，例：centos,suse等  |
  | ansible_distribution_major_version | 显示是系统主版本                   |
  | ansible_distribution_version       | 仅显示系统版本                     |
  | ansible_machine                    | 显示系统类型，例：32位，还是64位。 |
  | ansible_eth0                       | 仅显示eth0的信息                   |
  | ansible_hostname                   | 仅显示主机名                       |
  | ansible_kernel                     | 仅显示内核版本                     |
  | ansible_lvm                        | 显示lvm相关信息                    |
  | ansible_memtotal_mb                | 显示系统总内存                     |
  | ansible_memfree_mb                 | 显示可用系统内存                   |
  | ansible_memory_mb                  | 详细显示内存情况                   |
  | ansible_swaptotal_mb               | 显示总的swap内存                   |
  | ansible_swapfree_mb                | 显示swap内存的可用内存             |
  | ansible_mounts                     | 显示系统磁盘挂载情况               |
  | ansible_processor                  | 显示cpu个数(具体显示每个cpu的型号) |
  | ansible_processor_vcpus            | 显示cpu个数(只显示总的个数)        |
  
- 获取子信息方法:

  	ansible_eth0[ipv4]
