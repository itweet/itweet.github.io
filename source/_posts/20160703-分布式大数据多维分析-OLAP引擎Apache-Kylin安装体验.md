---
title: 分布式大数据多维分析（OLAP）引擎Apache Kylin安装体验
date: 2016-07-03 17:21:35
category: BigData
tags: kylin
---
Apache Kylin旨在减少Hadoop在10亿及百亿规模以上数据级别的情况下的查询延迟，目前底层数据存储基于HBase，具有较强的可伸缩性。

# 环境依赖
  + hadoop-2.7.1
  + hbase-1.1.5
  + apache-hive-2.0.1-bin

# 配置环境变量

下载kylin基于hbase1.x的部署包
```
wget https://dist.apache.org/repos/dist/release/kylin/apache-kylin-1.5.2.1/apache-kylin-1.5.2.1-bin.tar.gz
```

配置kylin环境变量
```
$ cat scripts/hadoop.sh 
export HADOOP_HOME=/opt/cloud/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

$ cat scripts/hive.sh 
export HIVE_HOME=/opt/cloud/hive
export HCAT_HOME=$HIVE_HOME/hcatalog
export HIVE_CONF=$HIVE_HOME/conf
export PATH=$PATH:$HIVE_HOME/bin:$HIVE_HOME/sbin

$ cat scripts/hbase.sh 
export HBASE_HOME=/opt/cloud/hbase/
export PATH=$PATH:$HBASE_HOME/bin/:$HBASE_HOME/sbin/

$ cat scripts/kylin.sh 
export KYLIN_HOME=/opt/cloud/kylin
export PATH=$PATH:$KYLIN_HOME/bin

$ ln -s /opt/cloud/scripts/kylin.sh /etc/profile.d/kylin.sh
```

# 检查kylin环境
```
$ /opt/cloud/kylin/bin/check-env.sh 
KYLIN_HOME is set to /opt/cloud/kylin
```

working space init...
```
$ WORKING_DIR=`sh $KYLIN_HOME/bin/get-properties.sh kylin.hdfs.working.dir`
$ sudo -uhdfs hadoop fs -mkdir -p $WORKING_DIR    
```

注意下面，hdfs权限，我这里root是超级用户，kylin也安装在root下，所以无权限问题，如果kylin安装在其它非超级用户，需要事先创建目录，赋权此目录给安装启动kylin用户。
```
$ hadoop fs -ls /|grep kylin
drwxr-xr-x   - root supergroup          0 2016-07-03 18:26 /kylin
```

比如：在kylin用户安装启动kylin,hdfs超级用户是hdfs
```
$ su - hdfs

sudo -uhdfs hadoop fs -mkdir /kylin
sudo -uhdfs hadoop fs -chown -R kylin:kylin /kylin
```

# 启动kylin

```
$ kylin.sh start
```

遇到如下问题，hdfs权限不够，而无法创建初始化用户目录：
```
$ hadoop fs -mkdir /user/root
mkdir: Permission denied: user=root, access=WRITE, inode="/user/
root":hdfs:hdfs:drwxr-xr-x

$ sudo -uhdfs hadoop fs -mkdir /user/root    
$ sudo -uhdfs hadoop fs -chown root:hdfs /user/root
$ kylin.sh start
```

启动kylin信息:
```
KYLIN_HOME is set to /opt/cloud/kylin/bin/../
kylin.security.profile is set to testing
Logging initialized using configuration in file:/opt/cloud/apache-hive-2.0.1-bin/conf/hive-log4j2.properties
HIVE_CONF is set to: /opt/cloud/hive/conf, use it to locate hive configurations.
HCAT_HOME is set to: /opt/cloud/hive/hcatalog, use it to find hcatalog path:

hbase dependency: /opt/cloud/hbase/lib/hbase-common-1.1.5.jar
KYLIN_JVM_SETTINGS is -Xms1024M -Xmx4096M -XX:MaxPermSize=128M -verbose:gc -XX:+PrintGCDetails -XX:+PrintGCDateStamps -Xloggc:/opt/cloud/kylin/bin/..//logs/kylin.gc.10205 -XX:+UseGCLogFileRotation -XX:NumberOfGCLogFiles=10 -XX:GCLogFileSize=64M
KYLIN_DEBUG_SETTINGS is not set, will not enable remote debuging
KYLIN_LD_LIBRARY_SETTINGS is not set, Usually it's okay unless you want to specify your own native path
A new Kylin instance is started by root, stop it using "kylin.sh stop"
Please visit http://<ip>:7070/kylin
You can check the log at /opt/cloud/kylin/bin/../logs/kylin.log
```

