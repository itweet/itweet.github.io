---
title: set hive-map-sum for hive
date: 2015-08-04 18:34:13
category: BigData
tags: Hive
---
# 1、增加map数量

首先调整上一步reducer生成文件数据，下面可以把reduce设置为160，即生成160个文件
set mapred.reduce.tasks=160;
create table test as 
select * from temp
distribute by rand(123);

# 2、单纯调整map数量，增加map num
===================初步 filenum ：150 num , filesize: 1.2 G , map ：7 num, reduce : 100 num ====================================
hive (bigdata)> set mapreduce.job.reduces;                                                                                                           
mapreduce.job.reduces=-1                                
hive (default)> set mapred.map.tasks;
mapred.map.tasks=200
hive (default)> set mapred.reduce.tasks;
mapred.reduce.tasks=-1 --(default： 2)
hive (default)> set dfs.block.size;
dfs.block.size=134217728
hive (bigdata)> set mapred.min.split.size;
mapred.min.split.size=1
hive (default)> set mapred.max.split.size;
mapred.max.split.size=256000000


drop table default.tb_user_terminal_test;
create table default.tb_user_terminal_test as  select sum(mdn),usp,times,start_time from bigdata.tb_user_terminal_udp_s2 group by mdn,times,start_time,usp;

-- Time taken: 74.709 seconds

====================
hive (bigdata)> set mapred.map.tasks;
mapred.map.tasks=160
hive (bigdata)> set mapreduce.job.reduces;                                                                                                           
mapreduce.job.reduces=100                                
hive (bigdata)> set mapred.reduce.tasks;
mapred.reduce.tasks=150
hive (bigdata)> set dfs.block.size;
dfs.block.size=16777216
hive (bigdata)> set mapred.min.split.size;
mapred.min.split.size=1
hive (bigdata)> set mapred.max.split.size;
mapred.max.split.size=2560000
 
drop table default.tb_user_terminal_test;
create table default.tb_user_terminal_test as  select sum(mdn),usp,times,start_time from bigdata.tb_user_terminal_udp_s2 group by mdn,times,start_time,usp;

-- Time taken: 126.13 seconds

===================
hive (default)> set mapreduce.job.reduces;
mapreduce.job.reduces=100
hive (default)> set mapred.map.tasks;
mapred.map.tasks=200
hive (default)> set mapred.reduce.tasks;
mapred.reduce.tasks=100
hive (default)> set dfs.block.size;
dfs.block.size=134217728
hive (default)> set mapred.min.split.size;
mapred.min.split.size=1
hive (default)> set mapred.max.split.size;
mapred.max.split.size=25600000

drop table default.tb_user_terminal_test;
create table default.tb_user_terminal_test as  select sum(mdn),usp,times,start_time from bigdata.tb_user_terminal_udp_s2 group by mdn,times,start_time,usp;

-- Time taken: 47.179 seconds

===================
hive (default)> set mapreduce.job.reduces;
mapreduce.job.reduces=100
hive (default)> set mapred.map.tasks; -- *
mapred.map.tasks=200
hive (default)> set mapred.reduce.tasks; -- *
mapred.reduce.tasks=58        
hive (default)> set dfs.block.size; 
dfs.block.size=134217728       -- *
hive (default)> set mapred.min.split.size;
mapred.min.split.size=1
hive (default)> set mapred.max.split.size;
mapred.max.split.size=25600000   -- *

drop table default.tb_user_terminal_test;
create table default.tb_user_terminal_test as  select sum(mdn),usp,times,start_time from bigdata.tb_user_terminal_udp_s2 group by mdn,times,start_time,usp;

-- Time taken: 40.749 seconds

======================最终调整=== filesize : 1.2g, map ：150 num, reduce : 58 num , file: 150 num ========================

hive (default)> set mapreduce.job.reduces;
mapreduce.job.reduces=100
hive (default)> set mapred.map.tasks; 
mapred.map.tasks=200
hive (default)> set mapred.reduce.tasks; 
mapred.reduce.tasks=58        
hive (default)>  set hive.merge.mapredfiles;
hive.merge.mapredfiles=false
hive (default)> set dfs.block.size; 
dfs.block.size=134217728       
hive (default)> set mapred.min.split.size;
mapred.min.split.size=1
hive (default)> set mapred.max.split.size;
mapred.max.split.size=4560000   
hive (default)> set hive.groupby.skewindata;
set hive.groupby.skewindata=true

