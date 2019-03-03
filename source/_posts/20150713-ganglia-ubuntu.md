---
title: ganglia-ubuntu
date: 2015-07-13 17:00:54
description: Ganglia是UC Berkeley发起的一个开源集群监视项目，设计用于测量数以千计的节点。
category: Monitoring
tags: monitor
---

# ganglia 
   Ganglia是UC Berkeley发起的一个开源集群监视项目，设计用于测量数以千计的节点。
   Ganglia的核心包含gmond、gmetad以及一个Web前端。主要是用来监控系统性能，如：
   cpu 、mem、硬盘利用率， I/O负载、网络流量情况等，通过曲线很容易见到每个节点
   的工作状态，对合理调整、分配系统资源，提高系统整体性能起到重要作用。

# Install and config Ganglia on CDH5
## Install

### Server node

####　1. install packages
```
	sudo apt-get install ganglia-monitor ganglia-webfrontend gmetad
```

#### 2. edit /etc/ganglia/gmond.conf
```
	sample gmond.conf setting:
	cluster {
	  name = "CDH5"
	  owner = "unspecified"
	  latlong = "unspecified"
	  url = "unspecified"
	}

	udp_send_channel {
	/*  mcast_join = xxx */
	  host = xxx.xxx.xxx.1 /* your ganglia server ip */
	  port = 8649
	  ttl = 1
	}

	udp_recv_channel {
	/*  mcast_join = xxx */
	  port = 8649
	/*  bind = xxx */
	}
```
	
#### 3. scp /etc/ganglia/gmond.conf to all the other nodes

#### 4. edit /etc/ganglia/gmetad.conf
	
	sample gmond.conf setting:
	data_source "CDH5" xxx.xxx.xxx.1 xxx.xxx.xxx.2 xxx.xxx.xxx.3 ...


### Other nodes

### 1. install ganglia monitor
```	
	sudo apt-get install ganglia-monitor
```

### 2. copy gmond.conf from server node to /etc/ganglia
```	
	sudo mv gmond.conf /etc/ganglia/
```

### 3. restart ganglia monitor service
```	
	sudo service ganglia-monitor restart


	Config: CDH5 components Hadoop Metrics2 setting
	hadoop-metrics2.properties

	HDFS
	NameNode
	*.sink.ganglia.class=org.apache.hadoop.metrics2.sink.ganglia.GangliaSink31
	*.period=10
	namenode.sink.ganglia.servers=10.10.114.120:8649

	DataNode
	*.sink.ganglia.class=org.apache.hadoop.metrics2.sink.ganglia.GangliaSink31
	*.period=10
	datanode.sink.ganglia.servers=10.10.114.120:8649

	SecondaryNameNode
	*.sink.ganglia.class=org.apache.hadoop.metrics2.sink.ganglia.GangliaSink31
	*.period=10
	secondarynamenode.sink.ganglia.servers=10.10.114.120:8649

	YARN
	ResourceManager
	*.sink.ganglia.class=org.apache.hadoop.metrics2.sink.ganglia.GangliaSink31
	*.period=10
	resourcemanager.sink.ganglia.servers=10.10.114.120:8649
	maptask.sink.ganglia.servers=10.10.114.120:8649 
	reducetask.sink.ganglia.servers=10.10.114.120:8649

	NodeManager
	*.sink.ganglia.class=org.apache.hadoop.metrics2.sink.ganglia.GangliaSink31
	*.period=10
	nodemanager.sink.ganglia.servers=10.10.114.120:8649
	maptask.sink.ganglia.servers=10.10.114.120:8649 
	reducetask.sink.ganglia.servers=10.10.114.120:8649

	HBase
	Master Server
	*.sink.ganglia.class=org.apache.hadoop.metrics2.sink.ganglia.GangliaSink31
	*.sink.ganglia.period=10
	hbase.sink.ganglia.period=10
	hbase.sink.ganglia.servers=10.10.114.120:8649

	Region Server
	*.sink.ganglia.class=org.apache.hadoop.metrics2.sink.ganglia.GangliaSink31
	*.sink.ganglia.period=10
	hbase.sink.ganglia.period=10
	hbase.sink.ganglia.servers=10.10.114.120:8649

	*(there are too many metrics generated from RegionServer, each region of all of tables generates some metrics... be careful if you turn on the ganglia hadoop metrics2 sink on HBase RegionServer)
```

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/