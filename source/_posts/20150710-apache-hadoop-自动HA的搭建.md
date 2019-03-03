---
title: Hadoop 的 HA 手动搭建
date: 2015-07-10 17:05:01
description: Hadoop 的 HA 手动搭建。
category: BigData
tags: hadoop
---

- 1、 core-site.xml
```
<configuration>
<property>
<name>fs.defaultFS</name>
<value>hdfs://mycluster</value>
</property>
<property>
<name>hadoop.tmp.dir</name>
<value>/data/whoami/hadoop</value>
</property>

<property>
<name>ha.zookeeper.quorum</name>
<value>server1:2181,server2:2181,server3:2181</value>
</property>

<property>
<name>fs.trash.interval</name>
<value>2000</value>
</property>
</configuration>
```

- 2、hdfs-site.xml
```
<configuration>
<property>
<name>dfs.replication</name>
<value>2</value>
</property>

<property>
<name>dfs.nameservices</name>
<value>mycluster</value>
</property>

<property>
<name>dfs.ha.namenodes.mycluster</name>
<value>nn1,nn2</value>
</property>

<property>
<name>dfs.namenode.rpc-address.mycluster.nn1</name>
<value>server1:9000</value>
</property>

<property>
<name>dfs.namenode.http-address.mycluster.nn1</name>
<value>server1:50070</value>
</property>

<property>
<name>dfs.namenode.rpc-address.mycluster.nn2</name>
<value>server2:9000</value>
</property>

<property>
<name>dfs.namenode.http-address.mycluster.nn2</name>
<value>server2:50070</value>
</property>

<property>
<name>dfs.ha.automatic-failover.enabled.mycluster</name>
<value>true</value>
</property>

<property>
<name>dfs.namenode.shared.edits.dir</name>
<value>qjournal://server1:8485;server2:8485;server3:8485/mycluster</value>
</property>

<property>
<name>dfs.journalnode.edits.dir</name>
<value>/data/whoami/hadoop/journal</value>
</property>

<property>
<name>dfs.ha.fencing.methods</name>
<value>sshfence</value>
</property>

<property>
<name>dfs.ha.fencing.ssh.private-key-files</name>
<value>/home/whomai/.ssh/id_rsa</value>
</property>

<property>
<name>dfs.client.failover.proxy.provider.mycluster</name>
<value>org.apache.hadoop.hdfs.server.namenode.ha.ConfiguredFailoverProxyProvider</value>
</property>
</configuration>
```
    

