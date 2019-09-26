---
title: 如何在CentOS上安装配置ownCloud
date: 2016-08-14 16:38:20
category: BigData
tags: owncloud
---
据其官方网站，ownCloud可以让你通过一个Web界面或者WebDAV访问你的文件。它还提供了一个平台，可以轻松地查看、编辑和同步您所有设备的通讯录、日历和书签。尽管ownCloud与广泛使用Dropbox非常相似，但主要区别在于ownCloud是免费的，开源的，从而可以自己的服务器上建立与Dropbox类似的云存储服务。使用ownCloud你可以完整地访问和控制您的私人数据，而对存储空间（除了硬盘容量）或客户端的连接数量没有限制。

ownCloud提供了社区版（免费）和企业版（面向企业的有偿支持）。预编译的ownCloud社区版可以提供了CentOS、Debian、Fedora、openSUSE、，SLE和Ubuntu版本。本教程将演示如何在Debian Wheezy上安装和在配置ownCloud社区版。

在CentOS上安装 ownCloud,进入官方网站：http://owncloud.org，并点击‘Download'按钮。
在"Get Started!"页面选择， ”Get ownCloud Server“栏目的“Download”，进入下一个页面选择"packages for auto updates"按钮。左下方点击“continue”。可以进入一个支持多操作系统的选项，选择自己操作系统的图标，在下方即可下载对应操作系统的安装包。

ownCloud还提供了几种选择，比如：[“appliances for easy deployment”](https://owncloud.org/install/#instructions-server)，提供多种系统版本的云镜像文件，可以通过镜像文件直接创建带有ownCloud的云主机。页面直接可以下载到，基于ubuntu 14制作的多种格式的镜像：

- [OVA](http://download.owncloud.org/community/production/vm/Ubuntu_14.04-owncloud-9.1.0-1.1-201607211103.ova.zip)
- [QCOW2](http://download.owncloud.org/community/production/vm/Ubuntu_14.04-owncloud-9.1.0-1.1-201607211103.qcow2.zip)
- [RAW](http://download.owncloud.org/community/production/vm/Ubuntu_14.04-owncloud-9.1.0-1.1-201607211103.raw.zip)
- [VHDX](http://download.owncloud.org/community/production/vm/Ubuntu_14.04-owncloud-9.1.0-1.1-201607211103.vhdx.zip)
- [VMDK](http://download.owncloud.org/community/production/vm/Ubuntu_14.04-owncloud-9.1.0-1.1-201607211103.vmdk.zip)
- [VMX](http://download.owncloud.org/community/production/vm/Ubuntu_14.04-owncloud-9.1.0-1.1-201607211103.vmx.zip)

除官方提供的上面镜像之外，还有第三方提供的各种操作系统的云镜像供选择，页面直接可跳转到对应的系统下载地址。

这里CentOS安装包下载地址为：https://download.owncloud.org/download/repositories/stable/owncloud/

选择对应的操作系统版本，选择centos，即可出来对应centos6.x , centos 7.x的安装方法，继续。。。

* 关闭防火墙
```
/etc/init.d/iptables stop
```

* Mysql Install
```
yum install mysql-server

/etc/init.d/mysqld start

chkconfig mysqld on

mysql_secure_installation   # init ...

mysql -uroot -padmin

mysql> create database owncloud;
```

* 添加仓库地址到centos 6.x系统中
```
rpm --import https://download.owncloud.org/download/repositories/stable/CentOS_6/repodata/repomd.xml.key
```

* Install OwnCloud by CentOS 6.x
 
 参考：`https://download.owncloud.org/download/repositories/stable/owncloud/`

```
wget http://download.owncloud.org/download/repositories/stable/CentOS_6/ce:stable.repo -O /etc/yum.repos.d/ce:stable.repo

yum clean expire-cache

yum search owncloud

wget https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm
wget https://rpms.remirepo.net/enterprise/remi-release-6.rpm
rpm -Uvh epel-release-latest-6.noarch.rpm
rpm -Uvh remi-release-6.rpm

yum install owncloud    

/etc/init.d/httpd start

netstat -lntop |grep 80
```

* 打开你的浏览器并定位到你的ownCloud实例中，地址是 http://your_ip/owncloud/   
 `访问请注意，性能告警，默认使用数据库SQLite，可以通过前段修改为mysql,设置管理员密码`

* 安装桌面同步或移动客户端等
打开链接：http://owncloud.org/install/ 有适用于Windows, Mac OS X， Linux， iOS， Android客户端。选择下载，安装即可。

桌面同步客户端可以连续同步、选择文件夹同步、多文件夹同步。多文件夹同步是你可以同步对多个文件夹位置进行同步到多个ownCloud文件夹下。

ownCloud的使用过程基本跟主流云存储服务商雷同，就不一一细述了。
这是一个面向企业或者个人的私有云存储系统，让用户在各大服务商提供的服务之外能有别的选择。至少，数据是真正掌握在自己手中的。

把个人数据放家里的私有数据中心里面也是不错的选择。这里推荐一款不错的小型塔式服务器HP MicroServer Gen8 E3-1230V2 8G,特点就是容量够大，可以放入6块3T硬盘。个人完全够用啦。当然你也可以自己DIY一个服务器放家里，也是很好的选择，我自己就[DIY](https://www.itweet.cn/2016/06/14/private-cloud/)了一个32g，24虚拟机内核,1块ssd安装系统，2块sata做数据盘这样的配置放家里。当然我安装私有云在上面，可惜配置太低起不了几个云服务器。如果你家里有一个私有云，直接无需安装，下载ownload提供的ubuntu镜像即可自动生成带有owncloud功能的云主机，直接使用。最好把它数据存储目录，存储到私有云的云盘之中，好扩展。

* 为了保证，有足够的存储空间
  底层可以修改为一个分布式文件系统架构，这样就可以变成一个分布式云盘，或者挂载一个大硬盘。
```
  setenforce 0
  cd /var/www/html/owncloud/

  mv data data_bak
  mkdir data

  mount /dev/vdb /var/www/html/owncloud/data

  chown apache:apache data
  chmod 774 data
  chmod o-r data

  mv data_bak/* data/
  mv data_bak/.ocdata  data/
  mv data_bak/.htaccess data/
```

例如：
```
[root@cockroach-test owncloud]# df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/vda1        50G  1.7G   45G   4% /
tmpfs           939M     0  939M   0% /dev/shm
/dev/vdb        985G  461M  934G   1% /var/www/html/owncloud/data
```

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/
