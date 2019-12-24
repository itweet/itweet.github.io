---
title: building hadoop for centos
date: 2015-07-27 09:24:19
category: BigData
tags: hadoop
---
# 1、获取hadoop源码
```
wget http://apache.fayea.com/hadoop/common/hadoop-2.6.0/hadoop-2.6.0-src.tar.gz
```

# 2、编译hadoop所需环境

`# tar -zxvf hadoop-2.6.0-src.tar.gz `


Build instructions for Hadoop

-------------------------------------------------------------------------------
Requirements:

* Unix System
* JDK 1.6+
* Maven 3.0 or later
* Findbugs 1.3.9 (if running findbugs)
* ProtocolBuffer 2.5.0
* CMake 2.6 or newer (if compiling native code), must be 3.0 or newer on Mac
* Zlib devel (if compiling native code)
* openssl devel ( if compiling native hadoop-pipes )
* Internet connection for first build (to fetch all Maven and Hadoop dependencies)

安装：
- JDK 1.7.0_75和Maven 3.0.5都已经安装好并配置了环境变量，直接开始安装其他依赖。
- Findbugs
- ProtocolBuffer
- CMake、Zlib、openssl 
    $ sudo yum -y install gcc gcc-c++ autoconf automake cmake libtool ncurses-devel openssl-devel lzo-devel zlib-devel
-  Snappy 

# 编译

http://hadoop.apache.org/docs/r2.6.0/hadoop-project-dist/hadoop-common/NativeLibraries.html

