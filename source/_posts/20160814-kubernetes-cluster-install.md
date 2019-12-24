---
title: kubernetes-cluster-install
date: 2016-08-14 17:19:40
category: Cloud
tags: kubernates
---
Install Kubernetes which is the Orchestration System for Docker Containers.
For example, Configure Kubernetes Cluster with 1 Admon Node and 3 Container Node like follows.


Centos 7.2 Own  kubernetes yum source,so yum install kubernetes,docker Because of the dependencies,Automatic installation!


```
									192.168.2.120
		                       +---------------------+
		                       | [   Admin Node    ] |
		                       |kubernetes-controller|
		                       |                     |
		                       +----------+----------+
                                  	      |
+----------------------+                  |          	     +----------------------+  
| [ kubernetes-node-1] | 192.168.2.121    |   192.168.2.122  |[ kubernetes-node-2 ] |
|        node-1        +------------------+------------------+         node-2       |
|                      |                  |  		         |                      |
+----------------------+                  |   		         +----------------------+
										  |
							   +----------+-----------+  
							   | [ kubernetes-node-3] |
							   |        node-3        |
							   |                      |
							   +----------------------+ 
							   	    192.168.2.123
```

# Init all machine
[1] Master Node
```
sudo systemctl stop firewalld && sudo systemctl disable firewalld
sudo yum install -y ntp.x86_64
```

[2] all slave Node 
```
sudo systemctl stop firewalld && sudo systemctl disable firewalld
sudo yum install -y ntp.x86_64
```

# Configure Admon Node on this section.

[1]	Install required packages.

```
[root@kubernetes-controller ~]# yum -y install kubernetes etcd flannel
```

[2]	Configure Kubernetes.
```
# generate RSA key
[root@kubernetes-controller ~]# openssl genrsa -out /etc/kubernetes/service.key 2048

[root@kubernetes-controller ~]#  vi /etc/kubernetes/controller-manager
# line 7: add
KUBE_CONTROLLER_MANAGER_ARGS="--service_account_private_key_file=/etc/kubernetes/service.key"


[root@kubernetes-controller ~]# vi /etc/kubernetes/apiserver

#line 8:change
KUBE_API_ADDRESS="--address=0.0.0.0"

# line 17: change to Admin Node's hostname or IP address
KUBE_ETCD_SERVERS="--etcd-servers=http://kubernetes-controller:2379"

# line 20: IP range for Kubernetes service (change it if need)
KUBE_SERVICE_ADDRESSES="--service-cluster-ip-range=10.254.0.0/16"

# line 26: add
KUBE_API_ARGS="--service_account_key_file=/etc/kubernetes/service.key"


[root@kubernetes-controller ~]# vi /etc/etcd/etcd.conf

# line 8: uncomment
ETCD_LISTEN_PEER_URLS="http://localhost:2380"

# line 9: add etcd Host's hostname or IP address
ETCD_LISTEN_CLIENT_URLS="http://kubernetes-controller:2379,http://localhost:2379"


[root@kubernetes-controller ~]#  vi /etc/kubernetes/config

# line 22: change to Admin Node's hostname or IP address
KUBE_MASTER="--master=http://kubernetes-controller:8080"


[root@kubernetes-controller ~]# systemctl start etcd kube-apiserver kube-controller-manager kube-scheduler ntpd
[root@kubernetes-controller ~]# systemctl enable etcd kube-apiserver kube-controller-manager kube-scheduler ntpd
```

