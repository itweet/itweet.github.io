---
title: Apache-Cassandra-Cluster
date: 2015-09-21 09:16:20
category: BigData
tags: cassandra
---
# 简介：
Cassandra 是一个分布式的存储引擎，用来管理分布在大量普通商用级别服务器上面的海量的结构化数据，可以提供高可用性，不存在单点故障。Cassandra设计目标，是运行在千台规模的服务器节点上面，节点可以跨越IDC.在这个规模上，大小组件都会频繁的发生故障。当故障发生时，Cassandra通过对持久层状态的有效管理，来达成整个系统的可靠性和扩展性。在很多场合，Cassandra作为一个数据库来使用，因此他借鉴了很多数据库的设计和实现策略，但是他不能支持完整的关系数据库模型；相反，他提供给客户端一个简单的数据模型，客户端可以通过这个模型，来动态控制数据的布局和格式。Cassandra系统设计成可以运行在大量廉价商用机上面，具备高写吞吐量的同时，不牺牲读性能。

```
- 特性
  ● 分布式
  ● 基于column的结构化
  ● 高伸展性
```

# get cassandra package
```
[whoami@server1 ~]$ tar -zxvf /data/software/
apache-cassandra-2.2.1-bin.tar.gz -C ./

[whoami@server1 ~]$ ln -s apache-cassandra-2.2.1 cassandra   
```

# configing 
```
----server1
[whoami@server1 conf]$ tail -3 cassandra.yaml 
data_file_directories:
        - /data/whoami/cassandra/data
commitlog_directory: /data/whoami/cassandra/commitlog
saved_caches_directory: /data/whoami/cassandra/saved_caches

seed_provider:    
    - class_name: org.apache.cassandra.locator.SimpleSeedProvider
      parameters:
          # seeds is actually a comma-delimited list of addresses.
          # Ex: "<ip1>,<ip2>,<ip3>"
          - seeds: "server1"

listen_address: server1

rpc_address: server1

cluster_name: 'Test Cluster'

1、data_file_directories 可以一次同时设置几个不同目录，cassandra 会自动同步所有目录的数据。
2、由于 Cassandra 采用去中心化结构，所以当集群里的一台机器（节点）启动之后需要一个途径通知当前集群（有新节点加入啦），Cassandra 的配置文件里有一个 seeds 的设置项，所谓的 seeds 就是能够联系集群中所有节点的一台计算机，假如集群中所有的节点位于同一个机房同一个子网，那么只要随意挑选几台比较稳定的计算机即可。在当前的例子中因为只有3台机器，所以我挑选第一台作为种子节点，配置如下：
    seed_provider:
    # Addresses of hosts that are deemed contact points. 
    # Cassandra nodes use this list of hosts to find each other and learn
    # the topology of the ring.  You must change this if you are running
    # multiple nodes!
    - class_name: org.apache.cassandra.locator.SimpleSeedProvider
      parameters:
          # seeds is actually a comma-delimited list of addresses.
          # Ex: "<ip1>,<ip2>,<ip3>"
          - seeds: "server1"

[whoami@server1 ~]$ scp -rq apache-cassandra-2.2.1 server2:/home/whoami/
  
配置好的 Cassandra 复制到第2和第3台机器，同时创建相关的目录，还需要修改
listen_address 和 rpc_address 为实际机器的IP地址。至此所有的配置完成了。

----server2

cluster_name: 'mycluster'
seed_provider:    
    - class_name: org.apache.cassandra.locator.SimpleSeedProvider
      parameters:
          # seeds is actually a comma-delimited list of addresses.
          # Ex: "<ip1>,<ip2>,<ip3>"
          - seeds: "server1"
        
listen_address: server2
rpc_address: server2

data_file_directories:
        - /data/whoami/cassandra/data
commitlog_directory: /data/whoami/cassandra/commitlog
saved_caches_directory: /data/whoami/cassandra/saved_caches

----server3,server4
省略，参考server2

```

# start cassandra

在相应的节点执行：
```
$ bin/cassandra -f or bin/cassandra
```

参数 -f 的作用是让 Cassandra 以前端程序方式运行，这样有利于调试和观察日志信息，而在实际生产环境中这个参数是不需要的（即 Cassandra 会以 daemon 方式运行）。

