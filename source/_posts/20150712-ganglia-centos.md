---
title: ganglia-centos
date: 2015-07-12 16:59:26
description: Ganglia是UC Berkeley发起的一个开源集群监视项目，设计用于测量数以千计的节点。
category: BigData
tags: monitor
---

# ganglia 
   Ganglia是UC Berkeley发起的一个开源集群监视项目，设计用于测量数以千计的节点。
   Ganglia的核心包含gmond、gmetad以及一个Web前端。主要是用来监控系统性能，如：
   cpu 、mem、硬盘利用率， I/O负载、网络流量情况等，通过曲线很容易见到每个节点
   的工作状态，对合理调整、分配系统资源，提高系统整体性能起到重要作用。
   ![](http://g.hiphotos.baidu.com/baike/c0%3Dbaike80%2C5%2C5%2C80%2C26/sign=565a7df0720e0cf3b4fa46a96b2f997a/d058ccbf6c81800adfd059ecb13533fa828b471f.jpg)

# Centos安装Ganglia

## 1、安装ganglia
```
		[root@itr-mastertest01 local]#  rpm -Uvh  http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
		[root@itr-mastertest02 local]#  rpm -Uvh  http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
		[root@itr-nodetest01 local]#  rpm -Uvh  http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
		[root@itr-nodetest02 local]#  rpm -Uvh  http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
		[root@itr-mastertest01 local]# yum install rrdtool ganglia-gmetad ganglia-gmond ganglia-web httpd php -y
		[root@itr-mastertest01 local]# rpm -e ganglia-web-3.1.7-6.el6.x86_64		这里卸载web我们下面自己安装一个版本
		[root@itr-mastertest01 ~]# rpm -qa | grep ganglia 		验证rmp安装
			ganglia-3.1.7-6.el6.x86_64
			ganglia-gmetad-3.1.7-6.el6.x86_64
			ganglia-gmond-3.1.7-6.el6.x86_64

		[root@itr-mastertest02 local]# yum search ganglia-gmond
	  	[root@itr-mastertest02 local]# yum install ganglia-gmond -y
	  	[root@itr-mastertest02 ~]# rpm -qa | grep ganglia 		验证rmp安装
			ganglia-gmond-3.1.7-6.el6.x86_64
			ganglia-3.1.7-6.el6.x86_64

	  	[root@itr-nodetest01 local]# yum install ganglia-gmond -y

	  	[root@itr-nodetest02 local]# yum install ganglia-gmond -y
```

## 2、编辑配置文件
```
		[root@itr-mastertest01 ~]# vim /etc/ganglia/gmond.conf
			cluster {
			  name = "cluster1"
			  owner = "unspecified"
			  latlong = "unspecified"
			  url = "unspecified"
			}
			/* Feel free to specify as many udp_send_channels as you like.  Gmond
			   used to only support having a single channel */
			udp_send_channel {
			 /* mcast_join = 239.2.11.71*/
			  host = 192.168.2.200
			  port = 8649
			  ttl = 1
			}

			/* You can specify as many udp_recv_channels as you like as well. */
			udp_recv_channel {
			 /*mcast_join = 239.2.11.71*/
			  port = 8649
			 /* bind = 239.2.11.71*/
			}

		[root@itr-mastertest01 ~]# vim /etc/ganglia/gmetad.conf
			data_source "cluster1" 10 192.168.2.200 192.168.2.201 192.168.2.202 192.168.2.203

		[root@itr-mastertest01 ~]# scp /etc/ganglia/gmond.conf itr-mastertest02:/etc/ganglia/
	  	[root@itr-mastertest01 ~]# scp /etc/ganglia/gmond.conf itr-nodetest01:/etc/ganglia/
	  	[root@itr-mastertest01 ~]# scp /etc/ganglia/gmond.conf itr-nodetest02:/etc/ganglia/
```

## 3、设置开机自动启动
```		
		[root@itr-mastertest01 local]# chkconfig --levels 235 gmond on
	  	[root@itr-mastertest01 local]# chkconfig --list gmond 
	  	[root@itr-mastertest01 local]# chkconfig --levels 235 gmetad on
	  	[root@itr-mastertest01 local]# chkconfig --levels 235 httpd on

	  	[root@itr-mastertest02 local]# chkconfig --levels 235 gmond on
	  	[root@itr-nodetest01 local]# chkconfig --levels 235 gmond on
	  	[root@itr-nodetest02 local]# chkconfig --levels 235 gmond on
```

## 4、启动
```		
		[root@itr-mastertest01 local]# service gmond start
		[root@itr-mastertest01 local]# service gmetad start
		[root@itr-mastertest01 local]# service httpd start
		[root@itr-mastertest01 local]# service httpd start    

		[root@itr-mastertest01 ~]# ps aux | grep apache*  		验证apache
		root      1736  0.0  0.1 105488   912 pts/0    S+   09:21   0:00 grep apache*
		[root@itr-mastertest01 ~]# ps aux | grep ganglia* 		验证ganglia
		ganglia   1191  0.1  0.2 228468  1932 ?        Sl   08:48   0:03 /usr/sbin/gmetad
		ganglia   1515  0.0  0.2 147736  2396 ?        Ss   08:48   0:00 /usr/sbin/gmond
		root      1741  0.0  0.1 105488   912 pts/0    S+   09:22   0:00 grep ganglia*

		[root@itr-mastertest02 ~]#  ps aux | grep ganglia* 		其他节点验证
		ganglia   1622  0.0  0.2 146792  1836 ?        Ss   08:49   0:00 /usr/sbin/gmond
		root      1825  0.0  0.1 105488   908 pts/0    S+   09:24   0:00 grep ganglia*
```

## 5、安装ganglia-web界面
```	
		[root@itr-mastertest01 local]# cd installpackage/
		[root@itr-mastertest01 installpackage]# tar -zxvf ganglia-web-3.5.12.tar.gz -C ../
		[root@itr-mastertest01 local]# cd ganglia-web-3.5.12/
		[root@itr-mastertest01 ganglia-web-3.5.12]# vim Makefile 
			GDESTDIR = /var/www/html/ganglia
			APACHE_USER = apahce              

		[root@itr-mastertest01 ganglia-web-3.5.12]# vi /etc/httpd/conf/httpd.conf
			User apache 							上面的用户和这样里对接
			Group apache

		[root@itr-mastertest01 ganglia-web-3.5.12]# make install
		[root@itr-mastertest01 ganglia-web-3.5.12]# LANG=en
		[root@itr-mastertest01 ganglia-web-3.5.12]#  service httpd status
		httpd (pid  5810) 正在运行...
		[root@itr-mastertest01 ganglia-web-3.5.12]# service gmetad status
		gmetad (pid 5844) 正在运行...
		[root@itr-mastertest01 ganglia-web-3.5.12]# service gmond status
		gmond (pid 5874) 正在运行...

		[root@itr-mastertest01 html]# chmod -R 777 /var/www/html/ganglia 		有时候web页面访问apache目录权限不够

		[root@itr-mastertest01 ganglia]# setenforce 0 							必须关闭selinux，否则web页面访问提示权限不够
		[root@itr-mastertest01 ganglia]#  vi /etc/selinux/
		[root@itr-mastertest01 ganglia]#  vi /etc/selinux/config 
		SELINUX=disabled

		[root@itr-mastertest01 ganglia]# scp /etc/selinux/config itr-mastertest02:/etc/selinux/
		[root@itr-mastertest01 ganglia]# scp /etc/selinux/config itr-nodetest02:/etc/selinux/  
		[root@itr-mastertest01 ganglia]# scp /etc/selinux/config itr-nodetest01:/etc/selinux/
```

## 6、配置hadoop文件发送信息给ganglia
```		
		[root@itr-mastertest01 hadoop]# vi /usr/local/hadoop-2.4.0/etc/hadoop/hadoop-metrics2.properties 
			#By AndrewHsu 2014-12-31
			#NameNode
			*.sink.ganglia.class=org.apache.hadoop.metrics2.sink.ganglia.GangliaSink31
			*.period=10
			namenode.sink.ganglia.servers=192.168.2.200:8649

			#DataNode
			*.sink.ganglia.class=org.apache.hadoop.metrics2.sink.ganglia.GangliaSink31
			*.period=10
			datanode.sink.ganglia.servers=192.168.2.200:8649

			#SecondaryNameNode
			*.sink.ganglia.class=org.apache.hadoop.metrics2.sink.ganglia.GangliaSink31
			*.period=10
			secondarynamenode.sink.ganglia.servers=192.168.2.200:8649

			#YARN
			#ResourceManager
			*.sink.ganglia.class=org.apache.hadoop.metrics2.sink.ganglia.GangliaSink31
			*.period=10
			resourcemanager.sink.ganglia.servers=192.168.2.200:8649
			maptask.sink.ganglia.servers=192.168.2.200:8649 
			reducetask.sink.ganglia.servers=192.168.2.200:8649

			#NodeManager
			*.sink.ganglia.class=org.apache.hadoop.metrics2.sink.ganglia.GangliaSink31
			*.period=10
			nodemanager.sink.ganglia.servers=192.168.2.200:8649
			maptask.sink.ganglia.servers=192.168.2.200:8649 
			reducetask.sink.ganglia.servers=192.168.2.200:8649

			[root@itr-mastertest01 local]# groupadd supergroup 			为制作nfs3挂载hdfs目录到本地而增加的组
			[root@itr-mastertest01 local]# cat /etc/group | grep supergroup
			supergroup:x:501:

			#scp conf to all node
			[root@itr-mastertest01 ~]# scp /usr/local/hadoop-2.4.0/etc/hadoop/hadoop-metrics2.properties itr-mastertest02:/usr/local/hadoop-2.4.0/etc/hadoop/

			[root@itr-mastertest01 ~]# scp /usr/local/hadoop-2.4.0/etc/hadoop/hadoop-metrics2.properties itr-nodetest01:/usr/local/hadoop-2.4.0/etc/hadoop/

			[root@itr-mastertest01 ~]# scp /usr/local/hadoop-2.4.0/etc/hadoop/hadoop-metrics2.properties itr-nodetest02:/usr/local/hadoop-2.4.0/etc/hadoop/
```

## 7、配置hbase发送信息给ganglia
```	
		[root@itr-mastertest01 conf]# vi /usr/local/hbase-0.98.6.1/conf/hadoop-metrics2-hbase.properties 
		#By AndrewHsu 2-14-12-31
		#HBase
		#Master Server
		*.sink.ganglia.class=org.apache.hadoop.metrics2.sink.ganglia.GangliaSink31
		*.sink.ganglia.period=10
		hbase.sink.ganglia.period=10
		hbase.sink.ganglia.servers=192.168.2.200:8649

		#Region Server
		*.sink.ganglia.class=org.apache.hadoop.metrics2.sink.ganglia.GangliaSink31
		*.sink.ganglia.period=10
		hbase.sink.ganglia.period=10
		hbase.sink.ganglia.servers=192.168.2.200:8649

		#scp conf to all node
		[root@itr-mastertest01 ~]# scp /usr/local/hbase-0.98.6.1/conf/hadoop-metrics2-hbase.properties itr-nodetest01:/usr/local/hbase-0.98.6.1/conf/
		[root@itr-mastertest01 ~]# scp /usr/local/hbase-0.98.6.1/conf/hadoop-metrics2-hbase.properties itr-nodetest02:/usr/local/hbase-0.98.6.1/conf/
```

## 8、webui界面
 > http://itr-mastertest01/ganglia/

