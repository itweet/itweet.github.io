---
title: Hbase-Region-split-policy
date: 2016-01-09 17:16:50
category: BigData
tags: hbase
---
# hbase-1.0简介
在 HBase 中，Table 被横向划分为 Region，它是一段数据的管理者，Region 被分发到 
RegionServer 上进行管理，一个 Region 只被一个 RegionServer 
管理，它的数据存储在 HDFS 上，是可以有多个副本的。

也就是说：管理者 (Region) 只有一个，数据有多个副本。

HBase 的以前实现中，当一台 RegionServer 
不可用时，需要数十秒甚至数分钟才可以完成发现和恢复工作，在这段时间内，这台 
RegionServer 上的 Region 是不可用的。当一个 Region 
不可用时，它需要一段时间才可以被其他 RegionServer 接管。

在最新的实现中，一个 Region 可以有多个副本（Region 
是数据的管理者，是实际数据的抽象），分布在多个 RegionServer 上。

> 特点：

- 1.有一个主 Region，多个从 Region。
- 2.只有主 Region 接收写请求，并把数据持久化到 HDFS 上。
- 3.从 Region 从 HDFS 中读取数据并服务读请求。
- 4.从 Region 可能会读到脏数据（主 Region 内存中的数据）。
- 5.读操作可以只读主，或者既可以读主又可读从（可配置）。

这样在主 Region 不可用时，用户仍可以读从 Region 
的数据。目前社区在进行的开发：主 Region 异步同步数据到从 Region，从而减少从 
Region 缺少的数据量。

Family 粒度的 Flush（减少小文件，优化磁盘 IO，提高读性能 HBASE-10201）

# split-compact
```
hbase.hregion.max.filesize ：配置region大小，0.94.12版本默认是10G，region的大小
与集群支持的总数据量有关系，如果总数据量小，则单个region太大，不利于并行的数据
处理，如果集群需支持的总数据量比较大，region太小，则会导致region的个数过多，导
致region的管理等成本过高，如果一个RS配置的磁盘总量为3T*12=36T数据量，数据复制3
份，则一台RS服务器可以存储10T的数据，如果每个region最大为10G，则最多1000个regio
n，如此看，94.12的这个默认配置还是比较合适的，不过如果要自己管理split，则应该调
大该值，并且在建表时规划好region数量和rowkey设计，进行region预建，做到一定时间
内，每个region的数据大小在一定的数据量之下，当发现有大的region，或者需要对整个
表进行region扩充时再进行split操作，一般提供在线服务的hbase集群均会弃用hbase的自
动split，转而自己管理split。

hbase.hregion.majorcompaction：配置major合并的间隔时间，默认为1天，可设置为0，
禁止自动的major合并，可手动或者通过脚本定期进行major合并，有两种compact：minor
和major，minor通常会把数个小的相邻的storeFile合并成一个大的storeFile，minor不会
删除标示为删除的数据和过期的数据，major会删除需删除的数据，major合并之后，一个s
tore只有一个storeFile文件，会对store的所有数据进行重写，有较大的性能消耗。
```


> ####hbase region####

 - Compact,Split
   - hbase.hregion.memstore.flush.size  default:128M
   - hbase.hregion.max.filesize (table_att==>MAX_FILESIZE) default:10G
   - hbase.hstore.compactionThreshold default:3
   - hbase.hregion.majorcompaction default:7day

 - Merge
    - 多个region合并,需要top cluster
    ```
    hbase  org.apache.hadoop.hbase.util.Merge  <table_name> <region1> <region2>
    ```

 - Scan cache
 - block cache  default：hfile.block.cache.size=0.4
 - bloom filter

