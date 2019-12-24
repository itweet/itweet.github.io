---
title: Docker Install Guide
date: 2016-08-12 16:50:22
category: Cloud
tags: docker
---
使用docker已经有1年多了，打算写一个系列，不知道能坚持吗？我太懒，只当为自己纪录吧！这一篇为docker基本使用文档！

Docker 是一個開源專案，誕生於 2013 年初，最初是 dotCloud 公司內部的一個業餘專案。它基於 Google 公司推出的 Go 語言實作。 專案後來加入了 Linux 基金會，遵從了 Apache 2.0 協議，原始碼在 GitHub 上進行維護。

网上文档成片，我就简单写写最佳实践吧。更多详细基础知识请参考文章最后的参考链接！

# Docker for Centos 6.x
Docker最为一个目前最流行的容器技术，可以支持多平台，主流unix系统，甚至是windows系列都能安装！这里演示Centos安装docker方式。并且给予这个版本给一些案例演示！

## Docker Install 
Centos 6.x默认没用docker的镜像源，需要手动安装一个epel源才可以找到包，并且包名docker-io，而在centos 7.x的包名确实docker
```
rpm -ivh https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm

yum info docker-io

sudo yum -y install docker-io
```

## start docker
手动启动docker，并且设置为开机自动启动！
```
/etc/init.d/docker start

chkconfig docker on
```

## docker hub
docker提供一个类似github的平台，可以供大家上传自己制作好的images，带有一定软件功能的docker容器，供全球使用者随意pull下来使用，并且修改参与共享。这就是docker hub。但是由于网络种种原因，很多源下载很慢或者失败，重拾几次或者用一些国内提供的docker hub源地址替代官方提供的docker hub，这样加快镜像的构建速度！
```
docker search centos

docker pull centos # For example: docker pull centos:5.11 or docker pull 

docker images
```

## dcoker container
  - 启动容器：docker run --name -h hostname
  - 停止容器：docker stop CONTAINER ID
  - 查看容器：docker ps 
  - 进入容器：docker exec | docker attach
  - 删除容器：docker rm option [-f]
  - 运行容器日志：docker logs CONTAINER ID

```
[root@server1 ~]# docker run centos /bin/echo 'Hello world'
Hello world
```

### 查看容器运行状态
```
[root@server1 ~]# docker ps -a
CONTAINER ID        IMAGE               COMMAND                CREATED              STATUS                          PORTS               NAMES
8c0e090d5b87        centos              "/bin/echo 'Hello wo   About a minute ago   Exited (0) About a minute ago                       sharp_cori
```

### 进入docker容器
```
[root@server1 ~]# docker run --name mydocker -it centos /bin/bash 

[root@4875a51a97cb /]# ps aux
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.0  11720  1864 ?        Ss   10:12   0:00 /bin/bash
root        18  0.0  0.0  35836  1488 ?        R+   10:13   0:00 ps aux

[root@4875a51a97cb tmp]# ls
ks-script-06FeP3

[root@4875a51a97cb tmp]# mkdir test

[root@4875a51a97cb tmp]# ls
ks-script-06FeP3  test

[root@4875a51a97cb tmp]# cat /etc/redhat-release 
CentOS Linux release 7.2.1511 (Core) 

[root@4875a51a97cb tmp]# exit
exit

[root@server1 ~]# docker ps -a
CONTAINER ID        IMAGE               COMMAND                CREATED             STATUS                      PORTS               NAMES
4875a51a97cb        centos              "/bin/bash"            12 minutes ago      Exited (0) 27 seconds ago                       mydocker            
8c0e090d5b87        centos              "/bin/echo 'Hello wo   16 minutes ago      Exited (0) 16 minutes ago                       sharp_cori    
```

