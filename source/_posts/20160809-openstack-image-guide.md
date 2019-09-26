---
title: openstack image guide 
date: 2016-08-09 18:07:30
category: Cloud
tags: openstack
---
# 介绍
在你拥有虚拟机镜像（也有人叫"虚拟器件"）之前，你的 OpenStack 计算云不太有用，这个指南描述了如何获取，创建以及修改 OpenStack 兼容的虚拟机镜像。

为了简化，有时文档使用 "镜像" 代替 "虚拟机镜像" 。

虚拟机镜像是什么？

一个虚拟机镜像是一个文件，文件内包含了已经安装好可启动操作系统的虚拟磁盘。

虚拟机镜像有不同的格式，下面具体列出。

* Raw
"raw" 镜像格式是最最简单的，并且是被 KVM 和 Xen 原生支持的格式，你可以想象裸格式镜像和块设备文件是二进制位相当的，就好像从块设备拷贝过来的，比方说，使用dd 命令将 /dev/sda 内容拷贝到一个文件。

* qcow2
qcow2 （QEMU 写时复制版本2）格式通常是KVM使用，相比裸格式，它有额外的特性，例如：

使用稀疏文件呈现方式，因此镜像尺寸更小。

支持快照。

因为qcow2 镜像是稀疏的，因此，qcow2镜像通常比裸格式镜像小，更小的文件意味着上传更快，因此通常转换裸格式镜像到qcow2格式上传比直接上传裸格式镜像文件更快。

注意：因为裸格式镜像不支持快照，OpenStack 计算节点在需要的时候将会自动转换裸格式镜像到qcow2格式。

by 原文：http://docs.openstack.org/zh_CN/image-guide/content/ch_introduction.html


# 安装kvm

```
sudo rpm -ivh http://mirrors.ustc.edu.cn/fedora/epel/6/x86_64/epel-release-6-8.noarch.rpm

yum install qemu-kvm qeum-kvm-tools virt-manager libvirt

/etc/init.d/libvirtd start

ifconfig virbr0

brctl show
```

# centos 镜像制作参考
   - http://docs.openstack.org/zh_CN/image-guide/content/virt-install.html
   - http://docs.openstack.org/zh_CN/image-guide/content/centos-image.html#d6e859
   - http://docs.openstack.org/image-guide/content/virt-install.html
   - http://docs.openstack.org/image-guide/content/centos-image.html#d6e859

# 检测kvm是否安装，并且处于可用状态
检查 libvirt 默认网络是否运行,vnc无法远程访问，请排查防火墙是否限制了访问。

在使用 libvirt 启动虚拟机前，检查它的 "default" 默认网络是否启动。虚拟机要连接到外网，它的默认网络必须激活。启动 libvirt 默认网络将创建 linux 网桥( 通常名称是virbr0 )，iptables 规则，以及dhcp服务器进程 dnsmasq 。

检查 "default" 默认网络是否激活，使用 virsh net-list 命令并查看 "default" 网络是否是启用状态。

```
virsh net-list
```

如果网络未激活，输入以下命令：
```
virsh net-start default
```

# 开始制作centos镜像

1.创建一个50g大小容量的qcow2格式的镜像文件

```
qemu-img create -f qcow2 /data/CentOS-6.7-x86_64-RedCloud-160723.qcow2 50G
```

2.这里使用的是centos-6.7的版本，即操作系统未rhel6,其他版本请参考下一条命令查看支持的操作系统版本，如下创建一个kvm类型的虚拟机，指定ram为1024m，磁盘大小为第一步创建的镜像文件。

```
virt-install --virt-type kvm --name CentOS-6.7-x86_64-RedCloud-160723 --ram 1024 \
--cdrom=/data/CentOS-6.7-x86_64-bin-DVD1.iso \
--disk path=/data/CentOS-6.7-x86_64-RedCloud-160723.qcow2,format=qcow2 \
--network network=default \
--graphics vnc,listen=0.0.0.0 --noautoconsole \
--os-type=linux --os-variant=rhel6
```

3.查看kvm支持哪些操作系统版本

```
virt-install --os-variant list
```

4.启动kvm虚拟机，开始安装系统

```
virsh vncdisplay CentOS-6.7-x86_64-RedCloud-160723
```

5.查看虚拟机状态

```
virsh list --all
```

6.使用 virsh 卸载磁盘，libvirt需要挂接一个空磁盘到之前挂接CDROM的地方，设备名应该是 hdc。可以使用 virsh dumpxml vm-image 命令来确认。

```
virsh dumpxml CentOS-6.7-x86_64-RedCloud-160723
```

7.以root用户使用virsh命令，执行下面的步骤完成挂载空磁盘并重启。如果你使用virt-manager安装,下面的命令也起相同作用，你也可以使用图形界面卸载磁盘并手工停止然后启动虚拟机。

```
virsh attach-disk --type cdrom --mode readonly CentOS-6.7-x86_64-RedCloud-160723 "" hdc

virsh destroy CentOS-6.7-x86_64-RedCloud-160723

virsh start CentOS-6.7-x86_64-RedCloud-160723
```

8.登陆到新创建的镜像内,一般通过vnc客户端可以登录,或者宿主机ssd登录，新建的虚拟机内。
   * 8.1 登陆虚拟机执行安装ACPI server，为了让虚拟化层能重启和关闭虚拟机，必须在虚拟机内安装并运行 acpid 服务。
   
