---
layout: post
title:  "Hadoop学习笔记（二）"
categories: big-data
---
##MapReduce进阶技巧

1.  遇到Join类型的问题，有以下几类解决方法：
    1)  最简单的reduce-side的Join，但是效率不高
    2)  使用分布式缓存来实现map-side的Join，适合被Join的表比较小，可以加载到内存中的场景。
    3)  更复杂的Join需要借助Hive和Pig等工具。
2.  用MapReduce实现图的遍历需要将算法分解成多部执行的作业(job)。
3.  [Avro](http://avro.apache.org)是一个序列化框架，可以用于RPC调用也可以用于MapReduce作业。
    依赖于Avro，可以实现语言无关的和复杂的数据类型。
    通过Avro扩展的MapReduce API可以将结构化数据以文件形式作为MapReduce作业的输入和输出。
    类似的框架还有[Protocal Buffers](http://code.google.com/p/protobuf)和[Thrift](http://thrift.apache.org)。

参考书籍：[Hadoop Beginer's Guide](http://book.douban.com/subject/22165649/)
