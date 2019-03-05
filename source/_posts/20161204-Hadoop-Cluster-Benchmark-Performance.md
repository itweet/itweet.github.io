---
title: Hadoop Cluster Benchmark Performance
date: 2016-12-04 17:08:27
category: BigData
tags: Benchmark
---
# 基础环境

*云主机 4 台*	
	云主机类型名称	m1.xlarge-max
	内存				32GB
	VCPU数量			8 VCPU
	磁盘				50GB

*操作系统版本 CentOS release 6.8 (Final)*

```
uname -a
   Linux bigdata-server-1 2.6.32-642.el6.x86_64 #1 SMP Tue May 10 17:27:01 UTC 2016 x86_64 x86_64 x86_64 GNU/Linux
```

# 命令行安装集群管理服务
```
wget http://archive.cloudera.com/cm5/installer/5.9.0/cloudera-manager-installer.bin

chmod u+x cloudera-manager-installer.bin 

sudo ./cloudera-manager-installer.bin 
```

# 可视化安装集群
集群管理服务安装成功后，会提供访问此admin管理页面：http://192.168.0.46:7180/cmf/login
然后就可以根据提示安装好CDH集群。

* 注意：
	1. 选择存储库，部分可以选择自定义源，这样可以利用离线内部源进行安装集群，效率和安装成功率才能接近99.99%
	2. 集群服务器ntp时间同步，如果不同步，yarn，hbase，zookeeper可能会报错

# HDFS Benchmark Testing
DFSIO是一个标准的HDFS的Benchmark工具，位于test包中。功能简单明了，测试的是读和写的性能指标。Terasort包含三个工具，分别是teragen：用来生成供排序的随机数据；terasort：用来将随机数据排序；teravalidate：校验terasort的排序结果是否正确。

## TestDFSIO write

```
time hadoop jar ./hadoop-mapreduce-client-jobclient.jar TestDFSIO -write -nrFiles 3 -fileSize 2000
```

结果：

```
16/12/04 16:57:18 INFO fs.TestDFSIO: ----- TestDFSIO ----- : write
16/12/04 16:57:18 INFO fs.TestDFSIO:            Date & time: Sun Dec 04 16:57:18 CST 2016
16/12/04 16:57:18 INFO fs.TestDFSIO:        Number of files: 3
16/12/04 16:57:18 INFO fs.TestDFSIO: Total MBytes processed: 6000.0
16/12/04 16:57:18 INFO fs.TestDFSIO:      Throughput mb/sec: 24.702133440924847
16/12/04 16:57:18 INFO fs.TestDFSIO: Average IO rate mb/sec: 24.771690368652344
16/12/04 16:57:18 INFO fs.TestDFSIO:  IO rate std deviation: 1.28838119507988
16/12/04 16:57:18 INFO fs.TestDFSIO:     Test exec time sec: 114.55
16/12/04 16:57:18 INFO fs.TestDFSIO: 

real    1m57.742s
user    0m6.706s
sys 0m0.323s

```

## TestDFSIO read

```
time hadoop jar ./hadoop-mapreduce-client-jobclient.jar TestDFSIO -read -nrFiles 3 -fileSize 2000
```

结果：

```
16/12/04 17:00:11 INFO fs.TestDFSIO: ----- TestDFSIO ----- : read
16/12/04 17:00:11 INFO fs.TestDFSIO:            Date & time: Sun Dec 04 17:00:11 CST 2016
16/12/04 17:00:11 INFO fs.TestDFSIO:        Number of files: 3
16/12/04 17:00:11 INFO fs.TestDFSIO: Total MBytes processed: 6000.0
16/12/04 17:00:11 INFO fs.TestDFSIO:      Throughput mb/sec: 905.2504526252263
16/12/04 17:00:11 INFO fs.TestDFSIO: Average IO rate mb/sec: 905.80126953125
16/12/04 17:00:11 INFO fs.TestDFSIO:  IO rate std deviation: 22.144358549657525
16/12/04 17:00:11 INFO fs.TestDFSIO:     Test exec time sec: 25.189
16/12/04 17:00:11 INFO fs.TestDFSIO: 

real    0m28.377s
user    0m6.108s
sys 0m0.315s
```