- 3、yarn-site.xml
```   
<configuration>
<property>
  <name>yarn.nodemanager.aux-services</name>
  <value>mapreduce_shuffle</value>
</property>

<property>
  <name>yarn.nodemanager.aux-services.mapreduce.shuffle.class</name>
  <value>org.apache.hadoop.mapred.ShuffleHandler</value>
</property>

<property>
  <name>yarn.nodemanager.local-dirs</name>
  <value>/data/whoami/hadoop/nm</value>
</property>

<property>
  <name>yarn.nodemanager.log-dirs</name>
  <value>/data/whoami/hadoop/logs</value>
</property>

<property>
  <name>yarn.log-aggregation-enable</name>
  <value>true</value>
</property> 

<property>
  <description>Where to aggregate logs</description>
  <name>yarn.nodemanager.remote-app-log-dir</name>
  <value>hdfs://mycluster/var/log/hadoop-yarn/apps</value>
</property>

<!-- Resource Manager Configs -->
<property>
  <name>yarn.resourcemanager.connect.retry-interval.ms</name>
  <value>2000</value>
</property>

<property>
  <name>yarn.resourcemanager.ha.enabled</name>
  <value>true</value>
</property>

<property>
  <name>yarn.resourcemanager.ha.automatic-failover.enabled</name>
  <value>true</value>
</property>

<property>
  <name>yarn.resourcemanager.ha.automatic-failover.embedded</name>
  <value>true</value>
</property>

<property>
  <name>yarn.resourcemanager.cluster-id</name>
  <value>yarn-cluster</value>
</property>

<property>
  <name>yarn.resourcemanager.ha.rm-ids</name>
  <value>rm1,rm2</value>
</property>

<property>
  <name>yarn.resourcemanager.ha.id</name>
  <value>rm1</value>
</property>

<property>
  <name>yarn.resourcemanager.scheduler.class</name>
  <value>org.apache.hadoop.yarn.server.resourcemanager.scheduler.fair.FairScheduler</value>
</property>

<property>
  <name>yarn.resourcemanager.recovery.enabled</name>
  <value>true</value>
</property>

<property>
  <name>yarn.resourcemanager.store.class</name>
  <value>org.apache.hadoop.yarn.server.resourcemanager.recovery.ZKRMStateStore</value>
</property>

<property>
  <name>yarn.resourcemanager.zk.state-store.address</name>
  <value>server1:2181,server2:2181,server3:2181</value>
</property>

<property>
  <name>yarn.app.mapreduce.am.scheduler.connection.wait.interval-ms</name>
  <value>5000</value>
</property>
 

  <!-- RM1 configs -->
<property>
  <name>yarn.resourcemanager.address.rm1</name>
  <value>server1:23140</value>
</property>

<property>
  <name>yarn.resourcemanager.scheduler.address.rm1</name>
  <value>server1:23130</value>
</property>

<property>
  <name>yarn.resourcemanager.webapp.https.address.rm1</name>
  <value>server1:23189</value>
</property>

<property>
  <name>yarn.resourcemanager.webapp.address.rm1</name>
  <value>server1:23188</value>
</property>

<property>
  <name>yarn.resourcemanager.resource-tracker.address.rm1</name>
  <value>server1:23125</value>
</property>

<property>
  <name>yarn.resourcemanager.admin.address.rm1</name>
  <value>server1:23141</value>
</property>


<!-- RM2 configs -->
<property>
  <name>yarn.resourcemanager.address.rm2</name>
  <value>server2:23140</value>
</property>

<property>
  <name>yarn.resourcemanager.scheduler.address.rm2</name>
  <value>server2:23130</value>
</property>

<property>
  <name>yarn.resourcemanager.webapp.https.address.rm2</name>
  <value>server2:23189</value>
</property>

<property>
  <name>yarn.resourcemanager.webapp.address.rm2</name>
  <value>server2:23188</value>
</property>

<property>
  <name>yarn.resourcemanager.resource-tracker.address.rm2</name>
  <value>server2:23125</value>
</property>

<property>
  <name>yarn.resourcemanager.admin.address.rm2</name>
  <value>server2:23141</value>
</property>


<!-- Node Manager Configs -->
<property>
  <description>Address where the localizer IPC is.</description>
  <name>yarn.nodemanager.localizer.address</name>
  <value>0.0.0.0:23344</value>
</property>

<property>
  <description>NM Webapp address.</description>
  <name>yarn.nodemanager.webapp.address</name>
  <value>0.0.0.0:23999</value>
</property>

  <property>
    <name>yarn.nodemanager.local-dirs</name>
    <value>/data/whoami/hadoop/nodemanager/yarn/local</value>
  </property>

  <property>
    <name>yarn.nodemanager.log-dirs</name>
    <value>/data/whoami/hadoop/nodemanager/yarn/log</value>
  </property>

<property>
  <name>mapreduce.shuffle.port</name>
  <value>23080</value>
</property>

<property>
  <name>yarn.resourcemanager.zk-address</name>
  <value>server1:2181,server2:2181,server3:2181</value>
</property>
</configuration>
```

- 4、mapred-site.xml
```
    <configuration>
<property>
<name>mapreduce.jobhistory.address</name>
<value>server1:10020</value>
</property>
<property>
<name>mapreduce.jobhistory.webapp.address</name>
<value>server1:19888</value>
</property>
<property>
<name>mapreduce.jobhistory.webapp.https.address</name>
<value>server1:19890</value>
</property>
<property>
<name>mapreduce.jobhistory.admin.address</name>
<value>server1:10033</value>
</property>
<property>
<name>mapreduce.framework.name</name>
<value>yarn</value>
</property>
<property>
<name>yarn.app.mapreduce.am.staging-dir</name>
<value>/user</value>
</property>
<property>
<name>mapreduce.task.timeout</name>
<value>1800000</value>
</property>
    </configuration>
```

