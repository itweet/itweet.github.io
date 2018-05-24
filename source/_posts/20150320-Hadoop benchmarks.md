---
title: Hadoop benchmarks
date: 2015-03-20 17:07:09
category: BigData
tags: Benchmarks
---
# 一. Hadoop基准测试
## Hadoop自带了几个基准测试，被打包在几个jar包中。本文主要是cloudera版本测试
```	
	[hsu@server01 ~]$ ls /opt/cloudera/parcels/CDH-5.2.0-1.cdh5.2.0.p0.36/lib/hadoop-0.20-mapreduce/hadoop* | egrep "examples|test"
	/opt/cloudera/parcels/CDH-5.2.0-1.cdh5.2.0.p0.36/lib/hadoop-0.20-mapreduce/hadoop-examples-2.5.0-mr1-cdh5.2.0.jar
	/opt/cloudera/parcels/CDH-5.2.0-1.cdh5.2.0.p0.36/lib/hadoop-0.20-mapreduce/hadoop-examples.jar
	/opt/cloudera/parcels/CDH-5.2.0-1.cdh5.2.0.p0.36/lib/hadoop-0.20-mapreduce/hadoop-test-2.5.0-mr1-cdh5.2.0.jar
	/opt/cloudera/parcels/CDH-5.2.0-1.cdh5.2.0.p0.36/lib/hadoop-0.20-mapreduce/hadoop-test.jar
```

### (1)、Hadoop Test
#### 当不带参数调用hadoop-test-0.20.2-cdh3u3.jar时，会列出所有的测试程序：
```	  
	  [hsu@server01 ~]$ sudo hadoop jar /opt/cloudera/parcels/CDH-5.2.0-1.cdh5.2.0.p0.36/lib/hadoop-0.20-mapreduce/hadoop-test.jar 
	  An example program must be given as the first argument.
	  Valid program names are:
	  DFSCIOTest: Distributed i/o benchmark of libhdfs.
	  DistributedFSCheck: Distributed checkup of the file system consistency.
	  MRReliabilityTest: A program that tests the reliability of the MR framework by injecting faults/failures
	  TestDFSIO: Distributed i/o benchmark.
	  dfsthroughput: measure hdfs throughput
	  filebench: Benchmark SequenceFile(Input|Output)Format (block,record compressed and uncompressed), Text(Input|Output)Format (compressed and uncompressed)
	  loadgen: Generic map/reduce load generator
	  mapredtest: A map/reduce test check.
	  minicluster: Single process HDFS and MR cluster.
	  mrbench: A map/reduce benchmark that can create many small jobs
	  nnbench: A benchmark that stresses the namenode.
	  testarrayfile: A test for flat files of binary key/value pairs.
	  testbigmapoutput: A map/reduce program that works on a very big non-splittable file and does identity map/reduce
	  testfilesystem: A test for FileSystem read/write.
	  testmapredsort: A map/reduce program that validates the map-reduce framework's sort.
	  testrpc: A test for rpc.
	  testsequencefile: A test for flat files of binary key value pairs.
	  testsequencefileinputformat: A test for sequence file input format.
	  testsetfile: A test for flat files of binary key/value pairs.
	  testtextinputformat: A test for text input format.
	  threadedmapbench: A map/reduce benchmark that compares the performance of maps with multiple spills over maps with 1 spill

      == 这些程序从多个角度对Hadoop进行测试，TestDFSIO、mrbench和nnbench是三个广泛被使用的测试。
```
	
### (2) TestDFSIO write

#### TestDFSIO用于测试HDFS的IO性能，使用一个MapReduce作业来并发地执行读写操作，每个map任务用于读或写每个文件，map的输出用于收集与处理文件相关的统计信息，reduce用于累积统计信息，并产生summary。TestDFSIO的用法如下：
```		
		TestDFSIO
		Usage: TestDFSIO [genericOptions] -read | -write | -append | -clean [-nrFiles N] [-fileSize Size[B|KB|MB|GB|TB]] [-resFile resultFileName] [-bufferSize Bytes] [-rootDir]
```

