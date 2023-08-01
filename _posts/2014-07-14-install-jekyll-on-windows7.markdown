---
layout: post
title:  "在Windows7上安装Jekyll"
date:   2014-07-14 00:21:00
categories: jekyll
---

最后更新: 2014-07-26

2014-07-26 更新了支持Windows下watch的gem安装

Jekyll 2.1是完全支持Windows7下安装的, 具体步骤如下:

1. 安装ruby环境. 推荐使用[RubyInstaller for Windows][ruby-installer]. 安装Ruby 1.9.3-p545和配套的开发包(DEVELOPMENT KIT).

2. 因为Gem源在国内访问较慢, 改成淘宝的国内镜像源, 安装速度会提高很多. 具体设置参考[如下网址][gem-mirror].

3. 正式开始安装jekyll. 
打开集成ruby的命令行, 输入如下命令: `gem install jekyll`

4. 安装好后, 在命令行输入以下指令测试安装. `jekyll -v`

5. 新建一个博客.

    `jekyll new my-jekyll-blog`

    运行后生成一个目录.

6. 进入目录并输入以下指令后会启动内嵌的Web服务器.

    `cd my-jekyll-blog`

    `jekyll serve`

7. 在浏览器中访问http://localhost:4000. 
`重要`这时候你会看到一个空白页面, 说明Web服务器启动出错了.

8. 错误原因是默认的`语法高亮`组件在Windows7下需要额外安装. 
很麻烦的(依赖python). 
幸运的是Jekyll2.0后支持了源生的Gem来支持`语法高亮`.

    按以下操作来开启源生Gem. 打开_config.yml, 最后添加一行
    `highlighter: rouge`

    然后安装rouge的Gem`gem install rouge`

    按CTRL+C关闭Web服务器, 再重新敲入jekyll serve启动Web服务器就好了.

9. Windows下可能还会遇到中文编码问题, 所以新建的文件请使用不带BOM的UTF-8编码. 

    有两种方法设定文件编码的格式: 一种是在`_config.yml`里添加`encoding: utf-8`.

    另一种需要在Windows的命令行下输入chcp 65001来设置命令行的Code Page为UTF-8.

	>注意: 笔者曾经遇到一个错误: 不能在build阶段将about.md转换成html后放到_site目录. 
	最后原因就是about.md使用了UTF-8 with BOM的错误格式.

10. Windows下默认不支持侦听文件改动的功能, 需要额外安装gem.

    命令如下: `gem install wdm`.

    Web服务器启动的命令则变成`jekyll serve --watch`

    具体可以参考[Jekyll on Windows][jekyll-on-windows]和[Run Jekyll on Windows][jekyll-windows].

[ruby-installer]:    http://rubyinstaller.org/downloads/
[gem-mirror]:        http://ruby.taobao.org/
[jekyll-on-windows]: http://jekyllrb.com/docs/windows/#installation
[jekyll-windows]:    http://jekyll-windows.juthilo.com/
