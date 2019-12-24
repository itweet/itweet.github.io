---
title: Hive on Spark 整合测试
date: 2016-06-27 17:27:41
category: BigData
tags: SQL
---
根据官方给出的文档，进行编译打包，需要注意的是，"Hive on Spark is available from Hive 1.1+ onward,It is still under active development in "spark" and "spark2" branches, and is periodically merged into the "master" branch for Hive."
  - YARN Mode: http://spark.apache.org/docs/latest/running-on-yarn.html 
  - Standalone Mode: https://spark.apache.org/docs/latest/spark-standalone.html

# build package with［hive on spark]
[Hive on Spark](https://cwiki.apache.org/confluence/display/Hive/Hive+on+Spark%3A+Getting+Started#HiveonSpark:GettingStarted-ConfiguringHive)
```
$ wget https://dist.apache.org/repos/dist/release/spark/spark-1.6.2/spark-1.6.2.tgz
$ export MAVEN_OPTS="-Xmx2g -XX:MaxPermSize=512M -XX:ReservedCodeCacheSize=512m"
```

通过执行如下命令，可以完成打包，注意不要加hive参数，spark的包必须时没有集成过hive的，所以需要自己手动编译，官方提供的都是集成hive的：
```
./make-distribution.sh --name "hadoop2-without-hive" --tgz "-Pyarn,hadoop-provided,hadoop-2.6,parquet-provided"

[INFO] Replacing original artifact with shaded artifact.
[INFO] Replacing /data/spark-1.6.2/external/kafka-assembly/target/spark-streaming-kafka-assembly_2.10-1.6.2.jar with /data/spark-1.6.2/external/kafka-assembly/target/spark-streaming-kafka-assembly_2.10-1.6.2-shaded.jar
[INFO] Dependency-reduced POM written at: /data/spark-1.6.2/external/kafka-assembly/dependency-reduced-pom.xml
[INFO] Dependency-reduced POM written at: /data/spark-1.6.2/external/kafka-assembly/dependency-reduced-pom.xml
[INFO] 
[INFO] --- maven-source-plugin:2.4:jar-no-fork (create-source-jar) @ spark-streaming-kafka-assembly_2.10 ---
[INFO] Building jar: /data/spark-1.6.2/external/kafka-assembly/target/spark-streaming-kafka-assembly_2.10-1.6.2-sources.jar
[INFO] 
[INFO] --- maven-source-plugin:2.4:test-jar-no-fork (create-source-jar) @ spark-streaming-kafka-assembly_2.10 ---
[INFO] Building jar: /data/spark-1.6.2/external/kafka-assembly/target/spark-streaming-kafka-assembly_2.10-1.6.2-test-sources.jar
[INFO] ------------------------------------------------------------------------
[INFO] Reactor Summary:
[INFO] 
[INFO] Spark Project Parent POM ........................... SUCCESS [ 11.410 s]
[INFO] Spark Project Test Tags ............................ SUCCESS [  6.995 s]
[INFO] Spark Project Launcher ............................. SUCCESS [01:18 min]
[INFO] Spark Project Networking ........................... SUCCESS [ 30.344 s]
[INFO] Spark Project Shuffle Streaming Service ............ SUCCESS [ 15.242 s]
[INFO] Spark Project Unsafe ............................... SUCCESS [01:11 min]
[INFO] Spark Project Core ................................. SUCCESS [11:11 min]
[INFO] Spark Project Bagel ................................ SUCCESS [ 12.017 s]
[INFO] Spark Project GraphX ............................... SUCCESS [ 50.978 s]
[INFO] Spark Project Streaming ............................ SUCCESS [01:24 min]
[INFO] Spark Project Catalyst ............................. SUCCESS [01:24 min]
[INFO] Spark Project SQL .................................. SUCCESS [01:39 min]
[INFO] Spark Project ML Library ........................... SUCCESS [01:36 min]
[INFO] Spark Project Tools ................................ SUCCESS [  3.208 s]
[INFO] Spark Project Hive ................................. SUCCESS [01:00 min]
[INFO] Spark Project Docker Integration Tests ............. SUCCESS [  4.042 s]
[INFO] Spark Project REPL ................................. SUCCESS [ 12.562 s]
[INFO] Spark Project YARN Shuffle Service ................. SUCCESS [  8.056 s]
[INFO] Spark Project YARN ................................. SUCCESS [ 41.988 s]
[INFO] Spark Project Assembly ............................. SUCCESS [01:08 min]
[INFO] Spark Project External Twitter ..................... SUCCESS [ 10.449 s]
[INFO] Spark Project External Flume Sink .................. SUCCESS [ 13.694 s]
[INFO] Spark Project External Flume ....................... SUCCESS [ 14.953 s]
[INFO] Spark Project External Flume Assembly .............. SUCCESS [  5.518 s]
[INFO] Spark Project External MQTT ........................ SUCCESS [ 53.497 s]
[INFO] Spark Project External MQTT Assembly ............... SUCCESS [ 51.715 s]
[INFO] Spark Project External ZeroMQ ...................... SUCCESS [ 27.235 s]
[INFO] Spark Project External Kafka ....................... SUCCESS [ 15.628 s]
[INFO] Spark Project Examples ............................. SUCCESS [02:13 min]
[INFO] Spark Project External Kafka Assembly .............. SUCCESS [ 11.596 s]
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 30:52 min
[INFO] Finished at: 2016-06-27T18:11:33+08:00
[INFO] Final Memory: 104M/1071M
[INFO] ------------------------------------------------------------------------
+ rm -rf /data/spark-1.6.2/dist
+ mkdir -p /data/spark-1.6.2/dist/lib
+ echo 'Spark 1.6.2 built for Hadoop 2.6.0'
+ echo 'Build flags: -Pyarn,hadoop-provided,hadoop-2.6,parquet-provided'
+ cp /data/spark-1.6.2/assembly/target/scala-2.10/spark-assembly-1.6.2-hadoop2.6.0.jar /data/spark-1.6.2/dist/lib/
+ cp /data/spark-1.6.2/examples/target/scala-2.10/spark-examples-1.6.2-hadoop2.6.0.jar /data/spark-1.6.2/dist/lib/
+ cp /data/spark-1.6.2/network/yarn/target/scala-2.10/spark-1.6.2-yarn-shuffle.jar /data/spark-1.6.2/dist/lib/
+ mkdir -p /data/spark-1.6.2/dist/examples/src/main
+ cp -r /data/spark-1.6.2/examples/src/main /data/spark-1.6.2/dist/examples/src/
+ '[' 0 == 1 ']'
+ cp /data/spark-1.6.2/LICENSE /data/spark-1.6.2/dist
+ cp -r /data/spark-1.6.2/licenses /data/spark-1.6.2/dist
+ cp /data/spark-1.6.2/NOTICE /data/spark-1.6.2/dist
+ '[' -e /data/spark-1.6.2/CHANGES.txt ']'
+ cp /data/spark-1.6.2/CHANGES.txt /data/spark-1.6.2/dist
+ cp -r /data/spark-1.6.2/data /data/spark-1.6.2/dist
+ mkdir /data/spark-1.6.2/dist/conf
+ cp /data/spark-1.6.2/conf/docker.properties.template /data/spark-1.6.2/conf/fairscheduler.xml.template /data/spark-1.6.2/conf/log4j.properties.template /data/spark-1.6.2/conf/metrics.properties.template /data/spark-1.6.2/conf/slaves.template /data/spark-1.6.2/conf/spark-defaults.conf.template /data/spark-1.6.2/conf/spark-env.sh.template /data/spark-1.6.2/dist/conf
+ cp /data/spark-1.6.2/README.md /data/spark-1.6.2/dist
+ cp -r /data/spark-1.6.2/bin /data/spark-1.6.2/dist
+ cp -r /data/spark-1.6.2/python /data/spark-1.6.2/dist
+ cp -r /data/spark-1.6.2/sbin /data/spark-1.6.2/dist
+ cp -r /data/spark-1.6.2/ec2 /data/spark-1.6.2/dist
+ '[' -d /data/spark-1.6.2/R/lib/SparkR ']'
+ '[' false == true ']'
+ '[' true == true ']'
+ TARDIR_NAME=spark-1.6.2-bin-hadoop2-without-hive
+ TARDIR=/data/spark-1.6.2/spark-1.6.2-bin-hadoop2-without-hive
+ rm -rf /data/spark-1.6.2/spark-1.6.2-bin-hadoop2-without-hive
+ cp -r /data/spark-1.6.2/dist /data/spark-1.6.2/spark-1.6.2-bin-hadoop2-without-hive
+ tar czf spark-1.6.2-bin-hadoop2-without-hive.tgz -C /data/spark-1.6.2 spark-1.6.2-bin-hadoop2-without-hive
+ rm -rf /data/spark-1.6.2/spark-1.6.2-bin-hadoop2-without-hive
```

# required
 ** hive-2.1.0支持spark-1.6.0 **

# Configuring Hive
1、环境变量中配置spark_home
```
[root@bigdata-server-1 cloud]# echo $SPARK_HOME
/opt/cloud/hive-on-spark
```

2、进入hive-cli命令行，使用set的方式设置以下参数，也可在hive-site.xml中配置
```
set spark.home = /opt/cloud/hive-on-spark;
add jar /opt/cloud/hive-on-spark/lib/spark-assembly-1.6.2-hadoop2.6.0.jar;
set spark.master=yarn-client;  //默认即为yarn-client模式
set hive.execution.engine=spark;
set spark.eventLog.enabled=true;
set spark.eventLog.dir=hdfs://bigdata-server-1:8020/tmp/sparkeventlog;
set spark.executor.memory=1g; 
set spark.executor.instances=10;  //executor数量
set spark.driver.memory=1g; 
set spark.serializer=org.apache.spark.serializer.KryoSerializer;
```

3、执行sql测试spark引擎
```

```