#### 以下的例子将往HDFS中写入10个1000MB的文件：
```		
		[hsu@server01 ~]$ sudo hadoop jar /opt/cloudera/parcels/CDH-5.2.0-1.cdh5.2.0.p0.36/lib/hadoop-0.20-mapreduce/hadoop-test.jar TestDFSIO -write -nrFiles 10 -fileSize 1000
		15/01/13 15:14:17 INFO fs.TestDFSIO: TestDFSIO.1.7
		15/01/13 15:14:17 INFO fs.TestDFSIO: nrFiles = 10
		15/01/13 15:14:17 INFO fs.TestDFSIO: nrBytes (MB) = 1000.0
		15/01/13 15:14:17 INFO fs.TestDFSIO: bufferSize = 1000000
		15/01/13 15:14:17 INFO fs.TestDFSIO: baseDir = /benchmarks/TestDFSIO
		15/01/13 15:14:18 INFO fs.TestDFSIO: creating control file: 1048576000 bytes, 10 files
		15/01/13 15:14:19 INFO fs.TestDFSIO: created control files for: 10 files
		15/01/13 15:15:23 INFO fs.TestDFSIO: ----- TestDFSIO ----- : write
		15/01/13 15:15:23 INFO fs.TestDFSIO:            Date & time: Tue Jan 13 15:15:23 CST 2015
		15/01/13 15:15:23 INFO fs.TestDFSIO:        Number of files: 10
		15/01/13 15:15:23 INFO fs.TestDFSIO: Total MBytes processed: 10000.0
		15/01/13 15:15:23 INFO fs.TestDFSIO:      Throughput mb/sec: 29.67623230554649
		15/01/13 15:15:23 INFO fs.TestDFSIO: Average IO rate mb/sec: 29.899526596069336
		15/01/13 15:15:23 INFO fs.TestDFSIO:  IO rate std deviation: 2.6268824639446526
		15/01/13 15:15:23 INFO fs.TestDFSIO:     Test exec time sec: 64.203
		15/01/13 15:15:23 INFO fs.TestDFSIO: 
```

### (3) TestDFSIO read
#### 以下的例子将从HDFS中读取10个1000MB的文件：

```		
		[hsu@server01 ~]$ sudo hadoop jar /opt/cloudera/parcels/CDH-5.2.0-1.cdh5.2.0.p0.36/lib/hadoop-0.20-mapreduce/hadoop-test.jar TestDFSIO -read -nrFiles 10 -fileSize 1000
		15/01/13 15:42:35 INFO fs.TestDFSIO: TestDFSIO.1.7
		15/01/13 15:42:35 INFO fs.TestDFSIO: nrFiles = 10
		15/01/13 15:42:35 INFO fs.TestDFSIO: nrBytes (MB) = 1000.0
		15/01/13 15:42:35 INFO fs.TestDFSIO: bufferSize = 1000000
		15/01/13 15:42:35 INFO fs.TestDFSIO: baseDir = /benchmarks/TestDFSIO
		15/01/13 15:42:36 INFO fs.TestDFSIO: creating control file: 1048576000 bytes, 10 files
		15/01/13 15:42:37 INFO fs.TestDFSIO: created control files for: 10 files
```

### (4) 清空测试数据

```		
		[hsu@server01 ~]$ sudo hadoop jar /opt/cloudera/parcels/CDH-5.2.0-1.cdh5.2.0.p0.36/lib/hadoop-0.20-mapreduce/hadoop-test.jar TestDFSIO -clean
		15/01/13 15:46:51 INFO fs.TestDFSIO: TestDFSIO.1.7
		15/01/13 15:46:51 INFO fs.TestDFSIO: nrFiles = 1
		15/01/13 15:46:51 INFO fs.TestDFSIO: nrBytes (MB) = 1.0
		15/01/13 15:46:51 INFO fs.TestDFSIO: bufferSize = 1000000
		15/01/13 15:46:51 INFO fs.TestDFSIO: baseDir = /benchmarks/TestDFSIO
		15/01/13 15:46:52 INFO fs.TestDFSIO: Cleaning up test files
```

### (4) nnbench测试[NameNode benchmark (nnbench)]

#### nnbench用于测试NameNode的负载，它会生成很多与HDFS相关的请求，给NameNode施加较大的压力。这个测试能在HDFS上模拟创建、读取、重命名和删除文件等操作。nnbench的用法如下：