所有节点启动后可以通过 bin/nodetool 工具管理集群，比如查看所有节点运行情况：
```

[whoami@server1 ~]$ cassandra/bin/nodetool status
Datacenter: datacenter1
=======================
Status=Up/Down
|/ State=Normal/Leaving/Joining/Moving
--  Address          Load       Tokens       Owns    Host ID                               Rack
UN  192.168.111.200  131.22 KB  256          ?       c88dce49-f6bc-43a4-adfb-597694faae9e  rack1
UN  192.168.111.201  103.11 KB  256          ?       1cfc5153-f974-44b3-bb5e-b9a54759d023  rack1

Note: Non-system keyspaces don't have the same replication settings, effective ownership information is meaningless
```

# show cluster status
```
[whoami@server1 ~]$ cassandra/bin/nodetool status
Datacenter: datacenter1
=======================
Status=Up/Down
|/ State=Normal/Leaving/Joining/Moving
--  Address          Load       Tokens       Owns    Host ID                               Rack
UN  192.168.111.202  108.12 KB  256          ?       334d3c5f-3265-47da-adc0-d6b21a8d569c  rack1
UN  192.168.111.203  14.39 KB   256          ?       9b67e6c0-0e6d-4787-9858-504765f97126  rack1
UN  192.168.111.200  196.94 KB  256          ?       c88dce49-f6bc-43a4-adfb-597694faae9e  rack1
UN  192.168.111.201  181.84 KB  256          ?       1cfc5153-f974-44b3-bb5e-b9a54759d023  rack1

Note: Non-system keyspaces don't have the same replication settings, effective ownership information is meaningless
```

# cfstats 查询各个CF详细的统计信息，包括写入次数，相响应时间，memtable信息等。
```
[whoami@server1 ~]$ cassandra/bin/nodetool -h localhost  cfstats       
Keyspace: system_traces
        Read Count: 0
        Read Latency: NaN ms.
        Write Count: 0
        Write Latency: NaN ms.
        Pending Flushes: 0
```

# 异常一个下线节点
```
[whoami@server1 ~]$ cassandra/bin/nodetool -h localhost info
ID                     : c88dce49-f6bc-43a4-adfb-597694faae9e
Gossip active          : true
Thrift active          : false
Native Transport active: true
Load                   : 196.94 KB
Generation No          : 1442595318
Uptime (seconds)       : 724
Heap Memory (MB)       : 47.95 / 1198.00
Off Heap Memory (MB)   : 0.00
Data Center            : datacenter1
Rack                   : rack1
Exceptions             : 0
Key Cache              : entries 11, size 864 bytes, capacity 59 MB, 32 hits, 45 requests, 0.711 recent hit rate, 14400 save period in seconds
Row Cache              : entries 0, size 0 bytes, capacity 0 bytes, 0 hits, 0 requests, NaN recent hit rate, 0 save period in seconds
Counter Cache          : entries 0, size 0 bytes, capacity 29 MB, 0 hits, 0 requests, NaN recent hit rate, 7200 save period in seconds
Token                  : (invoke with -T/--tokens to see all 256 tokens)

[whoami@server1 ~]$ bin/nodetool -host 192.168.0.101 removetoken c88dce49-f6bc-43a4-adfb-597694faae9e
```

# 备份数据
```
创建一个快照
$ bin/nodetool -host server1 snapshot
```

