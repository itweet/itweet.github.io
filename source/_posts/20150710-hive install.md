---
title: hive install
date: 2015-07-10 17:29:55
category: BigData
tags: Hive
---
# 1、安装mysql-5.5

** From server2

- (1)、rpm包安装mysql
```	
	# rpm -qa | grep mysql  [查询是否自带mysql]
	# rpm -e mysql-libs-5.1.71-1.el6.x86_64 --nodeps	[不验证依赖卸载]
	# rpm -qa | grep mysql   [再次查看卸载是否成功]
	# rpm -i MySQL-server-5.5.40-1.linux2.6.x86_64.rpm		[安装服务端]
	# mysqld_safe &		[后台启动，jobs查看]
    # rpm -i MySQL-client-5.5.40-1.linux2.6.x86_64.rpm [安装客户端]
```

> or

```
$ yum install mysql-server
$ /etc/init.d/mysqld start
$ chkconfig --add mysqld
$ chkconfig mysqld on
$ chkconfig --list|grep mysqld

$ mysql_secure_installation #设置初始化信息
```

- (2)、修改数据库配置信息

```
        # mysql_secure_installation
                NOTE: RUNNING ALL PARTS OF THIS SCRIPT IS RECOMMENDED FOR ALL MySQL
                SERVERS IN PRODUCTION USE!  PLEASE READ EACH STEP CAREFULLY!

                In order to log into MySQL to secure it, we'll need the current
                password for the root user.  If you've just installed MySQL, and
                you haven't set the root password yet, the password will be blank,
                so you should just press enter here.

                Enter current password for root (enter for none):   //当前密码,第一次使用为null
                    OK, successfully used password, moving on...

                    Setting the root password ensures that nobody can log into the MySQL
                    root user without the proper authorisation.

                    Set root password? [Y/n] Y      //设置密码
                    New password:                   /admin
                    Re-enter new password:          //admin
                    Password updated successfully!
                    Reloading privilege tables..
                    ... Success!

                    By default, a MySQL installation has an anonymous user, allowing anyone
                    to log into MySQL without having to have a user account created for
                    them.  This is intended only for testing, and to make the installation
                    go a bit smoother.  You should remove them before moving into a
                    production environment.

                    Remove anonymous users? [Y/n] n     //是否删除匿名用户
                    ... skipping.

                    Normally, root should only be allowed to connect from 'localhost'.  This
                    ensures that someone cannot guess at the root password from the network.

                    Disallow root login remotely? [Y/n] n       //不允许root远程登录
                    ... skipping.

                    By default, MySQL comes with a database named 'test' that anyone can
                    access.  This is also intended only for testing, and should be removed
                    before moving into a production environment.

                    Remove test database and access to it? [Y/n] n  //是否删除测试数据库
                    ... skipping.

                    Reloading the privilege tables will ensure that all changes made so far
                    will take effect immediately.

                    Reload privilege tables now? [Y/n] Y        //重新加载权限表
                    ... Success!

                    Cleaning up...

                    All done!  If you've completed all of the above steps, your MySQL
                    installation should now be secure.

                    Thanks for using MySQL!
```
    
- (3)、登录mysql数据库验证

```
        # mysql -uroot -padmin
```
   
- (4)创建数据库并授权
```
        #  mysql -uroot -padmin
        mysql> create database hive;
        [授权hive在任何位置(%)远程可以登陆]
        mysql> grant all on hive.* to 'hive'@'%' identified by 'hive'; 
        mysql> grant all on hive.* to 'hive'@'server2' identified by 'hive';
        mysql> flush privileges;    [刷新权限]
```
   
- (5)使用的是SQLyog数据库可视化软件连接验证

# 2、hive-0.13.1的安装

- (1)、解压
```        
    # tar -zxvf apache-hive-0.13.1-bin.tar.gz -C /usr/local/
```
    
- (2)、scp hive-0.13.1 [hive安装在server2]
```        
  # scp -rq hive-0.13.1 server2:/usr/local/
```
    
- (3)、cp配置文件
```        
        # cp hive-exec-log4j.properties.template hive-exec-log4j.properties
        # cp hive-log4j.properties.template hive-log4j.properties
        # cp hive-env.sh.template hive-env.sh
        # cp hive-default.xml.template hive-site.xml
```

- (4)、配置hive-config.sh
```        
        vi /usr/local/hive-0.13.1/bin/hive-config.sh
        export JAVA_HOME=/usr/local/jdk1.7.0_45
        export HIVE_HOME=/usr/local/hive-0.13.1
        export HADOOP_HOME=/usr/local/hadoop-2.4.0
```
    