##### 以下例子使用12个mapper和6个reducer来创建1000个文件：
```		
		[hsu@server01 ~]$ sudo hadoop jar /opt/cloudera/parcels/CDH-5.2.0-1.cdh5.2.0.p0.36/lib/hadoop-0.20-mapreduce/hadoop-test.jar nnbench -operation create_write -maps 12 -reduces 6 -blockSize 1 -bytesToWrite 0 -numberOfFiles 1000 -replicationFactorPerFile 3 -readFileAfterOpen true -baseDir /benchmarks/NNBench-`hostname -s`
		NameNode Benchmark 0.4
		15/01/13 15:53:33 INFO hdfs.NNBench: Test Inputs: 
		15/01/13 15:53:33 INFO hdfs.NNBench:            Test Operation: create_write
		15/01/13 15:53:33 INFO hdfs.NNBench:                Start time: 2015-01-13 15:55:33,585
		15/01/13 15:53:33 INFO hdfs.NNBench:            Number of maps: 12
		15/01/13 15:53:33 INFO hdfs.NNBench:         Number of reduces: 6
		15/01/13 15:53:33 INFO hdfs.NNBench:                Block Size: 1
		15/01/13 15:53:33 INFO hdfs.NNBench:            Bytes to write: 0
		15/01/13 15:53:33 INFO hdfs.NNBench:        Bytes per checksum: 1
		15/01/13 15:53:33 INFO hdfs.NNBench:           Number of files: 1000
		15/01/13 15:53:33 INFO hdfs.NNBench:        Replication factor: 3
		15/01/13 15:53:33 INFO hdfs.NNBench:                  Base dir: /benchmarks/NNBench-server01
		15/01/13 15:53:33 INFO hdfs.NNBench:      Read file after open: true
		15/01/13 15:53:34 INFO hdfs.NNBench: Deleting data directory
		15/01/13 15:53:34 INFO hdfs.NNBench: Creating 12 control files

		15/01/13 15:56:06 INFO hdfs.NNBench: -------------- NNBench -------------- : 
		15/01/13 15:56:06 INFO hdfs.NNBench:                                Version: NameNode Benchmark 0.4
		15/01/13 15:56:06 INFO hdfs.NNBench:                            Date & time: 2015-01-13 15:56:06,539
		15/01/13 15:56:06 INFO hdfs.NNBench: 
		15/01/13 15:56:06 INFO hdfs.NNBench:                         Test Operation: create_write
		15/01/13 15:56:06 INFO hdfs.NNBench:                             Start time: 2015-01-13 15:55:33,585
		15/01/13 15:56:06 INFO hdfs.NNBench:                            Maps to run: 12
		15/01/13 15:56:06 INFO hdfs.NNBench:                         Reduces to run: 6
		15/01/13 15:56:06 INFO hdfs.NNBench:                     Block Size (bytes): 1
		15/01/13 15:56:06 INFO hdfs.NNBench:                         Bytes to write: 0
		15/01/13 15:56:06 INFO hdfs.NNBench:                     Bytes per checksum: 1
		15/01/13 15:56:06 INFO hdfs.NNBench:                        Number of files: 1000
		15/01/13 15:56:06 INFO hdfs.NNBench:                     Replication factor: 3
		15/01/13 15:56:06 INFO hdfs.NNBench:             Successful file operations: 0
		15/01/13 15:56:06 INFO hdfs.NNBench: 
		15/01/13 15:56:06 INFO hdfs.NNBench:         # maps that missed the barrier: 0
		15/01/13 15:56:06 INFO hdfs.NNBench:                           # exceptions: 0
		15/01/13 15:56:06 INFO hdfs.NNBench: 
		15/01/13 15:56:06 INFO hdfs.NNBench:                TPS: Create/Write/Close: 0
		15/01/13 15:56:06 INFO hdfs.NNBench: Avg exec time (ms): Create/Write/Close: 0.0
		15/01/13 15:56:06 INFO hdfs.NNBench:             Avg Lat (ms): Create/Write: NaN
		15/01/13 15:56:06 INFO hdfs.NNBench:                    Avg Lat (ms): Close: NaN
		15/01/13 15:56:06 INFO hdfs.NNBench: 
		15/01/13 15:56:06 INFO hdfs.NNBench:                  RAW DATA: AL Total #1: 0
		15/01/13 15:56:06 INFO hdfs.NNBench:                  RAW DATA: AL Total #2: 0
		15/01/13 15:56:06 INFO hdfs.NNBench:               RAW DATA: TPS Total (ms): 0
		15/01/13 15:56:06 INFO hdfs.NNBench:        RAW DATA: Longest Map Time (ms): 0.0
		15/01/13 15:56:06 INFO hdfs.NNBench:                    RAW DATA: Late maps: 0
		15/01/13 15:56:06 INFO hdfs.NNBench:              RAW DATA: # of exceptions: 0
		15/01/13 15:56:06 INFO hdfs.NNBench: 
```

### (5) mrbench测试[MapReduce benchmark (mrbench)]

