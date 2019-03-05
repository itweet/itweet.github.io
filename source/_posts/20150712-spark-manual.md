---
title: spark manual
date: 2015-07-12 18:37:36
description: Spark 的安装与使用
category: BigData
tags: spark
---
# 集群概述
本文章涉及spark安装部署，spark-sql,spark-shell,streaming等等的应用demo...[saprk文章](https://www.itweet.cn/categories/spark/)

## 部署过程详解

Spark布置环境中组件构成如下图所示。
![](https://www.itweet.cn/screenshots/cluster-overview.png)

-   `Driver Program` 简要来说在spark-shell中输入的wordcount语句对应于上图的Driver Program。
-   `Cluster Manager` 就是对应于上面提到的master，主要起到deploy management的作用
-   `Worker Node` 与Master相比，这是slave node。上面运行各个executor，executor可以对应于线程。executor处理两种基本的业务逻辑，一种就是driver programme，另一种就是job在提交之后拆分成各个stage，每个stage可以运行一到多个task

`Notes`: 在集群（cluster）方式下，Cluster Manager运行在一个`jvm`进程之中，而worker运行在另一个`jvm`进程中。在local cluster中，这些`jvm`进程都在同一台机器中，如果是真正的Standalone或Mesos及Yarn集群，worker与master或分布于不同的主机之上。

## JOB的生成和运行

job生成的简单流程如下

   -    1、首先应用程序创建SparkContext的实例，如实例为sc
   -    2、利用SparkContext的实例来创建生成RDD
   -    3、经过一连串的transformation操作，原始的RDD转换成为其它类型的RDD
   -    4、当action作用于转换之后RDD时，会调用SparkContext的runJob方法
   -    5、sc.runJob的调用是后面一连串反应的起点，关键性的跃变就发生在此处
 
调用路径大致如下

   -    1、sc.runJob->dagScheduler.runJob->submitJob
   -    2、DAGScheduler::submitJob会创建JobSummitted的event发送给内嵌类eventProcessActor
   -    3、eventProcessActor在接收到JobSubmmitted之后调用processEvent处理函数
   -    4、job到stage的转换，生成finalStage并提交运行，关键是调用submitStage
   -    5、在submitStage中会计算stage之间的依赖关系，依赖关系分为宽依赖和窄依赖两种
   -    6、如果计算中发现当前的stage没有任何依赖或者所有的依赖都已经准备完毕，则提交task
   -    7、提交task是调用函数submitMissingTasks来完成
   -    8、task真正运行在哪个worker上面是由TaskScheduler来管理，也就是上面的submitMissingTasks会调用TaskScheduler::submitTasks
   -    9、TaskSchedulerImpl中会根据Spark的当前运行模式来创建相应的backend，如果是在单机运行则创建LocalBackend
   -    10、LocalBackend收到TaskSchedulerImpl传递进来的ReceiveOffers事件
   -    11、receiveOffers->executor.launchTask->TaskRunner.run

   代码片段executor.lauchTask

    def launchTask(context: ExecutorBackend, taskId: Long, serializedTask: ByteBuffer) {
    val tr = new TaskRunner(context, taskId, serializedTask)
    runningTasks.put(taskId, tr)
    threadPool.execute(tr)
  }

  最终的逻辑处理切切实实是发生在TaskRunner这么一个executor之内。
  运算结果是包装成为MapStatus然后通过一系列的内部消息传递，反馈到DAGScheduler

# 编译spark

## 获取源码
    `wget http://mirror.bit.edu.cn/apache/spark/spark-1.4.0/spark-1.4.0.tgz`
    `tar -zxf spark-1.4.0.tgz`
    `cd spark-1.4.0`

## 编译支持hive，yarn，tachyon

### 1、`[ERROR] PermGen space -> [Help 1]`
    export MAVEN_OPTS="-Xmx2g -XX:MaxPermSize=512M -XX:ReservedCodeCacheSize=512m"

### 2、编译
    mvn -Pyarn -Phive -Phive-thriftserver -Dhadoop.version=2.4.0 -DskipTests clean package

### 3、生成部署包
    ./make-distribution.sh --with-tachyon --tgz -Phive -Phive-thriftserver -Pyarn -Dhadoop.version=2.4.0

### 4、编译spark支持ganglia插件
https://spark.apache.org/docs/latest/monitoring.html
```
    export MAVEN_OPTS="-Xmx3g -XX:MaxPermSize=1512M -XX:ReservedCodeCacheSize=1512m"
    mvn clean package -DskipTests -Pyarn -Phadoop-2.4 -Dhadoop.version=2.4.0 -Phive -Phive-thriftserver -Pspark-ganglia-lgpl
```
   
`[ERROR] mvn <goals> -rf :spark-mllib_2.10`

>参考：http://stackoverflow.com/questions/29354461/spark-1-3-0-build-failure
>      https://issues.apache.org/jira/browse/SPARK-6532

>调试：mvn -DskipTests -X clean package，是个bug已解决！
pom.xml文件中修改

```    
    <plugin>
        <groupId>org.scalastyle</groupId>
        <artifactId>scalastyle-maven-plugin</artifactId>
        <version>0.4.0</version>
        <configuration>
          <verbose>false</verbose>
          <failOnViolation>true</failOnViolation>
          <includeTestSourceDirectory>false</includeTestSourceDirectory>
          <failOnWarning>false</failOnWarning>
          <sourceDirectory>${basedir}/src/main/scala</sourceDirectory>
          <testSourceDirectory>${basedir}/src/test/scala</testSourceDirectory>
          <configLocation>scalastyle-config.xml</configLocation>
          <outputFile>scalastyle-output.xml</outputFile>
          <outputEncoding>UTF-8</outputEncoding>
          <inputEncoding>UTF-8</inputEncoding> <!--add this line-->
        </configuration>
        <executions>
          <execution>
            <phase>package</phase>
            <goals>
              <goal>check</goal>
            </goals>
          </execution>
        </executions>
      </plugin>
```

>由于windows编译生成部署包那个脚本不能用，所以自己制作部署包！
>参考官网编译后的目录来构建！


# Spark Standalone Mode

## 配置

### 1、配置spark-defaults.conf

    $ cat spark-defaults.conf 
    # Default system properties included when running spark-submit.
    # This is useful for setting default environmental settings.
    # Example:
    # spark.master                     spark://master:7077
    # spark.eventLog.enabled           true
    # spark.eventLog.dir               hdfs://namenode:8021/directory
    # spark.serializer                 org.apache.spark.serializer.KryoSerializer
    # spark.driver.memory              5g
    # spark.executor.extraJavaOptions  -XX:+PrintGCDetails -Dkey=value -Dnumbers="one two three"
    spark.master            spark://server1:7077
    spark.eventLog.enabled  true
    spark.eventLog.dir      hdfs://mycluster/tmp/spark
    spark.serializer        org.apache.spark.serializer.KryoSerializer
    spark.executor.memory   8g
    spark.local.dir  /data/spark/localdata
    spark.driver.memory   10g
    spark.history.fs.logDirectory /data/spark/local
    spark.scheduler.mode  FAIR  

### 2、配置saprk-evn.sh
    $ cat spark-env.sh
    export JAVA_HOME=/usr/java/jdk1.6.0_31/
    export SCALA_HOME=/usr/apps/scala-2.10.4
    export HIVE_HOME=/etc/hive
    export HIVE_CONF_DIR=$HIVE_HOME/conf
    export HADOOP_HOME=/etc/hadoop
    export HADOOP_CONF_DIR=/etc/hadoop/etc
    
    export SPARK_MASTER_IP=server1
    export SPARK_MASTER_PORT=7077
    export SPARK_MASTER_WEBUI_PORT=8090
    export SPARK_LOCAL_DIRS=/data/spark/localdata
    
    # - SPARK_MASTER_OPTS
    export SPARK_WORKER_CORES=20
    export SPARK_WORKER_MEMORY=120g
    export SPARK_WORKER_PORT=8991
    export SPARK_WORKER_WEBUI_PORT=8992
    export SPARK_WORKER_INSTANCES=1
    export SPARK_WORKER_DIR=/data/spark/workdir
    export SPARK_WORKER_OPTS="-Dspark.worker.cleanup.enabled=false  -Dspark.worker.cleanup.interval=1800  -Dspark.worker.cleanup.appDataTtl=604800"
    export SPARK_DAEMON_MEMORY=2048m
    export SPARK_DAEMON_JAVA_OPTS="-Dspark.deploy.recoveryMode=ZOOKEEPER   -Dspark.deploy.zookeeper.url=server1:2181,server2:2181,server3:2181 -Dspark.deploy.zookeeper.dir=/spark"
    export SPARK_WORKER_OPTS="-Dspark.worker.cleanup.enabled=true  -Dspark.worker.cleanup.interval=1800  -Dspark.worker.cleanup.appDataTtl=604800"
    
    export SPARK_JAR=/usr/lib/spark/assembly/target/scala-2.10/spark-assembly-1.4.0-SNAPSHOT-hadoop2.4.0.jar
    export SPARK_CLASSPATH=/usr/lib/hive/lib/mysql-connector-java.jar
    export HADOOP_CONF_DIR=/usr/lib/hadoop/etc/hadoop
    export SPARK_DAEMON_JAVA_OPTS=" -XX:NewRatio=1  -verbose:gc -XX:+PrintGCDetails -Xloggc:/tmp/gc.log -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/tmp/saprk_heapdum.hprof -XX:+UseParNewGC -XX:+UseConcMarkSweepGC -XX:+UseCMSCompactAtFullCollection -XX:CMSInitiatingOccupancyFraction=60 -XX:+PrintGCTimeStamps"
    export SPARK_LOG_DIR=/var/log/spark

### 3、配置log4j
根据各自情况配置log日志级别方便调试！

### 4、配置fairscheduler.xml
```
$ cat fairscheduler.xml
<?xml version="1.0"?>
<allocations>
  <pool name="test1">
    <schedulingMode>FAIR</schedulingMode>
    <weight>2</weight>
    <minShare>20</minShare>
  </pool>
  <pool name="test2">
     <schedulingMode>FAIR</schedulingMode>
     <weight>2</weight>
     <minShare>10</minShare>
  </pool>
  <pool name="default">
    <schedulingMode>FAIR</schedulingMode>
    <weight>1</weight>
    <minShare>10</minShare>
  </pool>
```

#### 4.1 spark-sql使用队列
```
    SET spark.sql.thriftserver.scheduler.pool=test1;
    select * from default.abc;
    ........
```

#### 4.2 应用程序中使用队列
```
    // Assuming sc is your SparkContext variable
    sc.setLocalProperty("spark.scheduler.pool", "pool1")
```

# spark on yarn
配置基本不变,但是无需启动spark集群，而直接依赖yarn集群！

yarn-spark-sql:
    `spark-sql --master yarn-client --executor-memory 2g`

yarn-spark-shell:
    `spark-shell --master yarn-client --executor-memory 2g`

```
    $ spark-sql --master yarn-client --executor-memory 2g --verbose 
    Run with --help for usage help or --verbose for debug output
```

# 使用spark

>启动saprk集群：
  `$SPARK_HOME/sbin/start-all.sh`  

>停止集群
  `$SPARK_HOME/sbin/stop-all.sh`

## 1、saprk-sql
### spark cli start
```
    $ spark-sql --master spark://server1:7077 --executor-memory 16g --total-executor-cores 200
```

### start-thriftserver.sh jdbc
This script accepts all bin/spark-submit command line options, plus a --hiveconf option to specify Hive properties. You may run ./sbin/start-thriftserver.sh --help for a complete list of all available options. By default, the server listens on localhost:10000. You may override this bahaviour via either environment variables, i.e.:
export HIVE_SERVER2_THRIFT_PORT=<listening-port>
export HIVE_SERVER2_THRIFT_BIND_HOST=<listening-host>
./sbin/start-thriftserver.sh \
  --master <master-uri> \
  ...
or system properties:
./sbin/start-thriftserver.sh \
  --hiveconf hive.server2.thrift.port=<listening-port> \
  --hiveconf hive.server2.thrift.bind.host=<listening-host> \
  --master <master-uri>
  ...

```
    $ start-thriftserver.sh spark://server1:7077 --executor-memory 16g --total-executor-cores 200  --conf spark.storage.memoryFraction=0.8 spark-internal spark.shuffle.consolidateFiles=true spark.shuffle.spill.compress=true spark.kryoserializer.buffer.mb 128 --hiveconf hive.server2.thrift.port=9981
```

### spark-sql beeline
```
    $SPARK_HOME/bin/spark-sql --master spark://server1:7077 -e "show databases"
    
    $SPARK_HOME/bin/spark-sql -h
    
    $SPARK_HOME/bin/beeline -u "jdbc:hive2://server1:10000" -e "show databases" --  outputformat=table
    
    $SPARK_HOME/bin/beeline -u "jdbc:hive2://server1:10000" -n hsu -p hsu -d org.apache.hive.jdbc.HiveDriver --color=true -e <<EOF 'show databases'
    EOF
```

## 2、使用spark-shell
这里需要注意，spark-shell必须在主节点启动，否则启动会失败！
```
    $spark_home/bin/spark-shell --master spark://server1:7077 --executor-memory 2g --total-executor-cores 5

    scala api：
    val textFile = spark.textFile("hdfs://...")
    val errors = textFile.filter(line => line.contains("ERROR"))
    // Count all the errors
    errors.count()
    // Count errors mentioning MySQL
    errors.filter(line => line.contains("MySQL")).count()
    // Fetch the MySQL errors as an array of strings
    errors.filter(line => line.contains("MySQL")).collect()
```


## 3、streaming
### 3.1 数据源来自网络端口
server2利用nc发送数据,这边不断生成数据,streaming不断计算
```
    $ sudo nc -lk 9999
    hello word
```

```
    # spark/bin/spark-submit --class com.sparkjvm.streaming.yarn.NewHdfsWordCount --master spark://server1:7077 ./spark-yarn-1.0-SNAPSHOT.jar server2 9999 10
```

![](https://www.itweet.cn/screenshots/streaming-net.png)

程序
```
    object NewHdfsWordCount {
      def main(args: Array[String]) {
        if (args.length < 3) {
          System.err.println("Usage: HdfsWordCount <master> <directory> <seconds>")
          System.exit(1)
        }
        //新建StreamingContext
        val ssc = new StreamingContext(new SparkConf(), Seconds(args(2).toInt))

        //创建FileInputDStream，并指向特定目录
        val lines = ssc.socketTextStream(args(0), args(1).toInt, StorageLevel.MEMORY_ONLY_SER)
        val words = lines.flatMap(_.split(" "))
        val wordCounts = words.map(x => (x, 1)).reduceByKey(_ + _)
        wordCounts.print()
        ssc.start()
        ssc.awaitTermination()
      }
    }
```

### 3.2 数据来源hdfs
```
$ hadoop fs -cat /data/test/a
a
a
a
a
a
```

提交程序
```
spark/bin/spark-submit --class com.sparkjvm.streaming.standalone.HdfsWordCount --master spark://server1:7077 --executor-memory 10G --total-executor-cores 10 ./spark-yarn-1.0-SNAPSHOT.jar hdfs://mycluster/data/test
```

put数据到test目录
```
$  hadoop fs -put b /data/test/b
$  hadoop fs -cat /data/test/b  
b
b
b
b
b
```

![](https://www.itweet.cn/screenshots/streaming-hdfs.png)

```
$  hadoop fs -put c /data/test
$  hadoop fs -cat /data/test/c
c
c
c
c
c
```

![](https://www.itweet.cn/screenshots/streaming-hdfs-1.png)

### 3.3 kafka+sparkstreaming

![](https://www.itweet.cn/screenshots/kafka_streaming.png)

程序
```
object DirectKafkaWordCount {
  def main(args: Array[String]) {
    if (args.length < 2) {
      System.err.println(s"""
        |Usage: DirectKafkaWordCount <brokers> <topics>
        |  <brokers> is a list of one or more Kafka brokers
        |  <topics> is a list of one or more kafka topics to consume from
        |
        """.stripMargin)
      System.exit(1)
    }

    StreamingExamples.setStreamingLogLevels()

    val Array(brokers, topics) = args

    // Create context with 2 second batch interval
    val sparkConf = new SparkConf().setAppName("DirectKafkaWordCount")
    val ssc =  new StreamingContext(sparkConf, Seconds(2))

    // Create direct kafka stream with brokers and topics
    val topicsSet = topics.split(",").toSet
    val kafkaParams = Map[String, String]("metadata.broker.list" -> brokers)
    val messages = KafkaUtils.createDirectStream[String, String, StringDecoder, StringDecoder](
      ssc, kafkaParams, topicsSet)

    // Get the lines, split them into words, count the words and print
    val lines = messages.map(_._2)
    
    val words = lines.flatMap(_.split(" "))
    val wordCounts = words.map(x => (x, 1L)).reduceByKey(_ + _)
    wordCounts.print()

    // Start the computation
    ssc.start()
    ssc.awaitTermination()
  }
}
```

提交任务
```
spark/bin/spark-submit --class org.sparkjvm.streaming.kafka.DirectKafkaWordCount --master spark://server1:7077 ./org.spark.code-1.0-SNAPSHOT-jar-with-dependencies.jar server1:9092,server2:9092,server3:9092,server4:9092,server5:9092,server6:9092,server7:9092,server8:9092,server9:9092,server10:9092 test
```

kafka发送数据到test topic
```
    kafka/bin/kafka-console-producer.sh --broker-list server1:9092 --topic test
    a b c
    d e f
```

![](https://www.itweet.cn/screenshots/kafka_streaming_1.png)

### 3.4 kafka+streaming more[0.13.1+]
```
    The new API is simpler to use than the previous one.
    // Define the Kafka parameters, broker list must be specified
    val kafkaParams = Map("metadata.broker.list" -> "localhost:9092,anotherhost:9092")

    // Define which topics to read from
    val topics = Set("sometopic", "anothertopic")
    
    // Create the direct stream with the Kafka parameters and topics
    val kafkaStream = KafkaUtils.createDirectStream[String, String, StringDecoder, StringDecoder](streamingContext, kafkaParams, topics)
    Since this direct approach does not have any receivers, you do not have to worry about creating multiple input DStreams to create more receivers. Nor do you have to configure the number of Kafka partitions to be consumed per receiver. Each Kafka partition will be automatically read in parallel.  Furthermore, each Kafka partition will correspond to a RDD partition, thus simplifying the parallelism model.
    In addition to the new streaming API, we have also introduced KafkaUtils.createRDD(), which can be used to run batch jobs on Kafka data.
    // Define the offset ranges to read in the batch job
    val offsetRanges = Array(
     OffsetRange("some-topic", 0, 110, 220),
    OffsetRange("some-topic", 1, 100, 313),
    OffsetRange("another-topic", 0, 456, 789)
    )

    // Create the RDD based on the offset ranges
    val rdd = KafkaUtils.createRDD[String, String, StringDecoder, StringDecoder](sparkContext, kafkaParams, offsetRanges)
    If you want to learn more about the API and the details of how it was implemented, take a look at the following.
```

参考：
http://spark.apache.org/docs/latest/streaming-kafka-integration.html

## 3.5 MLlib
    https://spark.apache.org/docs/latest/mllib-guide.html

>在有些情况下，你需要进行一些ETL工作，然后训练一个机器学习的模型，最后进行一些查询，如果是使用Spark，你可以在一段程序中将这三部分的逻辑完成形成一个大的有向无环图（DAG），而且Spark会对大的有向无环图进行整体优化。

例如下面的程序：
```
  val points = sqlContext.sql(   “SELECT latitude, longitude FROM   historic_tweets”)  
  
  val model = KMeans.train(points, 10)  
  
  sc.twitterStream(...)   .map(t => (model.closestCenter(t.location), 1)).reduceByWindow(“5s”, _ + _)
```

## 3.6 GraphX
    https://spark.apache.org/docs/latest/graphx-programming-guide.html

## 3.7 Reducer number
    In Shark, default reducer number is 1 and is controlled by the property mapred.reduce.tasks. Spark SQL deprecates this property in favor ofspark.sql.shuffle.partitions, whose default value is 200. Users may customize this property via SET:
    SET spark.sql.shuffle.partitions=10;
    SELECT page, count(*) c
    FROM logs_last_month_cached
    GROUP BY page ORDER BY c DESC LIMIT 10;
    You may also put this property in hive-site.xml to override the default value.
    For now, the mapred.reduce.tasks property is still recognized, and is converted to spark.sql.shuffle.partitions automatically.

## 3.8  spark 查看 job history 日志

- (1). 修改配置文件

  SPARK_HOME/conf 下:
  spark-defaults.conf 增加如下内容
```  
  spark.eventLog.enabled true 
  spark.eventLog.dir hdfs://server01:8020/tmp/spark 
  spark.eventLog.compress true
```
 
  spark-env.sh 增加如下内容

```  
  export SPARK_HISTORY_OPTS="-Dspark.history.ui.port=18080 -Dspark.history.retainedApplications=3 -Dspark.history.fs.logDirectory=hdfs://server01:8020/tmp/spark"
```

- (2). 启动start-history-server.sh

  SPARK_HOME/sbin 下: 执行 ./start-history-server.sh
  
  spark job history webui: server01:18080
  
  在spark任务运行完成之后,依然可通过web页面查看日志

- (3). history server相关的配置参数描述

```
spark.history.updateInterval 
　　默认值：10 
　　以秒为单位，更新日志相关信息的时间间隔

spark.history.retainedApplications 
　　默认值：50 
　　在内存中保存Application历史记录的个数，如果超过这个值，旧的应用程序信息将被删除，当再次访问已被删除的应用信息时需要重新构建页面。

spark.history.ui.port 
　　默认值：18080 
　　HistoryServer的web端口

spark.history.kerberos.enabled 
　　默认值：false 
　　是否使用kerberos方式登录访问HistoryServer，对于持久层位于安全集群的HDFS上是有用的，如果设置为true，就要配置下面的两个属性

spark.history.kerberos.principal 
　　默认值：用于HistoryServer的kerberos主体名称

spark.history.kerberos.keytab 
　　用于HistoryServer的kerberos keytab文件位置

spark.history.ui.acls.enable 
　　默认值：false 
　　授权用户查看应用程序信息的时候是否检查acl。如果启用，只有应用程序所有者和spark.ui.view.acls指定的用户可以查看应用程序信息;否则，不做任何检查

spark.eventLog.enabled 
　　默认值：false 
　　是否记录Spark事件，用于应用程序在完成后重构webUI

spark.eventLog.dir 
　　默认值：file:///tmp/spark-events 
　　保存日志相关信息的路径，可以是hdfs://开头的HDFS路径，也可以是file://开头的本地路径，都需要提前创建

spark.eventLog.compress 
　　默认值：false 
　　是否压缩记录Spark事件，前提spark.eventLog.enabled为true，默认使用的是snappy
```

参考：https://spark.apache.org/


原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/