- (5)、配置hive-site.xml [mysql做metastore]
```
//连接地址,基本配置
<property>
<name>javax.jdo.option.ConnectionURL</name>
<value>jdbc:mysql://server2:3306/hive?createDatabaseIfNotExist=true</value>
</property>
<property>
//mysql驱动
<name>javax.jdo.option.ConnectionDriverName</name>
<value>com.mysql.jdbc.Driver</value>
</property>
//用户名
<property>
<name>javax.jdo.option.ConnectionUserName</name>
<value>hive</value>
</property>
//用户密码
<property>
<name>javax.jdo.option.ConnectionPassword</name>
<value>hive</value>
</property>
//默认数据库位置
<property>
    <name>hive.metastore.warehouse.dir</name>
    <value>/user/hive/warehouse</value>
    <description>location of default database for the warehouse</description>
</property>

//hive远程metastore的thrift地址        
<property>
  <name>hive.metastore.uris</name>
  <value>thrift://server2:9083</value>
</property>


//hiveserver2的配置
<property>  
    <name>hive.support.concurrency</name>   
    <description>Enable Hive's Table Lock Manager Service</description>   
    <value>true</value>  
</property> 
<property>  
    <name>hive.zookeeper.quorum</name>  
    <description>Zookeeper quorum used by Hive's Table Lock Manager</description>
    <value>server1,server2,server3</value>
</property> 
<property>
  <name>hive.zookeeper.client.port</name>
  <value>2181</value>
  <description>The port of zookeeper servers to talk to. This is only needed for read/write locks.</description>
</property>
<property>  
    <name>hive.server2.thrift.bind.host</name>
    <value>server2</value>
    <description>Bind host on which to run the HiveServer2 Thrift interface. Can    be overridden by setting $HIVE_SERVER2_THRIFT_BIND_HOST</description>  
</property> 

//关闭推测式执行,一些优化项
<property>
 <name>hive.mapred.reduce.tasks.speculative.execution</name>
 <value>false</value>
</property>
<property>
 <name>mapreduce.reduce.speculative</name>
 <value>false</value>
</property>
小表mapjoin
<property>
 <name>hive.ignore.mapjoin.hint</name>
 <value>false</value>
</property>
<property>
 <name>hive.mapjoin.smalltable.filesize</name>
 <value>500000000</value>
</property>
并行执行
<property>
 <name>hive.exec.parallel</name>
 <value>true</value>
</property>
<property>
 <name>hive.exec.parallel.thread.number</name>
 <value>16</value>
</property>
客户端显示
<property>
 <name>hive.cli.print.current.db</name>
 <value>true</value>
</property>
<property>
 <name>hive.cli.print.header</name>
 <value>true</value>
</property>
关闭自动统计
<property>
 <name>hive.stats.autogather</name>
 <value>false</value>
</property>
```

- (6)、cp mysql-connector-java-5.1.26-bin.jar 到hive-0.13.1/lib

- (7)、启动metastore
```    
    # hive-0.13.1/bin/hive --service metastore &       [jobs查看]
```
    
- (8)、启动hive
```    
    # hive-0.13.1/bin/hive
```
    
- (9)、启动hiveserver2 [jdbc服务]
```
    # hive-0.13.1/bin/hive --service hiveserver2 --hiveconf hive.server2.thrift.port=14000 start &

    [hsu@server2 ~]$ lsof -i :14000
    COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
    java    3460  hsu  306u  IPv4  29485      0t0  TCP server2:scotty-ft->server1:18243 (ESTABLISHED)
    java    3460  hsu  313u  IPv4  29484      0t0  TCP server2:scotty-ft (LISTEN)
```