#### mrbench会多次重复执行一个小作业，用于检查在机群上小作业的运行是否可重复以及运行是否高效。mrbench的用法如下：

```		
		[hsu@server01 ~]$ sudo hadoop jar /opt/cloudera/parcels/CDH-5.2.0-1.cdh5.2.0.p0.36/lib/hadoop-0.20-mapreduce/hadoop-test.jar mrbench --help
		MRBenchmark.0.0.2
		Usage: mrbench [-baseDir <base DFS path for output/input, default is /benchmarks/MRBench>] [-jar <local path to job jar file containing Mapper and Reducer implementations, default is current jar file>] [-numRuns <number of times to run the job, default is 1>] [-maps <number of maps for each run, default is 2>] [-reduces <number of reduces for each run, default is 1>] [-inputLines <number of input lines to generate, default is 1>] [-inputType <type of input to generate, one of ascending (default), descending, random>] [-verbose]
```

#### 以下例子会运行一个小作业50次：
```		
		[hsu@server01 ~]$ sudo hadoop jar /opt/cloudera/parcels/CDH-5.2.0-1.cdh5.2.0.p0.36/lib/hadoop-0.20-mapreduce/hadoop-test.jar mrbench -numRuns 50
		MRBenchmark.0.0.2
		15/01/13 16:17:19 INFO mapred.MRBench: creating control file: 1 numLines, ASCENDING sortOrder
		15/01/13 16:17:20 INFO mapred.MRBench: created control file: /benchmarks/MRBench/mr_input/input_331064064.txt
		15/01/13 16:17:20 INFO mapred.MRBench: Running job 0: input=hdfs://server01:8020/benchmarks/MRBench/mr_input output=hdfs://server01:8020/benchmarks/MRBench/mr_output/output_556018847

		DataLines       Maps    Reduces AvgTime (milliseconds)
		1               2       1       26748
```
以上结果表示平均作业完成时间是26秒。

#### 以下例子会运行一个小作业500次：
```		
		[hsu@server01 ~]$ sudo hadoop jar /opt/cloudera/parcels/CDH-5.2.0-1.cdh5.2.0.p0.36/lib/hadoop-0.20-mapreduce/hadoop-test.jar mrbench -numRuns 500 -maps 20 -reduces 10 -inputLines 50 -verbose
		MRBenchmark.0.0.2
		15/01/14 10:43:53 INFO mapred.MRBench: creating control file: 1 numLines, ASCENDING sortOrder
		15/01/14 10:43:54 INFO mapred.MRBench: created control file: /benchmarks/MRBench/mr_input/input_-1773312505.txt
		15/01/14 10:43:54 INFO mapred.MRBench: Running job 0: input=hdfs://server01:8020/benchmarks/MRBench/mr_input output=hdfs://server01:8020/benchmarks/MRBench/mr_output/output_-447811996
		15/01/14 10:43:54 INFO client.RMProxy: Connecting to ResourceManager at server01/135.33.5.53:8032
		15/01/14 10:43:54 INFO client.RMProxy: Connecting to ResourceManager at server01/135.33.5.53:8032
		15/01/14 10:43:54 INFO mapred.FileInputFormat: Total input paths to process : 1
		15/01/14 10:43:55 INFO mapreduce.JobSubmitter: number of splits:2
		15/01/14 10:43:55 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1420542591388_0112
		15/01/14 10:43:55 INFO impl.YarnClientImpl: Submitted application application_1420542591388_0112
		15/01/14 10:43:55 INFO mapreduce.Job: The url to track the job: http://server01:8088/proxy/application_1420542591388_0112/
		15/01/14 10:43:55 INFO mapreduce.Job: Running job: job_1420542591388_0112
		15/01/14 10:44:06 INFO mapreduce.Job: Job job_1420542591388_0112 running in uber mode : false
		Total milliseconds for task: 494 = 29859
		Total milliseconds for task: 495 = 29878
		Total milliseconds for task: 496 = 29908
		Total milliseconds for task: 497 = 29943
		Total milliseconds for task: 498 = 29897
		Total milliseconds for task: 499 = 29919
		Total milliseconds for task: 500 = 28881
		DataLines       Maps    Reduces AvgTime (milliseconds)
		50              40      20      31298
```
以上结果表示平均作业完成时间是31秒。

