---
title: skynet development for mac
date: 2016-08-28 18:35:07
category: Developer
tags: skynet
---
**大型分布式监控软件-skynet**

# Python Dev
 在Mac下面通过BrewHome来安装[Python Dev](http://pythonguidecn.readthedocs.io/zh/latest/starting/install/osx.html)环境，安装完成之后，调整系统环境变量，由于Mac Terminal我试用了(oh my zsh)[https://jikelab.github.io/tech-labs/2016/04/11/macbook-pro-conf/]所以用户环境变量修改`~/.zshrc`文件，在此文件末尾添加如下一行
```
export PATH=/usr/local/bin:/usr/local/sbin:$PATH
```

接下来可以开始安装Python 2.7：
```
brew install python     # 可通过brew info python查看详细版本信息,默认安装最新的版本
```

或者安装Python 3.0:
```
brew install python3    # 可通过brew info python查看详细版本信息,默认安装最新的版本
```

耗时大概几分钟,即可安装完成！

Setuptools & Pip,Homebrew会自动安装好Setuptools和 pip 。 Setuptools提供 easy_install 命令，实现通过网络（通常Internet）下载和安装第三方Python包。 还可以轻松地将这种网络安装的方式加入到自己开发的Python应用中。

pip 是一款方便安装和管理Python 包的工具， 在一些方面 ， 它更优于 easy_install ，故更推荐它。

根据安装完成信息，提示执行如下升级Setuptools & Pip版本：
```
pip install --upgrade pip setuptools    # python 2.7

pip3 install --upgrade pip setuptools   # python 3.0
```

pip && python
```
➜  ~ pip --version
pip 8.1.2 from /usr/local/lib/python2.7/site-packages (python 2.7)

➜  ~ python --version   # 默认Mac自带 Python 2.7.10,没有自带Setuptools & Pip
Python 2.7.11
```

Phthon 虚拟环境(Virtual Environment)

虚拟环境工具(virturalenv)通过为不同项目创建专属的Python虚拟环境，以实现其依赖的库独立保存在不同的路径。 这解决了“项目X依赖包版本1.x，但项目Y依赖包版本为4.x”的难题，并且维持全局的site-packages目录干净、易管理。

举个例子，通过这个工具可以实现依赖Django 1.3的项目与依赖Django 1.0的项目共存。

进一步了解与使用请参考文档 [Virtual Environments](http://github.com/kennethreitz/python-guide/blob/master/docs/dev/virtualenvs.rst)。

[Python编辑器](http://python.freelycode.com/contribution/list/2)
[虚拟环境工具(virturalenv)构建](http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001432712108300322c61f256c74803b43bfd65c6f8d0d0000)

```
pip install virtualenv

git clone git@github.com:skyneteye/skynet.git

cd skynet/

virtualenv --no-site-packages venv  # 创建一个独立的Python运行环境，参数--no-site-packages，得到一个不带任何第三方的“干净”的python运行环境。

source venv/bin/activate        # 进入venv这个独立环境

pip freeze > requirements.txt   # 获取环境所有依赖

cat requirements.txt |wc -l     # 返回结果为0，说明环境是一个干净，独立的环境

pip install grpcio-tools        # pip安装包测试一下

pip freeze > requirements.txt   # 再次验证是否有依赖包

cat requirements.txt            # 可以看到安装grpcio-tools依赖到了多个包
enum34==1.1.6
futures==3.0.5
grpcio==1.0.0
grpcio-tools==1.0.0
protobuf==3.0.0
six==1.10.0

pip install psutil

pip install influxdb

pip freeze > requirements.txt

cat requirements.txt 
enum34==1.1.6
futures==3.0.5
grpcio==1.0.0
grpcio-tools==1.0.0
influxdb==3.0.0
protobuf==3.0.0
psutil==4.3.1
python-dateutil==2.5.3
pytz==2016.7
requests==2.11.1
six==1.10.0
```

在venv环境下，用pip安装的包都被安装到venv这个环境下，系统Python环境不受任何影响。也就是说，venv环境是专门针对skynet这个应用创建的，符合我们的初衷。

退出当前venv环境，此时就回到了正常的环境，现在pip或python均是在系统Python环境下执行。

```
deactivate 
```

完全可以针对每个应用创建独立的Python运行环境，这样就可以对每个应用的Python环境进行隔离。

virtualenv是如何创建“独立”的Python运行环境的呢？原理很简单，就是把系统Python复制一份到virtualenv的环境，用命令source venv/bin/activate进入一个virtualenv环境时，virtualenv会修改相关环境变量，让命令python和pip均指向当前的virtualenv环境。

小结: virtualenv为应用提供了隔离的Python运行环境，解决了不同应用间多版本的冲突问题。

# gRPC
 * gRPC 
    - https://github.com/google/protobuf/releases/tag/v3.0.0
    - https://github.com/grpc/grpc
    - http://doc.oschina.net/grpc
    - http://www.grpc.io
    - https://github.com/grpc/grpc/tree/master/examples/python

github releases版本为Protocol Buffers v3.0.0-GA，通过brew安装protocol,可以安装开发者版本3.0.0-beta-2
```
➜  ~ brew info protobuf
protobuf: stable 2.6.1 (bottled), devel 3.0.0-beta-2, HEAD
Protocol buffers (Google's data interchange format)

# brew安装出现timeout，翻墙也无法解决，通过github下载提供的macos二进制包，配环境变量即可
➜  ~ brew install --devel protobuf 

➜  ~ pip install grpcio
➜  ~ pip install grpcio-tools 
➜  ~ pip install psutil
```

Download the example
```
  $ # Clone the repository to get the example code:
  $ git clone https://github.com/grpc/grpc
  $ # Navigate to the "hello, world" Python example:
  $ cd grpc/examples/python/helloworld
```

Try it!

 - Run the server
```
 $ python2.7 greeter_server.py &
```

 - Run the client
```
 $ python2.7 greeter_client.py  # 返回结果“Greeter client received: Hello, you!”
```

 - Run Codegen
```
$ tree
.
├── protos
│   └── helloworld.proto
└── run_codegen.py

$ cat protos/helloworld.proto 
syntax = "proto3";

option java_multiple_files = true;
option java_package = "io.grpc.examples.helloworld";
option java_outer_classname = "HelloWorldProto";
option objc_class_prefix = "HLW";

package helloworld;

// The greeting service definition.
service Greeter {
      // Sends a greeting
      rpc SayHello (HelloRequest) returns (HelloReply) {}
}

// The request message containing the user's name.
message HelloRequest {
      string name = 1;
}

// The response message containing the greetings
message HelloReply {
      string message = 1;
}

$ cat run_codegen.py
"""Runs protoc with the gRPC plugin to generate messages and gRPC stubs."""

from grpc.tools import protoc

protoc.main(
    (
    '',
    '-I./protos',
    '--python_out=.',
    '--grpc_python_out=.',
    './protos/helloworld.proto',
    )
)

$ python run_codegen.py

$ tree
.
├── helloworld_pb2.py
├── protos
│   └── helloworld.proto
└── run_codegen.py
```

# rrdtool ubuntu install
  - http://martybugs.net/linux/rrdtool/
  - apt-get install librrds-perl rrdtool

# influxdb for ubuntu
  - https://docs.influxdata.com/influxdb/v0.9/introduction/installation/

# psutil
 - pip install psutil --trusted-host pypi.douban.com

# influxdb
 - pip install influxdb --trusted-host mirrors.aliyun.com

# jinja2 or Mako

# Atlas


# FAQ
  - gRPC 安装失败，因为Google被墙的问题，访问`googlemock.googlecode.com` timed out,翻墙解决.

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/