- (10)、测试hiveserver2
```    
    使用beeline控制台连接hiveserver2：
    $ /usr/local/hive-0.13.1/beeline> !connect jdbc:hive2://server2:14000 -uhsu -phsu org.apache.hive.jdbc.HiveDriver

    $ beeline --help
    Usage: java org.apache.hive.cli.beeline.BeeLine 
   -u <database url>               the JDBC URL to connect to
   -n <username>                   the username to connect as
   -p <password>                   the password to connect as
   -d <driver class>               the driver class to use

    # hive1.2.1测试
    
    !connect jdbc:hive2://server2:14000 -udefault -nhsu -phsu -dorg.apache.hive.jdbc.HiveDriver

    [hsu@server1 ~]$ beeline 
    Beeline version 1.2.1 by Apache Hive
    beeline> !connect jdbc:hive2://server2:14000 
    Connecting to jdbc:hive2://server2:14000
    Enter username for jdbc:hive2://server2:14000: 
    Enter password for jdbc:hive2://server2:14000: 
    Error: Failed to open new session: java.lang.RuntimeException: java.lang.RuntimeException: org.apache.hadoop.security.AccessControlException: Permission denied: user=anonymous, access=EXECUTE, inode="/tmp":hsu:supergroup:drwx------
        at org.apache.hadoop.hdfs.server.namenode.FSPermissionChecker.checkFsPermission(FSPermissionChecker.java:271)
        at org.apache.hadoop.hdfs.server.namenode.FSPermissionChecker.check(FSPermissionChecker.java:257)
        at org.apache.hadoop.hdfs.server.namenode.FSPermissionChecker.checkTraverse(FSPermissionChecker.java:208)
        at org.apache.hadoop.hdfs.server.namenode.FSPermissionChecker.checkPermission(FSPermissionChecker.java:171)
        at org.apache.hadoop.hdfs.server.namenode.FSNamesystem.checkPermission(FSNamesystem.java:6512)
        at org.apache.hadoop.hdfs.server.namenode.FSNamesystem.getFileInfo(FSNamesystem.java:4140)
        at org.apache.hadoop.hdfs.server.namenode.NameNodeRpcServer.getFileInfo(NameNodeRpcServer.java:838)
        at org.apache.hadoop.hdfs.protocolPB.ClientNamenodeProtocolServerSideTranslatorPB.getFileInfo(ClientNamenodeProtocolServerSideTranslatorPB.java:821)
        at org.apache.hadoop.hdfs.protocol.proto.ClientNamenodeProtocolProtos$ClientNamenodeProtocol$2.callBlockingMethod(ClientNamenodeProtocolProtos.java)
        at org.apache.hadoop.ipc.ProtobufRpcEngine$Server$ProtoBufRpcInvoker.call(ProtobufRpcEngine.java:619)
        at org.apache.hadoop.ipc.RPC$Server.call(RPC.java:962)
        at org.apache.hadoop.ipc.Server$Handler$1.run(Server.java:2039)
        at org.apache.hadoop.ipc.Server$Handler$1.run(Server.java:2035)
        at java.security.AccessController.doPrivileged(Native Method)
        at javax.security.auth.Subject.doAs(Subject.java:415)
        at org.apache.hadoop.security.UserGroupInformation.doAs(UserGroupInformation.java:1628)
        at org.apache.hadoop.ipc.Server$Handler.run(Server.java:2033) (state=,code=0)

    解决：
    [hsu@server2 ~]$ hadoop fs -ls /tmp
    Found 2 items
    drwx-wx-wx   - hsu supergroup          0 2015-08-13 14:57 /tmp/hive
    drwx------   - hsu supergroup          0 2015-08-06 13:03 /tmp/hsu

    [hsu@server2 ~]$ hadoop fs -chmod 777 /tmp
    [hsu@server2 ~]$ hadoop fs -ls /
    drwxrwxrwx   - hsu supergroup          0 2015-08-13 14:57 /tmp

    0: jdbc:hive2://server2:14000>   !connect jdbc:hive2://server2:14000 
    Connecting to jdbc:hive2://server2:14000
    Enter username for jdbc:hive2://server2:14000: hsu
    Enter password for jdbc:hive2://server2:14000: ***
    Connected to: Apache Hive (version 1.2.1)
    Driver: Hive JDBC (version 1.2.1)
    Transaction isolation: TRANSACTION_REPEATABLE_READ
    1: jdbc:hive2://server2:14000> create table test(id int);
    No rows affected (20.356 seconds)
    1: jdbc:hive2://server2:14000> 
    
    1: jdbc:hive2://server2:14000>  insert into table test values (1), (2), (3);
    INFO  : Number of reduce tasks is set to 0 since there's no reduce operator
    WARN  : Hadoop command-line option parsing not performed. Implement the Tool interface and execute your application with ToolRunner to remedy this.
    INFO  : number of splits:1
    INFO  : Submitting tokens for job: job_1439448136822_0001
    INFO  : The url to track the job: http://server1:23188/proxy/application_1439448136822_0001/
    INFO  : Starting Job = job_1439448136822_0001, Tracking URL = http://server1:23188/proxy/application_1439448136822_0001/
    INFO  : Kill Command = /home/hsu/hadoop/bin/hadoop job  -kill job_1439448136822_0001
    INFO  : Hadoop job information for Stage-1: number of mappers: 1; number of reducers: 0
    INFO  : 2015-08-13 16:00:31,907 Stage-1 map = 0%,  reduce = 0%
    INFO  : 2015-08-13 16:01:22,538 Stage-1 map = 100%,  reduce = 0%, Cumulative CPU 1.56 sec
    INFO  : MapReduce Total cumulative CPU time: 1 seconds 560 msec
    INFO  : Ended Job = job_1439448136822_0001
    INFO  : Stage-3 is selected by condition resolver.
    INFO  : Stage-2 is filtered out by condition resolver.
    INFO  : Stage-4 is filtered out by condition resolver.
    INFO  : Moving data to: hdfs://mycluster/user/hive/warehouse/test/.hive-staging_hive_2015-08-13_15-59-12_208_7322597341621072670-1/-ext-10000 from hdfs://mycluster/user/hive/warehouse/test/.hive-staging_hive_2015-08-13_15-59-12_208_7322597341621072670-1/-ext-10002
    INFO  : Loading data to table default.test from hdfs://mycluster/user/hive/warehouse/test/.hive-staging_hive_2015-08-13_15-59-12_208_7322597341621072670-1/-ext-10000

    1: jdbc:hive2://server2:14000> select * from test;
    +----------+--+
    | test.id  |
    +----------+--+
    | 1        |
    | 2        |
    | 3        |
    +----------+--+
    3 rows selected (0.324 seconds)
```

