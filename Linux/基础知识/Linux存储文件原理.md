### cp 引发的思考 

今天用 `cp` 命令，给惊到了！背景是这样的：他用 `cp` 拷贝了一个 100 G的文件，竟然一秒不到就拷贝完成了！

用 `ls` 看一把文件，显示文件确实是 100 G。

```
sh-4.4# ls -lh
-rw-r--r-- 1 root root 100G Mar  6 12:22 test.txt
```

但是copy起来为什么会这么快呢？

```
sh-4.4# time cp ./test.txt ./test.txt.cp

real 0m0.107s
user 0m0.008s
sys 0m0.085s
```

一个 SATA 机械盘的写能力能到 150 M/s （大部分的机械盘都是到不了这个值的）就算非常不错了，正常情况下，copy 一个 100G 的文件至少要 682 秒 ( 100 G/ 150 M/s )，也就是 11 分钟。

实际情况却是 `cp` 一秒没到就完成了工作，惊呆了，为啥呢？

更诡异的是：他的文件系统只有 40 G，为啥里面会有一个 100 G的文件呢？

同事把我找来，看看这个诡异的问题。

#### 分析文件

我让他先用 `du` 命令看一下，却只有 2M ，根本不是100G，这是怎么回事？

```
sh-4.4# du -sh ./test.txt
2.0M ./test.txt
```

再看 `stat` 命令显示的信息：

```
sh-4.4# stat ./test.txt
  File: ./test.txt
  Size: 107374182400 Blocks: 4096       IO Block: 4096   regular file
Device: 78h/120d Inode: 3148347     Links: 1
Access: (0644/-rw-r--r--)  Uid: (    0/    root)   Gid: (    0/    root)
Access: 2021-03-13 12:22:00.888871000 +0000
Modify: 2021-03-13 12:22:46.562243000 +0000
Change: 2021-03-13 12:22:46.562243000 +0000
 Birth: -
```

`stat` 命令输出解释：

1. Size 为 107374182400（知识点：单位是字节），也就是 100G ；
2. Blocks 这个指标显示为 4096（知识点：**一个 Block 的单位固定是 512 字节**，也就是一个扇区的大小），这里表示为 2M；

划重点：

- Size 表示的是文件大小，这个也是大多数人看到的大小；
- Blocks 表示的是物理实际占用空间；

同事问道：“**文件大小和实际物理占用，这两个竟然不是相同的概念 ！为什么是这样？**”

“看来，我们必须得深入文件系统才能理解了，来，我给你好好讲讲。”

### 文件系统

文件系统听起来很高大上，通俗话就用来存数据的一个容器而已，本质和你的行李箱、仓库没有啥区别，只不过文件系统存储的是数字产品而已。

我有一个视频文件，我把这个视频放到这个文件系统里，下次来拿，要能拿到我完整的视频文件数据，这就是文件系统，对外提供的就是存取服务。

#### 现实的存取场景

例如你到火车站使用寄存服务：

**存行李的时候**，是不是要登记一些个人信息？对吧，至少自己名字要写上。可能还会给你一个牌子，让你挂手上，这个东西就是为了标示每一个唯一的行李。



**取行李的时候**，要报自己名字，有牌子的给他牌子，然后工作人员才能去特定的位置找到你的行李

