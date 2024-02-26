---
layout: post
title:  "[置顶]基于Amazon Bedrock的text2sql解决方案介绍"
date:   2099-01-01 00:00:00
categories: genai
---

## 什么是text2sql技术?

text2sql是一种自然语言理解技术,可以将用户用自然语言提出的问题自动转换成数据库查询语句。用户只需要用自然语言描述问题,text2sql系统就可以生成对应的SQL查询语句,从数据库中获取结果。这极大地简化了数据库查询的过程,用户无需了解SQL语法,就可以通过语音或文本进行数据分析和查询。

## 什么是Amazon Bedrock

Amazon Bedrock是一个无服务器的机器学习服务,可以帮助开发者快速构建自然语言理解应用。它内置了预训练好的语言模型,开发者可以通过简单的配置就获得强大的NLP能力,如命名实体识别、情感分析、文本分类等。Bedrock还提供了对话管理功能,可以帮助开发任务型对话机器人。

## 用户使用场景

1. 面向运营人员的销售数据分析, 根据数据库里的销售明细数据,按照时间、产品、地区、客户等维度分析销售额、利润等指标。例如,运营人员可以通过语音提问“上个月北京地区笔记本电脑的销售额是多少?”,text2sql系统即可自动生成SQL语句,从数据库提取上个月北京地区笔记本电脑的销售总额。

2. 面向销售人员的绩效数据查询, 根据SFE数据库里的销售数据,分析销售个人或者团队的绩效达成情况。例如,销售人员可以通过语音提问“我这个月的销售业绩完成率是多少?”,text2sql系统可以自动统计出该销售人员本月的销售目标和实际完成数,计算出销售业绩完成率。

## 解决方案特点

1. 利用最先进的闭源和开源LLM来生成SQL,API调用按Token数量进行计费,没有任何运行时开销。这可以确保生成的SQL语句语义正确、符合业务逻辑,而且计费方式灵活。

2. 利用AWS托管服务来减少运维开销,例如使用Amazon EC2提供可靠的计算资源,使用Amazon RDS来托管关系数据库。开发者无需管理基础设施,可以更专注于应用开发。

3. 使用IaC工具编写代码来初始化和更新基础架构,实现自动化部署,提高敏捷性。开发者可以使用AWS CloudFormation, AWS CDK等IaC工具,通过代码控制基础架构的部署和更新。

## 用户体验

1. 提供Web UI供业务用户进行聊天式数据查询。用户无需了解SQL语法,通过聊天界面输入问题,即可获取结果,操作非常简单方便。

2. 提供后台配置界面供模型调优人员进行配置。模型调优人员可以通过友好的界面管理数据库Schema标注、管理向量Embedding数据等,无需修改代码即可优化对话效果。

## 更多技术细节参考

[使用 Bedrock 和 RAG 构建 Text2SQL 行业数据查询助手](https://aws.amazon.com/cn/blogs/china/build-text2sql-industry-data-query-assistant-using-bedrock-and-rag/)

[浅谈 LLM RAG 对话机器人和 Text2SQL 的设计和实现](https://aws.amazon.com/cn/blogs/china/design-and-implementation-of-llm-rag-conversational-robot-and-text2sql/)

## 代码参考

[Guidance for Natural Language Queries of Relational Databases on AWS](https://github.com/aws-solutions-library-samples/guidance-for-natural-language-queries-of-relational-databases-on-aws)