- (11)、hive安装目录加入环境变量中

```        
       # vi /etc/profile

        附录1：hiveserver1和hiveserver2的区别
        Hiveserver1 和hiveserver2的JDBC区别：
        HiveServer version    Connection URL             Driver Class
        HiveServer2           jdbc:hive2://:              org.apache.hive.jdbc.HiveDriver
        HiveServer1           jdbc:hive://:               org.apache.hadoop.hive.jdbc.HiveDriver

    参考地址：https://cwiki.apache.org/confluence/display/Hive/HiveServer2+Clients
```

# 3、hive的语法介绍

- (1) 创建

```
        hive (default)> create table t1(int id);     [创建表]
        hive (default)> create table t2(id int,name string) row format delimited fields terminated by '\t';   [指定行分割符]
```

- (2) 加载数据
```        
        hive (default)> load data local inpath '/usr/local/testdata/id' into table t1;  [linux本地加载数据到hive,copy数据]
        hive (default)> load data local inpath '/usr/local/name' into table t2;         [linux本地加载数据到hive,copy数据]
```
    
- (3) 删除表

```        
        hive (default)> drop table t1;      [受控表managed table,从hdfs删除数据,metastore元数据信息删除]
        mysql> select * from TBLS;  [TBL_TYPE字段记录表类型MANAGED_TABLE or other]
```

# 4 受控表(MANAGED_TABLE)包括内部表，分区表，桶表。

- (5) 分区表[数据在不同文件目录中,扫描范围]

```        
        hive (default)> create table t3(id int,name string) partitioned by(grade int) row format delimited fields terminated by '\t';    [创建分区表]
        hive (default)> load data local inpath '/usr/local/name' into table t3 partition(grade=1);  [加载数据]
        hive (default)> select * from t3 where grade=1;     [分区字段可以作用过滤条件，是一个文件夹的标识]

        hive (default)> create table enroll(id int,name string) partitioned by(year int,month int) row format delimited fields terminated by '\t';
        load data local inpath '/usr/local/name' into table enroll partition(year=2014,month=11-12);
```

- (6) 桶表(bucket table)
```        
        表链接中使用，提高效率
        hive (default)> create table bucket_test(id int,name string) clustered by(id)  into 3 buckets;   [按照id分为3个桶]
        hive (default)> set hive.enforce.bucketing=true;        [启用桶表]

        insert overwrite table buckets select ... from ...      [插入数据]
        hive (default)> insert overwrite table bucket_test select id,name from t2;
```
   
- (7) 外部表EXTERNAL_TABLE[删除表，只删除表定义，对HDFS的数据不会删除]{外部分区表}
```
        # hadoop fs -put name /testdata/external_teble
        hive (default)> create external table external_test(id int,name string) row format delimited fields terminated by '\t' location '/testdata/external_table';
        hive (default)> select id,name from external_test order by id desc;
```
    
# 5、命令行工具
    (1) # hive
    (2) # hive -e "select * from t2";
    (3) # hive -e "select * from t2" >> a
    (4) # hive -S -e "select * from t2" >> a
    (5) # hive --hiveconf hive.querylog.location=/usr/local/hive-0.13.1/logs
    (6) hive (default)> set hive.querylog.location;
        hive.querylog.location=/tmp/root
    (7) hive -f file
    (8) source file
    (9) /root/.hiverc 和 /root/.hivehistory 

    搜狗数据
        use sougoulibs;
        create external table sogou(dt string, websession string, word string, s_seq int, c_seq int, website string) 
        row format delimited fields terminated by '\t' lines terminated by '\n' stored as textfile location '/labs/sogou/'; 

