晚上有空，又在VMware虚拟机上安装了CentOS 7.7版本，在配置好网络后，在安装nginx时出现以下错误：



问题原因：
在百度上查了一下，出现这个的原因是因为本地yum源中没有我们想要的nginx，那么我们就需要下载新的CentOS-Base.repo。

解决步骤：
1、备份原来的CentOS-Base.repo

mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.bak20200321
2、下载新的CentOS-Base.repo 到/etc/yum.repos.d/

####centos 6版本
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-6.repo

####centos 7版本
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo

####centos 8版本
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-8.repo
3、运行 yum makecache

作用：就是把服务器的包信息下载到本地电脑缓存起来，makecache建立一个缓存，以后用install时就在缓存中搜索，提高了速度。

4、安装epel源

yum -y install epel-release 
5、安装NGINX服务

yum -y install nginx
————————————————
版权声明：本文为CSDN博主「-纸短情长」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/l_liangkk/article/details/105003088
