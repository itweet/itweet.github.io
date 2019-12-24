---
title: Phoenix-hbase
date: 2015-07-16 18:28:48
description: Phoenix，由saleforce.com开源的一个项目，后又捐给了Apache。它相当于一个Java中间件，帮助开发者，像使用jdbc访问关系型数据库一样，访问NoSql数据库HBase。
category: BigData
tags: hbase
---
![](http://phoenix.apache.org/images/phoenix-logo-small.png)

>phoenix，由saleforce.com开源的一个项目，后又捐给了Apache。它相当于一个Java中间件，帮助开发者，像使用jdbc访问关系型数据库一样，访问NoSql数据库HBase。

>phoenix，操作的表及数据，存储在hbase上。phoenix只是需要和Hbase进行表关联起来。然后再用工具进行一些读或写操作。

>其实，可以把Phoenix只看成一种代替HBase的语法的一个工具。虽然可以用java可以用jdbc来连接phoenix，然后操作HBase，但是在生产环境中，不可以用在OLTP中。在线事务处理的环境中，需要低延迟，而Phoenix在查询HBase时，虽然做了一些优化，但延迟还是不小。所以依然是用在OLAT中，再将结果返回存储下来。

>Phoenix官网上，对Phoenix讲解已经很好了。可以看官网，更正式一些。http://phoenix.apache.org/

![](http://phoenix.apache.org/images/sqlline.png)

# 一、基本环境准备

## 1、安装好hbase，hbase正常使用！

>hbase安装参考我的另外一篇博文：https://www.itweet.cn/2015/07/15/Hbase-Distributed-install/

```
    [hsu@server1 ~]$ hbase shell
    15/03/15 15:58:57 INFO Configuration.deprecation: hadoop.native.lib is  deprecated. Instead, use io.native.lib.available
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
     user1|ts1                         column=sf:c1, timestamp=1426406452681,   value=sku                                                   
     user1|ts2                         column=sf:c1, timestamp=1426406477190,   value=sku188                                                
     user1|ts3                         column=sf:s1, timestamp=1426406482547,   value=sku123                                                
    3 row(s) in 0.0810 seconds
    hbase(main):006:0>!q
```

## 2、hbase master所在server1上
```
    [hsu@server1 ~]$ hbase version
    15/03/15 16:03:08 INFO util.VersionInfo: HBase 0.98.6-cdh5.2.0
   
    
    [hsu@server1 ~]$ which hbase
    /usr/bin/hbase
```

## 3、当前系统软件信息
```
[hsu@server1 ~]$ java -version 
java version "1.7.0_09-icedtea"
OpenJDK Runtime Environment (rhel-2.3.4.1.el6_3-x86_64)
OpenJDK 64-Bit Server VM (build 23.2-b09, mixed mode)

[hsu@server1 ~]$ cat /etc/redhat-release 
Red Hat Enterprise Linux Server release 6.4 (Santiago)
[hsu@server1 ~]$ uname -a
Linux server1 2.6.32-358.el6.x86_64 #1 SMP Tue Jan 29 11:47:41 EST 2013 x86_64 x86_64 x86_64 GNU/Linux
```

# 二、安装phoenix

## 1、phoenix与hbase版本对应关系
    http://phoenix.apache.org/download.html
    phoenix与HBase版本对应关系
    Phoenix 2.x - HBase 0.94.x
    Phoenix 3.x - HBase 0.94.x
    Phoenix 4.x - HBase 0.98.1+

## 2、hbase的配置文件
```
# cat hbase-site.xml 
<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
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
  <name>hbase.master</name>
  <value>server1:60010</value>
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
         <name>hbase.regionserver.hlog.replication</name>
         <value>2</value>
        </property>
</configuration>
```


## 3、hbase安装目录
```
[hsu@server2 lib]$ pwd
/opt/cloudera/parcels/CDH/lib/hbase/lib
```

## 4、安装phoenix
> 注意：phoenix需要安装在hbase master节点上

http://phoenix.apache.org/installation.html#
```
[hsu@svr99 ~]$ ls -l software/phoenix-4.3.0-bin.tar.gz     
-rw-rw-r-- 1 hsu hsu 71958249 Mar 15 15:41 software/phoenix-4.3.0-bin.tar.gz
[hsu@svr99 ~]$ scp software/phoenix-4.3.0-bin.tar.gz server1:~
[hsu@server1 ~]$ ls -l phoenix-4.3.0-bin.tar.gz 
-rw-rw-r-- 1 hsu hsu 71958249 Mar 15 16:31 phoenix-4.3.0-bin.tar.gz
```

### 4.1 Download
> Download and expand the latest phoenix-[version]-bin.tar.
```
    [hsu@server1 ~]$ tar -zxf phoenix-4.3.0-bin.tar.gz
    [hsu@server1 ~]$ ln -s phoenix-4.3.0-bin phoenix
```

### 4.2 Add the phoenix jar

> Add the phoenix-[version]-server.jar to the classpath of all HBase region

```
    [hsu@server1 ~]$ cd phoenix
    [hsu@server1 phoenix]$ sudo scp phoenix-4.3.0-server.jar 
    server2:/opt/cloudera/parcels/CDH/lib/hbase/lib/    

    [hsu@server1 phoenix]$ sudo scp phoenix-4.3.0-server.jar 、
    server3:/opt/cloudera/parcels/CDH/lib/hbase/lib/

    [hsu@server1 phoenix]$ sudo scp phoenix-4.3.0-server.jar 
    server4:/opt/cloudera/parcels/CDH/lib/hbase/lib/

    [hsu@server1 phoenix]$ sudo cp  phoenix-4.3.0-server.jar
     /opt/cloudera/parcels/CDH/lib/hbase/lib/

    [hsu@server2 ~]$ ls /opt/cloudera/parcels/CDH/lib/hbase/lib/phoenix-4.3.0-server.jar 
    /opt/cloudera/parcels/CDH/lib/hbase/lib/phoenix-4.3.0-server.jar

```

### 4.3 copy conf to phoenix

> copy hbase conf file to phoenix bin

```
    [hsu@server1 bin]$ cp hbase-site.xml hbase-site.xml.ori
    [hsu@server1 bin]$ cp /opt/cloudera/parcels/CDH/lib/hbase/conf/hbase-site.xml /home/hsu/phoenix/bin/
    [hsu@server1 bin]$ ll hbase-site.xml*
    -rw-r--r-- 1 hsu hsu 1473 Mar 15 16:57 hbase-site.xml
    -rw-r--r-- 1 hsu hsu 1136 Mar 15 16:57 hbase-site.xml.ori
```

### 4.4 Restart HBase
    Cludera cdh version hbase的 start-hbase.sh and stop-hbase.sh脚本我硬是没找到！

#### 4.4.1 CDH 版本hbase

>cdh-5.3.0-0.98.6-cdh5.2.0版本集群copy phoenix到lib

>重启集群一直无法成功，删除所有节点/opt/cloudera/parcels/CDH/lib/hbase/lib/phoenix-core-4.3.0.jar  包后重启，居然不报错了，奇葩吧！
sudo rm -f /opt/cloudera/parcels/CDH/lib/hbase/lib/phoenix-core-4.3.0.jar
出现这个奇葩问题是我没有注意看安装文档，我copy phoenix-core-[version].jar文件到所有的hbase/lib下面，导致重启hbase的registerserver一直启动失败：
Add the phoenix-[version]-server.jar to the classpath of all HBase region server and master and remove any previous version. An easy way to do this is to copy it into the HBase lib directory (use phoenix-core-[version].jar for Phoenix 3.x)

>当我放置正确的jar到hbase/lib下面以后照样还是registerserver报错！再次删除所有节点的包，重启恢复正常：
sudo rm -f /opt/cloudera/parcels/CDH/lib/hbase/lib/phoenix-4.3.0-server.jar  

#### 4.4.2 apache版本hbase

>apache 0.98.6.1-hadoop2版本

>Apache版本的hbase 0.98.6.1-hadoop2重启无异常，启动正常！

```
    [root@server1 bin]# hbase shell
    2015-03-15 19:23:35,387 INFO  [main] Configuration.deprecation: hadoop.native.lib is deprecated. Instead, use io.native.lib.available
    HBase Shell; enter 'help<RETURN>' for list of supported commands.
    Type "exit<RETURN>" to leave the HBase Shell
    Version 0.98.6.1-hadoop2, r96a1af660b33879f19a47e9113bf802ad59c7146, Sun Sep 14 21:27:25 PDT 2014

    hbase(main):001:0> list
    TABLE                                                                                                                                 
    SLF4J: Class path contains multiple SLF4J bindings.
    SLF4J: Found binding in [jar:file:/usr/local/hbase-0.98.6.1/lib/slf4j-log4j12-1.6.4.jar!/org/slf4j/impl/StaticLoggerBinder.class]
    SLF4J: Found binding in [jar:file:/usr/local/hadoop-2.4.0/share/hadoop/common/lib/slf4j-log4j12-1.7.5.jar!/org/slf4j/impl/StaticLoggerBinder.class]
    SLF4J: See http://www.slf4j.org/codes.html#multiple_bindings for an explanation.
    t1                                                                                                                                    
    test2                                                                                                                                 
    2 row(s) in 20.2820 seconds

    => ["t1", "test2"]
    hbase(main):002:0> scan 't1'
    ROW                                COLUMN+CELL                                                                                        
     rk1                               column=t1:c2, timestamp=1416914603519, value=\xE6\x8B\x9C\xE6\x8B\x9C                              
     rk1                               column=t1:cf2, timestamp=1416913804175, value=\xE6\x9F\xB3\xE6\xA0\x91                             
    1 row(s) in 1.1890 seconds
```

### 4.5 add phoenix jar to classpath

>Add the phoenix-[version]-client.jar to the classpath of any Phoenix client

```
[hsu@server1 phoenix]$ vi /home/hsu/.bash_profile
[hsu@server1 phoenix]$ tail -3 /home/hsu/.bash_profile 
export PHOENIX_HOME=/home/hsu/phoenix/
export CLASSPATH=$CLASSPATH:$PHOENIX_HOME/phoenix-4.3.0-client.jar
[hsu@server1 phoenix]$ source /home/hsu/.bash_profile
```

### 4.5 启动phoenix连接hbase集群
```
[hsu@server1 ~]$ cd phoenix/bin/
[hsu@server1 bin]$ cat readme.txt         #查看使用方式
```

#### cdh版本hbase测试

> 4.5.1 cdh-5.3.0-0.98.6-cdh5.2.0 版本测试[失败]

```
[hsu@server1 bin]$ ./sqlline.py server1:2181
报错：
15/03/15 17:15:19 WARN util.DynamicClassLoader: Failed to identify the fs of dir hdfs://server1:8020/hbase/lib, ignored
java.io.IOException: No FileSystem for scheme: hdfs
[hsu@server2 ~]$ hadoop fs -ls hdfs://server1:8020/hbase|wc -l
8
出现此问题是因为没有操作4.5这一步

[hsu@server1 phoenix]$ bin/sqlline.py server1:2181
Setting property: [isolation, TRANSACTION_READ_COMMITTED]
issuing: !connect jdbc:phoenix:server1:2181 none none org.apache.phoenix.jdbc.PhoenixDriver
Connecting to jdbc:phoenix:server1:2181
SLF4J: Failed to load class "org.slf4j.impl.StaticLoggerBinder".
SLF4J: Defaulting to no-operation (NOP) logger implementation
SLF4J: See http://www.slf4j.org/codes.html#StaticLoggerBinder for further details.
15/03/15 17:46:25 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
15/03/15 17:46:25 WARN impl.MetricsConfig: Cannot locate configuration: tried hadoop-metrics2-phoenix.properties,hadoop-metrics2.properties
#这里cdh habase版本，一直处于等待状态，因为copy lib到hbase/lib后重启一直不正常！

后面继续测试：
cp phoenix-4.3.0-server.jar /opt/cloudera/parcels/CDH/lib/hbase/lib/
sudo chmod 777 /opt/cloudera/parcels/CDH/lib/hbase/lib/phoenix-4.3.0-server.jar      

重启hbase：依然未解决意外退出，日志信息无报错！
```

#### apache hbase 版本测试

>4.5.2 Apache hbase 0.98.6.1-hadoop2版本测试[成功]

```
[root@server1 bin]# ./sqlline.py server1:2181
java.io.IOException: No FileSystem for scheme: hdfs

[root@server1 local]# ln -s phoenix-4.3.0-bin phoenix

[root@server1 ~]# cat /etc/profile|grep 'CLASSPATH:$HADOOP_HOME/lib'
export CLASSPATH=$CLASSPATH:$HADOOP_HOME/lib

[root@server1 ~]# tail -3 .bash_profile    
export PHOENIX_HOME=/usr/local/phoenix/
export CLASSPATH=$CLASSPATH:$PHOENIX_HOME/phoenix-4.3.0-client.jar

[root@server1 hdfs]# echo $CLASSPATH
.:/usr/local/jdk1.7.0_45/lib:/usr/local/jdk1.7.0_45/jre/lib:.:/usr/local/jdk1.7.0_45/lib:/usr/local/jdk1.7.0_45/jre/lib:.:/usr/local/jdk1.7.0_45/lib:/usr/local/jdk1.7.0_45/jre/lib::/usr/local/phoenix-4.3.0-bin/phoenix-4.3.0-client.jar:/usr/local/phoenix//phoenix-4.3.0-client.jar:/usr/local/hadoop-2.4.0/lib:/usr/local/hadoop-2.4.0/share/hadoop/hdfs

[root@server1 bin]# ./sqlline.py server1:2181
Setting property: [isolation, TRANSACTION_READ_COMMITTED]
issuing: !connect jdbc:phoenix:server1:2181 none none org.apache.phoenix.jdbc.PhoenixDriver
Connecting to jdbc:phoenix:server1:2181
15/03/15 20:03:23 WARN util.DynamicClassLoader: Failed to identify the fs of dir hdfs://server1:9000/user/hbase/lib, ignored
java.io.IOException: No FileSystem for scheme: hdfs
Connected to: Phoenix (version 4.3)
Driver: PhoenixEmbeddedDriver (version 4.3)
Autocommit status: true
Transaction isolation: TRANSACTION_READ_COMMITTED
Building list of tables and columns for tab-completion (set fastconnect to true to skip)...
70/70 (100%) Done
Done
sqlline version 1.1.8
0: jdbc:phoenix:server1:2181> !help
    !all                Execute the specified SQL against all the current connections
    !autocommit         Set autocommit mode on or off
    !batch              Start or execute a batch of statements
    !brief              Set verbose mode off
    !call               Execute a callable statement
    !close              Close the current connection to the database
    !closeall           Close all current open connections
    !columns            List all the columns for the specified table
    !commit             Commit the current transaction (if autocommit is off)
    !connect            Open a new connection to the database.
    !dbinfo             Give metadata information about the database
    !describe           Describe a table
    !dropall            Drop all tables in the current database
    !exportedkeys       List all the exported keys for the specified table
    !go                 Select the current connection
    !help               Print a summary of command usage
    !history            Display the command history
    !importedkeys       List all the imported keys for the specified table
    !indexes            List all the indexes for the specified table
    !isolation          Set the transaction isolation for this connection
    !list               List the current connections
    !manual             Display the SQLLine manual
    !metadata           Obtain metadata information
    !nativesql          Show the native SQL for the specified statement
    !outputformat       Set the output format for displaying results
                        (table,vertical,csv,tsv,xmlattrs,xmlelements)
    !primarykeys        List all the primary keys for the specified table
    !procedures         List all the procedures
    !properties         Connect to the database specified in the properties file(s)
    !quit               Exits the program
    !reconnect          Reconnect to the database
    !record             Record all output to the specified file
    !rehash             Fetch table and column names for command completion
    !rollback           Roll back the current transaction (if autocommit is off)
    !run                Run a script from the specified file
    !save               Save the current variabes and aliases
    !scan               Scan for installed JDBC drivers
    !script             Start saving a script to a file
    !set                Set a sqlline variable
0: jdbc:phoenix:server1:2181> !list
1 active connection:
 #0  open     jdbc:phoenix:server1:2181

0: jdbc:phoenix:server1:2181>  select * from SYSTEM.CATALOG;
+------------------------------------------+------------------------------------------+------------------------------------------+------+
|                TENANT_ID                 |               TABLE_SCHEM                |                TABLE_NAME                |      |
+------------------------------------------+------------------------------------------+------------------------------------------+------+
|                                          |                                          | TEST                                     |      |
|                                          |                                          | TEST                                     | MYCO |
|                                          |                                          | TEST                                     | MYKE |
|                                          | SYSTEM                                   | CATALOG                                  |      |
|                                          | SYSTEM                                   | CATALOG                                  | ARRA |
.....省略...

#在hbase验证是否可以看到有test表,也可以看到phoenix生成的系统表
hbase(main):002:0> list
TABLE                                                                                                                                    
SYSTEM.CATALOG                                                                                                                           
SYSTEM.SEQUENCE                                                                                                                          
SYSTEM.STATS                                                                                                                             
TEST                                                                                                                                     
TEST01                                                                                                                                   
5 row(s) in 2.3750 seconds

=> ["SYSTEM.CATALOG", "SYSTEM.SEQUENCE", "SYSTEM.STATS", "TEST", "TEST01"]

```


# 问题
- 1、解决java.io.IOException: No FileSystem for scheme: hdfs 

```
[root@server1 lib]# cat /etc/profile|grep 'CLASSPATH:/usr/local/hbase-0.98.6.1/lib'
export CLASSPATH=$CLASSPATH:/usr/local/hbase-0.98.6.1/lib
[root@server1 lib]# source /etc/profile
[root@server1 bin]# sqlline.py server1:2181/hbase   
```

```
WARN util.DynamicClassLoader: Failed to identify the fs of 
dir hdfs://server01:54310/hbase/lib, ignored
java.io.IOException: No FileSystem for scheme: hdfs
        at org.apache.hadoop.fs.FileSystem.getFileSystemClass(FileSystem.java:2421)  
        at org.apache.hadoop.fs.FileSystem.createFileSystem(FileSystem.java:2428)  
        at org.apache.hadoop.fs.FileSystem.access$200(FileSystem.java:88)  
        at org.apache.hadoop.fs.FileSystem$Cache.getInternal(FileSystem.java:2467)  
        at org.apache.hadoop.fs.FileSystem$Cache.get(FileSystem.java:2449)  
        at org.apache.hadoop.fs.FileSystem.get(FileSystem.java:367)  
        at FileCopyToHdfs.readFromHdfs(FileCopyToHdfs.java:65)  
        at FileCopyToHdfs.main(FileCopyToHdfs.java:26) 
```

- 解决：
这是因为该包下默认的core-default.xml没有配置如下属性。
修改hbase的lib/hadoop-common-2.2.0.jar包里面的core-default.xml添加重启集群
```
    <property>  
        <name>fs.hdfs.impl</name>  
        <value>org.apache.hadoop.hdfs.DistributedFileSystem</value>  
        <description>The FileSystem for hdfs: uris.</description>  
    </property>  

    hadoop fs -rm -f hdfs://server1:9000/user/hbase/lib/hadoop-common-2.2.0.jar
    hadoop fs -put hadoop-common-2.2.0.jar hdfs://server1:9000/user/hbase/lib
```

`上属性指定fs.hdfs.impl的实现类。添加完后，未解决。`

```
在HDP官网找到相同错误：http://docs.hortonworks.com/HDPDocuments/HDP2/HDP-2.1.3/bk_installing_manually_book/content/rpm-chap-phoenix.html

我通过在${PHOENIX_HOME}/bin/hbase-site.xml中添加设置解决了问题。
<property>  
        <name>fs.hdfs.impl</name>  
        <value>org.apache.hadoop.hdfs.DistributedFileSystem</value>  
</property> 
    [root@server1 bin]# ./sqlline.py server1:2181
    Setting property: [isolation, TRANSACTION_READ_COMMITTED]
    issuing: !connect jdbc:phoenix:server1:2181 none none org.apache.phoenix.jdbc.PhoenixDriver
    Connecting to jdbc:phoenix:server1:2181
    SLF4J: Failed to load class "org.slf4j.impl.StaticLoggerBinder".
    SLF4J: Defaulting to no-operation (NOP) logger implementation
    SLF4J: See http://www.slf4j.org/codes.html#StaticLoggerBinder for further details.
    15/07/16 16:59:56 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
    Connected to: Phoenix (version 4.3)
    Driver: PhoenixEmbeddedDriver (version 4.3)
    Autocommit status: true
    Transaction isolation: TRANSACTION_READ_COMMITTED
    Building list of tables and columns for tab-completion (set fastconnect to true to skip)...
    74/74 (100%) Done
    Done
    sqlline version 1.1.8
    0: jdbc:phoenix:server1:2181> 
    0: jdbc:phoenix:server1:2181> !table
+-----------+-------------+------------+------+
| TABLE_CAT | TABLE_SCHEM | TABLE_NAME |      |
+-----------+-------------+------------+------+
|           | SYSTEM      | CATALOG    | SYST |
|           | SYSTEM      | SEQUENCE   | SYST |
|           | SYSTEM      | STATS      | SYST |
|           |             | ABC        | TABL |
|           |             | TEST       | TABL |
+-----------+-------------+------------+------+
```

- 2：hbase创建的表没有加载进来，只看到phoenix初始化的表和新建的表，hbase里面创建的表没有显示出来！

>尝试hbase shell创建一张表TEST01查看是否phoenix也能加载到！phoenix创建的表可以被看到，而hbase里面创建的不能别看到。

```
0: jdbc:phoenix:server1:2181> !table
+-----------+-------------+------------+------+
| TABLE_CAT | TABLE_SCHEM | TABLE_NAME |      |
+-----------+-------------+------------+------+
|           | SYSTEM      | CATALOG    | SYST |
|           | SYSTEM      | SEQUENCE   | SYST |
|           | SYSTEM      | STATS      | SYST |
|           |             | TEST       | TABL |
+-----------+-------------+------------+------+
```

```
[root@server1 bin]# sqlline.py server1,server2,server3

进入zkCli.sh查看phoenix生成的节点数据
[root@server2 local]# zookeeper-3.4.6/bin/zkCli.sh

进入phoenix客户端
[root@server1 bin]# sqlline.py server1:2181/hbase
Setting property: [isolation, TRANSACTION_READ_COMMITTED]
issuing: !connect jdbc:phoenix:server1:2181/hbase none none org.apache.phoenix.jdbc.PhoenixDriver
Connecting to jdbc:phoenix:server1:2181/hbase

#依然没有成功，加载hbase shell创建的表！
查看webui看看两种不同客户端创建的表有何区别，后面表定义有很大不同，所以这里可以看出问题所在！下面TEST表示phoenix创建的，TEST01是Hbase shell创建...

TEST    1   'TEST', {TABLE_ATTRIBUTES => {coprocessor$1 => '|org.apache.phoenix.coprocessor.ScanRegionObserver|805306366|', coprocessor$2 => '|org.apache.phoenix.coprocessor.UngroupedAggregateRegionObserver|805306366|', coprocessor$3 => '|org.apache.phoenix.coprocessor.GroupedAggregateRegionObserver|805306366|', coprocessor$4 => '|org.apache.phoenix.coprocessor.ServerCachingEndpointImpl|805306366|', coprocessor$5 => '|org.apache.phoenix.hbase.index.Indexer|805306366|index.builder=org.apache.phoenix.index.PhoenixIndexBuilder,org.apache.hadoop.hbase.index.codec.class=org.apache.phoenix.index.PhoenixIndexCodec', coprocessor$6 => '|org.apache.hadoop.hbase.regionserver.LocalIndexSplitter|805306366|'}, {NAME => '0', DATA_BLOCK_ENCODING => 'FAST_DIFF'}

TEST01  1   'TEST01', {NAME => 'lf'}, {NAME => 'sf'}
```

## 5、java连接phoenix
http://phoenix.apache.org/faq.html
```
    package org.sparkjvm.jdbc.phoenix;

    import java.sql.Connection;
    import java.sql.DriverManager;
    import java.sql.PreparedStatement;
    import java.sql.ResultSet;
    import java.sql.SQLException;
    import java.sql.Statement;

    /**
     - Created by Andrew on 2015/3/15.
     */
    public class PhoenixConnectTest {
        public static void main(String[] args) throws SQLException {
            Statement stmt = null;
            ResultSet rset = null;
            //String driver = "org.apache.phoenix.jdbc.PhoenixDriver";

            Connection con = DriverManager.getConnection("jdbc:phoenix:server1:2181");
    //        Connection con = DriverManager.getConnection("jdbc:phoenix:server1,server2,server3");
            stmt = con.createStatement();

    //        stmt.executeUpdate("create table test (mykey integer not null primary key, mycolumn varchar)");
    //        stmt.executeUpdate("upsert into test values (1,'Hello')");
    //        stmt.executeUpdate("upsert into test values (2,'World!')");
            con.commit();

            PreparedStatement statement = con.prepareStatement("select * from test");
            rset = statement.executeQuery();
            while (rset.next()) {
                System.out.println(rset.getString("mycolumn"));
            }
            statement.close();
            con.close();
        }
    }
```

>结果：hello world!

>执行以上代码后在后台客户端查询表生成情况！

```
0: jdbc:phoenix:server1:2181> select * from TEST;
+------------------------------------------+------------------------------------------+
|                  MYKEY                   |                 MYCOLUMN                 |
+------------------------------------------+------------------------------------------+
| 1                                        | Hello                                    |
| 2                                        | World!                                   |
+------------------------------------------+------------------------------------------+
2 rows selected (0.17 seconds)
```

>命令行操作

```
0: jdbc:phoenix:server1:2181> create table abc(a integer primary key, b integer) ; 
No rows affected (7.342 seconds)

0: jdbc:phoenix:server1:2181> UPSERT INTO abc VALUES (1, 1); 
1 row affected (1.586 seconds)

0: jdbc:phoenix:server1:2181> UPSERT INTO abc VALUES (1, 1); 
1 row affected (1.586 seconds)
0: jdbc:phoenix:server1:2181> UPSERT INTO abc VALUES (1, 2); 
1 row affected (0.581 seconds)
0: jdbc:phoenix:server1:2181> UPSERT INTO abc VALUES (2, 1); 
1 row affected (0.099 seconds)

0: jdbc:phoenix:server1:2181> select * from abc;
0: jdbc:phoenix:server1:2181> select * from abc;
+------------------------------------------+---------------------------------+
|                    A                     |             B                     |
+------------------------------------------+---------------------------------+
| 1                                        |          2                      |
| 2                                        |          1                      |
+------------------------------------------+----------------------------------+
2 rows selected (0.11 seconds)
```

>查看hbase里面是否有abc表

```
    [root@server3 bin]# hbase shell
    2015-07-16 15:32:41,808 INFO  [main] Configuration.deprecation: hadoop.native.lib is deprecated. Instead, use io.native.lib.available
    HBase Shell; enter 'help<RETURN>' for list of supported commands.
    Type "exit<RETURN>" to leave the HBase Shell
    Version 0.98.6.1-hadoop2, r96a1af660b33879f19a47e9113bf802ad59c7146, Sun Sep 14 21:27:25 PDT 2014

    hbase(main):001:0> list
    TABLE                                                                      
    ABC                                                                                                                                      
    SYSTEM.CATALOG                                                                                                                           
    SYSTEM.SEQUENCE                                                                                                                          
    SYSTEM.STATS                                                                                                                             
    TEST                                                                                                                                     
    TEST01                                                                                                                                   
    6 row(s) in 2.6710 seconds

    => ["ABC", "SYSTEM.CATALOG", "SYSTEM.SEQUENCE", "SYSTEM.STATS", "TEST", "TEST01"]

    hbase(main):003:0> scan 'ABC'
    ROW                                 COLUMN+CELL                                                                                          
     \x80\x00\x00\x01                   column=0:B, timestamp=1437031486946, value=\x80\x00\x00\x02                                          
     \x80\x00\x00\x01                   column=0:_0, timestamp=1437031486946, value=                                                         
     \x80\x00\x00\x02                   column=0:B, timestamp=1437031493300, value=\x80\x00\x00\x01                                          
     \x80\x00\x00\x02                   column=0:_0, timestamp=1437031493300, value=                                                         
    2 row(s) in 2.2190 seconds

    hbase(main):004:0>
```


## 6、docker run phoenix
    http://blog.sequenceiq.com/blog/2014/09/04/sql-on-hbase-with-apache-phoenix/

# 二、Mapping to an Existing HBase Table
    http://phoenix.apache.org/index.html#Mapping-to-an-Existing-HBase-Table
    Hbase端操作：
    hbase(main):007:0> disable 't1'
    0 row(s) in 2.3870 seconds
    hbase(main):008:0> drop 't1'
    0 row(s) in 1.3260 seconds
    
    create 't1', {NAME => 'f1', VERSIONS => 5}
    put 't1', 'baiyc_20150716_0001', 'f1:val', 'baiyc1'
    put 't1', 'baiyc_20150716_0001', 'f1:name', 'baiyc1'
    put 't1', 'baiyc_20150716_0002', 'f1:val', 'baiyc2'
    
    Phoenix操作：
    CREATE VIEW "t1" ( k VARCHAR primary key, "name" VARCHAR, "val" VARCHAR) default_column_family='f1';
    select * from "t1";
    
    2、多列族操作；
    Hbase端操作
    create 'userc',{NAME=>'base',VERSION=>3 },{NAME=>'ext',VERSION=>1 } 
    put 'userc', 'baiyc_20150716_0001', 'base:name', 'baiyc1'
    put 'userc', 'baiyc_20150716_0001', 'base:age', '11'
    put 'userc', 'baiyc_20150716_0001', 'ext:sex', 'm'
    put 'userc', 'baiyc_20150716_0001', 'ext:heigh', '170'
    put 'userc', 'zhangs_20150716_0001', 'base:name', 'zhangs1'
    put 'userc', 'zhangs_20150716_0001', 'base:age', '31'
    put 'userc', 'zhangs_20150716_0001', 'ext:sex', 'f'
    put 'userc', 'zhangs_20150716_0001', 'ext:heigh', '160'
    Phoenix操作：
    CREATE VIEW "userc" ( rowkey VARCHAR primary key, "name" VARCHAR, "age" VARCHAR) default_column_family='base'; --ok
    select * from "userc";
    DROP VIEW IF EXISTS "userc";
    3、查询phoenix客户端创建表，直接使用大写字母的表名，如果查询视图，视图名称必须使用双引号括起来查询且区分大小写；
    phoenix客户端查询操作：
```
    0: jdbc:phoenix:server1:2181>  CREATE VIEW "userc" ( rowkey VARCHAR primary key, "name" VARCHAR, "age" VARCHAR) default_column_family='base';
    No rows affected (6.347 seconds)
    0: jdbc:phoenix:server1:2181> select * from "userc";
    +----------------------+---------+-----+
    | ROWKEY               | name    | age |
    +----------------------+---------+-----+
    | baiyc_20150716_0001  | baiyc1  | 11  |
    | zhangs_20150716_0001 | zhangs1 | 31  |
    +----------------------+---------+-----+
    2 rows selected (0.421 seconds)
    0: jdbc:phoenix:server1:2181> select "ROWKEY","name","age" from "userc"; 
    +----------------------+---------+-----+
    | ROWKEY               | name    | age |
    +----------------------+---------+-----+
    | baiyc_20150716_0001  | baiyc1  | 11  |
    | zhangs_20150716_0001 | zhangs1 | 31  |
    +----------------------+---------+-----+
    2 rows selected (0.15 seconds)

    phoenix程序java代码查询操作：
    String querySql = "select * from \"userc\" "; //可查询视图中所有字段信息,视图名称必须使用双引号括起来查询且区分大小写，表明是查询一个视图，不是查询表；
    4、为了大小写不敏感，建议所有定义表名、列族名、字段名等都使用大写，要求客户端用户查询也全部使用大写操作。
```

# hbase-1.1.5 整合phoenix－4.7.0
```
2016-06-26 00:16:09,713 ERROR [RS_OPEN_REGION-bigdata-server-1:16020-0] handler.OpenRegionHandler: Failed open of region=SYSTEM.CATALOG,,1466870656182.03e30d1b07989af24fcbcb1173fcfd91., starting to roll back the global memstore size.
java.io.IOException: Class org.apache.phoenix.coprocessor.MetaDataRegionObserver cannot be loaded
...........
2016-06-26 00:16:15,153 INFO  [regionserver/server1/192.168.2.201:16020] regionserver.HRegionServer: regionserver/server1/192.168.2.201:16020 exiting
2016-06-26 00:16:15,153 ERROR [main] regionserver.HRegionServerCommandLine: Region server exiting
java.lang.RuntimeException: HRegionServer Aborted
...........
```
出现如上错误，是因为我安装官网重新安装一次hbase，并没有按照我的文档按照，没有把phoenix-xxx-server.jar copy到所有节点hbase／lib下面，而是根据官网说的，jar放到classpath：
```
[root@server1]# env|grep CLASSPATH
HADOOP_CLASSPATH=:/opt/cloud/tez/conf:/opt/cloud/tez/*:/opt/cloud/tez/lib/*
CLASSPATH=:/opt/cloud/phoenix/phoenix-4.7.0-HBase-1.1-client.jar,/opt/cloud/phoenix/phoenix-4.7.0-HBase-1.1-server.jar
```
这样做是不行的，而我把`phoenix-4.7.0-HBase-1.1-server.jar`放到所有`hbase`的`lib`目录下，可以正常初始化完成，而不是卡住phoenix客户端，去看所有regionserver节点，发现都down掉了！

待续…

# 三、有关phoenix，hbase,impala,hive性能测试
>https://github.com/forcedotcom/phoenix/wiki/Performance
>https://blogs.apache.org/phoenix/
>https://blogs.apache.org/phoenix/entry/tpc_in_apache_phoenix


