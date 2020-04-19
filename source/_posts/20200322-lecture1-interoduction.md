---
title: Lecture1-interoduction
date: 2020-03-22 00:46:50
description: MIT 6.824 - Distributed Systems (Spring 2020).
tags: [spring, 6.824, 2020, mit]
category: 6.824
---

## Lecture interoduction

### Quick Preview 

* parrlelism
* fault-tolerant
* physical
* secvrits / isolated

* Challenges
    - challenges
    - partial failure
    - performance

* Course Structure
    - lectures
    - papers - 每周一篇 paper
        + 比如：mapreduce paper
    - examples
    - labs  
        + lab1 - MapReduce
        + lab2 - Raft fault-tolerant
        + lab3 - k/v server
        + lab4 - sharded k/v server
    - project (optional)

* Infrastructure abstractions
    - Storage
    - Comms 
    - computer

* Impl
    - RPC、Threads、consistency

* Performance
    - scalability - 2X computers -> 2X throughput

* fault-tolerant
    - availability              |   Non-volatile storage
    - recoverability            |   Replication

* Topic - consistency
    - Put(k,v)
    - Get(K) -> v
    - examples

### MapReduce

因为没有必要让工程师花费所有的时间来编写分布式系统软件，也要有大量的面向普通业务的开发工作，因此，这些不是很熟悉分布式系统的普通工程师确实需要某种框架可以让他们轻松大胆地编写他们想进行的任何分析工作，例如：排序算法、Web索引或链接分析器等，并在写这些应用程序时无所畏惧，同时无需担心它是否能在数以千计的计算机上运行的诸多细节，比如：如果将这些工作分散到这些计算机上、如何组织所需任何数据的移动、如果应对不可避免的故障。因此寻找和创造一种框架使得非专业人员也能轻松开发和运行大型分布式计算系统，已处理海量的数据，正是 MapReduce 全部意义所在。

![mapreduce principle](https://www.itweet.cn/screenshots/6.824/mapreduce-principle.png)

* Map(k,v)

```
split v into words   # K is filename, ignore

for each word w
    emit(w, "1")
```

* Reduce(k,v)

```
emit(len(v))
```

reference：http://www.itweet.cn/2018/04/23/mapreduce-osdi04/

### homework: lab1 mapreduce

* Reference：
    - 6.824 - Spring 2020: https://pdos.csail.mit.edu/6.824/
    - 6.824 Lab 1: MapReduce: https://pdos.csail.mit.edu/6.824/labs/lab-mr.html