### (6)  Hadoop Examples
#### 除了上文提到的测试，Hadoop还自带了一些例子，比如WordCount和TeraSort，这些例子在hadoop-examples*.jar中。
```		
		[hsu@server01 ~]$ ls /opt/cloudera/parcels/CDH-5.2.0-1.cdh5.2.0.p0.36/lib/hadoop-0.20-mapreduce/hadoop-examples*
		/opt/cloudera/parcels/CDH-5.2.0-1.cdh5.2.0.p0.36/lib/hadoop-0.20-mapreduce/hadoop-examples-2.5.0-mr1-cdh5.2.0.jar
		/opt/cloudera/parcels/CDH-5.2.0-1.cdh5.2.0.p0.36/lib/hadoop-0.20-mapreduce/hadoop-examples.jar
```

#### 执行以下命令会列出所有的示例程序：
```	
		[hsu@server01 ~]$ sudo hadoop jar /opt/cloudera/parcels/CDH-5.2.0-1.cdh5.2.0.p0.36/lib/hadoop-0.20-mapreduce/hadoop-examples.jar
		  An example program must be given as the first argument.
		  Valid program names are:
		  aggregatewordcount: An Aggregate based map/reduce program that counts the words in the input files.
		  aggregatewordhist: An Aggregate based map/reduce program that computes the histogram of the words in the input files.
		  bbp: A map/reduce program that uses Bailey-Borwein-Plouffe to compute exact digits of Pi.
		  dbcount: An example job that count the pageview counts from a database.
		  distbbp: A map/reduce program that uses a BBP-type formula to compute exact bits of Pi.
		  grep: A map/reduce program that counts the matches of a regex in the input.
		  join: A job that effects a join over sorted, equally partitioned datasets
		  multifilewc: A job that counts words from several files.
		  pentomino: A map/reduce tile laying program to find solutions to pentomino problems.
		  pi: A map/reduce program that estimates Pi using a quasi-Monte Carlo method.
		  randomtextwriter: A map/reduce program that writes 10GB of random textual data per node.
		  randomwriter: A map/reduce program that writes 10GB of random data per node.
		  secondarysort: An example defining a secondary sort to the reduce.
		  sort: A map/reduce program that sorts the data written by the random writer.
		  sudoku: A sudoku solver.
		  teragen: Generate data for the terasort
		  terasort: Run the terasort
		  teravalidate: Checking results of terasort
		  wordcount: A map/reduce program that counts the words in the input files.
		  wordmean: A map/reduce program that counts the average length of the words in the input files.
		  wordmedian: A map/reduce program that counts the median length of the words in the input files.
		  wordstandarddeviation: A map/reduce program that counts the standard deviation of the length of the words in the input files.
```

### (7) TeraSort[TeraSort: Run the actual TeraSort benchmark]

#### 一个完整的TeraSort测试需要按以下三步执行：
- 1、用TeraGen生成随机数据
- 2、对输入数据运行TeraSort
- 3、用TeraValidate验证排好序的输出数据并不需要在每次测试时都生成输入数据，生成一次数据之后，每次测试可以跳过第一步。

- TeraGen的用法如下：
```
			$ hadoop jar hadoop-*examples*.jar teragen <number of 100-byte rows> <output dir>
```
以下命令运行TeraGen生成10GB的输入数据，并输出到目录/examples/terasort-input：

```			
[hsu@server01 ~]$ sudo hadoop jar /opt/cloudera/parcels/CDH-5.2.0-1.cdh5.2.0.p0.36/lib/hadoop-0.20-mapreduce/hadoop-examples.jar teragen 100000000 /examples/terasort-input
			15/01/13 16:57:34 INFO client.RMProxy: Connecting to ResourceManager at server01/135.33.5.53:8032
			15/01/13 16:57:35 INFO terasort.TeraSort: Generating 100000000 using 2
			15/01/13 16:57:35 INFO mapreduce.JobSubmitter: number of splits:2
			15/01/13 16:59:07 INFO mapreduce.Job: Job job_1420542591388_0105 completed successfully
			15/01/13 16:59:08 INFO mapreduce.Job: Counters: 31
			        File System Counters
			                FILE: Number of bytes read=0
			                FILE: Number of bytes written=211922
			                FILE: Number of read operations=0
			                FILE: Number of large read operations=0
			                FILE: Number of write operations=0
			                HDFS: Number of bytes read=170
			                HDFS: Number of bytes written=10000000000
			                HDFS: Number of read operations=8
			                HDFS: Number of large read operations=0
			                HDFS: Number of write operations=4
			        Job Counters 
			                Launched map tasks=2
			                Other local map tasks=2
			                Total time spent by all maps in occupied slots (ms)=150416
			                Total time spent by all reduces in occupied slots (ms)=0
			                Total time spent by all map tasks (ms)=150416
			                Total vcore-seconds taken by all map tasks=150416
			                Total megabyte-seconds taken by all map tasks=154025984
			        Map-Reduce Framework
			                Map input records=100000000
			                Map output records=100000000
			                Input split bytes=170
			                Spilled Records=0
			                Failed Shuffles=0
			                Merged Map outputs=0
			                GC time elapsed (ms)=1230
			                CPU time spent (ms)=175090
			                Physical memory (bytes) snapshot=504807424
			                Virtual memory (bytes) snapshot=3230924800
			                Total committed heap usage (bytes)=1363148800
			        org.apache.hadoop.examples.terasort.TeraGen$Counters
			                CHECKSUM=214760662691937609
			        File Input Format Counters 
			                Bytes Read=0
			        File Output Format Counters 
			                Bytes Written=10000000000
```
- TeraGen产生的数据每行的格式如下：

			<10 bytes key><10 bytes rowid><78 bytes filler>\r\n
