---
title: Zabbix Use
date: 2016-01-02 18:49:58
category: BigData
tags: zabbix
---
# 监控概述
- 1、主机监控
    * 1.1 硬件
    * 1.2 Cpu
    * 1.3 Memory
    * IO
        * 2.1 Disk IO
        * 2.2 Network IO

- 2、业务监控
- 3、故障检测分析
- 4、应用监控

```
    不同业务类型CPU,MEM各种指标不同，IO密集型，CPU密集型，比如数据库服务器(IO,CPU)，大数据集群服务器不同业务类型(IO密集型，CPU密集型)，对监控指标健康评判有很大区别！
    
    1、CPU监控，idle time,user time,system time
    
    2、内存监控，total,used,free,shared,buffers(缓冲-加速操作),cached(减少IO,mem交互,增强数据读取效率)

    监控系统: 
        a.首先确定业务类型;
        b.熟悉监控指标;
        c.确定性能基准线;
        d.使用工具-获取数据-展示-设置阈值-触发报警-告警通知-通知升级;
```

# 环境准备
## 1. install EPEL
```
[whoami@apache-server ~]$ sudo rpm -ivh https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm
Retrieving https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm
warning: /var/tmp/rpm-tmp.UjvRv8: Header V3 RSA/SHA256 Signature, key ID 0608b895: NOKEY
Preparing...                ########################################### [100%]
   1:epel-release           ########################################### [100%]
```

## 2. install io util
```
http://www.tecmint.com/install-iotop-monitor-linux-disk-io-in-rhel-centos-and-fedora/

[whoami@apache-server ~]$ sudo yum update kernel 
[whoami@apache-server ~]$ sudo yum install python python-ctypes
[whoami@apache-server ~]$ sudo yum install iostat -y
[whoami@apache-server ~]$ sudo yum install iftop -y
[whoami@apache-server ~]$ sudo yum install iotop -y

[whoami@apache-server ~]$ iostat 
avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           0.11    0.00    0.26    0.39    0.00   99.24

Device:            tps   Blk_read/s   Blk_wrtn/s   Blk_read   Blk_wrtn
scd0              0.01         0.04         0.00        352          0
sda               1.11        77.50        12.72     675406     110836

[whoami@apache-server ~]$  iostat -n 1 2

[whoami@apache-server ~]$ iostat -x 1 1

[whoami@apache-server ~]$ sudo iftop -n 

[whoami@apache-server ~]$ sudo iotop -n 1
```

## 3. 准备2台主机
```
-- 提前做好hosts映射
[whoami@apache-server ~]$ hostname 
apache-server

[whoami@server1 ~]$ hostname 
server1

-- 替换国内yum源
http://mirrors.163.com/.help/CentOS6-Base-163.repo

[whoami@server1 yum.repos.d]$ sudo wget http://mirrors.163.com/.help/CentOS6-Base-163.repo
[whoami@server1 yum.repos.d]$ yum clean all && yum makecache

--关闭selinux，iptable
[whoami@apache-server conf]$ sudo setenforce 0 
[whoami@apache-server conf]$ cat /etc/selinux/config |grep SELINUX=disabled
SELINUX=disabled
```

## 4. 安装基础软件包
```
[whoami@apache-server ~]$ sudo  yum install httpd php mysql mysql-server php-pdo php-mysql gcc gcc-c++ glibc mysql mysql-devel libxml2-devel curl curl-devel net-snmp net-snmp-devel libssh2-devel OpenIPMI-devel php-gd php-xml php-mbstring php-bcmath -y
```

# zbbix install
## zabbix iso 
``` 
http://www.zabbix.com/download.php

Live CD/DVD (.iso) : 
    http://ncu.dl.sourceforge.net/project/zabbix/ZABBIX Latest Stable/2.4.6/Zabbix_2.4_x86_64_13.1.x86_64-2.4.6.iso

[whoami@apache-server 6]$ yum list|grep zabbix|wc -l
43
```

