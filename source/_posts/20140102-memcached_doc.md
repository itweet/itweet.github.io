---
title: memcached_doc
date: 2014-01-02 08:43:05
description: Memcached 是一个高性能的分布式内存对象缓存系统，用于动态Web应用以减轻数据库负载。
category: BigData
tags: MemDB
---

Memcached 是一个高性能的分布式内存对象缓存系统，用于动态Web应用以减轻数据库负载。它通过在内存中缓存数据和对象来减少读取数据库的次数，从而提高动态、数据库驱动网站的速度。Memcached基于一个存储键/值对的hashmap。其守护进程（daemon ）是用C写的，但是客户端可以用任何语言来编写，并通过memcached协议与守护进程通信。

https://github.com/gwhalin/Memcached-Java-Client

# 1、安装

## 源码安装
```
    wget http://www.danga.com/memcached/dist/memcached-1.2.0.tar.gz
    wget http://www.monkey.org/~provos/libevent-1.2.tar.gz
```

## yum安装基础依赖
```
    # yum install libevent libevent-devel -y
    # find / -name libevent*|grep so
    /usr/lib64/libevent_extra-1.4.so.2.1.3
    /usr/lib64/libevent-1.4.so.2
    /usr/lib64/libevent_core-1.4.so.2.1.3
    /usr/lib64/libevent_extra-1.4.so.2
    /usr/lib64/samba/libevents.so
    /usr/lib64/libevent.so
    /usr/lib64/libevent_core.so
    /usr/lib64/libevent_extra.so
    /usr/lib64/libevent_core-1.4.so.2
    /usr/lib64/libevent-1.4.so.2.1.3
    
    # tar -zxvf memcached-1.2.0.tar.gz 
    # cd memcached-1.2.0
    # yum install gcc -y   ！！error==configure: error: no acceptable C compiler found in $PATH
    # ./configure -with-libevent=/usr
    # make && make install  
```

## 检测安装是否成功
```
[root@itr-nodetest02 memcached-1.2.0]#  ls -al /usr/local/bin/mem*
-rwxr-xr-x 1 root root 113124 May 23 10:00 /usr/local/bin/memcached
-rwxr-xr-x 1 root root 117479 May 23 10:00 /usr/local/bin/memcached-debug
```

# 2、启动Memcached服务
## 2.1.启动Memcache的服务器端：
```	
    #  /usr/local/bin/memcached -d -m 10 -u root -l 192.168.2.203 -p 11211 -c 256 -P /tmp/memcached.pid

	-d选项是启动一个守护进程，
	-m是分配给Memcache使用的内存数量，单位是MB，我这里是10MB，
	-u是运行Memcache的用户，我这里是root，
	-l是监听的服务器IP地址，如果有多个地址的话，我这里指定了服务器的IP地址192.168.0.200，
	-p是设置Memcache监听的端口，我这里设置了12000，最好是1024以上的端口，
	-c选项是最大运行的并发连接数，默认是1024，我这里设置了256，按照你服务器的负载量来设定，
	-P是设置保存Memcache的pid文件，我这里是保存在 /tmp/memcached.pid，
```

## 3、测试Memcached:
```	
    # lsof -i :11211
	COMMAND    PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
	memcached 4142 root    3u  IPv4  45398      0t0  TCP itr-nodetest02:memcache (LISTEN)
	memcached 4142 root    4u  IPv4  45399      0t0  UDP itr-nodetest02:memcache 

	# yum install telnet -y
	# telnet 192.168.2.203 11211
	Trying 192.168.2.203...
	Connected to 192.168.2.203.
	Escape character is '^]'.
	^]
	telnet> quit
	Connection closed.
	[root@itr-nodetest02 memcached-1.2.0]# ps -ef|grep memcached
	root      4142     1  0 10:04 ?        00:00:00 /usr/local/bin/memcached -d -m 10 -u root -l 192.168.2.203 -p 11211 -c 256 -P /tmp/memcached.pid
```


