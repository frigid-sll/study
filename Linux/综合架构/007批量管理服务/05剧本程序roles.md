##### 剧本编写完的问题

- 目录结构不够规范
- 编写好的任务如何重复调用
- 服务端配置文件改动，客户端参数信息也自动变化
- 汇总剧本中没有显示主机角色信息
- 一个剧本内容信息过多，不容易进行阅读，如何进行拆分



#### ansible程序roles ---规范

##### 第一个历程：规范目录结构

##### 在roles目录中创建相关文件(每个目录里都有main.yaml)

- 编写tasks目录中的main.yml文件

  - nfs-server

    ```
    cd nfs-server/tasks
    vim main.yml
    #将之前要执行的tasks内容复制过来
    
    - name: 01-copy conf file
      copy: src=exports dest=/etc
      notify: restart nfs server
    - name: 02-create data dir
      file: path={{ Data_dir }} state=directory owner=nfsnobody group=nfsnobody
    - name: 03-boot server
      service: name={{ item }} state=started enabled=yes
      with_items:
        - rpcbind
        - nfs
    ```

  - nfs-client

    ```
    - name: 01-mount
      mount: src=172.16.1.31:{{ Data_dir }} path=/mnt fstype=nfs state=mounted
    - name: 02-check mount info
      shell: df -h|grep {{ Data_dir }}
      register: mount_info
    - name: display mount info
      debug: msg={{ mount_info.stdout_lines }}
    ```

  - rsync

    ```
    - name: 01-installed rsync
      yum: name=rsync state=installed
    - name: 02-push conf file
      template: src=rsyncd.conf dest=/etc/
      notify: restart rsync server
    - name: 03-create user
      user: name=rsync create_home=no shell=/sbin/nologin
    - name: 04-create backup dir
      file: path={{ Data_dir }} state=directory owner=rsync group=rsync
    - name: 05-create password file
      copy: content=rsync_backup:oldboy123 dest=/etc/rsync.password mode=600
    - name: 06-start rsync server
      service: name=rsyncd state=started enabled=yes
    ```

- 编写vars目录中的main.yaml文件

  - nfs-server

    ```
    cd ../vars
    vim main.yml
    
    Data_dir: /data
    第二个变量: 变量值
    ```

  - rsync

    ```
    Data_dir: /backup
    Port_info: 874
    ```

- 编写files目录中的文件(在tasks中main.yaml中调取exports文件直接就写exports)

  - nfs-server

    ```
    cd ../files
    cp /etc/ansible/ansible-playbook/nfs-file/nfs-server/exports exports
    ```

- 编写handlers目录中的main.yaml文件

  - nfs-server

    ```
    cd ../handlers
    vim main.yml
    
    - name: restart nfs server
      service: name=nfs state=restarted
    - name: 第二个触发器name
    	要做的事
    ```

  - rsync

    ```
    - name : restart rsync server
      service: name=rsyncd state=restarted
    ```

- 编写templates

  - rsync：tasks中使用template模块来调用templates里面的文件

    ```
    cd /etc/ansible/roles/rsync/templates/
    cp /etc/rsyncd.conf ./
    cp /etc/rsyncd.password ./
    
    vim rsyncd.conf
    port = {{ Port_info }}
    ```

- 编写一个主剧本文件

  ```
  cd /etc/ansible/roles
  vim site.yml
  
  - hosts: nfs_server
    roles:
      - nfs-server
  
  - hosts: nfs_clients
    roles:
      - nfs-clents
  
  - hosts: rsync_server
    roles:
      - rsync
  ```

- 执行剧本

  ```
  ansible-playbook -C site.yml
  ```

  



##### main.yml拆分整合

```
vim tasks/main.yml

- include_tasks: copy.yml
- include_tasks: create.yml
```



##### 客户端和服务端整合（加判断）

```
- import_tasks: server
  when ansible_ip_address == '192.168.1.1'
- import_tasks: client
  when ansible_ip_address == '192.168.1.2'
```





