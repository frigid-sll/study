- ##### 将nginx.config的user改为和启动用户一致

```
vim conf/nginx.conf
```

<img src="https://img-blog.csdn.net/20170718094235060?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvb25seXN1bm55Ym95/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center">

- ##### 缺少index.html或者index.php文件，就是配置文件中index index.html index.htm这行中的指定的文件。

```
server {
        listen       80;
        listen       [::]:80;
        server_name  121.41.90.219;
        root         /usr/share/nginx/html/wordpress;
        index        index.php index.html;                  ######这里！！
    }   

```

- ##### 权限问题，如果nginx没有web目录的操作权限，也会出现403错误。

```
chmod -R 777 wordpress/
```

- ##### SELinux设置为开启状态（enabled）的原因。

  - 查看当前selinux的状态

    ```
    /usr/sbin/sestatus
    ```

  - 将SELINUX=enforcing 修改为 SELINUX=disabled 状态

    ```
    vi /etc/selinux/config
    
    ###修改内容：
    #SELINUX=enforcing
    SELINUX=disabled
    ```

  - 重启

    ```
    reboot
    ```

    