## Zabbix 环境准备
```
http://sourceforge.net/projects/zabbix/files/ZABBIX%20Latest%20Stable/2.4.7/zabbix-2.4.7.tar.gz/download

[whoami@apache-server zabbix]$ tar zxf zabbix-2.4.7.tar.gz 

-- start apache server
[whoami@apache-server zabbix]$ sudo /etc/init.d/httpd restart
Stopping httpd:                                            [  OK  ]
Starting httpd:                                            [  OK  ]

-- mysql 配置
[whoami@apache-server zabbix]$ sudo cp /usr/share/mysql/my-medium.cnf /etc/my.cnf 

[whoami@apache-server zabbix]$ sudo vim /etc/my.cnf 
# The MySQL server
[mysqld]
default-storage-engine = innodb
innodb_file_per_table
collation-server = utf8_general_ci
init-connect = 'set NAMES utf8'
character-set-server = utf8

[whoami@apache-server zabbix]$ sudo /etc/init.d/mysqld restart


[whoami@apache-server zabbix]$ sudo lsof -i :3306
COMMAND  PID  USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
mysqld  3316 mysql   11u  IPv4  49880      0t0  TCP *:mysql (LISTEN)

-- apache server test
[whoami@apache-server zabbix]$ cd /var/www/html/
[whoami@apache-server html]$ cat info.php 
<?php
 phpinfo();
?>
   验证：http://apache-server/info.php
```

## Zabbix init database
```
mysql> create database zabbix;
mysql> grant all on zabbix.* to zabbix@localhost identified by 'admin'; 
mysql> flush privileges;

--init database table
[whoami@apache-server mysql]$ pwd
/data/zabbix/zabbix-2.4.7/database/mysql
[whoami@apache-server mysql]$ mysql -u zabbix -padmin zabbix < schema.sql 
[whoami@apache-server mysql]$ mysql -u zabbix -padmin zabbix < images.sql 
[whoami@apache-server mysql]$ mysql -u zabbix -padmin zabbix < data.sql
[whoami@apache-server mysql]$ mysql -u zabbix -padmin -e 'use zabbix;show tables;'|wc -l
105
```

# Zabbix Source install Server
```
[whoami@apache-server zabbix-2.4.7]$ cd /data/zabbix/zabbix-2.4.7

[whoami@apache-server zabbix-2.4.7]$ ./configure --prefix=/data/zabbix/zabbix_server --enable-server --with-mysql --enable-ipv6 --with-net-snmp --with-libcurl --with-libxml2 --with-openipmi --with-ssh2

[whoami@apache-server zabbix-2.4.7]$ make install

[whoami@apache-server zabbix-2.4.7]$ ls /data/zabbix/zabbix_server/
etc  lib  sbin  share

-- copy 源码中web页面到apache服务器根目录
[whoami@apache-server php]$ cd /data/zabbix/zabbix-2.4.7/frontends/php
[whoami@apache-server php]$ mkdir /data/html/zabbix/
[whoami@apache-server php]$ cp -r * /data/html/zabbix/
[whoami@apache-server html]$ sudo chown -R apache.apache /var/www/html/ 
[whoami@apache-server etc]$ sudo chown -R apache.apache /data/html/

--修改配置文件，database,zabbix log
[whoami@apache-server zabbix-2.4.7]$ cd /data/zabbix/zabbix_server/
[whoami@apache-server etc]$ pwd
/data/zabbix/zabbix_server/etc

[whoami@apache-server etc]$ grep '^[a-Z]' zabbix_server.conf
LogFile=/tmp/zabbix_server.log
DBHost=localhost
DBName=zabbix
DBUser=zabbix
DBPassword=admin

--- starting zabbix server
[whoami@apache-server etc]$ /data/zabbix/zabbix_server/sbin/zabbix_server -c /data/zabbix/zabbix_server/etc/zabbix_server.conf

--日志目录&&端口
[whoami@apache-server etc]$ cat /tmp/zabbix_server.log 
[whoami@apache-server etc]$ lsof -i :10051|wc -l
55

-- php 配置文件修改
[whoami@apache-server etc]$ cat /etc/php.ini
post_max_size = 16M
max_execution_time = 300
max_input_time = 300
date.timezone = PRC
[whoami@apache-server etc]$ sudo /etc/init.d/httpd restart
Stopping httpd:                                            [  OK  ]
Starting httpd:                                            [  OK  ]

-- 访问zabbix web页面
    http://apache-server/zabbix/setup.php
    web页面安装zabbix...
    1. Check of pre-requisites 完全正常即可开始安装
```

