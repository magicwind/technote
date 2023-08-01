---
layout: post
title:  "在Ubuntu上配置邮件服务"
date:   2014-08-14 21:02:04
categories: ubuntu
---

##简介

Ubuntu默认的邮件传送代理(Mail Transfer Agent aka MTA)是Postfix。
但是还需要安装dovecot来支持邮件客户端（如outlook，foxmail，iOS的Mail)的收发。
本文主要介绍如何安装配置postfix和dovecot，并且允许使用邮件客户端来收发邮件。

**环境**: ubuntu 12.04, postfix 2.9.6, dovecot 2.0.19

###如何察看版本

postfix: `postconf -v mail_version`

dovecot: `dovecot --version`

###什么是MTA

MTA就是一个邮件发送和接收服务器。
如果你需要注册几个邮箱，并且使用你自己的域名的话，MTA就必不可少了。
如果你仅仅是使用@hotmail.com，@163.com结尾的邮箱，那么MTA就不需要了。
MTA主要实现了SMTP协议和相关的安全协议，postfix就是MTA的一个标准实现。
dovecot是一个开源的IMAP和POP3邮件服务器，需要和MTA配合使用。

##安装

最简单是方法是使用`sudo tasksel install mail-server`命令，或者使用`sudo apt-get install postfix`

安装时遇到的问题使用默认选项就可以了，在后面我们还可以修改配置。

##配置

###配置postfix

在命令行输入:

`sudo dpkg-reconfigure postfix`

遇到问题输入对应的答案（将server1.example.com替换成你的域名）:

1.  General type of mail configuration: Internet Site
2.  System mail name: server1.example.com
3.  Root and postmaster mail recipient: <admin_user_name>
4.  Other destinations for mail: server1.example.com, example.com, localhost.example.com, localhost
5.  Force synchronous updates on mail queue?: No
6.  Local networks: 127.0.0.0/8
7.  Mailbox size limit (bytes): 0
8.  Local address extension character: +
9.  Internet protocols to use: all

以上配置也可以直接使用VIM修改`sudo vim /etc/postfix/main.cf`

编辑*/etc/postfix/main.cf*， 配置开启SASL客户端认证
{% highlight txt %}
smtpd_recipient_restrictions = permit_mynetworks, permit_sasl_authenticated, reject_unauth_destination
smtpd_sasl_auth_enable = yes
smtpd_sasl_path = private/auth
smtpd_sasl_type = dovecot
{% endhighlight %}

再重新加载配置`postfix reload`

###配置dovecot

**邮件格式**

mbox是默认的格式。它是传统的unix邮件格式。用户的收件箱一般储存在/var/mail或者/var/spool/mail。
一个文件包含了多封邮件。

maildir是另一种常见的格式。它的特点是一个文件只包含一封邮件。所以这个格式更加可靠和安全。

这两个格式postfix和dovecot都支持。这里我们选择mbox。

编辑*/etc/dovecot/conf.d/10-mail.conf*，设置
{% highlight txt %}
mail_location = mbox:~/mail:INBOX=/var/mail/%u
mail_access_groups = mail  #解决权限问题
{% endhighlight %}
编辑*/etc/dovecot/conf.d/10-auth.conf*，设置
{% highlight txt %}
auth_machanisms = plain login  #允许postfix的SMTP协议认证客户端
service auth {
  unix_listener /var/spool/postfix/private/auth {
    group = postfix
    mode = 0666
    user = postfix
  }
}
{% endhighlight %}
再重新加载配置`doveadm reload`

###日志文件

完成上述配置后，你可以开始测试邮件服务了。
**注意：root用户是无法使用客户端收邮件的。**
请创建一个新用户（命令adduser）供邮件客户端使用。

如果发现问题，记得察看日志文件`/var/log/mail.log`

###检查服务是否启动
netstat -an | grep 143 （检查端口143是否被侦听）

##Cheatsheet
以下命令需要root权限

|组件 |察看非默认配置|配置文件目录|重新加载配置|
|:----|:------------|:---------|:--------:|
|postfix|postconf -n|/etc/postfix|postfix reload|
|dovecot|doveconf -n|/etc/dovecot/conf.d/|doveadm reload|

###所有非配置一览
**postfix**
{% highlight txt %}
alias_database = hash:/etc/aliases
alias_maps = hash:/etc/aliases
append_dot_mydomain = no
biff = no
config_directory = /etc/postfix
inet_interfaces = all
inet_protocols = all
mailbox_command = procmail -a "$EXTENSION"
mailbox_size_limit = 0
mydestination = example.com, localhost.localdomain, localhost
myhostname = example.com
mynetworks = 127.0.0.0/8 [::ffff:127.0.0.0]/104 [::1]/128
myorigin = /etc/mailname
readme_directory = no
recipient_delimiter = +
relayhost =
smtp_tls_session_cache_database = btree:${data_directory}/smtp_scache
smtpd_banner = $myhostname ESMTP $mail_name (Ubuntu)
smtpd_recipient_restrictions = permit_mynetworks, permit_sasl_authenticated, reject_unauth_destination
smtpd_sasl_auth_enable = yes
smtpd_sasl_path = private/auth
smtpd_sasl_type = dovecot
smtpd_tls_cert_file = /etc/ssl/certs/ssl-cert-snakeoil.pem
smtpd_tls_key_file = /etc/ssl/private/ssl-cert-snakeoil.key
smtpd_tls_session_cache_database = btree:${data_directory}/smtpd_scache
smtpd_use_tls = yes
{% endhighlight %}
**dovecot**
{% highlight txt %}
auth_mechanisms = plain login
mail_access_groups = mail
mail_location = mbox:~/mail:INBOX=/var/mail/%u
passdb {
  driver = pam
}
protocols = " imap pop3"
service auth {
  unix_listener /var/spool/postfix/private/auth {
    group = postfix
    mode = 0666
    user = postfix
  }
}
ssl_cert = </etc/ssl/certs/dovecot.pem
ssl_key = </etc/ssl/private/dovecot.pem
userdb {
  driver = passwd
}
{% endhighlight %}
