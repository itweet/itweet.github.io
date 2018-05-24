---
title: Hadoop issue collections
date: 2016-03-17 17:11:33
category: BigData
tags: hadoop
---
整理在工作中遇到的Hadoop平台遇到的报错信息，以及解决思路。

# 问题1：基于Yarn统一资源管理平台配置导致
  - 错误信息：
`Application application_1458180019333_0002 failed 2 times due to AM Container`
`for appattempt_1458180019333_0002_000002 exited with exitCode: -1000`
`For more detailed output, check application tracking page:http://`
`server-02:8088/proxy/application_1458180019333_0002/Then, click on links to `
`logs of each attempt.Diagnostics: Not able to initialize user directories in` 
`any of the configured local directories for user hadoop`
`Failing this attempt. Failing the application.`
  
  - 原因：
  
  Actually this is due to the permission issues on some of the yarn local directories. I started using LinuxContainerExecutor (in non secure mode with nonsecure-mode.local-user as kailash) and made corresponding changes. However due to some (unknown) reason NodeManager failed to clean local directories for users, and there still existed directories with previous user (in my case yarn).
  So to solve this, I first had to find the value of the property yarn.nodemanager.local-dirs (with Cloudera use search option to find this property for YARN service, otherwise look into yarn-site.xml in hadoop conf directory), and then delate the files/directories under usercache for all the node manager nodes. In my case, I used:

