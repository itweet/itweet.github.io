---
title: Hbase Distibuted Install
date: 2015-07-16 17:13:42
description: HBase是一个分布式的、面向列的开源数据库，该技术来源于 Fay Chang 所撰写的Google论文“Bigtable：一个结构化数据的分布式存储系统”。
category: BigData
tags: hbase
---

HBase是一个分布式的、面向列的开源数据库，该技术来源于 Fay Chang 所撰写的Google论文“Bigtable：一个结构化数据的分布式存储系统”。就像Bigtable利用了Google文件系统（File System）所提供的分布式数据存储一样，HBase在Hadoop之上提供了类似于Bigtable的能力。HBase是Apache的Hadoop项目的子项目。HBase不同于一般的关系数据库，它是一个适合于非结构化数据存储的数据库。另一个不同的是HBase基于列的而不是基于行的模式。

# 1、hbase的分布模式

## 1.1 在server1上解压缩
	[root@server1 installpackage]# tar -zxvf hbase-0.98.6.1-hadoop2-bin.tar.gz -C /usr/local/
	[root@server1 local]# mv hbase-0.98.6.1-hadoop2 hbase-0.98.6.1

## 1.2 编辑文件conf/hbase-env.sh 修改内容
    export JAVA_HOME=/usr/local/jdk1.7.0_45
	export HBASE_MANAGES_ZK=false	[不适用hbase自己带的zk]

##1.3 编辑文件conf/hbase-site.xml
	[root@server1 conf]# vi hbase-site.xml 
	<property>
	  <name>hbase.rootdir</name>
	  <value>hdfs://server1:9000/user/hbase</value>
	</property>
	<property>
	  <name>hbase.cluster.distributed</name>
	  <value>true</value>
	</property>
	<property>
	  <name>hbase.zookeeper.quorum</name>
	  <value>server1,server2,server3</value>
	</property>	
	<property>  
	 <name>hbase.zookeeper.property.clientPort</name>  
	 <value>2181</value>  
	 <description>Property fromZooKeeper's config zoo.cfg.  
	 The port at which the clients willconnect.  
	 </description>  
	</property>
	<property>
	 <name>dfs.support.append</name>
	 <value>true</value>
	</property>  
	<property>
	 <name>hbase.tmp.dir</name>
	 <value>/tmp/hbase</value>
	 </property>
	<property>
	  <name>hbase.master</name>
	  <value>server1:60010</value>
	</property>	
	<property>
	 <name>hbase.regionserver.hlog.replication</name>
	 <value>2</value>
	</property>

多master配置
```
单台master的配置
hbase.master
master:60000
这是我们通常配置的，这样就定义了master是的ip和端口。
但是当我们需要配置多台master进行，我们只需要提供端口，因为选择真正的master的事情会又zookeeper去处理。
多台master的配置
                hbase.master.port
                60000
```

## 1.4 编辑文件conf/regionservers
	[root@server1 conf]# vi regionservers
    server3
    server4	

## 1.5 复制hbase到nodetest01、nodetest02节点
	[root@server1 local]# scp -rq hbase-0.98.6.1 server3:/usr/local/
	[root@server1 local]# scp -rq hbase-0.98.6.1 server4:/usr/local/

## 1.6 启动hbase之前，要检查hadoop的hdfs、zookeeper集群是否正常运行
    [root@server1 local]# hbase-0.98.6.1/bin/start-hbase.sh


## 1.7 检查
   执行jps命令，在server1上看到1个新的java进程，分别是HMaster
   查看http://server1:60010,hbase-1.1.2 版本修改默认端口16010 
   地址：http://server1:16010/master-status

## 1.7 Habse CLI
- 创建一张最简单的表
  hbase(main):004:0> create 't1','fm1'【表名，列族名】

- lise table
  hbase(main):005:0> list

```
	$ hbase shell
	15/03/15 15:58:57 INFO Configuration.deprecation: hadoop.native.lib is deprecated. Instead, use io.native.lib.availablee
	HBase Shell; enter 'help<RETURN>' for list of supported commands.
	Type "exit<RETURN>" to leave the HBase Shell
	Version 0.98.6-cdh5.2.0, rUnknown, Sat Oct 11 15:15:15 PDT 2014

	hbase(main):001:0> list
	TABLE                                                                                                                                  
	aaa                                                                                                                                    
	test                                                                                                                                   
	2 row(s) in 3.2560 seconds

	=> ["aaa", "test"]
	hbase(main):002:0> create 'test1', 'lf', 'sf'
	0 row(s) in 1.0330 seconds

	=> Hbase::Table - test1
	hbase(main):003:0> put 'test1', 'user1|ts1', 'sf:c1', 'sku'
	0 row(s) in 0.2010 seconds

	hbase(main):004:0> put 'test1', 'user1|ts2', 'sf:c1', 'sku188'
	0 row(s) in 0.0320 seconds

	hbase(main):005:0> put 'test1', 'user1|ts3', 'sf:s1', 'sku123'
	0 row(s) in 0.0290 seconds

	hbase(main):006:0> scan 'test1'
	ROW                                COLUMN+CELL                                                                                         
	 user1|ts1                         column=sf:c1, timestamp=1426406452681, value=sku                                                   
	 user1|ts2                         column=sf:c1, timestamp=1426406477190, value=sku188                                                
	 user1|ts3                         column=sf:s1, timestamp=1426406482547, value=sku123                                                
	3 row(s) in 0.0810 seconds
	hbase(main):006:0>!q
```

参考资料：http://hbase.apache.org/
		  http://abloz.com/hbase/book.html


原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/