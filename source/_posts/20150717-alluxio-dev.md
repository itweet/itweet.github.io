---
title: alluxio-dev
date: 2015-07-17 09:14:07
category: BigData
tags: alluxio
---

# 1、获取tachyon源码
```
	git clone git@github.com:amplab/tachyon.git
```

# 2、tachyon的编译支持hadoop2.2.0
	$ cd tachyon
	$ mvn clean package -Djava.version=1.7 -Dhadoop.version=2.2.0 -DskipTests
	[INFO] Scanning for projects...
	[INFO] ------------------------------------------------------------------------
	[INFO] Reactor Build Order:
	[INFO] 
	[INFO] Tachyon Project Parent
	[INFO] Tachyon Project Core
	[INFO] Tachyon Project Client
	[INFO]                                                                         
	[INFO] ------------------------------------------------------------------------
	[INFO] Building Tachyon Project Parent 0.5.0
	[INFO] ------------------------------------------------------------------------
	[INFO] 
	[INFO] --- maven-clean-plugin:2.4.1:clean (default-clean) @ tachyon-parent ---
	[INFO] 
	[INFO] --- maven-enforcer-plugin:1.0:enforce (enforce-maven) @ tachyon-parent ---
	[INFO]                                                                         
	[INFO] ------------------------------------------------------------------------
	[INFO] Building Tachyon Project Core 0.5.0
	[INFO] ------------------------------------------------------------------------
	[INFO] 
	[INFO] --- maven-clean-plugin:2.4.1:clean (default-clean) @ tachyon ---
	[INFO] Deleting /usr/local/tachyon-0.5.0/core/target
	[INFO] 
	[INFO] --- maven-enforcer-plugin:1.0:enforce (enforce-maven) @ tachyon ---
	[INFO] 
	[INFO] --- maven-resources-plugin:2.5:resources (default-resources) @ tachyon ---
	[debug] execute contextualize
	[INFO] Using 'UTF-8' encoding to copy filtered resources.
	[INFO] Copying 1 resource
	[INFO] 
	[INFO] --- maven-compiler-plugin:3.1:compile (default-compile) @ tachyon ---
	[INFO] Changes detected - recompiling the module!
	[INFO] Building jar: /usr/local/tachyon-0.5.0/client/target/tachyon-client-0.5.0.jar
	[INFO] 
	[INFO] --- maven-assembly-plugin:2.4:single (make-assembly) @ tachyon-client ---
	[INFO] Building jar: /usr/local/tachyon-0.5.0/client/target/tachyon-client-0.5.0-jar-with-dependencies.jar
	[INFO] ------------------------------------------------------------------------
	[INFO] Reactor Summary:
	[INFO] 
	[INFO] Tachyon Project Parent ............................ SUCCESS [1.675s]
	[INFO] Tachyon Project Core .............................. SUCCESS [1:08.545s]
	[INFO] Tachyon Project Client ............................ SUCCESS [21.605s]
	[INFO] ------------------------------------------------------------------------
	[INFO] BUILD SUCCESS
	[INFO] ------------------------------------------------------------------------
	[INFO] Total time: 1:32.185s
	[INFO] Finished at: Sat Jan 17 08:38:26 CST 2015
	[INFO] Final Memory: 39M/159M
	[INFO] ------------------------------------------------------------------------

> 注意版本：0.7+的版本对项目结构做了重构,模块会增多！

参考：
  - http://www.alluxio.org/
  - http://www.alluxio.org/docs/master/cn/Getting-Started.html


原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/