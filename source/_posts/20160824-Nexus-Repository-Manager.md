---
title: Nexus Repository Manager 
date: 2016-08-24 18:06:29
category: BigData
tags: nexus
---
搭建nexus私服，功能我就不一一列举了。好处多多。我这里选择一个openstack云主机来演示，如何通过docker这样的技术，以非常优雅的方式，自动安装好企业内部的私服服务器！

云主机信息
  - 云硬盘：Disk /dev/vdb: 1073.7 GB, 1073741824000 bytes, 2097152000 sectors
  - 系统盘：Disk /dev/vda: 53.7 GB, 53687091200 bytes, 104857600 sectors
  - 内存：8G
  - CPU: 2 core
  - Linux: CentOS Linux release 7.2.1511 (Core) 

格式化云硬盘自动挂载
```
mkfs.xfs -L /data /dev/vdb  

mkdir /data

echo "LABEL=/data           /data                 xfs    defaults        0 1" >> /etc/fstab 

mount -a && mount
```

Docker安装
```
yum install docker -y

systemctl start docker.service

systemctl enable docker.service 
```

Nexus安装
```
docker pull sonatype/nexus
```

* Volume mapping to local host machine:

```
mkdir /data/nexus-data && chown -R 200 /data/nexus-data

docker run -d -p 8081:8081 --name nexus -v /data/nexus-data:/sonatype-work sonatype/nexus

docker logs -f nexus
```

* For examples: 
```
docker ps -l|grep Up
9ddcacef915c        sonatype/nexus      "/bin/sh -c '${JAVA_H"   8 minutes ago       Up 4 minutes        0.0.0.0:8081->8081/tcp   nexus
```

* To test:
```
    curl http://localhost:8081/service/local/status
```

* Note:
    Default credentials are: admin / admin123

Nexus dockerfile
 https://hub.docker.com/r/sonatype/nexus/
```
vi Dockerfile

FROM       centos:centos7
MAINTAINER Sonatype <cloud-ops@sonatype.com>

ENV SONATYPE_WORK /sonatype-work
ENV NEXUS_VERSION 2.13.0-01

ENV JAVA_HOME /opt/java
ENV JAVA_VERSION_MAJOR 8
ENV JAVA_VERSION_MINOR 74
ENV JAVA_VERSION_BUILD 02

RUN yum install -y \
  curl tar createrepo \
  && yum clean all

# install Oracle JRE
RUN mkdir -p /opt \
  && curl --fail --silent --location --retry 3 \
  --header "Cookie: oraclelicense=accept-securebackup-cookie; " \
  http://download.oracle.com/otn-pub/java/jdk/${JAVA_VERSION_MAJOR}u${JAVA_VERSION_MINOR}-b${JAVA_VERSION_BUILD}/server-jre-${JAVA_VERSION_MAJOR}u${JAVA_VERSION_MINOR}-linux-x64.tar.gz \
  | gunzip \
  | tar -x -C /opt \
  && ln -s /opt/jdk1.${JAVA_VERSION_MAJOR}.0_${JAVA_VERSION_MINOR} ${JAVA_HOME}

RUN mkdir -p /opt/sonatype/nexus \
  && curl --fail --silent --location --retry 3 \
    https://download.sonatype.com/nexus/oss/nexus-${NEXUS_VERSION}-bundle.tar.gz \
  | gunzip \
  | tar x -C /tmp nexus-${NEXUS_VERSION} \
  && mv /tmp/nexus-${NEXUS_VERSION}/* /opt/sonatype/nexus/ \
  && rm -rf /tmp/nexus-${NEXUS_VERSION}

RUN useradd -r -u 200 -m -c "nexus role account" -d ${SONATYPE_WORK} -s /bin/false nexus

VOLUME ${SONATYPE_WORK}

EXPOSE 8081
WORKDIR /opt/sonatype/nexus
USER nexus
ENV CONTEXT_PATH /
ENV MAX_HEAP 768m
ENV MIN_HEAP 256m
ENV JAVA_OPTS -server -Djava.net.preferIPv4Stack=true
ENV LAUNCHER_CONF ./conf/jetty.xml ./conf/jetty-requestlog.xml
CMD ${JAVA_HOME}/bin/java \
  -Dnexus-work=${SONATYPE_WORK} -Dnexus-webapp-context-path=${CONTEXT_PATH} \
  -Xms${MIN_HEAP} -Xmx${MAX_HEAP} \
  -cp 'conf/:lib/*' \
  ${JAVA_OPTS} \
  org.sonatype.nexus.bootstrap.Launcher ${LAUNCHER_CONF}

```

Nexus 使用
    Google之...

### FAQ
 启动报错，如下，因为selinux没有关闭导致，关闭即可解决
```
WARN  [jetty-main-1] *SYSTEM org.sonatype.nexus.util.LockFile - Failed to write lock file
java.io.FileNotFoundException: /sonatype-work/nexus.lock (Permission denied)

# setenforce 0

# getenforce 
Permissive

# vi /etc/selinux/config 
  SELINUX=permissive

```


