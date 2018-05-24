---
title: openstack-issue
date: 2016-06-16 18:09:51
category: Cloud
tags: openstack
---
openstack 生产环境问题纪录。

# 1、horizon “router_gateway  DOWN”

`horizon 页面路由显示信息 “router_gateway   DOWN”，路由－》接口－》外部网关－》状态：停止 ｜ 默认：创建`

- 初步认定是openstack的bug，虽然是down状态但是不影响使用

- 排查过程
 + 1.1 页面看到外部网关“停止状态”的固定IP地址，通过如下命令过滤出来，最后获取状态看到“down”
[root@controller ~(keystone_admin)]# `neutron port-list|grep 192.168.2.100`
| 857833bb-ae82-40c2-a6db-498b71660f17 |      | fa:16:3e:20:b8:b2 | {"subnet_id": "e380ee29-c00f-485b-9ab2-7da3466cb9e1", "ip_address": "192.168.2.100"} |

[root@controller ~(keystone_admin)]# `neutron port-show`857833bb-ae82-40c2-a6db-498b71660f17|grep status
| status                | `DOWN`                                        

[root@controller ~(keystone_admin)]# `neutron router-show router|grep status`
| status                | ACTIVE                                               

[root@controller ~(keystone_admin)]#  `neutron help | grep route`  
  l3-agent-list-hosting-router      List L3 agents hosting a router.
  l3-agent-router-add               Add a router to a L3 agent.
  l3-agent-router-remove            Remove a router from a L3 agent.
  net-gateway-connect               Add an internal network interface to a router.
  router-create                     Create a router for a given tenant.
  router-delete                     Delete a given router.
  router-gateway-clear              Remove an external network gateway from a router.
  router-gateway-set                Set the external network gateway for a router.
  router-interface-add              Add an internal network interface to a router.
  router-interface-delete           Remove an internal network interface from a router.
  router-list                       List routers that belong to a given tenant.
  router-list-on-l3-agent           List the routers on a L3 agent.
  router-port-list                  List ports that belong to a given tenant, with specified router.
  router-show                       Show information of a given router.
  router-update                     Update router's information.

# 2、修改主机配置大小，导致数据迁移失败。
 openstack 故障：Authentication required 500，页面看到是调整大小的时候报错。
 
 修改主机大小，会新建立一个主机，把旧的数据迁移到新的主机，在完成最后的合并工作，但是由于物理机压力太大，导致迁移失败。后天看到有两个虚拟机，处于关闭状态。

- 手动重启主机实例，去前台的vnc客户端看到，主机启动了，没有任何问题，正常可以使用，就前台有个错误状态让人不爽。
```
[root@openstack-controller ~]# virsh list --all 
 Id    Name                           State
----------------------------------------------------
 136   instance-0000003a              running
 -     instance-0000003c              shut off
 -     instance-00000079              shut off

[root@controller ~]# virsh start instance-0000003c 
Domain instance-0000003c started

[root@openstack-controller ~]# virsh list --all              
 Id    Name                           State
----------------------------------------------------
 136   instance-0000003a              running
 137   instance-0000003c              running
 -     instance-00000079              shut off
```

- 虽然云主机正常使用，但是前台无法在管理到此云主机,想办法把数据和服务先迁移走。然后单独修改数据库状态，使它正常接收管理，恢复正常使用。

# 3、虚拟机一直处于删除状态－前台卡死－发现前后端数据不一致
  检测发现，虚拟机一直处于删除状态，无法释放。

通过source keystone_admin，进入管理员权限，查看虚拟机状态，发现处于deleteing状态。
```
[root@controller ~(keystone_admin)]# nova list|grep deleting
| c6eb16d4-d607-4c98-b329-9defc4ba7586 | RedHadoop03          | ACTIVE | deleting   | Running     | private=172.16.1.242                |
| 227a1b8b-93cf-4e55-af73-db0d60e80a69 | RedHadoop04          | ACTIVE | deleting   | Running     | private=172.16.1.243                |
```

> 解决方法，首先reset-state这台虚拟机，然后执行`nova delte 虚拟机ID`进行删除。

* reset 虚拟机
```
[root@controller nova(keystone_admin)]# nova reset-state --active c6eb16d4-d607-4c98-b329-9defc4ba7586
Reset state for server c6eb16d4-d607-4c98-b329-9defc4ba7586 succeeded; new state is active
```

