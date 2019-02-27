---
title: Cloudera-manager-installaction
date: 2015-07-10 16:44:18
category: Monitoring
tags: cloudera
---
 Cloudera提出了Hybrid Open Source的架构：核心组件名称叫CDH（Cloudera's Distribution including Apache Hadoop），开源免费并与Apache社区同步，用户无限制使用，保证Hadoop基本功能持续可用，不会被厂家绑定；数据治理和系统管理组件闭源且需要商业许可，支持客户可以更好更方便的使用Hadoop技术，如部署安全策略等。Cloudera也在商业组件部分提供在企业生产环境中运行Hadoop所必需的运维功能，而这些功能并不被开源社区所覆盖，如无宕机滚动升级、异步灾备等。

* 1: Cloudera-manager-installaction

# 1、基本环境准备
	[hadoop@hadoop html]$ sudo chkconfig iptables off   禁用防火墙
	[hadoop@hadoop html]$ vi /etc/selinux/config 		禁用selinux,SELINUX=disabled

	注：保存重启系统

# 2、Cloudera Manager的离线安装包下载,构建CM本地源
```
[hsu@apache-server html]$ tree cm5/
cm5/
|-- installer
|   |-- 5.4.7 -> latest
|   `-- latest
|       `-- cloudera-manager-installer.bin
`-- redhat
    `-- 6
        `-- x86_64
            `-- cm
                |-- 5 -> 5.4.7
                |-- 5.2.0
                |   |-- RPMS
                |   |   `-- x86_64
                |   |       |-- cloudera-manager-agent-5.2.0-1.cm520.p0.60.el6.x86_64.rpm
                |   |       |-- cloudera-manager-daemons-5.2.0-1.cm520.p0.60.el6.x86_64.rpm
                |   |       |-- cloudera-manager-server-5.2.0-1.cm520.p0.60.el6.x86_64.rpm
                |   |       |-- cloudera-manager-server-db-2-5.2.0-1.cm520.p0.60.el6.x86_64.rpm
                |   |       |-- enterprise-debuginfo-5.2.0-1.cm520.p0.60.el6.x86_64.rpm
                |   |       |-- jdk-6u31-linux-amd64.rpm
                |   |       |-- oracle-j2sdk1.7-1.7.0+update45-1.x86_64.rpm
                |   |       `-- oracle-j2sdk1.7-1.7.0+update67-1.x86_64.rpm
                |   `-- repodata
                |       |-- filelists.xml.gz
                |       |-- filelists.xml.gz.asc
                |       |-- other.xml.gz
                |       |-- other.xml.gz.asc
                |       |-- primary.xml.asc
                |       |-- primary.xml.gz
                |       |-- repomd.xml
                |       `-- repomd.xml.asc
                |-- 5.4.7
                |   |-- RPMS
                |   |   |-- noarch
                |   |   `-- x86_64
                |   |       |-- cloudera-manager-agent-5.4.7-1.cm547.p0.10.el6.x86_64.rpm
                |   |       |-- cloudera-manager-daemons-5.4.7-1.cm547.p0.10.el6.x86_64.rpm
                |   |       |-- cloudera-manager-server-5.4.7-1.cm547.p0.10.el6.x86_64.rpm
                |   |       |-- cloudera-manager-server-db-2-5.4.7-1.cm547.p0.10.el6.x86_64.rpm
                |   |       |-- enterprise-debuginfo-5.4.7-1.cm547.p0.10.el6.x86_64.rpm
                |   |       |-- jdk-6u31-linux-amd64.rpm
                |   |       `-- oracle-j2sdk1.7-1.7.0+update67-1.x86_64.rpm
                |   |-- mirrors
                |   `-- repodata
                |       |-- filelists.xml.gz
                |       |-- filelists.xml.gz.txt
                |       |-- other.xml.gz
                |       |-- other.xml.gz.txt
                |       |-- primary.xml.gz
                |       |-- primary.xml.gz.txt
                |       |-- repomd.xml
                |       `-- repomd.xml.txt
                |-- RPM-GPG-KEY-cloudera
                `-- cloudera-manager.repo

17 directories, 35 files