### 获取centos6.6容器
```
[root@server1 ~]# docker pull centos:6.6

[root@server1 ~]# docker run --name mycentos -it centos:6.6 /bin/bash 

[root@eae421cf2af9 /]# ip ad li # CentOS 7 容器没有自带这个命令
13: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP 
    link/ether 02:42:ac:11:00:03 brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.3/16 scope global eth0
    inet6 fe80::42:acff:fe11:3/64 scope link 
       valid_lft forever preferred_lft forever
15: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN 
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever

[root@eae421cf2af9 /]# ifconfig eth0
eth0      Link encap:Ethernet  HWaddr 02:42:AC:11:00:03  
          inet addr:172.17.0.3  Bcast:0.0.0.0  Mask:255.255.0.0

[root@eae421cf2af9 /]# exit
exit

[root@server1 ~]# docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
centos              latest              60e65a8e4030        6 weeks ago         196.6 MB
centos              6.6                 12c9d795d85a        4 months ago        202.6 MB
```

### 启动终止容器
```
[root@server1 ~]# docker ps -a  # CONTAINER ID

[root@server1 ~]# docker start eae421cf2af9
eae421cf2af9

[root@server1 ~]# docker ps -a
CONTAINER ID        IMAGE               COMMAND                CREATED             STATUS                      PORTS               NAMES
eae421cf2af9        centos:6.6          "/bin/bash"            4 minutes ago       Up 19 seconds                                   mycentos            
4875a51a97cb        centos              "/bin/bash"            19 minutes ago      Exited (0) 7 minutes ago                        mydocker            
8c0e090d5b87        centos              "/bin/echo 'Hello wo   24 minutes ago      Exited (0) 24 minutes ago                       sharp_cori  

[root@server1 ~]# docker stop eae421cf2af9 
eae421cf2af9

[root@server1 ~]# docker ps -a
CONTAINER ID        IMAGE               COMMAND                CREATED             STATUS                       PORTS               NAMES
eae421cf2af9        centos:6.6          "/bin/bash"            5 minutes ago       Exited (137) 8 seconds ago                       mycentos            
4875a51a97cb        centos              "/bin/bash"            20 minutes ago      Exited (0) 8 minutes ago                         mydocker            
8c0e090d5b87        centos              "/bin/echo 'Hello wo   25 minutes ago      Exited (0) 25 minutes ago                        sharp_cori      
```

### 容器后台运行
```
[root@server1 ~]# docker run -d --name myid centos 
e2e9964282ab789a8f7cab4a397cbf22a8f91d83dbb80173698f1f64aa46b75e
[root@server1 ~]# docker ps -a
CONTAINER ID        IMAGE               COMMAND                CREATED              STATUS                          PORTS               NAMES
e2e9964282ab        centos              "/bin/bash"            3 seconds ago        Exited (0) 3 seconds ago                            myid   

[root@server1 ~]# docker run -d --name mycentos2 centos:6.6 /bin/bash 
986e7a8976c2be2d2bb1707eacd3277a2c3368f95bb02ed0919c2abf7e4ef5ed
[root@server1 ~]# docker ps -a
CONTAINER ID        IMAGE               COMMAND                CREATED              STATUS                          PORTS               NAMES
986e7a8976c2        centos:6.6          "/bin/bash"            5 seconds ago        Exited (0) 4 seconds ago                            mycentos2    

[root@server1 ~]# docker run -d --name mynginx nginx
Unable to find image 'nginx:latest' locally
latest: Pulling from nginx
77e39ee82117: Pull complete 
5eb1402f0414: Pull complete 
2f4509f0578a: Pull complete 
cc87edc856de: Pull complete 
9b35f2e19927: Pull complete 
6fbf62f05baf: Pull complete 
d4202c2d289c: Pull complete 
2b1e900b514d: Pull complete 
Digest: sha256:c42cbe1c6f4e91aa873a23c988826e3604b0a1ae90aaf3351923db855a953399
Status: Downloaded newer image for nginx:latest
2d7a73f9f499f65a3ed5d27ff7f85660611dedc8dbefb475371bfa9c7643d9d6

[root@server1 ~]# docker ps -a
CONTAINER ID        IMAGE               COMMAND                CREATED              STATUS                        PORTS               NAMES
2d7a73f9f499        nginx               "nginx -g 'daemon of   About a minute ago   Up About a minute             80/tcp, 443/tcp     mynginx      

[root@server1 ~]# docker ps -a|grep nginx
2d7a73f9f499        nginx               "nginx -g 'daemon of   2 minutes ago       Up 2 minutes                  80/tcp, 443/tcp     mynginx 
```

