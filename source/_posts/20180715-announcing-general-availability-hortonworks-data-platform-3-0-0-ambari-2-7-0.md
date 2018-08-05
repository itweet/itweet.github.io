---
title: Hortonworks Data Platform 3.0.0平台宣布正式GA
date: 2018-07-15 16:14:23
tags: [hortonworks,ambari]
category: BigData
---

## HDP 3.0.0 GA 

Hortonworks Data Platform 3.0.0版本，基本上集成Hadoop社区生态最新版本的强大功能特性，实现真正混合型数据平台。

如图，HDP 3.0.0 版本核心功能特性。

![](https://2xbbhjxc6wk3v21p62t8n4d4-wpengine.netdna-ssl.com/wp-content/uploads/2018/07/HDP-3.0-benefits.png)

我们上篇，其实就介绍了大数据数据平台发展的几个方向，而HDP做为一个资深玩家，当然引领了一个重要的发展方向，那就是完全基于HDFS和YARN发展整个发行版，我们知道Hortonworks公司一直是一个务实，并且很实在的团队，一直深耕Hive和Hadoop，贡献了很多代码，开发了很多新特性，在社区也有很大的影响力。

随着，近几年大数据平台发展日渐稳定，开始更多关注实用、应用层面，也淘汰很多行业内的企业。大多都开始寻求转型之路。IT行业基本每隔3年就是一个新的革新，新陈代谢超级快，而近两年比较火的是区块链、AI、Hadoop in Cloud、数据湖、容器等。

Hortonworks公司，做为一家开源软件公司，一直务实努力耕耘社区，积极贡献代码，一直是我等崇拜追赶的对象，趋势的把握和时机的掌握刚刚好；HDP 3.0.0 的发布，在强调高性能的同时，新增多个新特性：

* TensorFlow，Caffe等深度学习框架的支持，预览版。
* 企业Data Lake的支持。
* 一直在勤勤恳恳努力改良的Hive，支持Real-time，ACID。
* 混合型存储，融合云端，支持S3、ADLS、Hadoop纠删码等。
* Yarn完美支持调度容器，实现长任务的运行和管理，K8S表示不服。
* Ambari一直受人病诟的UI以及无法支撑大规模集群管理，支持5000个节点的管理，全新的UI。
* 基于容器化、GPU等的支持。

这是大数据生态系统的一个巨大的飞跃。

![](https://www.itweet.cn/screenshots/Hortonworks-HDP-3-0-GA.png)

## A new start

HDP 3.0是大数据生态系统的一次巨大飞跃，整个堆栈发生了重大变化，扩展了生态系统(支持深度学习和第三方Docker Application)。 HDP 3.0完全支持云端和本地化部署。HDP 3.0 很多新的功能都是基于Apache Hadoop 3.1，包括容器化、GPU支持、Erasure Coding和Namenode Federation。

![](https://2xbbhjxc6wk3v21p62t8n4d4-wpengine.netdna-ssl.com/wp-content/uploads/2018/07/HDP-3.0-Marketecture.png)

因为Apache Hadoop 3.1的重大特性进化，让Hadoop生态更加开放包容容器、AI、Cloud。Yarn往更加通用的资源管理框架发展，挑战者K8s。HDFS则往更加实用，稳定的方面发展，目前还是一骑绝尘，私有化部署难逢对手，支持基于HDFS Core的数据Balance，免受新增节点数据不均衡，需要手动均衡的痛点，Erasure Coding降低存储成本，HDFS可对接多种云端存储产品也是一些新的探索方向，我们看到HDFS往更加稳定、实用的方面发展。

HDP 3.0还移除一些臃肿的系统，常年无人使用，社区并未发展。终于是意识到做为一家开源软件公司，封装了一堆零散的组件，形成了一个平台产品，但是做为一个技术型产品，门槛是很高的，这是一个商业险话题，我们不讨论。HDP很长一段时间，都会是技术人员才能使用的软件产品，而国人早就基于这样的基础数据平台，开发数据中间件，支撑更加上层的应用，离客户更近，赚的盆满钵满，而对自己坚实的基础支撑系统，并未有任何的正向反馈，国人开源软件只痛，唏嘘一下。还是那句话，只论技术，不讨论。

HDP 3.0 删除了Apache Falcon，Apache Mahout，Apache Flume和Apache Hue等组件，并将Apache Slider功能融合到Apache YARN中。

关于，平台组件选型、维护与控制方面CDH显然做得更加自然一些，而HDP很长一段时间一直基于社区最新的组件打包，全都整个到一个平台，基本上都在Ambari、以及社区几个重要的组件上开发核心特性。由于组件众多，维护显然成本巨大，对于一些边缘性组件投入明显不足，精力分散，产品考虑不够完备，甚至放弃自己辛辛苦苦设计的软件，开源之路未顺利进行下去。

HDP 3.0.0 我看到了一些全新的变化，这是很好的开始，HDP产品化工作一直不如CDH，还是一个非常技术性的产品，并且对自身组件没有很强的把控能力，导致产品表现一直弱于CDH，长时间都在堆叠组件的道路上越走越远，产品组件也越来越臃肿，最明显的是HDP数据产品，覆盖的分析场景不够全面，导致很多安装了HDP产品的用户，还要手动维护一个即席分析组件，比如：Presto、Impala、MPPDB、Drill等。

![](https://2xbbhjxc6wk3v21p62t8n4d4-wpengine.netdna-ssl.com/wp-content/uploads/2018/07/asparagus.png)

如图，HDP产品路线图，希望HDP未来能更加焦距，做好产品，降低数据分析门槛，从一个技术性产品，变成更切合市场的数据平台产品。

## 总结

企业级大数据产品，日渐成熟，开始分出尽力追赶一些目前主流的技术趋势，通过平台融合、整合资源，通过强大的计算和存储数据能力，更好地服务于客户。HDP 3.0 完全依托Hadoop社区优势、新特性，发布了更加强大，跨时代的大数据产品。

数据存储

> 1、Erasure Coding降低存储成本，将存储开销降低50％，保证3副本的数据可靠性。
> 2、Namenode Federation，支持多Namespace，同一个集群，逻辑上隔离使用。
> 3、云存储支持，Google、S3、ADLS等存储连接器。
> 4、DataNode，内置磁盘数据均衡器。

数据操作系统

Apache Hadoop YARN的突出特点包括：

> 1、Apache YARN容器化服务支持，运行Docker Spark Job，支持Slider功能
> 2、Apache YARN支持管理与调度GPU
> 3、支持队列内抢占，支持同一队列中不同应用程序（批量，实时）之间的负载均衡
> 4、增强的可靠性，可用性和可维护性，用户和开发人员友好的Apache YARN UI
> 5、Timeline server 2.0，基于流式的应用程序性能管理。

实时数据库

基于Apache Hive最新的强大特性：

> 1、LLAP融合Hive，提供强大工作负载，基于资源池，用户用户组分配资源。
> 2、默认情况下启用ACID功能，对数据更新的完全支持。
> 3、Hive Warehouse Connector，使得Spark更好的连接Hive。
> 4、物化视图，加快数据分析效率，提升查询速度。
> 5、JDBC存储连接器，Hive连接查询支持JDBC的数据源。

机器学习和深度学习平台

Apache Spark，Apache Zeppelin，Livy等项目。

> 1、支持Apache Spark 2.3.1 GA
> 2、支持在Docker容器中运行Spark作业
> 3、TensorFlow 1.8（仅限技术预览版）

流处理引擎

Apache Kafka和Apache Storm的突出特点包括：

> 1、支持Kafka 1.0.1 & 支持Storm 1.2.1

最终，所有做大数据产品的公司都会回归社区。`Cloudera CDH 6.0 Bate`版本的发布已然说明问题，全都回归`Hadoop 3.x`，发布全新升级的大数据产品。

更多新功能，可访问官网了解。

下一篇，我们聊一聊《Cloudera CDH 6.0》产品，有何特性？技术栈选型和发展方向和HDP有何异同？

参考：

[1] https://hortonworks.com/blog/announcing-general-availability-hortonworks-data-platform-3-0-0-ambari-2-7-0-smartsense-1-5-0/

[2] http://www.itweet.cn/2018/07/02/micro-service-architecture-based-on-restful/

欢迎关注微信公众号[Whoami]，阅读更多内容。

![Whoami公众号](https://github.com/itweet/labs/raw/master/common/img/weixin_public.gif)

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/archives/