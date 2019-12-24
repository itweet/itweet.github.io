---
title: zookeeper cluster deploy
date: 2015-01-01 18:51:29
description: ZooKeeper是一个分布式的，开放源码的分布式应用程序协调服务，它包含一个简单的原语集，分布式应用程序可以基于它实现同步服务，配置维护和命名服务等。
category: BigData
tags: zookeeper
---
>ZooKeeper是一个分布式的，开放源码的分布式应用程序协调服务，它包含一个简单的原
>语集，分布式应用程序可以基于它实现同步服务，配置维护和命名服务等。Zookeeper是
>hadoop的一个子项目，其发展历程无需赘述。在分布式应用中，由于工程师不能很好地使
>用锁机制，以及基于消息的协调机制不适合在某些应用中使用，因此需要有一种可靠的、
>可扩展的、分布式的、可配置的协调机制来统一系统的状态。Zookeeper的目的就在
>于此。

# zk的特点
- 一致性：无论客户端连接到哪一个服务器，客户端将看到相同的 ZooKeeper 视图。

- 可靠性：一旦一个更新操作被应用，那么在客户端再次更新它之前，它的值将不会
  改变。

- 实时性：Zookeeper只保证最终一致性, 但是实时的一致性可以由客户端调用自己来
  保证,通过调用sync()方法.

- 等待无关（ wait-free）：慢的或者失效的client不干预快速的client的请求。

- 原子性：更新操作要么成功要么失败，没有第三种结果。

- 顺序一致性：客户端的更新顺序与它们被发送的顺序相一致。

> 1.最终一致性：client不论连接到哪个Server，展示给它都是同一个视图，这是zookeeper最重要的性能。

> 2 .可靠性：具有简单、健壮、良好的性能，如果消息m被到一台服务器接受，那么它将被所有的服务器接受。

> 3 .实时性：Zookeeper保证客户端将在一个时间间隔范围内获得服务器的更新信息，或者服务器失效的信息。但由于网络延时等原因，Zookeeper不能保证两个客户端能同时得到刚更新的数据，如果需要最新数据，应该在读数据之前调用sync()接口。

> 4 .等待无关（wait-free）：慢的或者失效的client不得干预快速的client的请求，使得每个client都能有效的等待。

> 5.原子性：更新只能成功或者失败，没有中间状态。

> 6 .顺序性：包括全局有序和偏序两种：全局有序是指如果在一台服务器上消息a在消息b前发布，则在所有Server上消息a都将在消息b前被发布；偏序是指如果一个消息b在消息a后被同一个发送者发布，a必将排在b前面。

# zk的原理

> ![](https://www.itweet.cn/screenshots/zk.jpg)

>Zookeeper的核心是原子广播，这个机制保证了各个Server之间的同步。实现这个机制的协议叫做Zab协议。Zab协议有两种模式，它们分别是恢复模式（选主）和广播模式（同步）。当服务启动或者在领导者崩溃后，Zab就进入了恢复模式，当领导者被选举出来，且大多数Server完成了和leader的状态同步以后，恢复模式就结束了。状态同步保证了leader和Server具有相同的系统状态。
>为了保证事务的顺序一致性，zookeeper采用了递增的事务id号（zxid）来标识事务。所有的提议（proposal）都在被提出的时候加上了zxid。实现中zxid是一个64位的数字，它高32位是epoch用来标识leader关系是否改变，每次一个leader被选出来，它都会有一个新的epoch，标识当前属于那个leader的统治时期。低32位用于递增计数。
>每个Server在工作过程中有三种状态：

> - LOOKING：当前Server不知道leader是谁，正在搜寻!
> - LEADING：当前Server即为选举出来的leader!
> - FOLLOWING：leader已经选举出来，当前Server与之同步!

# 基础环境条件
－－映射主机名，相互能ping通，参照视频教程完成基础优化，符合Hadoop平台环境要求。
  $ cat /etc/hosts
    192.168.2.1 server1
    192.168.2.2 server2
    192.168.2.3 server3
    192.168.2.4 server4

# zk角色
![](https://www.itweet.cn/screenshots/zk-observer.jpg)

# zk集群搭建
>获取zk安装包
>http://www.apache.org/dyn/closer.cgi/zookeeper/

## 1、解压
`tar -zxvf zookeeper-3.4.6.tar.gz `

## 2、复制示例文件
```	
－－修改配置文件
    cp /usr/local/zookeeper-3.4.6/conf/zoo_sample.cfg /usr/local/zookeeper-3.4.6/conf/zoo.cfg
```

## 3、修改zoo.cfg
```	
    修改数据存放目录：dataDir=/usr/local/zookeeper-3.4.6/data
	配置三台zk服务器
		server.1=server1:2888:3888
		server.2=server2:2888:3888
		server.3=server3:2888:3888
```

## 4、创建data文件夹
```	
    mkdir /usr/local/zookeeper-3.4.6/data
```

## 5、进入data目录
```		
        vi myid -->内容为1
		   有表示符1,代表第server.1台server
```

## 6、scp zookeeper
```	
    scp -rq zookeeper-3.4.6 server2:/usr/local/
	scp -rq zookeeper-3.4.6 server3:/usr/local/
```

## 7、修改myid文件
```	
    [root@server2 data]# vi myid  [值为2] 或者echo 2 > /usr/local/zookeeper-3.4.6/data/myid
	[root@server3 data]# vi myid	[值为3]
```

## 8、启动执行zk
```	
    [root@server1 local]# zk zookeeper-3.4.6/bin/zkServer.sh start
	[root@server2 local]# zk zookeeper-3.4.6/bin/zkServer.sh start
	[root@server3 local]# zookeeper-3.4.6/bin/zkServer.sh start
```

## 9、查看zk状态
```	
    [root@server1 local]# zookeeper-3.4.6/bin/zkServer.sh status
```

## 10、进入zk客户端
```	
    [root@server1 local]# zookeeper-3.4.6/bin/zkCli.sh 
		[zk: localhost:2181(CONNECTED) 3] get /zookeeper/quota [代表节点，每个节点存放数据信息]
```

https://www.tutorialspoint.com/zookeeper/zookeeper_cli.htm


