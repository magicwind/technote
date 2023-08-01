---
layout: post
title:  "Airflow的配置"
categories: airflow
---

本文主要介绍Airflow的Web认证和邮件发送服务的相关配置。

## 认证（Authentication）

Airflow默认安装好后，是没有认证的，所有功能都是开放的。

Airflow提供了多种用户认证方式，有Password, OAuth, LDAP等方式。

初期使用的话，使用Password认证方式就满足需求了，所以这里只介绍Password认证的配置。

配置前，先确保一下模块已经安装：
`pip install apache-airflow[password]`

然后修改配置文件airflow.cfg中的webserver节开启密码验证功能。

```
[webserver]
authenticate = true
# 以下配置如果没有，请增加
auth_backend = airflow.contrib.auth.backends.password_auth
```

紧接着在Airflow的虚拟环境下用Python REPL运行以下代码，将初始用户帐号和密码信息写入DB。

```
import airflow
from airflow import models, settings
from airflow.contrib.auth.backends.password_auth import PasswordUser
user = PasswordUser(models.User())
user.username = 'admin'
user.email = 'admin@example.com'
user.password = 'passwd1'
session = settings.Session()
session.add(user)
session.commit()
session.close()
exit()
```

上面执行`user.password = 'passwd1'`时，如果遇到报错`AttributeError: can't set attribute`，而且SQLAlchemy是1.2.0版本，则是由于SQLAlchemy版本与Airflow代码不兼容引起的。
解决方法是将SQLAlchemy降级到1.1.15版本就可以修复。

可以执行`pip install 'sqlalchemy<1.2'`，就可以安装1.1版本。

最后，重启webserver即可看见登录页面。


## SMTP邮件发送服务配置

SMTP服务的配置比较简单，修改airflow.cfg

```
[smtp]
smtp_host = smtp.163.com
smtp_starttls = True
smtp_ssl = False
smtp_user = someone@163.com
smtp_password = 123
smtp_port = 25
smtp_mail_from = someone@163.com
```

需要注意的是如果配置有问题，需要DEBUG SMTP服务的话，最好自己写个Python程序来测试。

我在使用163或者Outlook邮箱时，都遇到了一些问题：163的是把我发送的邮件当作垃圾邮件而拒绝，Outlook则是认证总是失败。

最后使用了SendCloud的邮件服务才可以在Amazon EC2的实例上正常的发送邮件。

附上测试SMTP服务的Python代码：

``` python
from smtplib import SMTP
from email.mime.text import MIMEText
from email.header import Header

def send_email(SMTP_host, user, password, from_addr, to_addrs, subject, content):
    email_client = SMTP(SMTP_host)
    # 开启SMTP会话详细日志
    email_client.set_debuglevel(1)
    email_client.ehlo()
    email_client.starttls()
    email_client.ehlo()
    email_client.login(user, password)
    # create msg
    msg = MIMEText(content,'plain','utf-8')
    msg['Subject'] = Header(subject, 'utf-8')#subject
    msg['From'] = from_addr
    msg['To'] = to_addrs
    email_client.sendmail(from_addr, to_addrs, msg.as_string())

    email_client.quit()

if __name__ == "__main__":
   send_email("smtp.sendcloud.net", "api-user", "api-key", "no-reply@sc-mail.magicwind.top", "feng@oriente.com", "Notice", "ETL Start")
```

配置完SMTP服务后，重启Web Server服务即可生效。