* 查看虚拟机状态
```
[root@controller nova(keystone_admin)]# nova show c6eb16d4-d607-4c98-b329-9defc4ba7586
+--------------------------------------+----------------------------------------------------------+
| Property                             | Value                                                    |
+--------------------------------------+----------------------------------------------------------+
| OS-DCF:diskConfig                    | MANUAL                                                   |
| OS-EXT-AZ:availability_zone          | nova                                                     |
| OS-EXT-SRV-ATTR:host                 | compute1                                                 |
| OS-EXT-SRV-ATTR:hypervisor_hostname  | compute1                                                 |
| OS-EXT-SRV-ATTR:instance_name        | instance-000001ea                                        |
| OS-EXT-STS:power_state               | 1                                                        |
| OS-EXT-STS:task_state                | -                                                        |
| OS-EXT-STS:vm_state                  | active                                                   |
| OS-SRV-USG:launched_at               | 2016-07-25T07:51:36.000000                               |
| OS-SRV-USG:terminated_at             | -                                                        |
| accessIPv4                           |                                                          |
| accessIPv6                           |                                                          |
| config_drive                         |                                                          |
| created                              | 2016-07-25T07:50:57Z                                     |
| flavor                               | m1.xlarge (5)                                            |
| hostId                               | 02a55d5ba7a2ec4a8af2d59c8267befc2378810113c2e6532fe0417a |
| id                                   | c6eb16d4-d607-4c98-b329-9defc4ba7586                     |
| image                                | demo (a304281c-7524-444e-ab39-29a9658b8944)              |
| key_name                             | jin                                                      |
| metadata                             | {}                                                       |
| name                                 | RedHadoop03                                              |
| os-extended-volumes:volumes_attached | []                                                       |
| progress                             | 0                                                        |
| status                               | ACTIVE                                                   |
| tenant_id                            | d62eac96a5294336b1f508b5757088f6                         |
| updated                              | 2016-07-26T08:55:54Z                                     |
| user_id                              | b113bbc4934e4a71882206e516f2931e                         |
+--------------------------------------+----------------------------------------------------------+
```

* 删除虚拟机
```
[root@controller nova(keystone_admin)]# nova delete c6eb16d4-d607-4c98-b329-9defc4ba7586
Request to delete server c6eb16d4-d607-4c98-b329-9defc4ba7586 has been accepted.
```

* 可通过`virsh list --all`命令查看是否删除干净，在配合`nova list`命令排查，查看是否还有一直处于删除状态的云主机。

# 3. 云硬盘error、error deleting、deleting状态
起因是因为，机房断电了，重启之后，openstack集群其中有一台服务器启动后，网线未成功连接，导致此主机IP无法连接；而在这个时候，我并没有发现有一台服务器未加入集群，删除了一个快底层未glusterfs集群的云硬盘，接下来就出现了一直处于删除状态！

通过cinder命令查看云硬盘状态：
```
[root@openstack-controller ~(keystone_openstack-cloud)]# cinder list
+--------------------------------------+----------------+----------------------------+------+-------------+----------+--------------------------------------+
|                  ID                  |     Status     |            Name            | Size | Volume Type | Bootable |             Attached to              |
+--------------------------------------+----------------+----------------------------+------+-------------+----------+--------------------------------------+
| 11cb3510-533e-4db4-9999-ff2c7b72695a |     error      |   x86-build-glusterfs-1    | 100  |  GlusterFS  |   true   | cbc4f7ab-c167-4478-9982-64909f55e52e |
| 3d07bbcd-c648-4bda-a0ee-96b9877b7a4b |     in-use     | gitlib-server-glusterfs-1  | 1000 |  GlusterFS  |  false   | b232560d-af7a-47f0-80c6-f708b9bda45e |
| 751b6804-ce57-48d1-bbce-c0b9d4d10a97 | error_deleting | rancher-server-glusterfs-1 |  20  |  GlusterFS  |  false   |                                      |
+--------------------------------------+----------------+----------------------------+------+-------------+----------+--------------------------------------+
```

登录数据库，`user cinder;` 进入库，查看volumes表信息：
```
MariaDB [cinder]> select deleted,status,deleted_at from volumes where id='751b6804-ce57-48d1-bbce-c0b9d4d10a97';
+---------+----------------+------------+
| deleted | status         | deleted_at |
+---------+----------------+------------+
|       0 | error_deleting | NULL       |
+---------+----------------+------------+
1 row in set (0.01 sec)
```

