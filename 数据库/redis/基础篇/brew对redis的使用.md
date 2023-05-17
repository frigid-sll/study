##### 安装某个工具，例如redis。默认安装的是稳定版本

```
brew install redis
```



##### 查找某个软件包

```
brew search **
```



##### 列出已经安装的软件的包

```
brew list
```



##### 卸载某个软件的包

```
brew uninstall **
```



##### 更新某个软件包

```
brew upgrade **
```



##### 查看指定软件包的说明

```
brew info **
```



##### 清理缓存

```
brew cache clean
```



##### 启动某个服务(redis)

```
brew services start redis
```



##### Redis第一次启动

```
redis-server /opt/homebrew/etc/redis.conf
```





##### 验证是否启动

```
redis-cli ping
```



##### 关闭redis服务

```
brew services stop redis
```



##### 重启服务

```
brew services restart redis
```



##### 打开图形化界面

```
redis-cli
```



##### 允许远程访问

```
vim /opt/homebrew/etc/redis.conf

注释bind，默认情况下redis不允许远程访问，只允许本机访问
#bind 127.0.0.1

注：在redis3.2之后，redis增加了protected-mode，在这个模式下，即使注释掉了bind 127.0.0.1，再访问redisd时候还是报错，需要把protected-mode yes改为protected-mode no
```