清空测试数据：
```
time hadoop jar ./hadoop-mapreduce-client-jobclient.jar TestDFSIO -clean
```

## Namenode benchmark
```
time hadoop jar ./hadoop-mapreduce-client-jobclient.jar nnbench -operation create_write -maps 4 -reduces 4 -blockSize 1 -bytesToWrite 0 -numberOfFiles 100 -replicationFactorPerFile 3 -readFileAfterOpen true -baseDir /benchmarks/NNBench-`hostname -s`
```

结果：

```
16/12/04 17:07:41 INFO hdfs.NNBench: -------------- NNBench -------------- : 
16/12/04 17:07:41 INFO hdfs.NNBench:                                Version: NameNode Benchmark 0.4
16/12/04 17:07:41 INFO hdfs.NNBench:                            Date & time: 2016-12-04 17:07:41,678
16/12/04 17:07:41 INFO hdfs.NNBench: 
16/12/04 17:07:41 INFO hdfs.NNBench:                         Test Operation: create_write
16/12/04 17:07:41 INFO hdfs.NNBench:                             Start time: 2016-12-04 17:07:30,458
16/12/04 17:07:41 INFO hdfs.NNBench:                            Maps to run: 4
16/12/04 17:07:41 INFO hdfs.NNBench:                         Reduces to run: 4
16/12/04 17:07:41 INFO hdfs.NNBench:                     Block Size (bytes): 1
16/12/04 17:07:41 INFO hdfs.NNBench:                         Bytes to write: 0
16/12/04 17:07:41 INFO hdfs.NNBench:                     Bytes per checksum: 1
16/12/04 17:07:41 INFO hdfs.NNBench:                        Number of files: 100
16/12/04 17:07:41 INFO hdfs.NNBench:                     Replication factor: 3
16/12/04 17:07:41 INFO hdfs.NNBench:             Successful file operations: 0
16/12/04 17:07:41 INFO hdfs.NNBench: 
16/12/04 17:07:41 INFO hdfs.NNBench:         # maps that missed the barrier: 0
16/12/04 17:07:41 INFO hdfs.NNBench:                           # exceptions: 0
16/12/04 17:07:41 INFO hdfs.NNBench: 
16/12/04 17:07:41 INFO hdfs.NNBench:                TPS: Create/Write/Close: 0
16/12/04 17:07:41 INFO hdfs.NNBench: Avg exec time (ms): Create/Write/Close: Infinity
16/12/04 17:07:41 INFO hdfs.NNBench:             Avg Lat (ms): Create/Write: NaN
16/12/04 17:07:41 INFO hdfs.NNBench:                    Avg Lat (ms): Close: NaN
16/12/04 17:07:41 INFO hdfs.NNBench: 
16/12/04 17:07:41 INFO hdfs.NNBench:                  RAW DATA: AL Total #1: 0
16/12/04 17:07:41 INFO hdfs.NNBench:                  RAW DATA: AL Total #2: 0
16/12/04 17:07:41 INFO hdfs.NNBench:               RAW DATA: TPS Total (ms): 9458
16/12/04 17:07:41 INFO hdfs.NNBench:        RAW DATA: Longest Map Time (ms): 0.0
16/12/04 17:07:41 INFO hdfs.NNBench:                    RAW DATA: Late maps: 0
16/12/04 17:07:41 INFO hdfs.NNBench:              RAW DATA: # of exceptions: 0
16/12/04 17:07:41 INFO hdfs.NNBench: 

real    2m12.007s
user    0m6.464s
sys 0m0.379s
```

## MapReduce benchmark
```
time hadoop jar ./hadoop-mapreduce-client-jobclient.jar mrbench -numRuns 50
```

结果：
```
DataLines   Maps    Reduces AvgTime (milliseconds)
1       2   1   20059

real    16m45.947s
user    0m16.096s
sys 0m1.674s
```

