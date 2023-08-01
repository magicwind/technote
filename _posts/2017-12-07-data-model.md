---
layout: post
title:  "数据仓库的数据模型设计"
categories: analytics
---

## 目的
设计数据模型是数仓搭建中的一个重要环节，本文主要介绍工具和基本概念。

## 工具

主要使用Navicat Data Modeler，有基本版可以免费无期限的试用。

## 方法

数据模型主要可以分为三个层次：概念模型，逻辑模型，物理模型。概念模型是最抽象的，物理模型是最具体的。一般的设计是遵循从抽象到具体的过程。

一般设计流程是，先在纸上进行概念模型设计，然后在电脑上完成逻辑模型设计，最后由工具生成特定数据库的物理模型。

<table border="1" class="listing" cellpaddiing="6" cellspacing="0">
<tbody>
<tr><td>Feature</td><td>Conceptual</td><td>Logical</td><td>Physical</td></tr>
<tr><td>Entity Names</td><td><center>✓</center></td><td><center>✓</center></td><td> &nbsp; </td></tr>
<tr><td>Entity Relationships</td><td><center>✓</center></td><td><center>✓</center></td><td> &nbsp; </td></tr>
<tr><td>Attributes</td><td> &nbsp; </td><td><center>✓</center></td><td> &nbsp; </td></tr>
<tr><td>Primary Keys</td><td> &nbsp; </td><td><center>✓</center></td><td><center>✓</center></td></tr>
<tr><td>Foreign Keys</td><td> &nbsp; </td><td><center>✓</center></td><td><center>✓</center></td></tr>
<tr><td>Table Names</td><td> &nbsp; </td><td> &nbsp; </td><td><center>✓</center></td></tr>
<tr><td>Column Names</td><td> &nbsp; </td><td> &nbsp; </td><td><center>✓</center></td></tr>
<tr><td>Column Data Types</td><td> &nbsp; </td><td> &nbsp; </td><td><center>✓</center></td></tr>
</tbody>
</table>

### 概念模型
可以快速的在纸上设计和修改。概念模型来源于业务需求，实体和关系的设计主要考虑业务需要，这个阶段无需考虑数据库设计。

特点：
1. 高度抽象
2. 容易理解
3. 容易改进
4. 只有实体和抽象的关系

### 逻辑模型
主要设计工作是定义实体的主键和外键关系。

特点：
1. 实体有了属性
2. 定义了关键属性和一般属性
3. 定义了主键和外键关系
4. 比起概念模型，它定义更多细节
5. 属性名可读性强，比如可以叫做Production Description。

### 物理模型
需要根据数据库的特点来设计和优化，一般可以使用工具将逻辑模型转化成物理模型。还需要根据数据的特点来定义字段类型和索引等等。

特点：
1. 实体变成了数据库表
2. 属性变成了列名
3. 表名是符合数据库要求的
4. 列名也是符合数据库要求的
5. 数据类型是数据库特定的
6. 用户较难理解
7. 修改起来比逻辑模型更难
8. 可以包含索引、约束等对象