[hsu@yndx-bigdata-web01 html]$ tree cdh5/
cdh5/
|-- parcels
|   |-- 5 -> 5.4.7
|   |-- 5.2.0.36
|   |   |-- CDH-5.2.0-1.cdh5.2.0.p0.36-el6.parcel
|   |   `-- manifest.json
|   |-- 5.4.7
|   |   |-- CDH-5.4.7-1.cdh5.4.7.p0.3-el5.parcel
|   |   |-- CDH-5.4.7-1.cdh5.4.7.p0.3-el5.parcel.sha1
|   |   |-- CDH-5.4.7-1.cdh5.4.7.p0.3-el6.parcel
|   |   |-- CDH-5.4.7-1.cdh5.4.7.p0.3-el6.parcel.sha1
|   |   |-- CDH-5.4.7-1.cdh5.4.7.p0.3-precise.parcel
|   |   |-- CDH-5.4.7-1.cdh5.4.7.p0.3-precise.parcel.sha1
|   |   |-- CDH-5.4.7-1.cdh5.4.7.p0.3-sles11.parcel
|   |   |-- CDH-5.4.7-1.cdh5.4.7.p0.3-sles11.parcel.sha1
|   |   |-- CDH-5.4.7-1.cdh5.4.7.p0.3-trusty.parcel
|   |   |-- CDH-5.4.7-1.cdh5.4.7.p0.3-trusty.parcel.sha1
|   |   |-- CDH-5.4.7-1.cdh5.4.7.p0.3-wheezy.parcel
|   |   |-- CDH-5.4.7-1.cdh5.4.7.p0.3-wheezy.parcel.sha1
|   |   `-- manifest.json
|   `-- latest -> 5.4.7
`-- redhat
    `-- 6
        `-- x86_64
            `-- cdh
                |-- 5 -> 5.4.7
                |-- 5.4 -> 5.4.7
                |-- 5.4.7
                |   |-- RPMS
                |   |   |-- noarch
                |   |   |   |-- avro-doc-1.7.6+cdh5.4.7+96-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- avro-libs-1.7.6+cdh5.4.7+96-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- avro-tools-1.7.6+cdh5.4.7+96-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- bigtop-tomcat-0.7.0+cdh5.4.7+0-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- bigtop-utils-0.7.0+cdh5.4.7+0-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- crunch-0.11.0+cdh5.4.7+75-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- crunch-doc-0.11.0+cdh5.4.7+75-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- flume-ng-1.5.0+cdh5.4.7+136-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- flume-ng-agent-1.5.0+cdh5.4.7+136-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- flume-ng-doc-1.5.0+cdh5.4.7+136-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- hbase-solr-1.5+cdh5.4.7+60-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- hbase-solr-doc-1.5+cdh5.4.7+60-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- hbase-solr-indexer-1.5+cdh5.4.7+60-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- hive-1.1.0+cdh5.4.7+233-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- hive-hbase-1.1.0+cdh5.4.7+233-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- hive-hcatalog-1.1.0+cdh5.4.7+233-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- hive-jdbc-1.1.0+cdh5.4.7+233-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- hive-metastore-1.1.0+cdh5.4.7+233-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- hive-server-1.1.0+cdh5.4.7+233-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- hive-server2-1.1.0+cdh5.4.7+233-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- hive-webhcat-1.1.0+cdh5.4.7+233-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- hive-webhcat-server-1.1.0+cdh5.4.7+233-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- kite-1.0.0+cdh5.4.7+39-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- llama-1.0.0+cdh5.4.7+0-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- llama-doc-1.0.0+cdh5.4.7+0-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- llama-master-1.0.0+cdh5.4.7+0-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- mahout-0.9+cdh5.4.7+27-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- mahout-doc-0.9+cdh5.4.7+27-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- oozie-4.1.0+cdh5.4.7+151-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- oozie-client-4.1.0+cdh5.4.7+151-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- parquet-1.5.0+cdh5.4.7+99-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- parquet-format-2.1.0+cdh5.4.7+15-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- pig-0.12.0+cdh5.4.7+67-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- pig-udf-datafu-1.1.0+cdh5.4.7+24-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- search-1.0.0+cdh5.4.7+0-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- sentry-1.4.0+cdh5.4.7+179-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- sentry-hdfs-plugin-1.4.0+cdh5.4.7+179-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- sentry-store-1.4.0+cdh5.4.7+179-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- solr-4.10.3+cdh5.4.7+269-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- solr-crunch-1.0.0+cdh5.4.7+0-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- solr-doc-4.10.3+cdh5.4.7+269-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- solr-mapreduce-1.0.0+cdh5.4.7+0-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- solr-server-4.10.3+cdh5.4.7+269-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- spark-core-1.3.0+cdh5.4.7+50-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- spark-history-server-1.3.0+cdh5.4.7+50-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- spark-master-1.3.0+cdh5.4.7+50-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- spark-python-1.3.0+cdh5.4.7+50-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- spark-worker-1.3.0+cdh5.4.7+50-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- sqoop-1.4.5+cdh5.4.7+116-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- sqoop-metastore-1.4.5+cdh5.4.7+116-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- sqoop2-1.99.5+cdh5.4.7+40-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- sqoop2-client-1.99.5+cdh5.4.7+40-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   |-- sqoop2-server-1.99.5+cdh5.4.7+40-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   |   `-- whirr-0.9.0+cdh5.4.7+20-1.cdh5.4.7.p0.3.el6.noarch.rpm
                |   |   `-- x86_64
                |   |       |-- bigtop-jsvc-0.6.0+cdh5.4.7+680-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- bigtop-jsvc-debuginfo-0.6.0+cdh5.4.7+680-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hadoop-0.20-conf-pseudo-2.6.0+cdh5.4.7+642-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hadoop-0.20-mapreduce-2.6.0+cdh5.4.7+642-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hadoop-0.20-mapreduce-jobtracker-2.6.0+cdh5.4.7+642-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hadoop-0.20-mapreduce-jobtrackerha-2.6.0+cdh5.4.7+642-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hadoop-0.20-mapreduce-tasktracker-2.6.0+cdh5.4.7+642-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hadoop-0.20-mapreduce-zkfc-2.6.0+cdh5.4.7+642-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hadoop-2.6.0+cdh5.4.7+642-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hadoop-client-2.6.0+cdh5.4.7+642-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hadoop-conf-pseudo-2.6.0+cdh5.4.7+642-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hadoop-debuginfo-2.6.0+cdh5.4.7+642-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hadoop-doc-2.6.0+cdh5.4.7+642-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hadoop-hdfs-2.6.0+cdh5.4.7+642-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hadoop-hdfs-datanode-2.6.0+cdh5.4.7+642-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hadoop-hdfs-fuse-2.6.0+cdh5.4.7+642-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hadoop-hdfs-journalnode-2.6.0+cdh5.4.7+642-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hadoop-hdfs-namenode-2.6.0+cdh5.4.7+642-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hadoop-hdfs-nfs3-2.6.0+cdh5.4.7+642-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hadoop-hdfs-secondarynamenode-2.6.0+cdh5.4.7+642-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hadoop-hdfs-zkfc-2.6.0+cdh5.4.7+642-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hadoop-httpfs-2.6.0+cdh5.4.7+642-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hadoop-kms-2.6.0+cdh5.4.7+642-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hadoop-kms-server-2.6.0+cdh5.4.7+642-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hadoop-libhdfs-2.6.0+cdh5.4.7+642-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hadoop-libhdfs-devel-2.6.0+cdh5.4.7+642-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hadoop-mapreduce-2.6.0+cdh5.4.7+642-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hadoop-mapreduce-historyserver-2.6.0+cdh5.4.7+642-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hadoop-yarn-2.6.0+cdh5.4.7+642-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hadoop-yarn-nodemanager-2.6.0+cdh5.4.7+642-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hadoop-yarn-proxyserver-2.6.0+cdh5.4.7+642-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hadoop-yarn-resourcemanager-2.6.0+cdh5.4.7+642-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hbase-1.0.0+cdh5.4.7+183-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hbase-doc-1.0.0+cdh5.4.7+183-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hbase-master-1.0.0+cdh5.4.7+183-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hbase-regionserver-1.0.0+cdh5.4.7+183-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hbase-rest-1.0.0+cdh5.4.7+183-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hbase-thrift-1.0.0+cdh5.4.7+183-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hue-3.7.0+cdh5.4.7+1298-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hue-beeswax-3.7.0+cdh5.4.7+1298-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hue-common-3.7.0+cdh5.4.7+1298-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hue-doc-3.7.0+cdh5.4.7+1298-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hue-hbase-3.7.0+cdh5.4.7+1298-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hue-impala-3.7.0+cdh5.4.7+1298-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hue-pig-3.7.0+cdh5.4.7+1298-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hue-plugins-3.7.0+cdh5.4.7+1298-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hue-rdbms-3.7.0+cdh5.4.7+1298-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hue-search-3.7.0+cdh5.4.7+1298-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hue-security-3.7.0+cdh5.4.7+1298-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hue-server-3.7.0+cdh5.4.7+1298-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hue-spark-3.7.0+cdh5.4.7+1298-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hue-sqoop-3.7.0+cdh5.4.7+1298-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- hue-zookeeper-3.7.0+cdh5.4.7+1298-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- impala-2.2.0+cdh5.4.7+0-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- impala-catalog-2.2.0+cdh5.4.7+0-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- impala-debuginfo-2.2.0+cdh5.4.7+0-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- impala-server-2.2.0+cdh5.4.7+0-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- impala-shell-2.2.0+cdh5.4.7+0-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- impala-state-store-2.2.0+cdh5.4.7+0-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- impala-udf-devel-2.2.0+cdh5.4.7+0-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- zookeeper-3.4.5+cdh5.4.7+96-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- zookeeper-debuginfo-3.4.5+cdh5.4.7+96-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       |-- zookeeper-native-3.4.5+cdh5.4.7+96-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |       `-- zookeeper-server-3.4.5+cdh5.4.7+96-1.cdh5.4.7.p0.3.el6.x86_64.rpm
                |   |-- SRPMS
                |   |   |-- avro-libs-1.7.6+cdh5.4.7+96-1.cdh5.4.7.p0.3.src.rpm
                |   |   |-- bigtop-jsvc-0.6.0+cdh5.4.7+680-1.cdh5.4.7.p0.3.src.rpm
                |   |   |-- bigtop-tomcat-0.7.0+cdh5.4.7+0-1.cdh5.4.7.p0.3.src.rpm
                |   |   |-- bigtop-utils-0.7.0+cdh5.4.7+0-1.cdh5.4.7.p0.3.src.rpm
                |   |   |-- crunch-0.11.0+cdh5.4.7+75-1.cdh5.4.7.p0.3.src.rpm
                |   |   |-- flume-ng-1.5.0+cdh5.4.7+136-1.cdh5.4.7.p0.3.src.rpm
                |   |   |-- hadoop-2.6.0+cdh5.4.7+642-1.cdh5.4.7.p0.3.src.rpm
                |   |   |-- hbase-1.0.0+cdh5.4.7+183-1.cdh5.4.7.p0.3.src.rpm
                |   |   |-- hbase-solr-1.5+cdh5.4.7+60-1.cdh5.4.7.p0.3.src.rpm
                |   |   |-- hive-1.1.0+cdh5.4.7+233-1.cdh5.4.7.p0.3.src.rpm
                |   |   |-- hue-3.7.0+cdh5.4.7+1298-1.cdh5.4.7.p0.3.src.rpm
                |   |   |-- impala-2.2.0+cdh5.4.7+0-1.cdh5.4.7.p0.3.src.rpm
                |   |   |-- kite-1.0.0+cdh5.4.7+39-1.cdh5.4.7.p0.3.src.rpm
                |   |   |-- llama-1.0.0+cdh5.4.7+0-1.cdh5.4.7.p0.3.src.rpm
                |   |   |-- mahout-0.9+cdh5.4.7+27-1.cdh5.4.7.p0.3.src.rpm
                |   |   |-- oozie-4.1.0+cdh5.4.7+151-1.cdh5.4.7.p0.3.src.rpm
                |   |   |-- parquet-1.5.0+cdh5.4.7+99-1.cdh5.4.7.p0.3.src.rpm
                |   |   |-- parquet-format-2.1.0+cdh5.4.7+15-1.cdh5.4.7.p0.3.src.rpm
                |   |   |-- pig-0.12.0+cdh5.4.7+67-1.cdh5.4.7.p0.3.src.rpm
                |   |   |-- pig-udf-datafu-1.1.0+cdh5.4.7+24-1.cdh5.4.7.p0.3.src.rpm
                |   |   |-- search-1.0.0+cdh5.4.7+0-1.cdh5.4.7.p0.3.src.rpm
                |   |   |-- sentry-1.4.0+cdh5.4.7+179-1.cdh5.4.7.p0.3.src.rpm
                |   |   |-- solr-4.10.3+cdh5.4.7+269-1.cdh5.4.7.p0.3.src.rpm
                |   |   |-- spark-core-1.3.0+cdh5.4.7+50-1.cdh5.4.7.p0.3.src.rpm
                |   |   |-- sqoop-1.4.5+cdh5.4.7+116-1.cdh5.4.7.p0.3.src.rpm
                |   |   |-- sqoop2-1.99.5+cdh5.4.7+40-1.cdh5.4.7.p0.3.src.rpm
                |   |   |-- whirr-0.9.0+cdh5.4.7+20-1.cdh5.4.7.p0.3.src.rpm
                |   |   `-- zookeeper-3.4.5+cdh5.4.7+96-1.cdh5.4.7.p0.3.src.rpm
                |   |-- mirrors
                |   `-- repodata
                |       |-- filelists.xml.gz
                |       |-- filelists.xml.gz.asc
                |       |-- other.xml.gz
                |       |-- other.xml.gz.asc
                |       |-- primary.xml.gz
                |       |-- primary.xml.gz.asc
                |       |-- repomd.xml
                |       `-- repomd.xml.asc
                |-- RPM-GPG-KEY-cloudera
                `-- cloudera-cdh5.repo

