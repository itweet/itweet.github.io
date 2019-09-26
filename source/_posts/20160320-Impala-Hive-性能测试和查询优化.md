---
title: Impala - Hive 性能测试和查询优化
date: 2016-03-20 13:55:00
category: BigData
tags: Hive
---
## 版本信息
Hadoop 2.6.0-cdh5.4.7
impalad version 2.2.0-cdh5.4.7
hive 1.1.0-cdh5.4.7

## Impala SQL 方言编写的表创建语句
CREATE EXTERNAL TABLE books(
  id BIGINT,
  isbn STRING,
  category STRING,
  publish_date date,
  publisher STRING,
  price FLOAT
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '|'
LOCATION '/data/books/';
 
CREATE EXTERNAL TABLE customers(
  id BIGINT,
  name STRING,
  date_of_birth date,
  gender STRING,
  state STRING,
  email STRING,
  phone STRING
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '|'
LOCATION '/data/customers/';
 
CREATE EXTERNAL TABLE transactions(
  id BIGINT,
  customer_id BIGINT,
  book_id BIGINT,
  quantity INT,
  transaction_date TIMESTAMP
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '|'
LOCATION '/data/transactions/';

## 示例数据

- 使用以下命令下载可自动创建测试数据的程序的 JAR：
```
wget http://elasticmapreduce.s3.amazonaws.com/samples/impala/dbgen-1.0-jar-with-dependencies.jar
```

- 使用以下命令启动程序以创建测试数据。在此示例中，命令行参数指定输出路径 /mnt/dbgen，并将 books、customers 和 transactions 表的大小各指定为 4GB。
```

java -cp dbgen-1.0-jar-with-dependencies.jar DBGen -p ./data -b 4 -c 4 -t 4

  $ tree ./data/         
  ./data/
  ├── books
  │?? └── books
  ├── customers
  │?? └── customers
  └── transactions
      └── transactions
```

- 使用以下命令，在集群的 HDFS 文件系统中创建新文件夹，并将测试数据从主节点的本地文件系统复制到 HDFS：
```
sudo -uhdfs hadoop fs -mkdir /data/
sudo -uhdfs hadoop fs -mkdir /data/books
sudo -uhdfs hadoop fs -mkdir /data/customers
sudo -uhdfs hadoop fs -mkdir /data/transactions

sudo -uhdfs hadoop fs -chown -R hadoop:hadoop /data/*

hadoop fs -put ./data/* /data/
hadoop fs -ls -h -R /data/
```

$ head books/books
0|1-45812-668-3|EDUCATION|1986-06-14|Shinchosha|50.99
1|9-69091-140-1|BODY-MIND-SPIRIT|1983-07-29|Lefebvre-Sarrut|91.99
2|3-73425-809-9|TRANSPORTATION|1996-07-08|Mondadori|54.99
3|8-23483-356-2|FAMILY-RELATIONSHIPS|2002-08-20|Lefebvre-Sarrut|172.99
4|3-58984-308-3|POETRY|1974-06-13|EKSMO|155.99
5|2-34120-729-8|TRAVEL|2004-06-30|Cengage|190.99
6|0-38870-277-1|TRAVEL|2013-05-26|Education and Media Group |73.99
7|8-74275-772-8|LAW|2012-05-01|Holtzbrinck|112.99
8|4-41109-927-4|LITERARY-CRITICISM|1986-04-06|OLMA Media Group|82.99
9|8-45276-479-4|TRAVEL|1998-07-04|Lefebvre-Sarrut|180.99

$ head customers/customers
0|Bailey RUIZ|1947-12-19|M|CT|bailey.ruiz.1947@hotmail.com|114-925-4866
1|Taylor BUTLER|1938-07-30|M|IL|taylor.butler.1938@yahoo.com|517-158-1597
2|Henry BROOKS|1956-12-27|M|IN|henry.brooks.1956@yahoo.com|221-653-3887
3|Kaitlyn WRIGHT|1988-11-20|F|NE|kaitlyn.wright.1988@hotmail.com|645-726-8901
4|Miles LOPEZ|1956-03-15|F|ND|miles.lopez.1956@hotmail.com|222-770-7004
5|Mackenzie PETERSON|1970-09-05|F|NJ|mackenzie.peterson.1970@outlook.com|114-521-5716
6|Maria SPENCER|2002-12-20|F|TX|maria.spencer.2002@yahoo.com|377-612-4105
7|Sienna HENDERSON|1982-11-04|F|MO|sienna.henderson.1982@gmail.com|199-288-5062
8|Samantha WALLACE|1998-03-06|F|TN|samantha.wallace.1998@hotmail.com|711-348-7410
9|Nevaeh PETERSON|1991-06-26|F|AL|nevaeh.peterson.1991@live.com|651-686-3436

$ head transactions/transactions
0|360677155|84060207|4|2010-03-24 10:24:22
1|228662770|136084430|5|2009-07-03 14:53:09
2|355529188|26348618|9|2009-09-13 11:53:26
3|1729168|20837134|5|2006-01-05 19:31:19
4|196166644|99142444|19|2007-01-02 15:07:38
5|43026573|479157832|17|2010-04-14 16:42:29
6|306402023|356688712|12|2010-05-24 22:15:54
7|359871959|312932516|31|2000-04-03 11:06:38
8|379787207|265709742|45|2013-09-09 06:01:06
9|144155611|137684093|11|2010-06-06 17:07:07

## 表大小
下表显示每个表的行计数（以百万行为单位）。GB 值指示每个表的文本文件的大小。在输入类中，books、customers 和 transactions 表始终具有相同大小。
输入类（每个表的大小）     4GB
Books 表（百万行）         63
Customers 表（百万行）     53 
Transactions 表（百万行）  87

## 查询
我们在性能测试中使用了四种不同的查询类型：
- Q1:扫描查询
```
SELECT COUNT(*)
FROM customers
WHERE name = 'Asher MATTHEWS';
```

- 此查询对整个表执行表扫描。通过此查询，我们主要测试：

    + 与 Hive 读取吞吐量相比较的 Impala 读取吞吐量。
    + 对于给定的合计内存大小，在执行表扫描时是否存在输入大小限制，如果存在，Impala 可以处理的最大输入大小是多少？

- Q2:聚合查询
```
SELECT category, count(*) cnt
FROM books
GROUP BY category
ORDER BY cnt DESC LIMIT 10;
```

聚合查询扫描单个表、对行分组并计算每个组的大小。

- Q3：两个表之间的联接查询
```
--Impala
SELECT tmp.book_category, ROUND(tmp.revenue, 2) AS revenue
FROM (
  SELECT books.category AS book_category, SUM(books.price * transactions.quantity) AS revenue
  FROM books JOIN [SHUFFLE] transactions ON (
    transactions.book_id = books.id
    AND YEAR(transactions.transaction_date) BETWEEN 2008 AND 2010
  )
  GROUP BY books.category
) tmp
ORDER BY revenue DESC LIMIT 10;

--Hive
SELECT tmp.book_category, ROUND(tmp.revenue, 2) AS revenue
FROM (
  SELECT books.category AS book_category, SUM(books.price * transactions.quantity) AS revenue
  FROM books JOIN transactions ON (
    transactions.book_id = books.id
    AND YEAR(transactions.transaction_date) BETWEEN 2008 AND 2010
  )
  GROUP BY books.category
) tmp
ORDER BY revenue DESC LIMIT 10;
```

此查询将 books 表与 transactions 表联接，以找到特定时间段内具有最大总收入的前 10 种图书类别。在此实验中，我们对联接操作测试了 Impala 的性能并将这些结果与 Hive 进行比较。

- Q4：三个表之间的联接查询
```
--Impala
SELECT tmp.book_category, ROUND(tmp.revenue, 2) AS revenue
FROM (
  SELECT books.category AS book_category, SUM(books.price * transactions.quantity) AS revenue
  FROM books
  JOIN [SHUFFLE] transactions ON (
    transactions.book_id = books.id
  )
  JOIN [SHUFFLE] customers ON (
    transactions.customer_id = customers.id
    AND customers.state IN ('WA', 'CA', 'NY')
  )
  GROUP BY books.category
) tmp
ORDER BY revenue DESC LIMIT 10;

--Hive
SELECT tmp.book_category, ROUND(tmp.revenue, 2) AS revenue
FROM (
  SELECT books.category AS book_category, SUM(books.price * transactions.quantity) AS revenue
  FROM books
  JOIN transactions ON (
    transactions.book_id = books.id
  )
  JOIN customers ON (
    transactions.customer_id = customers.id
    AND customers.state IN ('WA', 'CA', 'NY')
  )
  GROUP BY books.category
) tmp
ORDER BY revenue DESC LIMIT 10;
```

第四个查询联接三个表，在我们的性能测试中是使用最多内存的查询。

－ 05、两表之间的关联查询
```
  SELECT tmp.book_category, ROUND(tmp.revenue, 2) AS revenue
  FROM (
    SELECT books_orc.category AS book_category, SUM(books_orc.price * transactions_orc.quantity) AS revenue
    FROM books_orc JOIN transactions_orc ON (
      transactions_orc.book_id = books_orc.id
    )
    GROUP BY books_orc.category
  ) tmp
  ORDER BY revenue DESC LIMIT 10;
```

## 性能测试结果
 SQL   Hive       Impala
 Q1    30.291s    1.43s
 Q2    64.282s    1.84s
 Q3    118.524s   8.95s
 Q4    233.448s   20.11s
 q5    30s        20s

## 查询优化
Impala 的内存要求由查询类型确定。没有简单且通用的规则来确定集群可以处理的最大数据大小与其合计内存大小之间的相关性。

Impala 不将整个表加载到内存中，因此可用内存量不会限制它可以处理的表大小。Impala 在内存中构建哈希表，如联接的右侧表或聚合的结果集。此外，Impala 使用内存作为 I/O 缓冲区，集群上的处理器核心数和扫描程序的速度确定使所有核心保持繁忙状态所需的缓冲量。例如，简单的 SELECT count(*) FROM table 语句仅使用 I/O 缓冲区内存。

例如，我们实验的第 1 部分中的 m1.xlarge 集群只有 60 GB 内存，但是当我们执行单个表扫描时，我们能够处理 128 GB 及更大的表。因为 Impala 不需要缓存查询的整个结果集，所以它将结果集流式传输回客户端。相反，执行联接操作时，Impala 可能很快用尽集群的内存，即使合计表大小小于合计内存量。要充分利用可用资源，优化查询极其重要。在此部分中，我们以 Q3 为例说明了一些在内存不足错误发生时可以尝试的优化方法。

下面显示的是在特定数据节点上的 impalad 进程由于内存问题而崩溃时，您会收到的典型消息。要确认内存不足问题，只需登录数据节点并使用 top 命令监控内存使用率 (%MEM)。请注意，即使对于同一个查询，内存不足错误可能不会始终在同一个节点上发生。另外，无需执行任何操作即可从内存不足错误中恢复，因为 impalad 会自动重新启动。

```
Backend 6:Couldn't open transport for ip-10-139-0-87.ec2.internal:22000(connect() failed: Connection refused)
```

简单的查询优化方法可能很有效地允许查询使用更少的内存，从而避免发生内存不足错误。例如，Q3 的第一个版本（预优化）如下所示，其中 transactions 表位于 JOIN 左侧，而 books 表位于右侧：

```
SELECT tmp.book_category, ROUND(tmp.revenue, 2) AS revenue
FROM (
  SELECT books.category AS book_category, SUM(books.price * transactions.quantity) AS revenue
  FROM transactions JOIN books ON (
    transactions.book_id = books.id
    AND YEAR(transactions.transaction_date) BETWEEN 2008 AND 2010
  )
  GROUP BY books.category
) tmp
ORDER BY revenue DESC LIMIT 10;
```

此查询仅适用于 4 GB 输入类，对 8 GB 及更大大小会失败，因为会出现内存不足错误。要了解原因，必须考虑 Impala 如何执行查询。为准备进行联接，Impala 通过仅包含 category、price 和 id 列的 books 表构建哈希表。transactions 表中没有任何内容在内存中进行缓存。但是，因为 Impala 在此示例中广播右侧表，所以 books 表会复制到需要 books 表进行联接的所有节点。在高于 1.2.1 的 Impala 版本中，Impala 基于表统计数据，在广播与分区联接之间进行基于成本的决策。我们仅在 JOIN 语句中交换这两个表来获得 Q3 的第二个版本，如下所示：
```
SELECT tmp.book_category, ROUND(tmp.revenue, 2) AS revenue
FROM (
  SELECT books.category AS book_category, SUM(books.price * transactions.quantity) AS revenue
  FROM books JOIN transactions ON (
    transactions.book_id = books.id
    AND YEAR(transactions.transaction_date) BETWEEN 2008 AND 2010
  )
  GROUP BY books.category
) tmp
ORDER BY revenue DESC LIMIT 10;
```

Q3 的第二个版本更高效，因为只有 transactions 表的一部分才进行广播，而不是整个 books 表。但是，当我们扩展为 32 GB 输入类时，即使 Q3 的第二个版本也会由于内存约束而开始失败。为了进一步优化查询，我们添加了一个提示，以强制 Impala 使用“分区联接”，这会创建最终版本的 Q3，如上面的“查询”部分所示。通过所有这些优化，我们最终设法为高达 64 GB 的输入类成功地执行 Q3，从而可获得内存效率比第一个版本高 16 倍的查询。可通过许多其他方式为 Impala 优化查询，我们将这些方法视为从硬件获取最佳性能并避免内存不足错误的好方法。

## Impala 用户定义的函数
Impala 支持使用 Java 或 C++ 编写的用户定义的函数 (UDF)。此外，您还可以修改为 Hive 创建的 UDF 或用户定义的聚合函数，以便用于 Impala。有关 Hive UDF 的更多信息，请转到 https://cwiki.apache.org/confluence/display/Hive/LanguageManual+UDF。

## Impala 支持的文件和压缩格式

选择正确的文件类型和压缩对于优化 Impala 集群性能非常重要。借助 Impala，您可以查询以下数据类型：

   - Parquet
   - Avro
   - RCFile
   - SequenceFile
   - 非结构化文本

此外，Impala 还支持以下压缩类型：

   - Snappy
   - GZIP
   - LZO（仅用于文本文件）
   - Deflate（Parquet 和文本除外）
   - BZIP2（Parquet 和文本除外）

根据文件类型和压缩，您可能需要使用 Hive 加载数据或创建表。

## Llama on yarn
LLama是impala运行在yarn上面的一个解决方案，但是通过使用下来看，impala-2.2版本的llama依然无法很好的运行在yarn上面，虽然已经去掉beta标签，同样的SQL在独立模式下面运行飞快，而放到llama模式下，运行效率低下，数据量太大还会出现卡住的现象，资源一直无法释放，进度也永远不会变化。所以llama还无法用于生产。因为我们集群硬件配置比较特殊的原因，所以可能判断不太准确，如果是配置高度一致，硬件配置高内存，也许能解决问题。这也从侧面说明impala对硬件的要求很高。配置太低无法很好的运行。

参考：
https://docs.aws.amazon.com/ElasticMapReduce/latest/DeveloperGuide/impala-optimization.html

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/