---
title: zookeeper 大量logs解决
date: 2015-01-01 18:52:26
category: BigData
tags: zookeeper
---
我们经常会遇到有大量zookeeper的日志，我们该如何处理，要么删除，要么禁止输出，这两种该如何实现？我讲两种方法：

# 方法一：日志清除工具PurgeTxnLog 

>zookeeper运行时间长了以后，日志会成为一个比较大的问题。比如作者压力测试hbase 
>一周以后，zookeeper日志文件达到了10G的规模。由于zookeeper日志文件不能随意删除
>，因为一个长时间不更新的节点完全有可能存在于几 天前的一个日志文件中。那么如何
>安全地删除它们呢？可以自己编写程序处理，但是zookeeper也提供给了我们一个方便的
>小工具：PurgeTxnLog 。
 
`java -Djava.ext.dirs=lib org.apache.zookeeper.server.PurgeTxnLog log_path snap_path -n 10`

>其中-n 表示要保留多少个文件，不能低于3

>P.S:这里的路径一定要是zookeeper的log的根路径哦，就是version-x
>那一层路径。代码里会到输入路径里去找version-x目录，然后再去找下面的log文件


# 方法2：禁止日志输出

解决办法：
    log4j.logger.包名=OFF

>P.S:上面为Java代码中加入即可。


原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/