```
$ export MAVEN_OPTS="-Xms256m -Xmx512m"
$ mvn package -Pdist,native -DskipTests -Dtar -Drequire.snappy

main:
     [exec] $ tar cf hadoop-2.6.0.tar hadoop-2.6.0
     [exec] $ gzip -f hadoop-2.6.0.tar
     [exec] 
     [exec] Hadoop dist tar available at: /usr/local/git/hadoop-2.6.0-src/hadoop-dist/target/hadoop-2.6.0.tar.gz
     [exec] 
[INFO] Executed tasks
[INFO] 
[INFO] --- maven-javadoc-plugin:2.8.1:jar (module-javadocs) @ hadoop-dist ---
[INFO] Building jar: /usr/local/git/hadoop-2.6.0-src/hadoop-dist/target/hadoop-dist-2.6.0-javadoc.jar
[INFO] ------------------------------------------------------------------------
[INFO] Reactor Summary:
[INFO] 
[INFO] Apache Hadoop Main ................................ SUCCESS [2.629s]
[INFO] Apache Hadoop Project POM ......................... SUCCESS [2.143s]
[INFO] Apache Hadoop Annotations ......................... SUCCESS [5.317s]
[INFO] Apache Hadoop Assemblies .......................... SUCCESS [0.523s]
[INFO] Apache Hadoop Project Dist POM .................... SUCCESS [3.057s]
[INFO] Apache Hadoop Maven Plugins ....................... SUCCESS [5.695s]
[INFO] Apache Hadoop MiniKDC ............................. SUCCESS [4.925s]
[INFO] Apache Hadoop Auth ................................ SUCCESS [7.325s]
[INFO] Apache Hadoop Auth Examples ....................... SUCCESS [4.235s]
[INFO] Apache Hadoop Common .............................. SUCCESS [3:01.196s]
[INFO] Apache Hadoop NFS ................................. SUCCESS [21.923s]
[INFO] Apache Hadoop KMS ................................. SUCCESS [27.282s]
[INFO] Apache Hadoop Common Project ...................... SUCCESS [0.035s]
[INFO] Apache Hadoop HDFS ................................ SUCCESS [6:06.008s]
[INFO] Apache Hadoop HttpFS .............................. SUCCESS [1:04.210s]
[INFO] Apache Hadoop HDFS BookKeeper Journal ............. SUCCESS [18.907s]
[INFO] Apache Hadoop HDFS-NFS ............................ SUCCESS [6.766s]
[INFO] Apache Hadoop HDFS Project ........................ SUCCESS [0.032s]
[INFO] hadoop-yarn ....................................... SUCCESS [0.060s]
[INFO] hadoop-yarn-api ................................... SUCCESS [2:03.424s]
[INFO] hadoop-yarn-common ................................ SUCCESS [57.819s]
[INFO] hadoop-yarn-server ................................ SUCCESS [0.180s]
[INFO] hadoop-yarn-server-common ......................... SUCCESS [18.783s]
[INFO] hadoop-yarn-server-nodemanager .................... SUCCESS [34.622s]
[INFO] hadoop-yarn-server-web-proxy ...................... SUCCESS [5.318s]
[INFO] hadoop-yarn-server-applicationhistoryservice ...... SUCCESS [10.880s]
[INFO] hadoop-yarn-server-resourcemanager ................ SUCCESS [33.005s]
[INFO] hadoop-yarn-server-tests .......................... SUCCESS [8.366s]
[INFO] hadoop-yarn-client ................................ SUCCESS [11.520s]
[INFO] hadoop-yarn-applications .......................... SUCCESS [0.162s]
[INFO] hadoop-yarn-applications-distributedshell ......... SUCCESS [4.895s]
[INFO] hadoop-yarn-applications-unmanaged-am-launcher .... SUCCESS [3.499s]
[INFO] hadoop-yarn-site .................................. SUCCESS [0.127s]
[INFO] hadoop-yarn-registry .............................. SUCCESS [10.132s]
[INFO] hadoop-yarn-project ............................... SUCCESS [6.510s]
[INFO] hadoop-mapreduce-client ........................... SUCCESS [0.183s]
[INFO] hadoop-mapreduce-client-core ...................... SUCCESS [41.075s]
[INFO] hadoop-mapreduce-client-common .................... SUCCESS [25.373s]
[INFO] hadoop-mapreduce-client-shuffle ................... SUCCESS [5.812s]
[INFO] hadoop-mapreduce-client-app ....................... SUCCESS [16.379s]
[INFO] hadoop-mapreduce-client-hs ........................ SUCCESS [13.148s]
[INFO] hadoop-mapreduce-client-jobclient ................. SUCCESS [9.226s]
[INFO] hadoop-mapreduce-client-hs-plugins ................ SUCCESS [2.436s]
[INFO] Apache Hadoop MapReduce Examples .................. SUCCESS [9.628s]
[INFO] hadoop-mapreduce .................................. SUCCESS [6.813s]
[INFO] Apache Hadoop MapReduce Streaming ................. SUCCESS [7.435s]
[INFO] Apache Hadoop Distributed Copy .................... SUCCESS [11.833s]
[INFO] Apache Hadoop Archives ............................ SUCCESS [2.964s]
[INFO] Apache Hadoop Rumen ............................... SUCCESS [9.944s]
[INFO] Apache Hadoop Gridmix ............................. SUCCESS [6.646s]
[INFO] Apache Hadoop Data Join ........................... SUCCESS [5.549s]
[INFO] Apache Hadoop Ant Tasks ........................... SUCCESS [3.227s]
[INFO] Apache Hadoop Extras .............................. SUCCESS [4.833s]
[INFO] Apache Hadoop Pipes ............................... SUCCESS [10.372s]
[INFO] Apache Hadoop OpenStack support ................... SUCCESS [7.556s]
[INFO] Apache Hadoop Amazon Web Services support ......... SUCCESS [18.788s]
[INFO] Apache Hadoop Client .............................. SUCCESS [9.438s]
[INFO] Apache Hadoop Mini-Cluster ........................ SUCCESS [0.216s]
[INFO] Apache Hadoop Scheduler Load Simulator ............ SUCCESS [9.126s]
[INFO] Apache Hadoop Tools Dist .......................... SUCCESS [16.608s]
[INFO] Apache Hadoop Tools ............................... SUCCESS [0.026s]
[INFO] Apache Hadoop Distribution ........................ SUCCESS [1:02.537s]
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 22:54.692s
[INFO] Finished at: Sat Jul 25 08:54:27 CST 2015
[INFO] Final Memory: 140M/458M
[INFO] ------------------------------------------------------------------------

# cd hadoop-dist/target/
# ls hadoop-2.6.0.tar.gz 
hadoop-2.6.0.tar.gz
```

参考：源码文件中BUILDING.txt文件！

