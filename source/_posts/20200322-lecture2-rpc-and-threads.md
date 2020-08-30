---
title: Lecture2-rpc-and-threads
date: 2020-03-22 00:47:06
description: MIT 6.824 - Distributed Systems (Spring 2020)
tags: [spring, 6.824, 2020, mit]
category: 6.824
---

golang - 大肆夸赞一番

* I/O concurrency

* CPU Parallelism

* Thread Challenges

* 多线程爬虫 Demo
    * sync.Mutex 
    * lock
    * thread
    * Goroutine

* primary-backup replication

* state transfer
    - memrory: 内存状态的转移到另外机器，实现起来比较简单

* replication state machine
    - OP: 操作状态转移，相对复杂，需要考虑很多种情况
    - what state？
    - VMware Fault Tolerance (FT) 

* 如何解决脑裂？
    - 网络分区导致脑裂？
    - 主从副本 primary crash 导致的脑裂？

- MapReduce: Simplified Data Processing on Large Clusters
- The Google File System
- The Design of a Practical System for Fault-Tolerant Virtual Machines