##### 整合后的目录

```
cd /etc/ansible/roles

#创建客户端和服务端都要执行的yml目录
mkdir {nfs-public,rsync-public}

#创建角色目录下面的字目录
mkdir {nfs-server,nfs-client,rsync-server,rsync-client}/{vars,tasks,templates,handlers,files}

tree
.
├── main.yml
├── nfs-client
│   ├── files：保存需要分发文件目录（第三步执行）
│   ├── handlers：保存触发器配置文件信息（第四步执行）
│   ├── tasks：保存要执行的动作信息文件(第一步执行)
│   │   ├── client.yml
│   │   └── main.yml
│   ├── templates：保存需要分发模版文件，模版文件中可以设置变量信息
│   └── vars：保存变量信息文件（第二步执行）
│       └── main.yml
├── nfs-public
│   └── nfs-install.yml
├── nfs-server
│   ├── files
│   │   └── exports
│   ├── handlers
│   │   └── main.yml
│   ├── tasks
│   │   ├── main.yml
│   │   └── server.yml
│   ├── templates
│   └── vars
│       └── main.yml
├── rsync-client
│   ├── files
│   │   └── rsync.password
│   ├── handlers
│   ├── tasks
│   │   ├── client.yml
│   │   └── main.yml
│   ├── templates
│   └── vars
│       └── main.yml
├── rsync-public
│   └── rsync-install.yml
└── rsync-server
    ├── files
    │   └── rsync.password
    ├── handlers
    │   └── main.yml
    ├── tasks
    │   ├── main.yml
    │   └── server.yml
    ├── templates
    │   └── rsyncd.conf
    └── vars
        └── main.yml
        
```

- main.yml

  ```
  - hosts: server
    remote_user: root
    gather_facts: no
    roles:
      - nfs-server
      - rsync-server
  
  - hosts: client
    remote_user: root
    gather_facts: no
    roles:
      - nfs-client
      - rsync-client
  ```

- /etc/hosts

  ```
  ip   andun
  ip   applet
  ```

- /etc/ansible/hosts

  ```
  [server]
  andun:221
  
  [client]
  applet
  ```

- /nfs-client/vars/main.yml（这个不能用整合）

  ```
  [root@pert vars]# pwd
  /etc/ansible/roles/nfs-client/vars
  [root@pert vars]# ls
  main.yml
  [root@pert vars]# cat main.yml 
  Data_dir: /nfs-data
  ```

- /nfs-client/tasks/client.yml

  ```
  - name: 01-mount
    mount: src=ip:{{ Data_dir }} path=/mnt fstype=nfs state=mounted
  - name: 02-check mount info
    shell: df -h|grep {{ Data_dir }}
    register: mount_info
  - name: display mount info
    debug: msg={{ mount_info.stdout_lines }}
  ```

- /nfs-client/tasks/main.yml

  ```
  - include_tasks: /etc/ansible/roles/nfs-public/nfs-install.yml
  - include_tasks: client.yml
  ```

- /etc/ansible/roles/nfs-public/nfs-install.yml

  ```
  - name: 01-install nfs software
    yum:
      name: ['nfs-utils','rpcbind']
      state: installed
  ```

- /nfs-server/tasks/main.yml

  ```
  - include_tasks: /etc/ansible/roles/nfs-public/nfs-install.yml
  - include_tasks: server.yml
  ```
  
- /nfs-server/tasks/server.yml

  ```
  - name: 01-copy conf file
    copy: src=exports dest=/etc
    notify: restart nfs server
  - name: 02-create data dir
    file: path={{ Data_dir }} state=directory owner=nfsnobody group=nfsnobody
  - name: 03-boot server
    service: name={{ item }} state=started enabled=yes
    with_items:
      - rpcbind
      - nfs
  ```
  
- /nfs-server/vars/main.py

  ```
  Data_dir: /nfs-data
  ```
  