## Hadoop MapReduce Algorithm Testing
```
TeraGen	time hadoop jar hadoop-mapreduce-examples.jar teragen 500000000 /terasort-input1

TeraSort	time hadoop jar  hadoop-mapreduce-examples.jar terasort /terasort-input1 /terasort-output1

TeraValidate	time hadoop jar hadoop-mapreduce-examples.jar teravalidate /terasort-output1 /terasort-validate1

WordCount	time hadoop jar hadoop-mapreduce-examples.jar wordcount /terasort-input1 /wordcount-output1

Shuffle	time hadoop jar hadoop-mapreduce-examples.jar randomtextwriter
-D mapred.output.compress=false \
-D mapreduce.randomtextwriter.bytespermap=107374182 \
-D mapreduce.randomtextwriter.mapsperhost=2 \
/randomtextwriter_output"
```

# Hbase YCSB Testing
 英文全称：Yahoo! Cloud Serving Benchmark (YCSB) 。是Yahoo公司的一个用来对云服务进行基础测试的工具。目标是促进新一代云数据服务系统的性能比较。为四个广泛使用的系统：Cassandra,、HBase、PNUTS和一个简单的片式MySQL执行，订了套核心基准测试和结果报告。

YCSB的特点：可扩展的，除了很容易对新系统进行基准测试，支持新定义的简单工作量。

## Hbase建表
```
hbase(main):005:0> create 'usertable','family'
```

## 加载数据测试
```
ycsb load hbase10 -P ../workloads/workloada -cp /etc/hbase/conf -p table=usertable -p columnfamily=family -p recordcount=100000 -threads 10
```

结果：

```
[OVERALL], RunTime(ms), 26717.0
[OVERALL], Throughput(ops/sec), 3742.9352097915184
[TOTAL_GCS_PS_Scavenge], Count, 23.0
[TOTAL_GC_TIME_PS_Scavenge], Time(ms), 99.0
[TOTAL_GC_TIME_%_PS_Scavenge], Time(%), 0.37055058576936034
[TOTAL_GCS_PS_MarkSweep], Count, 0.0
[TOTAL_GC_TIME_PS_MarkSweep], Time(ms), 0.0
[TOTAL_GC_TIME_%_PS_MarkSweep], Time(%), 0.0
[TOTAL_GCs], Count, 23.0
[TOTAL_GC_TIME], Time(ms), 99.0
[TOTAL_GC_TIME_%], Time(%), 0.37055058576936034
[CLEANUP], Operations, 20.0
[CLEANUP], AverageLatency(us), 6181.25
[CLEANUP], MinLatency(us), 2.0
[CLEANUP], MaxLatency(us), 123135.0
[CLEANUP], 95thPercentileLatency(us), 420.0
[CLEANUP], 99thPercentileLatency(us), 123135.0
[INSERT], Operations, 100000.0
[INSERT], AverageLatency(us), 2545.76251
[INSERT], MinLatency(us), 1272.0
[INSERT], MaxLatency(us), 286719.0
[INSERT], 95thPercentileLatency(us), 3891.0
[INSERT], 99thPercentileLatency(us), 6143.0
[INSERT], Return=OK, 100000
```

## 执行事物 主要有read 和 update操作
```
./ycsb run hbase10 -P ../workloads/workloada -cp /etc/hbase/conf  -p measurementtype=timeseries -p columnfamily=family -p timeseries.granularity=2000 -p threads=10
```

结果：
```
[OVERALL], RunTime(ms), 4301.0
[OVERALL], Throughput(ops/sec), 232.50406882120438
[TOTAL_GCS_PS_Scavenge], Count, 1.0
[TOTAL_GC_TIME_PS_Scavenge], Time(ms), 17.0
[TOTAL_GC_TIME_%_PS_Scavenge], Time(%), 0.3952569169960474
[TOTAL_GCS_PS_MarkSweep], Count, 0.0
[TOTAL_GC_TIME_PS_MarkSweep], Time(ms), 0.0
[TOTAL_GC_TIME_%_PS_MarkSweep], Time(%), 0.0
[TOTAL_GCs], Count, 1.0
[TOTAL_GC_TIME], Time(ms), 17.0
[TOTAL_GC_TIME_%], Time(%), 0.3952569169960474
[CLEANUP], Operations, 2
[CLEANUP], AverageLatency(us), 58443.5
[CLEANUP], MinLatency(us), 16
[CLEANUP], MaxLatency(us), 116871
[CLEANUP], 0, 58443.5
[READ], Operations, 486
[READ], AverageLatency(us), 2295.1543209876545
[READ], MinLatency(us), 1581
[READ], MaxLatency(us), 21426
[READ], Return=OK, 486
[READ], 0, 2434.181818181818
[READ], 2000, 1968.2
[UPDATE], Operations, 514
[UPDATE], AverageLatency(us), 3591.52140077821
[UPDATE], MinLatency(us), 2473
[UPDATE], MaxLatency(us), 155133
[UPDATE], Return=OK, 514
[UPDATE], 0, 3848.6112759643916
[UPDATE], 2000, 3102.0338983050847
```

