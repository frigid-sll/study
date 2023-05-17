##### 系统中如何对文件进行压缩处理：tar

- 语法

  ```
  tar zcvf /oldboy/old.tar.gz 指定要压缩的文件
  
  z：压缩的方式为zip
  c：创建压缩包文件
  v：显示压缩的过程
  f：指定压缩包文件路径信息
  f一定要写在最后
  
  tar zcvhf /oldboy/old.tar.gz /etc
  
  h：要写在f的前面，要打包的文件里面如果有软链接文件 打包的是软链接的指向文件，这样就可以避免打包后的链接文件无效
  ```

- 检查是否压缩成功

  - 将原文件先进性移走,防止解压后覆盖原文件

    ```
    mv /oldboy/services /tmp
    ```

  - 解压数据包

    ```
    tar xvf /oldboy/old.tar.gz
    
    x:extract 提取，解压包
    C:指定解压后文件的路径
    
    tar xvfC  1.txt.tar.gz /www/
    ```

  - 检查解压后的文件和原文件是否一样

    - diff

      ```
      diff /oldboy/oldboy/old /tmp/old
      #如果一致不报任何信息
      #如果不一致会出现提示
      前面文件的行数a后面文件的行数
      结果
      ```

    - vimdiff

      ```
      vimdiff /oldboy/oldboy/old /tmp/old
      ```

- 在不解压的情况下查看压缩包里面的数据

  ```
  tar tf /old.tar.gz
  ```

- 压缩过程信息说明

  ```
  tar：Removing leading '/' from member names
  默认将压缩时绝对路径的根信息就行移除
  
  用相对路径进行压缩的时候就不会进行提示，解压后也没有绝对路径的目录结构 
  ```

- 在压缩文件的时候将有些文件不进行压缩

  ```
  tar zcvf /tmp/old.tar.gz ./oldboy --exclude=./oldboy/1.txt
  
  exclude 排除
  include 包含
  要进行压缩的文件和要排除的文件要么都用绝对路径，要么都是相对路径，不然会排除失败
  ```

- 在压缩文件的时候批量文件不进行压缩

  - 编写好排除文件

    ```
    vim /tmp/exclude.txt
    /oldboy/1.txt
    /oldboy/1.png
    /oldboy/1.jpg
    ```

  - 执行命令进行批量排除

    ```
    tar zcvf /tmp/old.tar.gz /oldboy --exclude-from=/tmp/exclude.txt
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