# cassandra-cql
```
[whoami@server1 cassandra]$ bin/cqlsh server1
Connected to mycluster at server1:9042.
[cqlsh 5.0.1 | Cassandra 2.2.1 | CQL spec 3.3.0 | Native protocol v4]
Use HELP for help.
cqlsh> help

Documented shell commands:
===========================
CAPTURE  CLS          COPY  DESCRIBE  EXPAND  LOGIN   SERIAL  SOURCE 
CLEAR    CONSISTENCY  DESC  EXIT      HELP    PAGING  SHOW    TRACING

CQL help topics:
================
ALTER                        CREATE_TABLE_TYPES  PERMISSIONS        
ALTER_ADD                    CREATE_USER         REVOKE             
ALTER_ALTER                  DATE_INPUT          REVOKE_ROLE        
ALTER_DROP                   DELETE              SELECT             
ALTER_RENAME                 DELETE_COLUMNS      SELECT_COLUMNFAMILY
ALTER_USER                   DELETE_USING        SELECT_EXPR        
ALTER_WITH                   DELETE_WHERE        SELECT_LIMIT       
APPLY                        DROP                SELECT_TABLE       
ASCII_OUTPUT                 DROP_AGGREGATE      SELECT_WHERE       
BEGIN                        DROP_COLUMNFAMILY   TEXT_OUTPUT        
BLOB_INPUT                   DROP_FUNCTION       TIMESTAMP_INPUT    
BOOLEAN_INPUT                DROP_INDEX          TIMESTAMP_OUTPUT   
COMPOUND_PRIMARY_KEYS        DROP_KEYSPACE       TIME_INPUT         
CREATE                       DROP_ROLE           TRUNCATE           
CREATE_AGGREGATE             DROP_TABLE          TYPES              
CREATE_COLUMNFAMILY          DROP_USER           UPDATE             
CREATE_COLUMNFAMILY_OPTIONS  GRANT               UPDATE_COUNTERS    
CREATE_COLUMNFAMILY_TYPES    GRANT_ROLE          UPDATE_SET         
CREATE_FUNCTION              INSERT              UPDATE_USING       
CREATE_INDEX                 INT_INPUT           UPDATE_WHERE       
CREATE_KEYSPACE              LIST                USE                
CREATE_ROLE                  LIST_PERMISSIONS    UUID_INPUT         
CREATE_TABLE                 LIST_ROLES        
CREATE_TABLE_OPTIONS         LIST_USERS        


1、创建空间，可以理解为创建数据库
cqlsh> CREATE KEYSPACE mykeyspace
   ... WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };

2、使用mykeyspace
cqlsh> USE mykeyspace;

3、创建表
cqlsh:mykeyspace> CREATE TABLE users (
              ...   user_id int PRIMARY KEY,
              ...   fname text,
              ...   lname text
              ... );

4、插入数据
INSERT INTO users (user_id,  fname, lname) VALUES (1745, 'john', 'smith');
INSERT INTO users (user_id,  fname, lname) VALUES (1744, 'john', 'doe');
INSERT INTO users (user_id,  fname, lname) VALUES (1746, 'john', 'smith');


5、查询
cqlsh:mykeyspace> SELECT * FROM users;

 user_id | fname | lname
---------+-------+-------
    1745 |  john | smith
    1744 |  john |   doe
    1746 |  john | smith

(3 rows)

6、创建索引
cqlsh:mykeyspace> CREATE INDEX ON users (lname);
cqlsh:mykeyspace> SELECT * FROM users WHERE lname = 'smith';

 user_id | fname | lname
---------+-------+-------
    1745 |  john | smith
    1746 |  john | smith

(2 rows)

7、查询节点
cqlsh:mykeyspace> SELECT peer,data_center,host_id FROM system.peers; 

 peer            | data_center | host_id
-----------------+-------------+--------------------------------------
 192.168.111.202 | datacenter1 | 334d3c5f-3265-47da-adc0-d6b21a8d569c
 192.168.111.203 | datacenter1 | 9b67e6c0-0e6d-4787-9858-504765f97126
 192.168.111.201 | datacenter1 | 1cfc5153-f974-44b3-bb5e-b9a54759d023

(3 rows)

cqlsh:mykeyspace> SHOW version
[cqlsh 5.0.1 | Cassandra 2.2.1 | CQL spec 3.3.0 | Native protocol v4]
cqlsh:mykeyspace> SHOW host
Connected to mycluster at server1:9042.
cqlsh:mykeyspace> SHOW SESSION;

cqlsh:mykeyspace> DESCRIBE mykeyspace.users;

CREATE TABLE mykeyspace.users (
    user_id int PRIMARY KEY,
    fname text,
    lname text
) WITH bloom_filter_fp_chance = 0.01
    AND caching = '{"keys":"ALL", "rows_per_partition":"NONE"}'
    AND comment = ''
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy'}
    AND compression = {'sstable_compression': 'org.apache.cassandra.io.compress.LZ4Compressor'}
    AND dclocal_read_repair_chance = 0.1
    AND default_time_to_live = 0
    AND gc_grace_seconds = 864000
    AND max_index_interval = 2048
    AND memtable_flush_period_in_ms = 0
    AND min_index_interval = 128
    AND read_repair_chance = 0.0
    AND speculative_retry = '99.0PERCENTILE';
CREATE INDEX users_lname_idx ON mykeyspace.users (lname);

cqlsh:mykeyspace> SELECT keyspace_name,columnfamily_name,cf_id FROM system.schema_columnfamilies WHERE keyspace_name = 'mykeyspace';

 keyspace_name | columnfamily_name | cf_id
---------------+-------------------+--------------------------------------
    mykeyspace |             users | f45405a0-5e2b-11e5-adb6-bfcb7a5c7b40

(1 rows)

cqlsh:mykeyspace>  SELECT keyspace_name,columnfamily_name,column_name,component_index,index_name,index_options,index_type,type FROM system.schema_columns WHERE keyspace_name = 'mykeyspace';

 keyspace_name | columnfamily_name | column_name | component_index | index_name      | index_options | index_type | type
---------------+-------------------+-------------+-----------------+-----------------+---------------+------------+---------------
    mykeyspace |             users |       fname |               0 |            null |          null |       null |       regular
    mykeyspace |             users |       lname |               0 | users_lname_idx |            {} | COMPOSITES |       regular
    mykeyspace |             users |     user_id |            null |            null |          null |       null | partition_key

(3 rows)

[whoami@server1 bin]$ nodetool proxyhistograms
proxy histograms
Percentile      Read Latency     Write Latency     Range Latency
                    (micros)          (micros)          (micros)
50%                  4055.27           5839.59          12108.97
75%                 17436.92          14530.76          25109.16
95%                 52066.35          14530.76         962624.93
98%                 62479.63          14530.76        1386179.89
99%                 89970.66          14530.76        1386179.89
Min                   263.21           1358.10           2346.80
Max                 89970.66          14530.76        1386179.89

[whoami@server1 bin]$  nodetool status mykeyspace
Datacenter: datacenter1
=======================
Status=Up/Down
|/ State=Normal/Leaving/Joining/Moving
--  Address          Load       Tokens       Owns (effective)  Host ID                               Rack
UN  192.168.111.202  699.43 KB  256          22.9%             334d3c5f-3265-47da-adc0-d6b21a8d569c  rack1
UN  192.168.111.203  667.12 KB  256          25.6%             9b67e6c0-0e6d-4787-9858-504765f97126  rack1
UN  192.168.111.200  1.4 MB     256          26.0%             c88dce49-f6bc-43a4-adfb-597694faae9e  rack1
UN  192.168.111.201  757.62 KB  256          25.5%             1cfc5153-f974-44b3-bb5e-b9a54759d023  rack1

[whoami@server1 bin]$ nodetool -h localhost -p 7199 cfstats|wc -l
966
```

