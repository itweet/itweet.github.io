---
title: linux for Desktop
date: 2016-05-14 17:22:29
category: Linux
tags: desktop
---
由于集群在安装的时候，选择最小化min安装方式，而且自定义选择安装的libary。而没有选择安装图形化界面，这样在实际生产环境中是推荐的方式。完全基于terminal方式管理Linux服务器。
但是，某些特殊时期，需要通过图形画界面进行一些特殊的操作，比如我遇到的，需要在Linux服务器中安装一个图形化[VMware-Workstation](https://jikelab.github.io/tech-labs/2015/11/23/linux-install-vm/)软件，做虚拟化实验环境。这样的需求虽然比较少见，但是也得满足，下面我就来写一写在Linux中安装图形化组件的方法。

# 查看目前Linux包组安装情况
```
yum grouplist
```

# 安装包组桌面程序
``` 
yum -y groupinstall Desktop 
```

# 安装x window程序
```
yum -y groupinstall "X Window System"
```

# 启动图形化界面
```
xstart
```

# 安装火狐浏览器
```
 yum install firefox -y
```


原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/
