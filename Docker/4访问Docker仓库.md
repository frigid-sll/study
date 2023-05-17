##### 仓库(repository)是集中存放镜像的地方，又分<span style='color:red'>公共仓库</span>和<span style='color:red'>私有仓库</span>。

有时候容易把仓库与注册服务器混淆。实际上注册服务器是存放仓库的具体服务器，一个注册服务器上可以有多个仓库，而每个仓库下面可以有多个镜像。从这方面来说，仓库可以被认为是一个具体的项目或目录。例如对于仓库地址<a href=#>private-docker.com/ubuntu</a>来说，<a href='#'>private-docker.com</a>是注册服务器地址，ubuntu是仓库名。



在本章中，笔者将分别介绍使用 Docker Hub 官方仓库进行登录、下载等基本操作，以 及使用国内社区提供的仓库下载镜像；最后还将介绍创建和使用私有仓库的基本操作。



- #### Docker Hub 公共镜像市场

Docker Hub 是 Docker 官方提供的最大的公 共镜像仓库，目前包括了超过 100 000 的镜 像，地址为 https://hub.docker.com。 大部分对镜像的需求，都可以通过在 Docker Hub 中直接 下载镜像来实现



#### 1.登录

可以通过命令执行

```
docker login
```

命令来输入用户名、密码和邮箱来完成注册和登陆。注册成功后，本地用户目录下会自动创建<span style='color:red'><b>./docker/config.json</b></span>文件,保存用户的认证信息。

登陆成功的用户可以上传个人制作的镜像到Docker Hub.



#### 2.基本操作

用户无需登陆即可通过

```
docker search
```

命令来查找官方仓库中的镜像，并利用 

````
docker pull 
````

命令来将它下载到本地。

在镜像的章节（第 3 章），已经具体介绍了如何使用 docker [image] pull 命令来搜 寻镜像。 例如以 centos 为关键词进行搜索：

```
docker search centos 
```

根据是否为官方提供，可将这些镜像资源分为两类：

- 一种是类似于centos这样的基础镜像，也成为根镜像。这些镜像是由Docker公司创建、验证、支持、提供，这样的镜像往往使用单个单词作为名字； 
- 另一种类型的镜像，比如 ansible/centos7-ansible 镜像，是由 Docker 用户 ansible 创建并维护的，带有用户名称为前缀，表明是某用户下的某仓库。 可以通过 用户名称前缀“user name／镜像名”来指定使用某个用户提供的镜像。 



下载官方 centas 镜像到本地，代码如下所示：

```
 docker pull centos 
```

用户也可以在登录后通过 docker push 命令来将本地镜像推送到 Docker Hub。



#### 3.自动创建

自动创建（ Automated Builds）是 Docker Hub 提供的自动化服务，这一功能可以自动跟 随项目代码的变更而重新构建镜像。

例如，用户构建了某应用镜像，如果应用发布新版本，用户需要手动更新镜像。 而自动 创建则允许用户通过 Docker Hub 指定跟踪一个目标网站（目前支持 GitHub 或 BitBucket）上 的项目，一旦项目发生新的提交，则自动执行创建。

 要配置自动创建，包括如下的步骤： 

1 ）创建并登录 Docker Hub，以及目标网站如 Github; 

2 ）在目标网站中允许 Docker Hub 访问服务； 

3 ）在 Docker Hub 中配置一个“自动创建”类型的项目； 

4 ）选取一个目标网站中的项目（需要含 Dockerfile）和分支； 

5 ）指定 Dockerfile 的位置，并提交创建。 之后，可以在 Docker Hub 的“自动创建”页面中跟踪每次创建的状态。



#### 第三方镜像市场

国内不少云服务商都提供了 Docker 镜像市场包括腾讯云、 网易云、阿里云等。 下面 以时速云为例，介绍如何使用这些市场



##### 查看镜像 

访问 https://hub.tenxcloud.com，即可看到己存在的仓库和存储的镜像，包括 Ubuntu、 Java、 Mongo、 MySQL、 Nginx 等热 门仓库和镜像。 时速云官方仓库中的镜像会保持与 Docker Hub 中官方镜像的同步。 以 MongoDB 仓库为例 ，其中包括了 2.6、 3.0 和 3.2 等镜像。