# Monitoring with MX4J
```
wget http://downloads.sourceforge.net/project/mx4j/MX4J%20Binary/3.0.2/mx4j-3.0.2.tar.gz?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fmx4j%2Ffiles%2FMX4J%2520Binary%2F3.0.2%2F&ts=1442568047&use_mirror=nchc
```

# Monitoring a Cassandra cluster
  http://docs.datastax.com/en/cassandra/2.2/cassandra/operations/opsMonitoring.html
  http://pimin.net/archives/388
```
install Manage Existing Cluster

wget http://downloads.datastax.com/community/opscenter.tar.gz
[whoami@server1 ~]$ tar -zxvf opscenter-5.2.1.tar.gz 
[whoami@server1 ~]$ cd opscenter-5.2.1
[whoami@server1 opscenter-5.2.1]$ bin/opscenter 
[whoami@server1 opscenter-5.2.1]$ lsof -i :8888
COMMAND     PID   USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
python2.6 18406 whoami    6u  IPv4 525585      0t0  TCP *:ddi-tcp-1 (LISTEN)

install agent
手动安装agent：在OpsCenter的目录下有个agent目录，我们需要的agent就在里面。不安装agent无法显示监控指标...所有节点stomp_interface配置项一致！

[whoami@server1 opscenter-5.2.1]$ cd agent
[whoami@server1 agent]$ echo "stomp_interface: server1" >> ./conf/address.yaml
[whoami@server1 agent]$ bin/datastax-agent
```

