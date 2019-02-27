---
title: Cloudera-Enterprise-6
date: 2018-08-05 12:17:34
description: 今天，我们聊一聊在中国最受欢迎Cloudera CDH，CDH是世界级的大数据产品，同时也是一家伟大的开源软件公司。
tags: [cloudera,2018]
category: CDH
---

今天，我们聊一聊在中国最受欢迎Cloudera CDH，CDH是世界级的大数据产品，同时也是一家伟大的开源软件公司。

接着上期的话题，聊一聊`Cloudera Enterprise 6.0`的新特性。

Cloudera CDH以下简称CDH，CDH做为企业级的大数据产品，一直以稳定可靠，小白式安装、升级、文档丰富著称，这也是最受欢迎的产品。

CDH多年来，一直提供社区版、试用版、商业版三个版本，但是社区版几乎没有任何限制，可以免费使用，并且功能越来越强大，所以大部分公司几乎都是用的社区版，商业版主要是提供技术支持和锦上添花的审计、lineage、告警等功能，如果企业有一定的技术能力，使用社区版几乎能解决企业数据分析的所有需求。

CDH一直保持稳定、可靠，并且自己维护分支，高昂的成本，CDH也是最保守的大数据发行版。从CDH一开始的发布到现在，几乎整个stack没有很多的变化，很早CDH就基本解决离线和即席查询的痛点，所以其他厂商一直在补功课，他却一直在优化和完善整个CDH的功能，最近的几个版本为了迎合时代发展，引入云和AI的支持，Cloudera Data Science Workbench(CDSW) 和 ALTUS。

CDH整个软件栈一直很保守，核心功能主要是：

* 存储层：HDFS、Hbase、Kudu
* 资源调度、安全和管理员：YARN、Cloudera Manager、Cloudera Navigator
* 数据处理：分析性数据(Impala)、模型(SAS、R、Spark、CDSW)、流计算(SparkStreaming)、NoSQL数据库(Hbase)、数据转换和解析(SQOOP、Flume、MR、Spark、Hive)。

CDH5版本以来，基本提供以上功能，整个产品的一体化程度以及数据产品提供哪些能力边界思考的非常清晰，造了很多轮子，基本都是符合业界发展的趋势，CDH很多功能领先业界，产品完备性以及研发方向的投入都是非常正确的，基本没有夭折的项目，可以说是非常成功的产品了。反观对手HDP，在堆砌功能的方向上越走越远，导致整个软件栈非常庞大，几乎不可控制，功能得优化、产品的一体化做得比较欠缺、虽然百分比开源，但是缺乏一个企业级产品的很多关键特性，这也是很多人选择CDH的原因吧。

都各有优缺点，CDH在技术力量的投入和研发上话费大量精力和金钱，产品比较成功，但是市场收益其实一般，大家都用社区版，这样的现象在中国很常见，你们都懂的。

CDH包含的软件，几乎都是出自自己公司只手，80%的软件都是自己公司研发出来开源到Apache社区，并且都是顶级项目，可想而知技术力量多强大，几乎是热衷开源事业，对底层软件感兴趣的人的天堂。

Hadoop为核心的CDH产品，主要的研发力量，放在提供很多企业级的产品特性：早期的即席查询引擎Impala，12年就启动研发的Kudu，为了弥补Hbase、HDFS的短板，让产品更加的完整，以及HDFS的内核级Balance，企业级的权限、审计、血缘、多租户: Sentry、Cloudera navigator等，产品一体化和功能的完备性思考的非常到位，覆盖了大多数数据分析场，经过这几年的发展已然非常的成熟，CDH做为一个半闭源的产品，企业级核心特性基本都可以免费使用，但是代码不开源，定制化和修改几乎不可能，但是对于大多数用户来说，基本不会有这样的需求，只要产品可靠稳定，易于使用就够了，这个是CDH产品化的过程中非常出彩的地方，开源软件产品化的过人之处。

HDP包含的软件，几乎都来自社区，他们主要的精力类似CDH，他们为了支持即席查询一直在优化Hive，弄出一个Tez，也是在最近几个HDP发行版中才渐渐可用。还有很多精力花费在Hadoop 3.0上，对Hadoop YARN开发了很多核心的特性，比如：支持长服务的运行，支持深度学习框架等，HDP 在YARN上的投入是非常巨大的，其它有安全、日志聚合、管理、审计、血缘：Ranger、LogSearch、Ambari、Atlas，还有几乎夭折的项目：Falcon、Knox活跃度很低，整个产品提供26+以上的组件，大部分都不是核心投入，导致整个软件栈异常庞大，不易维护，产品的一体化和整体控制力比较低，但是支持的组件多，灵活、可定制化组合强也是一些优势，至少比社区版本有了更多的可靠性和可维护性的便利，支持不够还可以修改，这也是HDP百分百开源的优势。然而，产品化方面就做的相对弱一些，堆砌组件始终不是长久之计，HDP3渐渐开始收敛，应该也是渐渐意识到这样的问题了吧。

两大Hadoop发行商，各有特点。

我们下面看看CDH 6有哪些过人之处：

![](https://www.itweet.cn/screenshots/cloudera-enterprise-6.png)

基本上都是核心组件的版本大升级，比如：一直保持Hadoop 2.6升级为3.0，Hive升级2.1，Hbase升级2.0，Spark升级2.2，kafka升级1.0等。CDH 6是做为bate版本发布的，Cloudera公司对于CDH产品的稳定性和可靠性的重视，CDH 6可以算是CDH产品的重大版本升级，也支持了很多核心功能。

支持基于GPU进行深度学习，Hive 2矢量化执行，大幅度提升性能。Hbase 2.0提供多租户隔离能力，CM支持支持2,500多个节点。

AI深度学习的支持，Cloudera提供CDSW，面向开发人员的一个开发工具，提供一整套从开发到模型上线的整体解决方案，基于k8s提供动力。Hortonworks HDP产品，一直在优化和完善YARN支持GPU，提供的AI产品方案，完全基于YARN提供动力。

我们看到在AI产品方面，两大Hadoop发行商都交出的自己的答卷，在未来的一段时间，我会往这个方向写更多的实践内容。

参考：

[1] https://www.cloudera.com/documentation/enterprise/6/release-notes/topics/rg_cdh_600_new_features.html
[2] https://www.cloudera.com/products/cloudera-enterprise-6.html
[3] http://blog.cloudera.com/blog/2018/05/new-in-cloudera-enterprise-6-0-analytic-search/

![Whoami公众号](https://github.com/itweet/labs/raw/master/common/img/weixin_public.gif)

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/archives/