##### ansible批量管理服务概述

- 基于python开发的自动化软件工具
- 基于SSH远程管理服务实现远程主机批量管理



##### ansible批量管理服务意义

- 提高工作的效率
- 提高工作准确度
- 减少维护的成本
- 减少重复性工作



##### ansible批量管理服务功能

- 批量系统操作配置
- 批量软件服务部署
- 批量文件数据分发
- 批量系统信息收集



#### ansible批量管理服务部署

##### 管理端服务器

- 安装部署软件

  ```
  yum install -y ansible
  需要依赖epel的yum源
  
  /etc/ansible/ansible.cfg	服务配置文件
  /etc/ansible/hosts	主机清单文件
  /etc/ansible/roles	角色目录
  ```

- 需要编写主机清单文件，定义可以管理的主机信息（这里面的主机要分发好公钥）

  ```
  vim /etc/ansible/hosts
  
  第一个ip
  第二个ip
  第三个ip
  ```

- 测试是否可以管理多个主机

  ```
  ansible all -a "hostname"
  
  ansible 172.16.1.31,172.16.1.41 -a "hostname"
  ```
  



##### 如何配置主机清单

- 分组配置主机

  ```
  [web]
  第一个ip
  第二个ip
  
  [data]
  第一个ip
  第二个ip
  ```

  - 管理的时候要根据分组名进行管理，**不能使用IP**

    ```
    ansible web -a "hostname"
    ```

- 主机名符号匹配配置

  ```
  [web]
  172.16.1.[7:9]
  
  相当于
  [web]
  172.16.1.7
  172.16.1.8
  172.16.1.9
  ```

- 根据主机名配置

  ```
  [web]
  web01
  
  cat /etc/hosts
  172.16.1.7 web01
  ```

- 跟上非标准远程端口

  ```
  [web]
  web01:222
  ```

- 主机使用特殊的变量

  - 不用分发公钥就进行连接

    ```
    [web]
    172.16.1.7 ansible_ssh_port=22 ansible_ssh_user=root ansible_ssh_pass=root
    ```

  - 不用在hosts文件中做映射

    ```
    [web]
    web01 ansible_ssh_host=172.16.1.7 ansible_ssh_port=22 ansible_ssh_user=root ansible_ssh_pass=root
    ```

- 主机组名嵌入式配置

  ```
  [rsync:children]
  rsync_server
  rsync_client
  
  [rsync_server]
  web01
  
  [rsync_client]
  web02
  web03
  ```

- 嵌入变量信息配置

  ```
  [web]
  web01
  web02
  
  [web:vars]
  ansible_ssh_port=22
  ansible_ssh_user=root
  ansible_ssh_pass=123456
  ```

  



##### ansible服务架构信息

- 主机清单配置
- 软件模块信息
- 基于秘钥连接主机
- 主机需要关闭selinux
- 软件剧本功能



##### ansible学习帮助手册如何查看

- 列出模块使用简介

  ```
  ansible-doc -l
  ```

- 指定一个模块详细说明

  ```
  ansible-doc -s fetch
  ```

- 查询模块在剧本中的应用方法

  ```
  ansible-doc fetch
  ```

  



##### ansible输出颜色说明

- 绿色：查看主机信息/对主机未做改动
- 黄色：对主机数据信息进行了修改
- 红色：命令执行出错了
- 粉色：警告信息
- 蓝色：显示ansible命令执行过程



##### ansible输出信息解释

- 对哪台主机进行操作
- 是否对主机信息进行修改
- 生成一个文件校验码 == MD5数值
- 显示目标路径信息
- 显示复制后文件uid信息
- 显示复制后文件属组信息
- 生成一个文件校验码 == MD5数值
- 显示复制后文件权限信息
- 显示复制后文件属主信息
- 显示文件的大小信息



##### ansible服务特点

- 管理端不需要启动服务程序（no server）
- 管理端不需要编写配置文件（/etc/ansible/ansible.cfg）
- 受控端不需要安装软件程序（libselinux-python）
  - 被管理端selinux服务没有关闭——影响ansible软件管理
  - libselinux-python让selinux开启的状态也可以使用ansible程序
- 受控端不需要启动服务程序（no agent）
- 服务程序管理操作模块众多（module）
- 利用脚本编写来实现自动化（playbook）



##### 远程主机无法管理问题分析

- 管理端没有分发好主机的公钥
- 被管理端远程服务出现问题
  - /usr/sbin/sshd -D：负责建立新的远程连接
  - sushi: root@pts/0：用于维护当前的远程连接（windows—linux）
  - sshd：root@notty：用于维护远程连接（ansible—被管理端）
- 被管理端进程出现卡死情况
  - 杀掉sshd：root@notty进程
