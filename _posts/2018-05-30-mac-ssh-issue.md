---
layout: post
title:  "macOS更新10.13.4后SSH的问题"
categories: macos
---

好久没有更新了！今天当我用SSH登录远程服务器时，报错了。使用SSH的Verbose参数看了下DEBUG日志，看不出名堂。
```
$ ssh root@xx.100.xx.xx -vvv
OpenSSH_7.6p1, LibreSSL 2.6.2
debug1: Reading configuration data /Users/feng/.ssh/config
debug1: Reading configuration data /etc/ssh/ssh_config
debug1: /etc/ssh/ssh_config line 48: Applying options for *
debug1: /etc/ssh/ssh_config line 52: Applying options for *
debug2: ssh_connect_direct: needpriv 0
....
debug2: compression ctos: none,zlib
debug2: compression stoc: none,zlib
debug2: languages ctos:
debug2: languages stoc:
debug2: first_kex_follows 0
debug2: reserved 0
debug1: kex: algorithm: diffie-hellman-group-exchange-sha1
debug1: kex: host key algorithm: ssh-rsa
Unable to negotiate with xx.100.xx.xx port 22: no matching cipher found. Their offer: aes128-cbc,3des-cbc,blowfish-cbc,cast128-cbc,arcfour,aes192-cbc,aes256-cbc,rijndael-cbc@lysator.liu.se
```

## Solution

Google了一下，发现是由于升级macOS High Sierra 到 version 10.13.x (x > 2)后出现的问题。

解决方式很简单：

打开这个文件并编辑：~/.ssh/config (如果没有就创建)，增加这行
```
Ciphers aes128-ctr,aes192-ctr,aes256-ctr,aes128-cbc,3des-cbc
```
不建议修改系统级别的/etc/ssh/ssh_config，不太清楚Apple为啥更新这个文件。

另外，今天使用Airflow时，发现Python3.6.4也有一个问题是升级导致的，原因时Apple更改了Fork进程的方式，下次再记录下这个问题的解决方法。