> Hbase访问数据时Compact,Split带来的问题

 - region offline,mapper访问region识别
 - 调整参数控制Compact,Split
    - hbase.hregion.majorcompaction
        - 真的设置为0就行了？
    - hbase.hstore.compactionThreshold
        - Region中文件个数多于此值,开始compact
        - 可能进入minor,合并较小StoreFile
    - hbase.hregion.memstore.flush.size
        - memstore何时写入HStore
    - hbase.hregion.max.filesize (table_att==>MAX_FILESIZE)
        - Region何时开始split
    - hbase.hstore.blockingStoreFiles
        - max.filesize < flush.size*blockingStoreFiles以保证region不会被block
  
    有两种类型的紧缩：次紧缩和主紧缩。minor紧缩通常会将数个小的相邻的文件合并成一个大的。Minor不会删除打上删除标记的数据，也不会删除过期的数据，Major紧缩会删除过期的数据。有些时候minor紧缩就会将一个store中的全部文件紧缩，实际上这个时候他本身就是一个major压缩。对于一个minor紧缩是如何紧缩的，可以参见ascii diagram in the Store source code.

    在执行一个major紧缩之后，一个store只会有一个sotrefile,通常情况下这样可以提供性能。注意：major紧缩将会将store中的数据全部重写，在一个负载很大的系统中，这个操作是很伤的。所以在大型系统中，通常会自己Section 2.8.2.8, “管理 Splitting”。

    紧缩 不会 进行分区合并。参考 Section 14.2.2, “Merge” 获取更多合并的信息。

  - offpeak hour
    规定在集群不繁忙的时候hbase做自动split,Compact,比如凌晨

    ```
    配置项     默认值     含义
    hbase.hstore.compaction.ratio   1.2F    
    hbase.hstore.compaction.ratio.offpeak   5.0F    与下面两个参数联用
    hbase.offpeak.start.hour    -1  设置hbase offpeak开始时间[0,23]
    hbase.offpeak.end.hour  -1  设置hbase offpeak结束时间 [0,23]

    http://www.binospace.com/index.php/in-depth-understanding-of-the-hbase-compaction/
    ```

  - merge

    ``` 
    hbase org.apache.hadoop.hbase.util.Merge <tablename> <region1> <region2>
    ```

> 案例

```
    hbase.hregion.majorcompaction default：7  ==> 
    hbase.hstore.compactionThreshold default: 3  ==> 8,如果集群中storefile超过8个,和flush.size相关,region超过4G,才开始split
    
    hbase.hregion.memstore.flush.size default: 128M ==> 512M 防止storefile过多,过多storefile导致region compaction
    hbase.hregion.max.filesize default: 10G   ==> 32G,评估一天写入数据量,分配到不同region最大大小.
    hbase.hstore.blockingStoreFiles default: 10 ==>  16,避免一个region产生过多storefile,storefile就被block了。
```

> 获取region详细信息

```
scan 'hbase:meta', {COLUMNS => 'info:regioninfo'}
     
hbase(main):017:0> scan 'hbase:meta', {COLUMNS => 'info:regioninfo', LIMIT => 1}
ROW                                    COLUMN+CELL                                                                                                     
 cust_info,,1450145518714.ddefa1ac4420 column=info:regioninfo, timestamp=1450145519580, value={ENCODED => ddefa1ac442063171ca6ef9f9f0e9e2f, NAME => 'cu
 63171ca6ef9f9f0e9e2f.                 st_info,,1450145518714.ddefa1ac442063171ca6ef9f9f0e9e2f.', STARTKEY => '', ENDKEY => ''}'} 

hbase(main):008:0> scan 'hbase:namespace', {COLUMNS => 'info:d'}
ROW                                    COLUMN+CELL                                                                                                     
 default                               column=info:d, timestamp=1446179703117, value=\x0A\x07default                                                   
 hbase                                 column=info:d, timestamp=1446179703143, value=\x0A\x05hbase                                                     
2 row(s) in 0.0150 seconds
```

# hbase snappy
```
snappy hbase 结果>>

表名                    未压缩大小   压缩后大小   压缩比例%
user_last_live20151230   2.3 T        0.35T         85
```

参考：http://hbase.apache.org

