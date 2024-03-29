---
layout: post
title:  "docker openldap的安装"
categories: docker
---

## LDAPS
操作系统时Amazon Linux

官方说明里关于LDAPS的配置介绍的比较简略，现将测试结果记录如下：

1. 启动容器的命令里可以增加env: LDAP_TLS_VERIFY_CLIENT，忽略Client证书验证：
    ```
    docker run --name ldap-service --hostname ldap.service.my --detach -p 389:389 -p 636:636 --env LDAP_TLS_VERIFY_CLIENT=try osixia/openldap:1.4.0
    ```

    LDAP_TLS_VERIFY_CLIENT可以设置为never或try, 默认是demand

2. 测试LDAPS连接可以使用
    ```
    ldapwhoami -x -H ldaps://ldap.service.my -v
    ```
    连接证书验证失败时会报错：
    ```
    ldap_initialize( ldaps://ldap.service.my:636/??base )
    ldap_sasl_bind(SIMPLE): Can't contact LDAP server (-1)
    ```
    解决方法参考3, 4

    可以查看openldap容器的日志获取具体的错误：
    ```
    TLS: can't accept: No certificate was found..
    or
    TLS: can't accept: A TLS fatal alert has been received..
    ```

3. 先要获取OpenLDAP server的CA根证书:
    ```
    openssl s_client -connect ldap.service.my:636 -showcerts
    ```

    要取输出里第二个证书的内容：
    ```
    1 s:/C=US/O=A1A Car Wash/OU=Information Technology Dep./L=Albuquerque/ST=New Mexico/CN=docker-light-baseimage
    i:/C=US/O=A1A Car Wash/OU=Information Technology Dep./L=Albuquerque/ST=New Mexico/CN=docker-light-baseimage
    -----BEGIN CERTIFICATE-----
    <此处省略>
    -----END CERTIFICATE-----
    ```

    将BEGIN和END之间（含）的内容复制到新文件ca.pem

4. 有两种方式设置客户端验证使用的证书

   1) 使用环境变量

    ```
    LDAPTLS_REQCERT=demand LDAPTLS_CACERT=ca.pem ldapwhoami -x -H ldaps://ldap.service.my -v
    ```
    如果还是连接失败，就把LDAPTLS_REQCERT设置为never

   2) 修改配置文件
    /etc/openldap/ldap.conf
    增加下面两个配置：
    ```
    TLS_CACERT /home/ec2-user/ca.pem
    TLS_REQCERT try
    ```

5. 有个SSL的小知识点是我想到的，但是没去考证: 客户端只需要配置CA根证书就可以验证服务端证书了，而不需要服务端的公有证书。

6. 使用docker openldap自己生成的SSL证书有风险，只可以在内网中使用。

