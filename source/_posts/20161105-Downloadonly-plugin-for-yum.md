---
title: Downloadonly plugin for yum
date: 2016-11-05 16:55:41
category: BigData
tags: Downloadonly
---
There are two ways to download a package without installing it.

One is using the "downloadonly" plugin for yum, the other is using "yumdownloader" utility.


# Downloadonly plugin for yum

1. Install the package including "downloadonly" plugin:

```
	(RHEL5)
	# yum install yum-downloadonly

	(RHEL6)
	# yum install yum-plugin-downloadonly
```

2. Run yum command with "--downloadonly" option as follows:

```
	# yum install --downloadonly --downloaddir=<directory> <package>
```

3. Confirm the RPM files are available in the specified download directory.

Note:
    * Before using the plugin, check /etc/yum/pluginconf.d/downloadonly.conf to confirm that this plugin is "enabled=1"
    * This is applicable for "yum install/yum update" and not for "yum groupinstall". Use "yum groupinfo" to identify packages within a specific group.
    * If only the package name is specified, the latest available package is downloaded (such as sshd). Otherwise, you can specify the full package name and version (such as httpd-2.2.3-22.el5).
    * If you do not use the --downloaddir option, files are saved by default in /var/cache/yum/ in rhel-{arch}-channel/packages
    * If desired, you can download multiple packages on the same command.
    * You still need to re-download the repodata if the repodata expires before you re-use the cache. By default it takes two hours to expire.

# Yumdownloader
If downloading a installed package, "yumdownloader" is useful.

1. Install the yum-utils package:
```
# yum install yum-utils
```

2. Run the command followed by the desired package:
```
# yumdownloader <package>
```

Note:
    * The package is saved in the current working directly by default; use the --destdir option to specify an alternate location.
    * Be sure to add --resolve if you need to download dependencies.

# Example by Centos 6.8
```
# cat /etc/redhat-release 
CentOS release 6.8 (Final)

yumdownloader --resolve --destdir=/root/mysql-server mysql-server

yumdownloader --resolve --destdir=/root/owncloud owncloud

/etc/init.d/iptables stop
chkconfig iptables off

rpm -ivh *.rpm   

/etc/init.d/httpd start

netstat -lntop |grep 80

chkconfig httpd on
chkconfig mysqld on
```