drop table default.tb_user_terminal_test;
create table default.tb_user_terminal_test as  select sum(mdn),usp,times,start_time from bigdata.tb_user_terminal_udp_s2 group by mdn,times,start_time,usp;

--Time taken: 42.903 seconds

`由于我们需求是没有reducer，为了提高集群资源利用率，手动提高了map的数量！`

`结论：提高了map ：7-->150 num，最后平均跑2h的任务，缩减平均10min!`

每个任务执行执行效率都比较均衡：
![](https://www.itweet.cn/screenshots/hive-map.png)

合理分配map,reduce个数,让某些大任务可以运行集群极限的map,reduce个数，这里怎么确定呢，需要参考[yarn的资源调优](https://www.itweet.cn/2015/07/24/yarn-resources-manager-allocation/),让任务没有Pending，一起Running，那样就不会有任务拖后腿！提高执行效率！当然这里的优化参数最好针对每个应用内部设置！

# 3、FileInputFormat中的getSplits-->plitSize由来
```
/** Splits files returned by {@link #listStatus(JobConf)} when
   * they're too big.*/ 
  public InputSplit[] getSplits(JobConf job, int numSplits)
    throws IOException {
    StopWatch sw = new StopWatch().start();
    FileStatus[] files = listStatus(job);
    
    // Save the number of input files for metrics/loadgen
    job.setLong(NUM_INPUT_FILES, files.length);
    long totalSize = 0;                           // compute total size
    for (FileStatus file: files) {                // check we have valid files
      if (file.isDirectory()) {
        throw new IOException("Not a file: "+ file.getPath());
      }
      totalSize += file.getLen();
    }

    long goalSize = totalSize / (numSplits == 0 ? 1 : numSplits);
    long minSize = Math.max(job.getLong(org.apache.hadoop.mapreduce.lib.input.
      FileInputFormat.SPLIT_MINSIZE, 1), minSplitSize);

    // generate splits
    ArrayList<FileSplit> splits = new ArrayList<FileSplit>(numSplits);
    NetworkTopology clusterMap = new NetworkTopology();
    for (FileStatus file: files) {
      Path path = file.getPath();
      long length = file.getLen();
      if (length != 0) {
        FileSystem fs = path.getFileSystem(job);
        BlockLocation[] blkLocations;
        if (file instanceof LocatedFileStatus) {
          blkLocations = ((LocatedFileStatus) file).getBlockLocations();
        } else {
          blkLocations = fs.getFileBlockLocations(file, 0, length);
        }
        if (isSplitable(fs, path)) {
          long blockSize = file.getBlockSize();
          long splitSize = computeSplitSize(goalSize, minSize, blockSize);

          long bytesRemaining = length;
          while (((double) bytesRemaining)/splitSize > SPLIT_SLOP) {
            String[][] splitHosts = getSplitHostsAndCachedHosts(blkLocations,
                length-bytesRemaining, splitSize, clusterMap);
            splits.add(makeSplit(path, length-bytesRemaining, splitSize,
                splitHosts[0], splitHosts[1]));
            bytesRemaining -= splitSize;
          }

          if (bytesRemaining != 0) {
            String[][] splitHosts = getSplitHostsAndCachedHosts(blkLocations, length
                - bytesRemaining, bytesRemaining, clusterMap);
            splits.add(makeSplit(path, length - bytesRemaining, bytesRemaining,
                splitHosts[0], splitHosts[1]));
          }
        } else {
          String[][] splitHosts = getSplitHostsAndCachedHosts(blkLocations,0,length,clusterMap);
          splits.add(makeSplit(path, 0, length, splitHosts[0], splitHosts[1]));
        }
      } else { 
        //Create empty hosts array for zero length files
        splits.add(makeSplit(path, 0, length, new String[0]));
      }
    }
    sw.stop();
    if (LOG.isDebugEnabled()) {
      LOG.debug("Total # of splits generated by getSplits: " + splits.size()
          + ", TimeTaken: " + sw.now(TimeUnit.MILLISECONDS));
    }
    return splits.toArray(new FileSplit[splits.size()]);
  }
```

参考：[yarn的资源调优](https://www.itweet.cn/2015/07/24/yarn-resources-manager-allocation/),配合此文完成合理资源分配! 


原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/