> rm -rf /yarn/nm/usercache/*
  
  - 问题分析：

    在配置impala基于yarn的完全自由管理，最后发现集群硬件严重不一致，llama项目让impala可以通过yarn申请资源，配置成功后，在执行小的复杂查询时没有任何问题，一旦数据量太大，会出现资源分配的问题，导致无法提供足够资源而报错，impalad mem_limit安装官网也做了限制了，并没有得到解决。最后取消配置，集群一切正常，再提交mapreducer,spark等基于yarn的计算引擎之时，发现各上面错误信息，一个
    任务都无法执行成功。排查问题步骤。
    
    + 1、通过日志信息，确定大概方向。
    + 2、在开源社区各大国外论坛寻找解决方案，未果。
    + 3、排查源码，是什么导致输出次错误信息，发现是因为权限问题无法初始化。
    + 4、首先尝试找到相关yarn临时目录，备份目录后删除cache目录。重新提交任务初始化。
    + 5、整合解决问题时间大概在3个小时。就是一个权限问题。
      
      * 配置基于yarn完全资源管理后权限：
      ```
      $ ls -l /data01/yarn/nm/usercache/
        total 1
        drwxr-s--- 4 nobody yarn 4096 Feb 24 00:19 hadoop
      ```
      * 未配置基于yarn完全资源管理权限：
      ```
      $ ls -l /data01/yarn/nm/usercache/
      total 1
      drwxr-x--- 4 yarn yarn 4096 Mar 17 11:33 hadoop
      ```

    找到：yarn.nodemanager.local-dirs ，删除这个路径下面的
    usercache目录中的所有文件包括目录，即可解决。

# 问题2：Container xxx is running beyond physical memory limits

  - 日志：
  ```
  Container [pid=134663,containerID=container_1430287094897_0049_02_067966] is running beyond physical memory limits. Current usage: 1.0 GB of 1 GB physical memory used; 1.5 GB of 10 GB virtual memory used. Killing container. Dump of the process-tree for
  ```

  - 问题分析：
  从日志可以看出，container使用内存超过虚拟内存的限制，导致如上问题。默认2.1；
  NodeManager端设置，类似系统层面的overcommit问题,需要调节yarn.nodemanager.vmem-pmem-ratio相关参数，在yarn-site.xml修改:
  ```
   <property>
    <name>yarn.nodemanager.vmem-pmem-ratio</name>
        <value>10</value>
    </property>
    –或者yarn.nodemanager.vmem-check-enabled，false掉 
    <property>
        <name>yarn.nodemanager.vmem-check-enabled</name>
        <value>false</value>
    </property>
  ```

# 问题3：jvm系常见java heap space
  - 日志
  ```
  xxx java heap space/ java heap space xxx 各种oom信息
  ```

  - 问题分析
  ```
  通过日志定位问题，一般调节参数思路，相关mem,heap设置参数：
    -内存：mapreduce.map.memory.mb
    –Heap Size：-Xmx在mapreduce.map.java.opts做相同调整
    –内存：mapreduce.reduce.memory.mb
    –Heap Size：-Xmx在mapreduce.reduce.java.opts做相同调整
  ```

  - yarn资源管理&&优化参考如下文章
    + [yarn-resources-manager-allocation](https://jikelab.github.io/tech-labs/2015/07/24/yarn-resources-manager-allocation/)

# 问题4: llama on yarn使用问题
  - 日志
  ```
  ERROR:  com.cloudera.llama.util.LlamaException: RESERVATION_ASKING_MORE_MB - Reservation '44590e9da89d8e3:a5ba70d7dcb599a3', expansion 'null' is asking for more memory in mb '129008' than capacity '76800' on node 'bigdata-server-04'., com.cloudera.llama.util.LlamaException: RESERVATION_ASKING_MORE_MB - Reservation '44590e9da89d8e3:a5ba70d7dcb599a3', expansion 'null' is asking for more memory in mb '129008' than capacity '76800' on node 'server-04'.,        at com.cloudera.llama.am.impl.ExpansionReservationsLlamaAM.checkAndUpdateCapacity(ExpansionReservationsLlamaAM.java:170),       at com.cloudera.llama.am.impl.ExpansionReservationsLlamaAM.reserve(ExpansionReservationsLlamaAM.java:129),     at com.cloudera.llama.am.impl.APIContractLlamaAM.reserve(APIContractLlamaAM.java:144),         at com.cloudera.llama.am.LlamaAMServiceImpl.Reserve(LlamaAMServiceImpl.java:132),       at com.cloudera.llama.am.MetricLlamaAMService.Reserve(MetricLlamaAMService.java:140),  at com.cloudera.llama.thrift.LlamaAMService$Processor$Reserve.getResult(LlamaAMService.java:512),      at com.cloudera.llama.thrift.LlamaAMService$Processor$Reserve.getResult(LlamaAMService.java:497),       at org.apache.thrift.ProcessFunction.process(ProcessFunction.java:39),         at org.apache.thrift.TBaseProcessor.process(TBaseProcessor.java:39),    at org.apache.thrift.server.TThreadPoolServer$WorkerProcess.run(TThreadPoolServer.java:206),   at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1145),    at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:615),     at java.lang.Thread.run(Thread.java:745)
  WARNING: The following tables are missing relevant table and/or column statistics.
  bigdata.terminal_all
  ```

  - 分析问题
  ```
  根据错误日志，去cloudera官网blog各种翻文档，查看相关内存配置参数和限制，集群硬件mem严重不一致，在资源评估分配的时候，impalad分别在这些不同配置mem的节点，
  根据官网说法mem_limit也做了限制，依然无法解决。impalad申请内存是非常夸张的方式，如下参数mem调整。
  
  ==> Impala Daemon 内存限制，mem_limit，impalad内存设置导致问题：导致的问题如下，需要限制impalad
  内存使用，注意如果一个集群有多种不同硬件配置
  yarn.nodemanager.resource.memory-mb这个参数注意限制。

  单表数据量太大，虽然做了各种限制，但是依然会报错，未解决，还不够成熟和yarn集成，取消llama配置，独立部署模式就可以了，一模一样的SQL可以执行成功，我无言以对。
  ```

  - 问题小结
  
  问题原因：由于集群中，上中下有三种配置服务器，内存在65-128g，128-256g都有，而hdfs，impala,hbase,yarn,sparkstreaming，prestodb都分布在这些节点上面，impalad是必须和datanode在一个节点，这就涉及到资源分配问题。通过简单对集群角色3组，不同组角色在不同硬件资源，mem,cpu,磁盘有不同的三套配置。llama项目使得impala资源分配交给Yarn。在这样资源严重不一致情况下。llama评估资源在某些节点实际资源就不和大环境统一，从而出现问题。
  
  解决问题方案：尽快引用hadoop 2.7+版本提高的基于标签调度策略，可以给集群不同
  nodemanager节点打标签，提交任务的时候可以指定什么类型应用提交到那些节点执行，
  从而在同一个集群中实现异构集群的思路。YARN某些资源池下面拥有某些高性能高配置
  服务器，某些低性能低配置在一个资源池，某些不上不下配置的服务器，同时拥有高性能标签，低性能标签。调度的时候，会同时存在不同的技术引擎的任务；比如：内存计算代表:spark,tez,impala,drill,presto，磁盘计算：mr,hive,pig,mahout，流计算：sparkstreaming,storm。不同任务指定到不同的资源池。达到基于YARN的统一资源管理和调度。

# 问题5：升级Namenode HA出现Hive metadata信息访问hdfs问题
  - 日志：
  ```
  he.hadoop.mapreduce.TaskCounter instead
  2015-06-20 16:28:54,901 ERROR [main]: exec.Task (SessionState.java:printError(545)) - Failed with exception Wrong FS: hdfs://server-01:8020/apps/hive/temp/temp_base, expected: hdfs://mycluster
  java.lang.IllegalArgumentException: Wrong FS: hdfs://server-01:8020/apps/hive/temp/temp_base, expected: hdfs://mycluster
        at org.apache.hadoop.fs.FileSystem.checkPath(FileSystem.java:642)
        at org.apache.hadoop.hdfs.DistributedFileSystem.getPathName(DistributedFileSystem.java:181)

  ```

  - 分析问题：
  ```
  升级HA之后hive源数据信息hdfs地址问题，排查hive元数据信息发现，原来是hdfs路径
  原来时某个节点非HA的地址，升级namenode为HA之后，地址并没有跟着变化，需要手动
  修改hive 元数据信息比如存储在mysql中hdfs路径信息为HA的地址，可以解决。
  ```

# 问题6：HDFS ERROR - Failed to close inode 330916
 - 日志：
 ```
 HDFS报错: Failed to close inode 330916
 16/03/15 23:19:17 INFO util.HiveUtil: Run Hive Sql:MSCK REPAIR TABLE TB_INTERF_KW_TEMP
  16/03/15 23:19:18 ERROR hdfs.DFSClient: Failed to close inode 330916
  org.apache.hadoop.ipc.RemoteException(org.apache.hadoop.hdfs.server.namenode.LeaseExpiredException): No lease on /tmp/abc/data/dictionary/KwTemp.txt (inode 330916): File does not exist. Holder DFSClient_NONMAPREDUCE_-1085844490_1 does not have any open files.
 ```

 - 分析问题：
 ```
 程序使用HDFS api操作的时候，在mr中操作，判断一个目录是否存在，而导致的问题，总之是API和集群沟通问题。
 ```

# 问题7: 根目录空间利用率100%，导致namenode进入安全模式
  
  最初报错信息如下：
  ```
  Caused by: org.apache.hadoop.ipc.RemoteException(org.apache.hadoop.hdfs.server.namenode.SafeModeException): Cannot create directory /tmp/hive/root/e5e52596-727b-414d-a02a-b78aeb44109d. Name node is in safe mode.
  Resources are low on NN. Please add or free up more resources then turn off safe mode manually. NOTE:  If you turn off safe mode before adding resources, the NN will immediately return to safe mode. Use "hdfs dfsadmin -safemode leave" to turn safe mode off.
  ```

1、进入超级用户，尝试让hdfs退出安全模式。
```
[root@bigdata-server-1 ~]# su - hdfs
Last login: Tue Jun 14 22:06:06 EDT 2016 on pts/0
[hdfs@bigdata-server-1 ~]$ hdfs dfsadmin -safemode leave
OpenJDK 64-Bit Server VM warning: Insufficient space for shared memory file:
   12493
Try using the -Djava.io.tmpdir= option to select an alternate temp location.

Safe mode is OFF
```

2、发现报错，从信息看是空间问题，往下看，尝试之行进入hive客户端,发现如下错误。
```
[hdfs@bigdata-server-1 ~]$ hive
OpenJDK 64-Bit Server VM warning: Insufficient space for shared memory file:
   12570
Try using the -Djava.io.tmpdir= option to select an alternate temp location.

SLF4J: Class path contains multiple SLF4J bindings.
SLF4J: See http://www.slf4j.org/codes.html#multiple_bindings for an explanation.
SLF4J: Actual binding is of type [org.slf4j.impl.Log4jLoggerFactory]
OpenJDK 64-Bit Server VM warning: Insufficient space for shared memory file:
   12550
Try using the -Djava.io.tmpdir= option to select an alternate temp location.

Exception in thread "main" java.io.IOException: Mkdirs failed to create /tmp/hadoop-unjar2180896952508096842
        at org.apache.hadoop.util.RunJar.ensureDirectory(RunJar.java:129)
        at org.apache.hadoop.util.RunJar.run(RunJar.java:198)
        at org.apache.hadoop.util.RunJar.main(RunJar.java:136)
```

3、判断为空间不足，“df -h”验证一下,果然根目录100%了，清理文件，启动down掉服务，退出安全模式，即可
```
[hdfs@bigdata-server-1 ~]$ df -h
Filesystem                Size  Used Avail Use% Mounted on
/dev/mapper/asianux-root   44G   42G     0 100% /
devtmpfs                  3.7G     0  3.7G   0% /dev
tmpfs                     3.8G     0  3.8G   0% /dev/shm

[hdfs@bigdata-server-1 ~]$ hdfs dfsadmin -safemode leave
[hdfs@bigdata-server-1 ~]$ hdfs dfsadmin -safemode get 
Safe mode is OFF
```

4、总结
  造成这样问题的原因，归根结底是因为对集群的监控不到位，比如：服务器监控报警，可以用zabbix／ganglia/nagios来做，未做的原因是因为他是测试环境，不过这个也是不可原谅的错误了。一定要注意监控集群的健康状况，才能避免这样的低级错误。

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/