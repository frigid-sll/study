##### 安装

```
brew tap mongodb/brew
brew install mongodb-community@4.4
```

@ 符号后面的 4.4 是最新版本号。
安装信息：

- 安装路径：/opt/homebrew/Cellar/mongodb-community@4.4/4.4.18
- 运行 MongoDB
  - 我们可以使用 brew 命令或 mongod 命令来启动服务。

```
brew 启动：
brew services start mongodb-community@4.4
brew 停止：
brew services stop mongodb-community@4.4
```

- 建立软链接

  ```
  ln -s /opt/homebrew/Cellar/mongodb-community@4.4/4.4.18/bin/mongo /opt/homebrew/bin/mongo
  ```

  



##### brew安装命令

```
可选择国内下载源
/bin/zsh -c "$(curl -fsSL https://gitee.com/cunkai/HomebrewCN/raw/master/Homebrew.sh)"

        Brew自动安装程序运行完成
          国内地址已经配置完成
  桌面的Old_Homebrew文件夹，大致看看没有你需要的可以删除。
              初步介绍几个brew命令
本地软件库列表：brew ls
查找软件：brew search google（其中google替换为要查找的关键字）
查看brew版本：brew -v  更新brew版本：brew update
安装cask软件：brew install --cask firefox 把firefox换成你要安装的
        
        欢迎右键点击下方地址-打开URL 来给点个赞
         https://zhuanlan.zhihu.com/p/111014448 
 安装成功 但还需要重启终端 或者 运行 source /Users/jiakang/.zprofile   否则可能无法使用


brew uninstall --cask google-chrome

切换镜像源 参考
https://blog.csdn.net/H_WeiC/article/details/107857302

```





