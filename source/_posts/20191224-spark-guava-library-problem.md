---
title: Spark guava 库引发的系列问题
date: 2019-12-24 03:43:38
description: 扩展 spark 支持各种新的数据源读写功能，由于 guava 冲突造成的系列问题。
tags: [Spark, 2019]
category: JDP
---

最近在扩展 spark structured streaming 功能的时候，遇到几个疑难问题，今天一并记录一下，方便以后翻旧帐。。。

一切都要从 maven-shade-plugin 插件开始说起，我在扩展 spark structured streaming 功能时，需要充分考虑未来的可扩展性和易用性，最好能沉淀出一个小框架，呈现为一个 lib 库，基于这个库能够快速的扩展新的数据源。

首先，我先调研了一下现有需要支持的数据源，总共 4+，基本都是在公司内部大规模使用的分布式数据存储系统。现有需要实现，数据源需要支持 read -> process -> write 功能。中间 process 需要充分考虑自定义处理逻辑的能力。优先支持流式 API 功能，其次支持批量 API 功能。

经过一番调研和思考，我抽象出 source，process，sink，JobConf 三种接口以及若干方法。source 和 sink 对应 4+ 数据源，每种数据源都会有一个基本的数据对象，支持对象进行读写数据源，读写时支持基本的谓词下推，每种数据源根据存储规则，进行最大化的并行 scan。Process 接口支持基本的数据处理转换方法，基于 spark 的 dataset 进行封装。JobConf 实现配置化数据源信息的自动加载和多方数据来源的 merge，JobConf 实现了类似 SpringBoot 的自动化配置功能，只需要把支持的数据源的相关配置到 `xxx-dev.propergies`，根据默认配置 job.profiles.active 指定 dev 则默认去 resources 中载入其中的带 `xxx.` 开头的全部配置，在具体的 API 代码中 new 相关的 source & sink 对象则自动加载相应配置，实现任务的提交和计算。整体打包为一个 shade jar 包，运行时通过 `-Djob.config.location = /path/xxx-prod.propergies` 在外部实现动态加载配置。

我主要从以下几个方面考虑：

易用性：提交时只需要一个 jar 包和一个外部的配置文件，进行提交任务并计算。

可扩展性：抽象出一个基本的框架，简称：A 模块。新增数据源，只需要依赖基础的 A 模块，配置文件中配置相关 source，sink 配置信息。然后，编写 Process 的业务转换逻辑，利用 JobConf 进行本地调试和上线，能降低大部分的调试功能。

快速入门：A 模块，支持的数据源都提供相互读写、数据缓缓的测试用例，代码级指导，快速扩展新的面相特定业务的模块功能。提供详细的 README 指导如何在 IDEA 和 线上集群发起任务。

进入正题，在使用我提供的库扩展新功能时，主要遇到如下两个问题：


问题1: `java.lang.ClassNotFoundException: kafka.DefaultSource`

```
19/12/23 13:34:54 INFO ApplicationMaster: Unregistering ApplicationMaster with FAILED (diag message: User class threw exception: java.lang.ClassNotFoundException: Failed to find data source: kafka. Please find packages at http://spark.apache.org/third-party-projects.html
	at org.apache.spark.sql.execution.datasources.DataSource$.lookupDataSource(DataSource.scala:639)
	at org.apache.spark.sql.streaming.DataStreamReader.load(DataStreamReader.scala:159)
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:498)
	at org.apache.spark.deploy.yarn.ApplicationMaster$$anon$4.run(ApplicationMaster.scala:721)
Caused by: java.lang.ClassNotFoundException: kafka.DefaultSource
	at java.net.URLClassLoader.findClass(URLClassLoader.java:381)
	at java.lang.ClassLoader.loadClass(ClassLoader.java:424)
	at java.lang.ClassLoader.loadClass(ClassLoader.java:357)
	at org.apache.spark.sql.execution.datasources.DataSource$$anonfun$23$$anonfun$apply$15.apply(DataSource.scala:622)
	at org.apache.spark.sql.execution.datasources.DataSource$$anonfun$23$$anonfun$apply$15.apply(DataSource.scala:622)
	at scala.util.Try$.apply(Try.scala:192)
	at org.apache.spark.sql.execution.datasources.DataSource$$anonfun$23.apply(DataSource.scala:622)
	at org.apache.spark.sql.execution.datasources.DataSource$$anonfun$23.apply(DataSource.scala:622)
	at scala.util.Try.orElse(Try.scala:84)
	at org.apache.spark.sql.execution.datasources.DataSource$.lookupDataSource(DataSource.scala:622)
	... 11 more
)

```

