---
layout: post
title:  "AWS EMR配置Presto LDAP认证"
categories: aws ldap
---

# AWS EMR配置Presto LDAP认证

前提：
LDAP服务需要启用LDAPS连接

步骤如下：

1. 将ldap_server.crt上传到S3

2. 将ldap_server证书导入keystore
    ```
    aws s3 cp s3://your_bucket/certs/ldap_server.crt .
    sudo keytool -import -keystore /usr/lib/jvm/jre/lib/security/cacerts -trustcacerts -alias ldap_server -file ldap_server.crt -storepass changeit
    ```

3. 创建Java Keystore File for TLS
    ```
    keytool -genkeypair -alias presto -keyalg RSA -keystore presto_keystore.jks

    Enter keystore password:
    Re-enter new password:
    What is your first and last name?
    [Unknown]:  ec2-13-250-yy-xx.ap-southeast-1.compute.amazonaws.com
    What is the name of your organizational unit?
    [Unknown]:  datateam
    What is the name of your organization?
    [Unknown]:  mycomp
    What is the name of your City or Locality?
    [Unknown]:  Shanghai
    What is the name of your State or Province?
    [Unknown]:  Shanghai
    What is the two-letter country code for this unit?
    [Unknown]:  CN
    Is CN=ec2-13-250-yy-xx.ap-southeast-1.compute.amazonaws.com, OU=datateam, O=mycomp, L=Shanghai, ST=Shanghai, C=CN correct?
    [no]:  yes

    Enter key password for <presto>
        (RETURN if same as keystore password):
    ```

4. 修改EMR集群配置中master实例组的presto cordinator的https访问
    ```
    presto-config http-server.authentication.type PASSWORD
    presto-config http-server.https.enabled true
    presto-config http-server.https.port 8890
    presto-config http-server.https.keystore.path /home/hadoop/presto_keystore.jks
    presto-config http-server.https.keystore.key xxx
    ```

5. 修改EMR集群配置中master实例组的presto condinator LDAP登录

    先在master的机器上/etc/hosts里增加

    (ldap-server-ip) ldap-server

    ```
    presto-password-authenticator password-authenticator.name ldap
    presto-password-authenticator ldap.url ldaps://ldap-server:636
    presto-password-authenticator ldap.user-bind-pattern cn=${USER},ou=datateam,dc=mycomp,dc=com
    ```

6. Presto CLI连接

    修改presto-env.sh

    `export EXTRA_ARGS="--server https://ec2-13-250-yy-xx.ap-southeast-1.compute.amazonaws.com:8890"`

    这里域名要和第3步的Common Name一致，否则会遇到以下错误：
    Error running command: javax.net.ssl.SSLPeerUnverifiedException: Hostname ip-a-b-c-d.ap-southeast-1.compute.internal not verified:

    命令行如下
    ```
    ./presto-cli \
    --keystore-path presto_keystore.jks \
    --keystore-password password \
    --catalog <catalog> \
    --schema <schema> \
    --user <LDAP user> \
    --password
    ```

    使用keystore没有使用truststore安全，因为keystore里包含里私钥，需要将keystore中的公钥转换成truststore，使用truststore的命令行如下：
    ```
    ./presto-cli \
    --truststore-path presto_truststore.jks \
    --truststore-password password \
    --catalog <catalog> \
    --schema <schema> \
    --user <LDAP user> \
    --password
    ```

    登录后即使密码错误也会进入提示行presto>，但是执行show tables会认证失败的错误。

7. Keystore转Truststore
    ```
    keytool -exportcert \
            -alias presto \
            -file presto_server.cer \
            -keystore presto_keystore.jks \
            -storepass <pass>

    keytool -importcert \
            -alias presto \
            -file presto_server.cer \
            -keystore presto_truststore.jks \
            -storepass <pass>
    ```

## 常见错误
1. 日志里/var/log/presto/server.log

    Caused by: java.security.cert.CertificateException: No subject alternative DNS name matching ip-10-10-4-173 found.

    要注意下面#5的DNSName一定要和第5步中ldaps://(ldap-server):636中的ldap-server一致。

    ```
    [hadoop@ip-172-31-96-42 ~]$ keytool -list -keystore /usr/lib/jvm/jre/lib/security/cacerts -trustcacerts -storepass changeit -v  -alias ldap_server
    Alias name: ldap_server
    Creation date: Jul 6, 2020
    Entry type: trustedCertEntry

    Owner: CN=ldap-server, OU=Information Technology Dep., O=A1A Car Wash, L=Albuquerque, ST=New Mexico, C=US
    Issuer: CN=docker-light-baseimage, ST=New Mexico, L=Albuquerque, OU=Information Technology Dep., O=A1A Car Wash, C=US

    ...

    #5: ObjectId: 2.5.29.17 Criticality=false
    SubjectAlternativeName [
    DNSName: ldap-server
    ]

    #6: ObjectId: 2.5.29.14 Criticality=false
    ...
    ```

## 常用keytool命令

1. Check which certificates are in a Java keystore

    `keytool -list -v -keystore keystore.jks`

2. Check a particular keystore entry using an alias

    `keytool -list -v -keystore keystore.jks -alias mydomain`

3. Delete a certificate from a Java Keytool keystore

    `keytool -delete -alias mydomain -keystore keystore.jks`

4. List Trusted CA Certs

    `keytool -list -v -keystore $JAVA_HOME/jre/lib/security/cacerts`


## Reference
1. https://www.sslshopper.com/article-most-common-java-keytool-keystore-commands.html

2. https://prestodb.io/docs/current/security/ldap.html

3. https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-presto-ldap.html#emr-presto-ldap-seccfg

4. Book: "Presto: The Definitive Guide"
