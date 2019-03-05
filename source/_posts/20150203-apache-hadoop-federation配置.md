---
title: apache hadoop federation配置
date: 2015-02-03 17:06:17
description: HDFS Federation的配置和使用，可以让HDFS的访问支持虚拟视图FS。
category: BigData
tags: hadoop
---
# 节点分配
 - ns1的namenode：server01
 - ns2的namenode：server02
 - datanode：server03,server04

## 3.1 配置文件(hadoop-env.sh、core-site.xml、hdfs-site.xml、yarn-site.xml、mapred-site.xml、slaves)

### 3.1.1 hadoop-env.sh
```
	export JAVA_HOME=/usr/local/jdk1.7.0_45
```

### 3.1.2 core-site.xml

	<property>
	<name>fs.defaultFS</name>
	<value>hdfs://ns1</value>
	</property>

	<property>
	<name>hadoop.tmp.dir</name>
	<value>/usr/local/hadoop-2.4.0/tmp</value>
	</property>

	<property>
	<name>fs.viewfs.mounttable.default.link./ns0</name>
	<value>hdfs://server01:9000/</value>
	</property>
	<property>
	<name>fs.viewfs.mounttable.default.link./ns1</name>
	<value>hdfs://server02:9000</value>
	</property>

### 3.1.3 hdfs-site.xml

	<property>
	<name>dfs.replication</name>
	<value>2</value>
	</property>

	<property>
	<name>dfs.nameservices</name>
	<value>ns1,ns2</value>
	</property>

	<property>
	<name>dfs.ha.namenodes.ns1</name>
	<value>nn1</value>
	</property>

	<property>
	<name>dfs.namenode.rpc-address.ns1.nn1</name>
	<value>server01:9000</value>
	</property>

	<property>
	<name>dfs.namenode.http-address.ns1.nn1</name>
	<value>server01:50070</value>
	</property>


	<property>
	<name>dfs.ha.namenodes.ns2</name>
	<value>nn2</value>
	</property>

	<property>
	<name>dfs.namenode.rpc-address.ns2.nn2</name>
	<value>server02:9000</value>
	</property>

	<property>
	<name>dfs.namenode.http-address.ns2.nn2</name>
	<value>server02:50070</value>
	</property>


### 3.1.4 slaves
```
	server03
	server04
```

### 3.1.5 scp
- 复制配置信息到其他节点

### 3.2 格式化namenode、启动namenode

- 在server01上执行hadoop/bin/hdfs namenode -format -clusterId clusterid1
- 在server01上执行hadoop/sbin/hadoop-daemon.sh start namenode
	 
- 在server02上执行hadoop/bin/hdfs namenode -format -clusterId clusterid1
	 	【clusterId的值与server01上执行的clusterId的值完全相同。如果不同，就属于同一个federation】
- 在server02上执行hadoop/sbin/hadoop-daemon.sh start namenode

### 3.3 启动datanode
 
- 在server01上分别执行
	hadoop/sbin/hadoop-daemons.sh start datanode


### 3.5 启动resourcemanager和nodemanager

- 在server01上执行 
	hadoop/sbin/start-yarn.sh start resourcemanager

### 3.6 验证：

 - viewFS是跨隶属于同一个federation的多个hdfs的文件管理系统。

 - 使用server01:50070/dfsclusterhealth.jsp查看集群情况
 - 使用```hadoop/bin/hdfs dfs -ls viewfs:///```统一查看联邦中的数据内容


原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/