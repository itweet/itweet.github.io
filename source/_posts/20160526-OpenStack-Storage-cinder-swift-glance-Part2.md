---
title: OpenStack Storage cinder-swift-glance Part2
date: 2016-05-26 18:14:02
category: Cloud
tags: openstack
---
Swift——提供对象存储 （Object Storage），在概念上类似于Amazon S3服务，不过swift具有很强的扩展性、冗余和持久性，也兼容S3 API
Glance——提供虚机镜像（Image）存储和管理，包括了很多与Amazon AMI catalog相似的功能。（Glance的后台数据从最初的实践来看是存放在Swift的）。
Cinder——提供块存储（Block Storage），类似于Amazon的EBS块存储服务，目前仅给虚机挂载使用。
（Amazon一直是OpenStack设计之初的假象对手和挑战对象，所以基本上关键的功能模块都有对应项目。除了上面提到的三个组件，对于AWS中的重要的EC2服务，OpenStack中是Nova来对应，并且保持和EC2 API的兼容性，有不同的方法可以实现）
三个组件中，Glance主要是虚机镜像的管理，所以相对简单；Swift作为对象存储已经很成熟，连CloudStack也支持它。Cinder是比较新出现的块存储，设计理念不错，并且和商业存储有结合的机会，所以厂商比较积极。
![](https://jikelab.github.io/tech-labs/screenshots/openstack-framework.png)

# Swift应用
![](https://jikelab.github.io/tech-labs/screenshots/openstack-swift.png)

## 1.网盘。
Swift的对称分布式架构和多proxy多节点的设计导致它从基因里就适合于多用户大并发的应用模式，最典型的应用莫过于类似Dropbox的网盘应用，Dropbox去年底已经突破一亿用户数，对于这种规模的访问，良好的架构设计是能够支撑的根本原因。
Swift的对称架构使得数据节点从逻辑上看处于同级别，每台节点上同时都具有数据和相关的元数据。并且元数据的核心数据结构使用的是哈希环，一致性哈希算法对于节点的增减都只需重定位环空间中的一小部分数据,具有较好的容错性和可扩展性。另外数据是无状态的，每个数据在磁盘上都是完整的存储。这几点综合起来保证了存储的本身的良好的扩展性。
另外和应用的结合上，Swift是说HTTP协议这种语言的，这使得应用和存储的交互变得简单，不需要考虑底层基础构架的细节，应用软件不需要进行任何的修改就可以让系统整体扩展到非常大的程度。

## 2.IaaS公有云
Swift在设计中的线性扩展，高并发和多租户支持等特性，使得它也非常适合做为IaaS的选择，公有云规模较大，更多的遇到大量虚机并发启动这种情况，所以对于虚机镜像的后台存储具体来说，实际上的挑战在于大数据（超过G）的并发读性能，Swift在OpenStack中一开始就是作为镜像库的后台存储，经过RACKSpace上千台机器的部署规模下的数年实践，Swift已经被证明是一个成熟的选择。
另外如果基于IaaS要提供上层的SaaS 服务，多租户是一个不可避免的问题，Swift的架构设计本身就是支持多租户的，这样对接起来更方便。

## 3.备份归档
RackSpace的主营业务就是数据的备份归档，所以Swift在这个领域也是久经考验，同时他们还延展出一种新业务--“热归档”。由于长尾效应，数据可能被调用的时间窗越来越长，热归档能够保证应用归档数据能够在分钟级别重新获取，和传统磁带机归档方案中的数小时而言，是一个很大的进步。

## 4. 移动互联网和CDN
移动互联网和手机游戏等产生大量的用户数据，数据量不是很大但是用户数很多，这也是Swift能够处理的领域。

至于加上CDN，如果使用Swift，云存储就可以直接响应移动设备，不需要专门的服务器去响应这个HTTP的请求，也不需要在数据传输中再经过移动设备上的文件系统，直接是用HTTP 协议上传云端。如果把经常被平台访问的数据缓存起来，利用一定的优化机制，数据可以从不同的地点分发到你的用户那里，这样就能提高访问的速度，我最近看到Swift的开发社区有人在讨论视频网站应用和Swift的结合，窃以为是值得关注的方向。

# Glance应用
Glance比较简单，是一个虚机镜像的存储。向前端nova（或者是安装了Glance-client的其他虚拟管理平台）提供镜像服务，包括存储，查询和检索。这个模块本身不存储大量的数据，需要挂载后台存储（Swift，S3。。。）来存放实际的镜像数据。
![](https://jikelab.github.io/tech-labs/screenshots/openstack-glance.png)

Glance主要包括下面几个部分：
1.API service： glance-api 主要是用来接受Nova的各种api调用请求，将请求放入RBMQ交由后台处理，。

2.Glacne-registry 用来和MySQL数据库进行交互，存储或者获取镜像的元数据，注意，刚才在Swift中提到，Swift在自己的Storage Server中是不保存元数据的，这儿的元数据是指保存在MySQL数据库中的关于镜像的一些信息，这个元数据是属于Glance的。

3.Image store： 后台存储接口，通过它获取镜像，后台挂载的默认存储是Swift，但同时也支持Amazon S3等其他的镜像。

Glance从某种角度上看起来有点像虚拟存储，也提供API，可以实现比较完整的镜像管理功能。所以理论上其他云平台也可以使用它。

Glance比较简单，又限于云内部，所以没啥可以多展开讨论的，不如看看新出来的块存储组件Cinder，目前我对Cinder基本的看法是总体的设计不错，细节和功能还有很多需要完善的地方，离一个成熟的产品还有点距离。

Cinder
OpenStack到F版本有比较大的改变，其中之一就是将之前在Nova中的部分持久性块存储功能（Nova-Volume）分离了出来，独立为新的组件Cinder。它通过整合后端多种存储，用API接口为外界提供块存储服务，主要核心是对卷的管理，允许对卷，卷的类型，卷的快照进行处理。

# cinder 应用
![](https://jikelab.github.io/tech-labs/screenshots/openstack-cinder.png)

Cinder包含以下三个主要组成部分

API service：Cinder-api 是主要服务接口, 负责接受和处理外界的API请求，并将请求放入RabbitMQ队列，交由后端执行。 Cinder目前提供Volume API V2

Scheduler service: 处理任务队列的任务，并根据预定策略选择合适的Volume Service节点来执行任务。目前版本的cinder仅仅提供了一个Simple Scheduler, 该调度器选择卷数量最少的一个活跃节点来创建卷。

Volume service: 该服务运行在存储节点上，管理存储空间，塔处理cinder数据库的维护状态的读写请求，通过消息队列和直接在块存储设备或软件上与其他进程交互。每个存储节点都有一个Volume Service，若干个这样的存储节点联合起来可以构成一个存储资源池。

Cinder通过添加不同厂商的指定drivers来为了支持不同类型和型号的存储。目前能支持的商业存储设备有EMC 和IBM的几款，也能通过LVM支持本地存储和NFS协议支持NAS存储，所以Netapp的NAS应该也没问题，新的glusterfs,ceph多种后端存储支持。Cinder主要和Openstack的Nova内部交互，为之提供虚机实例所需要的卷Attach上去，但是理论上也可以单独向外界提供块存储。

部署上，可以把三个服务部署在一台服务器，也可以独立部署到不同物理节点
现在Cinder还是不够成熟，有几个明显的问题还没很好解决，一是支持的商业存储还不够多，而且还不支持FC SAN，另外单点故障隐患没解决，内部的schedule调度算法也太简单。另外由于它把各种存储整合进来又加了一层，管理倒是有办法了，但是效率肯定是有影响，性能肯定有损耗，但这也是没办法的事了。

Openstack通过两年多发展，变得越来越庞大。目前光存储就出现了三种：对象存储、镜像存储和块存储。这也是为了满足更多不同的需求，体现出开源项目灵活快速的特性。总的说来，当选择一套存储系统的时候，如果考虑到将来会被多个应用所共同使用，应该视为长期的决策。Openstack作为一个开放的系统，最主要是解决软硬件供应商锁定的问题，可以随时选择新的硬件供应商，将新的硬件和已有的硬件组成混合的集群，统一管理，当然也可以替换软件技术服务的提供商，不用动应用。这是开源本身的优势！

> 以上内容，摘自网络。
> 下面我重点来介绍cinder/ceap组件的安装使用。

# For Example
  Openstack系列第一篇自动化部署完成之后，此篇文章讲解企业级私有云后端云盘存储选型。默认allinone安装完成之后，系统自带一个基于lvm vloume的cinder存储。

### Dependencies
```
[root@openstack-controller ~]# cat /etc/redhat-release 
CentOS Linux release 7.2.1511 (Core) 
[root@openstack-compute ~]# cat /etc/redhat-release 
CentOS Linux release 7.2.1511 (Core) 
```

##  Gluster && LVM Vloume

### 1. Install glusterfs

`allinone安装的时候，已经自动安装了部分glusterfs包,并且需要通过rdo提供的源来安装glusterfs,`
`否则会有一些依赖冲突问题,导致无法安装成功。`

以下命令在所有准备glusterfs集群的服务器都执行：
```
$ rpm -qa | grep gluster*     

glusterfs-client-xlators-3.7.1-16.0.1.el7.centos.x86_64
glusterfs-3.7.1-16.0.1.el7.centos.x86_64
glusterfs-api-3.7.1-16.0.1.el7.centos.x86_64
glusterfs-libs-3.7.1-16.0.1.el7.centos.x86_64

$ yum install wget -y

$ yum install centos-release-gluster37         # ==> CentOS-Gluster-3.7.repo

$ rpm -qa *gluster*
glusterfs-client-xlators-3.7.1-16.0.1.el7.centos.x86_64
centos-release-gluster37-1.0-4.el7.centos.noarch
glusterfs-3.7.1-16.0.1.el7.centos.x86_64
glusterfs-api-3.7.1-16.0.1.el7.centos.x86_64
glusterfs-libs-3.7.1-16.0.1.el7.centos.x86_64

$ yum clean all

$ yum install glusterfs-server

$ service glusterd start / systemctl start glusterd.service
$ service glusterd status / systemctl status glusterd.service

$ systemctl enable glusterd.service
$ systemctl is-enabled glusterd.service

$ ps aux|grep gluster|wc -l
2
```

### 2. glusterfs cluster configuratioin
```
From "server1"
    gluster peer probe server2

From "server2"
    gluster peer probe server1

[root@openstack-controller ~]# gluster peer probe openstack-compute
peer probe: success. 
[root@openstack-controller ~]# gluster peer probe openstack-controller
peer probe: success. Probe on localhost not needed
```

### 3. glusterfs volume manager

你需要在两台主机执行如下命令，创建出glusterfs使用的本地磁盘目录地址。
```
mkdir /var/glusterfs/exp1 -p
```

你需要在glusterfs任意一台主机执行,如下命令,replica代表副本数量，可以理解为raid1,这个是glusterfs做为分布式文件系统，为cinder提供数据安全的有效保障：
```   
[root@openstack-controller ~]# gluster volume create cinder-volome01 replica 2 openstack-centos:/var/glusterfs/exp1 openstack-compute:/var/glusterfs/exp1 ＃创建带2份数据拷贝的卷
volume create: cinder-volome01: success: please start the volume to access data

[root@openstack-controller ~]# gluster volume start cinder-volome01 #启动卷

volume start: cinder-volome01: success

[root@openstack-controller ~]# gluster volume info

Volume Name: cinder-volume01
Type: Replicate
Volume ID: efe3c9a1-4bf9-4e45-a136-00ce8cd05d9f
Status: Started
Number of Bricks: 1 x 2 = 2
Transport-type: tcp
Bricks:
Brick1: openstack-centos:/var/glusterfs/exp1
Brick2: openstack-compute:/var/glusterfs/exp1
Options Reconfigured:
performance.readdir-ahead: on

[root@openstack-controller ~]# gluster
gluster> peer status
Number of Peers: 1

Hostname: openstack-compute
Uuid: bbcc8087-a584-4b7d-9631-cbd1e2e7151b
State: Peer in Cluster (Connected)

gluster> pool list
UUID                                    Hostname                State
bbcc8087-a584-4b7d-9631-cbd1e2e7151b    openstack-compute       Connected 
bc854ea5-8f67-4637-bf13-d2a46b109eb4    localhost               Connected 

gluster> volume info 
Volume Name: cinder-volume01
Type: Replicate
Volume ID: efe3c9a1-4bf9-4e45-a136-00ce8cd05d9f
Status: Started
Number of Bricks: 1 x 2 = 2
Transport-type: tcp
Bricks:
Brick1: openstack-controller:/var/glusterfs/exp1
Brick2: openstack-compute:/var/glusterfs/exp1
Options Reconfigured:
performance.readdir-ahead: on
```

### 4. Cinder plugin glusterfs and lvm volume
默认cinder自带lvm volume卷功能，其实cinder可以同时支持多种后端存储方式共存，下面介绍lvm,glusterfs共存的配置信息内容。

以下内容请在cinder安装节点执行：
```
[root@openstack-controller ~]# vim /etc/cinder/glusterfs_shares
  172.16.0.210:/cinder-volume01

[root@openstack-controller ~]# vim /etc/cinder/cinder.conf
  
enabled_backends=lvm,GlusterFS_Driver

[lvm]
iscsi_helper=lioadm
volume_group=cinder-volumes
iscsi_ip_address=172.16.0.210
volume_driver=cinder.volume.drivers.lvm.LVMVolumeDriver
volumes_dir=/var/lib/cinder/volumes
iscsi_protocol=iscsi
volume_backend_name=lvm

[GlusterFS_Driver]
volume_group=GlusterFS_Driver
volume_driver=cinder.volume.drivers.glusterfs.GlusterfsDriver
volume_backend_name=GlusterFS-Storage
glusterfs_shares_config = /etc/cinder/glusterfs_shares
glusterfs_mount_point_base = /var/lib/cinder/glusterfs

[root@openstack-controller ~]# mkdir /var/lib/cinder/glusterfs
[root@openstack-controller ~]# chown cinder:cinder /var/lib/cinder/glusterfs/

[root@openstack-controller ~]# systemctl restart openstack-cinder-volume.service

[root@openstack-controller ~(keystone_admin)]# cinder type-create GlusterFS
+--------------------------------------+-----------+-------------+-----------+
|                  ID                  |    Name   | Description | Is_Public |
+--------------------------------------+-----------+-------------+-----------+
| 4e236e8f-6592-45fc-a25a-b2f189f90439 | GlusterFS |      -      |    True   |
+--------------------------------------+-----------+-------------+-----------+

[root@openstack-controller ~(keystone_admin)]# source keystonerc_admin 

[root@openstack-controller ~(keystone_admin)]# cinder type-key GlusterFS set volume_backend_name=GlusterFS-Storage

[root@openstack-controller ~]# mount|grep glusterfs   #验证完成，说明glusterfs挂载成功
172.16.0.210:/cinder-volume01 on /var/lib/cinder/glusterfs/3e58f5c16b6f5406de3c8f9eb2623ad0 type fuse.glusterfs (rw,relatime,user_id=0,group_id=0,default_permissions,allow_other,max_read=131072)

[root@openstack-controller ~]# cat /etc/cinder/cinder.conf |grep glusterfs_shares
glusterfs_shares_config = /etc/cinder/glusterfs_shares
```

通过此命令可以查看openstack相关命令：
```
# systemctl |grep openstack|wc -l
35
```

cinder相关命令：
```
[root@openstack-controller ~(keystone_admin)]# cinder type-list
+--------------------------------------+-----------+-------------+-----------+
|                  ID                  |    Name   | Description | Is_Public |
+--------------------------------------+-----------+-------------+-----------+
| 038cb62b-6905-43bd-a4b2-632d171c6d3d |   iscsi   |      -      |    True   |
| 5e8fa387-cb4d-4dee-b0d2-9646f82c2008 | GlusterFS |      -      |    True   |
+--------------------------------------+-----------+-------------+-----------+

[root@openstack-controller ~(keystone_admin)]# cinder list
+--------------------------------------+-----------+-------------------+------+-------------+----------+-------------+
|                  ID                  |   Status  |        Name       | Size | Volume Type | Bootable | Attached to |
+--------------------------------------+-----------+-------------------+------+-------------+----------+-------------+
| 8d320989-f6f0-4c36-9ffc-9955e65d5390 | available | glusterfs-test-01 |  1   |  GlusterFS  |  false   |             |
| af4777b6-7ab1-4b00-a4d6-757f6c03bb7c | available | glusterfs-test-02 |  1   |  GlusterFS  |  false   |             |
| cd2b9a15-b3d8-4e4e-8fa0-9b27e6503144 | available |     test-iscsi    |  1   |    iscsi    |  false   |             |
+--------------------------------------+-----------+-------------------+------+-------------+----------+-------------+

[root@openstack-controller ~(keystone_admin)]# cinder service-list 
+------------------+-----------------------------------+------+---------+-------+----------------------------+-----------------+
|      Binary      |                Host               | Zone |  Status | State |         Updated_at         | Disabled Reason |
+------------------+-----------------------------------+------+---------+-------+----------------------------+-----------------+
|  cinder-backup   |          openstack-controller         | nova | enabled |   up  | 2016-05-26T19:37:18.000000 |        -        |
| cinder-scheduler |          openstack-controller         | nova | enabled |   up  | 2016-05-26T19:37:23.000000 |        -        |
|  cinder-volume   | openstack-controller@GlusterFS_Driver | nova | enabled |   up  | 2016-05-26T19:37:22.000000 |        -        |
|  cinder-volume   |        openstack-controller@lvm       | nova | enabled |   up  | 2016-05-26T19:37:16.000000 |        -        |
+------------------+-----------------------------------+------+---------+-------+----------------------------+-----------------+

-- volume - lvm
$ systemctl status openstack-cinder-volume.service

-- lvm 查看lv信息
$ lvdisplay 
```

## Dashboard
 登录到可视化页面，点击选择卷，创建云硬盘按钮，即可看到两种云硬盘类型，基于lvm创建iscsi类型和glusterfs的类型。最终效果如下图：
![](https://jikelab.github.io/tech-labs/screenshots/openstack-cinder-volume.png)

## NFS and Other Storage driver
  按照相关文档完成安装,最后修改cinder.conf文件，和cinder整合，举列如下:

For NFS:
```
yum install -y nfs-utils rpcbind

mkdir /data/nfs -p

cat /etc/exports
/data/nfs 127.16.0.0/24(rw,sync,no_root_squash)

/bin/systemctl start  rpcbind.service
/bin/systemctl status  rpcbind.service  
/bin/systemctl start nfs.service  
/bin/systemctl status nfs.service  
/bin/systemctl reload nfs.service 

$ sudo exportfs -rv 
exporting 127.16.0.0/24:/data/nfs

$ showmount -e  127.16.0.210
Export list for 127.16.0.210:
/data/nfs 127.16.0.0/24

cat /etc/cinder/nfs_shares
172.16.0.210:/data/nfs
```

Cinder Multiple Storage configuartion: 
```
$ vim /etc/cinder/cinder.conf
[DEFAULT]  
enabled_backends = lvm,GlusterFS_Driver,ibm,NFS-Driver
  
[lvm]  
volume_driver = cinder.volume.drivers.lvm.LVMVolumeDriver  
volume_backend_name=LVM  
volume_group = cinder-volumes  
iscsi_protocol = iscsi  
iscsi_helper = lioadm  
  
[GlusterFS_Driver]
volume_group=GlusterFS_Driver
volume_driver=cinder.volume.drivers.glusterfs.GlusterfsDriver
volume_backend_name=GlusterFS-Storage
glusterfs_shares_config = /etc/cinder/glusterfs_shares
glusterfs_mount_point_base = /var/lib/cinder/glusterfs 

[NFS-Driver]
volume_group=NFS-Driver
volume_driver=cinder.volume.drivers.nfs.NfsDriver
volume_backend_name=NFS-Storage
nfs_shares_config=/etc/cinder/nfs_shares
nfs_mount_point_base=$state_path/mnt

[ibm]  
volume_driver = cinder.volume.drivers.ibm.storwize_svc.StorwizeSVCDriver  
san_ip = 172.16.0.210  
san_login = www.itweet.cn  
san_password = 123456  
storwize_svc_volpool_name = vtt1  
storwize_svc_connection_protocol = iSCSI  
volume_backend_name=IBM  

$ cinder type-create NFS
$ cinder type-key NFS set volume_backend_name=NFS-Storage

$ systemctl restart openstack-cinder-volume

$ cinder service-list
```

## Openstack Glance
 openstack image
```
(openstack) help image 
Command "image" matches:
  image add project
  image create
  image delete
  image list
  image remove project
  image save
  image set
  image show

openstack image create "demo" --file /tmp/demo.img --disk-format qcow2 --container-format bare --public
```

## openstack ceph
[待续...](http://my.oschina.net/JerryBaby/blog/376858)

## Conclusion
 openstack多种后端存储，也是由于商业案例越来越多，导致需要多种存储系统满足不同的业务需求，从这一点看前途光明，的确解决很多现实问题。cinder发展为支持多后端存储方式是必然趋势，因为有很多企业级存储系统需要整合；而很多大厂对openstack不予余力的投入社区开发也促使他更快的成熟。swift，glance组件用来存储其他类型数据,解决块存储，对象存储,镜像存储问题，也是分而治之的道理。在玩openstack的时候就会发现，各种各样的组件，无意是增加了学习的复杂度，使用维护上面也非常复杂，进而导致安装非常复杂。安装根本就是不安，就只剩下装，装完这个装那个，这组件安装失败，另外组件起不来，说多了都是泪啊。不过redhat做了一个基于puppet自动化安装脚本，相对来说方便了不少；这样一键安装的缺点也显而易见，都不知道有多少组件，出问题怎么排查，所以还得对各个组件的功能和配置非常熟悉，才能对症下药解决问题。我写openstack实际使用系列文章，也是为了让想学习openstack的人更容易入门，后续openstack系列完结后，我会开源一个基于saltstack自动化部署openstack的软件开源到我的[Github](https://github.com/itweet)上面。欢迎关注。

## FAQ
 Centos6.x --> Centos7.x 多了些变化，慢慢熟悉
```
systemctl is-enabled iptables.service
systemctl is-enabled servicename.service #查询服务是否开机启动
systemctl enable *.service #开机运行服务
systemctl disable *.service #取消开机运行
systemctl start *.service #启动服务
systemctl stop *.service #停止服务
systemctl restart *.service #重启服务
systemctl reload *.service #重新加载服务配置文件
systemctl status *.service #查询服务运行状态
systemctl --failed #显示启动失败的服务
```

参考：http://gluster.readthedocs.io/en/latest/Quick-Start-Guide/Quickstart/
     http://www.gluster.org/community/documentation/index.php/GlusterFS_Cinder
     https://www.gluster.org/

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/