- address.yaml详细参数说明
```
The address.yaml configuration file

The address.yaml file contains configuration options for the DataStax Agent.

Note: As of version 5.1 of OpsCenter, the hosts option in address.yaml now determines which nodes the agent connects to. For further information on configuration changes and migration paths, see the Upgrade Guide.
Configuration options

stomp_interface
(Required) Reachable IP address of the opscenterd machine. The connection is made on stomp_port.
stomp_port
The stomp_port used by opscenterd. Default: 61620.
use_ssl
Whether to use SSL communication between the agent and opscenterd. Affects both the STOMP connection and agent HTTP server. Corresponds to [agents] use_ssl in opscenterd.conf. Setting this option to 1 turns on SSL connections. Default: 0.
local_interface
The IP used to identify the node in opscenterd. If broadcast_address is set in cassandra.yaml, this should be the same as that; otherwise, it is typically the same as listen_address in cassandra.yaml. A good check is to confirm that this address is the same as the address that nodetool ring outputs. If not set, the agent attempts to determine the proper IP address via JMX.
agent_rpc_interface
The IP that the agent HTTP server listens on. In a multiple region deployment, this is typically a private IP. Default: Matches rpc_interface from cassandra.yaml.
agent_rpc_broadcast_address
The IP that the central OpsCenter process uses to connect to the DataStax agent. Default: Matches agent_rpc_interface.
api_port
The port used for the agent's HTTP endpoint. Default: 61621.
hosts
The DataStax Enterprise node or nodes responsible for storing OpsCenter data. By default, this will be the local node, but may be configured to store data on a separate cluster. The hosts option accepts an array of strings specifying the IP addresses of the node or nodes. For example, ["1.2.3.4"] or ["1.2.3.4", "1.2.3.5"].
cassandra_port
Port used to connect to the local cassandra node. The native transport port.
cassandra_user
The username used to connect to cassandra when authentication is enabled.
cassandra_pass
The password used to connect to cassandra when authentication is enabled.
jmx_host
Host used to connect to local JMX server. Default: 127.0.0.1.
jmx_port
Port used to connect to local JMX server. Default: 7199.
jmx_user
The username used to connect to the local JMX server if JMX authentication is enabled on the node.
jmx_pass
The password used to connect to the local JMX server if JMX authentication is enabled on the node.
cassandra-conf
The agent attempts to auto-detect the location of the cassandra.yaml file via JMX, but if it cannot, this option must be set to the full path of cassandra.yaml. By default /etc/cassandra/cassandra.yaml on Installer-Services or package installations or /path/to/install/conf/cassandra.yaml on Installer-No Services or tarball installations.
cassandra_install_location
The base directory where DataStax Enterprise or Cassandra is installed. When not set, the agent attempts to auto-detect the location but cannot do so in all cases.
cassandra_log_location
The location of the Cassandra system.log file. This option is only used for the diagnostics tarball, and should only be set if system.log is in a non-standard location.
poll_period
The length of time in seconds between attempts to collect metrics. Default: 60.
disk_usage_update_period
The length of time in seconds to wait between attempts to poll the disk for usage. Default: 60.
jmx_thread_pool_size
The size of the thread pool used for long-running JMX connections. Default: 5.
jmx_operations_pool_size
The size of the JMX connection pool used for JMX operations. Default: 4.
jmx_retry_timeout
The number of retries to attempt while establishing the cassandra host id. Default: 30.
nodedetails_threadpool_size
The size of the thread pool used to obtain node details. Default: 3.
realtime_interval
The length of time in seconds between polling attempts to capture rapidly changing real-time information. Default: 5.
shorttime_interval
The length of time in seconds between polling attempts to capture information that changes frequently (e.g., OS load, data size, running tasks). Default: 10.
longtime_interval
The length of time in seconds between polling attempts to capture information that changes infrequently. Default: 300.
ec2_metadata_api_host
The EC2 metadata api host used to determine information about the node if it is on EC2. Default: 169.254.169.254.
metrics_enabled
Whether to collect and store metrics for the local node. Setting this option to 0 turns off metrics collection. Default: 1.
jmx_metrics_threadpool_size
The size of the thread pool used for collecting metrics over JMX. Default: 4.
metrics_ignored_keyspaces
A comma-separated list of keyspaces ignored by metrics collection. Example: "ks1, ks2, ks3".
metrics_ignored_column_families
A comma-separated list of tables (formerly referred to as column families) ignored by metrics collection. Example: "ks1.cf1, ks1.cf2, ks2.cf1".
metrics_ignored_solr_cores
A comma-separated list of solr cores ignored by metrics collection. Example: "ks1.cf1, ks1.cf2, ks2.cf1".
async_queue_size
The maximum number of queued cassandra operations. If your cluster experiences bursty cassandra stress, increasing this queue size might help. Default: 5000.
async_pool_size
The pool size to use for async operations to cassandra. Default when using local storage: 2. Default when using remote storage: 4.
max_pending_repairs
The maximum number of repairs that might be pending. Exceeding this number blocks new repairs. Default: 5.
ssl_keystore
The SSL keystore location for agents to use to connect to CQL.
ssl_keystore_password
The SSL truststore password for agents to use to connect to CQL.
kerberos_service
The Kerberos service name to use when using Kerberos authentication within DSE.
storage_keyspace
The keyspace that the agent uses to store data.
runs_sudo
Sets whether the DataStax Agent runs using sudo. Setting this option to false means the agent does not use sudo, and the agent user does not run using elevated privileges. Setting this option to true means the agent runs with elevated privileges using sudo.
restore_req_update_period
The frequency in seconds with which status updates are sent to opscenterd during Restore operations in the Backup Service. Default: 60.
backup_staging_dir
The directory used for staging commitlogs to be backed up.
tmp_dir
The location of the Backup Service staging directory for backups. The default location is /var/lib/datastax-agent/tmp.
remote_backup_retries
The number of attempts to make when file download fails during a restore. Default: 3.
remote_backup_timeout
The timeout in milliseconds for the connection used to push backups to remote destinations. Default: 1000.
remote_backup_retry_delay
The delay in milliseconds between remote backup retries. Default: 5000.
remote_verify_initial_delay
Initial delay in milliseconds to wait before checking if a file was successfully uploaded during a backup operation. This configuration option works in conjunction with the remote_verify_max option to distinguish between broken versus tardy backups when cleaning up SSTables. The remote_verify_initial_delay value doubles each time a file transfer validation failure occurs until the value exceeds the remote_verify_max value. Default: 1000 (1 second).
remote_verify_max
The maximum time period in milliseconds to wait after a file upload has completed but is still unreadable from the remote destination. When this delay is exceeded, the file transfer is considered failed. This configuration option works in conjunction with the remote_verify_initial_delay option to distinguish between broken versus tardy backups when cleaning up SSTables. Default: 30000 (30 seconds).
restore_on_transfer_failure
When set to true, a failed file transfer from the remote destination does not halt the restore process. A future restore attempt uses any successfully transferred files. Default: false.
backup_file_queue_max
The maximum number of files that can be queued for an upload to a remote destination. Increasing this number consumes more memory. Default: 10000.
remote_backup_region
The AWS region to use for remote backup transfers. Default: us-west-1.
max_file_transfer_attempts
The maximum number of attempts to upload a file or create a remote destination. Default: 30.
trace_delay
The time in milliseconds to wait between issuing a query to trace and fetching trace events in the Performance Service Slow Query panel. Default: 300.
max-seconds-to-sleep
When stream throttling is configured in Backup Service transfers to or from a remote destination, this setting acts as a cap on how long to sleep when throttling. The cap prevents prematurely closing connections due to inactivity. Default: 25 (seconds).
seconds-to-read-kill-channel
Delay in seconds used to verify that the Backup Service transfer should stop. Default: 0.005.
unthrottled-default
A very large number used for bytes per second if no throttle is selected. Default: 10000000000.
slow_query_past
How far into the past in milliseconds to look for slow queries. Default: 3600000 (1,000 hours).
slow_query_refresh
Time in seconds between slow query refreshes. Default: 5.
slow_query_fetch_size
The limit to how many slow queries are fetched. Default: 2000.
slow_query_ignore
A list of keyspaces to ignore in the slow query log of the Performance Service. Default: ["OpsCenter" "dse_perf"].
config_encryption_active
Specifies whether opscenter should attempt to decrypt sensitive config values. Default: False.
config_encryption_key_name
Filename to use for the encryption key. If a custom name is not specified, opsc_system_key is used by default.
config_encryption_key_path
Path where the encryption key should be located. If unspecified, the directory of address.yaml is used by default.
max_reconnect_time
Maximum delay in ms for an agent to attempt reconnecting to Cassandra. The default is 15000 ms (15 s).
```

