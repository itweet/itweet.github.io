---
title: Docker Install for centos 7
date: 2016-08-13 16:52:20
category: Cloud
tags: docker
---
Install Docker which is the Operating System-Level Virtualization Tool, which automates the deployment of applications inside Containers.

[1] Install Docker.
```
[root@kubernetes-controller ~]#  yum -y install docker

[root@kubernetes-controller ~]# systemctl start docker 
[root@kubernetes-controller ~]# systemctl enable docker 
```

[2] Download the official image and create a Container and output the words "Welcome to the Docker World" inside the Container.
```
# download a centos image
[root@kubernetes-controller ~]# docker pull centos 
Using default tag: latest
Trying to pull repository docker.io/library/centos ... 
latest: Pulling from docker.io/library/centos
3d8673bd162a: Pulling fs layer 
.....
.....
3d8673bd162a: Pull complete 
Digest: sha256:a66ffcb73930584413de83311ca11a4cb4938c9b2521d331026dad970c19adf4
Status: Downloaded newer image for docker.io/centos:latest

# show images 
[root@kubernetes-controller ~]# docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
docker.io/centos    latest              970633036444        2 weeks ago         196.7 MB

# run echo inside Container
[root@kubernetes-controller ~]# docker run centos /bin/echo "Welcome to the Docker World" 
WARNING: IPv4 forwarding is disabled. Networking will not work.
Welcome to the Docker World
```

[3] Connect to the interactive session of a Container with "i" and "t" option like follows. If exit from the Container session, the process of a Container finishes.
```
[root@kubernetes-controller ~]# docker run -i -t centos /bin/bash 
[root@97e4ec079410 /]#    # Container's console

[root@97e4ec079410 /]# uname -a 
Linux 97e4ec079410 3.10.0-327.el7.x86_64 #1 SMP Thu Nov 19 22:10:57 UTC 2015 x86_64 x86_64 x86_64 GNU/Linux

[root@97e4ec079410 /]# exit
exit

[root@kubernetes-controller ~]#     # success run docker images
```

[4] If exit from the Container session with keeping container's process, push Ctrl+p, and Ctrl+q key
```
[root@kubernetes-controller ~]# docker run -i -t centos /bin/bash 
[root@dedab2202eb5 /]# 

# Ctrl+p, Ctrl+q key to back to Host's console
[root@dedab2202eb5 /]# [root@kubernetes-controller ~]#     


# show docker last run container process
[root@kubernetes-controller ~]# docker ps -l
CONTAINER ID        IMAGE               COMMAND             CREATED              STATUS              PORTS               NAMES
dedab2202eb5        centos              "/bin/bash"         About a minute ago   Up About a minute                       fervent_rosalind


# connect to container's session
[root@kubernetes-controller ~]# docker attach dedab2202eb5
[root@dedab2202eb5 /]#     # connected success


# shutdown container's process from Host's console

[root@kubernetes-controller ~]# docker kill dedab2202eb5

[root@kubernetes-controller ~]# docker ps 
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
```


原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/
