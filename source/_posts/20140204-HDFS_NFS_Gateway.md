---
title: HDFS_NFS_Gateway
date: 2014-02-04 08:54:31
category: BigData
tags: hdfs
---
1、mount hdfs，关闭 linux自带的几个和 hdfs需要启动冲突的服务
</br>
参考:
</br>
>(1) service nfs stop and service rpcbind stop </br>
>(2) hadoop portmap or hadoop-daemon.sh start portmap

	[hsu@server01 mnt]$ service portmap stop 
	[hsu@server01 mnt]$ sudo service rpcbind stop
	[hsu@server01 mnt]$ sudo hdfs portmap &
	[hsu@server01 mnt]$ jobs 		验证后台运行任务
	[1]+  Running                 sudo hdfs portmap &
	[hsu@server01 mnt]$ ps aux | grep portmap
	root     224585  0.0  0.0 148020  2068 pts/0    S    14:09   0:00 sudo hdfs portmap
	
	[hsu@server01 /]$ ls -la /sbin/mount.* 		查看mount
	-rwxr-xr-x. 1 root root  40592 Apr 17  2012 /sbin/mount.cifs
	-rwxr-xr-x. 1 root root  11616 Nov  3  2011 /sbin/mount.fuse
	-rwsr-xr-x. 1 root root 122880 May 30  2012 /sbin/mount.nfs
 	lrwxrwxrwx. 1 root root      9 Jul  2 18:22 /sbin/mount.nfs4 -> mount.nfs	
	-rwxr-xr-x. 1 root root   1338 Apr  6  2012 /sbin/mount.tmpfs

2、挂在nfs3
       参考：hadoop nfs3  OR   hadoop-daemon.sh start nfs3

	[hsu@server01 mnt]$ sudo -u hdfs hdfs nfs3 & 		后台运行nfs3
	[hsu@server01 mnt]$ jobs 						验证后台任务
	[1]-  Running                 sudo hdfs portmap &
	[2]+  Running                 sudo -u hdfs hdfs nfs3 &
	[hsu@server01 mnt]$ ps aux | grep nfs3
	root     225450  0.0  0.0 148020  2064 pts/0    S    14:14   0:00 sudo -u hdfs hdfs nfs3

3、Execute the following command to verify if all the services are up and running
	
	[hsu@server01 mnt]$ rpcinfo -p server01
	    program vers proto   port  service
	    100005    2   tcp   4242  mountd
	    100000    2   udp    111  portmapper
	    100000    2   tcp    111  portmapper
	    100005    1   tcp   4242  mountd
	    100003    3   tcp   2049  nfs
	    100005    1   udp   4242  mountd
	    100005    3   udp   4242  mountd
	    100005    3   tcp   4242  mountd
	    100005    2   udp   4242  mountd

4、Verify if the HDFS namespace is exported and can be mounted
	
	[hsu@server01 mnt]$ showmount -e server01       
	Export list for server01:
	/ *

5、mount -t nfs -o vers=3,proto=tcp,nolock $server:/  $mount_point

	[hsu@server01 /]$ hdfs -help | egrep 'portmap|nfs3'
	  portmap              run a portmap service
	  nfs3                 run an NFS version 3 gateway
	[hsu@server01 /]$ sudo mount -t nfs -o vers=3,proto=tcp,nolock server01:/ /mnt/hdfs  挂载成功！
	[hsu@server01 /]$ mount | grep hdfs
	server01:/ on /mnt/hdfs type nfs (rw,vers=3,proto=tcp,nolock,addr=135.33.5.53)
	
	问题1：查看文件的时候都会显示：14/12/30 14:23:55 INFO nfs3.IdUserGroup: Can't map group supergroup. Use its string hashcode:-1710818332 
	java.io.IOException: No such group:supergroup。
	
	原因1：nfsServer linux本地没有supergroup这个组？cat /etc/group | grep supergroup
	
	解决1：
		[hsu@server01 /]$ sudo umount /mnt/hdfs    取消挂载
		[hsu@server01 /]$ sudo which groupadd          
		/usr/sbin/groupadd
		[hsu@server01 /]$ sudo /usr/sbin/groupadd supergroup
		[hsu@server01 /]$ sudo cat /etc/group | grep supergroup
		supergroup:x:1005:
		[hsu@server01 /]$ sudo mount -t nfs -o vers=3,proto=tcp,nolock server01:/ /mnt/hdfs 		再次挂载
		14/12/30 15:07:35 INFO mount.RpcProgramMountd: Giving handle (fileId:16385) to client for export /
		14/12/30 15:07:35 WARN oncrpc.RpcProgram: Invalid RPC call program 100227
		14/12/30 15:07:35 INFO nfs3.IdUserGroup: Update cache now
		14/12/30 15:07:35 INFO nfs3.IdUserGroup: Not doing static UID/GID mapping because '/etc/nfs.map' does not exist.
		14/12/30 15:07:35 INFO nfs3.IdUserGroup: Updated user map size: 63
		14/12/30 15:07:35 INFO nfs3.IdUserGroup: Updated group map size: 89
		[hsu@server01 /]$ showmount -e server01
		Export list for server01:
		/ *
		[hsu@server01 /]$ ls /mnt/hdfs/
		hbase  system  tmp  user  zeus
		
6、stop service

	 (1) hadoop-daemon.sh stop nfs3      
	 (2) hadoop-daemon.sh stop portmap


原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/