** 其中：
 1、key是一些随机字符，每个字符的ASCII码取值范围为[32, 126] </n>
 2、rowid是一个整数，右对齐 </n>
 3、filler由7组字符组成，每组有10个字符（最后一组8个），字符从’A'到’Z'依次取值</n>		
- 以下命令运行TeraSort对数据进行排序，并将结果输出到目录/examples/terasort-output：
```
			[hsu@server01 ~]$ sudo hadoop jar /opt/cloudera/parcels/CDH-5.2.0-1.cdh5.2.0.p0.36/lib/hadoop-0.20-mapreduce/hadoop-examples.jar terasort /examples/terasort-input /examples/terasort-output
			15/01/13 17:08:08 INFO terasort.TeraSort: starting
			15/01/13 17:08:10 INFO input.FileInputFormat: Total input paths to process : 2
			Spent 187ms computing base-splits.
			Spent 3ms computing TeraScheduler splits.
			Computing input splits took 192ms
			Sampling 10 splits of 76
			Making 144 from 100000 sampled records
			Computing parititions took 596ms
			Spent 791ms computing partitions.terasort /examples/terasort-input /examples/terasort-output
			15/01/13 17:09:13 INFO mapreduce.Job: Counters: 50
			        File System Counters
			                FILE: Number of bytes read=4461968618
			                FILE: Number of bytes written=8889668662
			                FILE: Number of read operations=0
			                FILE: Number of large read operations=0
			                FILE: Number of write operations=0
			                HDFS: Number of bytes read=10000010260
			                HDFS: Number of bytes written=10000000000
			                HDFS: Number of read operations=660
			                HDFS: Number of large read operations=0
			                HDFS: Number of write operations=288
			        Job Counters 
			                Launched map tasks=76
			                Launched reduce tasks=144
			                Data-local map tasks=75
			                Rack-local map tasks=1
			                Total time spent by all maps in occupied slots (ms)=933160
			                Total time spent by all reduces in occupied slots (ms)=1227475
			                Total time spent by all map tasks (ms)=933160
			                Total time spent by all reduce tasks (ms)=1227475
			                Total vcore-seconds taken by all map tasks=933160
			                Total vcore-seconds taken by all reduce tasks=1227475
			                Total megabyte-seconds taken by all map tasks=955555840
			                Total megabyte-seconds taken by all reduce tasks=1256934400
			        Map-Reduce Framework
			                Map input records=100000000
			                Map output records=100000000
			                Map output bytes=10200000000
			                Map output materialized bytes=4403942936
			                Input split bytes=10260
			                Combine input records=0
			                Combine output records=0
			                Reduce input groups=100000000
			                Reduce shuffle bytes=4403942936
			                Reduce input records=100000000
			                Reduce output records=100000000
			                Spilled Records=200000000
			                Shuffled Maps =10944
			                Failed Shuffles=0
			                Merged Map outputs=10944
			                GC time elapsed (ms)=45169
			                CPU time spent (ms)=2021010
			                Physical memory (bytes) snapshot=95792517120
			                Virtual memory (bytes) snapshot=357225058304
			                Total committed heap usage (bytes)=174283816960
			        Shuffle Errors
			                BAD_ID=0
			                CONNECTION=0
			                IO_ERROR=0
			                WRONG_LENGTH=0
			                WRONG_MAP=0
			                WRONG_REDUCE=0
			        File Input Format Counters 
			                Bytes Read=10000000000
			        File Output Format Counters 
			                Bytes Written=10000000000
			15/01/13 17:09:13 INFO terasort.TeraSort: done
```

