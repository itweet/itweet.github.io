---
title: zeppelin install
date: 2016-06-12 18:50:39
category: BigData
tags: zeppelin
---
Zeppelin是一个Web笔记形式的交互式数据查询分析工具，可以在线用scala和SQL对数据进行查询分析并生成报表。Zeppelin的后台数据引擎可以是Spark（目前只有Spark），开发者可以通过实现更多的解释器来为Zeppelin添加数据引擎。

 本文，介绍zeppelin 编译安装,入门使用介绍。

# Requirements
  + Git
  + Java 1.7
  + Tested on Mac OSX, Ubuntu 14.X, CentOS 6.X, Windows 7 Pro SP1
  + Maven (if you want to build from the source code)
  + Node.js Package Manager (npm, downloaded by Maven during build phase)

# 编译环境构建
## git install
```
[root@gitlab-machine ~]# git version
git version 1.7.1
```

## install jdk
```
[root@gitlab-machine ~]# wget http://download.oracle.com/otn-pub/java/jdk/7u79-b15/jdk-7u79-linux-x64.tar.gz

[root@gitlab-machine ~]# tar -zxf jdk-7u79-linux-x64.tar.gz -C /opt/

[root@gitlab-machine ~]# cd /opt/

[root@gitlab-machine opt]# ln -s jdk1.7.0_79 jdk

[root@gitlab-machine opt]# tail -5 ~/.bash_profile  
export JAVA_HOME=/opt/jdk
    
export PATH=.:$JAVA_HOME/bin:$PATH
    
export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar

[root@gitlab-machine opt]# source ~/.bash_profile 
[root@gitlab-machine opt]# java -version
java version "1.7.0_79"
Java(TM) SE Runtime Environment (build 1.7.0_79-b15)
Java HotSpot(TM) 64-Bit Server VM (build 24.79-b02, mixed mode)
```

## install maven
```
[root@gitlab-machine opt]# wget http://www.eu.apache.org/dist/maven/maven-3/3.3.3/binaries/apache-maven-3.3.3-bin.tar.gz

[root@gitlab-machine opt]# tar -zxf apache-maven-3.3.3-bin.tar.gz 

[root@gitlab-machine opt]# ln -s apache-maven-3.3.3 maven

[root@gitlab-machine opt]# echo "export MAVEN_HOME=/opt/maven" >> ~/.bash_profile

[root@gitlab-machine opt]# echo "export PATH=$MAVEN_HOME/bin:$PATH:$HOME/bin" >> ~/.bash_profile

[root@gitlab-machine opt]# source  ~/.bash_profile
[root@gitlab-machine opt]# mvn -version
Apache Maven 3.3.3 (7994120775791599e205a5524ec3e0dfe41d4a06; 2015-04-22T19:57:37+08:00)
Maven home: /opt/maven
Java version: 1.7.0_79, vendor: Oracle Corporation
Java home: /opt/jdk1.7.0_79/jre
Default locale: en_US, platform encoding: UTF-8
OS name: "linux", version: "2.6.32-504.el6.x86_64", arch: "amd64", family: "unix"
```

## install node.js
```
yum install http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm

yum repolist

[root@gitlab-machine opt]# yum search nodejs npm|wc -l
21

[root@gitlab-machine opt]# sudo yum install nodejs npm --enablerepo=epel

[root@gitlab-machine opt]# node -v
v0.10.42

[root@gitlab-machine opt]# npm -v
1.3.6

[root@gitlab-machine opt]# cd /data/
```

