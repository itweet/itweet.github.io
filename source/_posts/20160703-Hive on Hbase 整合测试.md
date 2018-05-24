---
title: Hive on Hbase 整合测试
date: 2016-07-03 17:26:17
category: BigData
tags: HbaseSQL
---
Hbase做为一个k-v查询系统，被使用在海量数据简单查询应用中。有时候会有一些复杂查询操作，需要写很多nosql的脚本或者程序！为了降低使用门槛，而sql的通用性，让大家都往sql on hbase方向发展： 
    
   * 1、支持友好的sql语法
   * 2、通用型的odbcjdbc接口
   * 3、对接主流bi可视化工具
   * 4、开箱即用无缝兼容对接

基于上面的想法，很多公司脑洞大开，做了一些中间解决方案，比如：
    
   * 1、hive on hbase 
   * 2、phoenix on hbase 
   * 3、spark on hbase  
   * 4、impala on hbase 
   * 5、drill on hbase 
   * 6、presto on hbase 
   * 7、kylin on hbase 

可以看到hbase这个分布式nosql数据库是多么受人欢迎了吧！而hive整合hbase是其中最早的方案，hive查询hbase就是简单的把hbase作为一个hive数据源来使用，导致无法利用到hbase做为nosql数据库各方面的优势；虽然提供了便捷性，但没有特别大的优势，性能反而损失巨大！

# Required
  hive on hbase经过测试，有兼容性问题，整合如下：
  + hive-2.0.1 connect hbase-1.1.5 兼容
  + hive-1.2.1 connect hbase-1.1.5 不兼容
  + hive-1.2.1 on tez 0.7.1 connect hbase-1.1.5 不可用
  + hive-2.0.1 on tez 0.7.1 不兼容
  
  hbase和hive整合，只需要配置基础环境变量即可完成整合：
  ```
    # cat /etc/profile.d/hbase.sh 
    export HBASE_HOME=/opt/cloud/hbase/
    export PATH=$PATH:$HBASE_HOME/bin/:$HBASE_HOME/sbin/

    # cat /etc/profile.d/hive.sh 
    export HIVE_HOME=/opt/cloud/hive
    export PATH=$PATH:$HIVE_HOME/bin:$HIVE_HOME/sbin
  ```

# Hive on Hbase Test
```
# hive
Hive-on-MR is deprecated in Hive 2 and may not be available in the future versions. Consider using a different execution engine (i.e. tez, spark) or using Hive 1.X releases.

hive> set hive.execution.engine;
hive.execution.engine=mr

hive> CREATE TABLE itweet_cn (
    > rowkey string,
    > cf1 map<STRING,STRING>,
    > cf2 map<STRING,STRING>,
    > cf3 map<STRING,STRING>
    > ) STORED BY 'org.apache.hadoop.hive.hbase.HBaseStorageHandler'
    > WITH SERDEPROPERTIES ("hbase.columns.mapping" = ":key,cf1:,cf2:,cf3:")
    > TBLPROPERTIES ("hbase.table.name" = "itweet_cn");
OK
Time taken: 1.855 seconds

hive> INSERT INTO TABLE itweet_cn
    > SELECT 'row1' AS rowkey,
    > map('c1','hadoop.apcahe.org') AS cf1,
    > map('c2','itweet.cn') AS cf2,
    > map('c2','www.itweet.cn') AS cf3 
    > FROM DUAL 
    > limit 1;
Time taken: 47.35 seconds

hive (default)> set hive.cli.print.header=true;
hive (default)> set hive.cli.print.current.db=true;

hive (default)> select * from itweet_cn;
OK
itweet_cn.rowkey        itweet_cn.cf1   itweet_cn.cf2   itweet_cn.cf3
row1    {"c1":"hadoop.apcahe.org"}      {"c2":"itweet.cn"}      {"c2":"www.itweet.cn"}
Time taken: 0.284 seconds, Fetched: 1 row(s)
```