修改server2上的yarn-site.xml
修改为下面的值：
```
<property>
    <name>yarn.resourcemanager.ha.id</name>
    <value>rm2</value>
</property>
```

- 5、slaves
```
    server3
    server04
```
    
- 6、hadoop-env.sh修改
```
    JAVA_HOME指定为jdk安装目录，JAVA_HOME=/usr/local/jdk1.7.0_45
```
   
- 7、scp hadoop-2.6.0
```  
    [root@server1 local]# scp -rq hadoop-2.6.0 server2:/usr/local/
    [root@server1 local]# scp -rq hadoop-2.6.0 server3:/usr/local/
    [root@server1 local]# scp -rq hadoop-2.6.0 server04:/usr/local/
```
    
- 8、启动journalnode
```
    [root@server1 local]# hadoop-daemon.sh start journalnode
    [root@server2 local]# hadoop-daemon.sh start journalnode
    [root@server3 local]# hadoop-daemon.sh start journalnode
```

- 9、格式化zkfc集群
```
    [root@server1 local]# hadoop-2.6.0/bin/hdfs zkfc -formatZK
```
    
- 10、格式化hdfs文件系统[格式化namenode,接着启动namenode]
```   
    [root@server1 tmp]# hadoop-2.6.0/bin/hdfs namenode -format -clusterId mycluster
    [root@server1 tmp]# hadoop-2.6.0/sbin/hadoop-daemon.sh start namenode
    [root@server2 tmp]# hadoop-2.6.0/bin/hdfs namenode -bootstrapStandby
    [root@server2 tmp]# hadoop-2.6.0/sbin/hadoop-daemon.sh start namenode
```
    
- 11、启动datanode
```    
    [root@server1 local]# /hadoop-2.6.0/sbin/hadoop-daemons.sh start datanode
```
    
- 10、启动zkfc [DFSZKFailoverController]
```    
    [root@server1 local]# /hadoop-2.6.0/sbin/hadoop-daemon.sh start zkfc
    [root@server2 tmp]# /hadoop-2.6.0/sbin/hadoop-daemon.sh start zkfc
```
    
- 11、启动yarn
```    
    [root@server1 local]# $ start-yarn.sh
    [hsu@server2 hadoop]$ yarn-daemon.sh start resourcemanager
```

active node：http://server1:23188/cluster/apps
standby node: http://server2:23188/cluster/apps

`目前处于standby node是无法看到详细信息的，kill active状态节点验证.`

`[hsu@server1 ~]$ kill 5709`

---
http://server2:23188/cluster/cluster 地址看到信息：ResourceManager HA state: active

http://server1:23188/cluster/cluster 地址看到信息：ResourceManager HA state:  standby

- 12、测试hdfs+Yarn+MR
```    
    [root@server1 local]# hadoop-2.6.0/bin/hadoop fs -put /hadoop-env.sh /testdata
    [root@server1 local]# hadoop-2.6.0/bin/hadoop jar hadoop-mapreduce-examples-2.6.0.jar wordcount /testdata /output
```
    
- 13、启动historyserver [查询作业执行的详细情况]
```   
    [root@server1 local]# mr-jobhistory-daemon.sh start historyserver  
```

- 14、native库问题
```
$ hadoop/bin/hadoop fs -put zookeeper.out  /input
15/07/20 13:19:30 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable

需要自己编译一个hadoop的包。在64位机器。
```

参考：http://hadoop.apache.org/docs/r2.4.1/hadoop-yarn/hadoop-yarn-site/ResourceManagerHA.html

#### Hadoop版本历史
<div style="text-align:center;"><img src="https://www.itweet.cn/screenshots/version.png" style="vertical-align:middle;"/></div>


原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/
