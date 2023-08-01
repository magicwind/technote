---
layout: post
title:  "Hadoop学习笔记（一）"
date:   2014-08-15 00:00:00
categories: big-data
---
##开发MapReduce程序

1.  可以使用**Hadoop Streaming**技术来用脚本语言（如ruby）快速测试map和reduce任务。
    可用于原型开发和初期的数据分析。
2.  使用**命令行和 \| 操作符**来模拟MapReduce流程。
3.  使用**ChainMapper**来进行字段校验和转换， 有两点要注意：
    对除了最后一个的所有的Mapper，它的输出必须和下一个Mapper的输入匹配
    对最后一个Mapper，他的输出必须和下一个Reducer的输入匹配
4.  使用**Distributed Cache**，主要为了在所有节点的任务间共享数据。
    数据以文件作为载体，文件可以是任意格式，比如文本格式，二进制格式。
    文件将被传输到每一个节点。
5.  可以使用自定义的**计数器(Counter)**来记录异常数据的数量。计数器的数据会实时地更新到管理界面。

参考书籍：[Hadoop Beginer's Guide](http://book.douban.com/subject/22165649/)
