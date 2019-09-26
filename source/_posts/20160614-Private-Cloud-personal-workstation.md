---
title: Private Cloud personal workstation
date: 2016-06-14 18:31:20
category: Cloud
tags: DIY
---
DIY个人工作站，终于开始投入使用了，在做虚拟化的时候遇到了一些小问题，纪录一下！

主机到手之后，各种性能测试，各种安装系统各种折腾了一把，发现兼容性良好，没啥大问题，没崩万幸。

后续终于确定使用一款操作系统，但是为了方便演示企业级环境，我弄了vmware产品，启动时提示如下：

* 此主机支持 Intel VT-x,但Intel VT-x处于禁用状态。
  - 如果已经在bios/固件设置中禁用intel tv-x,或者主机更改此设置后从未重新启动，则intel tv-x可能被禁用

* 解决，在bios开启此项功能
  - 1、重启主机，启动的时候根据提示按键进入bios设置页面，我的是f2
  - 2、选择configutation,在选择intel virtual technology，此时选项是disabled
  - 3、将disabled改为enabled
  - 4、保存设置，重启

![](https://www.itweet.cn/screenshots/virtualization-configuartion.png)

* 硬件
    - CPU E5-2683 V3 (new)
    - 24核心、CPU x5650*2、32G内存、240G SSD，2TB硬盘 (old)


原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/