### 删除容器,必须先停止容器
```
[root@server1 ~]# docker rm 2d7a73f9f499
Error response from daemon: Cannot destroy container 2d7a73f9f499: Conflict, You cannot remove a running container. Stop the container before attempting removal or use -f
Error: failed to remove containers: [2d7a73f9f499]

[root@server1 ~]# docker rm 064fcc873164  #rm删除容器，rmi删除镜像
064fcc873164

[root@server1 ~]# docker rm 8965a9ba1b17 e2e9964282ab 986e7a8976c2
8965a9ba1b17
e2e9964282ab
986e7a8976c2

[root@server1 ~]# docker ps -a
CONTAINER ID        IMAGE               COMMAND                CREATED             STATUS                      PORTS               NAMES
2d7a73f9f499        nginx               "nginx -g 'daemon of   7 minutes ago       Up 7 minutes                80/tcp, 443/tcp     mynginx             
8c0e090d5b87        centos              "/bin/echo 'Hello wo   46 minutes ago      Exited (0) 46 minutes ago                       sharp_cori  
```

### 进入已经运行的容器方式
```
[root@server1 ~]# docker ps -l  #最后一个运行容器
CONTAINER ID        IMAGE               COMMAND                CREATED             STATUS              PORTS               NAMES
2d7a73f9f499        nginx               "nginx -g 'daemon of   15 minutes ago      Up 15 minutes       80/tcp, 443/tcp     mynginx 

[root@server1 ~]# docker attach 2d7a73f9f499  #此命令有些时候无法进去容器,或者不支持,如果ctrl+c,那么容器会自动停止
^C[root@server1 ~]# docker ps -a
CONTAINER ID        IMAGE               COMMAND                CREATED             STATUS                     PORTS               NAMES
2d7a73f9f499        nginx               "nginx -g 'daemon of   19 minutes ago      Exited (0) 3 seconds ago                       mynginx   

[root@server1 ~]# yum install util-linux   #通过这个软件包提供的命令进入容器

[root@server1 ~]# docker start 2d7a73f9f499
2d7a73f9f499

[root@server1 ~]# docker ps -a             
CONTAINER ID        IMAGE               COMMAND                CREATED             STATUS              PORTS               NAMES
2d7a73f9f499        nginx               "nginx -g 'daemon of   23 minutes ago      Up 11 seconds       80/tcp, 443/tcp     mynginx

[root@server1 ~]# docker inspect --format "{{.State.Pid}}" mynginx  #获取容器运行的pid
5782

[root@server1 ~]# nsenter --target 5782 --mount --uts --ipc --net --pid
root@2d7a73f9f499:/# 

root@2d7a73f9f499:/# ps aux
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.1  31484  2948 ?        Ss   11:09   0:00 nginx: master process nginx -g daemon off;
nginx        6  0.0  0.0  31860  1716 ?        S    11:09   0:00 nginx: worker process
root         7  0.0  0.1  20232  2028 ?        S    11:13   0:00 -bash

root@2d7a73f9f499:/# cat /etc/nginx/nginx.conf

root@2d7a73f9f499:/# cd /etc/nginx/

root@2d7a73f9f499:/etc/nginx# cat conf.d/default.conf |grep root
        root   /usr/share/nginx/html;   #nginx root目录

root@2d7a73f9f499:~# exit 
logout

[root@server1 ~]# cat in.sh  #进入容器脚本
#!/bin/bash
CNAME=$1
CPID=$(docker inspect --format "{{.State.Pid}}" $CNAME)
nsenter --target "$CPID" --mount --uts --ipc --net --pid

[root@server1 ~]# sh in.sh mynginx
root@2d7a73f9f499:/# exit
logout
```