### (8) terasort-validate 验证是否有序

#### 以下命令运行TeraValidate来验证TeraSort输出的数据是否有序，如果检测到问题，将乱序的key输出到目录/examples/terasort-validate
```	
	[hsu@server01 ~]$ sudo hadoop jar /opt/cloudera/parcels/CDH-5.2.0-1.cdh5.2.0.p0.36/lib/hadoop-0.20-mapreduce/hadoop-examples.jar teravalidate /examples/terasort-output /examples/terasort-validate
		15/01/13 17:17:37 INFO client.RMProxy: Connecting to ResourceManager at server01/135.33.5.53:8032
		15/01/13 17:17:38 INFO input.FileInputFormat: Total input paths to process : 144
		Spent 93ms computing base-splits.
		Spent 3ms computing TeraScheduler splits.
		15/01/13 17:17:38 INFO mapreduce.JobSubmitter: number of splits:144
		15/01/13 17:17:38 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1420542591388_0107
		15/01/13 17:17:38 INFO impl.YarnClientImpl: Submitted application application_1420542591388_0107teravalidate /examples/terasort-output /examples/terasort-validate
		15/01/13 17:18:12 INFO mapreduce.Job: Job job_1420542591388_0107 completed successfully
		15/01/13 17:18:12 INFO mapreduce.Job: Counters: 50
		        File System Counters
		                FILE: Number of bytes read=6963
		                FILE: Number of bytes written=15445453
		                FILE: Number of read operations=0
		                FILE: Number of large read operations=0
		                FILE: Number of write operations=0
		                HDFS: Number of bytes read=10000019584
		                HDFS: Number of bytes written=25
		                HDFS: Number of read operations=435
		                HDFS: Number of large read operations=0
		                HDFS: Number of write operations=2
		        Job Counters 
		                Launched map tasks=144
		                Launched reduce tasks=1
		                Data-local map tasks=142
		                Rack-local map tasks=2
		                Total time spent by all maps in occupied slots (ms)=685624
		                Total time spent by all reduces in occupied slots (ms)=3384
		                Total time spent by all map tasks (ms)=685624
		                Total time spent by all reduce tasks (ms)=3384
		                Total vcore-seconds taken by all map tasks=685624
		                Total vcore-seconds taken by all reduce tasks=3384
		                Total megabyte-seconds taken by all map tasks=702078976
		                Total megabyte-seconds taken by all reduce tasks=3465216
		        Map-Reduce Framework
		                Map input records=100000000
		                Map output records=432
		                Map output bytes=11664
		                Map output materialized bytes=13830
		                Input split bytes=19584
		                Combine input records=0
		                Combine output records=0
		                Reduce input groups=289
		                Reduce shuffle bytes=13830
		                Reduce input records=432
		                Reduce output records=1
		                Spilled Records=864
		                Shuffled Maps =144
		                Failed Shuffles=0
		                Merged Map outputs=144
		                GC time elapsed (ms)=4014
		                CPU time spent (ms)=334280
		                Physical memory (bytes) snapshot=85470654464
		                Virtual memory (bytes) snapshot=234019295232
		                Total committed heap usage (bytes)=114868879360
		        Shuffle Errors
		                BAD_ID=0
		                CONNECTION=0
		                IO_ERROR=0
		                WRONG_LENGTH=0
		                WRONG_MAP=0
		                WRONG_REDUCE=0
		        File Input Format Counters 
		                Bytes Read=10000000000
		        File Output Format Counters 
		                Bytes Written=25

			[hsu@server01 ~]$ hadoop fs -cat /examples/terasort-validate/*                                                           checksum        2fafbaf537afd49
```
结论：检测通过

### (10) 总结
#### 在提交任务目录下会生成两个文件
```	
			[hsu@server01 ~]$ LANG=en
			[hsu@server01 ~]$ ll
			total 16
			-rw-r--r-- 1 root root 1142 Jan 13 15:56 NNBench_results.log
			-rw-r--r-- 1 root root  903 Jan 13 15:43 TestDFSIO_results.log
```

约对176838144行数据进行排序，部分数据：
```			
			0000000: 	00 00 00 a7 0d 2a a8 02 da da 00 11 30 30 30 30	  .....*......0000
			0000010: 	30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30	  0000000000000000
```

#### 参考资料：
		http://www.michael-noll.com/blog/2011/04/09/benchmarking-and-stress-testing-an-hadoop-cluster-with-terasort-testdfsio-nnbench-mrbench/
		https://github.com/intel-hadoop/HiBench

