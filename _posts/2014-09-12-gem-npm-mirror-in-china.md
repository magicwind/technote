---
layout: post
title:  "Gem和NPM的国内镜像"
categories: ruby nodejs
---
##背景

Gem是ruby的包安装工具，NPM是nodejs的包安装和依赖管理工具。
因为两者的服务器都在美国，所以国内访问速度很慢。
这就导致执行bundle install（bundler是ruby的包依赖管理工具）或者npm install的时候经常会失败，用户体验相当不好。

好在国内大公司阿里给这些服务都做了镜像，大大加快了包下载的速度。

下面简单介绍一下这些镜像的使用方法。

测试环境：
Mac 10.9.4, gem 2.0.14, npm 1.4.23

##Gem镜像
访问网址[ruby.taobao.org](http://ruby.taobao.org/)，页面里的“如何使用”讲述了替换默认源地址的方法。
这里这指出几点需要注意的地方：

1.  要注意http和https的区别。有些系统默认源地址是http协议的，所以移除默认源的命令就变成`gem sources --remove https://rubygems.org/`。
2.  执行`gem sources -l`，请确保只有一个淘宝的源。

之后就可以使用`gem install [gem-name]`体验极速地安装体验了。

##NPM镜像
访问网址[npm.taobao.org](http://npm.taobao.org/)，阅读“使用说明”这一节。
网站提供了两种安装方式：一种是直接安装cnpm包，另一种是建立一个别名（alias）。

第一种方式比较简单，但是会在系统里多安装一个cnpm包。推荐新手使用。

第二种方式比较干净，只需要修改.bashrc或者.zshrc。不知道后者的可以访问[oh my zsh](http://ohmyz.sh/)。在使用中发现一个缺点就是：如果在cnpm前面加上sudo的话，会报错。具体如下：
{% highlight bash %}
$ sudo cnpm install -g yo
sudo: cnpm: command not found
{% endhighlight %}
解决办法就是使用如下命令代替：

`$ sudo npm install -g yo --registry=https://registry.npm.taobao.org`

任一种方式安装完以后，就可以使用`cnpm install [package-name]`命令来安装新包了。相比国外服务器，速度至少快了5倍以上。

##题外话
有了这些镜像，ruby和nodejs的用户体验提升了一大截。安装的过程也很愉悦，基本上不会遇到因为网络问题而造成的失败了。就像上网时小猫变光纤后，所体会到的高大上。

最近在学习Vagrant和Docker，这两者都需要从国外服务器下载大的镜像文件。
现在国内访问速度很慢，大大影响了用户体验。希望以后国内也有类似的镜像服务出现。
