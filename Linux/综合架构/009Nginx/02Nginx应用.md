##### 利用nginx服务搭建一个网站（www）

- 第一个历程：编写虚拟主机配置文件

  ```
  cd /etc/nginx/conf.d/
  #扩展名只能是.conf。因为主配置文件里加载的.conf
  #cat /etc/nginx/nginx.conf
  #include /etc/nginx/conf.d/*.conf
  
  vim www.conf
  server {
  	listen 80;
  	server_name 域名;
  	location /oldboy {
  		root /usr/share/nginx/html;
  		index index.html;
  	}
  }
  ```

- 第二个历程：需要获取开发人员编写的网站代码（首页代码）

- 第三个历程：重启nginx服务

  ```
  systemctl reload nginx
  或
  nginx -s reload
  ```

  - 检查语法是否正确

    ```
    nginx -t
    或全部显示配置文件
    nginx -T
    ```

- 第四个历程：编写DNS配置信息

  - 真实域名：在阿里云上进行DNS解析记录配置

  - 模拟域名：在电脑里配置hosts文件

    ```
    ip 域名
    ```

- 第五个历程：进行测试访问



##### 访问过程原理说明：先去找root然后找location最后找index

- listen：访问端口

- server_name：ip或域名（域名需要解析）

- location：

  - /：不需要额外创建目录

  - /有内容：需要额外创建目录

    ```
    [root@pert nginx]# cat test.conf 
    server {
      listen 777;
      server_name linglong.fun;
      location /old {
        root /www/wwwroot/test_nginx/html;
        index index.html;
      }
    }
    
    [root@pert html]# pwd
    /www/wwwroot/test_nginx/html
    [root@pert html]# tree
    .
    └── old
        └── index.html
    ```

  - 访问时输入linglong.fun:777/old即访问的是index.html

- root：站点目录（**目录权限要是配置文件里面设置的属主和属组**）

- index：首页文件

**PS：如果有重复的地址端口，展示的是最先设置的**



##### 部署搭建网站常见错误

- 服务配置文件编写不正确
  - 404错误
    - 修改nginx配置文件：location
    - 在站点目录中创建相应目录或文件数据信息
  - 403错误
    - 不要禁止访问
    - 没有首页文件
- DNS信息配置不正确
- 配置文件修改一定要重启服务；站点目录中代码文件信息调整不需要重启服务
- 站点目录权限设置要正确



##### 企业中虚拟主机访问方式

- 基于域名的方式进行访问

- 基于地址的方式进行访问

  ```
  server {
    listen 10.0.0.7:80;
    server_name linglong.fun;
    location /old {
      root /www/wwwroot/test_nginx/html;
      index index.html;
    }
  }
  
  只能用10.0.0.7进行访问
  地址修改重启只能使用systemctl restart nginx
  用reload无效
  查看哪些ip可以访问
  netstat -nptl|grep nginx
  ```

- 基于端口的方式进行访问

  ```
  server {
    listen 777;
    server_name linglong.fun;
    location /old {
      root /www/wwwroot/test_nginx/html;
      index index.html;
    }
  }
  ```



##### 网站页面的访问原理

- 将域名进行解析：www.baidu.com —— 180.101.50.242
- 建立TCP的连接（四层协议）
  - 180.101.50.242 目标端口 80
- 根据应用层HTTP协议发出请求
  - 请求报文：hosts：www.baidu.com
- 没有相同域名的server主机，会找满足端口要求的第一个主机
  - 显示主机的网站页面



##### 企业中网站的安全访问配置

- 根据用户访问的地址进行控制

  - 10.0.0.0/24 www.oldboy.com/AV/ 不能访问

  - 172.16.1.0/24 www.oldboy.com/AV/ 可以访问

    - 局部配置

      ```
      server {
        listen 777;
        server_name linglong.fun;
        location /old {
          root /www/wwwroot/test_nginx/html;
          index index.html;
        }
        location /AV {
          root /www/wwwroot/test_nginx/html;
          index index.html;
          deny 10.0.0.0/24;
          allow 172.16.1.0/24;
        }
      }
      ```

    - 全局配置，每个location都识别的是同一个root和index

      ```
      server {
        listen 777;
        server_name linglong.fun;
        root /www/wwwroot/test_nginx/html;
        index index.html;
        location /AV {
          deny 10.0.0.0/24;
          allow 172.16.1.0/24;
        }
      }
      ```

  - 补充：

    - location外面的信息：全局配置信息
    - location内部的信息：局部配置信息

- 根据用户访问进行认证（需要输入账号密码）

  - 第一个历程：编写配置文件

    ```
    server {
      listen 777;
      server_name linglong.fun;
      location /old {
        root /www/wwwroot/test_nginx/html;
        index index.html;
        auth_basic  "开启用户认证";
        auth_basic_user_file password/htpasswd;
      }
      location /AV {
        root /www/wwwroot/test_nginx/html;
        index index.html;
        deny 10.0.0.0/24;
        allow 172.16.1.0/24;
      }
    }
    ```

  - 第二个历程：创建密码文件（文件中密码信息必须是密文的）

    -  查询是否安装

      ```
      rpm -qf `which htpasswd`
      ```

    - 安装htpasswd

      ```
      yum install -y httpd
      ```

    - htpasswd参数说明

      | 参数 | 解释                                          |
      | ---- | --------------------------------------------- |
      | -c   | 创建一个密码文件                              |
      | -n   | 不会更新文件，显示文件内容信息                |
      | -b   | 免交互方式输入用户密码信息                    |
      | -i   | 读取密码采用标准输入方式并不做检查            |
      | -m   | md5的加密算法（默认）                         |
      | -B   | 其他的加密方式                                |
      | C    | 其他的加密方式                                |
      | -d   | 其他的加密方式                                |
      | -s   | 其他的加密方式                                |
      | -p   | 不进行加密                                    |
      | -D   | 删除加密文件<br />htpasswd -D 文件 文件用户名 |
      | -V   |                                               |

    - 创建密码文件（记住bc就可以了）

      ```
      htpasswd -bc ./htpasswd 用户名 密码
      ```

    - 修改密码文件权限

      ```
      chmod 600 ./htpasswd
      #属主和属组都改成nginx.conf里面设置的worker进程属主和属组
      chown www.www ./htpasswd
      ```



##### Nginx模块

- nginx访问模块：ngx_http_access_moudle，举例配置：

  ```
  location / {
    deny 192.168.1.1;
    allow 192.168.1.0/24;
    allow 10.1.1.0/16;
    allow 2001:0db8::/32
    deny all;
  }
  ```

- nginx认证模块：ngx_http_auth_basic_module

  ```
  location / {
    auth_basic  "closed site";  #开启认证功能,后面的内容随便写，是一个提示作用，但是要有这一行
    auth_basic_user_file conf/htpasswd;  #加载用户密码文件，最好用相对路径，也可以用绝对路径
  }
  ```