## build zeppline
```
[root@gitlab-machine opt]# cd /data/

[root@gitlab-machine data]# wget https://github.com/apache/zeppelin/archive/v0.5.6.zip

[root@gitlab-machine data]# unzip v0.5.6.zip 

[root@gitlab-machine data]# cd zeppelin-0.5.6/

[root@gitlab-machine zeppelin-0.5.6]# nohup mvn clean package -Pspark-1.6 -Phadoop-2.6 -Pyarn -Ppyspark -DskipTests > nohup.out &

[root@gitlab-machine zeppelin-0.5.6]# jobs
[1]+  Running                 nohup mvn clean package -Pspark-1.6 -Phadoop-2.6 -Pyarn -Ppyspark -DskipTests > nohup.out &

[root@gitlab-machine ~]# tail -f /data/zeppelin-0.5.6/nohup.out 
    [INFO] Reactor Build Order:
    [INFO] 
    [INFO] Zeppelin
    [INFO] Zeppelin: Interpreter
    [INFO] Zeppelin: Zengine
    [INFO] Zeppelin: Spark dependencies
    [INFO] Zeppelin: Spark
    [INFO] Zeppelin: Markdown interpreter
    [INFO] Zeppelin: Angular interpreter
    [INFO] Zeppelin: Shell interpreter
    [INFO] Zeppelin: Hive interpreter
    [INFO] Zeppelin: Apache Phoenix Interpreter
    [INFO] Zeppelin: PostgreSQL interpreter
    [INFO] Zeppelin: Tajo interpreter
    [INFO] Zeppelin: Flink
    [INFO] Zeppelin: Apache Ignite interpreter
    [INFO] Zeppelin: Kylin interpreter
    [INFO] Zeppelin: Lens interpreter
    [INFO] Zeppelin: Cassandra
    [INFO] Zeppelin: Elasticsearch interpreter
    [INFO] Zeppelin: web Application
    [INFO] Zeppelin: Server
    [INFO] Zeppelin: Packaging distribution
```

## Package
```
    $ export MAVEN_OPTS="-Xmx2g -XX:MaxPermSize=1024m"

    $ nohup mvn clean package -Pbuild-distr -Pspark-1.6 -Phadoop-2.6 -Pyarn -Ppyspark -DskipTests > nohup.out &

[INFO] Reading assembly descriptor: src/assemble/distribution.xml
[INFO] Copying files to /data/zeppelin-0.5.6/zeppelin-distribution/target/zeppelin-0.5.6-incubating
[INFO] Building tar: /data/zeppelin-0.5.6/zeppelin-distribution/target/zeppelin-0.5.6-incubating.tar.gz
[INFO] 
[INFO] --- maven-site-plugin:3.4:attach-descriptor (attach-descriptor) @ zeppelin-distribution ---
[INFO] ------------------------------------------------------------------------
[INFO] Reactor Summary:
[INFO] 
[INFO] Zeppelin ........................................... SUCCESS [  6.620 s]
[INFO] Zeppelin: Interpreter .............................. SUCCESS [ 13.075 s]
[INFO] Zeppelin: Zengine .................................. SUCCESS [  9.248 s]
[INFO] Zeppelin: Spark dependencies ....................... SUCCESS [ 44.619 s]
[INFO] Zeppelin: Spark .................................... SUCCESS [ 46.444 s]
[INFO] Zeppelin: Markdown interpreter ..................... SUCCESS [  0.620 s]
[INFO] Zeppelin: Angular interpreter ...................... SUCCESS [  0.423 s]
[INFO] Zeppelin: Shell interpreter ........................ SUCCESS [  0.470 s]
[INFO] Zeppelin: Hive interpreter ......................... SUCCESS [  1.962 s]
[INFO] Zeppelin: Apache Phoenix Interpreter ............... SUCCESS [  4.581 s]
[INFO] Zeppelin: PostgreSQL interpreter ................... SUCCESS [  0.453 s]
[INFO] Zeppelin: Tajo interpreter ......................... SUCCESS [  1.529 s]
[INFO] Zeppelin: Flink .................................... SUCCESS [  7.911 s]
[INFO] Zeppelin: Apache Ignite interpreter ................ SUCCESS [  0.604 s]
[INFO] Zeppelin: Kylin interpreter ........................ SUCCESS [  0.323 s]
[INFO] Zeppelin: Lens interpreter ......................... SUCCESS [  2.798 s]
[INFO] Zeppelin: Cassandra ................................ SUCCESS [01:14 min]
[INFO] Zeppelin: Elasticsearch interpreter ................ SUCCESS [  2.570 s]
[INFO] Zeppelin: web Application .......................... SUCCESS [01:02 min]
[INFO] Zeppelin: Server ................................... SUCCESS [01:58 min]
[INFO] Zeppelin: Packaging distribution ................... SUCCESS [01:02 min]
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 07:42 min
[INFO] Finished at: 2016-06-14T10:58:05+08:00
[INFO] Final Memory: 171M/466M
[INFO] ------------------------------------------------------------------------
```

