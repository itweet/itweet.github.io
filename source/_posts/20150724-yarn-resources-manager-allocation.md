---
title: yarn-resources-manager-allocation
date: 2015-07-24 18:49:18
description: Hadoop YARN同时支持内存和CPU两种资源的调度（默认只支持内存，如果想进一步调度CPU，需要自己进行一些配置），本文将介绍YARN是如何对这些资源进行调度和隔离的。
category: BigData
tags: YARN
---

Hadoop YARN同时支持内存和CPU两种资源的调度（默认只支持内存，如果想进一步调度CPU，需要自己进行一些配置），本文将介绍YARN是如何对这些资源进行调度和隔离的。
在YARN中，资源管理由ResourceManager和NodeManager共同完成，其中，ResourceManager中的调度器负责资源的分配，而NodeManager则负责资源的供给和隔离。ResourceManager将某个NodeManager上资源分配给任务（这就是所谓的“资源调度”）后，NodeManager需按照要求为任务提供相应的资源，甚至保证这些资源应具有独占性，为任务运行提供基础的保证，这就是所谓的资源隔离。
  YARN会管理集群中所有机器的可用计算资源. 基于这些资源YARN会调度应用
(比如MapReduce)发来的资源请求,然后YARN会通过分配Container来给每个应用
提供处理能力, Container是YARN中处理能力的基本单元, 是对内存, CPU等的封装.

日志：

    Container [pid=134663,containerID=container_1430287094897_0049_02_067966] is running beyond physical memory limits. Current usage: 1.0 GB of 1 GB physical memory used; 1.5 GB of 10 GB virtual memory used. Killing container. Dump of the process-tree for


    Error: Java heap space

问题1：Container  xxx is running beyond physical memory limits
问题2：java heap space


# 优化原则
```
--调节参数列表
 
 • Yarn 
   - nodemanager:
     > CPU：yarn.nodemanager.resource.cpu-vcores = 8
     > 内存：yarn.nodemanager.resource.memory-mb = 8G
   - resourcermanager
     > 资源分配尽量与NodeManager端保持一致

 • Map Tasks:
    > mapreduce.map.memory.mb=2240   # Container size
    > mapreduce.map.java.opts=-Xmx2016m  # JVM arguments for a Map task;mapreduce.map.memory.mb*0.85
    > mapreduce.map.cpu.vcores=1
 
 • Reduce Tasks:
    > mapreduce.reduce.memory.mb=2240  # Container size
    > mapreduce.reduce.java.opts=-Xmx2016m  # JVM arguments for a Reduce task;mapreduce.map.memory.mb*0.85
    > mapreduce.reduce.cpu.vcores=1
 
 • MapReduce Application Master   
    > yarn.app.mapreduce.am.resource.mb=2240  # Container size
    > yarn.app.mapreduce.am.command-opts=-Xmx2016m  # JVM arguments for an Application Master
    > yarn.app.mapreduce.am.resource.cpu-vcores=1
 
 • Trouble Shooting
    > yarn.nodemanager.vmem-pmem-ratio
    > yarn.nodemanager.vmem-check-enabled

 • Client 
    > mapreduce.job.reduces = (节点数 * reduce slot数) 的倍数
    
    > mapreduce.client.submit.file.replication
    
    > 编码
      -  mapreduce.output.fileoutputformat.compress.codec
      -  mapreduce.map.output.compress.codec
      -  mapreduce.output.fileoutputformat.compress.type
        * org.apache.hadoop.io.compress.DefaultCodec
        * org.apache.hadoop.io.compress.SnappyCodec  #最佳选择
        * org.apache.hadoop.io.compress.BZip2Codec / GzipCodec #压缩比例最高，但是耗时
        
    > io.sort
      - mapreduce.task.io.sort.factor
      - mapreduce.task.io.sort.mb 
    
    > mapreduce.map.sort.spill.percent 
    
    > mapreduce.reduce.shuffle.parallelcopies
    
    > Other：io.file.buffer.szie SequenceFiles(目前比较少用，都用rcfile,parquet,orcfile)

--Yarn参数调节,根据实际硬件环境分配,后面有案例
[root@server1 ~]# python yarn-utils.py -c 32 -m 128 -d 11 -k False
 Using cores=32 memory=128GB disks=11 hbase=False
 Profile: cores=32 memory=106496MB reserved=24GB usableMem=104GB disks=11
 Num Container=20
 Container Ram=5120MB
 Used Ram=100GB
 Unused Ram=24GB
 yarn.scheduler.minimum-allocation-mb=5120
 yarn.scheduler.maximum-allocation-mb=102400
 yarn.nodemanager.resource.memory-mb=102400
 mapreduce.map.memory.mb=5120
 mapreduce.map.java.opts=-Xmx4096m
 mapreduce.reduce.memory.mb=5120
 mapreduce.reduce.java.opts=-Xmx4096m
 yarn.app.mapreduce.am.resource.mb=5120
 yarn.app.mapreduce.am.command-opts=-Xmx4096m
 mapreduce.task.io.sort.mb=2048

[root@server1 ~]# python yarn-utils.py -c 32 -m 128 -d 11 -k False
 Using cores=32 memory=128GB disks=11 hbase=False
 Profile: cores=32 memory=106496MB reserved=24GB usableMem=104GB disks=11
 Num Container=20
 Container Ram=5120MB
 Used Ram=100GB
 Unused Ram=24GB
 yarn.scheduler.minimum-allocation-mb=5120
 yarn.scheduler.maximum-allocation-mb=102400
 yarn.nodemanager.resource.memory-mb=102400
 mapreduce.map.memory.mb=5120
 mapreduce.map.java.opts=-Xmx4096m
 mapreduce.reduce.memory.mb=5120
 mapreduce.reduce.java.opts=-Xmx4096m
 yarn.app.mapreduce.am.resource.mb=5120
 yarn.app.mapreduce.am.command-opts=-Xmx4096m
 mapreduce.task.io.sort.mb=2048

--参数含义：
Option            Description
   -c CORES    The number of cores on each host.
   -m MEMORY   The amount of memory on each host in GB.
   -d DISKS    The number of disks on each host.
   -k HBASE    "True" if HBase is installed, "False" if not.

-- YARN以及MAPREDUCE所有可用的内存资源应该要除去系统运行需要的以及其他的hadoop的一些程序，总共保留的内存=系统内存+HBASE内存。

服务器总内存    系统需要内存     HBase需要内存
4GB               1GB             1GB
8GB               2GB             1GB
16GB              2GB             2GB
24GB              4GB             4GB
48GB              6GB             8GB
64GB              8GB             8GB
72GB              8GB             8GB
96GB              12GB            16GB
128GB             24GB            24GB
255GB             32GB            32GB
512GB             64GB            64GB
```

