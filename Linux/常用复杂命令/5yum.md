##### Linux系统指定使用软件仓库文件，yum源文件

- 本地配置yum源

  ```
  https://opsx.alibaba.com/mirror
  点centos帮助
  使用curl 命令
  作用：
  从阿里云下载一个yum文件，更新默认的/etc/yum.repos.d/CentOS-Base.repo
  ```

- 安装软件

  ```
  yum install vim
  
  #-y 不用每次确认，多个包之间空格隔开
  yum install -y tree wget net-tools nmap bash-completion
  
  
  bash-completion:自动补全
  bash-completion-extra:自动补全
  lrzsz：windwos和linux的文件进行相互传输
  ```


- 查看可用的yum源

  ```
  yum repolist
  ```


- 可以安装和已安装的所有软件

  ```
  yum list
  ```

- 可以安装和已安装的所有软件包组信息

  ```
  yum grouplist
  ```

- 安装软件包组的方法

  ```
  yum groupinstall -y Development Tools
  ```

- 卸载包

  ```
  #将依赖包也卸载了 极其不建议
  yum erase cowsay -y
  
  #建议使用rpm卸载，只卸载这个包，不卸载它的其他依赖包
  rpm -e 软件包名 --nodeps
  
  --nodeps：解决有依赖包在使用这个包
  ```

- 查看一个命令属于哪个大礼包

  ```
  #查看locate命令属于哪个包，然后进行yum下载
  yum provides locate
  ```
  
  



##### yum安装软件出现问题，排错流程

- 访问外网ip地址不通
  - 网卡地址配置有问题
- 访问外网名称不通
  - DNS配置有问题
    - ping DNS的ip
    - 如果不通进行修改，在本地查看网络以太网的DNS是多少
- 检查是否已经有下载的进程了
  - 会报错一个pid号



##### yum源下载优化

- Linux和Windows软件安装程序的区别

  - windows：exe
  - linux：rpm

- yum软件优势：简单、快捷

  - 不需要到官方网站单独下载软件包（yum仓库）
  - 可以解决软件的依赖关系

- yum优化（/etc/yum.repos.d/）

  - 优化基础的yum源文件

    - 通过阿里镜像源进行优化

  - 优化扩展的yum源（阿里云eplo选项）

    - 通过阿离镜像源进行优化

      ```
      wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7...
      ```

  - 检查可用的yum源信息

    ```
    yum repolist
    ```

- 好玩的软件包

  ```
  sl
  cowsay 内容
  animalsay 内容
  bash-completion：补全命令
  ```

- 确认软件是否安装

  ```
  rpm -qa sl 查看软件包是否存在
  
  rpm -ql sl 查看软件包有哪些东西
  
  
  
  rpm -qf `which ssh` 查看系统文件中是属于哪个软件包
  
  q：query 查询
  a：all 所有
  l：list 列表显示
  f；file 文件
  ```