## docker 网络访问 
```
[root@server1 ~]# brctl show
bridge name     bridge id               STP enabled     interfaces
docker0         8000.dad9e43403b6       no              veth44be944
virbr0          8000.525400353d8e       yes             virbr0-nic

[root@server1 ~]# iptables -t nat -L -n
Chain PREROUTING (policy ACCEPT)
target     prot opt source               destination         
DOCKER     all  --  0.0.0.0/0            0.0.0.0/0           ADDRTYPE match dst-type LOCAL 

Chain POSTROUTING (policy ACCEPT)
target     prot opt source               destination         
MASQUERADE  tcp  --  192.168.122.0/24    !192.168.122.0/24    masq ports: 1024-65535 
MASQUERADE  udp  --  192.168.122.0/24    !192.168.122.0/24    masq ports: 1024-65535 
MASQUERADE  all  --  192.168.122.0/24    !192.168.122.0/24    
MASQUERADE  all  --  172.17.0.0/16        0.0.0.0/0           

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination         
DOCKER     all  --  0.0.0.0/0           !127.0.0.0/8         ADDRTYPE match dst-type LOCAL 

Chain DOCKER (2 references)
target     prot opt source               destination      

[root@server1 ~]# sh in.sh mynginx  #进入容器可以上网
root@2d7a73f9f499:/# ping baidu.com
PING baidu.com (123.125.114.144): 56 data bytes
64 bytes from 123.125.114.144: icmp_seq=0 ttl=50 time=77.808 ms

root@2d7a73f9f499:/# ip ad li
37: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP 
    link/ether 02:42:ac:11:00:0b brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.11/16 scope global eth0
    inet6 fe80::42:acff:fe11:b/64 scope link 
       valid_lft forever preferred_lft forever
39: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN 
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever

root@2d7a73f9f499:/# ping 192.168.2.1
PING 192.168.2.1 (192.168.2.1): 56 data bytes
64 bytes from 192.168.2.1: icmp_seq=0 ttl=63 time=2.125 ms

root@2d7a73f9f499:/# ping 192.168.199.1  
PING 192.168.199.1 (192.168.199.1): 56 data bytes
64 bytes from 192.168.199.1: icmp_seq=0 ttl=251 time=6.571 ms

root@2d7a73f9f499:/# ip ro li
172.17.0.0/16 dev eth0  proto kernel  scope link  src 172.17.0.11 
default via 172.17.42.1 dev eth0 

root@2d7a73f9f499:/# exit 
logout
[root@server1 ~]# ifconfig 
docker0   Link encap:Ethernet  HWaddr DA:D9:E4:34:03:B6  
          inet addr:172.17.42.1  Bcast:0.0.0.0  Mask:255.255.0.0
          inet6 addr: fe80::7458:f8ff:fe2d:bec/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:62 errors:0 dropped:0 overruns:0 frame:0
          TX packets:21 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:4163 (4.0 KiB)  TX bytes:1891 (1.8 KiB)
```

docker提供一种端口映射功能，可以让我们访问宿主机IP，可以转发到容器内部，某个服务的端口，从而达到访问容器内服务的目的。有两种端口映射方式：1.随机映射 2.指定映射

