---
layout: post
title:  "使用Dropwizard快速搭建微服务"
categories: j2ee
---
##介绍

Dropwizard是一个适合开发REST服务的轻量级Java框架。由Yammer团队负责开发并开源。
目前最新的稳定版本是0.7.1。

Dropwizard算不上是一个全新的框架，但是它是建立在若干成熟的库的基础上，并把他们有机的整合起来。
作为一个轻量级框架，核心只包括了构建JSON服务的最小库集合。

##依赖
核心依赖的库包括：

1. 使用Jetty来担当Java容器，支持HTTP请求。
2. 使用实现了JAX-RS的Jersey来实现REST服务。
3. 使用[Jackson](http://wiki.fasterxml.com/JacksonHome)来支持JSON的序列化和反序列化。
4. 使用了[Metics](http://metrics.codahale.com/)来提供运行时监控信息
5. 使用了[Guava](http://code.google.com/p/guava-libraries/)提供优化过的数据结构和帮助类。
6. 日志使用Logback。
7. 使用Hibernate Validator作数据校验。
8. Joda Time来帮助处理日期和时间。

除了以上核心库，还有一些可选的模块来扩展功能：

1. Client模块：提供2种HTTP客户端来和其他WEB服务集成。
2. JDBI模块：使用JDBI库来连接关系型数据库。JDBI是一个灵活的模块化的数据访问库。
3. Migration模块：提供了数据库的版本控制。
4. Hibernate模块：集成了Hibernate来访问关系型数据库。
5. Authentication模块：提供了OAuth认证相关的接口。
6. Test模块：提供了帮助类来实现单元测试和集成测试。

##部署
Dropwizard一开始就是按照微服务的需求来开发的，所以部署的时候和传统Java应用不太一样。
传统Java应用都需要部署到容器内，比如tomcat，jboss。
而Dropwizard因为内置了Jetty容器，所以可以通过命令行独立运行。

Dropwizard的项目打包后，就只有一个jar文件和一个配置文件。

运行它只需要在命令行里输入：
`$ java -jar your-app.jar server app-configuration.yml`

其中app-configuration.yml就是配置文件。

可以看出Dropwizard的项目部署十分简单，而且所有的配置都集中在一个文件里。
当然也可以按照需求把配置拆分成多个文件。

##例子
按照官方文档，作者创建了一个Startup项目。具体代码就不贴了。
有兴趣的同学可以访问[这个地址](https://gitcafe.com/magicwind/dropwizard-startup)去下载。

下载完后，运行maven命令来打包应用：

`mvn clean package`

再运行以下命令初始化数据库：

`$ java -jar target\dropwizard-startup-1.0.0-SNAPSHOT.jar db migrate configuration.yml`

再运行以下命令启动服务：

`$ java -jar target\dropwizard-startup-1.0.0-SNAPSHOT.jar server configuration.yml`

服务启动后，可以看到如下输出：
{% highlight txt %}
INFO  [2014-10-14 09:36:55,605] org.hibernate.annotations.common.Version: HCANN000001: Hibernate Commons Annotations {4.0.4.Final}
INFO  [2014-10-14 09:36:55,612] org.hibernate.Version: HHH000412: Hibernate Core {4.3.5.Final}
INFO  [2014-10-14 09:36:55,613] org.hibernate.cfg.Environment: HHH000206: hibernate.properties not found
INFO  [2014-10-14 09:36:55,614] org.hibernate.cfg.Environment: HHH000021: Bytecode provider name : javassist
INFO  [2014-10-14 09:36:55,630] io.dropwizard.hibernate.SessionFactoryFactory: Entity classes: [me.fengxu.dao.entity.ProjectEntity]
INFO  [2014-10-14 09:36:55,934] org.hibernate.dialect.Dialect: HHH000400: Using dialect: org.hibernate.dialect.H2Dialect
INFO  [2014-10-14 09:36:56,030] org.hibernate.engine.transaction.internal.TransactionFactoryInitiator: HHH000399: Using default transaction strategy (direct JDB
C transactions)
INFO  [2014-10-14 09:36:56,033] org.hibernate.hql.internal.ast.ASTQueryTranslatorFactory: HHH000397: Using ASTQueryTranslatorFactory
INFO  [2014-10-14 09:36:56,577] io.dropwizard.server.ServerFactory: Starting DropWizard Startup
  _____              __          ___                  _    _____ _             _
 |  __ \             \ \        / (_)                | |  / ____| |           | |
 | |  | |_ __ ___  _ _\ \  /\  / / _ ______ _ _ __ __| | | (___ | |_ __ _ _ __| |_ _   _ _ __
 | |  | | '__/ _ \| '_ \ \/  \/ / | |_  / _` | '__/ _` |  \___ \| __/ _` | '__| __| | | | '_ \
 | |__| | | | (_) | |_) \  /\  /  | |/ / (_| | | | (_| |  ____) | || (_| | |  | |_| |_| | |_) |
 |_____/|_|  \___/| .__/ \/  \/   |_/___\__,_|_|  \__,_| |_____/ \__\__,_|_|   \__|\__,_| .__/
                  | |                                                                   | |
                  |_|                                                                   |_|
INFO  [2014-10-14 09:36:56,637] org.eclipse.jetty.setuid.SetUIDListener: Opened application@51411ab6{HTTP/1.1}{0.0.0.0:8080}
INFO  [2014-10-14 09:36:56,639] org.eclipse.jetty.setuid.SetUIDListener: Opened admin@940cc67{HTTP/1.1}{0.0.0.0:8081}
INFO  [2014-10-14 09:36:56,641] org.eclipse.jetty.server.Server: jetty-9.0.z-SNAPSHOT
INFO  [2014-10-14 09:36:56,756] com.sun.jersey.server.impl.application.WebApplicationImpl: Initiating Jersey application, version 'Jersey: 1.18.1 02/19/2014 03:
28 AM'
INFO  [2014-10-14 09:36:56,838] io.dropwizard.jersey.DropwizardResourceConfig: The following paths were found for the configured resources:

    GET     /tasks (me.fengxu.resources.TaskResource)
    GET     /users/{personId} (me.fengxu.resources.UserResource)
    GET     /protected (me.fengxu.resources.ProtectedResource)
    GET     /projects (me.fengxu.resources.ProjectResource)
    GET     /projects/{projectID} (me.fengxu.resources.ProjectResource)

INFO  [2014-10-14 09:36:57,014] org.eclipse.jetty.server.handler.ContextHandler: Started i.d.j.MutableServletContextHandler@c211bf8{/,null,AVAILABLE}
INFO  [2014-10-14 09:36:57,017] io.dropwizard.setup.AdminEnvironment: tasks =

    POST    /tasks/gc (io.dropwizard.servlets.tasks.GarbageCollectionTask)

INFO  [2014-10-14 09:36:57,021] org.eclipse.jetty.server.handler.ContextHandler: Started i.d.j.MutableServletContextHandler@516b0351{/,null,AVAILABLE}
INFO  [2014-10-14 09:36:57,078] org.eclipse.jetty.server.ServerConnector: Started application@51411ab6{HTTP/1.1}{0.0.0.0:8080}
INFO  [2014-10-14 09:36:57,081] org.eclipse.jetty.server.ServerConnector: Started admin@940cc67{HTTP/1.1}{0.0.0.0:8081}
{% endhighlight %}

最后打开浏览器，输入`http://localhost:8080/users/2`,可以看到JSON返回。

`{"name":"Ludwig Xu","email":"magicwind@msn.com"}`