![图片](https://mmbiz.qpic.cn/mmbiz_gif/KyXfCrME6ULJj5Pt7XZcQJ4u58uicgZxBVFsR8Ml54rzR5lsKm1Lp15wJ1f5DQ4n1gIhBdn4nVTiasnCRoWY2Jhg/640?wx_fmt=gif&wxfrom=5&wx_lazy=1)

> 划重点：存的时候必须记录一些关键信息（记录ID、给身份牌），取的时候才能正确定位到。

#### 文件系统

回到我们的文件系统，对比上面的行李存取行为，可以做个简单的类比；

1. 登记名字就是在文件系统记录文件名；
2. 生成的牌子就是元数据索引；
3. 你的行李就是文件；
4. 寄存室就是磁盘（容纳东西的物理空间）；
5. 管理员整套运行机制就是文件系统；

上面的对应并不是非常严谨，仅仅是帮助大家理解文件系统而已，让大家知道其实文件系统是非常朴实的一个东西，思想都来源于生活。

#### 空间管理

现在思考文件系统是怎么管理空间的？

如果，一个连续的大磁盘空间给你使用，你会怎么使用这段空间呢？

直观的一个想法，我把进来的数据就完整的放进去。

![图片](https://mmbiz.qpic.cn/mmbiz_gif/KyXfCrME6ULJj5Pt7XZcQJ4u58uicgZxBX8PEwpw5pkNIElcbK9J7BYsQgBvp926nydGicic5G8PKlITibI4eSzRCg/640?wx_fmt=gif&wxfrom=5&wx_lazy=1)

这种方式非常容易实现，属于眼前最简单，以后最麻烦的方式。因为会造成很多空洞，明明还有很多空间位置，但是由于整个太大，形状不合适（数据大小），哪里都放不下。因为你要放一个完整的空间。

怎么改进？有人会想，既然整个放不进去，那就剁碎了呗。这里塞一点，那里塞一点，就塞进去了。

对，思路完全正确。**改进的方式就是切分，把空间按照一定粒度切分**。每个小粒度的物理块命名为 Block，**每个 Block 一般是 4K 大小**，用户数据存到文件系统里来自然也是要切分，存储到磁盘上各个角落。

![图片](https://mmbiz.qpic.cn/mmbiz_gif/KyXfCrME6ULJj5Pt7XZcQJ4u58uicgZxBl4ADMvZqBAYrJ4T006Pztp0AhVW22xmwUIiajK44IJiah9lZjz835KeA/640?wx_fmt=gif&wxfrom=5&wx_lazy=1)

图示标号表示这个完整对象的 Block 的序号，用来复原对象用的。

随之而来又有一个问题：你光会切成块还不行，取文件数据的时候，还得把它们给组合起来才行。

**所以，要有一个表记录文件对应所有 Block 的位置，这个表被文件系统称为inode。**

写文件的流程是这样的：

1. 先写数据：数据先按照 Block 粒度存储到磁盘的各个位置；
2. 再写元数据：然后把 Block 所在的各个位置保存起来，即**inode**（我用一本书来表示）；

![图片](https://mmbiz.qpic.cn/mmbiz_gif/KyXfCrME6ULJj5Pt7XZcQJ4u58uicgZxBKtVmF3xWobXOdWnBZ4iaMib7k0RboTJBXArvnkI5Z8xY0yqoNrk2b8Hg/640?wx_fmt=gif&wxfrom=5&wx_lazy=1)

读文件流程则是：

1. 先读inode，找到各个 Block 的位置；
2. 然后读数据，构造一个完整的文件，给到用户；

![图片](https://mmbiz.qpic.cn/mmbiz_gif/KyXfCrME6ULJj5Pt7XZcQJ4u58uicgZxBb4wC8Sa37qibvgBRCSia4ec3GYHKlF6tIAe5wAC6ickXADOQK6W4faYtg/640?wx_fmt=gif&wxfrom=5&wx_lazy=1)

#### inode/block 概念

好，我们现在来看看inode，直观地感受一下：



这个inode有**文件元数据**和**Block数组**（长度是15），数组中前两项指向Block 3和Block 11，表示数据在这两个块中存着。

你肯定会意识到：Block数组只有15个元素，每个Block是4K， 难道一个文件最大只能是 15 * 4K =  60 K ?

这是绝对不行的！

最简单的办法就是：把这个Block数组长度给扩大！

比如我们想让文件系统最大支持100G的文件，Block数组需要这么长：

(100\*1024*1024)/4 = 26214400

Block数组中每一项是4个字节，那就需要(26214400*4)/1024/1024 = **100M**

为了支持100G的文件，我们的Block数组本身就得100M ！



并且对每个文件都是如此 ！即使这个文件只有1K！**这将是巨大浪费！**

肯定不能这么干，解决方案就是间接索引，按照约定，把这 15 个槽位分作 4 个不同类别来用：

1. 前 12 个槽位（也就是 0 - 11 ）我们成为**直接索引；**
2. 第 13 个位置，我们称为 1 级索引；
3. 第 14 个位置，我们称为 2 级索引；
4. 第 15 个位置，我们称为 3 级索引；

![图片](https://mmbiz.qpic.cn/mmbiz_png/4UtmXsuLoNd7TgWQgNicxERn4VwB6EKE0Gicqy7iaDaf0M6sgFjAwZY3JvxJuNjiauK63eoqUwzMY8ShUE6O1heNIw/640?wx_fmt=png&wxfrom=5&wx_lazy=1&wx_co=1)

直接索引：能存 12 个 block 编号，每个 block 4K，就是 `48K`，也就是说，48K 以内的文件，前 12 个槽位存储编号就能完全 hold 住。

**一级索引：**

也就是说这里存储的编号指向的 block 里面存储的也是 block 编号，里面的编号指向用户数据。一个 block  4K，**每个元素 4 字节**，也就是有 1024 个编号位置可以存储。所以，一级索引能寻址 `4M（1024 * 4K）`空间 。

![图片](https://mmbiz.qpic.cn/mmbiz_png/KyXfCrME6ULJj5Pt7XZcQJ4u58uicgZxBQQkssF7zK1eXc3U70SpPbzZNQNgsku6p8icn4CnDRjnxSc8RqibCpImg/640?wx_fmt=png&wxfrom=5&wx_lazy=1&wx_co=1)

**二级索引：**

二级索引是在一级索引的基础上多了一级而已，换算下来，有了 4M 的空间用来存储用户数据的编号。所以二级索引能寻址 `4G (4M/4 * 4K)` 的空间。

![图片](https://mmbiz.qpic.cn/mmbiz_png/KyXfCrME6ULJj5Pt7XZcQJ4u58uicgZxBBazl4SCfnb6RRV27LWXdp2FOYvVRz2Ircl6KY2c74tLbFyNrsUrgeg/640?wx_fmt=png&wxfrom=5&wx_lazy=1&wx_co=1)

**三级索引：**

三级索引是在二级索引的基础上又多了一级，也就是说，有了 4G 的空间来存储用户数据的 block 编号。所以二级索引能寻址 4T （4G/4 * 4K） 的空间。

![图片](https://mmbiz.qpic.cn/mmbiz_png/KyXfCrME6ULJj5Pt7XZcQJ4u58uicgZxBwEqE6zriaUZDtxSA7p4AQGyicHl0qFwDQu53dJc0KoqRTPuCVLr0VIlA/640?wx_fmt=png&wxfrom=5&wx_lazy=1&wx_co=1)

所以，在这种文件系统（如ext2）上，通过这种间接块索引的方式，最大能支撑的文件大小 = 48K + 4M + 4G + 4T ，约等于 4 T。

**这种多级索引寻址性能表现怎么样？**

- 在不超过 12 个数据块的小文件的寻址是最快的，访问文件中的任意数据理论只需要两次读盘，
  - 一次读 inode，一次读数据块。
- 访问大文件中的数据则需要最多五次读盘操作：
  - inode、一级间接寻址块、二级间接寻址块、三级间接寻址块、数据块。

#### 为什么cp那么快？

接下来我们要写入一个奇怪的文件，这个文件很大，但是真正的数据只有8K：

在[0,4K]这位置有4K的数据

在[1T , 1T+4K] 处也有4K数据

中间没有数据，这样的文件该如何写入硬盘？

1. 创建一个文件，这个时候分配一个 inode；
2. 在 [ 0，4K ] 的位置写入 4K 数据，这个时候只需要 一个 block，把这个编号写到 `block[0]` 这个位置保存起来；
3. 在 [ 1T，1T+4K ] 的位置写入 4K 数据，这个时候需要分配一个 block，因为这个位置已经落到三级索引才能表现的空间了，所以需要还需要分配出 3 个索引块；
4. 写入完成，close 文件；

**实际存储如图：**

![图片](https://mmbiz.qpic.cn/mmbiz_png/KyXfCrME6ULJj5Pt7XZcQJ4u58uicgZxB2jXc2BWvc6rt0fIyStcK5p3oiczrWmgINWZISyDxX2oMHn5kya3Hribg/640?wx_fmt=png&wxfrom=5&wx_lazy=1&wx_co=1)

这个时候，我们的文件看起来是超大文件，size 等于 1T+4K ，但里面实际的数据只有 8 K，位置分别是  [ 0，4K ] ，[ 1T，1T+4K ]。

由于没写数据的地方不用分配物理block块，所以实际占用的物理空间只有8K。

> **重点：文件 size 只是 inode 里面的一个属性，实际物理空间占用则是要看用户数据放了多少个 block ，没写数据的地方不用分配物理block块。**

这样的文件其实就是稀疏文件， 它的逻辑大小和实际物理空间是不相等的。

所以当我们用cp命令去复制一个这样的文件时，那肯定迅速就完成了。

#### 总结

好，我们再深入思考下，文件系统为什么能做到这一点？

1. 首先，最关键的是把磁盘空间切成离散的、定长的 block 来管理；
2. 然后，通过 inode 能查找到所有离散的数据（保存了所有的索引）；
3. 最后，实现索引块和数据块空间的后分配；

这三点是层层递进的。