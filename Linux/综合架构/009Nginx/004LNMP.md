##### 网站的LNMP架构是什么？

- L：Linux系统
  - selinux必须关闭，防火墙关闭
  - /tmp 1777权限
- N：Nginx服务
  - 处理用户的静态请求
- P：PHP服务
  - 处理动态的页面请求
  - 负责和数据库建立关系
- M：mysql服务（Mariadb）
  - 存储用户的字符串数据信息



##### 网站的LNMP架构部署

- nginx：ansible一键化部署

- mysql服务部署

  - 第一个历程：yum安装

    ```
    yum install mariadb-server mariadb -y
    ```

  - 第二个历程：启动数据库服务

    ```
    systemctl start mariadb.service
    systemctl enable mariadb.service
    ```

  - 第三个历程：设置密码

    ```
    mysqladmin -u root password '设置的密码'
    ```

  - 第四个历程：进入服务

    ```
    mysql -uroot -p设置的密码
    ```

- php服务部署

  - 第一个历程：更新yum源/卸载系统自带的php软件

    ```
    yum remove php-mysql php php-fpm php-common
    ```

  - 第二个历程：安装php软件

    ```
    yum install -y php71w php71w-cli php71w-common php71w-devel php71w-embedded php71w-gd php71w-mcrypt php71w-mbstring php71w-pdo php71w-xml php71w-fpm php71w-mysqlnd php71w-opcache php71w-pecl-memcached php71w-pecl-redis php71w-pecl-mongodb
    ```

  - 第三个历程：编写配置文件

    ```
    vim /etc/php-fpm.d/www.conf
    
    user = www
    group = www
    
    #保证nginx进程管理的用户与php管理的用户一致
    ```

  - 第四个历程：启动php服务

    ```
    systemctl start php-fpm
    ```



##### LNMP架构的原理：nginx+mysql+php

![image-20230209184357540](/Users/pert./Library/Application Support/typora-user-images/image-20230209184357540.png)

用户访问网站——>nginx(fastcgi_pass)——>FastCGI——>(php-fpm —— wrapper) php（php解析器）——> mysql（读取或写入）



##### 实现LNMP之间建立关系

- 编写nginx配置文件

  ```
  server {
    listen 80;
    server_name blog.com;
    location / {
      root /html/blog;
      index index.html;
    }
    location ~ \.php$ {
      root /www;  #php的站点目录
      fastcgi_index index.php;  #访问php没有默认访问的就是index.php
      fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name; #需要传输完整的参数，变量在下面include
      fastcgi_pass 127.0.0.1:9000;  #如果是php 转到9000端口
      include fastcgi_params;  #导入变量
    }
  }
  ```

- 重启nginx服务

  ```
  systemctl restart nginx
  ```

- 编写动态资源文件

  ```
  cd /www
  vim test.php
  
  <?php
  phpinfo();
  ?>
  ```

- 进行访问测试

  ```
  blog.com/test.php
  ```

  



##### 测试链接数据库

```
[rootewebol blog]# vim test mysql .php
<?php
$servername = "1ocalhost";
$username = "root"：
$password = "oldboy123";
//link id-mysql connect('主机名，，，用户，，，舒码，）：
//mysq1 -u用户 -p密码 -h 主机
$conn = mysql_connect($servername, $username,$password)；
if ($conn)
{
	echo "mysql successful by root !\n";
}else{
	die ("Connection failed: " . mysql_connect_error())；
}
?>
```



#####  部署搭建网站页面（代码上线）

- 第一个历程：获取代码信息——wordpress

- 第二个历程：将代码解压，解压后信息放入站点目录中

- 第三个历程：修改站点目录权限

  ```
  chown -R www.www 目录
  ```

- 第四个历程：进行网站页面初始化

- 第五个历程：对数据库服务进行配置

  - 创建数据库并检查

    ```
    create database wordpress;
    show databases;
    ```

  - 创建数据库管理用户并检查

    ```
    grant all on wordpress.* to 'wordpress'@'localhost' identified by 'wordpress用户密码'
    
    #给localhost的wordpress用户赋予wordpress库里所有表的all（增删改查）权限
    
    select user,host from mysql.user;
    ```

- 修改配置文件

  ```
  server {
    listen 80;
    server_name blog.com;
    location / {
      root /html/blog;
      index index.php index.html;
    }
    location ~ \.php$ {
      root /www;  #php的站点目录
      fastcgi_index index.php;  
      fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
      fastcgi_pass 127.0.0.1:9000;  
      include fastcgi_params;  
    }
  }
  
  #需要加上index.php,不然访问的时候默认访问的是index.html没有用，默认访问index.php的时候就交给9000端口处理了
  ```

  

  

##### 上传wordpress主题，报413错误，如何解决？

- 修改nginx配置文件vim blog.conf

  ```
  在server_name后面一行添加
  client_max_body_size 50m;
  修改nginx上传文件的大小限制，默认1M
  ```

- 修改php配置文件

  ```
  vim php.ini
  
  upload_max_filesize = 50M
  #修改php上传文件的大小限制，默认2M
  ```



##### 如何让LNMP架构和存储服务器建立联系？

- 根据图片链接地址获取图片存储位置：uri

-  使web服务器和存储服务器建立关系
  - 检查存储服务器是否正常
  - 编写存储服务配置文件
  
- 将web服务器blog存储的数据进行迁移

- 将目录进行挂载

- 挂载好后将迁移的数据恢复过来

- 默认存储服务器无法存储数据
  - 管理用户无法存储：nfs默认配置root_squash：将root用户映射为nfsnobody
  - 普通用户无法存储：nfs默认配置no_all_squash，不将普通用户身份进行映射
  
- 解决
  
  - 修改nfs配置文件，定义映射用户为www，因为web服务器那边的权限是www，nfs目录权限的是nfsnobody
  
    ```
    useradd www -u 1002
    chown -R www /data
    ```
  
  - 使root用户可以上传数据，anonuid可以指定的映射用户，将之前默认修改客户端的用户nfsnobody为www
  
    ```
    sed -ri.bak 's#(sync)#\1,anonuid=1002,anongid=1002#g' /etc/exports
    ```
  
- 重启服务
  
  ```
  systemctl reload nfs
  ```
  
  