### 随机映射容器端口到宿主机
```
[root@server1 ~]# docker run -P -d --name mynginx1 nginx
711c8bc3077d27196c4263cc75bb7fcb7f0bf2c02fb120054f011b9b9b134847

[root@server1 ~]# docker ps -a
CONTAINER ID        IMAGE               COMMAND                CREATED             STATUS              PORTS                                           NAMES
711c8bc3077d        nginx               "nginx -g 'daemon of   27 seconds ago      Up 27 seconds       0.0.0.0:32769->80/tcp, 0.0.0.0:32768->443/tcp   mynginx1            
2d7a73f9f499        nginx               "nginx -g 'daemon of   59 minutes ago      Up 35 minutes       80/tcp, 443/tcp                                 mynginx    
```

运行如上命令后，通过`docker ps -l`可以看到最后运行容器的信息，在这个时候通过宿主机IP:32769即可访问到容器中的nginx服务。

```
#获取运行容器的ip地址
[root@server1 ~]# docker inspect --format="{{.NetworkSettings.IPAddress}}" 39979df7a280
172.17.0.13
[root@server1 ~]# docker inspect --format="{{.NetworkSettings.IPAddress}}" mynginx2
172.17.0.13
[root@server1 ~]# docker inspect --format="{{.NetworkSettings.IPAddress}}" mynginx1
172.17.0.12
```

### 指定映射
```
[root@server1 ~]# docker stop 2d7a73f9f499
2d7a73f9f499

[root@server1 ~]# docker rm 2d7a73f9f499
2d7a73f9f499
[root@server1 ~]#  docker ps -a           

[root@server1 ~]# docker run -d -p 91:80 --name mynginx2 nginx
39979df7a280af50b1778094064002c413ebc47bba76133790c6c82663e242ed

[root@server1 ~]# docker ps -l
CONTAINER ID        IMAGE               COMMAND                CREATED             STATUS              PORTS                                           NAMES
39979df7a280        nginx               "nginx -g 'daemon of   22 seconds ago      Up 21 seconds       443/tcp, 0.0.0.0:91->80/tcp  
```

运行如上命令，访问宿主机ip:91即可访问到容器中的nginx.

## docker 数据管理
docker提供volume映射的方式，达到容器数据的持久化，为了保证容器一次构建全世界运行，所以不能依赖太多系统的特定变量。无状态的服务最理想化，但是很多时候有状态的服务有需要持久化存储数据，所以诞生这个功能。

### 数据卷
```
[root@server1 ~]# docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
nginx               latest              2b1e900b514d        2 weeks ago         134.4 MB
centos              latest              60e65a8e4030        6 weeks ago         196.6 MB
centos              6.6                 12c9d795d85a        4 months ago        202.6 MB

[root@server1 ~]# docker ps -l
CONTAINER ID        IMAGE               COMMAND                CREATED             STATUS              PORTS                         NAMES
39979df7a280        nginx               "nginx -g 'daemon of   2 hours ago         Up 2 hours          443/tcp, 0.0.0.0:91->80/tcp   mynginx2   

#启动一个容器centos,并且创建一个/data的数据卷
[root@server1 ~]# docker run -it --name volume-test1 -h nginx -v /data centos
[root@nginx /]# ps aux
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.0  11720  1868 ?        Ss   14:11   0:00 /bin/bash

[root@nginx /]# ls -ld /data/
drwxr-xr-x 2 root root 4096 Feb 11 14:11 /data/

[root@nginx /]# df -h|grep data
/dev/sda1                                                                                         20G  6.3G   13G  34% /data

#通过数据卷，容器把数据写入到物理主机那个地方，下面命令查看？
[root@server1 ~]# docker inspect -f {{.Volumes}} volume-test1
map[/data:/var/lib/docker/volumes/3f68063a817fee1155f4f50826eee3cf13827d4118fc4f614159dcb44431f88a/_data]

[root@server1~]# ls /var/lib/docker/volumes/3f68063a817fee1155f4f50826eee3cf13827d4118fc4f614159dcb44431f88a/_data/

[root@nginx /]# cd /data/
[root@nginx data]# pwd
/data
[root@nginx data]# touch docker_v

[root@server1 ~]# ls -l /var/lib/docker/volumes/3f68063a817fee1155f4f50826eee3cf13827d4118fc4f614159dcb44431f88a/_data/
total 0
-rw-r--r-- 1 root root 0 Feb 11 22:18 docker_v

#指定物理主机的一个目录，挂载到容器中的如何实现？
[root@server1 ~]# docker run -it --name volume-test2 -h centos -v /data:/data centos
[root@centos /]# ls /data/
CentOS-6.6-x86_64-bin-DVD1.iso  Centos-6.6-x68_64.raw  dfs  journal

[root@centos /]# ping baidu.com
PING baidu.com (220.181.57.217) 56(84) bytes of data.
64 bytes from 220.181.57.217: icmp_seq=1 ttl=53 time=76.7 ms

#挂载的目录为只读，不能写！在容器中无法写…
[root@server1 ~]# docker run -it --name volume-test2 -h centos -v /data:/data:ro centos

#挂载文件到容器,没有生效，新版可能不支持了
[root@server1 ~]# docker run -it --name volume-test3 -h centos -v /etc/hosts:/etc/hosts centos
[root@centos /]# cat /etc/hosts
172.17.0.17     centos
127.0.0.1       localhost
::1     localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
```

