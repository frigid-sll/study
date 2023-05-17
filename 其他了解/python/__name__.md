Python中的模块（.py文件）在创建之初会自动加载一些内建变量，`__name__`就是其中之一。Python模块中通常会定义很多变量和函数，这些变量和函数相当于模块中的一个功能，模块被导入到别的文件中，可以调用这些变量和函数。那么这时 `__name__ `的作用就彰显了，它可以标识模块的名字，可以显示一个模块的某功能是被自己执行还是被别的文件调用执行，假设模块A、B，模块A自己定义了功能C,模块B调用模块A，现在功能C被执行了：

如果C被A自己执行，也就是说模块执行了自己定义的功能，那么 __name__=='__main__'

如果C被B调用执行，也就是说当前模块调用执行了别的模块的功能，那么__name__=='A'（被调用模块的名字）

其实换一种说法也就是表示当前程序运行在哪一个模块中

下面举例说明：

首先自定义模块Student,在模块中定义功能Differ()

![img](https://img-blog.csdn.net/20180803104030307?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3htcDE2NjkyMTczMjc=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

然后先自身执行，结果如下， __name__=='__main__'

 ![img](https://img-blog.csdn.net/20180803104720293?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3htcDE2NjkyMTczMjc=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

然后B调用执行，结果 __name__=='Student'

​         ![img](https://img-blog.csdn.net/20180803104903268?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3htcDE2NjkyMTczMjc=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)![img](https://img-blog.csdn.net/20180803104928588?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3htcDE2NjkyMTczMjc=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

上面出两次结果，是因为python中导入模块会先将文件执行一遍，如下图

![img](https://img-blog.csdn.net/20180803105230704?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3htcDE2NjkyMTczMjc=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

到这儿可能有人已经注意到，上面的 __main__ 在python中作可以为函数的入口，而实际工程常用 if __name__=='__main__'来表示整个工程开始运行的入口。此外你如果不想让功能的某部分被别的模块调用执行，比如我自定的模块Student里的‘我的密码是xxx’,只有自己执行才可以打印密码。所有你可以把部分写在if语句里，只有__name__=='__main__'的时候才能执行。这个可以这么理解，在if语句之外代码是最外层的，有点“全局变量”的意思，放入if里面就成了私有的了。