20 directories, 185 files

#创建软连接
cd /var/www/cdh5/parcels
ln -s 5.4.1 5

cd /var/www/cm5/redhat/6/x86_64/cm
# ln -s 5.4.1 5 

# mkdir /var/www/redhat/cdh/ -p

# cp cm5/redhat/6/x86_64/cm/RPM-GPG-KEY-cloudera redhat/cdh/

[root@apache-server www]# tree redhat/
redhat/
+-- cdh
    +-- RPM-GPG-KEY-cloudera

1 directory, 1 file
```

![](https://www.itweet.cn/screenshots/yum-local.png)

	说明：要在生产系统部署CDH，先要实现Cloudera Manager的离线安装，安装好Cloudera Manager后，还要通过Cloudera Manager执行CDH的离线安装两个步骤。由于生产环境的封闭性以及国内网络环境，这些离线包很难从Cloudera的官方网站下载，所以需要将Cloudera的官方网站下载地址映射到本地IP。

# 3、配置一个http服务
```
	[root@apache-server html]$ sudo /etc/init.d/httpd start		启动httpd服务
	[hadoop@apache-server html]$ chkconfig --list httpd 检查httpd服务开机启动情况
	[hadoop@apache-server html]$ ps -ef|grep apache	查看此服务是否启动