[3]	Configure Flannel networking.
```
# create new file
# specify network range you like which is used inside Container Nodes
[root@kubernetes-controller ~]# vi flannel-config.json
 {
  "Network":"172.16.0.0/16",
  "SubnetLen":24,
  "Backend":{
    "Type":"vxlan",
    "VNI":1
  }
}


[root@kubernetes-controller ~]# vi /etc/sysconfig/flanneld

# line 4: change to Flannel Host's hostname or IP address
FLANNEL_ETCD="http://kubernetes-controller:2379"

# line 8: confirm the parameter
FLANNEL_ETCD_KEY="/atomic.io/network"


[root@kubernetes-controller ~]# etcdctl set atomic.io/network/config < flannel-config.json 
[root@kubernetes-controller ~]# etcdctl get atomic.io/network/config
 {
  "Network":"172.16.0.0/16",
  "SubnetLen":24,
  "Backend":{
    "Type":"vxlan",
    "VNI":1
  }
}

[root@kubernetes-controller ~]# systemctl start flanneld ntpd
[root@kubernetes-controller ~]# systemctl enable flanneld  ntpd
```

[4]	Make sure th settings. It's OK if following result is displayed.
```
[root@kubernetes-controller ~]# kubectl cluster-info 
Kubernetes master is running at http://localhost:8080
```

# Configure Container Node on this section.

[1]	[Install and Start Docker service on All Nodes, refer to here.](https://www.itweet.cn/2016/08/13/docker-install/)


[2]	Install Kubernetes and Flannel on All Nodes.
```
[root@kubernetes-node-1 ~]# yum -y install kubernetes flannel

```

[3]	Configure Kubernetes on all Nodes like follows.
```
[root@kubernetes-node-1 ~]# vi /etc/kubernetes/config
# line 22: change to Admin Node's hostname or IP address
KUBE_MASTER="--master=http://kubernetes-controller:8080"

[root@kubernetes-node-1 ~]# vi /etc/kubernetes/kubelet
# line 5: change
KUBELET_ADDRESS="--address=0.0.0.0"

# line 11: change to own hostname
KUBELET_HOSTNAME="--hostname-override=kubernetes-node-1"

# line 14: change to Admin Node's hostname or IP address
KUBELET_API_SERVER="--api-servers=http://kubernetes-controller:8080"


[root@kubernetes-node-1 ~]# vi /etc/sysconfig/flanneld
# line 4: change to Admin Node's hostname or IP address
FLANNEL_ETCD="http://kubernetes-controller:2379"


# stop docker0 interface
[root@kubernetes-node-1 ~]# nmcli c down docker0 
Connection 'docker0' successfully deactivated (D-Bus active path: /org/freedesktop/NetworkManager/ActiveConnection/1)

[root@kubernetes-node-1 ~]# systemctl start flanneld kube-proxy kubelet ntpd
[root@kubernetes-node-1 ~]# systemctl enable flanneld kube-proxy kubelet ntpd
[root@kubernetes-node-1 ~]# systemctl restart docker 

```

* node-1 node add kubernetes get nodes status

```
[root@kubernetes-controller ~]# kubectl get nodes 
NAME                STATUS    AGE
kubernetes-node-1   Ready     1m
```

* 2 nodes add kubernetes get node status

```
[root@kubernetes-controller ~]# kubectl get nodes 
NAME                STATUS    AGE
kubernetes-node-1   Ready     8m
kubernetes-node-2   Ready     1m
```

[4]	Make sure th settings. It's OK if the status of each node is Ready like follows.
```
[root@kubernetes-controller ~]#  kubectl get nodes
NAME                STATUS    AGE
kubernetes-node-1   Ready     37m
kubernetes-node-2   Ready     30m
kubernetes-node-3   Ready     22m
```


[5] 时间不同步会导致如下问题,同步主节点时间，重启服务即可解决：
```
[root@kubernetes-controller ~]# kubectl get nodes
NAME                STATUS     AGE
kubernetes-node-1   Ready      5h
kubernetes-node-2   NotReady   5h
kubernetes-node-3   NotReady   5h
```
时间一致性对于分布式应用程序来说，至关重要，稍有不慎导致，整个集群不可用，我就遇到很奇葩的问题，基础镜像源无法下载，待我同步所有节点时间重启所有服务之后居然，下载下来了。真奇怪，得多看看代码实现吧！不然就是一个黑盒子！难看透！后续章节创建pods就遇到时间不同步导致的问题！

