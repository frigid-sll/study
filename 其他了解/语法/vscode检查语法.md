##### 安装格式化工具

- 打开命令行窗口安装以下工具

  ```
  pip install -U flake8
  pip install -U autopep8
  ```

- 在VScode配置中打开首选项–>设置，搜索`python.linting.flake8enabled`
  

##### 安装完成后，Visual Studio Code可以通过以下快捷键 格式化代码：

```
On Windows 　　Shift + Alt + F

On Mac 　　Shift + Option + F

On Ubuntu　　 Ctrl + Shift + I
```

- 如果右下角跳出来让你安装的提示，点yes就可以了



##### 如果是想检查所有代码的话

- 安装tox
  ```
  pip install tox
  ```

- 执行检查命令

  ```
  tox -e pep8
  ```

所有不符合pep8规则的都会展示出来，一个个文件改就行了






