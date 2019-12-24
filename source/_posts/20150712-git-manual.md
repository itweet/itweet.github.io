---
title: git manual
date: 2015-07-12 17:01:49
description: Git 使用有段时间了,个人博客也是托管到git上面,经常用到的命令放到这，主要供自己查阅使用
category: BigData
tags: git
---

git使用有段时间了,个人博客也是托管到git上面,经常用到的命令放到这，主要供自己查阅使用，反复查阅能够加深印象，提升技能熟练度。如果你是还不知道 Git 是什么，建议先阅读 [廖雪峰的Git教程](http://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000)

# 1、注册github账号

# 2、install git client
>windows 系统
>msysgit
>注意此客户端不支持带有空格的文件夹名称

# 3、创建本地ssh

## 生成安全验证
```
    $ ssh-keygen -t rsa -C "xxx@qq.com"
```

## 复制文件内容到github的SSK  keys
```
    cd /c/Users/${username}/.ssh/
    cat id_rsa.pub
    xxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## 验证是否配置成功 
```
    $ ssh -T git@github.com
```

## 配置本地用户和邮箱
```
    $ git config --global user.name "itweet"
    $ git config --global user.email "xxx@qq.com"
```

到此Git客户端已安装及GitHub配置完成，现在可以从GitHub传输代码了。

# 4、git clone创建的github项目
 https://github.com/itweet/bigtable-sql.git

 注：github仓库对应多种地址，一个是通过http访问的地址，一个是通过ssh访问的地址。举例，
 HTTP格式地址为：https://github.com/itweet/bigtable-sql.git
 SSH格式地址为：git@github.com:itweet/bigtable-sql.git 
 通过http地址访问时可以不用配置公钥（PublicKey），但每次访问时都需要输入github的用户名和密码。
 
```
    $ git clone git@github.com:itweet/bigtable-sql.git
```

>在改项目创建README.md文件,提交本文件！

``` 
    $ git add README.md
    $ git commit -m "README for this project."
    $ git push origin master
```

 这就完成了一个基本的git clone和源文件修改后往github上推送的功能。

# 5、常用命令

## 工作流
Git 最核心的一个概念就是工作流。工作区(Workspace)是电脑中实际的目录；暂存区(Index)像个缓存区域，临时保存你的改动；最后是版本库(Repository)，分为本地仓库和远程仓库。下图描述的很清楚

![](https://www.itweet.cn/screenshots/git_workflow.jpg)

## 远程仓库

### 添加远程仓库

```
    git remote add origin git@server-name:path/repo-name.git  #添加一个远程库
```

### 查看远程仓库
```
    git remote      #要查看远程库的信息
    git remote -v   #显示更详细的信息
```

### 推送分支
```
    git push origin master    #推送到远程master分支
```

### 抓取分支
```
    git clone git@server-name:path/repo-name.git   #克隆远程仓库到本地(  能看到master分支)
    git checkout -b dev origin/dev  #创建远程origin的dev分支到本地，并命名为dev
    git pull origin master          #从远程分支进行更新 
    git fetch origin master         #获取远程分支上的数据
```

`$ git branch --set-upstream branch-name origin/branch-name`，可以建立起本地分支和远程分支的关联，之后可以直接`git pull`从远程抓取分支。
另外，`git pull` = `git fetch` + `merge` to local

### 删除远程分支
```
    $ git push origin --delete bugfix
    To https://github.com/wuchong/jacman
     - [deleted]         bugfix
```

## 历史管理

### 查看历史
```
    git log --pretty=oneline filename #一行显示
    git log -p -2      #显示最近2次提交内容的差异
    git show cb926e7   #查看某次修改
```

### 版本回退
```
    git reset --hard HEAD^    #回退到上一个版本
    git reset --hard cb926e7  #回退到具体某个版
    git reflog                #查看命令历史,常用于帮助找回丢失掉的commit
```

>用HEAD表示当前版本，上一个版本就是HEAD^，上上一个版本就是HEAD^^，HEAD~100就是上100个版本。

### 管理修改
```
    git status              #查看工作区、暂存区的状态
    git checkout -- <file>  #丢弃工作区上某个文件的修改
    git reset HEAD <file>   #丢弃暂存区上某个文件的修改，重新放回工作区
```

### 查看差异
```
    git diff              #查看未暂存的文件更新 
    git diff --cached     #查看已暂存文件的更新 
    git diff HEAD -- readme.txt  #查看工作区和版本库里面最新版本的区别
    git diff <source_branch> <target_branch>  #在合并改动之前，预览两个分支的差异
```

>使用内建的图形化git：`gitk`，可以更方便清晰地查看差异。当然 Github 客户端也不错。

### 删除文件
```
    git rm <file>           #直接删除文件
    git rm --cached <file>  #删除文件暂存状态
```

### 储藏和恢复
```
    git stash           #储藏当前工作
    git stash list      #查看储藏的工作现场
    git stash apply     #恢复工作现场，stash内容并不删除
    git stash pop       #恢复工作现场，并删除stash内容
```

## 分支管理

### 创建分支
```
    git branch develop              #只创建分支
    git checkout -b master develop  #创建并切换到 develop 分支
```

### 合并分支
```
    git checkout master         #切换到主分支
    git merge --no-ff develop   #把 develop 合并到 master 分支，no-ff  选项的作用是保留原分支记录
    git branch -d develop       #删除 develop 分支
```

## 标签

### 显示标签
```
    git tag         #列出现有标签 
    git show <tagname>  #显示标签信息
```

### 创建标签
```
    git tag v0.1    #新建标签，默认位 HEAD
    git tag v0.1 cb926e7  #对指定的 commit id 打标签
    git tag -a v0.1 -m 'version 0.1 released'   #新建带注释标签
```

### 操作标签
```
    git checkout <tagname>        #切换到标签
    
    git push origin <tagname>     #推送分支到源上
    git push origin --tags        #一次性推送全部尚未推送到远程的本地标签
    
    git tag -d <tagname>          #删除标签
    git push origin :refs/tags/<tagname>      #删除远程标签
```


## Git 设置

### 设置 commit 的用户和邮箱
```
    git config user.name "xx"               #设置 commit 的用户
    git config user.email.com "xx@xx.com"   #设置 commit 的邮箱
    git config format.pretty oneline            #显示历史记录时，每个提交的信息只显示一行
```

### 获取git配置信息
```
whoami@ubuntu:~$ git config --list
user.name=whoami
user.email=xxx@qq.com

whoami@ubuntu:~$  git config user.name
whoami
```

### 获取git命令帮助
```
git –help
man git
git –help
```

## 10 个迅速提升你 Git 水平的提示
http://www.oschina.net/translate/10-tips-git-next-level

## git rest 回退 commit
```
git reset --hard commit_id
git push -f origin master
```