# Hbase Check
```
# hbase shell

hbase(main):012:0> list 'itweet.*'
itweet_cn                                                                 
1 row(s) in 0.0110 seconds

hbase(main):013:0> scan 'itweet_cn'
ROW                                          COLUMN+CELL                                                                                                                      
 row1                                        column=cf1:c1, timestamp=1467522163061, value=hadoop.apcahe.org                                                                  
 row1                                        column=cf2:c2, timestamp=1467522163061, value=itweet.cn                                                                          
 row1                                        column=cf3:c2, timestamp=1467522163061, value=www.itweet.cn                                                                      
1 row(s) in 0.1160 seconds
```

# Phoenix on Hbase
 Phoenix on Hbase整合文档，参考：https://jikelab.github.io/tech-labs/2015/07/16/Phoenix-hbase/
```
# cat shell/phoenix-cli.sh 
sqlline.py bigdata-server-1:2181

# sh shell/phoenix-cli.sh 
Building list of tables and columns for tab-completion (set fastconnect to true to skip)...
85/85 (100%) Done
Done
sqlline version 1.1.8
0: jdbc:phoenix:bigdata-server-1:2181> !tables
+------------+--------------+-------------+---------------+----------+------------+----------------------------+-----------------+--------------+-----------------+----------+
| TABLE_CAT  | TABLE_SCHEM  | TABLE_NAME  |  TABLE_TYPE   | REMARKS  | TYPE_NAME  | SELF_REFERENCING_COL_NAME  | REF_GENERATION  | INDEX_STATE  | IMMUTABLE_ROWS  | SALT_BUC |
+------------+--------------+-------------+---------------+----------+------------+----------------------------+-----------------+--------------+-----------------+----------+
|            | SYSTEM       | CATALOG     | SYSTEM TABLE  |          |            |                            |                 |              | false           | null     |
|            | SYSTEM       | FUNCTION    | SYSTEM TABLE  |          |            |                            |                 |              | false           | null     |
|            | SYSTEM       | SEQUENCE    | SYSTEM TABLE  |          |            |                            |                 |              | false           | null     |
|            | SYSTEM       | STATS       | SYSTEM TABLE  |          |            |                            |                 |              | false           | null     |
|            |              | ABC         | TABLE         |          |            |                            |                 |              | false           | null     |
+------------+--------------+-------------+---------------+----------+------------+----------------------------+-----------------+--------------+-----------------+----------+

0: jdbc:phoenix:bigdata-server-1:2181> create table abc(a integer primary key, b integer) ; 
No rows affected (1.395 seconds)

0: jdbc:phoenix:bigdata-server-1:2181> UPSERT INTO abc VALUES (1, 1); 
1 row affected (0.139 seconds)
0: jdbc:phoenix:bigdata-server-1:2181> UPSERT INTO abc VALUES (1, 2); 
1 row affected (0.013 seconds)
0: jdbc:phoenix:bigdata-server-1:2181> UPSERT INTO abc VALUES (2, 1); 
1 row affected (0.014 seconds)
0: jdbc:phoenix:bigdata-server-1:2181> UPSERT INTO abc VALUES (1, 1); 
1 row affected (0.016 seconds)

0: jdbc:phoenix:bigdata-server-1:2181> select * from abc;
+----+----+
| A  | B  |
+----+----+
| 1  | 1  |
| 2  | 1  |
+----+----+
2 rows selected (0.065 seconds)
```

如下，看到phoenix不支持Hive的map数据类型。phoenix 支持[datatype](http://phoenix.apache.org/language/datatypes.html)列表
0: jdbc:phoenix:bigdata-server-1:2181>  CREATE VIEW "itweet_cn" ( rowkey VARCHAR primary key, "cf1" map, "cf2" map,"cf3" map) default_column_family='row1';
`Error: ERROR 201 (22000): Illegal data. Unsupported sql type: MAP (state=22000,code=201)`
`java.sql.SQLException: ERROR 201 (22000): Illegal data. Unsupported sql type: MAP`

phoenix－hbase文中版本集成，还遇到一个问题，hbase中存在的表，mapping时候报错，`ReadOnlyTableException: ERROR 505 (42000): Table is read only.`，而在很早以我集成的版本中没遇到过这样的问题！一摸一样的SQL!

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/