### 数据卷容器
```
[root@server1 ~]# docker run -it --name volume-test1 -h centos -v /data:/data centos  
[root@centos /]# exit
exit

[root@server1 ~]# docker ps -a
CONTAINER ID        IMAGE               COMMAND                CREATED             STATUS                     PORTS                         NAMES
af47fece9654        centos              "/bin/bash"            7 seconds ago       Exited (0) 4 seconds ago                                 volume-test1        
39979df7a280        nginx               "nginx -g 'daemon of   2 hours ago         Up 2 hours                 443/tcp, 0.0.0.0:91->80/tcp   mynginx2

#数据卷容器,使用其他容器已经挂载的数据卷路径,所有容器共享一个数据卷？
[root@server1 ~]# docker run -it --name volume-test2 -h centos --volumes-from volume-test1 centos      
[root@centos /]# ls /data/
CentOS-6.6-x86_64-bin-DVD1.iso  Centos-6.6-x68_64.raw  dfs  journal
```

## docker 镜像构建

### 手动构建镜像
```
#基于源码构建nginx镜像
$   yum install gcc-c++  
$   yum install zlib zlib-devel  
$   yum install openssl openssl--devel  
[root@nginx /]# rpm -ivh  http://download.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm

[root@server1 ~]# docker run --name nginx -h nginx -it centos:6.6 /bin/bash 
  注意：centos的镜像，不知道为何,在redhat宿主机运行,编译nginx不能通过…最后我只能在centos虚拟机重新尝试…编译报错：checking for C compiler ... found；替换了操作系统为centos依然如此,说明不是操作系统的问题，而是镜像问题，可忽略继续安装！

+++++++++++++++++++++++++++++++++++++++++++++++++
[root@centos ~]# cat /etc/redhat-release 
CentOS release 6.6 (Final)

[root@centos ~]# docker run --name nginx -h nginx -it centos:6.6 /bin/bash

[root@centos ~]# docker ps -a 
++++++++++++++++++++++++++++++++++++++++++++++++++

[root@centos ~]# docker images

[root@centos ~]# docker pull nginx

[root@centos ~]# docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
nginx               latest              2b1e900b514d        2 weeks ago         134.4 MB
centos              6.6                 12c9d795d85a        4 months ago        202.6 MB

[root@centos ~]# docker run --name nginx -h nginx -it centos:6.6 /bin/bash
[root@nginx /]# yum install -y wget gcc gcc-c++ make openssl openssl-devel tar

[root@nginx /]# wget http://nginx.org/download/nginx-1.9.11.tar.gz

---nginx的pcre模块
http://www.pcre.org/
[root@nginx /]# wget ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-8.37.tar.gz

[root@nginx /]# mv *.gz /usr/local/src/
[root@nginx /]# cd /usr/local/src/

[root@nginx src]# tar zxf pcre-8.37.tar.gz
[root@nginx src]# tar zxf nginx-1.9.11.tar.gz

[root@nginx src]# useradd -s /sbin/nologin -M www

[root@nginx src]# cd nginx-1.9.11
[root@nginx nginx-1.9.11]# ./configure --prefix=/usr/local/nginx --user=www --group=www --with-http_ssl_module --with-http_sub_module --with-pcre=/usr/local/src/pcre-8.37

[root@nginx nginx-1.9.11]# make

[root@nginx nginx-1.9.11]# make install

[root@nginx nginx-1.9.11]# ls -ld /usr/local/nginx
drwxr-xr-x 6 root root 4096 Feb 11 15:50 /usr/local/nginx

# 让容器启动的时候自动启动nginx,而nginx必须前台运行，nginx默认后台运行；docker会判断运行状态，导致运行之后就结束了，而没有达到启动nginx的目的
[root@nginx nginx-1.9.11]# yum install vim -y

[root@nginx nginx-1.9.11]# vim /usr/local/nginx/conf/nginx.conf
[root@nginx nginx-1.9.11]# head -1 /usr/local/nginx/conf/nginx.conf
daemon off;

[root@nginx nginx-1.9.11]# echo '/usr/local/nginx/sbin/nginx' > /etc/rc.local
[root@nginx nginx-1.9.11]# tail -1 /etc/rc.local    
/usr/local/nginx/sbin/nginx
[root@nginx nginx-1.9.11]# exit;
exit

[root@centos ~]# docker ps -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS                      PORTS               NAMES
f0031b268b26        centos:6.6          "/bin/bash"         About an hour ago   Exited (0) 24 seconds ago                       nginx     
[root@centos ~]# docker commit -m "centos6.6 and nginx-1.9.11" f0031b268b26 skyneteye/nginx:v1
9e78179003020986a7c970c314faff22706b55d762913d7b7f9e2d16702371e5


#测试构建的镜像
[root@centos ~]# docker run -d -p 92:80 skyneteye/nginx:v1
012e567670badb4983ba17066077ac27247c4befa8e999bedf4769a885db0795

============== 运行完成之后就自动退出了….

[root@centos ~]# docker run -it -h nginx skyneteye/nginx:v1
[root@nginx /]# vim /etc/rc.local 
[root@nginx /]# cat /etc/rc.local
#!/bin/sh
#
# This script will be executed *after* all the other init scripts.
# You can put your own initialization stuff in here if you don't
# want to do the full Sys V style init stuff.

touch /var/lock/subsys/local
[root@nginx /]# exit;
exit

[root@centos ~]# docker ps -l
CONTAINER ID        IMAGE                COMMAND             CREATED              STATUS                      PORTS               NAMES
5bfbd3201b47        skyneteye/nginx:v1   "/bin/bash"         About a minute ago   Exited (0) 29 seconds ago                       kickass_wozniak     
[root@centos ~]# docker commit -m "nginx v2" 5bfbd3201b47 skyneteye/nginx:v2
09c13432f72b6222df4aad7c71722354916a6dc7e03ecefbf43a530aedae8e09

[root@centos ~]# docker images

[root@centos ~]# docker run -d -p 99:80 skyneteye/nginx:v2 /usr/local/nginx/sbin/nginx
e30d529b741fe2c8152c6deba08dc9068cc59635fb3e2648992ea7910988c2d3
[root@centos ~]# docker ps -l
CONTAINER ID        IMAGE                COMMAND                CREATED             STATUS              PORTS                NAMES
e30d529b741f        skyneteye/nginx:v2   "/usr/local/nginx/sb   17 seconds ago      Up 16 seconds       0.0.0.0:99->80/tcp   boring_franklin   
```

