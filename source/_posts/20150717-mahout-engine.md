---
title: mahout-engine
date: 2015-07-17 17:50:22
description: Mahout 是 Apache Software Foundation（ASF） 旗下的一个开源项目，提供一些可扩展   的机器学习领域经典算法的实现，旨在帮助开发人员更加方便快捷地创建智能应用程序。   
category: AI
tags: Mahout
---
![](http://mahout.apache.org/images/mahout-logo-brudman.png)

Mahout 是 Apache Software Foundation（ASF） 旗下的一个开源项目，提供一些可扩展   的机器学习领域经典算法的实现，旨在帮助开发人员更加方便快捷地创建智能应用程序。   
Mahout包含许多实现，包括聚类、分类、推荐过滤、频繁子项挖掘。此外，通过使用  Apache Hadoop 库，Mahout 可以有效地扩展到云中。

# 一、maven构建mahout开发环境
> 开发环境
>$ mvn -v  
>Apache Maven 3.0.5 (r01de14724cdef164cd33c7c8c2fe155faf9602da; 2013-02-19   
>21:51:  
>28+0800)  
>Maven home: d:\software\apache\apache-maven-3.0.5  
>Java version: 1.7.0_67, vendor: Oracle Corporation  
>Java home: d:\software\Java\jdk1.7.0_67\jre  
>Default locale: zh_CN, platform encoding: GBK  
>OS name: "windows 8.1", version: "6.3", arch: "amd64", family: "windows"  

## 1、mvn命令生成标准java工程
```
    $ mvn archetype:generate -DarchetypeGroupId=org.apache.maven.archetypes 
    -DgroupId=cn.itweet.mymahout -DartifactId=myMahout -DpackageName=cn.itweet.mymahout -Dversion=1.0-SNAPSHOT -DinteractiveMode=false
```

```
    $ ls myMahout/
    pom.xml  src
```

## 2、把生成的java项目导入eclipse
```
    选择系统1.7jdk,以及maven插件，还有字符编码为utf-8！    
```

## 3、增加mahout依赖，修改pom.xml
```
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>cn.itweet.mymahout</groupId>
    <artifactId>myMahout</artifactId>
    <packaging>jar</packaging>
    <version>1.0-SNAPSHOT</version>
    <name>myMahout</name>
    <url>http://maven.apache.org</url>
    <properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <mahout.version>0.6</mahout.version>
    </properties>

    <dependencies>
    <dependency>
    <groupId>org.apache.mahout</groupId>
    <artifactId>mahout-core</artifactId>
    <version>${mahout.version}</version>
    </dependency>
    <dependency>
    <groupId>org.apache.mahout</groupId>
    <artifactId>mahout-integration</artifactId>
    <version>${mahout.version}</version>
    <exclusions>
    <exclusion>
    <groupId>org.mortbay.jetty</groupId>
    <artifactId>jetty</artifactId>
    </exclusion>
    <exclusion>
    <groupId>org.apache.cassandra</groupId>
    <artifactId>cassandra-all</artifactId>
    </exclusion>
    <exclusion>
    <groupId>me.prettyprint</groupId>
    <artifactId>hector-core</artifactId>
    </exclusion>
    </exclusions>
    </dependency>
    </dependencies>
    </project>
```

## 4、下载依赖
```
    $ cd myMahout/
    $ mvn clean install
```

# 二、用Mahout实现协同过滤userCF
## 1、manhout推荐引擎源码
```
Mahout的推荐引擎，要从org.apache.mahout.cf.taste包说起。
– common: 公共类包括，异常，数据刷新接口，权重常量
– eval: 定义构造器接口，类似于工厂模式
– model: 定义数据模型接口
– neighborhood: 定义近邻算法的接口
– recommender: 定义推荐算法的接口
– similarity: 定义相似度算法的接口
– transforms: 定义数据转换的接口
– hadoop: 基于hadoop的分步式算法的实现类
– impl: 单机内存算法实现类
```

## 2、程序开发: Mahout推荐API
```
   org.apache.mahout.cf.taste.model.DataModel.java
 org.apache.mahout.cf.taste.similarity. UserSimilarity.java
 org.apache.mahout.cf.taste.impl.neighborhood.NearestNUserNeighborhood.java
 org.apache.mahout.cf.taste.recommender.Recommender.java
```

## 3、demo
### 3.1 项目结构
```
D:\software\ProjectSource\scala_ws\myMahout>tree
D:.
├─.settings
├─datafile
├─src
│  ├─main
│  │  └─java
│  │      └─cn
│  │          └─itweet
│  │              └─mymahout
│  └─test
│      └─java
│          └─cn
│              └─itweet
│                  └─mymahout
└─target
    ├─classes
    │  └─cn
    │      └─itweet
    │          └─mymahout
    ├─maven-archiver
    ├─surefire
    ├─surefire-reports
    └─test-classes
        └─cn
            └─itweet
                └─mymahout
```

### 3.2 数据
```
1,101,5.0
1,102,3.0
1,103,2.5
2,101,2.0
2,102,2.5
2,103,5.0
2,104,2.0
3,101,2.5
3,104,4.0
3,105,4.5
3,107,5.0
4,101,5.0
4,103,3.0
4,104,4.5
4,106,4.0
5,101,4.0
5,102,3.0
5,103,2.0
5,104,4.0
5,105,3.5
5,106,4.0
```

>据解释：每一行有三列，第一列是用户ID，第二列是物品ID，第三列是用户对物品的打分。

>运行结果：  
`uid:1(104,4.274336)(106,4.000000)  
uid:2(105,4.055916)  
uid:3(103,3.360987)(102,2.773169)  
uid:4(102,3.000000)  
uid:5  
`

### 3.2 程序
```
package cn.itweet.mymahout;

import java.io.File;
import java.io.IOException;
import java.util.List;

import org.apache.mahout.cf.taste.common.TasteException;
import org.apache.mahout.cf.taste.impl.common.LongPrimitiveIterator;
import org.apache.mahout.cf.taste.impl.model.file.FileDataModel;
import org.apache.mahout.cf.taste.impl.neighborhood.NearestNUserNeighborhood;
import org.apache.mahout.cf.taste.impl.recommender.GenericUserBasedRecommender;
import org.apache.mahout.cf.taste.impl.similarity.EuclideanDistanceSimilarity;
import org.apache.mahout.cf.taste.model.DataModel;
import org.apache.mahout.cf.taste.recommender.RecommendedItem;
import org.apache.mahout.cf.taste.recommender.Recommender;
import org.apache.mahout.cf.taste.similarity.UserSimilarity;


/**
 * Created by root on 2015年7月17日
 */
public class UserCF {

    final static int NEIGHBORHOOD_NUM = 2;
    final static int RECOMMENDER_NUM = 3;

    public static void main(String[] args) throws IOException, TasteException {
        String file = "datafile/item.csv";
        DataModel model = new FileDataModel(new File(file));
        UserSimilarity user = new EuclideanDistanceSimilarity(model);
        NearestNUserNeighborhood neighbor = new NearestNUserNeighborhood(NEIGHBORHOOD_NUM, user, model);
        Recommender r = new GenericUserBasedRecommender(model, neighbor, user);
        LongPrimitiveIterator iter = model.getUserIDs();

        while (iter.hasNext()) {
            long uid = iter.nextLong();
            List<RecommendedItem> list = r.recommend(uid, RECOMMENDER_NUM);
            System.out.printf("uid:%s", uid);
            for (RecommendedItem ritem : list) {
                System.out.printf("(%s,%f)", ritem.getItemID(), ritem.getValue());
            }
            System.out.println();
        }
    }
}
```


# 三、 用Mahout实现推荐系统
## 1、开发前的规划
```
 BookEvaluator.java, 选出“评估推荐器”验证得分较高的算法
 BookResult.java, 对指定数量的结果人工比较
 BookFilterGenderResult.java，只保留男性用户的图书列表
```

## 2、人工对数据进行分析
> 根据最后计算结果去核对，推荐结果是否符合要求！或者符合自然现象.
> 推荐是否合理。通过比对找到一些规则去排除数据，让推荐系统更加准确!
> 利用可视化软件帮助完成分析过程！

# 四、mahout-kmeans聚类测试
```
http://mahout.apache.org/users/clustering/k-means-clustering.html

# wget http://archive.ics.uci.edu/ml/databases/synthetic_control/synthetic_cont
rol.data

# mahout org.apache.mahout.clustering.syntheticcontrol.kmeans.Job
error:Input path does not exist: hdfs://server1:8020/user/hive/testdata

$ hadoop fs -mkdir hdfs://server1:8020/user/hive/testdata

# sudo -u hdfs hadoop fs -put synthetic_control.data /user/hive/testdata

-- 查看结果
$ hadoop fs -ls hdfs://server1:8020/user/hive/output/data
-rw-r--r--   3 hive hdfs     335470 2015-09-03 01:07 hdfs://server1:8020/user/hive/output/data/part-m-00000

$ mahout vectordump -i ./output/data/part-m-00000
15/09/03 01:17:00 INFO common.AbstractJob: Command line arguments: {--endPhase=[2147483647], --input=[./output/data/part-m-00000], --startPhase=[0], --tempDir=[temp]}
15/09/03 01:17:03 INFO vectors.VectorDumper: Sort? false

{0:28.7812,31:26.6311,34:29.1495,4:28.9207,32:35.6541,5:33.7596,8:35.2479,6:25.3969,30:25.0293,24:33.0292,29:34.9424,17:26.5235,51:24.5556,36:26.1927,12:36.0253,23:29.5054,58:25.4652,21:29.27,11:29.2171,10:32.8717,15:32.8717,7:27.7849,28:26.1203,46:28.0721,33:28.4353,55:34.9879,54:34.9318,25:25.04,3:31.2834,49:29.747,41:26.2353,1:34.4632,26:28.9167,44:31.0558,37:33.3182,56:32.4721,42:28.9964,27:24.3437,50:31.4333,16:34.1173,40:35.5344,48:35.4973,39:27.0443,9:27.1159,52:33.7431,13:32.337,43:32.0036,19:26.3693,59:25.8717,2:31.3381,20:25.7744,18:27.6623,22:30.7326,35:28.1584,57:33.3759,45:34.2553,38:30.9772,47:28.9402,14:34.5249,53:25.0466}
{0:24.8923,31:32.5981,34:26.9414,4:27.8789,32:28.3038,5:31.5926,8:27.9516,6:31.4861,30:34.0765,24:31.9874,29:25.0701,17:35.6273,51:31.0205,36:33.1089,12:27.4867,23:30.4719,58:32.1005,21:24.1311,11:31.1887,10:27.5415,15:24.488,7:35.5469,28:33.6472,46:26.3458,33:26.1471,55:26.4244,54:33.6564,25:33.6615,3:32.8217,49:29.4047,41:26.5301,1:25.741,26:25.5511,44:32.8357,37:24.1491,56:28.4661,42:24.8578,27:30.4686,50:32.5577,16:27.5918,40:35.9519,48:28.9861,39:25.7906,9:31.6595,52:26.6418,13:31.391,43:25.9562,19:31.4167,59:26.691,2:27.5532,20:30.7447,18:35.4102,22:35.1422,35:31.5203,57:34.2484,45:28.5322,38:28.5157,47:30.6213,14:27.811,53:28.4331}
......

```

>参考：http://blog.fens.me/hadoop-mahout-maven-eclipse/ </br>
  http://blog.fens.me/mahout-recommend-engine/


原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/