```
		

`注：我们把CM安装需要的包都放到这个服务根目录下面了。`

# 4、配置本地映射ip到这个httpd服务
	
	[root@apache-server html]$ cat /etc/hosts
	
	192.168.2.200   server1
	192.168.2.201   server2
	192.168.2.202   server3
	192.168.2.203   server4

	192.168.2.124     archive.cloudera.com
	192.168.2.124     archive-primary.cloudera.com

	http://archive.cloudera.com/cm5/redhat/6/x86_64/cm/  在本地机器输入这个地址能访问到你搭建的这个本地源库

	注：注意映射地址是在所有要按照cdh的机器上配置，如果要验证是否大家离线源成功，请在windows本地hosts文件映射安装源地址，浏览器地址即可验证。

# 5、通过parcel方式安装CDH集群
  `如果选择rpm包安装cdh集群，那么请下载相关rpm包放到相应的apache服务器！`
```
[root@apache-server www]# tree cdh5/
cdh5/
`-- parcels
    `-- 5.4.1
        |-- CDH-5.4.1-1.cdh5.4.1.p0.6-el5.parcel
        |-- CDH-5.4.1-1.cdh5.4.1.p0.6-el5.parcel.sha1
        |-- CDH-5.4.1-1.cdh5.4.1.p0.6-el6.parcel
        |-- CDH-5.4.1-1.cdh5.4.1.p0.6-el6.parcel.sha1
        |-- CDH-5.4.1-1.cdh5.4.1.p0.6-precise.parcel
        |-- CDH-5.4.1-1.cdh5.4.1.p0.6-precise.parcel.sha1
        |-- CDH-5.4.1-1.cdh5.4.1.p0.6-sles11.parcel
        |-- CDH-5.4.1-1.cdh5.4.1.p0.6-sles11.parcel.sha1
        |-- CDH-5.4.1-1.cdh5.4.1.p0.6-trusty.parcel
        |-- CDH-5.4.1-1.cdh5.4.1.p0.6-trusty.parcel.sha1
        |-- CDH-5.4.1-1.cdh5.4.1.p0.6-wheezy.parcel
        |-- CDH-5.4.1-1.cdh5.4.1.p0.6-wheezy.parcel.sha1
        `-- manifest.json

2 directories, 13 files
```

