---
title: apache-hadoop-insall
date: 2017-05-07 09:02:11
category: BigData
tags: hadoop
---
1、 core-site.xml
```
	<configuration>
		<property>
			<name>fs.defaultFS</name>
			<value>hdfs://server01:9000</value>
		</property>
		<property>
			<name>hadoop.tmp.dir</name>
			<value>/usr/local/hadoop-2.5.0-cdh5.2.0/tmp</value>
		</property>
		<property>
			<name>fs.trash.interval</name>
			<value>2000</value>
		</property>
	</configuration>
```

2、hdfs-site.xml
```
 	<configuration>
	    <property>
	        <name>dfs.replication</name>
	        <value>1</value>
	    </property>
	    <property>
	        <name>dfs.permissions</name>
	        <value>false</value>
	    </property>
	</configuration>
```

3、yarn-site.xml
```
 	<configuration>
 		<property>
			<name>yarn.resourcemanager.hostname</name>
			<value>server01</value>
		</property>
        <property>
                <name>yarn.nodemanager.aux-services</name>
                <value>mapreduce_shuffle</value>
        </property>
	</configuration>
```

4、mapred-site.xml
```	
 	<configuration>
	    <property>
	        <name>mapreduce.framework.name</name>
	        <value>yarn</value>
	    </property>
	</configuration>
```

5、slaves
```
	server01
```

5、格式化hdfs文件系统
```
	bin/hdfs namenode -format
```

6、启动
```
	hadoop-daemon.sh start namenode/datanode
	yarn-daemon.sh start resourcemanager/nodemanager
```

7、测试
```
	hadoop jar hadoop-mapreduce-examples-2.4.0.jar wordcount /testdata /output
```