# Zabbix yum install agent
```
[whoami@apache-server mysql]$ yum list|grep zabbix22
zabbix22.x86_64                             2.2.11-1.el6                 epel  

[whoami@apache-server mysql]$ sudo yum install zabbix22-agent -y
[whoami@server1 ~]$ sudo yum install zabbix22-agent -y

--agent 配置
[whoami@apache-server html]$ sudo vim /etc/zabbix_agentd.conf
[whoami@apache-server html]$ grep '^[a-Z]' /etc/zabbix/zabbix_agentd.conf |grep Server
Server=apache-server
ServerActive=127.0.0.1

[whoami@apache-server html]$ grep '^[a-Z]' /etc/zabbix/zabbix_agentd.conf 
PidFile=/var/run/zabbix/zabbix_agentd.pid
LogFile=/var/log/zabbix/zabbix_agentd.log
LogFileSize=0
Server=192.168.2.125
ServerActive=127.0.0.1
Hostname=Zabbix server

-- staring zabbix agent
[whoami@apache-server html]$ sudo /etc/init.d/zabbix-agentd start
Starting Zabbix agent:                                     [  OK  ]
```

# 替换zabbix中文字体
```
[whoami@apache-server fonts]$ pwd
/data/html/zabbix/fonts

[whoami@apache-server fonts]$ sudo mv DejaVuSans.ttf DejaVuSans.ttf.ori

[whoami@apache-server fonts]$ sudo mv msyh.ttf DejaVuSans.ttf

[whoami@apache-server fonts]$ sudo chown apache.apache *.ttf 
```

# 添加zabbix监控主机
```
[whoami@server1 ~]$ cat /etc/zabbix_agentd.conf |grep Server=192
Server=192.168.2.125

[whoami@server1 ~]$ sudo /etc/init.d/zabbix-agentd start
Starting Zabbix agent:                                     [  OK  ]
```

# zabbix发送邮件报警
```
[whoami@apache-server ~]$ sudo /etc/init.d/postfix start

[whoami@apache-server ~]$ sudo lsof -i :25   
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
master  1314 root   12u  IPv4  10348      0t0  TCP localhost:smtp (LISTEN)
master  1314 root   13u  IPv6  10350      0t0  TCP localhost:smtp (LISTEN)


-- 手动停掉一个agent，触发报警测试
[whoami@server1 ~]$ sudo /etc/init.d/zabbix-agentd stop      
Shutting down Zabbix agent:                                [  OK  ]

-- 自定义报警方式，上面方式无法发送邮件
```

# zabbix自定义shell命令监控
```
[whoami@server1 ~]$ sudo ps aux | grep mysql|grep -v grep -c
2

--agent上面实现
[whoami@server1 ~]$ vim /etc/zabbix_agentd.conf 
### Option: UserParameter
#       User-defined parameter to monitor. There can be several user-defined parameters.
#       Format: UserParameter=<key>,<shell command>
#       See 'zabbix_agentd' directory for examples.
#
# Mandatory: no
# Default:
# UserParameter=
UserParameter = test,ps aux|wc -l
UserParameters=mysql-check,ps aux | grep mysql|grep -v grep -c

[whoami@server1 ~]$ sudo /etc/init.d/zabbix-agentd restart
Shutting down Zabbix agent:                                [  OK  ]
Starting Zabbix agent:                                     [  OK  ]

--另外一个节点验证，监控是否可获取值
[whoami@apache-server ~]$ zabbix_get -s server1 -k mysql-check
2
[whoami@apache-server ~]$ zabbix_get -s server1 -k test
133

--在web页面添加监控项，定义触发器
```

