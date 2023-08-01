---
layout: post
title:  "使用Shell脚本通过Telnet发送邮件"
categories: linux
---
##介绍

有时候我们需要在linux服务器上对外发送邮件，但是该服务器又没有配置MTA（如postfix或sendmail)。
没有MTA，就不能使用mail命令来发送邮件，所有需要直接使用Telnet连接外部的MTA来发送邮件。

##脚本
{% highlight bash %}
#!/bin/bash

send_mail()
{
  (sleep 2
  echo "ehlo smtp.example.org"
  sleep 2

  sleep 1
  echo "MAIL FROM:<noreply@example.org>"
  sleep 2

  arr=(${1//;/ })
  for i in ${arr[@]}  
  do  
    set -x
    echo "RCPT TO:<$i>"
    set +x
    sleep 3
  done

  sleep 1
  echo "data"
  sleep 2

  echo "from:Your Name Here<noreply@example.org>"
#echo "to:<to@example.com>"   I want to enable BCC here
  echo "subject:${2}"
#enable HTML mail
 	echo "MIME-Version: 1.0;"
	echo 'Content-Type: text/html; charset="UTF-8";'
  echo ""
  echo "${3}"
  echo "."
  sleep 2
  echo "QUIT") | telnet "smtp.example.org" "25"
}

#please specify the value for to(seperated by ;) subject body
send_mail "mail1@example.com;mail2@example.org" "mail subject" "<html>
<body>
<h1>Hello</h1>
<p>this is a important <a href=\"www.baidu.com\">link</a></p>
</body>
</html>
"
{% endhighlight %}

##运行结果
{% highlight txt %}
root@example-org:~> ./send-mail.sh
Trying 11.19.33.68...
Connected to smtp.example.org.
Escape character is '^]'.
220 smtp.example.org ESMTP ready.
250-smtp.example.org Hello smtp.example.org [11.19.33.68]
250-SIZE 52428800
250-PIPELINING
250-STARTTLS
250 HELP
250 OK
+ echo 'RCPT TO:<mail1@example.com>'
+ set +x
250 Accepted
+ echo 'RCPT TO:<mail2@example.org>'
+ set +x
250 Accepted
354 Enter message, ending with "." on a line by itself
250 OK id=1XKiQd-0000I7-2l
Connection closed by foreign host.
{% endhighlight %}

参考文章：
[鸟哥的Linux私房菜-Linux下使用telnet功能](http://linux.vbird.org/linux_server/0380sendmail.php#client_linux_telnet)
