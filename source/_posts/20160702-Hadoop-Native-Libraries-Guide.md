---
title: Hadoop Native Libraries Guide
date: 2016-07-02 17:12:38
category: BigData
tags: hadoop
---
hadoop Native Shared Libraries 使得Hadoop可以使用多种压缩编码算法，来提高数据的io处理性能。不同的压缩库需要依赖到很多Linux本地共享库文件，社区提供的二进制安装包，默认没有支持snappy这样在生产中最常用的压缩格式。而且社区没有提供64位的二进制安装包，在生产环境中一般都是x86 64位服务器，所以需要自己编译部署包。根据公司情况有一些修改的分支基础构建二进制安装包／rpm包。

我今天介绍，源码编译Hadoop支持多种Native Shared Libraries，编译完成默认支持所有native libraries。

文件压缩主要有两方面的好处：一方面节省文件存储空间；另一方面加速网络数据传输或磁盘读写。当处理大规模的数据时这些效果提升更加明显，因此我们需要仔细斟酌压缩在Hadoop环境下的使用,不同的Hadoop分析引擎对不同的数据压缩和文件格式有不同的性能特点，
请参考:[Hadoop列式存储引擎Parquet/ORC和snappy压缩](https://www.itweet.cn/2016/03/15/columnar-storage-parquet-and-orc/)

![](https://www.itweet.cn/screenshots/hadoop-native.png)

# Components

* The native hadoop library includes various components:
    - Compression Codecs (bzip2, lz4, snappy, zlib)
    
    - Native IO utilities for HDFS Short-Circuit Local Reads and Centralized Cache Management in HDFS
    
    - CRC32 checksum implementation

# Requirements:

```
* Unix System
* JDK 1.7+
* Maven 3.0 or later
* Findbugs 1.3.9 (if running findbugs)
* ProtocolBuffer 2.5.0
* CMake 2.6 or newer (if compiling native code), must be 3.0 or newer on Mac
* Zlib devel (if compiling native code)
* openssl devel ( if compiling native hadoop-pipes and to get the best HDFS encryption performance )
* Jansson C XML parsing library ( if compiling libwebhdfs )
* Linux FUSE (Filesystem in Userspace) version 2.6 or above ( if compiling fuse_dfs )
* Internet connection for first build (to fetch all Maven and Hadoop dependencies)
```

# Installing required 

* Installing required packages for clean install of Centos 6.x Desktop:
  
  Requirements: gcc c++, autoconf, automake, libtool, Java 6,JAVA_HOME set, Maven 3

* Native libraries

```
yum -y gcc c++ install lzo-devel zlib zlib-devel autoconf automake libtool cmake

yum -y install  svn   ncurses-devel 

yum install openssl-devel

yum install ant -y

yum install cmake -y
```

* Maven && JDK 1.7

```
# tail -6 ~/.bash_profile  
export JAVA_HOME=/opt/jdk
export MAVEN_HOME=/opt/maven

export PATH=.:$MAVEN_HOME/bin:$JAVA_HOME/bin:$PATH

export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar

# source ~/.bash_profile

# mvn -v
Apache Maven 3.3.3 (7994120775791599e205a5524ec3e0dfe41d4a06; 2015-04-22T19:57:37+08:00)
Maven home: /opt/maven
Java version: 1.7.0_45, vendor: Oracle Corporation
Java home: /opt/jdk1.7.0_45/jre
Default locale: en_US, platform encoding: UTF-8
OS name: "linux", version: "2.6.32-504.el6.x86_64", arch: "amd64", family: "unix"
```

* ProtocolBuffer 2.5.0 (required)

```
$ tar -zxvf protobuf-2.5.0.tar.gz
$ cd protobuf-2.5.0/
./configure 
make 
make install

$ protoc --version
libprotoc 2.5.0
```

* Optional packages

Snappy compression
```
yum -y install snappy snappy-devel
```

Bzip2
```
yum install bzip2 bzip2-devel bzip2-libs -y
```

Linux FUSE
```
yum install fuse fuse-devel fuse-libs 
```

snappy link
```
$ ls -lh /usr/lib64/ |grep snappy         
lrwxrwxrwx   1 root root   18 Jul  3 21:45 libsnappy.so -> libsnappy.so.1.1.4
lrwxrwxrwx.  1 root root   18 Feb 12 03:08 libsnappy.so.1 -> libsnappy.so.1.1.4
-rwxr-xr-x   1 root root  22K Nov 23  2013 libsnappy.so.1.1.4

ln -sf /usr/lib64/libsnappy.so.1.1.4 /usr/local/lib
ln -sf /usr/lib64/libsnappy.so /usr/local/lib
ln -sf /usr/lib64/libsnappy.so.1 /usr/local/lib

$ ls -lh /usr/local/lib|grep snappy
lrwxrwxrwx 1 root root   23 Jul  9 18:47 libsnappy.so -> /usr/lib64/libsnappy.so
lrwxrwxrwx 1 root root   25 Jul  9 18:47 libsnappy.so.1 -> /usr/lib64/libsnappy.so.1
lrwxrwxrwx 1 root root   29 Jul  9 18:48 libsnappy.so.1.1.4 -> /usr/lib64/libsnappy.so.1.1.4
```

# Building Hadoop in Snappy build

```
$ wget http://mirror.bit.edu.cn/apache/hadoop/common/hadoop-2.7.2/hadoop-2.7.2-src.tar.gz

$ tar -zxf hadoop-2.7.2-src.tar.gz
```

building Hadoop 

```
mvn clean package -DskipTests -Pdist,native -Dtar -Dsnappy.lib=/usr/local/lib -Dbundle.snappy
```

building Hadoop Info

```
main:
     [exec] $ tar cf hadoop-2.7.2.tar hadoop-2.7.2
     [exec] $ gzip -f hadoop-2.7.2.tar
     [exec] 
     [exec] Hadoop dist tar available at: /opt/hadoop-2.7.2-src/hadoop-dist/target/hadoop-2.7.2.tar.gz
     [exec] 
[INFO] Executed tasks
[INFO] 
[INFO] --- maven-javadoc-plugin:2.8.1:jar (module-javadocs) @ hadoop-dist ---
[INFO] Building jar: /opt/hadoop-2.7.2-src/hadoop-dist/target/hadoop-dist-2.7.2-javadoc.jar
[INFO] ------------------------------------------------------------------------
[INFO] Reactor Summary:
[INFO] 
[INFO] Apache Hadoop Main ................................. SUCCESS [  4.046 s]
[INFO] Apache Hadoop Project POM .......................... SUCCESS [  3.147 s]
[INFO] Apache Hadoop Annotations .......................... SUCCESS [  6.948 s]
[INFO] Apache Hadoop Assemblies ........................... SUCCESS [  0.382 s]
[INFO] Apache Hadoop Project Dist POM ..................... SUCCESS [  2.768 s]
[INFO] Apache Hadoop Maven Plugins ........................ SUCCESS [  4.699 s]
[INFO] Apache Hadoop MiniKDC .............................. SUCCESS [  5.243 s]
[INFO] Apache Hadoop Auth ................................. SUCCESS [  7.649 s]
[INFO] Apache Hadoop Auth Examples ........................ SUCCESS [  4.101 s]
[INFO] Apache Hadoop Common ............................... SUCCESS [02:50 min]
[INFO] Apache Hadoop NFS .................................. SUCCESS [  9.580 s]
[INFO] Apache Hadoop KMS .................................. SUCCESS [ 18.977 s]
[INFO] Apache Hadoop Common Project ....................... SUCCESS [  0.037 s]
[INFO] Apache Hadoop HDFS ................................. SUCCESS [04:24 min]
[INFO] Apache Hadoop HttpFS ............................... SUCCESS [ 24.689 s]
[INFO] Apache Hadoop HDFS BookKeeper Journal .............. SUCCESS [  8.890 s]
[INFO] Apache Hadoop HDFS-NFS ............................. SUCCESS [  6.085 s]
[INFO] Apache Hadoop HDFS Project ......................... SUCCESS [  0.684 s]
[INFO] hadoop-yarn ........................................ SUCCESS [  0.209 s]
[INFO] hadoop-yarn-api .................................... SUCCESS [02:27 min]
[INFO] hadoop-yarn-common ................................. SUCCESS [ 48.704 s]
[INFO] hadoop-yarn-server ................................. SUCCESS [  0.150 s]
[INFO] hadoop-yarn-server-common .......................... SUCCESS [ 18.128 s]
[INFO] hadoop-yarn-server-nodemanager ..................... SUCCESS [ 28.898 s]
[INFO] hadoop-yarn-server-web-proxy ....................... SUCCESS [  5.899 s]
[INFO] hadoop-yarn-server-applicationhistoryservice ....... SUCCESS [ 13.665 s]
[INFO] hadoop-yarn-server-resourcemanager ................. SUCCESS [ 31.929 s]
[INFO] hadoop-yarn-server-tests ........................... SUCCESS [  8.038 s]
[INFO] hadoop-yarn-client ................................. SUCCESS [ 12.032 s]
[INFO] hadoop-yarn-server-sharedcachemanager .............. SUCCESS [  4.674 s]
[INFO] hadoop-yarn-applications ........................... SUCCESS [  0.056 s]
[INFO] hadoop-yarn-applications-distributedshell .......... SUCCESS [  3.816 s]
[INFO] hadoop-yarn-applications-unmanaged-am-launcher ..... SUCCESS [  2.328 s]
[INFO] hadoop-yarn-site ................................... SUCCESS [  0.029 s]
[INFO] hadoop-yarn-registry ............................... SUCCESS [  8.030 s]
[INFO] hadoop-yarn-project ................................ SUCCESS [  4.697 s]
[INFO] hadoop-mapreduce-client ............................ SUCCESS [  0.101 s]
[INFO] hadoop-mapreduce-client-core ....................... SUCCESS [ 38.677 s]
[INFO] hadoop-mapreduce-client-common ..................... SUCCESS [ 25.883 s]
[INFO] hadoop-mapreduce-client-shuffle .................... SUCCESS [  6.625 s]
[INFO] hadoop-mapreduce-client-app ........................ SUCCESS [ 15.826 s]
[INFO] hadoop-mapreduce-client-hs ......................... SUCCESS [  9.873 s]
[INFO] hadoop-mapreduce-client-jobclient .................. SUCCESS [  8.766 s]
[INFO] hadoop-mapreduce-client-hs-plugins ................. SUCCESS [  2.425 s]
[INFO] Apache Hadoop MapReduce Examples ................... SUCCESS [  9.849 s]
[INFO] hadoop-mapreduce ................................... SUCCESS [  3.369 s]
[INFO] Apache Hadoop MapReduce Streaming .................. SUCCESS [  6.783 s]
[INFO] Apache Hadoop Distributed Copy ..................... SUCCESS [ 12.602 s]
[INFO] Apache Hadoop Archives ............................. SUCCESS [  2.728 s]
[INFO] Apache Hadoop Rumen ................................ SUCCESS [  9.200 s]
[INFO] Apache Hadoop Gridmix .............................. SUCCESS [  6.542 s]
[INFO] Apache Hadoop Data Join ............................ SUCCESS [  5.351 s]
[INFO] Apache Hadoop Ant Tasks ............................ SUCCESS [  3.234 s]
[INFO] Apache Hadoop Extras ............................... SUCCESS [  4.533 s]
[INFO] Apache Hadoop Pipes ................................ SUCCESS [  9.475 s]
[INFO] Apache Hadoop OpenStack support .................... SUCCESS [  6.788 s]
[INFO] Apache Hadoop Amazon Web Services support .......... SUCCESS [09:42 min]
[INFO] Apache Hadoop Azure support ........................ SUCCESS [ 41.264 s]
[INFO] Apache Hadoop Client ............................... SUCCESS [ 14.762 s]
[INFO] Apache Hadoop Mini-Cluster ......................... SUCCESS [  0.065 s]
[INFO] Apache Hadoop Scheduler Load Simulator ............. SUCCESS [  6.579 s]
[INFO] Apache Hadoop Tools Dist ........................... SUCCESS [ 16.842 s]
[INFO] Apache Hadoop Tools ................................ SUCCESS [  0.026 s]
[INFO] Apache Hadoop Distribution ......................... SUCCESS [ 45.423 s]
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 29:44 min
[INFO] Finished at: 2016-07-10T00:28:58+08:00
[INFO] Final Memory: 148M/667M
[INFO] ------------------------------------------------------------------------
```

# Hadoop Native checknative

```
# hadoop checknative -a

16/07/10 00:37:01 INFO bzip2.Bzip2Factory: Successfully loaded & initialized native-bzip2 library system-native
16/07/10 00:37:01 INFO zlib.ZlibFactory: Successfully loaded & initialized native-zlib library
Native library checking:
hadoop:  true /opt/hadoop-2.7.2/lib/native/libhadoop.so.1.0.0
zlib:    true /lib64/libz.so.1
snappy:  true /opt/hadoop-2.7.2/lib/native/libsnappy.so.1
lz4:     true revision:99
bzip2:   true /lib64/libbz2.so.1
openssl: true /usr/lib64/libcrypto.so
```

# Deploy hadoop 2.7.2
 参考Hadoop部署安装文档。
```
[root@bigdata-server-1 cloud]# hadoop checknative -a
16/07/10 18:39:48 INFO bzip2.Bzip2Factory: Successfully loaded & initialized native-bzip2 library system-native
16/07/10 18:39:48 INFO zlib.ZlibFactory: Successfully loaded & initialized native-zlib library
Native library checking:
hadoop:  true /opt/cloud/hadoop-2.7.2/lib/native/libhadoop.so.1.0.0
zlib:    true /lib64/libz.so.1
snappy:  true /opt/cloud/hadoop-2.7.2/lib/native/libsnappy.so.1
lz4:     true revision:99
bzip2:   true /lib64/libbz2.so.1
openssl: true /usr/lib64/libcrypto.so
```

参考：
    ＊ building hadoop: https://github.com/apache/hadoop/blob/trunk/BUILDING.txt
    ＊ NativeLibraries: http://hadoop.apache.org/docs/r2.7.2/hadoop-project-dist/hadoop-common/NativeLibraries.html


