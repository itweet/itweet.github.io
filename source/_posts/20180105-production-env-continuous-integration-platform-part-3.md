---
title: production-env-continuous-integration-platform-part-3
date: 2018-01-05 00:04:14
description: 持续集成平台实践，接上如何为持续集成平台选型？
category: BigData
tags: ci
---

## 简介

持续集成平台实践，接上[如何为持续集成平台选型？](http://itweet.cn/blog/2018/01/03/How-to-select-a-continuous-integration-platform-part-2)。

我今天介绍软件资源的准备工作。根据选型的结果，我们接下来分步骤完成持续企业持续集成平台的实践。

- Gitlab 企业级最佳代码仓库，OpenSource 。
- Docker 企业级容器，高效集装箱技术。
- Jforg 企业级私服仓库，Build过程加速。
- OpenStack 或 Vmware Vsphere，虚拟化，让基础环境飞起，高效率。
- Apache 亲切的目录树，各种软件源码自由访问，Http(s)协议。
- Jira，开发任务追踪管理。
- Confluence是一个专业的企业知识管理与协同软件。
- SlatStack 或 Puppet，自动化运维利器。

Atlassian公司产品Jira、Confluence强大项目协作工具，`Apache Foundation`影响全世界的顶级开源软件用它们来管理厉害。

沟通协作工具，微信企业版、钉钉、Slack、Skype等，喜欢`Slack`。

对中小团队而言，在选择工具时要秉承的原则是：简单易用，方便新成员学习，平台支持性好、性价比高、安全。

- 邮件：Gmail
- 待办清单：奇妙清单
- 客户沟通：Skype
- 团队沟通：Slack 超级强大，开发团队都在用的高效工具
- IM：微信
- CRM：自建
- 协同办公和文件备份共享：坚果云，正在尝试体验

如果还涉及开发的话：

- 代码管理：Bitbucket
- 开发任务分配：JIRA Software

## 实践

### GitLab

GitLab是利用 Ruby on Rails 一个开源的版本管理系统，实现一个自托管的Git项目仓库，可通过Web界面进行访问公开的或者私人项目。它拥有与Github类似的功能，能够浏览源代码，管理缺陷和注释。可以管理团队对仓库的访问，它非常易于浏览提交过的版本并提供一个文件历史库。团队成员可以利用内置的简单聊天程序(Wall)进行交流。它还提供一个代码片段收集功能可以轻松实现代码复用，便于日后有需要的时候进行查找。

GitLab是可视化的一个软件，让企业内部拥有类似GitHub一样的平台功能。又不失灵活性，当然最主要的还是学会`git`的使用，GitLab是一个很简单的东西，应用起来超级简单。

- Gitlab 实践参考: http://itweet.cn/blog/2016/05/09/Gitlab%20%E5%AE%89%E8%A3%85%E9%85%8D%E7%BD%AE

### Docker

Docker是一个开源工具，能将一个WEB应用封装在一个轻量级，便携且独立的容器里，然后可以运行在几乎任何服务环境下。 Docker的一般使用在以下几点： 自动化打包和部署应用。

Docker基本入门参考：

- Docker Install Guide：http://itweet.cn/blog/2016/08/12/Docker%20Install%20Guide

- Docker Install for centos 7：http://itweet.cn/blog/2016/08/13/Docker%20Install%20for%20centos%207

### Jfrog Artifactory

作为市场上第一个、唯一的、统一的artifacts仓库管理平台， JFrog Artifactory 完全支持任何语言或技术创建的软件包。

当前，Artifactory是唯一的一个 企业级的仓库管理平台，它支持安全的、集群的、高可用的Docker注册中心

与所有主流的 CI/CD 和 DevOps 工具集成，Artifactory提供了端到端、自动化且无缝的追踪工件从开发环境到生产环境的解决方案。

安装Easy，感受一下，如果你想体验，请通过Docker社区版镜像，否则如果你错误安装商业版，要求你注入授权码才能正常使用，我第一次安装的时候被坑惨。

* 社区版安装：

    - Running Artifactory OSS in a container

```
$ docker pull docker.bintray.io/jfrog/artifactory-oss:latest

$ docker run --name artifactory -d -p 80:8081 docker.bintray.io/jfrog/artifactory-oss:latest
```

* 企业版安装：

    - Running Artifactory Pro in a container

```
$ docker pull docker.bintray.io/jfrog/artifactory-pro:latest

$ docker run --name artifactory -d -p 80:8081 docker.bintray.io/jfrog/artifactory-pro:latest
```

然后，访问`http://you_artifactory_ip:80/artifactory/webapp/#/home`，开始愉快的玩起来。 

可以了各位，篇幅不易过长，持续集成系列会逐步展开实践。

### OpenStack

OpenStack 是一个面向IaaS 层的开源项目，用于实现公有云和私有云的部署及管理。 拥有众多大公司的行业背书和数以千计的社区成员， OpenStack 被看作是云计算的未来。

OpenStack复杂度挺高，我专门写了一个系列，具体实践参考：

- OpenStack系列：
    + http://itweet.cn/blog/select?title=openstack%E7%B3%BB%E5%88%97

- Openstack Series Course：
    + [openstack系列(1) - Kvm虚拟化技术](https://github.com/itweet/labs/blob/master/openstack-series/openstack%E7%B3%BB%E5%88%97(1)-Kvm%E8%99%9A%E6%8B%9F%E5%8C%96%E6%8A%80%E6%9C%AF.md)
    + [openstack系列(2) - 架构设计](https://github.com/itweet/labs/blob/master/openstack-series/openstack%E7%B3%BB%E5%88%97(2)-%E6%9E%B6%E6%9E%84%E8%AE%BE%E8%AE%A1.md)
    + [openstack系列(3) - 架构规划](https://github.com/itweet/labs/blob/master/openstack-series/openstack%E7%B3%BB%E5%88%97(3)-%E6%9E%B6%E6%9E%84%E8%A7%84%E5%88%92.md)
    + [openstack系列(4) - 基础环境](https://github.com/itweet/labs/blob/master/openstack-series/openstack%E7%B3%BB%E5%88%97(4)-%E5%9F%BA%E7%A1%80%E7%8E%AF%E5%A2%83.md)
    + [openstack系列(5) - M版 快速部署](https://github.com/itweet/labs/blob/master/openstack-series/openstack%E7%B3%BB%E5%88%97(5)-M%E7%89%88_%E5%BF%AB%E9%80%9F%E9%83%A8%E7%BD%B2.md)
    + [openstack系列(6) - M版 网络配置](https://github.com/itweet/labs/blob/master/openstack-series/openstack%E7%B3%BB%E5%88%97(6)-M%E7%89%88_%E7%BD%91%E7%BB%9C%E9%85%8D%E7%BD%AE.md)
    + [openstack系列(7) - M版 云主机](https://github.com/itweet/labs/blob/master/openstack-series/openstack%E7%B3%BB%E5%88%97(7)-M%E7%89%88_%E4%BA%91%E4%B8%BB%E6%9C%BA.md)
    + [openstack系列(8) - M版 扩容节点](https://github.com/itweet/labs/blob/master/openstack-series/openstack%E7%B3%BB%E5%88%97(8)-M%E7%89%88_%E6%89%A9%E5%AE%B9%E8%8A%82%E7%82%B9.md)
    + [openstack系列(9) - M版 云硬盘1](https://github.com/itweet/labs/blob/master/openstack-series/openstack%E7%B3%BB%E5%88%97(9)-M%E7%89%88_%E4%BA%91%E7%A1%AC%E7%9B%981.md)
    + [openstack系列(9) - M版 云硬盘2](https://github.com/itweet/labs/blob/master/openstack-series/openstack%E7%B3%BB%E5%88%97(9)-M%E7%89%88_%E4%BA%91%E7%A1%AC%E7%9B%982.md)
    + [openstack系列(10) - 平台使用](https://github.com/itweet/labs/blob/master/openstack-series/openstack%E7%B3%BB%E5%88%97(10)-%E5%B9%B3%E5%8F%B0%E4%BD%BF%E7%94%A8.md)
    + [openstack系列(11) - 平台运维](https://github.com/itweet/labs/blob/master/openstack-series/openstack%E7%B3%BB%E5%88%97(11)-%E5%B9%B3%E5%8F%B0%E8%BF%90%E7%BB%B4.md)
    + [openstack系列(11) - 后记](https://github.com/itweet/labs/blob/master/openstack-series/openstack%E7%B3%BB%E5%88%97(11)-%E5%90%8E%E8%AE%B0.md)

- Labs
    + https://github.com/jikelab/labs/tree/master/openstack-series

### Vmware Vsphere

VMware vSphere® 是业界领先的虚拟化平台，使用户能够自信地虚拟化任何应用、重新定义可用性和简化虚拟数据中心。最终可实现高度可用、恢复能力强的按需基础架构，这对于任何云计算环境而言都是理想的基础平台。

Vmware Vsphere小白式的产品，商业产品，高度产品化，成熟稳定，参考：

- VMW-vSPHR-Datasheet-6-0
    + https://www.vmware.com/files/cn/pdf/vsphere/VMW-vSPHR-Datasheet-6-0.pdf

- 我为什么弃用OpenStack转向VMware Vsphere
    + http://itweet.cn/blog/2017/12/21/Why-do-abandon-OpenStack-to-VMware-vSphere

- 《VMware vSphere企业级实践》持续集成系列，待发布^_^。

一个高度产品化的东西，小白用户都能安装使用，找时间编写一篇实践内容吧。

### Apache

今年是Apache软件基金会成立15周年纪念！Apache软件基金会成立于1999年，非盈利组织，英文名称 Apache Software Foundation，简称 ASF，最早源于开发Apache HTTP服务器的一个爱好者组织“Apache组织”。Apache软件基金会主要为开源项目提供组织、法务和其他形式的支持，它所支持的项目和软件产品都遵循Apache许可证（Apache License）。

最好的Web资源访问服务器，没有之一。

Apache服务器，我现在日常工作就是参与Apache社区软件的开发和维护，强大的组织。参考：

- 一片羽毛的故事
    + https://linux.cn/article-4319-1.html

- Docker Hub
    + https://hub.docker.com/_/httpd/

***安装Apache***

```
docker run -dit --name my-apache-app -p 8080:80 -v "$PWD":/usr/local/apache2/htdocs/ httpd:2.4
```

访问地址：`http://you_ip:8080`，持续集成系列逐步发布使用过程。

### Jira

JIRA 是一个缺陷跟踪管理系统，为针对缺陷管理、任务追踪和项目管理的商业性应用软件，开发者是澳大利亚的Atlassian。JIRA这个名字并不是一个缩写，而是截取自“Gojira”，日文的哥斯拉发音。

参考：https://www.atlassian.com/software/jira

### SlatStack 

SaltStack是一个服务器基础架构集中化管理平台，具备配置管理、远程执行、监控等功能，一般可以理解为简化版的puppet和加强版的func。SaltStack基于Python语言实现，结合轻量级消息队列（ZeroMQ）与Python第三方模块（Pyzmq、PyCrypto、Pyjinjia2、python-msgpack和PyYAML等）构建。
通过部署SaltStack环境，我们可以在成千上万台服务器上做到批量执行命令，根据不同业务特性进行配置集中化管理、分发文件、采集服务器数据、操作系统基础及软件包管理等，SaltStack是运维人员提高工作效率、规范业务配置与操作的利器。

附上，多年前我亲自编写，尘土飞扬的SaltStack应用指南：

- SaltStack-应用指南
    + https://github.com/itweet/labs/raw/master/devops/books

### Puppet

puppet是一种Linux、Unix、windows平台的集中配置管理系统，使用自有的puppet描述语言，可管理配置文件、用户、cron任务、软件包、系统服务等。 puppet把这些系统实体称之为资源，puppet的设计目标是简化对这些资源的管理以及妥善处理资源间的依赖关系。

我们内部的持续集成自动化框架底层就是用这种语言结合groovy编写，抽空会补全一下实践文档。

- Puppet官方博客
    + https://puppet.com/blog

- Puppet官网文档
    + https://puppet.com/docs

### Confluence

Confluence是一个专业的企业知识管理与协同软件，也可以用于构建企业wiki。使用简单，但它强大的编辑和站点管理特征能够帮助团队成员之间共享信息、文档协作、集体讨论，信息推送。

- Confluence中文演示站点
    + http://www.confluence.cn/dashboard.action;jsessionid=F337804FB6B4511899CBB7F09B4666A2

### Atlassian

一家SaaS公司，不雇佣一个销售人员，仅通过口碑获客，市值达10亿美金级别，极其罕见，纳斯达克上市公司Atlassian就是其中之一。Atlassian提供面向企业业务流程的协同办公产品，一般传统SaaS公司因销售成本高昂，很难跑出利润，如SaaS行业标杆Salesforce虽然接近盈利，但是在销售投入仍然占营收近50%，而Atlassian因为销售非常轻，销售成本占营收比重持续保持在20%左右。正是出于轻销售策略，Atlassian已经连续11年盈利，预期2017财年营收将达6亿美元。

Atlassian的销售策略如此成功，与其优秀的产品能力密不可分。Atlassian主要有5款产品，分别面向不同的市场。JIRA（项目、认为管理软件，2002年上线）、Confluence（企业知识管理与协同软件，2004年上线）、BitBucket（代码库，2010年上线）、HipChat（内部聊天/协作软件，2012年上线）以及JIRA Service Desk（服务台软件，2013年上线）。

## 小结

我们罗列选型之后，软件产品的搭建和使用，做为持续集成系列实践部分，主要是把我多年来积累的经验和文档做一个列表。详细内容我会逐步发布和更新，我曾经总结超过`10G`的材料，基本都是原创，涉及百分之五十的都是学着玩，没机会实践，导致他们永远沉睡，我会逐步开放出来。

持续集成平台做为企业开发、运维、产品交付非常强大的一个利器，用好甚至可以改变我们很多的坏毛病，降低企业成本，让开发、运维、产品达到统一，各自专注于自己喜欢的专业的领域，发挥更大的价值和效益。DevOps之路，我们会一步步实践，不断总结经验。

***参考***

[1]. https://www.jfrog.com/confluence/display/RTF/Installing+with+Docker
[2]. https://www.atlassian.com/software/jira
[3]. https://bitbucket.org/product
[4]. https://www.jfrog.com/confluence/display/RTF/Installing+with+Docker