```
yum install http://download.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm -y

yum install -y acpid && chkconfig acpid on
```

   * 8.2 在虚拟机操作内容,配置获取metadata,需要使用 cloud-init 获取公钥
   
```
yum install cloud-init -y
```

修改虚拟机配置文件

```
vi /boot/grub/menu.lst 
			default=0
			timeout=5
			serial --unit=0 --speed=115200
			terminal --timeout=1 serial console
			splashimage=(hd0,0)/grub/splash.xpm.gz
			hiddenmenu
			title CentOS 6 (2.6.32-573.el6.x86_64)
			        root (hd0,0)
			        kernel /vmlinuz-2.6.32-573.el6.x86_64 ro root=/dev/mapper/vg_os-lv_root rd_NO_LUKS LANG=en_US.UTF-8 rd_LVM_LV=vg_os/lv_root rd_NO_MD rd_LVM_LV=vg_os/lv_swap console=ttyS0,115200 SYSFONT=latarcyrheb-sun
			16 crashkernel=auto  KEYBOARDTYPE=pc KEYTABLE=us rd_NO_DM rhgb quiet
			        initrd /initramfs-2.6.32-573.el6.x86_64.img
```

cloud-init默认阻止root远程登录并且禁止password认证，只能centos用户通过秘钥登录，通过修改cloud-init配置解决
参考：https://gist.github.com/11xor6/4737097

```
vi /etc/cloud/cloud.cfg
users：
– defaults
   disable_root：0  #default 1
   ssh_pwauth： 1	#default 0

...省略...

```

关闭虚拟机

```
	shutdown -h now
```
  	
9.为最后使用virt-sysprep命令，先安装这个包，清除虚拟机启动生成的一些信息，此命了做虚拟机清理。

清理（删除 MAC 地址相关信息）

操作系统会在/etc/sysconfig/network-scripts/ifcfg-eth0 和 /etc/udev/rules.d/70-persistent-net.rules 这类文件记录下网卡MAC地址，但是，虚拟机的网卡MAC地址在每次虚拟机创建的时候都会不同，因此这些信息必须从配置文件删除掉。

目前有 virt-sysprep 工具可以完成清理虚拟机镜像内的 MAC 地址相关的信息。

```
yum install libguestfs-tools -y

virt-sysprep -d CentOS-6.7-x86_64-RedCloud-160723
```

10.删除 libvirt 虚拟机域

现在你可以上传虚拟机镜像到镜像服务了，不再需要 libvirt 来管理虚拟机镜像，使用 virsh undefine vm-image 命令完成。

```
virsh undefine CentOS-6.7-x86_64-RedCloud-160723
```

11.镜像准备完成

前面你使用 qemu-img create 命令创建的镜像已经准备好可以上传了，例如，你可以上传 CentOS-6.7-x86_64-RedCloud-160723.qcow2 文件到镜像服务。

12.qume import qcow2c
```
 virt-install --connect qemu:///system --ram 1024 -n rhel_64 -r 1024 --os-type=linux --os-variant=rhel6 --disk path=/data/CentOS-6-x86_64-GenericCloud-1604.qcow2c,device=disk,format=qcow2 --vcpus=1 --graphics vnc,listen=0.0.0.0 --noautoconsole --import

[root@bogon data]# virsh list --all
 Id    Name                           State
----------------------------------------------------
 1     rhel_64                        running
```

12. command line by network install
```
＃ 创建虚拟机
qemu-img create -f qcow2 /data/centos-6.8.qcow2 10G

# 通过vnc登录,根据Linux向导完成系统安装,reboot
virt-install --virt-type kvm --name centos-6.8 --ram 2024 \
--cdrom=/data/CentOS-6.8-x86_64-minimal.iso \
--disk path=/data/centos-6.8.qcow2,format=qcow2 \
--network network=default \
--graphics vnc,listen=0.0.0.0 --noautoconsole \
--os-type=linux --os-variant=rhel6  

virsh attach-disk --type cdrom --mode readonly centos-6.8 "" hdc

# 启动虚拟机
virsh start  centos-6.8 

# kvm machine exec

 echo "NOZEROCONF=yes" >> /etc/sysconfig/network

 yum install http://download.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm -y

 yum install -y acpid && chkconfig acpid on

 yum install -y qemu-guest-agent && chkconfig qemu-ga on
 
 yum install -y cloud-init

 yum install -y cloud-utils-growpart
 
 /sbin/shutdown -h now

 virt-sysprep -d centos-6.8 

 virt-sparsify  --tmp /img/ --compress centos-6.8.qcow2  centos-6.8.qcow2c

 virsh destroy  centos-6.8 
 virsh undefine centos-6.8 
```

# 13.guestfish changed image
```
- install kvm tools 
 sudo yum -y install libvirt qemu-kvm libguestfs-tools  # centos 6.x

- centos 6.6
wget http://cloud.centos.org/centos/6.6/images/CentOS-6-x86_64-GenericCloud-1607.qcow2c

- changed image
 guestfish --rw -a  CentOS-6-x86_64-GenericCloud-1607.qcow2c

# set image root password
virt-sysprep --root-password password:123456 -a CentOS-6-x86_64-GenericCloud-1607.qcow2c
```

# FAQ
 最后提醒一下，我安装官网怎么也无法正确让虚拟机获取公钥，可以通过秘钥登录，聪明的你发现博客中细微的差别了吗？哈哈。。。


原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/