```
浏览器输入：http://server1:8888,做一些相应的设置即可监控到cassandra集群.击“Manage Existing Cluster”，输入监控节点-->Enter at least one host / IP in the cluster (newline delimited)

1、进入系统后，提示需要安装4个agent，因为这里有四个cassandra节点！参考install agent
```

![1](http://www.itweet.github.io/screenshots/cassandra-mon.png)

![2](http://www.itweet.github.io/screenshots/cassandra-mon2.png)

![3](http://www.itweet.github.io/screenshots/cassandra-home.png)

![4](http://www.itweet.github.io/screenshots/cassandra-home1.png)

```
2、问题：手动安装某些功能无法使用，比如重启集群，无法使用！建议rpm包安装！
Error restarting cluster: Unable to find scripts for cassandra or dse in /etc/init.d/. If you are running Cassandra or DSE from a tarball installation, please fill out the custom scripts at /usr/share/datastax-agent/bin/(start|stop)-cassandra, or bin/(start|stop)-cassandra if the agent is running from a tarball installation. Dismiss
```

```
3、注意添加主机，需要所有cassandra节点都加入，不然agent会运行不正常!

http://docs.datastax.com/en/opscenter/5.2/opsc/online_help/opscAddingCluster_t.html
```

![5](http://www.itweet.github.io/screenshots/cassandra-hosts.png)

# stoping cluster
```
$ ps auwx | grep cassandra
$ sudo kill pid
```

# java connect cassandra
```
<dependency>
<groupId>com.datastax.cassandra</groupId>
<artifactId>cassandra-driver-core</artifactId>
<version>2.2.1</version>
</dependency>

```

# Configuring authentication
```
Configuring authentication
Steps for configuring authentication.
About this task
To configure Cassandra to use internal authentication, first make a change to the cassandra.yaml file and
increase the replication factor of the system_auth keyspace, as described in this procedure. Next, start up
Cassandra using the default user name and password (cassandra/cassandra), and start cqlsh using the
same credentials. Finally, use these CQL statements to set up user accounts to authorize users to access
the database objects:
Configuration
101
• ALTER ROLE
• ALTER USER
• CREATE ROLE
• CREATE USER
• DROP ROLE
• DROP USER
• LIST ROLES
• LIST USERS
Note: To configure authorization, see Internal authorization.
Procedure
1. Change the authenticator option in the cassandra.yaml file to PasswordAuthenticator.
By default, the authenticator option is set to AllowAllAuthenticator.
authenticator: PasswordAuthenticator
2. Increase the replication factor for the system_auth keyspace to N (number of nodes).
If you use the default, 1, and the node with the lone replica goes down, you will not be able to log into
the cluster because the system_auth keyspace was not replicated.
3. Restart the Cassandra client.
The default superuser name and password that you use to start the client is stored in Cassandra.
$ client_startup_string -u cassandra -p cassandra
4. Start cqlsh using the superuser name and password.
$ cqlsh -u cassandra -p cassandra
5. Create another superuser, not named cassandra. This step is optional but highly recommended.
6. Log in as that new superuser.
7. Change the cassandra user password to something long and incomprehensible, and then forget about
it. It won't be used again.
8. Take away the cassandra user's superuser status.
9. Use the CQL statements listed previously to set up user accounts and then grant permissions to access
the database objects.

http://heipark.iteye.com/blog/2004118
```

# datastax by rpm install cassandra cluster
- http://docs.datastax.com/en/landing_page/doc/landing_page/current.html


原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/

参考：
      文档：http://docs.datastax.com/en/cql/3.3/cql/cql_reference/cqlsh.html
      压缩数据：http://docs.datastax.com/en/cassandra/2.2/cassandra/operations/opsConfigCompress.html
      CQL: http://docs.datastax.com/en/cql/3.3/cql/cqlIntro.html
      cassadra细节：http://blog.sina.com.cn/s/blog_502c8cc40100p860.html
      
