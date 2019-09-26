---
title: Kubernetes Use Persistent Storage
date: 2016-08-16 17:20:41
category: Cloud
tags: kubernates
---
It's necessary to use external storage if you'd like to use Persistent Data.
    
For exmaple, Create a Pod with mounting external storage which is mapped with a directory for saving data on the Node Pod runs. The environment and Container image on this exmaple are the same with here.

# Container image for exmaples
For example, Create a Dockerfile to install httpd and add index.html, and also start httpd with 80 port.
```
# create a Dockerfile
[root@kubernetes-controller ~]# vi Dockerfile
FROM centos
MAINTAINER serverworld <admin@itweet.cn>
RUN yum -y install httpd
RUN echo "Hello DockerFile by itweet.cn" > /var/www/html/index.html
EXPOSE 80
CMD ["-D", "FOREGROUND"]
ENTRYPOINT ["/usr/sbin/httpd"]

# build image ⇒ docker build -t [image name]:[tag] . 
[root@kubernetes-controller ~]# docker build -t apache_server:latest ./Dockerfile 
unable to prepare context: context must be a directory: /root/Dockerfile
[root@kubernetes-controller ~]# docker build -t apache_server:latest .
Sending build context to Docker daemon 948.7 kB
Step 1 : FROM centos
 ---> 970633036444
Step 2 : MAINTAINER serverworld <admin@itweet.cn>
 ---> Running in 7f20b2eff551
 ---> 8041da7bcf1a
Removing intermediate container 7f20b2eff551
Step 3 : RUN yum -y install httpd
 ---> Running in 81073cca988b
Loaded plugins: fastestmirror, ovl
Determining fastest mirrors
 * base: mirrors.tuna.tsinghua.edu.cn
 * extras: mirrors.tuna.tsinghua.edu.cn
 * updates: mirror.bit.edu.cn
Resolving Dependencies
...
...
Step 7 : ENTRYPOINT /usr/sbin/httpd
 ---> Running in 16fa3fcd76dc
 ---> d165379a81f0
Removing intermediate container 16fa3fcd76dc
Successfully built d165379a81f0

[root@kubernetes-controller ~]# docker images 
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
apache_server       latest              d165379a81f0        52 seconds ago      321.9 MB
docker.io/centos    latest              970633036444        2 weeks ago         196.7 MB

[root@kubernetes-controller ~]# docker run -d -p 80:80 apache_server 
505d10f894084e1ea417091f6adbe44a7d8df8c7518c5c5dd3ddce1c5f0ed05f

[root@kubernetes-controller ~]# docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                NAMES
505d10f89408        apache_server       "/usr/sbin/httpd -D F"   14 seconds ago      Up 13 seconds       0.0.0.0:80->80/tcp   pensive_bhaskara

[root@kubernetes-controller ~]# curl http://localhost/
Hello DockerFile by itweet.cn
```


# Container image loads to All Nodes

[1] Copy a container image just created above to all other Nodes like follows.
```
# output container image to a file
[root@kubernetes-controller ~]# docker save apache_server > apache_server.tar

# copy the image to other Nodes
[root@kubernetes-controller ~]# scp apache_server.tar kubernetes-node-1:/root/
...
...
[root@kubernetes-controller ~]# scp apache_server.tar kubernetes-node-3:/root/
```

[2] Load the comtainer image just copied.
```
[root@kubernetes-node-1 ~]# docker load < apache_server.tar 
[root@kubernetes-node-1 ~]#  docker images apache_server
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
apache_server       latest              d165379a81f0        8 minutes ago       321.9 MB
```

关于kubernetes创建pod时，使用的镜像本地已经存在，但还一直在下载。如何create pod时可以跨过下载这一步，直接使用本地镜像？
    http://dockone.io/question/1075

#  Create a httpd Pods
[1] Admin Node.
```
[root@kubernetes-controller ~]# cat pod-httpd.yaml 
apiVersion: v1
kind: Pod
metadata:
  name: apache-httpd
spec:
  containers:
  - name: apache-httpd
    image: httpd
    ports:
    - containerPort: 80
    volumeMounts:
    # the volume to use (it's the one defined in "volumes" section)
    - name: httpd-storage
      # mount point inside Container
      mountPath: /var/www/html
  volumes:
  # any name you like
  - name: httpd-storage
    hostPath:
      # the directory on Host Node for saving data
      path: /tmp/httpd

[root@kubernetes-controller ~]# kubectl create -f pod-httpd.yaml 
pod "apache-httpd" created

[root@kubernetes-controller ~]#  kubectl get pods -o wide |grep apache-httpd  
apache-httpd                    0/1       ContainerCreating   0          27s       kubernetes-node-3

[root@kubernetes-controller ~]# kubectl get pod apache-httpd -o yaml | grep "podIP"  
  podIP: 172.16.45.5

```

[2] Move to a Node that Pod is running and make sure to work normally.
```
[root@kubernetes-node-3 ~]# curl http://172.16.45.5/
<html><body><h1>It works!</h1></body></html>

[root@kubernetes-node-3 ~]# echo "Kubernetes Persistent Storage && www.itweet.cn" > /tmp/httpd/index.html         

-- enter to a running container,look at volume mapping bit sucess

[root@kubernetes-node-3 ~]# nsenter --target 24207 --mount --uts --ipc --net --pid     
root@apache-httpd:/# 

[root@kubernetes-node-3 ~]# docker inspect -f '{{.State.Pid}}' b92a2432f8d2
24207
[root@kubernetes-node-3 ~]# nsenter --target 24207 --mount --uts --ipc --net --pid     
root@apache-httpd:/# ls /var/www/html/
index.html
root@apache-httpd:/# cat /var/www/html/index.html 
Kubernetes Persistent Storage && www.itweet.cn

-- not found , my self wirte content. because official httpd images "DocumentRoot" configuration is "/usr/local/apache2/htdocs/index.html"  

root@apache-httpd:/usr/local/apache2/conf# cat /usr/local/apache2/htdocs/index.html   
<html><body><h1>It works!</h1></body></html>
root@apache-httpd:/usr/local/apache2/conf# ls /usr/local/apache2/htdocs/index.html  -l
-rw-r--r--. 1 501 staff 45 Jun 11  2007 /usr/local/apache2/htdocs/index.html
```

This is kubernetes persistent storage,Host Machine install Distributed ceph or glusterfs in back-end storage.


原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/
