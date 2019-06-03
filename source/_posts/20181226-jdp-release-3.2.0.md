---
title: JDP Release 3.2.0
date: 2019-06-04 02:25:36
description: JDP 3.2 是 3.x 系列中的第三个版本，经过一段漫长时间的研发测试，测试已达到我们对软件可用性与稳定性的基准，今天全票通过，决定发布正式版本。
category: JDP
tags: JDP,3.2.0
---

# Release Note

JDP 3.2 是 3.x 系列中的第三个版本，经过一段漫长时间的研发测试，测试已达到我们对软件可用性与稳定性的基准，今天全票通过，决定发布正式版本。此版本拥有几大全新的功能以及组件，夯实 JDP 的的基石，立足于 3.1 版本，我们新增 FusionDB 跨多云协作分布式数据库引擎组件，未来 FusionDB 将做为 JDP 的核心组件进行研发，期待 FusionDB 未来真正的统一多源异构，跨云数据分析的联邦数据库的伟大愿景。目前一台 8G、6c 的虚拟机可安装和部署，实现在笔记本电脑也能体验 JDP 的完整功能。

为什么会如此漫长的时间，才发布 3.2.0.0 版本，各种缘由待我一一道来：

由于个人做了一个错误的决定，导致整个研发周期拉长，核心功能时间缩短，错过了最佳的研发时机，在此检讨。3.2.0.0 单方面新增对 Hadoop 3.1.1、Spark 2.4.0 版本的支持，由于社区还未支持，为了让 Spark 2.4.0 支持运行在 Hadoop3 上，新增适配 Hive3 以及 Hadoop3 的工作，导致花费了大量时间，并且进行了一些 Bugfix，而社区版 Spark 需要 3.0 才会支持 Hadoop3，目前还未发布。

如上，功能 release ，才开始着手 FusionDB 的设计与研发，导致没有抓住重点，致使 FusionDB 原本计划要实现的功能点，延期至下一个版本，未来版本我们会完全依托 Github project、issues 来统一管理与规划版本功能点和迭代，让更多小伙伴参与进来。

研发尾声，手忙脚乱，惊慌失措的做了一个半成品 CoreAI 组件，由于依赖了一堆 Docker 的东西，复杂度增加，经讨论决定此组件暂不 release，即不开放给 3.2.0.0 版本的用户使用，未来软件设计和软件质量符合我们对软件 release 基准时，在开放给用户使用。