- /nfs-server/files

  ```
  [root@pert nfs-server]# cd files
  [root@pert files]# tree
  .
  └── exports
  
  [root@pert files]# cat exports 
  /nfs-data ip地址(rw,sync)
  ```
  
- /rsync-public/

  ```
  [root@pert roles]# cd rsync-public/
  [root@pert rsync-public]# ls
  rsync-install.yml
  [root@pert rsync-public]# cat rsync-install.yml 
  - name: 01-install rsync server
    yum: name=rsync state=installed
  ```
  
- /rsync-client/tasks

  ```
  [root@pert rsync-client]# cd tasks/
  [root@pert tasks]# ls
  client.yml  main.yml
  [root@pert tasks]# cat client.yml 
  - name: 02-push password file
    copy: src=rsync.password dest=/etc/
  - name: 03-backup data
    shell: rsync -avz --port={{ Port }} {{ Data_dir }} rsync_backup@47.113.221.15::backup --password-file=/etc/rsync.password
  [root@pert tasks]# cat main.yml 
  - include_tasks: /etc/ansible/roles/rsync-public/rsync-install.yml
  - include_tasks: client.yml
  ```

- /rsync-client/vars

  ```
  [root@pert rsync-client]# cd vars/
  [root@pert vars]# ls
  main.yml
  [root@pert vars]# cat main.yml 
  Data_dir: /backup/
  Port: 873
  ```

- /rsync-clent/files

  ```
  [root@pert rsync-client]# cd files/
  [root@pert files]# ls
  rsync.password
  [root@pert files]# cat rsync.password 
  rsync_backup:pert
  ```

- rsync-server/files

  ```
  [root@pert rsync-server]# cd files/
  [root@pert files]# ls
  rsync.password
  [root@pert files]# cat rsync.password 
  rsync_backup:pert
  ```

  

- rsync-server/vars

  ```
  [root@pert rsync-server]# cd vars/
  [root@pert vars]# ls
  main.yml
  [root@pert vars]# cat main.yml 
  Backup_dir: /backup
  Port: 873
  ```

  

- rsync-server/templates

  ```
  [root@pert rsync-server]# cd templates/
  [root@pert templates]# ls
  rsyncd.conf
  [root@pert templates]# cat rsyncd.conf 
  uid = rsync
  #指定管理备份目录的用户组
  gid = rsync
  #定义rsync备份服务的端口号
  prot = {{ Port }} 
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
  #客户端是否可以看服务端模块信息，为了避免安全般要关闭
  list = false
  #允许传输备份数据的主机（白名单）
  hosts allow = ip
  #禁止传输备份数据的主机（黑名单）
  #hosts deny = 0.0.0.0/32
  #指定认证用户，登陆需要认证
  auto users = rsync_backup
  #指定认证用户密码文件 用户名称:密码信息
  secrets file = /etc/rsync.password
  #模块信息
  [backup]
  #模块中的配置参数
  comment = "backup dir"
  #指定备份目录，这个目录要存在
  path = /backup
  ```

  

- rsync-server/tasks

  ```
  [root@pert rsync-server]# cd tasks/
  [root@pert tasks]# ls
  main.yml  server.yml
  [root@pert tasks]# cat main.yml 
  - include_tasks: /etc/ansible/roles/rsync-public/rsync-install.yml
  - include_tasks: server.yml
  [root@pert tasks]# cat server.yml 
  - name: 02-push conf file
    template: src=rsyncd.conf dest=/etc/
    notify: restart rsync server
  - name: 03-create user
    user: name=rsync create_home=no shell=/sbin/nologin
  - name: 04-create backup dir
    file: path={{ Backup_dir }} state=directory owner=rsync group=rsync
  - name: 05-push password file
    copy: src=rsync.password dest=/etc/
  - name: 06-start rsync server
    service: name=rsyncd state=started enabled=yes
  ```

  
