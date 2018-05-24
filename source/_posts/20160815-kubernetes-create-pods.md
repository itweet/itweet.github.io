---
title: kubernetes-create-pods
date: 2016-08-15 17:18:09
category: Cloud
tags: kubernates
---
根据前一篇文章，安装好kubernetes集群，集群正常在运行，下面开始创建pods吧！

你可以选择，从github下载kubernetes源码，切换到kubernetes/examples/guestbook参考[官网文档](https://github.com/kubernetes/kubernetes/tree/master/examples/guestbook)搭建一个完整的应用来验证集群的基本功能。

```
[root@kubernetes-controller ~]#  kubectl get nodes
NAME                STATUS    AGE
kubernetes-node-1   Ready     37m
kubernetes-node-2   Ready     30m
kubernetes-node-3   Ready     22m
```

创建Namespace：kube-system
```
[root@kubernetes-controller ~]# vi namespace.yaml 
apiVersion: v1
kind: Namespace
metadata:
  name: kube-system

[root@kubernetes-controller ~]# kubectl get namespace
NAME      STATUS    AGE
default   Active    5h

[root@kubernetes-controller ~]# kubectl create -f namespace.yaml
namespace "kube-system" created

[root@kubernetes-controller ~]# kubectl get namespace           
NAME          STATUS    AGE
default       Active    5h
kube-system   Active    3s
```

启动一个nginx
 新建一个pod-nginx.yaml文件，用于描述 pod.
```
[root@kubernetes-controller ~]#  kubectl api-versions
autoscaling/v1
batch/v1
extensions/v1beta1
v1

[root@kubernetes-controller ~]# vi pod-nginx.yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
  - name: nginx
    image: nginx
    ports:
    - containerPort: 80
```

然后启动这个pod，检查状态
```
# create Pod
[root@kubernetes-controller ~]# kubectl create -f pod-nginx.yaml
pod "nginx" created

[root@kubernetes-controller ~]# kubectl get pods --all-namespaces
NAMESPACE   NAME      READY     STATUS              RESTARTS   AGE
default     nginx     0/1       ContainerCreating   0          15s

[root@kubernetes-controller ~]# kubectl describe pods nginx
```

可以看到，这个nginx-pod被调度到kubernetes-node3启动。
```
[root@kubernetes-controller ~]# kubectl describe pods nginx|tail -5
  FirstSeen     LastSeen        Count   From                    SubobjectPath   Type            Reason          Message
  ---------     --------        -----   ----                    -------------   --------        ------          -------
  2m            2m              1       {default-scheduler }                    Normal          Scheduled       Successfully assigned nginx to kubernetes-node-3

[root@kubernetes-controller ~]# kubectl get pods
NAME      READY     STATUS              RESTARTS   AGE
nginx     0/1       ContainerCreating   0          11m
```

接下来我们可以去kubernetes-node-3节点，看看是否有对应的镜像被拉取并启动,发现没用镜像也没有启动容器，额，再次检查发现，连接超时，国内网络环境，不得不说一句fuck！到那个节点search一下。等待好久都没结果，我们去配置文件找找为啥会有这样一个容器被pull！
```
 <invalid>     <invalid>       1       {kubelet kubernetes-node-3}                     Warning         FailedSync      Error syncing pod, skipping: failed to "StartContainer" for "POD" with ErrImagePull: "image pull failed for registry.access.redhat.com/rhel7/pod-infrastructure:latest, this may be because there are no credentials on this request.  details: (unable to ping registry endpoint https://registry.access.redhat.com/v0/\nv2 ping attempt failed with error: https://registry.access.redhat.com/v2/ does not appear to be a v2 registry endpoint\n v1 ping attempt failed with error: Get https://registry.access.redhat.com/v1/_ping: read tcp 192.168.2.123:42613->209.132.182.63:443: read: connection timed out)"

日志：
No such image: registry.access.redhat.com/rhel7/pod-infrastructure:latest"

[root@kubernetes-node-3 ~]# docker search registry.access.redhat.com/rhel7/pod-infrastructure:latest
```

在kubernetes-node的节点上都会有这样的一个基础镜像，`registry.access.redhat.com/rhel7/pod-infrastructure:latest`这个镜像是Pod 启动时的一个基础容器，你可以通过dokcer ps -a命令看到这个容器，类似windows系统服务,供kubenetes内部使用。pods无法运行，好可恶，只能提前下载下来导入进去啦！docker.io没用提供，google源又被封，只能考虑其他方式了！发现时间不同步，待我同步所有节点时间后，居然镜像就自己下载下来了。会自动run起这个容器。
http://kubernetes.io/docs/user-guide/images/

```
[root@kubernetes-node-2 kubernetes]# cat /etc/kubernetes/kubelet |grep KUBELET_POD_INFRA_CONTAINER
KUBELET_POD_INFRA_CONTAINER="--pod-infra-container-image=registry.access.redhat.com/rhel7/pod-infrastructure:latest"

[root@kubernetes-node-3 ~]# docker images
REPOSITORY                                            TAG                 IMAGE ID            CREATED             SIZE
registry.access.redhat.com/rhel7/pod-infrastructure   latest              ee020ceeef01        3 months ago        215.4 MB

[root@kubernetes-node-3 ~]# docker ps -a
CONTAINER ID        IMAGE                                                        COMMAND             CREATED             STATUS              PORTS               NAMES
3c00d5e7d1e9        registry.access.redhat.com/rhel7/pod-infrastructure:latest   "/pod"              7 minutes ago       Up 7 minutes                            k8s_POD.c36b0a77_nginx_default_e7bd8714-616f-11e6-a406-000c2980ea46_b03d011b

＃主节点,查看pod状态，正在pull nginx镜像！
[root@kubernetes-controller ~]# kubectl describe pods nginx|tail -6
  ---------     --------        -----   ----                            -------------           --------        ------                  -------
  8m            8m              1       {kubelet kubernetes-node-3}                             Warning         MissingClusterDNS       kubelet does not have ClusterDNS IP configured and cannot create Pod using "ClusterFirst" policy. Falling back to DNSDefault policy.
  8m            8m              1       {default-scheduler }                                    Normal          Scheduled               Successfully assigned nginx to kubernetes-node-3
  8m            8m              1       {kubelet kubernetes-node-3}     spec.containers{nginx}  Normal          Pulling                 pulling image "nginx"
```

经过我多次重试，终于把nginx下载下来了。
```
[root@kubernetes-node-3 ~]# docker pull nginx
Using default tag: latest
Trying to pull repository docker.io/library/nginx ... 
latest: Pulling from docker.io/library/nginx
51f5c6a04d83: Already exists 
a3ed95caeb02: Pulling fs layer 
51d229e136d0: Pull complete 
bcd41daec8cc: Pull complete 
Digest: sha256:0fe6413f3e30fcc5920bc8fa769280975b10b1c26721de956e1428b9e2f29d04
Status: Image is up to date for docker.io/nginx:latest

[root@kubernetes-node-3 ~]#  docker images
REPOSITORY                                            TAG                 IMAGE ID            CREATED             SIZE
docker.io/nginx                                       latest              0d409d33b27e        10 weeks ago        182.7 MB
registry.access.redhat.com/rhel7/pod-infrastructure   latest              ee020ceeef01        3 months ago        215.4 MB

[root@kubernetes-node-3 ~]# docker ps -a     
CONTAINER ID        IMAGE                                                        COMMAND                  CREATED             STATUS              PORTS               NAMES
2f2de065fd05        nginx                                                        "nginx -g 'daemon off"   21 seconds ago      Up 20 seconds                           k8s_nginx.fa5127aa_nginx_default_e7bd8714-616f-11e6-a406-000c2980ea46_f5a8b2ec
3c00d5e7d1e9        registry.access.redhat.com/rhel7/pod-infrastructure:latest   "/pod"                   53 minutes ago      Up 53 minutes                           k8s_POD.c36b0a77_nginx_default_e7bd8714-616f-11e6-a406-000c2980ea46_b03d011b
```
如上最后一条命了执行完成，可以看到up了两个容器，一个是pod系统基础容器，另一个是我创建的容器！

主节点查看pod状态,pod从创建经历了几个过程：Scheduled－>Pulling->Pulled->Created->Started
```
[root@kubernetes-controller ~]#  kubectl describe pod|tail -8
  58m           58m             1       {default-scheduler }                                    Normal          Scheduled               Successfully assigned nginx to kubernetes-node-3
  58m           58m             1       {kubelet kubernetes-node-3}     spec.containers{nginx}  Normal          Pulling                 pulling image "nginx"
  58m           5m              2       {kubelet kubernetes-node-3}                             Warning         MissingClusterDNS       kubelet does not have ClusterDNS IP configured and cannot create Pod using "ClusterFirst" policy. Falling back to DNSDefault policy.
  5m            5m              1       {kubelet kubernetes-node-3}     spec.containers{nginx}  Normal          Pulled                  Successfully pulled image "nginx"
  5m            5m              1       {kubelet kubernetes-node-3}     spec.containers{nginx}  Normal          Created                 Created container with docker id 2f2de065fd05
  5m            5m              1       {kubelet kubernetes-node-3}     spec.containers{nginx}  Normal          Started                 Started container with docker id 2f2de065fd05
```

查看pod日志内容,这个容器木有日志可看
```
[root@kubernetes-controller ~]# kubectl logs --tail=10 nginx  

[root@kubernetes-controller ~]# kubectl logs -f nginx

[root@kubernetes-node-3 ~]#  docker logs 2f2de065fd05
```

进入容器验证nginx,挺智能的，我进入容器失败,容器不支持，卡住,容器自动退出，docker ps -a里面立马启动一个新nginx容器。
```
[root@kubernetes-controller ~]# kubectl get pods
NAME      READY     STATUS    RESTARTS   AGE
nginx     1/1       Running   0          1h

[root@kubernetes-node-3 ~]#  docker inspect 3c00d5e7d1e9|grep IPAddress
            "SecondaryIPAddresses": null,
            "IPAddress": "172.16.60.2",
                    "IPAddress": "172.16.60.2",

[root@kubernetes-node-3 ~]# yum install util-linux

[root@kubernetes-node-3 ~]# docker inspect -f '{{.State.Pid}}' d1ea6b36b77e
24765

[root@kubernetes-node-3 ~]# nsenter --target 24765 --mount --uts --ipc --net --pid
-bash: warning: setlocale: LC_ALL: cannot change locale (en_US.utf-8)
root@nginx:/# ps aux
USER        PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root          1  0.0  0.0  31680  2868 ?        Ss   17:28   0:00 nginx: master process nginx -g daemon off;
nginx        10  0.0  0.0  32072  1692 ?        S    17:28   0:00 nginx: worker process
root         11  0.1  0.0  20288  1912 ?        S    17:49   0:00 -bash
root         15  0.0  0.0  17492  1164 ?        R+   17:49   0:00 ps aux
root@nginx:/# ps -ef|grep nginx
root          1      0  0 17:28 ?        00:00:00 nginx: master process nginx -g daemon off;
nginx        10      1  0 17:28 ?        00:00:00 nginx: worker process
root         17     11  0 17:50 ?        00:00:00 grep nginx

root@nginx:/# cat /etc/hosts|tail -1
172.16.60.2     nginx

root@nginx:/# ip addr           
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default 
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
5: eth0@if6: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue state UP group default 
    link/ether 02:42:ac:10:3c:02 brd ff:ff:ff:ff:ff:ff
    inet 172.16.60.2/24 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::42:acff:fe10:3c02/64 scope link 
       valid_lft forever preferred_lft forever

root@nginx:/# exit
logout

退出不会影响容器状态
[root@kubernetes-node-3 ~]# docker ps -l
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
d1ea6b36b77e        nginx               "nginx -g 'daemon off"   24 minutes ago      Up 24 minutes                           k8s_nginx.fa5127aa_nginx_default_e7bd8714-616f-11e6-a406-000c2980ea46_831516c2

# show Pods list
[root@kubernetes-controller ~]# kubectl get pods -o wide 
NAME      READY     STATUS    RESTARTS   AGE       NODE
nginx     1/1       Running   1          1h        kubernetes-node-3

# display assigned IP address on the Pod
[root@kubernetes-controller ~]# kubectl get pods nginx -o yaml | grep "podIP"  
  podIP: 172.16.60.2

# access to the Pod
[root@kubernetes-controller ~]# curl http://172.16.60.2/
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```

kubernetes-dashboard 下载被墙，只能找个hosts映射下,如下：
```
[root@kubernetes-controller ~]# tail -2 /etc/hosts
220.255.2.153   www.gcr.io
220.255.2.153   gcr.io
```

时速云，国内镜像站，挺不错，不过这里我没有采用 - https://hub.tenxcloud.com/search?q=kubernetes-dashboard&source=tenxcloud

# kubernetes-dashboard UI pods service
```
[root@kubernetes-controller ~]# wget https://rawgit.com/kubernetes/dashboard/master/src/deploy/kubernetes-dashboard.yaml

[root@kubernetes-controller ~]# vi kubernetes-dashboard.yaml 
#change 48 line
args:
- --apiserver-host=http://192.168.2.120:8080

[root@kubernetes-controller ~]# kubectl create -f kubernetes-dashboard.yaml
deployment "kubernetes-dashboard" created
You have exposed your service on an external port on all nodes in your
cluster.  If you want to expose this service to the external internet, you may
need to set up firewall rules for the service port(s) (tcp:32763) to serve traffic.

See http://releases.k8s.io/release-1.2/docs/user-guide/services-firewalls.md for more details.
service "kubernetes-dashboard" created

[root@kubernetes-controller ~]# kubectl get pods --namespace=kube-system
NAME                                   READY     STATUS              RESTARTS   AGE
kubernetes-dashboard-564869829-9ipet   0/1       ContainerCreating   0          11m

[root@kubernetes-controller ~]# kubectl get pods --namespace=default
NAME      READY     STATUS    RESTARTS   AGE
nginx     1/1       Running   0          40m

-- 调度到第一个node上面启动UI
[root@kubernetes-controller ~]# kubectl describe pods --namespace=kube-system|tail -3
  13m           13m             1       {default-scheduler }                    Normal          Scheduled       Successfully assigned kubernetes-dashboard-564869829-9ipet to kubernetes-node-1

[root@kubernetes-controller ~]# kubectl get svc --namespace=kube-system
NAME                   CLUSTER-IP       EXTERNAL-IP   PORT(S)   AGE
kubernetes-dashboard   10.254.247.205   nodes         80/TCP    29m

# ui启动报错，猜测是yaml缩近问题！修改yaml重新提交！
[root@kubernetes-node-1 ~]# docker logs 34d4de854cb7
Starting HTTP server on port 9090
Creating API server client for http://kubernetes-controller:8080
Error while initializing connection to Kubernetes apiserver. This most likely means that the cluster is misconfigured (e.g., it has invalid apiserver certificates or service accounts configuration) or the --apiserver-host param points to a server that does not exist. Reason: Get http://kubernetes-controller:8080/version: dial tcp: lookup kubernetes-controller on 114.114.114.114:53: no such host


[root@kubernetes-controller ~]# kubectl get po --namespace=kube-system
NAME                                   READY     STATUS             RESTARTS   AGE
kubernetes-dashboard-564869829-9ipet   0/1       CrashLoopBackOff   13         1h

[root@kubernetes-controller ~]# kubectl --namespace=kube-system get ep kubernetes-dashboard
NAME                   ENDPOINTS   AGE
kubernetes-dashboard               1h

#删除kubernetes-dashboard services,然后重建
[root@kubernetes-controller ~]# kubectl --namespace=kube-system delete deployments kubernetes-dashboard
deployment "kubernetes-dashboard" deleted
[root@kubernetes-controller ~]# kubectl --namespace=kube-system delete services kubernetes-dashboard   
service "kubernetes-dashboard" deleted

[root@kubernetes-controller ~]# kubectl --namespace=kube-system get ep kubernetes-dashboard            
Error from server: endpoints "kubernetes-dashboard" not found
[root@kubernetes-controller ~]# kubectl get po --namespace=kube-system  

[root@kubernetes-controller ~]# kubectl create -f kubernetes-dashboard.yaml

# 查看那个节点启动的kubernetes-dashboard 服务
[root@kubernetes-controller ~]# kubectl describe pods --namespace=kube-system 

#节点3调度起来了，就是yaml缩近问题
[root@kubernetes-node-3 ~]#  docker ps -a
CONTAINER ID        IMAGE                                                        COMMAND                  CREATED              STATUS              PORTS               NAMES
653605a9be93        gcr.io/google_containers/kubernetes-dashboard-amd64:v1.1.1   "/dashboard --port=90"   About a minute ago   Up About a minute                       k8s_kubernetes-dashboard.9b6ddaae_kubernetes-dashboard-1221276838-zh52d_kube-system_926ac1f1-61da-11e6-a406-000c2980ea46_11d0d1fc
d9efdc702581        registry.access.redhat.com/rhel7/pod-infrastructure:latest   "/pod"                   About a minute ago   Up About a minute                       k8s_POD.42430ae1_kubernetes-dashboard-1221276838-zh52d_kube-system_926ac1f1-61da-11e6-a406-000c2980ea46_c69022c9

[root@kubernetes-controller ~]# kubectl get svc --namespace=kube-system
NAME                   CLUSTER-IP       EXTERNAL-IP   PORT(S)   AGE
kubernetes-dashboard   10.254.217.183   nodes         80/TCP    4m

[root@kubernetes-controller ~]# kubectl get svc  --namespace=kube-system -o wide
NAME                   CLUSTER-IP       EXTERNAL-IP   PORT(S)   AGE       SELECTOR
kubernetes-dashboard   10.254.217.183   nodes         80/TCP    1h        app=kubernetes-dashboard
```
最后通过http://192.168.2.120:8080/ui  即可访问kubernetes-dashboard

# 验证kubernetes集群基本功能

快速启动,一键部署kubernetes 提供的guestbook,redis services example.

```
$ git clone https://github.com/kubernetes/kubernetes.git

$ cd kubernetes

$ kubectl create -f examples/guestbook/all-in-one/guestbook-all-in-one.yaml
service "redis-master" created
deployment "redis-master" created
service "redis-slave" created
deployment "redis-slave" created
service "frontend" created
deployment "frontend" created
```

列表所有的kubernetes services
```
[root@kubernetes-controller kubernetes]# kubectl get services
NAME           CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
frontend       10.254.210.70    <none>        80/TCP     1m
kubernetes     10.254.0.1       <none>        443/TCP    2h
redis-master   10.254.177.239   <none>        6379/TCP   1m
redis-slave    10.254.234.101   <none>        6379/TCP   1m

[root@kubernetes-controller ~]#  kubectl get pods
NAME                            READY     STATUS    RESTARTS   AGE
frontend-440143558-0iiy1        1/1       Running   0          8m
frontend-440143558-u5uja        1/1       Running   0          8m
frontend-440143558-xtlh3        1/1       Running   0          8m
nginx                           1/1       Running   0          1h
redis-master-2353460263-fqdoc   1/1       Running   0          8m
redis-slave-1691881626-fs9m6    1/1       Running   0          8m
redis-slave-1691881626-xex67    1/1       Running   0          8m

[root@kubernetes-controller ~]# curl http://172.16.49.3/
<html ng-app="redis">
  <head>
    <title>Guestbook</title>
    <link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.2.12/angular.min.js"></script>
    <script src="controllers.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/angular-ui-bootstrap/0.13.0/ui-bootstrap-tpls.js"></script>
  </head>
  <body ng-controller="RedisCtrl">
    <div style="width: 50%; margin-left: 20px">
      <h2>Guestbook</h2>
    <form>
    <fieldset>
    <input ng-model="msg" placeholder="Messages" class="form-control" type="text" name="input"><br>
    <button type="button" class="btn btn-primary" ng-click="controller.onRedis()">Submit</button>
    </fieldset>
    </form>
    <div>
      <div ng-repeat="msg in messages track by $index">
        {{msg}}
      </div>
    </div>
    </div>
  </body>
</html>

[root@kubernetes-controller ~]# kubectl describe pods redis-master-2353460263-fqdoc

[root@kubernetes-controller ~]#  kubectl logs redis-master-2353460263-fqdoc
                _._                                                  
           _.-``__ ''-._                                             
      _.-``    `.  `_.  ''-._           Redis 2.8.19 (00000000/0) 64 bit
  .-`` .-```.  ```\/    _.,_ ''-._                                   
 (    '      ,       .-`  | `,    )     Running in stand alone mode
 |`-._`-...-` __...-.``-._|'` _.-'|     Port: 6379
 |    `-._   `._    /     _.-'    |     PID: 1
  `-._    `-._  `-./  _.-'    _.-'                                   
 |`-._`-._    `-.__.-'    _.-'_.-'|                                  
 |    `-._`-._        _.-'_.-'    |           http://redis.io        
  `-._    `-._`-.__.-'_.-'    _.-'                                   
 |`-._`-._    `-.__.-'    _.-'_.-'|                                  
 |    `-._`-._        _.-'_.-'    |                                  
  `-._    `-._`-.__.-'_.-'    _.-'                                   
      `-._    `-.__.-'    _.-'                                       
          `-._        _.-'                                           
              `-.__.-'                  

[1] 17 Aug 10:40:38.156 # Server started, Redis version 2.8.19
[1] 17 Aug 10:40:38.157 # WARNING you have Transparent Huge Pages (THP) support enabled in your kernel. This will create latency and memory usage issues with Redis. To fix this issue run the command 'echo never > /sys/kernel/mm/transparent_hugepage/enabled' as root, and add it to your /etc/rc.local in order to retain the setting after a reboot. Redis must be restarted after THP is disabled.
[1] 17 Aug 10:40:38.157 # WARNING: The TCP backlog setting of 511 cannot be enforced because /proc/sys/net/core/somaxconn is set to the lower value of 128.
[1] 17 Aug 10:40:38.157 * The server is now ready to accept connections on port 6379


[root@kubernetes-controller ~]# kubectl get services
NAME           CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
frontend       10.254.210.70    <none>        80/TCP     15h
kubernetes     10.254.0.1       <none>        443/TCP    18h
redis-master   10.254.177.239   <none>        6379/TCP   15h
redis-slave    10.254.234.101   <none>        6379/TCP   15h

[root@kubernetes-controller ~]# kubectl get deployments
NAME           DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
frontend       3         3         3            3           15h
redis-master   1         1         1            1           15h
redis-slave    2         2         2            2           15h

[root@kubernetes-controller ~]# kubectl get pods
NAME                            READY     STATUS    RESTARTS   AGE
frontend-440143558-0iiy1        1/1       Running   0          15h
frontend-440143558-u5uja        1/1       Running   0          15h
frontend-440143558-xtlh3        1/1       Running   0          15h
nginx                           1/1       Running   0          17h
redis-master-2353460263-fqdoc   1/1       Running   0          15h
redis-slave-1691881626-fs9m6    1/1       Running   0          15h
redis-slave-1691881626-xex67    1/1       Running   0          15h

[root@kubernetes-controller ~]# kubectl get pods -L tier
NAME                            READY     STATUS    RESTARTS   AGE       TIER
frontend-440143558-0iiy1        1/1       Running   0          15h       frontend
frontend-440143558-u5uja        1/1       Running   0          15h       frontend
frontend-440143558-xtlh3        1/1       Running   0          15h       frontend
nginx                           1/1       Running   0          17h       <none>
redis-master-2353460263-fqdoc   1/1       Running   0          15h       backend
redis-slave-1691881626-fs9m6    1/1       Running   0          15h       backend
redis-slave-1691881626-xex67    1/1       Running   0          15h       backend
```

清理redis相关服务
```
[root@kubernetes-controller ~]#  kubectl get pods -o wide 
NAME                            READY     STATUS    RESTARTS   AGE       NODE
apache-httpd                    1/1       Running   0          41m       kubernetes-node-3
frontend-440143558-0iiy1        1/1       Running   0          4d        kubernetes-node-1
frontend-440143558-u5uja        1/1       Running   1          4d        kubernetes-node-3
frontend-440143558-xtlh3        1/1       Running   1          4d        kubernetes-node-2
nginx                           1/1       Running   0          4d        kubernetes-node-3
redis-master-2353460263-fqdoc   1/1       Running   0          4d        kubernetes-node-2
redis-slave-1691881626-fs9m6    1/1       Running   1          4d        kubernetes-node-3
redis-slave-1691881626-xex67    1/1       Running   0          4d        kubernetes-node-1

[root@kubernetes-controller ~]# kubectl delete deployments,services -l "app in (redis, guestbook)"
deployment "frontend" deleted
deployment "redis-master" deleted
deployment "redis-slave" deleted
service "frontend" deleted
service "redis-master" deleted
service "redis-slave" deleted

[root@kubernetes-controller ~]#  kubectl get pods -o wide 
NAME           READY     STATUS    RESTARTS   AGE       NODE
apache-httpd   1/1       Running   0          42m       kubernetes-node-3
nginx          1/1       Running   0          4d        kubernetes-node-3

```


原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/