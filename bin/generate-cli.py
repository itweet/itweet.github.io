#!/usr/bin/python
# -*- coding: UTF-8 -*-

from time import gmtime, strftime
import os
import sys, getopt

def create(title):
    currentTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    fileTime = strftime("%Y%m%d", gmtime())
    prifx = "../source/_posts/"
    fileName = prifx + fileTime + "-" + title.replace(" ","-")+".md"
    touch(fileName)
    writer(fileName, header(title.capitalize(), currentTime))
    #writer(fileName, footer()) 

def writer(path, content):
    with open(path, 'a') as f:
        f.write(content)
    print("write data to %s" %(path))

def touch(path):
    with open(path, 'a'):
        os.utime(path, None)
    print("create file %s" %(path))

def delete(title):
    try:
        fileTime = strftime("%Y%m%d", gmtime())
        prifx = "../source/_posts/"
        fileName = prifx + fileTime + "-" + title.replace(" ","-") +".md"
        os.remove(fileName)
        print("delete file %s" %(fileName))
    except OSError as e:  ## if failed, report it back to the user ##
        print(("Error: %s - %s." % (e.filename, e.strerror)))

def header(title, time):
    content = """---
title: %s
date: %s
description: Distributed Systems (Spring 2021).
tags: [fusiondb, 2021]
category: fusiondb
---""" %(title, time)
    return content

def footer():
    content="""

![Whoami公众号](https://github.com/realXuJiang/labs/raw/master/common/img/weixin_public.gif)

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
版权声明：自由转载-保持署名-非商业性-禁止演绎（[创意共享3.0许可证](https://creativecommons.org/licenses/by-nc-nd/3.0/deed.zh))
`本博客的文章集合:` http://www.itweet.cn/archives/"""
    return content

def main(argv):
   createfile = ''
   deletefile = ''
   try:
      opts, args = getopt.getopt(argv,"hc:d:",["cfile=","dfile="])
   except getopt.GetoptError:
      print('generate-cli.py -c <createfile> or -d <deletefile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('generate-cli.py -c <createfile> or -d <deletefile>')
         sys.exit()
      elif opt in ("-c", "--cfile"):
         createfile = arg
         create(arg)
      elif opt in ("-d", "--dfile"):
         deletefile = arg
         delete(arg)

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Run 'generate-cli.py -h' for usage.")
    main(sys.argv[1:])
