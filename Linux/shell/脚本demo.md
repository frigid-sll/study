##### 修改网卡信息然后记录：幂等性，一个脚本不用修改就可以对多个主机进行操作并且达到想要的结果

```
#!/bin/bash

#01. edior network ip info
sed -i "s#(10.0.)0(.200)#\11\2#g" /etc/简写路径/ifcfg-eth0 && \

#02. restart netwrok server
systemctl restart network && \

#03. 获取主机地址信息
echo "服务器修改后IP地址：`hostname -I`" >> /tmp/oldboy.txt
```



##### 使用变量批量创建目录

```
dir=oldgirl

mkdir /$dir/oldboy01
mkdir /$dir/oldboy02
mkdir /$dir/oldboy03
```





##### 如何要求输入的必须是整数

```
1.sh
#!/bin/bash

read -p "请输入第一个整数：" num
expr 1 + $num &>/dev/null
[ $? -ne 0 ] && echo "请输入整数" && exit 1
read -p "请输入第二个整数" num1
expr 1 + $num1 &>/dev/null
[ $? -ne 0 ] && echo "请输入整数" && exit 2
echo "$num+$num1=$[$num+$num1]"


或
test=123qqq
[[ $test =~ ^[0-9]+$ ]]
echo $?
```



##### 查看ip

```
curl cip.cc | awk 'NR==1 {print $3}'
```



##### Linux添加默认路由 route

```
route add default gw 10.0.0.254
route del default gw 10.0.0.254

ip route add 0/0 via 10.0.0.254
ip route del 0/0 via 10.0.0.254

0/0：从哪里来的都行 
```

- 查看路由表
  ```
  route -n
  ```

- 网卡添加ip地址

  ```
  for i in {10..200};do ip addr add 10.0.0.$i/24 dev eth0;done 
  ```

- 策略路由

  ```
  #查看策略路由
  ip ro list
  
  [root@pert ~]# cat /etc/iproute2/rt_tables
  #
  # reserved values
  #
  255     local
  254     main
  253     default
  0       unspec
  #
  # local
  #
  #1      inr.ruhep
  ```

- 添加一个表，给这个表设置一个路由

  - 编辑配置文件

    ```
    vim /etc/iproute2/rt_tables
    #
    # reserved values
    #
    255     local
    254     main
    253     default
    0       unspec
    200			test
    #
    # local
    #
    #1      inr.ruhep
    
    
    200是优先级，比前面小就可以了
    test 是添加的表名
    ```

  - 命令添加

    ```
    ip route add 0/0 via 10.0.0.254 table test
    ip rule add from 10.0.0.1 table test
    
    只要从10.0.0.1来的出的时候都走的test表，走的是test表里的网关
    
    10.0.0.1是你公司的公网ip 
    ```

    

  