# 优化前：
 yarn.nodemanager.resource.memory-mb
    8GB
 yarn.nodemanager.resource.cpu-vcores   
    32core

    pre Mapper 
    CPU:1   [mapreduce.map.cpu.vcores ]
    MEM:1G  [mapreduce.map.memory.mb ]
    ===> 8 map slot / node

    pre Reducer
    CPU:1   [mapreduce.reduce.cpu.vcores]
    MEM:1G  [mapreduce.reduce.memory.mb]
    ===> 8 reduce slot / node 【有8G内存，实际有CPU 32个，所以只能启动8个reduce在每个node上】

* map slot / reduce slot 由nodemanager的内存/CPU core上限与客户
端设置的单mapper， reducer内存/CPU使用值决定
* heapsize（ java.opts中的-Xmx）应根据单mapper， reducer内存进
行调整，而与slot个数无关 => heapsize不能大于memory.mb值，一
般设置为memory.mb的85%左右

# OOM 
  •内存、Heap 
    需要设置：
     -内存：mapreduce.map.memory.mb 
     –Heap Size：-Xmx在mapreduce.map.java.opts做相同调整 
     –内存：mapreduce.reduce.memory.mb 
     –Heap Size：-Xmx在mapreduce.reduce.java.opts做相同调整
    

# Container 超过了虚拟内存的使用限制
– Container XXX is running beyond virtual memory limits 
 • NodeManager端设置，类似系统层面的overcommit问题 
    –yarn.nodemanager.vmem-pmem-ratio 【默认2.1，我们的做法呢【物理内存和虚拟内存比率】值为了15，yarn-site.xml中修改】

        <property>
            <name>yarn.nodemanager.vmem-pmem-ratio</name>
                <value>10</value>
            </property>
        –或者yarn.nodemanager.vmem-check-enabled，false掉 
            <property>
                <name>yarn.nodemanager.vmem-check-enabled</name>
                <value>false</value>
            </property>

# 调优后：
mapreduce.map.java.opts, mapreduce.map.java.opts.max.heap=1.6G       
mapreduce.reduce.java.opts,mapreduce.reduce.java.opts.max.heap=3.3G
注意上面两个参数和下面的mapper,reducer的内存有关系,是下面mem的0.85倍！

yarn.nodemanager.resource.memory-mb=32GB
yarn.nodemanager.resource.cpu-vcores=32core

    pre Mapper 
    CPU:2   [mapreduce.map.cpu.vcores ]
    MEM:2G  [mapreduce.map.memory.mb ]
    ===> 16 map slot / node

    pre Reducer
    CPU:4   [mapreduce.reduce.cpu.vcores]
    MEM:4G  [mapreduce.reduce.memory.mb]
    ==> 8 reduce slot / node

# shuffle.parallelcopies如何计算?
（reduce.shuffle并行执行的副本数,最大线程数–sqrt(节点数* map slot数) 与 (节点数 * map slot数)/2 之间 ==>结果：{12-72}
mapreduce.reduce.shuffle.parallelcopies=68

```
`排序文件时要合并的流的数量。也就是说，在 reducer 端合并排序期间要使用的排序头
数量。此设置决定打开文件句柄数。并行合并更多文件可减少合并排序迭代次数并通过消
除磁盘 I/O 提高运行时间。注意：并行合并更多文件会使用更多的内存。如 'io.sort.
factor' 设置太高或最大 JVM 堆栈设置太低，会产生过多地垃圾回收。Hadoop 默认值为 
10，但 Cloudera 建议使用更高值。将是生成的客户端配置的一部分。`
```
mapreduce.task.io.sort.factor=64

xml配置
yarn.nodemanager.vmem-pmem-ratio=10 # yarn-site.xml 的 YARN 客户端高级配置
mapreduce.task.timeout=1800000


# impala调优
Impala 暂存目录：需要注意此目录磁盘空间问题！最好在单独的一个挂载点！  

## 1、内存
    -服务器端(impalad)
    Mem：default_query_options MEM_LIMIT=128g  

## 2、并发查询
    queue
        .queue_wait_timeout_ms默认只有60s
           - queue_wait_timeout_ms=600000
        .default pool设置

## 3、资源管理  
    -Dynamic Resource Pools
        .并发控制：max running queries

## 4、yarn资源隔离
http://hadoop.apache.org/docs/r2.7.1/hadoop-yarn/hadoop-yarn-site/NodeManagerCgroups.html

参考：http://www.itweet.cn


原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/