# 访问kylin web
 - http://bigdata-server-2:7070/kylin/login
 - ADMIN/KYLIN

后台建立好kylin数据库
```
hive> create database kylin;
OK
Time taken: 0.179 seconds

hive> use kylin;
OK
Time taken: 0.047 seconds

hive> create table test_kylin(id int,name string);
OK
Time taken: 0.207 seconds

hive> insert into test_kylin values(1,"kylin");

hive> select * from test_kylin;
OK
1       kylin
Time taken: 0.183 seconds, Fetched: 1 row(s)
```

# Impala-Hive-Performance-tuning
  - 参考本博客另一片文章，自动生成测试数据，然后通过kylin分析
    + https://www.itweet.cn/2016/03/20/Impala-Hive-performance-tuning/

# kylin by cube
  参考：http://kylin.apache.org/cn/docs/tutorial/web.html

# FAQ
`Cube error: org.apache.hadoop.hive.ql.metadata.HiveException: `
`java.lang.RuntimeException: native snappy library not available: this version`
`of libhadoop was built without snappy support.`

日志看到，kylin使用到snappy压缩：

```
SET mapreduce.map.output.compress.codec=org.apache.hadoop.io.compress.SnappyCodec;
SET mapreduce.output.fileoutputformat.compress.codec=org.apache.hadoop.io.compress.SnappyCodec;
```

Checknative snappy

发现，我们编译的时候，没有把各种native库编译进去。

```
$ hadoop checknative
16/07/03 20:51:14 INFO zlib.ZlibFactory: Successfully loaded & initialized native-zlib library
Native library checking:
hadoop:  true /opt/cloud/hadoop-2.7.1/lib/native/libhadoop.so
zlib:    true /lib64/libz.so.1
snappy:  false 
lz4:     true revision:99
bzip2:   false 
openssl: false Cannot load libcrypto.so (libcrypto.so: cannot open shared object file: No such file or directory)!


$ cd /usr/lib64/
$ ln -s libcrypto.so.1.0.1e libcrypto.so

$ hadoop checknative -a
16/07/03 20:57:16 WARN bzip2.Bzip2Factory: Failed to load/initialize native-bzip2 library system-native, will use pure-Java version
16/07/03 20:57:16 INFO zlib.ZlibFactory: Successfully loaded & initialized native-zlib library
Native library checking:
hadoop:  true /opt/cloud/hadoop-2.7.1/lib/native/libhadoop.so
zlib:    true /lib64/libz.so.1
snappy:  false 
lz4:     true revision:99
bzip2:   false 
openssl: true libcrypto.so
16/07/03 20:57:16 INFO util.ExitUtil: Exiting with status 1
```

libsnappy default path
```
$ find / -name libsnappy.so
/usr/lib64/libsnappy.so

ln -sf /usr/lib64/libsnappy.so.1.1.4 /usr/local/lib
ln -sf /usr/lib64/libsnappy.so /usr/local/lib
ln -sf /usr/lib64/libsnappy.so.1 /usr/local/lib
```

snappy package
```
$ yum -y install snappy snappy-devel

$ rpm -qa snappy*
snappy-1.1.0-1.el6.x86_64
snappy-devel-1.1.0-1.el6.x86_64
```

编译Hadoop默认支撑所有native库

> 请参考我的另外一篇文章：[Hadoop-Native-Libraries-Guide](https://www.itweet.cn/2016/07/02/Hadoop-Native-Libraries-Guide/)

参考：
Apache Kylin™: http://kylin.apache.org/
Extreme OLAP Engine for Big Data: http://kylin.apache.org/blog/
Apache Kylin的快速数据立方体算法——概述：http://www.infoq.com/cn/articles/apache-kylin-algorithm/


原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/