# 6、安装要的软件
```
  rpm -qa | grep mysql 		检查是否安装mysql
  rpm -e mysql-libs-5.1.71-1.el6.x86_64  	卸载
  rpm -e mysql-libs-5.1.71-1.el6.x86_64 --nodeps   强制卸载
  rpm -qa | grep mysql 	检查是否卸载
  rpm -i MySQL-server-5.5.40-1.linux2.6.x86_64.rpm    安装mysql
  mysqld_safe & 	启动mysql服务端
  rpm -i MySQL-client-5.5.40-1.linux2.6.x86_64.rpm  安装客户端
  mysql_secure_installation  修改密码以及初始化信息
  mysql -uroot -padmin 	登录
  sudo yum install mysql-connector-java


--mysql--
mysqladmin -u root password admin
mysql -uroot -padmin -e "
create database hive;
create database rman;
create database oozie;
grant all on hive.* to 'root'@'server1' identified by 'admin';
grant all on rman.* to 'root'@'server1' identified by 'admin';
grant all on oozie.* to 'root'@'server1' identified by 'admin';
flush privileges;
"
```

```  
--install jdk--
  tar -zxvf jdk-7u45-linux-x64.tar.gz -C ../  解压
  

--install cm--
  chmod u+x cloudera-manager-installer.bin    修改权限为可执行
  ./cloudera-manager-installer.bin  			安装CM

  [root@server1 installpackage]# cat /var/log/cloudera-manager-installer/4.install-cloudera-manager-server-db-2.log

  安装报错：Error: Package: cloudera-manager-server-db-2-5.0.0-1.cm500.p0.215.el6.x86_64 (cloudera-manager)
           	Requires: postgresql-server >= 8.4

           	解决方法：手动下载rpm文件并按顺序逐个安装，因为CM依赖于postgresql数据库。
			rpm -ivh postgresql-libs-8.4.20-1.el6_5.x86_64.rpm
			rpm -ivh postgresql-8.4.20-1.el6_5.x86_64.rpm  
			rpm -ivh postgresql-server-8.4.20-1.el6_5.x86_64.rpm

  [root@server1 installpackage]# ./cloudera-manager-installer.bin  	再次安装，即可成功

  [root@server1 installpackage]# netstat -an | grep 7180 		查看7180端口是否起来
	tcp        0      0 0.0.0.0:7180                0.0.0.0:*                   LISTEN      
	tcp        0      0 135.32.43.192:7180          135.32.43.209:63901         TIME_WAIT   
	tcp        0      0 135.32.43.192:7180          135.32.43.209:63902         TIME_WAIT   
	tcp        0      0 135.32.43.192:7180          135.32.43.209:63899         TIME_WAIT   
	tcp        0      0 135.32.43.192:7180          135.32.43.209:63895         TIME_WAIT 
```

