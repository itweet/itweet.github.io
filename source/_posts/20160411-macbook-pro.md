---
title: macbook-pro
date: 2016-04-11 17:47:47
category: Default
tags: macbook
---
- 从零搭建和配置OSX开发环境
 一直在用，ubuntu／frdora 虚拟机作为开发环境，windows系统做为日常上网系统，最近切换到mac，有些不太适应的地方，比如office开始适应苹果iWork,感觉用着不是特别顺利。除此之外，可能还要花费一些时间寻找在windows上的替代软件。幸好日常使用的软件都在Mac上找到合适的，不得不说Mac版本的软件设计感都特别强烈。 
 对于开发者来说，使用Mac真的非常方便，等同于在Linux一样的体验，最主要是界面友好，办公软件也能很好的满足需要。使用ubuntu很长时间，都止于开发环境，有些办公软件无法配套。Mac很好的解决这需求。

 今天我就来捋一捋，我使用的常规软件在Mac上的基本配置。

![](https://jikelab.github.io/tech-labs/screenshots/mac-pro.png)

# Sublime Text 全程指南
  
  + Install Sublimit Text3 for Mac
```
     $ wget https://download.sublimetext.com/Sublime%20Text%20Build%203103.dmg
```
  
  + Package Control
    作为安装 Sublime Text 插件的必备利器，Package Control 是这款编辑器的标配，可以方便开发人员快速安装需要的插件。
    安装方式，按Ctrl+`调出console,粘贴如下代码并且回车：
```
    import urllib.request,os,hashlib; h = '2915d1851351e5ee549c20394736b442' + '8bc59f460fa1548d1514676163dafc88'; pf = 'Package Control.sublime-package'; ipp = sublime.installed_packages_path(); urllib.request.install_opener( urllib.request.build_opener( urllib.request.ProxyHandler()) ); by = urllib.request.urlopen( 'http://packagecontrol.io/' + pf.replace(' ', '%20')).read(); dh = hashlib.sha256(by).hexdigest(); print('Error validating download (got %s instead of %s), please try manual install' % (dh, h)) if dh != h else open(os.path.join( ipp, pf), 'wb' ).write(by)
```
参考：https://packagecontrol.io/installation ｜ 安装成功之后，重启sublimit text3

  + Package Control 安装插件
    * 1 按下Ctrl+Shift+P调出命令面板
    * 2 输入install 调出 Install Package 选项并回车，然后在列表中选中要安装的插件。
      - 必备插件安装
        
        + git,常用功能。
        
        + Markdown Editing,SublimeText 不仅仅是能够查看和编辑 Markdown 文件，但它会视它们为格式很糟糕的纯文本。这个插件通过适当的颜色高亮和其它功能来更好地完成这些任务。
          
        + OmniMarkupPreviewer,预览markdown 编辑的效果,同时支持渲染代码。

        + SublimeLinter,SublimeLinter是少数几个能在sublime text 3工作的代码检查插件,SublimeLinter支持JavaScript、CSS、HTML、Java、PHP、Python、Ruby等十多种开发语言
        
        + Alignment,Aligment插件让开发者自动对齐代码，包括PHP、CSS、JavaScript语言。使得代码看起来更整齐美观，更具可读性。
        
        + themes
          
          * Agila Theme
          
          * Soda Theme
          
```
          * Soda Theme 是最受欢迎的 Sublime Text 主题。
            在mac安装右边栏现实不正常,在windows一直在用,不知道是否是设置问题???
          * 参考：https://github.com/buymeasoda/soda-theme
```
        + 推荐themes文章
          * [英文](https://scotch.io/bar-talk/best-sublime-text-3-themes-of-2015-and-2016)
          * [译文](http://webres.wang/best-sublime-text-3-themes-of-2015-and-2016/)

# 截图软件
  http://snip.qq.com

# 安装Mac包管理工具homebrew
```
  $ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

  $ brew doctor 
    Your system is ready to brew.

  $	brew search wget

  $ brew install wget
```
参考：https://github.com/Homebrew/homebrew/tree/master/share/doc/homebrew#readme

# 环境变量
  + 用户级别环境变量 ~/.bash_profile
    * touch ~/.bash_profile
  + 全局环境变量 ／etc/paths
  + 系统级环境变量 ／etc/bashrc
 
  + Mac系统的环境变量，加载顺序为：
    /etc/profile /etc/paths ~/.bash_profile ~/.bash_login ~/.profile ~/.bashrc
    当然/etc/profile和/etc/paths是系统级别的，系统启动就会加载，后面几个是当前用户级的环境变量。后面3个按照从前往后的顺序读取，如果~/.bash_profile文件存在，则后面的几个文件就会被忽略不读了，如果~/.bash_profile文件不存在，才会以此类推读取后面的文件。~/.bashrc没有上述规则，它是bash shell打开的时候载入的。

# terminal - oh my zsh 
   打造mac最强终端。
  +  文档
      - https://github.com/robbyrussell/oh-my-zsh/wiki/External-themes
      - https://github.com/robbyrussell/oh-my-zsh
      - http://huang-jerryc.com/2016/08/11/%E6%89%93%E9%80%A0%E9%AB%98%E6%95%88%E4%B8%AA%E6%80%A7Terminal%EF%BC%88%E4%BA%8C%EF%BC%89%E4%B9%8B%20zsh/?hmsr=toutiao.io&utm_medium=toutiao.io&utm_source=toutiao.io
      - http://huang-jerryc.com/2016/08/11/%E6%89%93%E9%80%A0%E9%AB%98%E6%95%88%E4%B8%AA%E6%80%A7Terminal%EF%BC%88%E4%B8%80%EF%BC%89%E4%B9%8B%20iTerm/

  + Basic Installation
```
     sh -c "$(wget https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)"
```
  
  `装完成之后退出当前会话重新打开一个终端窗口，你就可以见到这个彩色的提示了.`

  + Uninstalling Oh My Zsh
```
      Oh My Zsh isn't for everyone. We'll miss you, but we want to make this an easy breakup.

      If you want to uninstall oh-my-zsh, just run uninstall_oh_my_zsh from the command-line. 
      It will remove itself and revert your previous bash or zsh configuration.
```
    
  + Manual Updates
```
    upgrade_oh_my_zs
```
    
# vim 语法高亮
```
     cp /usr/share/vim/vimrc ~/.vimrc
     cat ~/.vimrc
      syntax on
      set nu!
      set cindent
      set background=dark
      set ruler
```

# tunnello vpn
  翻墙利器。啥都不说了，超级强大。

  + https://tunnello.com
    
# chrome plugin
  + Octotree
  
  + Postman - REST Client
  
  + 广告终结者
  
  + 花瓣网页收藏工具
  
  + Momentum
  
  + OneTab
  
  + 参考：http://www.zhihu.com/question/19594682

# vim plugins
  + https://github.com/VundleVim/Vundle.Vim
  + http://www.jianshu.com/p/a0b452f8f720

# github
  + brew install git
    Git安装完毕后，只需要使用git config简单配置下用户名和邮箱就可以使用了。

  + 参考：http://www.bootcss.com/p/git-guide/

# 在使用brew工具时，报了以下错误,github API 访问的权限限制
```
  Error:GitHub API rate limit exceeded for [xxxx]. (But here's the good news: Authenticated requests get a higher 
  rate limit. Check out the documentation for more details.)
  Try again in 5 minutes 54 seconds, or create an personal access token:
  https://github.com/settings/tokens
  and then set the token as: HOMEBREW_GITHUB_API_TOKEN
```

  首先打开,前提你得有github账户， https://github.com/settings/tokens/new
  登陆后，输入Homebrew，生成token
  设置环境变量HOMEBREW_GITHUB_API_TOKEN：
  将HOMEBREW_GITHUB_API_TOKEN变量设置为获取到的token,在终端输入:
  export HOMEBREW_GITHUB_API_TOKEN=XXXXXXXXXX

# Oracle账户
  - whoami@foxmail.com/123456

# vmware install
  - 序列号：FY7N2-6RGD2-081XZ-UYWQC-ZPKCA

# 视频录制软件 
  - Mac screenflow

# GIF动画制作软件
  - LiceCap
  - Gifox

# Node && Hexo个人博客

> 官网：https://hexo.io/
> http://www.jianshu.com/p/73779eacb494

* *  Install git && nodejs
``` 
  brew install node
  brew install git

  node -v 
  git --version
  
  npm -v

```

* * Install hexo cli && Init blog
```
  $ npm install -g hexo-cli
  
  $ hexo init <folder>
  $ cd <folder>
  $ npm install

 -- install plugins
  npm install hexo-migrator-rss --save
  npm install hexo-deployer-git --save

  npm install hexo-generator-feed --save
  npm install hexo-generator-sitemap --save

 -- theme
  http://www.blackshow.me/2015/11/25/hexo-theme-freemind-386-readme-cn/
```

# IDEA Development
 - PyCharm
 - IntelliJ IDEA
   + command+Insert 生成代码，比如gettr,settr，构造函数等
   + command+alt+L 格式化代码
   + command＋alt+R 运行类

# Other
  - VMware Fusion
    + 分辨率问题
    ```
    vmware fusion ubuntu 16.04 分辨率,不是全屏显示，解决方法：
      1. 在VMware Fusion 6.0.4下安装Ubuntu镜像：ubuntu-14.04.1-desktop-amd64.iso

      2. 点击虚拟机菜单栏-安装VMware Tools

      3. 在Ubuntu系统中找到VMwaretools-9.6.2-1294478.tar.gz，右键复制到“桌面”，然后“提取”，在桌面会生成一个文件夹：vmware-tools-distrib

      4. 打开Terminal终端窗口（搜索terminal），输入sudo su，输入密码，然后cd进入桌面的vmware-tools-distrib文件夹，sudo ./vmware-install.pl开始安装，一路按回车确认，安装结束后，输入reboot重启系统。
    ```
  - Foxmail

# 快捷键
  1、Command+空格键：Spotlight（推荐使用Alfred代替）
  2、Command+{C/V/X/A/Z/F}：复制/粘帖/剪切/全选/撤销/查找
  3、Command+Q：退出当前应用
  4、Command+Option+Esc：强制退出应用程序管理器
  5、Command+Delete：删除到回收站
  6、选定文件-回车：重命名文件
  7、剪切功能：Command+c复制，然后command＋option＋v 完成移动移动文件／文件夹
  8、Command+左箭头／右箭头 ，跳到行首／行尾
  9、Control+空格，切换中英文
  10、fn + f11，当前窗口和桌面来回切换
  11、更多 by http://jingyan.baidu.com/article/08b6a591aac09614a909224f.html

# 快速开启应用
  Spotlight 搜索功能，可以搜索 Mac 电脑系统大部分资源。搜索功能快捷键command+空格；
  几乎没有任何等待时间，能非常快速检索到你想查找的软件/文件。
![](https://jikelab.github.io/tech-labs/screenshots/Spotlight-pycharm.png)

# 办公软件
  Microsoft_Office_2016_Volume_Installer.pkg
  
# MarkDown编辑器
  提升写作效率的神器。
  
  - Mou
  - Ulysses
  - Day One

# Python && Pip

# Mac系统清理软件
  
  - cleanmymac

# 监控软件
  
  - Monity

# 图片无损压缩
  - ImageOptim
  - JPEGmini
  - Compress All

# 画流程图软件
 
  - OmniGraffle 
    + 亲测可用
```
    Omnigraffle Pro 6

    Name: mojado Serial: JYFE-JRJN-GSOT-GRAG-EVJI-TEFE-VJI

    Name: mojado@live.com Serial: IZAH-IRLI-EFDI-XAEM-JBJJ-JEFJ-BJJ

    Name: mojado@gnu.org Serial: EMIP-OSMG-CSJU-ZZBL-INXY-TEFI-NXY

    Name: Magic Mike Serial: LGEO-AVRN-TPGY-BZKR-WEQT-ZEB
```
  
  - processon
    + 在线流程图制作工具

  - XMind
    + 思维导图

# SecureCRT
  - SecureCRT
```
  sudo perl ~/Downloads/SecureCRT731/securecrt_mac_crack.pl /Applications/SecureCRT.app/Contents/MacOS/SecureCRT 
    ...
    crack successful
    ....
    省略很多信息， 打开SecureCRT，点击Enter License Data，写入这里成功后提示的license内容。
```

# FTP Tools
  - FileZilla

# Git Client
  - SourceTree
    + google account: MrRebot199@gmail.com
    + google account: hsuscript007@gmail.com

# RDBMS for mac
  - Navicat Premium for mac

# youtube 视频下载神器
  - http://www.clipconverter.cc/
  - (youtube-dl)[https://github.com/rg3/youtube-dl]
    + brew install youtube-dl
      * (使用手册)[https://www.zhihu.com/question/22247271]
    + (You-Get)[http://codingpy.com/article/using-you-get-to-download-videos/]

# mac app 
  - http://www.macbed.com/macosx/

# mac制作u盘系统安装盘
```
➜  sudo diskutil list /dev/disk2
/dev/disk2 (external, physical):
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:                                                     *8.0 GB     disk2

➜  sudo diskutil unmountDisk /dev/disk2

➜  sudo dd if=/Users/whoami/Downloads/CentOS/CentOS-6.7-x86_64-bin-DVD1.iso of=/dev/disk2 bs=1m
```

# Mac for python 2.7/3.0 install(Homebrew)
  - http://pythonguidecn.readthedocs.io/zh/latest/starting/install/osx.html

# Mac for docker
  docker提供了mac的安装包，直接可以安装使用。会以一个app的形式运行！


原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/