# Kafka Performance Testing
Kafka的一个核心特性是高吞吐率，因此本文的测试重点是Kafka的吞吐率。本文的测试共使用4台安装CentOS6.7的虚拟机，3台作为Broker.测试的指标主要是每秒多少兆字节数据，每秒多少条消息。

* $KAFKA_HOME/bin/kafka-producer-perf-test.sh 该脚本被设计用于测试Kafka Producer的性能，主要输出4项指标，总共发送消息量（以MB为单位），每秒发送消息量（MB/second），发送消息总数，每秒发送消息数（records/second）。除了将测试结果输出到标准输出外，该脚本还提供CSV Reporter，即将结果以CSV文件的形式存储，便于在其它分析工具中使用该测试结果

* $KAFKA_HOME/bin/kafka-consumer-perf-test.sh 该脚本用于测试Kafka Consumer的性能，测试指标与Producer性能测试脚本一样

*创建消息队列:*
```
./kafka-topics.sh --create --zookeeper wxb-1:2181,wxb-2:2181,wxb-3:2181 --replication-factor 3 --partitions 1 --topic itweet
Created topic "itweet".
```

*测试：kafka-producer-perf-test.sh*

*Demo*
```
./kafka-producer-perf-test.sh --topic test1 --num-records 100 --record-size 500 --throughput -1 --producer-props bootstrap.servers=127.0.0.1:9092 acks=0 buffer.memory=33554432 compression.type=gzip batch.size=10240 linger.ms=10

./kafka-producer-perf-test.sh --topic test1 --num-records 100 --record-size 5 --throughput -1 --producer-props bootstrap.servers=127.0.0.1:9092
```

```
./kafka-producer-perf-test.sh --topic itweet  --num-records 100000 --record-size 300000 --throughput -1  --producer-props bootstrap.servers=127.0.0.1:9092
```
产生消息队列，产生了100000条，每条大小为300kB;产生了100000个消息，每秒产生135.132579个消息，每秒产生的消息总大小为38.66 MB，平均延迟时间为827.39 ms，最大延迟时间为827.39 ms!

*测试：kafka-consumer-perf-test.sh*

*Demo*
```
./kafka-consumer-perf-test.sh --topic test1 --broker-list wxb-1,wxb-2,wxb-3 --messages 1000 --zookeeper localhost:2181 --threads 10
```

```
./kafka-consumer-perf-test.sh --topic itweet --broker-list wxb-1,wxb-2,wxb-3 --messages 100000 --zookeeper wxb-1,wxb-2,wxb-3 --threads 12
```
2016-12-21 14:55:54开始，2016-12-21 14:57:32结束，98s的消费时间（计算值）
消息队列的大小总数为28610.2295MB，每秒消费的消息大小为293.7637MB
消息队列的消息总数为100000条，每秒消费的消息个数为1026.7784个。

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/


参考：http://www.itweet.cn/2015/03/20/Hadoop-benchmarks/
     http://blog.cloudera.com/blog/category/performance/page/2/
     https://github.com/brianfrankcooper/YCSB/wiki/Getting-Started
     https://github.com/brianfrankcooper/YCSB/wiki/Running-a-Workload
     https://github.com/databricks/spark-sql-perf
     http://blog.cloudera.com/blog/2015/08/ycsb-the-open-standard-for-nosql-benchmarking-joins-cloudera-labs/
    http://blog.cloudera.com/blog/2016/11/ycsb-0-10-0-now-in-cloudera-labs/
    https://github.com/brianfrankcooper/YCSB/wiki/Running-a-Workload