# 7、安装CM过程报错

	--> Finished Dependency Resolution 
	Error: Package: cloudera-manager-agent-5.3.0-1.cm530.p0.166.el6.x86_64 (cloudera-manager) 
	Requires: fuse-libs 
	Error: Package: cloudera-manager-agent-5.3.0-1.cm530.p0.166.el6.x86_64 (cloudera-manager) 
	Requires: redhat-lsb 
	Error: Package: cloudera-manager-agent-5.3.0-1.cm530.p0.166.el6.x86_64 (cloudera-manager) 
	Requires: cyrus-sasl-gssapi 
	Error: Package: cloudera-manager-agent-5.3.0-1.cm530.p0.166.el6.x86_64 (cloudera-manager) 
	Requires: portmap 
	Error: Package: cloudera-manager-agent-5.3.0-1.cm530.p0.166.el6.x86_64 (cloudera-manager) 
	Requires: fuse 
	You could try using --skip-broken to work around the problem 
	You could try running: rpm -Va --nofiles --nodigest 
	END (1) 
	remote package cloudera-manager-agent could not be installed, giving up waiting for rollback request 

	换为国内源，安装 sudo yum install redhat-lsb -y， sudo yum install -y cyrus-sasl-gssapi portmap,sudo yum install fuse-libs fuse

	$ vi /etc/yum.repos.d/163.repo    #如果没有这个文件，新建一个，切记：$releasever被修改为了6
	[base]
	name=CentOS-$releasever - Base - 163.com
	baseurl=http://mirrors.163.com/centos/6/os/$basearch/
	enabled=1
	gpgcheck=0
	 
	[updates]
	name=CentOS-$releasever - Updates - 163.com
	baseurl=http://mirrors.163.com/centos/6/updates/$basearch/
	enabled=1
	gpgcheck=0
	 
	[extras]
	name=CentOS-$releasever - Extras - 163.com
	baseurl=http://mirrors.163.com/centos/6/extras/$basearch/
	enabled=1
	gpgcheck=0

	[root@server2 yum.repos.d]# yum clean all
	[root@server2 yum.repos.d]# yum makecache    #生成缓存

	[root@server2 yum.repos.d]# yum install redhat-lsb cyrus-sasl-gssapi portmap fuse-libs fuse -y

