##### 安装

```
brew search anaconda
brew install anaconda
```

##### 验证

```
conda --version
```

##### 卸载

```
rm -rf ~/anaconda3
```

**更新conda至最新版本**

```text
conda update conda
```

**创建新环境**

```text
conda create --name <env_name> <package_names>

conda create --name python2 python=2.7 ，即创建一个名为“python2”的环境，环境中安装版本为2.7的python


指定路径
conda create  -p /Users/pert/Documents/odoo-14.0/env python=3.8


```

**切换环境**

```text
source activate <env_name>
```

##### 退出环境

```
source deactivate
```

**显示已创建环境**

```text
conda info --envs
```

或

```text
conda info -e
```

或

```text
conda env list
```



**复制环境**

```text
conda create --name <new_env_name> --clone <copied_env_name>
```



- 注意：

① ***<copied_env_name>\*** 即为被复制/克隆环境名。环境名两边不加尖括号“<>”。

② ***<new_env_name>\*** 即为复制之后新环境的名称。环境名两边不加尖括号“<>”。

③ ***conda create --name py2 --clone python2\*** ，即为克隆名为“python2”的环境，克隆后的新环境名为“py2”。此时，环境中将同时存在“python2”和“py2”环境，且两个环境的配置相同。



**6. 删除环境**

```text
conda remove --name <env_name> --all
```

- 注意： ***<env_name>\*** 为被删除环境的名称。环境名两边不加尖括号“<>”。