# 6、hcatlog

参考：https://cwiki.apache.org/confluence/display/Hive/HCatalog

# 7、hive-1.2.1 cli启动报错
```
mysql> select * from VERSION;
+--------+----------------+------------------------------------+
| VER_ID | SCHEMA_VERSION | VERSION_COMMENT                    |
+--------+----------------+------------------------------------+
|      1 | 1.2.0          | Set by MetaStore hsu@192.168.2.201 |
+--------+----------------+------------------------------------+
1 row in set (0.00 sec)
```

```
[hsu@server2 ~]$ hive
Logging initialized using configuration in file:/home/hsu/apache-hive-1.2.1-bin/conf/hive-log4j.properties
[ERROR] Terminal initialization failed; falling back to unsupported
java.lang.IncompatibleClassChangeError: Found class jline.Terminal, but interface was expected
        at jline.TerminalFactory.create(TerminalFactory.java:101)
```

解决：
```
[hsu@server2 ~]$ ls hadoop/share/hadoop/yarn/lib/jline-0.9.94.jar 
hadoop/share/hadoop/yarn/lib/jline-0.9.94.jar
[hsu@server2 ~]$ ls hive/lib/jline-2.12.jar 
hive/lib/jline-2.12.jar

[hsu@server2 ~]$ mv hadoop/share/hadoop/yarn/lib/jline-0.9.94.jar hadoop/share/hadoop/yarn/lib/jline-0.9.94.jar.bak

[hsu@server2 ~]$ cp hive/lib/jline-2.12.jar hadoop/share/hadoop/yarn/lib/

[hsu@server2 ~]$ ls hadoop/share/hadoop/yarn/lib/jline-*
hadoop/share/hadoop/yarn/lib/jline-0.9.94.jar.bak  hadoop/share/hadoop/yarn/lib/jline-2.12.jar

[hsu@server2 ~]$ hive
Logging initialized using configuration in file:/home/hsu/apache-hive-1.2.1-bin/conf/hive-log4j.properties
hive (default)> show tables;
OK
tab_name
Time taken: 2.386 seconds
```

`由于使用的jline版本不一致导致问题~!`

# 7. Hive 2.0.1 FAQ
 启动报错：
 ```
 Required table missing : "`VERSION`" in Catalog "" Schema "". DataNucleus requires this table to perform its persistence operations. Either your MetaData is incorrect, or you need to enable "datanucleus.schema.autoCreateTables"
org.datanucleus.store.rdbms.exceptions.MissingTableException: Required table missing : "`VERSION`" in Catalog "" Schema "". DataNucleus requires this table to perform its persistence operations. Either your MetaData is incorrect, or you need to enable "datanucleus.schema.autoCreateTables"
        at org.datanucleus.store.rdbms.table.AbstractTable.exists(AbstractTable.java:606)
 ```
 解决：
    在hive-site.xml文件中加入如下配置解决
 ```
    <property>
        <name>datanucleus.readOnlyDatastore</name>
        <value>false</value>
    </property>
    <property> 
        <name>datanucleus.fixedDatastore</name>
        <value>false</value> 
    </property>
    <property> 
        <name>datanucleus.autoCreateSchema</name> 
        <value>true</value> 
    </property>
    <property>
        <name>datanucleus.autoCreateTables</name>
        <value>true</value>
    </property>
    <property>
        <name>datanucleus.autoCreateColumns</name>
        <value>true</value>
    </property>
 ```

# hive 2.0.1 beeline权限验证问题
 - https://community.hortonworks.com/questions/4905/error-while-running-hive-queries-from-zeppelin.html
 - http://stackoverflow.com/questions/25073792/error-e0902-exception-occured-user-root-is-not-allowed-to-impersonate-root
```
# core-site.xml添加，并重启集群hdfs & yarn
<property>
<name>hadoop.proxyuser.hadoop.hosts</name><value>*</value>
</property>
<property>
<name>hadoop.proxyuser.hadoop.groups</name><value>*</value>
</property>
```

# hive 2.0.1 and tez 0.7.1 兼容性问题
 1、整合hive 2.0.1 and tez 0.7.1发现一些class包没用被加载，提示是没用找到类。
 2、通过降低hive版本为 1.2.1发现没用任何问题，可以正常执行tez任务！
 3、社区查看hive2.0.1依赖的tez版本是0.8.3，打算重新手动编译在测试是否可行，待验证。
 4、这一点可以说明tez这个包各个版本直接接口的兼容性非常差，导致升级代价大，难以维护！

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/