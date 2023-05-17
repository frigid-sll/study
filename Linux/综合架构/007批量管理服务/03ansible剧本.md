

##### 剧本的作用：可以一键化完成多个任务

##### 剧本的组成部分

- 演员信息 **hosts**
- 干的事情 **tasks**

##### 剧本编写规范：pyyaml——三点要求

- 合理的信息缩进

  - 在ansible中一定不能用tab进行缩进

- 冒号的使用方法

  ```
  hosts: 172.16.1.41
  tasks:
  yum: name=xx
  ```

  - 使用冒号时后面要有空格信息
  - 以冒号结尾，冒号信息出现在注释说明中，后面不需要加上空格

- 短横线应用 -（列表功能）

  ```
  - 张三
    男
      - 打游戏
      - 运动
        湖南
  - 李四
    女
      打游戏
        湖南      
  ```

  - 使用短横线构成列表信息，短横线后面需要有空格



##### 剧本编写常见错误

- 剧本语法规范是否符合
  - 空格
  - 冒号
  - 短横线
- 剧本中模块是否使用正确
- 一个name只能有一个模块命令
- 剧本中尽量不要使用大量shell



##### 剧本执行出现错误排查思路

- 找到剧本中出现问题关键点
- 将剧本命令转为模块命令
- 将模块命令转为linux命令
  - 本地管理主机上执行命令调试
  - 远程被管理主机上执行命令测试



#### 剧本编写：自动化部署rsync服务

##### 服务端的操作

- 第一个历程：安装软件

  ```
  ansible all -m yum -a "name=rsync state=installed"
  ```

- 第二个历程：编写文件后批量分发

  ```
  ansible all -m copy -a "src=/xxx/rsyncd.conf dest=/etc/"
  ```

- 第三个历程：创建用户

  ```
  ansible all -m user -a "name=rsync create_home=no shell=/sbin/nologin"
  ```

- 第四个历程：创建目录

  ```
  ansible all -m file -a "dest=/backup state=directory owner=rsync group=rsync"
  ```

- 第五个历程：创建密码文件

  ```
  ansible all -m file -a "content='oldboy123' dest=/etc/rsync.password mode=600"
  ```

- 第六个历程：启动服务

  ```
  ansible all -m service -a "name=rsyncd state=started enabled=yes"
  ```

  

##### 用剧本编写

- 创建目录

  ```
  mkdir /etc/ansible/ansible-playbook 
  ```

- 编写剧本(剧本文件扩展名要写为yaml)

  - 方便识别文件是一个剧本文件
  - 文件编写时会有颜色提示

  ```
  cd /etc/ansible/ansible-playbook 
  vim rsync_server.yaml
  ```

  ```
  #都要做的事,嵌入式主机组名
  - hosts: rsync
    tasks:
      - name: 01-install rsync server
        yum: name=rsync state=installed
  
  #服务端，主机组名分组
  - hosts: rsync_server
    tasks:
      - name: 02-push conf file
        copy: src=../server_file/rsync_server/rsyncd.conf dest=/etc/
      - name: 03-create user
        user: name=rsync create_home=no shell=/sbin/nologin
      - name: 04-create backup dir
        file: path=/backup state=directory owner=rsync group=rsync
      - name: 05-create password file
        copy: content=rsync_backup:oldboy123 dest=/etc/rsync.password mode=600
      - name: 06-start rsync server
        service: name=rsyncd state=started enabled=yes
  
  #客户端，主机组名分组
  - hosts: rsync_client
    tasks:
      - name: 02-create password file
        copy: content=oldboy123 dest=/etc/rsync.password mode=600
      - name: 03-touch test file
        file: dest=/tmp/test.txt state=touch
      - name: 04-check 
        shell: rsync -avz /tmp/test.txt rsync_backup@172.16.1.41::backup --password-file=/etc/rsync.password
  ```

- 执行剧本

  - 第一个步骤：检查剧本的语法格式

    ```
    ansible-play --syntax-check rsync_server.yaml
    ```

  - 第二个步骤：模拟执行剧本

    ```
    ansible-play -C rsync_server.yaml
    ```

  - 第三个步骤：执行剧本

    ```
    ansible-play rsync_server.yaml
    ```



##### 指定主机清单进行执行剧本

```
ansible-playbook -i /etc/ansible/new_hosts 要执行的剧本
```






##### 剧本参数remote_user、gather_facts

```
remote_user: root
gather_facts: no    

这两个写在hosts下面，tasks上面
- hosts: all
  remote_user: root
  gather_facts: no
  tasks:
    - name: Ignore False
      yum: name={{ item }}  state=installed
      with_items:
       - bash-completion
       - bash-completion-extra
       - iotop  
```

- remote_user可用于Host和task中。也可以通过指定其通过sudo的方式在远程主机上执行任务，其可用于play全局或某任务；此外，甚至可以在sudo时使用sudo_user指定sudo时切换的用户。

- gather_facts不收集对应主机的信息，这样运行会快点。




#### 剧本功能实践介绍

##### 在剧本中设置变量信息

- 一个hosts设置的变量只能在当前hosts中使用

  ```
  - hosts:rsync_server
    vars:
      backupdir: /backup
      passfile: rsync.password
    - name: 04-create password file
      file: path={{ backupdir }}
    - name: 05-create password file
        	copy: content=rsync_backup:oldboy123 dest=/etc/{{ passfile }} mode=600
  
  - hosts:rsync_client
    vars:
      backupdir: /backup
      passfile: rsync.password
    - name: 04-create password file
      file: path={{ backupdir }}
    - name: 05-create password file
        	copy: content=rsync_backup:oldboy123 dest=/etc/{{ passfile }} mode=600
  ```

