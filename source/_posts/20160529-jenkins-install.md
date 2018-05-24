---
title: jenkins-install
date: 2016-05-29 13:57:10
category: Linux
tags: jenkins
---
Jenkins是基于Java开发的一种持续集成工具，用于监控持续重复的工作，功能包括：
 + 1、持续的软件版本发布/测试项目。
 + 2、监控外部调用执行的工作。

# Jenkins-install
## For linux
```
sudo wget -O /etc/yum.repos.d/jenkins.repo http://pkg.jenkins-ci.org/redhat/jenkins.repo
sudo rpm --import http://pkg.jenkins-ci.org/redhat/jenkins-ci.org.key

yum search jenkins
sudo yum install jenkins

yum install java-1.7.0-openjdk

sudo service jenkins start/stop/restart
sudo chkconfig jenkins on
```

# Jenkins info
* Jenkins will be launched as a daemon on startup. See /etc/init.d/jenkins for more details.

* The 'jenkins' user is created to run this service. If you change this to a different user via the config file, you must change the owner of /var/log/jenkins, /var/lib/jenkins, and /var/cache/jenkins.

* Log file will be placed in /var/log/jenkins/jenkins.log. Check this file if you are troubleshooting Jenkins.

* /etc/sysconfig/jenkins will capture configuration parameters for the launch.

* By default, Jenkins listen on port 8080. Access this port with your browser to start configuration.  Note that the built-in firewall may have to be opened to access this port from other computers.  (See http://www.cyberciti.biz/faq/disable-linux-firewall-under-centos-rhel-fedora/ for instructions how to disable the firewall permanently)

* A Jenkins RPM repository is added in /etc/yum.repos.d/jenkins.repo
```
vim /etc/sysconfig/jenkins 

    JENKINS_PORT="8080"
    JENKINS_USER="jenkins"

sudo service jenkins start
sudo chkconfig jenkins on

# lsof -i :8080|wc -l
3
```

# Jenkins WebUI
```
/etc/init.d/iptables stop
```

第一次访问需要输入初始密码,而密码被写入到日志文件中，日志在`/var/log/jenkins/jenkins.log`中，如下部分截取，包括初始密码。WebUI访问链接为：http://YOURHOST:8080

```
$ cat /var/log/jenkins/jenkins.log 
 Jenkins initial setup is required. An admin user has been created and a password generated.
Please use the following password to proceed to installation:

e34406819211493d9b415b085097ef77

This may also be found at: /var/lib/jenkins/secrets/initialAdminPassword
```

接下来进入`Customize Jenkins`页面，选择安装模式，使用Install suggested plugins安装,接下来`Getting Started`页面会自动安装很多常用插件到Jenkins服务器上；jenkins插件的默认安装位置为`/var/lib/jenkins/plugins/`;通过命令`tail -f /var/log/jenkins/jenkins.log `了解plugin安装进度。`Create First Admin User`页面创建你的第一个用户，至此Jenkins安装完成。

# Disable the firewall
  如果Centso6.x访问页面失败需要关闭防火墙或者设置防火墙规则,也有可能是8080端口没有启动，可通过lsof -i :8080在后台判断，也可以通过crul YOURHOST:8080访问看是否是服务没有正常启动。
  ```
  /etc/init.d/iptables stop
  ```

## From Centos 7.x
```
firewall-cmd --zone=public --add-port=8080/tcp --permanent
firewall-cmd --zone=public --add-service=http --permanent
firewall-cmd --reload

firewall-cmd --list-all
```

## Linux | ps
```
[root@docker-machine jenkins]# ps -ef|grep jenkins
jenkins    6693      1  2 08:01 ?        00:00:39 /etc/alternatives/java -Dcom.sun.akuma.Daemon=daemonized -Djava.awt.headless=true -DJENKINS_HOME=/var/lib/jenkins -jar /usr/lib/jenkins/jenkins.war --logfile=/var/log/jenkins/jenkins.log --webroot=/var/cache/jenkins/war --daemon --httpPort=8080 --debug=5 --handlerCountMax=100 --handlerCountMaxIdle=20
```

通过命令我们其实可以知道，Jenkins.war路径，log,webroot,运行用户等路径,比如web应用发布路径为`/var/cache/jenkins/`。通过查询路径的权限信息了解，运行于那个用户下。

```
[root@docker-machine jenkins]# ls -ld /var/log/jenkins/
drwxr-x---. 2 jenkins jenkins 4096 5月  29 08:01 /var/log/jenkins/
```

# Jenkins blueocean-plugin
  https://github.com/jenkinsci/blueocean-plugin

# Install Jenkins with Docker
  https://wiki.jenkins-ci.org/display/JENKINS/Installing+Jenkins+with+Docker

参考：https://jenkins.io//blog/2016/05/26/introducing-blue-ocean/
    https://wiki.jenkins-ci.org/display/JENKINS/Installing+Jenkins+on+Red+Hat+distributions
    https://github.com/jenkinsci/blueocean-plugin
    http://ftp.yz.yamagata-u.ac.jp/pub/misc/jenkins/war/1.658/‘
    

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/