---
title: Apache ozone object store architecture
date: 2021-01-21 01:10:39
description: Apache Ozone - 一个基于 raft 的分布式对象存储系统。
tags: [ozone, 2021, apache]
category: 6.824
---

## 1. 简介

Apache Hadoop Ozone 是一个分布式键值存储，可以有效管理大量小文件。Ozone 旨在与现有的 Apache Hadoop 生态系统很好地配合使用，并且满足了对新的开放源代码对象存储的需求，该对象存储旨在简化操作使用并将其扩展到单个集群数千个节点和数十亿个对象。

## 2. 了解可伸缩性问题

为了将 Ozone 扩展到数十亿个文件，我们需要解决 HDFS 中存在的两个瓶颈。

### 2.1 Namespace 可扩展性

我们不能再将整个 Namespace 存储在单个节点的内存中。关键点是 Namespace 拥有引用位置区域，因此我们可以仅将 working set 存储在内存中。 Namespace 交由称为 Ozone Manager 的服务管理。

### 2.2 Block Map 可扩展性

这是一个较难解决的问题。与 namespace 不同，由于存储节点（DataNodes）定期发送有关系统中每个 block 的报告，因此 Block Map 不具有引用位置。Ozone 将这个问题委托给了一个称为 Hadoop 分布式存储（HDDS）的共享通用存储层。

## 3. 积木（Building Blocks）

Ozone 由以下关键部分组成。
 
* 1. 使用现成的键值存储（RocksDB）构建的存储容器。

* 2. 通过 Apache Ratis 的 RAFT 共识协议。RAFT 是一种共识协议，其与 Paxos 相似，但易于理解和实现。Apache Ratis 是 RAFT 的开源 Java 实现，针对高吞吐进行了优化。

* 3. 存储容器管理（SCM）- 管理复制容器的生命周期。

* 4. Hadoop 分布式存储（HDDS）- 不包含 namespace block 信息的通用分布式存储层。

* 5. Ozone Manager（OM） - 实现 Ozone 键值 namespace 命名空间管理器。

## 4. 放在一起 （Putting it Together）

![积木](https://ndu0e1pobsf1dobtvj5nls3q-wpengine.netdna-ssl.com/wp-content/uploads/2019/06/Legos.png)

### 4.1 存储容器

在最底层，Ozone 将用户数据存储在存储容器中。容器是块名称及其数据的键-值对的集合。键是在容器内唯一的块名称。值是块数据，范围从 0 字节到 256MB。块名称不必是全局唯一的。

![](https://ndu0e1pobsf1dobtvj5nls3q-wpengine.netdna-ssl.com/wp-content/uploads/2019/06/Screen-Shot-2018-10-11-at-10.03.58-AM.png)

每个容器都支持一些简单的操作：

!()[https://ndu0e1pobsf1dobtvj5nls3q-wpengine.netdna-ssl.com/wp-content/uploads/2019/06/Screen-Shot-2018-10-11-at-10.04.52-AM.png]

容器使用 RocksDB 存储在磁盘上，并针对较大的值进行了一些优化。

### 4.2 RAFT 复制

分布式文件系统必须容忍单个磁盘/节点的丢失，因此我们需要一种通过网络复制容器的方法。为此，我们引入了一些容器的其他属性。

* 1. 容器是复制的最小单位。因此，其最大大小限制为 5GB （管理员可配置）。

* 2. 每个容器可以处于以下两种状态之一：打开或关闭。打开的容器可以接受新的键值存储，而关闭的容器是不可变的。

* 3. 每个容器都有三个副本。

	使用 RAFT 复制打开的容器状态更改（写入）。RAFT 是基于仲裁的协议，其中，仲裁的节点对变更进行投票，在给定的时间，单个节点充当领导者并提出更改建议。因此，所有容器操作都可以实时可靠的复制到至少2个法定数量的节点。

![](https://ndu0e1pobsf1dobtvj5nls3q-wpengine.netdna-ssl.com/wp-content/uploads/2019/06/Screen-Shot-2018-10-11-at-10.06.53-AM.png)

容器的副本存储在 DataNodes 上。

#### 4.2.1 容器生命周期

容器从打开状态开始，客户端写块来打开容器，然后用 commit 操作来最终确定块数据。写一个块有两个阶段：

* 1. 写入块数据。根据客户端的速度和网络/磁盘带宽，这可能会花费任意长时间。如果客户端在提交该块之前死亡，则 SCM 将自动垃圾收集不完整的数据。

* 2. commit 块。此操作从根本上使该块在容器中可见。

### 4.3 存储容器管理器（SCM）

现在，我们知道如何将块存储在容器中以及如何通过网络复制容器。下一步是构建一个集中服务，该服务知道所有容器在集群中存储位置，该服务是 SCM。

SCM 从所有 DataNode 定期获取报告，告知这些节点上的容器副本及其当前状态。SCM 可以选择三个 DataNode 的集合来存储一个新的开放容器，并指导他们相互形成 RAFT 复制环。

SCM 还会在容器满的时候，指示 Leader 副本 “close” 容器。SCM 还可以检测复制过的关闭容器，并确保每个关闭容器存在三个副本。

### 4.4. Containers + RAFT + SCM = HDDS!

通过上述三个构建基块，我们拥有创建 HDDS 的所有部分，这是一个没有全局 namespace 的分布式块存储层。

DataNodes 现在被分成三组，每组形成一个 rats 复制环。每个环可以有多个打开的容器。

SCM每30秒从每个DataNode接收一次报告，以通知每个节点上打开和关闭的容器副本。根据此报告，SCM做出决策，例如分配新容器，关闭打开的容器，在磁盘丢失/数据丢失时重新复制关闭的容器。

SCM的客户可以请求分配新块，然后将块数据写入分配的容器中。客户端还可以读取打开/关闭容器中的块并删除块。关键是HDDS本身并不关心单个容器的内容。内容完全由使用SCM的应用程序管理。

![](https://ndu0e1pobsf1dobtvj5nls3q-wpengine.netdna-ssl.com/wp-content/uploads/2019/06/Screen-Shot-2018-10-11-at-10.08.09-AM.png)

### 4.5 添加 Namespace – Ozone Manager

有了 HDDS，唯一缺少的元素就是全局键值名 namespace，这是由 Ozone Manager 提供的，OM是一个从键名到相应的块集合的映射服务。

客户端可以将多个块写入HDDS，然后提交它们的 key-> blocks 以原子方式映射到 OM，使 key 在 namespace 中可见。

![](https://ndu0e1pobsf1dobtvj5nls3q-wpengine.netdna-ssl.com/wp-content/uploads/2019/06/Screen-Shot-2018-10-11-at-10.11.26-AM.png)

OM 将自己的状态存储在 RocksDB 数据库中。

## 5. HDDS Beyond Ozone

HDDS 可由其他分布式文件系统实现用作块存储层，已讨论并可能在未来实施一些示例：

* 1. HDDS 上的 HDFS （HDFS-10419） – HDDS 可用于通过替换现有的 HDFS 块管理器来整齐地解决块空间可伸缩性问题。这个想法类似于HDFS-5477提案。

* 2. cBlocks （HDFS-11118） – 由 HDDS 存储支持的可装载 iSCSI 卷的原型。

* 3. 假设对象存储，该存储也将其命名空间存储在 HDDS 容器中。


还有更多…带上自己的名称空间！

附原文：https://blog.cloudera.com/apache-hadoop-ozone-object-store-architecture/

