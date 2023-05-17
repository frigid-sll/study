
##### find：查找文件

- 精确查找

  ```
  find 找寻的路径范围 -type 类型信息 -name “文件名称”
  
  find /etc -type f -name "ifcfg-eth0"
  ```

- 不区分大小写进行查找

  ```
  find /old -type f -iname 'a*'
  
  -iname：不区分大小写
  ```

- 模糊查找

  ```
  文件名称记得不是很清楚忘记的部分可以用*代替
  
  #忽略大小写
  find / -type f -iname 'old*'
  ```

- 按照大小来查

  ```
  #查找old下文件大小大于100k的文件
  find /old -type f -size +100
  
  #查找old下文件大小小于100k的文件
  find /old -type f -size -100
  
  #查找old下文件大小大于1M的文件
  find /old -type f -size +1M
  ```

- 不查找下一级目录里面的内容，只查找当前目录

  ```
  find /old -maxdepth 1 -type f -name "old"
  
  #深入两级将数字1改为2 就可以。
  #-maxdepth最好放在路径的后面、其他的前面
  ```

- 根据数据的权限进行查找

  ```
  find /oldboy -maxdepth 1 -type f -perm 644
  ```

- 将查找的数据进行删除

  ```
  find /old -type f -name "*.txt" -delete
  或
  find /old -type f -name "*.txt" -exec rm -rf {}\;
  或
  find /old -type f -name "*.txt"|xargs rm -f
  或
  rm -rf $(find /old -type f -name "*.txt")
  
  -delete：将查找的结果文件进行删除
  -exec：要执行什么操作，命令依次执行前面的每一行
  {}：将前面执行的结果放到这里面
  \:将分号转义
  ；：批量进行操作
  
  $()等同于``，将后面的命令执行结果 交给前面的命令执行
  但是``执行结果是一行的
  
  如果没有``单独执行命令的结果是多行
  
  所以在用管道符号的时候前面命令的执行结果如果需要一行一行都要生效需要加xargs，将前面执行的多行结果转为1行
  ```

- 将找到的东西进行复制

  ```
  find /old -type f -name "*.txt" -exec cp {} /tmp \;
  
  或
  
  find /old -type f -name "*.txt" | xargs -i cp {} /tmp
  
  -i:将前面命令的执行结果放在括号里
  
  或
  find /old -type f -name "*.txt" | xargs cp -t /tmp
  
  -t：将要拷贝的内容和拷贝到的目录换一下位置
  ```

- 将查找的东西进行批量压缩

  ```
  #这样压缩会只把最后一个文件进行压缩，前面的都被覆盖了
  find /old -maxdepth 1 -type f -name "*.txt" -exec tar zcvf /old/txt.tar.gz {} \;
  
  #正确压缩方法
  find /old -maxdepth 1 -type f -name "*.txt"|xargs tar zcvf /old/txt.tar.gz
  或
  tar zcvf /old/txt.tar.gz `find /old -maxdepth 1 -type f -name "*.txt"`
  
  ```

- 根据inode查找文件

  ```
  find / -type f -inum inode号码
  ```

- 根据时间查找文件

  ```
  find /old -type -f -mtime +10
  
  +10:十天以前的数据
  -10:近十天的数据
  10:正好前面第十天
  ```

  