如果，想要体验 JDP 3.2 版本，请访问[快速入门](http://www.fusionlab.cn/zh-cn/docs/intro/quickstart.html) 页面，提供云盘压缩包下载，您可以在私有网络的情况下安装使用 JDP。我们在此列出主要的版本变更，按组件进行分组：

* JDP 3.2 
    - ambari-2.7.3.0
    - clickhouse 3.2.0.0-108-19.4.0
    - jdp-select 3.2.0.0-108
    - kafka 3.2.0.0-108-1.0.1
    - superset 3.2.0.0-108-0.26.3
    - zookeeper 3.2.0.0-108-3.4.6
    - flink 3.2.0.0-108-1.7.0
    - spark 3.2.0.0-108-2.4.0
    - livy2 3.2.0.0-108-0.5.0
    - hbase 3.2.0.0-108-2.0.2
    - hadoop 3.2.0.0-108-3.1.1
    - fusiondb 3.2.0.0-108-0.1.0-incubator
    - coreai 3.2.0.0-108-0.1.0-incubator

相关 JDP Roadmap 访问[Github](https://github.com/fusionlabcn/jdp)

JDP 核心  

* 企业级 Core Data & Core AI 统一分析平台。
* One-stop solution：开箱即用 & 简单 & 易用。
* 高性能：万亿数据秒级响应，提供PB级数据存储。
* 扩展性：规模化部署，可达几百台集群规模。
* 可视化：可视化的数据收集、数据存储、数据分析、数据报表。
* 可靠性：集群提供副本容错机制，硬件故障不会造成数据丢失。
* 简单运维：日志、监控、报警、配置、服务一栈式管理。
* 简单易用：提供标准SQL，拖拽式数据分析。
* 全流程数据闭环：Load Data -> FQL Analysis -> Save Data
* FusionDB: 强大的批流统一、异构数据融合分布式数据库引擎。
* 真正的统一多源异构，跨多云协作、分析、处理数据海量数据的联邦数据库。
* FQL for Everyone & All in FQL 愿景。

# Next

## 3.1.0.0 

JDP 未来计划新增一些简单、易用、强大的 Batch & Stream 统一的一体化功能。全新的设计，在混口饭吃的工作中，抽出时间在设计与实现下一代数据流平台，而且 JDP 定位为一款真正企业级可用的一体化数据流平台，需要实现足够简单且强大的数据流处理和管理能力，这是我们设计 JDP 的初衷。

JDP 设计的组件和相关技术非常驳杂，整个研发过程漫长且耗费硬件资源，开发维护不易，我们已经在尽力的努力克服外部困难，规范化整个 Devops 流程，希望能改善目前效率的问题。

next JDP 版本中，会新增 Hadoop 3.2.x 版本以及 Spark、Flink 相关组件，一切的原因是为了更好；我们的流分析引擎核心 Runtime 支持 Spark 、Flink，用户无需感知这些 Runtime 技术，一体化的部署、运维、监控均有 JDP 实现，外部接口兼容标准的数据库协议，大大降低用户的成本，我们会有一层自己的数据库 DSL 设计，我们称为 FQL，其实是 SQL++，就这样。

JDP 3.2 中计划，会启动另外一个 `stack` 孵化工作，探索 k8s + ai 技术，毕竟行行转 ai，容器我一直比较抵触，体积超大，带状态服务支持弱，但 ai 各种 py 库，真的很适合容器化，升级方便，维护性成本高，难以规模化部署运维，涉及网络、存储、计算、调度、容器、分布式等技术，显然是庞然大物，国内专业玩 k8s 的公司，貌似基本难有做大的，企业级市场，基础设施难挣钱，业务挣钱，难有企业重视，基本都是使用层面，扯远啦；回归正题，JDP 需要去很好的解决这些问题，一切是为了更好，实现一体化流分析平台的价值，容器化 JDP 某些模块，长期看是利好的，可以降低成本。。。

未来的时间，我会逐渐披露更多细节，敬请期待。。。

## 3.2.0.0 

我们在 3.1.0.0 发布时的 Release 披露了我们 3.2.0.0 的 roadmap，我们来一一分析我们做到了那些？顺带披露一下我们 Next 版本的核心特性。

如 3.1.0.0 所述，我们 FusionDB 的设想由来已久，只是一直没有提上日程，而在 3.2.0.0 版本中我们终于 release 第一个 FusionDB 0.1.0 版本，我们做到了+1，我们终于开始做属于自己的分布式联邦数据库系统了，欧耶！

如 3.1.0.0 所述，将支持 Hadoop3 版本，其他组件完成相应适配融合，一下子把整个 JDP 变重了，不保证未来不会移除此组件，过程困难重重。我们做到了+1，欧耶！

如 3.1.0.0 所述，底层 Runtime 支持 Spark 、Flink，未做到，目前仅构建出 Flink，未做适配工作，技术栈选择需慎重，我们会综合考虑，是否未来会启用，我们未做到-1，啊，好失败！

如 3.1.0.0 所述，会启动另外一个 `stack` 孵化工作，探索 k8s + ai 技术，起名 CoreAI，未正式 release。容器技术选择需谨慎，会影响你的产品快速分发的，相信我，还是需要慎重选择呀。。。，我们未做到-1，啊，好失败！

Next

* Data Lake Storage
    - Unified storage layer，Support S3,OSS,ADLS,GCP
    - ACID transactions
    - Time Travel (data versioning) Transaction log records details Cloud-Native workload

* FusionDB
    - Standalone metastore server
    - Supports UPDATE, DELETE and MERGE
    - Unified batch & streaming syntax
    - Predicate Pushdown in DataSource
    - Add stream compute management
    - Adaptive execution

未来的时间，我们会更多专注于分布式数据库、分布式计算引擎，致力于提供易于使用、高性能、简单的统一分析平台而努力。

文末，附 JDP 3.2 近照一张。

![](http://www.fusionlab.cn/zh-cn/docs/intro/img/ambari%E2%80%93dashboard.png)

单机、分布式系统都能一体化的管理。。。

[1] JDP 官网: http://www.fusionlab.cn/

[2] JDP 快速启动：http://www.fusionlab.cn/zh-cn/docs/intro/quickstart.html

![Whoami公众号](https://github.com/itweet/labs/raw/master/common/img/weixin_public.gif)

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/archives/