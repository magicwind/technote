---
layout: post
title:  "初学者如何选择大数据平台"
date:   2014-08-07 21:02:04
categories: big-data
---

Hadoop随着大数据分析的流行而开始热起来。
对于初学者，一个好的开发环境是不可获缺的。
看了infoq上的一篇文章，得知Hadoop有太多版本可以选择，
新手往往不知道如何选择一个好的平台来学习。

于是专家提出若干建议：

1.  尽量不要使用Apache Hadoop的原始发行版本，除非你是熟悉Hadoop的开发者，熟悉它的各种配置。

2.  尽量使用商业的发行版本来学习，好处有
    - 商业发行版本的配置比较简单，相比原始版本，很多配置被简化了。
    - 商业发行版本一般打包了常用的和Hadoop相关的组件，避免了一个个手动安装配置的麻烦。
      这就好比开发者更喜欢使用LAMP安装包，而不是手动地一个一个去安装它们。
    - 商业发行版本一般都直接提供了虚拟机镜像，初学者只要安装虚拟机并下载镜像就能直接使用Hadoop。
      省去了配置安装系统和软件，并进行配置的时间。

3.  目前国内使用的比较多的商业发行版本有
    - [Cloudrea的CDH](http://www.cloudera.com/content/support/en/downloads.html)
    - [Hortonworks的CDP](http://zh.hortonworks.com/)
    - [MapR](http://www.mapr.com/)
    - [Amazon Elastic Map Reduce（EMR）](http://aws.amazon.com/cn/elasticmapreduce/)

关于MapReduce的基本原理：

采用了“分而治之”的思想，把复杂的计算拆分成若干个小的计算块分别计算，
然后将所有的计算结果聚合到一起得到最终结果。
每个小的计算块可以并行分发到不同的节点来完成，再将结果汇总到根节点，这就是所谓的分布式计算。

而且MapReduce处理的数据结构是基于key-value对，Map函数首先对key-value对进行变换，
变换的结果作为中间结果（也是key-value形式）再输入到Reduce函数。由Reduce函数生成最终结果。

整个流程用公式可以表示成：

`{K1, V1} -> {K2, List<V2>} -> {K3, V3}`

最后，希望越来越多的开发者加入到学习Hadoop的大潮中，用大数据分析来改善人类的生活。

参考文档：　[太多选择——如何挑选合适的大数据或Hadoop平台?](http://www.infoq.com/cn/articles/BigDataPlatform)
