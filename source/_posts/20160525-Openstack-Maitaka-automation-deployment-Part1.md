---
title: Openstack Maitaka automation deployment Part1
date: 2016-05-25 18:12:37
category: Cloud
tags: openstack
---
OpenStack是IaaS(基础设施即服务)组件，让任何人都可以自行建立和提供云端运算服务。
此外，OpenStack也用作建立防火墙内的“私有云”（Private Cloud），提供机构或企业内各部门共享资源。

OpenStack很可能在未来的基础设施即服务（IaaS）资源管理方面占据领导位置，成为公有云、私有云及混合云管理的“云操作系统”标准。

[Openstack](http://docs.openstack.org/)在企业级私有云市场目前是比较有希望的，目前我们就在公司内部构建基于openstack企业级私有云平台，根据硬件区分为两套软件架构，一套x86私有云，一套power高性私有云。

个人在使用和研究Openstack过程中，发现openstack目前虽然有很多不成熟的地方，但是企业级私有云架构的确非常合适，他有几个优点：
    1. 降低使用虚拟化软件产品的成本，在易用性上面已经做的非常出色，相比早期的KVM。
    2. 为开发测试提供虚拟资源弹性管理。
    3. 集成现有测试工具提供云端的测试服务。
    4. 通过openstack+docker+other实现软件系统自动化架构，

参考: [企业级开发平台持续集成自动化架构](https://www.itweet.cn/2016/05/05/Enterprise-Application-Development-Platform-Automatic-System/)

我个人在家里也弄了一套基于openstack的环境，自己DIY服务器，配置还算强劲吧，主要用做自己的开源项目使用，说实话真的非常方便，从此再也不用折腾vmware workstation，在家的工作站也够用。后面我打算把openstack做成一个系列文章，从基础软件自动化部署，到各个openstack组件的使用，openstack生产环境架构设计，后端存储设计，网络规划，镜像，虚拟机等方面展开。因为我觉得openstack是一个值得我大写特写的开源软件，初次使用我就被他深深吸引住了。很多模块功能设计的非常有意思。

今天，开启`openstack系列`专题第一篇内容，怎么通过redhat提供的rdo自动化安装openstack Maitaka版本。

# openstack allinone
  通过allinone可以自动化安装openstack集群。

# 基础环境

## 必备条件
  + Centos 7/Redhat7 最小化安装系统。
  + openstack-mitaka 版本
  + ssh免密码登录。
  + Linux基础优化/selinux关闭/关闭防火墙。

```
$ cat /etc/redhat-release 
 CentOS Linux release 7.2.1511 (Core)

$ sestatus -v
SELinux status:                 disabled  ＃关闭selinux

$ systemctl stop firewalld.service #停止firewall
$ systemctl disable firewalld.service #禁止firewall开机启动

$ echo '* - nofile 65535' >>  /etc/security/limits.conf
$ tail -1  /etc/security/limits.conf

$ cat /etc/environment 
LANG=en_US.utf-8
LC_ALL=en_US.utf-8

$ cat /etc/hosts|tail -2
172.16.0.210    openstack-controller        
172.16.0.148    openstack-compute1      
```

# Install Openstack Mitaka For allinone

## For Centos 7.x
  * 1、 install 
  
```
  $ sudo yum install -y centos-release-openstack-mitaka
  $ sudo yum update –y
  $ sudo yum install -y openstack-packstack
```
  
  * 2、 auto configuation
```
  $ sudo packstack --allinone
```
  看到如下图信息，说明安装成功。这样所有的服务都安装到了一台机器上，controller和compute节点都在一台服务器上，当然compute是可以不断自动添加节点进来的。
 
 ![](https://www.itweet.cn/screenshots/openstack-success.png)

## For Redhat 7.x 
```
$ sudo yum install -y https://www.rdoproject.org/repos/rdo-release.rpm
$ sudo yum update -y
$ sudo yum install -y openstack-packstack
$ packstack --allinone
```

## Installation Sucessfully
*  安装成功后，在／root下面生成两个keystone权限验证文件
```
[root@openstack-controller ~]# cat keystonerc_admin 
unset OS_SERVICE_TOKEN
export OS_USERNAME=admin
export OS_PASSWORD=06e9b0c19fa34890
export OS_AUTH_URL=http://192.168.0.200:5000/v2.0
export PS1='[\u@\h \W(keystone_admin)]\$ '

export OS_TENANT_NAME=admin
export OS_REGION_NAME=RegionOne

[root@openstack-controller ~]# cat keystonerc_demo 
unset OS_SERVICE_TOKEN
export OS_USERNAME=demo
export OS_PASSWORD=a3f02b1b68d444f0
export PS1='[\u@\h \W(keystone_demo)]\$ '
export OS_AUTH_URL=http://192.168.0.200:5000/v2.0

export OS_TENANT_NAME=demo
export OS_IDENTITY_API_VERSION=2.0

--source 才能有权限查询到相关的信息
[root@openstack-controller ~]# source keystonerc_admin 
[root@openstack-controller ~(keystone_admin)]# nova list --all-tenants

[root@openstack-controller ~(keystone_admin)]# keystone user-list
[root@openstack-controller~(keystone_admin)]# keystone service-list
[root@openstack-controller ~(keystone_admin)]# nova host-list
+-----------------------+-------------+----------+
| host_name             | service     | zone     |
+-----------------------+-------------+----------+
| openstack-controller  | cert        | internal |
| openstack-controller  | consoleauth | internal |
| openstack-controller  | scheduler   | internal |
| openstack-controller  | conductor   | internal |
| openstack-controller  | compute     | nova     |
+-----------------------+-------------+----------+
```
    
*  通过dashboard访问openstack
    Dashboard WebUI: http://openstack-controller/dashboard
    Dashboard Username/password: admin/your keystonerc_admin password

## Allinone Install openstack , You can also generate an answer file and use it on other systems
``` 
  $ sudo packstack --gen-answer-file=answerfile.txt
  $ cat answerfile.txt |wc -l
   1297
```

## Openstack网络配置

- OpenStack提供多种网络架构:
    + dhcp flat
    + VLAN
    + Vxlan
    + Linux bridge
    + GRE

   openstack网络类型包括flat、dhcp flat、vlan,vxlan,我这里选择vxlan方式; 
   `ps: openstack专题系列后面会有专门写网络架构设计内容.`

```
[root@openstack-controller network-scripts]# cat ifcfg-br-ex 
NAME="br-ex"
DEVICE="br-ex"
DEVICETYPE=ovs
TYPE=OVSBridge
ONBOOT=yes
IPV6INIT=no
BOOTPROTO=none
DNS1=114.114.114.114
DOMAIN=openstack-conntroller
DEFROUTE=yes
IPV4_FAILURE_FATAL=no
IPADDR=172.16.0.210
PREFIX=24
GATEWAY=172.16.0.1

[root@openstack-controller network-scripts]# cat ifcfg-eno16777736
NAME="eno16777736"
DEVICE="eno16777736"
ONBOOT="yes"
IPV6INIT=no
BOOTPROTO=none
DEVICETYPE=ovs
TYPE=OVSPort
OVS_BRIDGE=br-ex

[root@openstack-controller ~(keystone_admin)]#  systemctl restart network.service

[root@openstack-controller ~(keystone_admin)]#  systemctl status network.service
```

注意：这里的网络配置，在dashboard还需要做一些路由和private_sub,public_sub网络创建并且通过路由连接，才能正常使用，包括配置浮动IP，内网IP等。这里先略过，后续文章继续介绍。

## Dashboard可视化创建虚拟机

![](https://www.itweet.cn/screenshots/cloud_machine_list.png)

* 后端虚拟机运行状态查询
```
[root@openstack-controller ~(keystone_admin)]# virsh list --all
 Id    Name                           State
----------------------------------------------------
 11    instance-00000015              running
 12    instance-00000013              running

[root@openstack-compute ~]# virsh list --all
 Id    Name                           State
----------------------------------------------------
 6     instance-00000014              running
```

* 通过秘钥登陆虚拟机,CentOS-7-x86_64-GenericCloud官方提供的虚拟机仅仅支持秘钥登录
```
[whoami@openstack-controller .ssh]$ ssh -i whoami.key centos@172.16.0.219
[centos@test ~]$ sudo su - root
[centos@test ~]$ sudo -s
```

## Centos官方镜像
 * cirros镜像：http://download.cirros-cloud.net/0.3.4/
 
 * Images: http://cloud.centos.org/centos/7/images/
 
 * Dashboard页面上传镜像,通过本地文件，选择QCOW2类型，选择本地镜像源，取名后即可导入镜像:
```
$ wget http://download.cirros-cloud.net/0.3.4/cirros-0.3.4-x86_64-disk.img

[root@openstack-controller ~(keystone_admin)]# glance image-list
+--------------------------------------+------------------------------+
| ID                                   | Name                         |
+--------------------------------------+------------------------------+
| 112f10c4-af34-4fb5-bfea-af85d8652f8d | CentOS-7-x86_64-GenericCloud |
| 27598aa1-9cb3-490f-a76e-963ec46392c1 | cirros-0.3.4-x86_64          |
+--------------------------------------+------------------------------+
```

## Openstack Cinder－块存储（Block Storage）
[Cinder](https://wiki.openstack.org/wiki/CinderSupportMatrix)默认是实用volume lvm的存储方式，生产中根据不同的业务，肯定需要设计不同的存储架构；而Cinder就给我们提供了后端多种主流存储类型，比如：Ceph，Glusterfs，nfs, lvm；Cinder更像是一个存储接口，可以适配各种后端存储类型。

cinder与swift各自的用途是什么？

cinder是块存储，用来给虚拟机挂扩展硬盘，就是将cinder创建出来的卷，挂到虚拟机里。cinder是OpenStack到F版，将之前在Nova中的部分持久性块存储功能（Nova-Volume）分离了出来，独立为新的组件Cinder。

swift是一个系统，可以上传和下载，里面一般存储的是不经常修改的内容，比如用于存储 VM 镜像、备份和归档以及较小的文件，例如照片和电子邮件消息。更倾向于系统的管理。

块存储具有安全可靠、高并发大吞吐量、低时延、规格丰富、简单易用的特点，适用于文件系统、数据库或者其他需要原始块设备的系统软件或应用。

cinder理解为云硬盘，可以为任何虚拟机扩容存储，可以随意格式化，随时存取，并且支持多种后端存储类型，并且可以当做和Linux本地文件系统一样使用，没有任何成本，而他支持的各种后端存储类型，都有各自的特性比如集群可以冗余，副本防止数据丢失风险等优点; 对于swift可以作为网盘，用过云盘的应该不陌生，可以用来备份重要但是不常用的数据。

`Openstack专题系列后面会有专题写cinder后端存储架构设计内容。`

## FAQ
  - 看到后台都安装那些rpm包：
```
    tailf /var/log/messages
```
  
  - yum安装信息
```
    cat /var/log/yum.log |wc -l
    392
```
 
 - 服务异常排查
```   
查后台相关服务日志和进程状态
   $ sudo openstack-status |grep neutron
```


- 参考：
    + networking：https://www.rdoproject.org/networking/neutron-with-existing-external-network/
    + adding-a-compute-node: https://www.rdoproject.org/install/adding-a-compute-node/
    + Highly Available Openstack Deployments：https://github.com/beekhof/osp-ha-deploy/blob/master/ha-openstack.md
    + http://www.opencontrail.org/rdo-openstack-opencontrail-integration/