# zeppelin deploy
  可以开始启动zeppline程序，在web可视化界面利用大数据技术，数据分析探索。
```
[root@gitlab-machine ]# cp /data/zeppelin-0.5.6/zeppelin-distribution/target/zeppelin-0.5.6-incubating.tar.gz  -C /data/deploy/

[root@gitlab-machine zeppelin-0.5.6-incubating]# bin/zeppelin-daemon.sh start
Log dir doesn't exist, create /data/deploy/zeppelin-0.5.6-incubating/logs
Pid dir doesn't exist, create /data/deploy/zeppelin-0.5.6-incubating/run
Zeppelin start                                             [  OK  ]

[root@gitlab-machine zeppelin-0.5.6-incubating]# bin/zeppelin-daemon.sh start
Zeppelin start                                             [  OK  ]
[root@gitlab-machine zeppelin-0.5.6-incubating]# ls logs/
zeppelin-root-gitlab-machine.log  zeppelin-root-gitlab-machine.out

[root@gitlab-machine zeppelin-0.5.6-incubating]# lsof -i :8080
COMMAND   PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
java    38243 root  597u  IPv6 388928      0t0  TCP *:webcache (LISTEN)
```

# zeppelin configuartion
  涉及的配置文件有两个：
   zeppelin-env.sh.template  
   zeppelin-site.xml.template
   复制出来直接修改相关参数即可,详情请参考：http://zeppelin.apache.org/docs/0.5.6-incubating/

# FAQ
## 'npm install --color=false' failed
```
[INFO] Zeppelin: web Application .......................... FAILURE [12:32 min]
[INFO] Zeppelin: Server ................................... SKIPPED
[INFO] Zeppelin: Packaging distribution ................... SKIPPED
[INFO] ------------------------------------------------------------------------
[INFO] BUILD FAILURE
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 02:04 h
[INFO] Finished at: 2016-06-13T18:12:54+08:00
[INFO] Final Memory: 129M/410M
[INFO] ------------------------------------------------------------------------
[ERROR] Failed to execute goal com.github.eirslett:frontend-maven-plugin:0.0.23:npm (npm install) on project zeppelin-web: Failed to run task: 'npm install --color=false' failed. (error code 1) -> [Help 1]
[ERROR] 
[ERROR] To see the full stack trace of the errors, re-run Maven with the -e switch.
[ERROR] Re-run Maven using the -X switch to enable full debug logging.
[ERROR] 
[ERROR] For more information about the errors and possible solutions, please read the following articles:
[ERROR] [Help 1] http://cwiki.apache.org/confluence/display/MAVEN/MojoFailureException
[ERROR] 
[ERROR] After correcting the problems, you can resume the build with the command

解决：
    $ cd zeppelin-web
    
    $ npm install
    > phantomjs@1.9.20 install /data/zeppelin-0.5.6/zeppelin-web/node_modules/karma-phantomjs-launcher/node_modules/phantomjs
    > node install.js

    PhantomJS not found on PATH
    Downloading https://github.com/Medium/phantomjs/releases/download/v1.9.19/phantomjs-1.9.8-linux-x86_64.tar.bz2
    Saving to /data/zeppelin-0.5.6/zeppelin-web/node_modules/karma-phantomjs-launcher/node_modules/phantomjs/phantomjs/phantomjs-1.9.8-linux-x86_64.tar.bz2  #＃这个文件无法下载，去这个地址下载：“https://github-cloud.s3.amazonaws.com”出现连接"Connection timed out.“错误。重新执行多次即可通过，这个是世界2大互联网之间联系微妙的原因啦。
    Receiving...
    [==--------------------------------------] 4%
```

