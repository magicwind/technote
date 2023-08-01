---
layout: post
title:  "用Maven来进行集成测试"
categories: j2ee
---
## 介绍

一个J2EE后台完整的测试应该包括单元测试和集成测试。单元测试比较简单，用junit配合maven surefire插件就可以搞定。
而集成测试会相对复杂点，它需要将后台部署到Web容器中再进行测试。

通常集成测试的流程应该包含以下几步：

1.  将后台程序打包成war文件并安装到本地的Maven仓库
2.  集成测试项目启动Web容器（如tomcat或jetty)
3.  集成测试项目将后台war下载并部署到Web容器
4.  运行集成测试的测试用例
5.  关闭Web容器
6.  生成测试报告

##实现方法
我们使用两个Maven插件来实现集成测试。

1.  使用cargo插件来启动和关闭Web容器。
2.  使用failsafe插件来执行测试用例。
3.  Web容器以tomcat7为例，可以很方便的替换到其它cargo支持的容器。

##Maven配置

###cargo插件的配置
{% highlight xml %}
<build>
  <plugins>
    <plugin>
      <groupId>org.codehaus.cargo</groupId>
      <artifactId>cargo-maven2-plugin</artifactId>
      <configuration>
          <deployer></deployer>
          <deployables>
            <deployable>
              <groupId>me.fengxu</groupId>
              <artifactId>j2ee-startup-server</artifactId>
              <type>war</type>
              <properties>
                <context>server</context>
              </properties>
            </deployable>
          </deployables>
        </configuration>
      </plugin>
  </plugins>
  <pluginManagement>
    <plugins>
      <plugin>
        <!-- configure/start/stop container -->
        <groupId>org.codehaus.cargo</groupId>
        <artifactId>cargo-maven2-plugin</artifactId>
        <version>${cargo.version}</version>
        <configuration>
            <!-- Container configuration -->
            <wait>false</wait>
            <container>
                <containerId>tomcat7x</containerId>
                <zipUrlInstaller>
                    <url>http://archive.apache.org/dist/tomcat/tomcat-7/v7.0.16/bin/apache-tomcat-7.0.16.zip
                    </url>
                    <downloadDir>${project.build.directory}/downloads</downloadDir>
                    <extractDir>${project.build.directory}/extracts</extractDir>
                </zipUrlInstaller>
                <log>${project.build.directory}/cargo.log</log>
                <logLevel>debug</logLevel>
            </container>
            <!-- Configuration to use with the container -->
            <configuration>
                <properties>
                    <cargo.logging>high</cargo.logging>
                    <cargo.servlet.port>18080</cargo.servlet.port>
                    <coverage>true</coverage>
                </properties>
            </configuration>
        </configuration>
        <executions>
          <execution>
              <id>start-tomcat</id>
              <phase>pre-integration-test</phase>
              <goals>
                  <goal>start</goal>
              </goals>
          </execution>
          <execution>
              <id>stop-tomcat</id>
              <phase>post-integration-test</phase>
              <goals>
                  <goal>stop</goal>
              </goals>
          </execution>
        </executions>
      </plugin>
    </plugins>
  </pluginManagement>
</build>
{% endhighlight %}

###failsafe插件的配置
{% highlight xml %}
<build>
  <plugins>
    <plugin>
      <groupId>org.apache.maven.plugins</groupId>
      <artifactId>maven-failsafe-plugin</artifactId>
    </plugin>
  </plugins>
  <pluginManagement>
    <plugins>
        <plugin>
            <!-- run tests in **/*ITCase.java classes -->
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-failsafe-plugin</artifactId>
            <version>2.17</version>
            <configuration>
                <!-- <includes>
                  <include>**/TaskITCase.java</include>
                </includes> -->
                <excludes>
                </excludes>
            </configuration>
            <executions>
              <execution>
                  <goals>
                      <goal>integration-test</goal>
                      <goal>verify</goal>
                   </goals>
              </execution>
              </executions>
        </plugin>
      </plugins>
    </pluginManagement>
</build>
{% endhighlight %}

###一个简单的集成测试用例
{% highlight java %}
public class TaskITCase extends BaseCase {

    @Test
    public void testCreateTask() {
        System.out.println("*** test create a task ***");
        createTaskInternal("first task");
    }



    private Long createTaskInternal(String title) {
        String response = postRequest("/rest/tasks", "{ \"title\": \"" + title + "\" }");

        JsonAssert.with(response).assertEquals("$.title", title).assertNotNull("$.id");

        JSONObject taskJSON = new JSONObject(response);
        return taskJSON.getLong("id");
    }

    @Test
    public void testGetAllTasks() {
        System.out.println("*** test get all tasks ***");

        createTaskInternal("second task");
        createTaskInternal("third task");

        String response = getRequest("/rest/tasks");

        JsonAssert.with(response).assertThat("$..title", hasItems("third task","second task"));
    }

    @Test
    public void testSingleTask() {
        System.out.println("*** test get single task ***");

        Long id = createTaskInternal("fourth task");
        String response = getRequest("/rest/tasks/" + id);

        JsonAssert.with(response).assertEquals("$.title", "fourth task").assertNotNull("$.id");
    }
}
{% endhighlight %}

##示例代码
测试环境:
JDK: 1.6
Maven：3.0.5

[Git Repo](https://gitcafe.com/magicwind/j2ee-startup)

###运行集成测试的命令
下载示例代码后，CD到项目目录，在命令行输入`mvn clean install`。