很多原因可能导致volume 进入error或者error_deleting状态，此时无法再执行delete操作。这种情况大体分为两类：

 * 1.当执行cinder delete时，cinder连接不到glusterfs 云硬盘服务器，导致删除失败。
 * 2.当执行cinder delete时，cinder连接不到数据库，此时由于没有事务同步，导致ceph已经删除对应的image，但没有同步状态到数据库中，此时volume可能处于available或者deleting状态，如果再次执行delete操作，显然cinder已经找不到对应的image，所以会抛出错误异常，此时cinder volume会把它设为error_deleting状态，并且无法通过reset-state删除。

尝试执行如下命令：
```
  $ cinder reset-state volume_id
  $ cinder delete volume_id
```

如果还是失败
```
[root@openstack-controller ~(keystone_openstack-cloud)]# cinder delete 751b6804-ce57-48d1-bbce-c0b9d4d10a97
Delete for volume 751b6804-ce57-48d1-bbce-c0b9d4d10a97 failed: Invalid volume: Volume status must be available or error or error_restoring or error_extending and must not be migrating, attached, belong to a consistency group or have snapshots. (HTTP 400) (Request-ID: req-1769e1bc-b0bc-4688-bff7-fc88e8785cb0)
ERROR: Unable to delete any of the specified volumes.
```

此故障无法通过cinder命令删除，只能修改数据库状态,标识其为已删除状态（通常不直接删除记录）:
```
mysql -uroot -pxxx

MariaDB [cinder]> use cinder;

MariaDB [cinder]> update volumes set deleted=1 where id = "751b6804-ce57-48d1-bbce-c0b9d4d10a97";

MariaDB [cinder]> update volumes set status='deleted' where id = "751b6804-ce57-48d1-bbce-c0b9d4d10a97";

MariaDB [cinder]> update volumes set deleted_at='now()' where id = "751b6804-ce57-48d1-bbce-c0b9d4d10a97";

MariaDB [cinder]> select deleted,status,deleted_at from volumes where id='751b6804-ce57-48d1-bbce-c0b9d4d10a97';
+---------+---------+---------------------+
| deleted | status  | deleted_at          |
+---------+---------+---------------------+
|       1 | deleted | 0000-00-00 00:00:00 |
+---------+---------+---------------------+
1 row in set (0.00 sec)
```
如上，只需要修改cinder数据库的volumes表，修改deleted字段为1(整型的1，不是字符串)，status字段修改为"deleted"，deleted_at可修改为"now()",也可以不修改。

再次查看cinder卷信息，已经没有状态为删除错误的信息：
```
[root@openstack-controller ~(keystone_openstack-cloud)]# cinder list|grep error_deleting|wc -l
0
```

最后，删除对应的glusterfs目录下的volume信息：
```
[root@openstack-controller (keystone_openstack-cloud)]# ls /var/lib/cinder/glusterfs/c44e08da624e18a5d328451413fd4c27
volume-11cb3510-533e-4db4-9999-ff2c7b72695a  volume-3d07bbcd-c648-4bda-a0ee-96b9877b7a4b  volume-751b6804-ce57-48d1-bbce-c0b9d4d10a97

[root@openstack-controller (keystone_openstack-cloud)]# du -s -h /var/lib/cinder/glusterfs/c44e08da624e18a5d328451413fd4c27/volume-751b6804-ce57-48d1-bbce-c0b9d4d10a97 
527M  volume-751b6804-ce57-48d1-bbce-c0b9d4d10a97

[root@openstack-controller (keystone_openstack-cloud)]# rm -f /lib/cinder/glusterfs/c44e08da624e18a5d328451413fd4c27/volume-751b6804-ce57-48d1-bbce-c0b9d4d10a97
```
如此这般，才算解决问题呀！复杂。。。

# 4.openstack cinder volume error
事情是这样发生的，我们机房需要断电安装空调，我们关闭openstack所有云主机后，关闭操作系统，重启之后发现，云硬盘都处于error状态，但是不影响正常使用，就是dashboard看着不舒服.
```
# cinder list|grep error
| 11cb3510-533e-4db4-9999-ff2c7b72695a | error  |   x86-build-glusterfs-1   | 100  |  GlusterFS  |   true   | cbc4f7ab-c167-4478-9982-64909f55e52e |
| 3d07bbcd-c648-4bda-a0ee-96b9877b7a4b | error  | gitlib-server-glusterfs-1 | 1000 |  GlusterFS  |  false   | b232560d-af7a-47f0-80c6-f708b9bda45e |
```


原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/