##### rpm

```
rpm -qa sl 查看软件包是否存在

rpm -ql sl 查看软件包有哪些东西



rpm -qf `which ssh` 查看系统文件中是属于哪个软件包

q：query 查询
a：all 所有
l：list 列表显示
f；file 文件rpm -qa sl 查看软件包是否存在

rpm -ql sl 查看软件包有哪些东西

q：query 查询
a：all 所有
l：list 列表显示

#卸载单个软件包，不卸载依赖包。yum erase 软件包名会把依赖包也卸载了
rpm -e 软件包名 --nodeps

e：erase 抹除
--nodeps：解决有依赖包在使用这个包

rpm  -ivh 软件包名称.rpm
-i 	install 安装
-v	显示过程信息
-h	human	以人类可读方式展示信息
无法解决软件依赖
```



##### ss==netstat

```
ss -lntup

-l list 		 列表显示
-n number    显示端口号
-t tcp			 显示tcp网络协议
-u udp       显示udp网络协议
-p process		 进程信息显示出来

如何有netstat命令
yum instll -y net-tools

```

