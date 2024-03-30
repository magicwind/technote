---
layout: post
title:  "在斐讯N1盒子上安装CasaOS"
categories: casaos
---


CasaOS介绍
=====
CasaOS,这是一款由IceWhale公司推出的全新操作系统(严格来说, 是一个可以在Armbian等操作系统上安装的NAS应用)。

IceWhale是一家位于中国的高科技公司,专注于开发创新的软硬件解决方案。他们的愿景是打造一个开放、高效、安全的计算环境,满足个人和企业用户的不同需求。CasaOS正是IceWhale为实现这一目标而推出的开源操作系统。

CasaOS的核心理念是提供一个轻量级、模块化的操作系统,用户可以根据自己的需求,选择安装所需的组件。该系统基于Linux内核构建,采用了全新的图形界面设计,拥有现代化的外观和流畅的用户体验。同时,CasaOS还提供了强大的安全防护措施,确保用户的数据和隐私得到全面保护。

该系统的另一大亮点是对ARM架构的优化支持。随着物联网、边缘计算等新兴技术的发展,ARM处理器正在越来越多的设备中应用。CasaOS正是针对这一趋势做了大量优化工作,确保在ARM平台上表现出色。

准备工作
=====

1. 以N1盒子为例，最新的固件去[GitHub](https://github.com/ophub/amlogic-s9xxx-armbian/releases)下载，大佬一直在更新。
在Release下面下载这个文件（版本号和后缀时间可能不同）：
版本有Jammy(Ubuntu系统)和bookworm(Debian系统)2种, 都是LTS长时间支持的版本. 内核我选6.1的, 因为bookworm版本比Jammy版本体积要小(前者700MB, 后者900MB), 选了下载前者.

    文件名: Armbian_24.5.0_amlogic_s905d_bookworm_6.1.82_server_2024.03.16.img.gz

2. 下载U盘写入工具，可以使用balenaEtcher或rufus, 将下载的Armbian镜像写入U盘

3. 将U盘插入靠近HDMI口的USB接口里，插电，自动进入U盘系统。

    **注意**: 此步骤需要之前刷过机，可以从USB启动。如果不确定，那就先试试，如果启动不了，参照B站的教程刷吧。

4. 在路由器后台看到armbian设备，记住IP地址，用SSH工具登录。下面以Windows11的CMD命令提示符为例。

Armbian安装
=====
SSH进入Armbian系统: ssh root@ip_addr.

需要修改root密码.

命令行选zsh

然后创建一个新用户,并设置密码.

最后设置时区和语言.

接下来执行armbian-install命令开始安装.

设备ID选择101 (N1),文件系统选择ext4, 然后等待安装, 安装结束后执行poweroff命令,关机并拔下电源和USB盘,再重新上电.

到这里,armbian操作系统就装好了,系统已经安装到N1内置的存储上了, 启动结束后可以使用SSH重新登录,这里建议使用新建的用户名登录.

CasaOS安装
=====
现在开始安装CasaOS, 安装只需要执行一条命令就可以了: `curl -fsSL https://get.casaos.io | sudo bash`

然后需要输入密码,因为是非root用户安装.

看到一个告警, 剩余磁盘空间小于5GB, 是否继续安装, 输入1.

更新package manager比较慢, 有访问国外网站的网速有关系,请耐心等待.

casaos安装完毕直接可以在浏览器打开armbian的IP地址，不用输入端口号，自动进入casaos界面

创建用户名和密码就可以登录了。

用户名自定义，不要用root

casaos对大佬来说可能作用不是很大，但对我来说是非常好的系统，安装软件和挂载硬盘都简单了许多。

安装其他软件，例如qbittorrent, 打开App Store, 搜索qbit. 然后点击安装. 安装完成后, 可以看到应用图标出现在桌面上, 然后再点击设置, 在设置窗口里的右上角查看日志, 可以获取admin临时密码.

桌面点击qbittorrent图标打开web应用, 输入用户名admin和刚刚获取的临时密码登录. 在设置里可以修改语言.

qbittorrent的安装就先讲到这里, 实际使用还会外挂USB硬盘才行.

CasaOS对USB支持也相当不错, 把硬盘插入USB后, 就能在桌面看到硬盘, 然后可以在文件应用里查看文件系统了.

先讲到这里, 有什么问题可以在评论区留言.

本教程视频可以访问: [N1上如何安装CasaOS - 轻量级NAS系统](https://www.bilibili.com/video/BV1sm421n73J/?share_source=copy_web&vd_source=0d9d401ed97967bb285e97ad2617e06e)