# zabbix自定义shell脚本监控报警
```
--server端实现
[whoami@apache-server etc]$ sudo vim /data/zabbix/zabbix_server/etc/zabbix_server.conf

420 ### Option: AlertScriptsPath
421 #       Full path to location of custom alert scripts.
422 #       Default depends on compilation options.
423 #
424 # Mandatory: no
425 # Default:
426 # AlertScriptsPath=${datadir}/zabbix/alertscripts
AlertScriptsPath=/data/zabbix/zabbix_server/alertscripts

[whoami@apache-server etc]$ mkdir /data/zabbix/zabbix_server/alertscripts

--kill zabbix_server
[whoami@apache-server alertscripts]$ ps -ef|grep zabbix_server
[whoami@apache-server alertscripts]$ kill 1703

[whoami@apache-server alertscripts]$ /data/zabbix/zabbix_server/sbin/zabbix_server -c /data/zabbix/zabbix_server/etc/zabbix_server.conf

--到脚本目录写报警脚本
[whoami@apache-server alertscripts]$ cat sms.sh 
#!/bin/bash

sms_demo(){
        echo "$1" "$2" "$3" >> /tmp/sms.txt
}

main() {
        sms_demo "$1" "$2" "$3"
}

main "$1" "$2" "$3"

[whoami@apache-server alertscripts]$ sudo chown zabbix:zabbix sms.sh
[whoami@apache-server alertscripts]$ sudo chmod u+x sms.sh 

[whoami@apache-server alertscripts]$ sh sms.sh 1 2 3
[whoami@apache-server alertscripts]$ cat /tmp/sms.txt 
1 2 3

---web页面做如下操作:
    1、管理-->示警媒介类型的组态-->创建媒体类型，默认有三种sms,email,jabber
    2、管理-->用户-->成员-->示例媒介-->添加报警方式
    3、组态-->动作-->操作-->编辑-->修改发送方式
    4、报警声音开启,基本资料-->信息中-->选择开启

---测试报警
[whoami@apache-server alertscripts]$ tail -f /tmp/sms.txt 

[whoami@server1 ~]$ sudo /etc/init.d/mysqld stop 
Stopping mysqld:                                           [  OK  ]
[whoami@server1 ~]$ sudo /etc/init.d/mysqld start
Starting mysqld:                                           [  OK  ]

[whoami@apache-server alertscripts]$ cat /tmp/sms.txt 
whoami@itweet.cn PROBLEM: mysql is down Trigger: mysql is down
Trigger status: PROBLEM
Trigger severity: Disaster
Trigger URL: 

Item values:

1. mysql-check (linux-server1:mysql-check): 0
2. *UNKNOWN* (*UNKNOWN*:*UNKNOWN*): *UNKNOWN*
3. *UNKNOWN* (*UNKNOWN*:*UNKNOWN*): *UNKNOWN*

Original event ID: 157

whoami@itweet.cn OK: mysql is down Trigger: mysql is down
Trigger status: OK
Trigger severity: Disaster
Trigger URL: 

Item values:

1. mysql-check (linux-server1:mysql-check): 2
2. *UNKNOWN* (*UNKNOWN*:*UNKNOWN*): *UNKNOWN*
3. *UNKNOWN* (*UNKNOWN*:*UNKNOWN*): *UNKNOWN*

Original event ID: 157

--自定义报警信息值
1、组态-->动作-->动作
2、<默认信息>修改如下：
    {TRIGGER.NAME}
    {ITEM.NAME1} ({HOST.NAME1}:{ITEM.KEY1}): {ITEM.VALUE1}
3、恢复信息
    {TRIGGER.NAME}
    {ITEM.NAME1} ({HOST.NAME1}:{ITEM.KEY1}): {ITEM.VALUE1}

4、测试
[whoami@apache-server alertscripts]$ tail -f /tmp/sms.txt 
whoami@itweet.cn PROBLEM: mysql is down mysql is down
mysql-check (linux-server1:mysql-check): 0

whoami@itweet.cn OK: mysql is down mysql is down
mysql-check (linux-server1:mysql-check): 2
```

# web监控
```
[whoami@apache-server alertscripts]$ curl --head http://apache-server/zabbix/dashboard.php
HTTP/1.1 200 OK
Date: Tue, 05 Jan 2016 00:37:20 GMT
Server: Apache/2.2.15 (CentOS)
X-Powered-By: PHP/5.3.3
Set-Cookie: zbx_sessionid=9f0df7e514697a36becde98e2538c56c
Connection: close
Content-Type: text/html; charset=UTF-8
```


原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/


参考：https://www.zabbix.com/documentation/2.4/manual/installation/install_from_packages#red_hat_enterprise_linux_centos