# 二、hive/impala测试

### Impala/hive性能报告：
>> 下面对event_calling_201410(39.8G)和event_sms_201410(39.8G)做join操作和count(*)：

#### (1) count(*)操作
```			
			[yndx-bigdata-hadoop02:21000] > select count(*) from event_calling_201410;
			Query: select count(*) from event_calling_201410
			+-----------+
			| count(*)  |
			+-----------+
			| 425883373 |
			+-----------+
			Fetched 1 row(s) in 192.75s
			hive (i_bil_hb_m)> select count(*) from event_calling_201410;
			Total jobs = 1
			Launching Job 1 out of 1
			OK
			_c0
			425883373
			Time taken: 386.804 seconds, Fetched: 1 row(s)
			[yndx-bigdata-hadoop02:21000] > select count(*) from event_sms_201410;
			Query: select count(*) from event_sms_201410
			+----------+
			| count(*) |
			+----------+
			| 80675409 |
			+----------+
			Fetched 1 row(s) in 33.52s
```

#### (2) 两表join操作

```			
			hive (i_bil_hb_m)> select count(*) from event_calling_201410 c left outer join event_sms_201410 s on(s.calling_nbr=c.calling_nbr);  
			Total jobs = 2
			Stage-1 is selected by condition resolver.
			Launching Job 1 out of 2
			Number of reduce tasks not specified. Estimated from input data size: 279
			In order to change the average load for a reducer (in bytes):
			  set hive.exec.reducers.bytes.per.reducer=<number>
			In order to limit the maximum number of reducers:
			  set hive.exec.reducers.max=<number>
			In order to set a constant number of reducers:
			  set mapreduce.job.reduces=<number>
			Starting Job = job_1420542591388_0987, Tracking URL = http://yndx-bigdata-hadoop01:8088/proxy/application_1420542591388_0987/
			Kill Command = /opt/cloudera/parcels/CDH-5.2.0-1.cdh5.2.0.p0.36/lib/hadoop/bin/hadoop job  -kill job_1420542591388_0987
			Hadoop job information for Stage-1: number of mappers: 1110; number of reducers: 279
			2015-01-15 10:44:01,665 Stage-1 map = 100%,  reduce = 100%, Cumulative CPU 19731.27 sec
			MapReduce Total cumulative CPU time: 0 days 5 hours 28 minutes 51 seconds 270 msec
			Ended Job = job_1420542591388_0987
			Launching Job 2 out of 2
			Number of reduce tasks determined at compile time: 1
			In order to change the average load for a reducer (in bytes):
			  set hive.exec.reducers.bytes.per.reducer=<number>
			In order to limit the maximum number of reducers:
			  set hive.exec.reducers.max=<number>
			In order to set a constant number of reducers:
			  set mapreduce.job.reduces=<number>
			2015-01-15 10:44:33,709 Stage-2 map = 100%,  reduce = 100%, Cumulative CPU 15.28 sec
			MapReduce Total cumulative CPU time: 15 seconds 280 msec
			Ended Job = job_1420542591388_0988
			MapReduce Jobs Launched: 
			Stage-Stage-1: Map: 1110  Reduce: 279   Cumulative CPU: 19731.27 sec   HDFS Read: 298693978456 HDFS Write: 32922 SUCCESS
			Stage-Stage-2: Map: 7  Reduce: 1   Cumulative CPU: 15.28 sec   HDFS Read: 97828 HDFS Write: 12 SUCCESS
			Total MapReduce CPU Time Spent: 0 days 5 hours 29 minutes 6 seconds 550 msec
			OK
			_c0
			13106534553
			Time taken: 413.651 seconds, Fetched: 1 row(s)
			[yndx-bigdata-hadoop02:21000] >  select count(*) from event_calling_201410 c left outer join event_sms_201410 s on(s.calling_nbr=c.calling_nbr);
			Query: select count(*) from event_calling_201410 c left outer join event_sms_201410 s on(s.calling_nbr=c.calling_nbr)
			 +-------------+
			| count(*)    |
			+-------------+
			| 13106534553 |
			+-------------+
			Fetched 1 row(s) in 525.48s
```

### (3) 统计结果
```
Action		数据量(G)	   HiveTime(s)	   ImpalaTime(s) Hive结论 Imapla结论
Count(*)	 39.8			386.804			192.75		通过  警告阈值(内存)
join(2)		 39.8*2			413.651			525.48		通过  警告阈值(内存)
```


原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/