##### 下载镜像

下载镜像也是使用 

```
docker pull 
```

命令，但是要在镜像名称前添加注册服务器的具体地 址。 格式为 

```
index . tenxcloud . com/<namespace>/<repository> : <tag＞
```

例如，要下载 Docker 官方仓库中的 node: latest 镜像，可以使用如下命令：

```
docker pull index tenxcloud.com/docker_library/node latest 
```

正常情况下，镜像下载会比直接从 Docker Hub 下载快得多。 通过 docker images 命令来查看下载到本地的镜像：

```
docker images 
```

下载后，可以更新镜像的标签，与官方标签保持一致，方便使用：

```
docker tag index.tenxcloud.com/docker_l工brary/node latest node latest 
```

除了使用这些公共镜像服务外，还可以搭建本地的私有仓库服务器，将在下一节介绍。



#### 搭建本地私有仓库

##### 使用registry镜像创建私有仓库

安装 Docker 后， 可以通过官方提供的 registry 镜像来简单搭建一套本地私有仓库环境：

```
 docker run -d -p 5000:5000 registry:2 
```

这将自动下载井启动一个 registry容器，创建本地的私有仓库服务。 

默认情况下，仓库会被创建在容器的／var/lib/registry目录下。 可以通过 －v 参数来将镜 像文件存放在本地的指定路径。 例如下面的例子将上传的镜像放到／opt/data/registry 目录：

```
 docker run -d -p 5000 5000 -v /opt / data/registry:/var/lib/registry registry: 2 
```

此时－， 在本地将启动一个私有仓库服务，监听端口为 5000。



##### 管理私有仓库

首先在本书环境的笔记本上（ Linux Mint）搭建私有仓库，查看其地址为 10 . 0.2.2: 5000 ，然后在虚拟机系统（Ubuntu 18.04 ）里测试上传和下载镜像。 

在 Ubuntu 18.04 系统查看已有的镜像：

```
docker images
```

使用docker tag 命令将这个镜像标记为10.0.2.2:5000/test(格式为 docker tag IMAGE [:TAG] [REGISTRY.HOST/] [USERNAME/] NAME [:TAG］)

```
 docker tag ubuntu:18.04 10.0.2.2:5000/test 
 docker images
```

使用 docker push 上传标记的镜像：

```
docker push 10.0.2.2:5000/test
```

用 curl 查看仓库10.0.2.2:5000 中的镜像：

```
 curl http://10 O 2 2 5000/v2/search 
```

在结果中可以看到｛＂ description":"","name" : library/test" ｝，表明镜 像已经成功上传了。

现在可以到任意一台能访问到10.0.2.2 地址的机器去下载这个镜像了。 

比较新的 Docker 版本对安全性要求较高，会要求仓库支持 SSL/TLS 证书。 对于内部使 用的私有仓库，可以自行配置证书或关闭对仓库的安全性检查。

首先，修改 Docker daemon 的启动参数，添加如下参数，表示信任这个私有仓库，不进 行安全证书检查：

```
DOCKER_OPTS;”--insecure-registry 10.0.2.2:5000”
```

之后重启Docker服务，并从私有仓库中下载镜像到本地：

```
systemctl restart docker
docker pull 10.0.2.2:5000/test 
```

下载后，还可以添加一个更通用的标签 ubuntu: 18. 04 ，方便后续使用 ：

```
 docker tag 10 .0.2.2 :5000/test ubuntu : lB.04 
```

如果要使用安全证书，用户也可以从较知名的 CA 服务商（如 verisign）申请公开的 SSL/TLS 证书，或者使用 OpenSSL 等软件来自行生成



#### 本章小结

仓库是集中维护容器镜像的地方，为 Docker 镜像文件的分发和管理提供了便捷的途径。 本章介绍的 Docker Hub 和时速云镜像市场两个公共仓库服务，可以方便个人用户进行镜像 的下载和使用等操作。

 在企业的生产环境中，往往需要使用私有仓库来维护内部镜像，本章介绍了基本的搭建 操作，在后续部分中，将介绍私有仓库的更多配置选项。

 除了官方的 regis町项目外，用户还可以使用其他的开源方案（例如 nexus）来搭建私 有化的容器镜像仓库。