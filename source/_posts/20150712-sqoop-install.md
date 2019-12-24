---
title: sqoop install
date: 2015-07-12 18:40:13
description: SQOOP 的安装与使用
category: BigData
tags: sqoop
---
# 1.安装
 对应hadoop版本下载，目前我们使用的是hadoop2.x版本
 `wget http://mirrors.cnnic.cn/apache/sqoop/1.4.6/sqoop-1.4.6.bin__hadoop-2.0.4-alpha.tar.gz`

  我们使用的版本是sqoop-1.4.3.bin__hadoop-1.0.0.tar.gz，打算安装在/usr/local目录下。

  首先就是解压缩，重命名为sqoop，然后在文件/etc/profile中设置环境变量SQOOP_HOME。

  把mysql的jdbc驱动mysql-connector-java-5.1.10.jar复制到sqoop项目的lib目录下。

#2.重命名配置文件
   在${SQOOP_HOME}/conf中执行命令

   mv  sqoop-env-template.sh  sqoop-env.sh
   在conf目录下，有两个文件sqoop-site.xml和sqoop-site-template.   xml内容是完全一样的，不必在意，我们只关心sqoop-site.xml即可。

# 3.修改配置文件sqoop-env.sh

内容如下
```
    #Set path to where bin/hadoop is available
    export HADOOP_COMMON_HOME=/usr/local/hadoop/

    #Set path to where hadoop-*-core.jar is available
    export HADOOP_MAPRED_HOME=/usr/local/hadoop

    #set the path to where bin/hbase is available
    export HBASE_HOME=/usr/local/hbase

    #Set the path to where bin/hive is available
    export HIVE_HOME=/usr/local/hive

    #Set the path for where zookeper config dir is
    export ZOOCFGDIR=/usr/local/zk
```


