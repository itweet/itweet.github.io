---
title: Ambari离线安装HDP-Hadoop集群
date: 2015-08-31 17:20:19
category: Monitoring
tags: hortonworks
---
# 简介
 Hortonworks采用了100%完全开源策略，产品名称为HDP（Hortonworks Data Platform）。所有软件产品开源，用户免费使用，Hortonworks提供商业的技术支持服务。与CDH相比，管理软件使用开源Ambari，数据治理使用Atlas，安全组件使用Ranger而非Sentry，SQL继续紧抱Hive大腿。

>Apache Ambari是对Hadoop进行监控、管理和生命周期管理的开源项目。它也是一个为Hor
>tonworks数据平台选择管理组建的项目。Ambari向Hadoop MapReduce、HDFS、 
> HBase、Pig, Hive、HCatalog以及Zookeeper提供服务。

![](https://www.itweet.cn/screenshots/ambari-server.png)

# Step0: 搭建本地yum源
> 我选择的是hdp相关包放到了apache服务器上,yum源下载地址Setp1列出。

```
# tree -L 1 www/ 
www/
|-- ARTIFACTS
|-- HDP
|-- HDP-UTILS-1.1.0.20
|-- ambari -> ambari-2.1.0
`-- ambari-2.1.0

5 directories, 0 files

# tree -L 3 www/ 
www/
|-- ARTIFACTS
|-- HDP
|   `-- centos6
|       `-- 2.x
|-- HDP-UTILS-1.1.0.20
|   `-- repos
|       `-- centos6
|-- ambari -> ambari-2.1.0
`-- ambari-2.1.0
    `-- centos6
        |-- RPM-GPG-KEY
        |-- ambari
        |-- build.id
        |-- build_metadata.txt
        |-- changelog.txt
        |-- hdp_mon
        `-- repodata

14 directories, 3 files
```

> ssh？
> echo 'UseDNS no' > /etc/ssh/sshd_config && /etc/init.d/sshd restart

# Step1: Download the Ambari repository on the Ambari Server host
--hdp url--
```
wget http://public-repo-1.hortonworks.com/ambari/centos6/2.x/updates/2.1.0/ambari.repo
wget http://public-repo-1.hortonworks.com/ambari/centos6/ambari-2.1.0-centos6.tar.gz

wget http://public-repo-1.hortonworks.com/HDP/centos6/2.x/updates/2.3.0.0/HDP-2.3.0.0-centos6-rpm.tar.gz
wget http://public-repo-1.hortonworks.com/HDP-UTILS-1.1.0.20/repos/centos6/HDPUTILS-1.1.0.20-centos6.tar.gz

wget http://public-repo-1.hortonworks.com/HDP/centos6/2.x/updates/2.3.0.0/hdp.repo
```

`关于如果搭建apache服务器，制作离线安装源，这里就不做过多介绍...`

```
update root passwd
mysqladmin -u root password admin

--mysql--
create database ambari;
grant all on ambari.* to 'root'@'%' identified by 'admin';
grant all on ambari.* to 'ambari'@'%' identified by 'admin';
grant all on ambari.* to 'root'@'server1' identified by 'admin';
grant all on ambari.* to 'ambari'@'server1' identified by 'admin';

>> or

grant all on *.*  to 'root'@'server1' identified by '123456';   
grant all on *.*  to 'ambari'@'server1' identified by 'admin';   

flush privileges;    
```

`省略mysql安装直接使用`

```
--local yum resource--
sudo yum clean all
sudo yum repolist
```

# Step2: install ambari-server

```
  sudo yum install ambari-server 
```

# Step 3: setup ambari-server

```
ambari-server setup
```

`Downloading JDK from http://public-repo-1.hortonworks.com/ARTIFACTS/jdk-7u67-linux-x64.tar.gz to /var/lib/ambari-server/resources/jdk-7u67-linux-x64.tar.gz`

```
wget http://download.oracle.com/otn-pub/java/jdk/7u79-b15/jdk-7u79-linux-x64.tar.gz
sudo mv jdk-7u79-linux-x64.tar.gz /var/lib/ambari-server/resources/ 
sudo mv jdk-7u79-linux-x64.tar.gz jdk-7u67-linux-x64.tar.gz
```


```
WARNING: Before starting Ambari Server, you must run the following DDL against the database to create the schema: /var/lib/ambari-server/resources/Ambari-DDL-MySQL-CREATE.sql

$ sudo yum install mysql-connector-java
$ mysql -uroot -padmin
mysql> use ambari;
Database changed
mysql> source /var/lib/ambari-server/resources/Ambari-DDL-MySQL-CREATE.sql
```

```
$ sudo ambari-server setup
Using python  /usr/bin/python2.6
Setup ambari-server
Checking SELinux...
SELinux status is 'disabled'
Customize user account for ambari-server daemon [y/n] (n)? y
Enter user account for ambari-server daemon (root):
Adjusting ambari-server permissions and ownership...
Checking firewall status...
Checking JDK...
Do you want to change Oracle JDK [y/n] (n)? n
Completing setup...
Configuring database...
Enter advanced database configuration [y/n] (n)? y
Configuring database...
==============================================================================
Choose one of the following options:
[1] - PostgreSQL (Embedded)
[2] - Oracle
[3] - MySQL
[4] - PostgreSQL
[5] - Microsoft SQL Server (Tech Preview)
==============================================================================
Enter choice (1): 3
Hostname (localhost): 
Port (3306): 
Database name (ambari): 
Username (root): 
Enter Database Password (bigdata): 
Re-enter password: 
Configuring ambari database...
Copying JDBC drivers to server resources...
Configuring remote database connection properties...
WARNING: Before starting Ambari Server, you must run the following DDL against the database to create the schema: /var/lib/ambari-server/resources/Ambari-DDL-MySQL-CREATE.sql
Proceed with configuring remote database connection properties [y/n] (y)? y
Extracting system views...
...ambari-admin-2.1.0.1470.jar
...
Adjusting ambari-server permissions and ownership...
Ambari Server 'setup' completed successfully.
```

# Step 3: start Ambari

```
$ sudo ambari-server start
Using python  /usr/bin/python2.6
Starting ambari-server
Ambari Server running with administrator privileges.
Organizing resource files at /var/lib/ambari-server/resources...
Server PID at: /var/run/ambari-server/ambari-server.pid
Server out at: /var/log/ambari-server/ambari-server.out
Server log at: /var/log/ambari-server/ambari-server.log
Waiting for server start....................
Ambari Server 'start' completed successfully.
```

# Step 4: Deploy Cluster using Ambari Web UI

http://server2:8080/#/login

用户名：admin
密  码：admin

# Step 5: Install Hadoop cluster
    
    省略，都是下一步操作...

报错：http://zh.hortonworks.com/community/forums/topic/ambari-agent-registration-failure-on-rhel-6-5-due-to-openssl-2/

`Error`: 

```
INFO 2015-08-25 23:52:43,898 main.py:287 - Connecting to Ambari server at https://server2:8440 (192.168.2.201)
INFO 2015-08-25 23:52:43,898 NetUtil.py:59 - Connecting to https://server2:8440/ca
ERROR 2015-08-25 23:52:43,968 NetUtil.py:77 - [Errno 1] _ssl.c:492: error:100AE081:elliptic curve routines:EC_GROUP_new_by_curve_name:unknown group
ERROR 2015-08-25 23:52:43,968 NetUtil.py:78 - SSLError: Failed to connect. Please check `openssl` library versions. 
Refer to: https://bugzilla.redhat.com/show_bug.cgi?id=1022468 for more details. 

系统为centos 6.5
$ cat /etc/redhat-release 
CentOS release 6.5 (Final)
```

`此处为RHEL / CentOS 6.5一个小问题，更新openssl更新版本！即可解决！`

```
Remedy:

Check the OpenSSL library version installed on your host(s):
rpm -qa | grep openssl

openssl-1.0.1e-15.el6.x86_64

If the output says openssl-1.0.1e-15.x86_64 (1.0.1 build 15) you will need to upgrade the OpenSSL library by running the following command:
yum upgrade openssl

Verify you have the newer version of OpenSSL (1.0.1 build 16):
rpm -qa | grep openssl

openssl-1.0.1e-16.el6.x86_64

Restart Ambari Agent(s) and Click Retry Failed on the Wizard.
```

`升级脚本`
```
# openssl version
OpenSSL 1.0.1g 7 Apr 2014

# sudo rpm -e --justdb --nodeps openssl
# sudo rpm -qa|grep openssl  

# sudo rpm -ivh --force http://mirror.centos.org/centos/6/os/x86_64/Packages/openssl-1.0.1e-42.el6.x86_64.rpm 

# rpm -qa|grep openssl
openssl-1.0.1e-42.el6.x86_64

# openssl version  
OpenSSL 1.0.1e-fips 11 Feb 2013

完美解决openssl bug...头疼了一阵...
```

`如果出现乱码：echo 'LANG="en_US.UTF-8"' > /etc/sysconfig/i18n,修改字符集即可解决！`

```
Error: Package: snappy-devel-1.0.5-1.el6.x86_64 (HDP-UTILS-1.1.0.20)
           Requires: snappy(x86-64) = 1.0.5-1.el6
           Installed: snappy-1.1.0-1.el6.x86_64 (@anaconda-CentOS-201311272149.x86_64/6.5)
               snappy(x86-64) = 1.1.0-1.el6
           Available: snappy-1.0.5-1.el6.x86_64 (HDP-UTILS-1.1.0.20)
               snappy(x86-64) = 1.0.5-1.el6

解决
sudo rpm -e snappy-1.1.0-1.el6.x86_64 or [sudo rpm -e snappy-1.1.0-1.el6.x86_64 --nodeps]
yum -y install snappy*
```

```
错误1：
File "/usr/lib/python2.6/site-packages/resource_management/core/shell.py", line 291, in _call
    raise Fail(err_msg)
resource_management.core.exceptions.Fail: Execution of '/usr/bin/yum -d 0 -e 0 -y install ambari-metrics-monitor' returned 1. Error: Package: ambari-metrics-monitor-2.1.0-1470.x86_64 (Updates-ambari-2.1.0)
           Requires: python-devel
 You could try using --skip-broken to work around the problem
** Found 6 pre-existing rpmdb problem(s), 'yum check' output follows:
1:libreoffice-core-4.0.4.2-9.el6.x86_64 has missing requires of libjawt.so()(64bit)
1:libreoffice-core-4.0.4.2-9.el6.x86_64 has missing requires of libjawt.so(SUNWprivate_1.1)(64bit)
1:libreoffice-ure-4.0.4.2-9.el6.x86_64 has missing requires of jre >= ('0', '1.5.0', None)
2:postfix-2.6.6-2.2.el6_1.x86_64 has missing requires of libmysqlclient.so.16()(64bit)
2:postfix-2.6.6-2.2.el6_1.x86_64 has missing requires of libmysqlclient.so.16(libmysqlclient_16)(64bit)
2:postfix-2.6.6-2.2.el6_1.x86_64 has missing requires of mysql-libs


错误2：
  File "/usr/lib/python2.6/site-packages/resource_management/core/sudo.py", line 37, in chown
    return os.chown(path, uid, gid)
OSError: [Errno 1] Operation not permitted: '/data0/www/bbs/uc_server/data/avatar/hadoop/hdfs/namenode'

yum search python | grep python-devel

```

> `造成这些错误都是安装linux的时候基础包未选择，缺包可以制作cdrom挂载，来安装即可解决！`

- 到此即可一步步安装hadoop集群...

# Step 6: Test 集群使用
```
[whoami@server1 ~]$ sudo -uhive hive
hive> show tables;
OK
Time taken: 1.36 seconds
hive> create table test(id int);
OK
Time taken: 1.998 seconds
hive>   insert into table test values (1), (2), (3);
Query ID = hive_20150831184109_0c75d1e8-1003-4ade-bacf-03cd7408082f
Total jobs = 1
Launching Job 1 out of 1


Status: Running (Executing on YARN cluster with App id application_1441014845188_0002)

--------------------------------------------------------------------------------
        VERTICES      STATUS  TOTAL  COMPLETED  RUNNING  PENDING  FAILED  KILLED
--------------------------------------------------------------------------------
Map 1 ..........   SUCCEEDED      1          1        0        0       0       0
--------------------------------------------------------------------------------
VERTICES: 01/01  [==========================>>] 100%  ELAPSED TIME: 32.24 s    
--------------------------------------------------------------------------------
Loading data to table default.test
Table default.test stats: [numFiles=1, numRows=3, totalSize=6, rawDataSize=3]
OK
Time taken: 41.354 seconds
hive> show tables;
OK
test
values__tmp__table__1
Time taken: 0.112 seconds, Fetched: 2 row(s)
hive> select * from test;
OK
1
2
3
Time taken: 0.258 seconds, Fetched: 3 row(s)

hive> select count(1) from test;
OK
3
Time taken: 1.705 seconds, Fetched: 1 row(s)
```

`相关组件使用一切正常...`

# 小插曲
> 安装过程中使用了桌面，火狐等安装命令
> yum install firefox
> yum groupinstall -y   "Desktop"   "Desktop Platform"   "Desktop Platform 
> Development"　 "Fonts" 　"General Purpose Desktop"　 "Graphical 
> Administration Tools"　 "Graphics Creation Tools" 　"Input Methods" 　"X 
> Window System" 　"Chinese Support [zh]"　"Internet Browser"
> 
> iso yum 源来安装一些基础包
> 
> sudo mount -o loop /home/whoami/rhel-server-6.7-x86_64-dvd.iso /mnt/cdimg/
> 
> $  cat rhel-source.repo 
> [rhel-Server]
> name=Red Hat Server
> baseurl=file:///mnt/cdimg
> enable=1
> gpgcheck=0

`总结：如果要安装一切顺利，可在安装操作系统时把linux基础组件一并安装！`
||
VV
```
yum groupinstall "Compatibility libraries" "Base" "Development tools"
yum groupinstall "debugging Tools" "Dial-up Networking Support"

同时把mysql，postgresql都安装好！
```

# 配置Ambari Metrics为分布式
默认安装时Ambari Metrics为embedded模式，这样收集的所有数据是存放在Collector节点的本地的，大量的Metrics数据会挤占大量的本地存储空间，该为分布式模式后Metrics数据会放置到HDFS上，所以通常这是安装Ambari后必备一个操作。具体的操作可以参考：
http://docs.hortonworks.com/HDPDocuments/Ambari-2.1.0.0/bk_ambari_reference_guide/content/_configuring_ambari_metrics_for_distributed_mode.html

配置Metrics数据的生命周期

大量的Metrics会占用非常大的存储空间，集群经常出现conllector挂掉，所在节点空间满了的情况，设定Metrics数据的保留时间（TTL）是很必要的，控制Metrics数据保留时间的参数位于ams-site.xml中，以下是相关的配置项：
配置项                                 默认值           描述
timeline.metrics.host.aggregator.ttl  86400 1 minute resolution data purge interval. Default is 1 day.
timeline.metrics.host.aggregator.minute.ttl 604800  Host based X minutes resolution data purge interval. Default is 7 days.(X = configurable interval, default interval is 2 minutes)
timeline.metrics.host.aggregator.hourly.ttl 2592000 Host based hourly resolution data purge interval. Default is 30 days.
timeline.metrics.host.aggregator.daily.ttl  31536000  Host based daily resolution data purge interval. Default is 1 year.
timeline.metrics.cluster.aggregator.minute.ttl  2592000 Cluster wide minute resolution data purge interval. Default is 30 days.
timeline.metrics.cluster.aggregator.hourly.ttl  31536000  Cluster wide hourly resolution data purge interval. Default is 1 year.
timeline.metrics.cluster.aggregator.daily.ttl 63072000  Cluster wide daily resolution data purge interval. Default is 2 years.


原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/


参考：https://cwiki.apache.org/confluence/display/AMBARI/Installation+Guide+for+Ambari+2.1.0
