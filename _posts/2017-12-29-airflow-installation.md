---
layout: post
title:  "在AWS EC2上安装Apache Airflow"
categories: airflow
---

Amazon Linux自带的包管理工具是Yum，系统自带的Python版本是2.7。
Airflow可以同时支持Python2和3，这里我们选择在Python3环境下安装。

## 1. 先安装Python 3.6

{% highlight bash %}
sudo yum install python36.x86_64 python36-devel.x86_64
cd /usr/bin
sudo ln -s pip-3.6 pip3
{% endhighlight bash %}

## 2. 然后再安装Airflow的依赖系统包

（这些包是为了编译一部分Airflow所依赖的Python包）

{% highlight bash %}
sudo yum -y groupinstall development
sudo yum -y install zlib-devel
sudo yum -y install openssl-devel
sudo yum -y install mysql-devel
sudo yum -y install postgres-devel
{% endhighlight bash %}

## 3. 给安装Airflow先创建虚拟环境
``` bash
sudo pip3 install virtualenv
virtualenv ~/airflow-env
source ~/airflow-env/bin/activate
```

激活虚拟环境后安装Airflow及其依赖
``` bash
pip install airflow
pip install 'apache-airflow[devel]'
pip install 'apache-airflow[postgres]'
pip install pymysql
```

## 4. 初始化Airflow
设置Airlfow Home所在路径

```
export AIRFLOW_HOME=~/airflow
airflow
```

修改~/airflow/airflow.cfg，将数据库连接修改成

`sql_alchemy_conn = mysql+pymysql://airflow:airflow@localhost/airflow`

登录MySQL数据库，创建airflow数据库
``` sql
create database airflow ;  --UTF8 required
create user 'airflow'@'%' identified by 'airflow';
grant all on airflow.* to 'airflow'@'%';
flush privileges;
```

执行下面语句初始化数据库

`airflow initdb`

## 5. 启动airflow

启动管理界面：

`airflow webserver`

启动调度器：

`airflow scheduler`

至此，Airflow已安装部署完成。