---
title: SpringBoot 开篇介绍
date: 2016-12-03 18:05:26
category: Web Design
tags: Boot
---
本文主要记录，MySQL在Mac下的绿色安装方式，原因是最近在折腾springboot，并且利用springboot开发一款前端交通出行地图的web应用。使用springboot来进行敏捷开发，如果您曾经是一位Javaweb开发人员，那么你绝对不容错过springboot，他能让你专注业务内容实现，快速敏捷开发。

再也不用羡慕Python web.py , Django等框架（在工作中我大量使用Python，曾经写Javaweb，看到这样美好的软件也不得不为之赞叹），因为Java也能实现敏捷开发。如果您是一名hibernate+springmvc+spring的用户，你绝对可以在几天内快速上手springboot进行开发，对于一名未入Javaweb的同学，建议搞清楚spring系列，不然也玩不转。

在我写springboot的时候，老是想起大学和老师一起封装Hibernate的场景，那不就是springboot中的spring-boot-starter-data-jpa，可惜我们封装的没人家那么友好，老是感叹我们也早就应该写一个属于我们的springboot，现在国外的大牛实现了，我们还是继续拿来主义。^_^

更多springboot提供的模块，`spring-boot-starter-aop`,`spring-boot-starter-mail`,`spring-boot-starter-tomcat`,`spring-boot-starter-test`,`spring-boot-starter-jetty`,`spring-boot-starter-web`,`spring-boot-starter-jdbc`太多了，看到了吗？你没有看错，都是我们曾经大量使用的，jetty，tomcat，mail，aop,JUnit；你绝对应该立刻马上开始使用它。

一名软件工程师，最宝贵的绝对是你的时间，因为这个行业日新月异；在任何一个行业都难看到这样永远高速变化的盛况，一个企业可以在几年内成为庞然大物，几年内从这个地球消失无影无踪。这就是IT行业的高速变化属性；技术在这个行业也是永远在变，永远有最有才华的人在改造新的技术，开拓新的领域，革命永远在发生，不变就意味着消失。哈哈，好可怕，说远了哈。

一名软件工程师，最宝贵的绝对是你的时间，如果你不想法设法的提高你的工作效率，你怎么找女朋友，怎么有时间陪家人，怎么有时间锻炼身体，怎么有时间送小孩上学，基于此种种原因，任何IT人员都在不断寻找提高工作效率的方法。所以大家都各尽所能，推动技术的革新，永远处于快速发展中。用新陈代谢来形容再好不过，现在你们使用的工具是新的，但是迟早是会被代谢掉的，这是大自然的规律，没有人能逃脱它。人们站在巨人的肩膀上，不断的想改进现有的东西，来让世界变得更美好。

所以，为了找到女朋友，多一些时间陪家人，你应该使用最有效率的工具，让你事半功倍，节省更多时间，做更多自己想做的事情，所以SpringBoot你不容错过。

我(软件工程师)从工作开始一直在探索提升工作效率的方法，也有很多小工具，让我工作事半功倍，我可以说上那么几个：
    Dash | Evernote | IntelliJ Idea | PyCharm | Sublime Text | ShadowsocksX | Pocket | Alfred 3 | RescutTime | CheatSheet | SourceTree 
当然，还有各种Chrom插件工具，我不一一列举啦。

SpringBoot官方集成的模块列表：
    https://github.com/spring-projects/spring-boot/tree/master/spring-boot-starters

SpringBoot官方模块使用案例：
    https://github.com/spring-projects/spring-boot/tree/master/spring-boot-samples

![](https://www.itweet.cn/screenshots/spring-init.png)
SpringBoot是一个系列，后续介绍springboot和bigdata实时流计算结合做可视化展现的案例和架构，我会在深入使用它之后写一篇使用体验，是否真的能帮你节省 60% 时间，并且专注你的业务开发。

扯的可真的太远了，记录一下，我在Mac上安装SpringBoot需要使用的MySQL软件吧！

* Download Package

```
wget http://cdn.mysql.com//Downloads/MySQL-5.7/mysql-5.7.16-osx10.11-x86_64.tar.gz
```

* Extract Package

```
tar -zxvf mysql-5.7.16-osx10.11-x86_64.tar.gz -o /usr/local/
```

* Init MySQL

```
cd /usr/local/mysql

sudo bin/mysqld --initialize --user=mysql
..省略打印..
```

注意最后一行内容，带有MySQL初始化密码：
    `2016-11-28T14:51:34.216182Z 1 [Note] A temporary password is generated for root@localhost: sFfO:N!Ec1R<`

* MySQL start Operation

```
cd /usr/local/mysql

sudo support-files/mysql.server start

sudo support-files/mysql.server restart

sudo support-files/mysql.server status

sudo support-files/mysql.server stop
```

* Update root Passowrd

```
cd /usr/local/mysql/bin
./mysqladmin -u root -p password    # 新密码
Enter password:                     # 输入生成的临时密码
```

* Check mysql status

```
mysql -uroot -p123  #登录MySQL

netstat -an -p tcp |grep 3306
tcp46      0      0  *.3306                 *.*                    LISTEN    #查看MySQL状态
```

至此，MySQL安装完成，可以在代码中配置一下application.properties文件，pom引入MySQL，`spring-boot-starter-data-jpa`，开始操作数据库吧。


