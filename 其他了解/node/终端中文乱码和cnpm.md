```
打开配置文件 vim ~/.zshrc
在文件适当处添加如下代码

export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

source ~/.zshrc
```



```
方法一：安装cnpm镜像
这个是比较常用的方法，我首先也是使用了这个方法。

cnpm的安装方法，参考http://npm.taobao.org/


npm install -g cnpm --registry=https://registry.npm.taobao.org
在cmd中输入以上命令就可以了，然后再使用cnpm安装


cnpm install -g nodemon
后面的操作跟不使用镜像的操作是差不多的。


方法二：使用代理registry
在网上查阅了一些资料后，决定使用代理的方式，方法也很简单，就是


npm config set registry https://registry.npm.taobao.org
然后后续的install等命令还是通过npm运作，而不是cnpm。

查看全局安装的npm包
npm ls -g
```

