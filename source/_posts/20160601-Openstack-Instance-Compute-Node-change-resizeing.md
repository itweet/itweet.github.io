---
title: Openstack Instance Compute Node change resizeing
date: 2016-06-01 18:08:34
category: Cloud
tags: openstack
---
Resize a Running Instance on a Single Compute Node
One can resize a running instance in OpenStack by running the following nova command:
nova resize --poll 
The default behavior of this command is to invoke the nova scheduler to determine the best compute node for the resized instance. If there is only one compute node in the environment, the resize will fail.
We need to tell nova to allow resizing on the same host by modifying /etc/nova/nova.conf .
Modify /etc/nova/nova.conf
allow_resize_to_same_host=True
scheduler_default_filters=AllHostsFilter
By changing the default nova scheduler filter to AllHostsFilter , all compute hosts will be available and unfiltered. It is not a good idea to keep this setting in a multi-compute environment.
Restart Services
After making the changes to nova.conf, restart scheduler and compute services:
service nova-scheduler restart
service nova-compute restart
Resize Confirm
After resizing the instance, the status will change to VERIFY_RESIZE . One will see two copies of the instance in /var/lib/nova/instances : the original and the resized. Run the following command to verify the resize and delete the original instance:
nova resize-confirm

# Form example
## all node
```
vim /etc/nova/nova.conf
 allow_resize_to_same_host=True
 scheduler_default_filters=RetryFilter,AvailabilityZoneFilter,RamFilter,DiskFilte
r,ComputeFilter,ComputeCapabilitiesFilter,ImagePropertiesFilter,ServerGroupAntiA
ffinityFilter,ServerGroupAffinityFilter
```

## contollor node
```
systemctl restart openstack-nova-api.service  
systemctl restart openstack-nova-conductor.service    
systemctl restart openstack-nova-scheduler.service 
systemctl restart openstack-nova-cert.service         
systemctl restart openstack-nova-consoleauth.service  
systemctl restart openstack-nova-compute.service      
systemctl restart openstack-nova-novncproxy.service 

openstack-status 
```

## compute node
```
systemctl restart openstack-nova-compute.service

openstack-status 
```


原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/