执行如上最后一步命令，可以在宿主机IP:99访问到我们自己手动构建的nginx镜像。

### dockerfile
* 基础语法
    - FROM 依赖的基础镜像
    - MAINTAINER  维护者信息
    - RUN   Linux命令都加到RUN命令
    - ADD   COPY文件，会自动解压
    - WORKDIR   当前工作目录
    - VOLUME    目录挂在映射
    - EXPOSE    端口
    - RUN       运行容器

```
[root@centos ~]# mkdir /opt/docker-file
[root@centos ~]# cd /opt/docker-file/
[root@centos docker-file]# mkdir nginx
[root@centos docker-file]# cd nginx/
[root@centos nginx]# pwd
/opt/docker-file/nginx
[root@centos nginx]# ls
nginx-1.9.11.tar.gz  pcre-8.37.tar.gz

[root@centos nginx]# vim Dockerfile
[root@centos nginx]# cat Dockerfile 
# This is My first Dockerfile
# version 1.0
# Author: whoami

# Base images
FROM centos:6.6

# MAINTAINER info
MAINTAINER "you" <skynet199@foxmail.com>

# ADD
ADD nginx-1.9.11.tar.gz /usr/local/src
ADD pcre-8.37.tar.gz /usr/local/src

# RUN
RUN yum install -y wget gcc gcc-c++ make openssl-devel tar
RUN useradd -s /sbin/nologin -M www

#WORKDIR
WORKDIR /usr/local/src/nginx-1.9.11
RUN  ./configure --prefix=/usr/local/nginx --user=www --group=www --with-http_ssl_module --with-http_sub_module --with-pcre=/usr/local/src/pcre-8.37 && make && make install

RUN echo "daemon off;" >> /usr/local/nginx/conf/nginx.conf

# ENV
ENV PATH /usr/local/nginx/sbin:$PATH

# EXPOSE
EXPOSE 80

# VOLUME 
# VOLUME [ "/sys/fs/cgroup" ]

# CMD
CMD ["nginx"]

[root@centos nginx]# docker build -t nginx:1.9.11 /opt/docker-file/nginx/

此命令构建成功之后，即可开始测试容器的构建是否正确

[root@centos nginx]# docker ps -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS                         PORTS               NAMES
f0031b268b26        centos:6.6          "/bin/bash"         2 hours ago         Exited (0) About an hour ago                       nginx  

#前台运行
[root@centos nginx]# docker run -ti -v /data:/data:ro -p 80:80 nginx:1.9.11

#进入容器
[root@centos nginx]# docker run –d -h nginx -ti -v /data:/data:ro -p 80:80 nginx:1.9.11
247d1840b02e439872972832024517f306630f96f122a981e80f0a2a3948cd71

[root@centos nginx]# docker ps -l
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS                NAMES
247d1840b02e        nginx:1.9.11        "nginx"             18 seconds ago      Up 17 seconds       0.0.0.0:80->80/tcp   distracted_meitner

[root@centos nginx]# docker inspect --format "{{.State.Pid}}" 247d1840b02e
52876
[root@centos nginx]# nsenter --target 52876 --mount --uts --ipc --net --pid

[root@247d1840b02e /]# yum install lsof -y

#删除镜像
[root@centos nginx]# docker rmi -f nginx:1.9.11
```

## DockerUI & Shipyard && swarm
  docker可视化管理软件，docker集群的实现，后续内容介绍！

##  Docker-compose
    https://www.docker.com/products/docker-compose

## Docker Swarm
    https://www.docker.com/products/docker-swarm

## Docker-machine
    https://www.docker.com/products/docker-machine

## Install kali-linux-docker for Mac
    http://linux.im/2015/05/28/kali-linux-docker.html

## 优雅退出容器不会导致容器停止
```
  Ctrl+P+Q
```


参考：https://www.docker.com/
    https://philipzheng.gitbooks.io/docker_practice/content/introduction/what.html
    https://yeasy.gitbooks.io/docker_practice/content/introduction/what.html

