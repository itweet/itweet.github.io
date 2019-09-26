---
title: Fql-training
date: 2019-07-10 11:28:30
description: FusionDB FQL Training
tags: [FusionDB®,2019]
category: FusionDB
---

今天，介绍一个快速入门 FusionDB 的一个[GitHub工程](https://github.com/FusionDB/fql-training)，使用 FQL 实现跨不同数据源的联邦查询功能。现提供 Docker 版的 FusionDB，安装有 Docker 的机器都可以快速体验 FusionDB 的功能。

- fql-training: https://github.com/FusionDB/fql-training
- FusionDB Document: http://www.fusionlab.cn/zh-cn/fdb/quickstart.html

# FusionDB FQL Training

**This repository provides a training for FusionDB FQL.**

In this training you will learn to:

* run SQL queries on FusionDB
* run SQL++ queries on FusionDB
* use FusionDB's SQL JDBC Server
* write the result of SQL queries to RDBMS (MySQL、PostgreSQL、Oracle)、S3、ADLS  and HDFS

### Requirements

* Remote HDFS or RDBMS (MySQL、PostgreSQL、Oracle)/S3/ADLS/GCP/OSS etc.
* Optional: Jupyter Notebook、PSequel

You **only need [Docker](https://hub.docker.com/r/fusiondb/fusiondb)** to run this training. </br>
You don't need Java, Scala, or an IDE.

For more information, please refer to [FusionDB Document](http://www.fusionlab.cn/zh-cn/fdb/quickstart.html)

### Quickstart

Fusiondb is a simple and powerful federated database engine.

* Start FusionDB

```
docker run --name fdb -p 54322:54322 -itd fusiondb/fusiondb:0.1.0-beta
```

* Check FusionDB server

```
docker ps -a|grep fdb

lsof -i :54322
```

* Psycopg2 connecting FusionDB

```
import psycopg2
import pandas as pd
connection = psycopg2.connect("host=localhost port=54322 dbname=default user=fdb sslmode=disable")
df = pd.read_sql(sql="SELECT * FROM VALUES (1, 1), (1, 2) AS t(a, b);", con=connection)
df

## Load mysql table

df =pd.read_sql(sql="load 'mysql' options('url'='jdbc:mysql://localhost:53306/fdb_test','dbtable'='person','user'= 'root','password'='root') AS mysql_t2;", con=connection)
df =pd.read_sql(sql="SELECT * FROM mysql_t2;", con=connection)
df.head()

## Load Postgres table

df =pd.read_sql(sql="load 'postgresql' options('url'='jdbc:postgresql://localhost:15430/fdb','dbtable'='person','user'= 'fdb','password'='fdb123') AS gp_t1;", con=connection)
df =pd.read_sql(sql="SELECT * FROM gp_t1;", con=connection)
df.head()


## MySQL Table Join PostgreSQL Table

df =pd.read_sql(sql="CREATE table test as SELECT mysql_t2.* FROM mysql_t2 LEFT JOIN gp_t1 ON mysql_t2.id = gp_t1.id;", con=connection)
df =pd.read_sql(sql="SELECT * FROM test;", con=connection)
df.head()

## Load oracle table 

df =pd.read_sql(sql="load oracle options('url'='jdbc:oracle:thin:SYSTEM/oracle@//localhost:49161/xe','dbtable'='FDBTEST20','user'= 'SYSTEM','password'='oracle') AS ora_t1;", con=connection)
df =pd.read_sql(sql="SELECT * FROM ora_t1 limit 10;", con=connection)
df.head()


## Load HDFS parquet

df =pd.read_sql(sql="load 'hdfs://jdp-1:8020/tmp/spark-tpcds-data/web_site' format parquet AS web_site;", con=connection)
df =pd.read_sql(sql="SELECT * FROM web_site limit 10;", con=connection)
df.head()

## Save table to hdfs

df =pd.read_sql(sql="save overwrite web_site TO 'hdfs://jdp-1:8020/tmp/web_site_test' FORMAT parquet;", con=connection)
df =pd.read_sql(sql="load 'hdfs://jpd-1:8020/tmp/web_site_test' format parquet AS mysql_t2_par;", con=connection)
df =pd.read_sql(sql="SELECT * FROM mysql_t2_par limit 10;", con=connection)
df.head()
```

For more information, please refer to [FusionDB Document](http://www.fusionlab.cn/zh-cn/fdb/quickstart.html)


![Whoami公众号](https://github.com/itweet/labs/raw/master/common/img/weixin_public.gif)

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/archives/