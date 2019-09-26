---
title: How to quickly deploy flink on jdp platform
date: 2019-07-30 16:20:53
description: 如何快速部署 Flink 集群在 JDP 平台上。
tags: [Flink, 2019]
category: BigData
---

## 环境依赖

* JAVA_HOME = /usr/jdk64/jdk1.8.0_112

* HADOOP_CONF_DIR = /etc/hadoop/conf  # 包括 HDFS_CONF_DIR and YARN_CONF_DIR

`注意`: 安装官方文档安装的 JDP 3.2 集群，自带如上相关依赖，本演示是 Flink on Yarn 模式。

## 安装 JDP 安装包中自带的 Flink 软件包

目前 JDP 仅支持 Redhat 系列 7.x 的操作系统，故我们使用 yum 安装 Flink。

```
yum install flink_3_2_0_0_108 -y
```

## 修改 Flink 默认配置文件

1. 在 JDP 集群中安装 Flink on Yarn 集群，仅需配置 env.java.home 

```
grep -rn "env.java.home" /usr/jdp/current/flink/conf/flink-conf.yaml
19:env.java.home: /usr/jdk64/jdk1.8.0_112
```

JDP 集群中安装 Flink on Yarn `可选配置`，因为 JDP HADOOP_CONF_DIR 默认值和 Flink 配置默认值一致，故不需要配置。也可显示的在 config.sh 中 export HADOOP_CONF_DIR=xxx。

```
grep -rn "HADOOP_CONF_DIR" config.sh | head -1
19:export HADOOP_CONF_DIR=/etc/hadoop/conf
```

2. 添加 Flink 用户，并授予 hdfs 组权限，方便 Flink 读写 HDFS。

```
useradd flink -g hdfs
```

3. 创建 Flink 需要的log、run等目录。

```
mkdir /var/log/flink
mkdir /var/run/flink
```

4. 为新创建的 log、run 目录授予 Flink 读写权限

```
chown flink:root -R /var/log/flink
chown flink:root -R /var/run/flink
```

5. 初始化 flink 用户在 hdfs 的 home 目录

```
su - flink

hadoop fs -mkdir /user/flink
```

## 启动一个 Flink 集群运行于 YARN 上

1. 需要切换到 flink，执行启动一个 Flink on Yarn 集群

1.1 Start a long-running Flink cluster on YARN
```
su - flink

cd /usr/jdp/current/flink

./bin/yarn-session.sh -n 2 -tm 2024 -s 3 # 集群资源太小，配置不合理容易无法分配到资源，导致任务hang住。Specify the -s flag for the number of processing slots per Task Manager. We recommend to set the number of slots to the number of processors per machine.

./bin/yarn-session.sh -n 2 -tm 2024 -s 3 -d # -d 表示后台运行。- The Flink YARN client has been started in detached mode. In order to stop Flink on YARN, use the following command or a YARN web interface to stop it:
yarn application -kill application_1564483050501_0002
```

`注意`：启动时的提示`Setting HADOOP_CONF_DIR=/etc/hadoop/conf because no HADOOP_CONF_DIR was set.`，如果未设置 HADOOP_CONF_DIR，默认值 /etc/hadoop/conf；而 JDP 集群的 HADOOP_CONF_DIR 刚好在此处。

1.2 Run a Flink job on YARN

```
./bin/flink run -m yarn-cluster -p 4 -yjm 1024m -ytm 4096m ./examples/batch/WordCount.jar
```

3. 测试 flink on yarn 集群

3.1 Examples 经典案例：WordCount

```
./bin/flink run ./examples/batch/WordCount.jar

flink list
```

3.2 快速启动 flink sql clinet 

进入 SQL Client

```
./bin/sql-client.sh embedded
```

Running SQL Queries:

```
Flink SQL> SELECT 'Hello World';

Flink SQL> SELECT name, COUNT(*) AS cnt FROM (VALUES ('Bob'), ('Alice'), ('Greg'), ('Bob')) AS NameTable(name) GROUP BY name;
```

退出 SQL Client

```
Flink SQL> quit;
```

提交 `Flink WordCount` 程序，因为 YARN 容器资源 limit 导致失败，需要调整启动集群的资源配比。

`org.apache.hadoop.yarn.exceptions.InvalidResourceRequestException: Invalid resource request, requested resource type=[vcores] < 0 or greater than maximum allowed allocation. Requested resource=<memory:1024, vCores:4>, maximum allowed allocation=<memory:6656, vCores:3>, please note that maximum allowed allocation is calculated by scheduler based on maximum resource of registered NodeManagers, which might be less than configured maximum allocation=<memory:6656, vCores:3>`

4. 停止 Flink 集群，Flink 集群 -d 运行模式，需要通过 yarn 命令才能停止，具体如下：

```
yarn application --list

yarn application -kill application_1556800373836_0018
```

## 总结

简单演示如果在 JDP 平台快速部署 Flink 集群，JDP 发型包中默认已经自带 Flink rpm 包。yum 直接安装好之后配置一个env.java.home，就可以直接启动 flink on yarn 模式了，flink 本身模式比较多，Yarn Setup 支持 `Start a long-running Flink cluster on YARN`，`Run a Flink job on YARN`。今天我们演示的主要是前者，已经在 YARN 启动好一个 long-running 的 Flink 集群，在提交 Flink job 到此集群。主要遇到的问题是资源分配问题，导致任务无法申请到资源或请求资源超限而失败。Flink on Yarn 的 Job Manager 和 Task Manager 均运行在 YARN Container 中，资源请求受限于 YARN 对单个 Contrainer 的限制。由于我是个人环境，资源有限，安装过程我曾故意调整 YARN Container 资源 Limit 上限。如果是生产环境一般不会遇到此类问题，除非乱配置 Flink 提交的资源参数。

接下来，我会简单介绍一下，Flink sql-training 项目，帮助快速入门 Flink 的具体使用。

参考：

- [flink yarn setup](https://ci.apache.org/projects/flink/flink-docs-stable/ops/deployment/yarn_setup.html)
- [flink sql-training](https://github.com/ververica/sql-training)
- [flink sql client](https://ci.apache.org/projects/flink/flink-docs-stable/dev/table/sqlClient.html)

![Whoami公众号](https://github.com/itweet/labs/raw/master/common/img/weixin_public.gif)

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/archives/