## 'grunt --no-color' failed.
```
    [ERROR] Failed to execute goal com.github.eirslett:frontend-maven-plugin:0.0.23:grunt (grunt build) on project zeppelin-web: Failed to run task: 'grunt --no-color' failed. (error code 3) -> [Help 1]
```

解决：
```
    [root@gitlab-machine zeppelin-0.5.6]# cd zeppelin-web/
    [root@gitlab-machine zeppelin-web]# grunt build
    ERROR [launcher]: No binary for PhantomJS browser on your platform.
    Please, set "PHANTOMJS_BIN" env variable.
    Warning: Task "karma:unit" failed. Use --force to continue.

    1. 初步查看日志，可以看到是由于上一个错误的库phantomjs引起的错误。
    2. 进一步查看日志如下，发现在执行npm install可以通过了，而执行“bower --allow-root install”开始报错。
    [INFO] --- frontend-maven-plugin:0.0.23:npm (npm install) @ zeppelin-web ---
    [INFO] Running 'npm install --color=false' in /data/zeppelin-0.5.6/zeppelin-web
    [INFO] 
    [INFO] --- frontend-maven-plugin:0.0.23:bower (bower install) @ zeppelin-web ---
    [INFO] Running 'bower --allow-root install' in /data/zeppelin-0.5.6/zeppelin-web
    [ERROR] [{
    [ERROR]   "level": "info",
    [ERROR]   "id": "cached",
    [ERROR]   "message": "https://github.com/angular/bower-angular.git#1.3.8",

    [root@gitlab-machine zeppelin-0.5.6]# cd zeppelin-web/
    [root@gitlab-machine zeppelin-web]# bower install

    最终修改pom.xml信息解决问题,网上这么说的，编译过后启动web页面首页显示有些许问题，无奈啊，前端太渣，这个项目用到了grunt，bower，node，npm等前端技术，这个web模块比较难通过，tez-ui也一样，相对来说编译都不那么顺利。
<plugin>
    <execution>
      <id>install node and npm</id>
      <goals>
        <goal>install-node-and-npm</goal>
      </goals>
      <configuration>
        <nodeVersion>v0.10.18</nodeVersion>
        <npmVersion>1.3.8</npmVersion>
      </configuration>
    </execution>
    
    <execution>
      <id>npm install</id>
      <goals>
        <goal>npm</goal>
      </goals>
    </execution>

     <execution>
      <id>bower install</id>
      <goals>
          <goal>bower</goal>
      </goals>
      <configuration>
        <arguments>--allow-root install</arguments>
      </configuration>
    </execution>

  <execution>
      <id>grunt build</id>
      <goals>
          <goal>grunt</goal>
      </goals>
      <configuration>
        <arguments>--no-color --force</arguments>
      </configuration>
    </execution>

  </executions>
</plugin>
```

## Address already in use
 需要注意的是，Zeppelin默认是在8080端口上启动相关的web服务的，在你服务器上，如果这个端口已经被占用了，那么会导致Zeppelin启动失败，并在日志里面抛出以下的异常；ps:我的这个报错就因为我在主机上部署了gitlab导致端口被占用：
```
ERROR [2016-06-14 11:05:35,848] ({main} ZeppelinServer.java[main]:112) - Error while running jettyServer
java.net.BindException: Address already in use
        at sun.nio.ch.Net.bind0(Native Method)
```

## Installing Zeppelin on an Ambari-Managed Cluster
```
参考：http://hortonworks.com/hadoop-tutorial/apache-zeppelin-hdp-2-4/
```

参考地址：https://github.com/apache/zeppelin/
        http://zeppelin.apache.org/docs/0.5.6-incubating/install/install.html
        http://zeppelin.apache.org/docs/0.5.6-incubating/manual/interpreters.html
        https://www.tutorialspoint.com/zookeeper/zookeeper_cli.htm


