---
title: HiveServer2-JDBC中文支持
date: 2015-07-02 17:31:11
description: 如何配置 Hive JDBC 支持中文，早期Hive版本。
category: BigData
tags: Hive
---

```
export LANG=en_US.UTF-8
export HADOOP_OPTS="$HADOOP_OPTS -Dfile.encoding=UTF-8"

[hsu@yndx-bigdata-hadoop01 ~]$ sudo vi /opt/cloudera/parcels/CDH/lib/hive/bin/hiveserver2   #实际调用的hive脚本
[hsu@yndx-bigdata-hadoop01 ~]$ sudo vim /opt/cloudera/parcels/CDH/lib/hive/bin/hive  
. "$bin"/hive-config.sh 			#放到执行了hive-config脚本之后
export LANG=en_US.UTF-8
export HADOOP_OPTS="$HADOOP_OPTS -Dfile.encoding=UTF-8"
```