![last 3](https://www.itweet.cn/screenshots/cm1.png)

![last 2](https://www.itweet.cn/screenshots/cm2.png)
![last 1](https://www.itweet.cn/screenshots/cm3.png)

	至此，CM离线安装已完成！

	注意：如果你和我一样是用笔记本虚拟机搭建，可能会出现内存不够，导致CM挂掉情况请重启CM服务，/etc/init.d/cloudera-scm-server start，/etc/init.d/cloudera-scm-agent start，不得不赞叹，cloudera的强大，你启动CM服务后，文件继续断点开始分发！而不用重新开始。

# 8、在CM界面添加各种hadoop组件
- 通过http://server1:7180/地址登陆，用户名密码amdin/admin

- Add hosts
![](https://www.itweet.cn//screenshots/cm4.png)

- Parcel install
![](https://www.itweet.cn/screenshots/cm5.png)

- install error
```
Error: Package: cloudera-manager-agent-5.4.1-1.cm541.p0.197.el6.x86_64 (cloudera-manager)
Requires: fuse
Error: Package: cloudera-manager-agent-5.4.1-1.cm541.p0.197.el6.x86_64 (cloudera-manager)
Requires: fuse-libs
Error: Package: cloudera-manager-agent-5.4.1-1.cm541.p0.197.el6.x86_64 (cloudera-manager)
Requires: portmap
Error: Package: cloudera-manager-agent-5.4.1-1.cm541.p0.197.el6.x86_64 (cloudera-manager)
Requires: /lib/lsb/init-functions
Error: Package: cloudera-manager-agent-5.4.1-1.cm541.p0.197.el6.x86_64 (cloudera-manager)
Requires: cyrus-sasl-gssapi
You could try using --skip-broken to work around the problem
You could try running: rpm -Va --nofiles --nodigest 
```

`解决`：

```
# mkdir /mnt/cdimg/ && sudo mount -o loop /root/rhel-server-6.7-x86_64-dvd.iso /mnt/cdimg/

# cat /etc/yum.repos.d/local.repo 
[rhel-Local]
name=Red Hat Server
baseurl=file:///mnt/cdimg
enable=1
gpgcheck=0
```

![](https://www.itweet.cn/screenshots/cm6.png)

- 分发 Parcel package
![](https://www.itweet.cn/screenshots/cm7.png)

- install success

See the following vendor resources for more information:
```
  MySQL 5.5: http://dev.mysql.com/doc/refman/5.5/en/backup-and-recovery.html
  MySQL 5.6: http://dev.mysql.com/doc/refman/5.6/en/backup-and-recovery.html
  PostgreSQL 8.4: http://www.postgresql.org/docs/8.4/static/backup.html
  PostgreSQL 9.2: http://www.postgresql.org/docs/9.2/static/backup.html
  PostgreSQL 9.3: http://www.postgresql.org/docs/9.3/static/backup.html
  Oracle 11gR2: http://docs.oracle.com/cd/E11882_01/backup.112/e10642/toc.html
```

### FAQ
问题1：时间需要同步不然会报错，方式， ntpdate time.nist.gov
```
    sudo yum update && sudo yum install ntp && sudo service ntpd start
```

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/