- 在执行的时候传入变量值，不同组相同变量名同时赋予相同的值

  ```
  - hosts:rsync_server
    - name: 04-create password file
      file: path={{ backupdir }}
    - name: 05-create password file
        	copy: content=rsync_backup:oldboy123 dest=/etc/{{ passfile }} mode=600
  
  - hosts:rsync_client
    - name: 04-create password file
      file: path={{ backupdir }}
    - name: 05-create password file
        	copy: content=rsync_backup:oldboy123 dest=/etc/{{ passfile }} mode=600
        	
  #执行命令
  ansible-playbook -e backupdir=/data -e passfile=rsync-password rsync_server.yaml
  ```

- 在主机清单中设置变量

  ```
  - hosts:rsync_server
    - name: 04-create password file
      file: path={{ backupdir }}
    - name: 05-create password file
        	copy: content=rsync_backup:oldboy123 dest=/etc/{{ passfile }} mode=600
  
  - hosts:rsync_client
    - name: 04-create password file
      file: path={{ backupdir }}
    - name: 05-create password file
        	copy: content=rsync_backup:oldboy123 dest=/etc/{{ passfile }} mode=600
  
  vim /etc/ansible/hosts
  
  [rsync_server]
  web01
  
  [rsync_server:vars]
  backupdir=/data
  passfile=rsync-password
  
  [rsync_client]
  web02
  web03
  [rsync_client:vars]
  passfile=rsync-password
  
  #执行剧本
  ansible-playbook rsync_server.yaml
  ```

- 三种变量设置方式都配置了，三种方式的优先级

  - 最优先：命令行变量设置
  - 次优先：剧本中变量设置
  - 最后：主机清单变量设置

- 如何设置全局变量：

  - roles
  - 剧本整合



##### 在剧本中设置注册信息（检查客户端服务是否开启，在执行剧本的时候可以显示信息）

```
- hosts: oldboy
  tasks:
    - name: check server port
      shell: netstat -lntup|grep 873  #端口信息
      register: get_server_port  #端口信息
    - name: display port info
      debug: msg={{ get_server_port.stdout_lines }}


stdout_lines:标准输出（显示美化）
```



##### 在剧本中设置判断信息

- 如何指定判断条件(setup模块中有的)，当when条件成立的时候执行name下的命令

  ```
  - hosts: oldboy
    tasks:
      - name: check server port
        shell: netstat -lntup|grep 873  #端口信息
        register: get_server_port  #端口信息
        when: (ansible_hostname == "nfs")
      - name: display port info
        debug: msg={{ get_server_port.stdout_lines }}
  ```
  
  

##### 在剧本中设置循环信息

```
vim test04.yml
- hosts: all
  tasks:
    - name: Add Users
      user: name={{ item.name }} groups={{ item.groups }} state=present
      with_items: 
        - { name: 'testuser1', groups: 'rsync' }
        - { name: 'testuser2', groups: 'testuser1' }
```

- 批量下载

  - ansible方式

    ```
    vim test05.yml
    - hosts: all
      tasks:
        - name: Installed Pkg
          yum: name={{ item }}  state=present
          with_items:
           - bash-completion
           - bash-completion-extra
           - iotop	
    ```

  - saltstack方式（推荐使用——ansible可以识别）

    ```
    - name: 01-install software
      yum:
        name: ['rsync','tree','wget']
        state: installed
    ```

    



##### 在剧本中设置忽略错误

- 默认playbook会检查命令和模块的返回状态，如遇到错误就中断playbook的执行，可以加入**ignore_errors: yes**忽略错误

```
- hosts: all
  remote_user: root
  gather_facts: no
  tasks:
    - name: Ignore False
      yum: name={{ item }}  state=installed
      with_items:
       - bash-completion
       - bash-completion-extra
       - iotop  
      ignore_errors: yes
    - name: touch new file
      file: path=/tmp/oldboy_ignore state=touch
```

- 如果不忽略后面的创建文件就不会执行
  - 错误是要安装的模块没有

- 忽略后面的创建文件命令就会执行



##### 在剧本中设置标签功能：单独执行剧本中的某个name

- 设置标签：tags

  ```
  #rsync.yaml
  
  - hosts: oldboy
    tasks:
      - name: check server port
        shell: netstat -lntup|grep 873  #端口信息
        register: get_server_port  #端口信息
        when: (ansible_hostname == "nfs")
        tags: check
      - name: display port info
        debug: msg={{ get_server_port.stdout_lines }}
        tags: output
  ```

- 执行剧本中的单个标签：**--tags**

  ```
  ansible-playbook --tags=check rsync.yaml
  ```

- 跳过某个标签执行其他的：**--skip-tags**

  ```
  ansible-playbook --skip-tags=check rsync.yaml
  ```



##### 在剧本中设置触发信息

```
- hosts: all
  tasks:
    - name: 01-push file
      copy: src=./remind_darling.sh dest=/tmp/
      notify: push
    - name: 02-install iotop
      yum: name=iotop state=installed
  handlers:
    - name: push
      copy: src=./1.txt dest=/tmp/
```

- **notify**设置的内容要和下面**handlers中name**设置的一样，才可以生效

- 当copy过去的文件在目标服务器中不存在或者文件内容不一样时就会触发下面的handlers

- 当目标服务器中有要传过去的文件并且文件内容一致的时候不触发

  

##### 将多个剧本整合

- 编写整合的脚本

  ```
  vim all.yaml
  
  - import_playbook: rsync-server.yaml
  - import_playbook: nfs-server.yaml
  ```

- 执行脚本

  ```
  ansible-playbook all.yaml
  相当于执行了
  rsync-server.yaml和nfs-server.yaml
  ```