我确定，相关 spark structured streaming 依赖的包都已经打进去了，提交任务依然报错。经过一番 Debug，发现时因为我们自己扩展的 spark datasource 代码中有一个文件 `resources/META-INF/services/org.apache.spark.sql.sources.DataSourceRegister`, 而 Kafka 的官方扩展里面也有一个名称一样的文件：

- kafka-0-10-sql： org.apache.spark.sql.kafka010.KafkaSourceProvider
- xxx-engine-xxx: org.apache.spark.sql.xxx.xxxSourceProvider

因为打包优先级的问题，造成我们的文件覆盖了 Kafka 的文件内容，造成提交到集群时一直报如上错误。Spark 就是依靠此文件中的内容，动态的加载相关的 class 文件，进而实现动态加载自定义数据源的功能。

**我们如何解决此问题？**

方案一：

在 `resources/META-INF/services/org.apache.spark.sql.sources.DataSourceRegister` 文件中，加入 Kafka 以及自己扩展的几个 xxxSourceProvider，可解决问题。

方案二：

使用 maven assembly 和 shade 插件进行同名 service 文件内容合并。

```
<transformers>
    <transformer implementation="org.apache.maven.plugins.shade.resource.ServicesResourceTransformer"/>
</transformers>
```

方案三：

大型工程中，一般避免生成 `uber-jar` 包，springboot 就是一个例子，网络上面充斥着 springboot 各种 jar 依赖冲突问题。模块划分清晰，生成的 jar 只有自己写的代码，依赖的第三方 lib 统一放到一个文件夹中，写一个脚本去控制启动进程，或发起一个任务。build 直接生成一个tag.gz，自带 jar、配置文件、启动脚本。线上直接解压修改配置就能跑。

问题2: IDEA 运行的非常成功，打成统一的 `uber-jar` 到线上提交到集群报错：java.lang.NoSuchMethodError: com.google.common.hash.Hashing.farmHashFingerprint64()

```
Caused by: java.lang.NoSuchMethodError: com.google.common.hash.Hashing.farmHashFingerprint64()Lcom/google/common/hash/HashFunction;
	at com.aliyun.openservices.aliyun.log.producer.internals.Utils.generateProducerHash(Utils.java:31)
	at com.aliyun.openservices.aliyun.log.producer.LogProducer.<init>(LogProducer.java:91)
```

遇到此坑的人不在少数：

- SparkR：https://sparkr.atlassian.net/browse/SPARKR-211

- Hive：https://issues.apache.org/jira/browse/HIVE-7387

经过一番排查发现我们依赖的一个模块使用 guava 版本 22.0，而 spark 集群自带 14.0，导致冲突，而无法正常工作。做为运行在 spark 集群上的任务，spark 加载 guava 包优先级高于我们自己的包。

我们依赖的包使用到 guava 版本 22.0 中比较新的方法，而在 14.0 版本还没有这样的方法。在不能修改对方代码的前提下，有如下方案：

- spark 集群的包升级一下，风险较高，容易造成未知问题。
- 另外一种方式是利用 maven 插件重命名自己的 guava 包。

利用 maven 插件 shade 重命名包解决问题。

```
<relocations>
    <relocation>
        <pattern>com.google.common</pattern>
        <shadedPattern>com.xxx.xxx.shaded.com.google.common</shadedPattern>
    </relocation>
</relocations>
```

如何减少此类问题，依赖大型工程，需要考虑自己项目引入包的版本是否和大型工程依赖的包有冲突，尽量使用下载量最大的版本。避免使用到一些新特性，而造成上面问题。

