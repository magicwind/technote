---
layout: post
title:  "基于云的协作是广告技术后Cookie时代的救命稻草 – 但它能持续吗?"
categories: adtech
---

云基础设施供应商正在渗透到数据驱动的广告领域。

第三方广告技术公司正在成为使用公有云来构建解决方案的服务提供商 – 主要是亚马逊云科技 (AWS)、谷歌云平台 (GCP)、Snowflake 和微软 Azure。

这一趋势催生了数据Clean Room和Customer Data Platform等技术,对于许多大的广告主而言,在后Cookie时代需要将云服务纳入计划。

如果你问问云厂商自己,他们可能会称之为Daft Punk革命 – 更好、更快、更强大。但MarTech公司选择在云平台下构建业务的真正原因是用户隐私。

不过,问题依然存在:这种跨云协作系统能否在现实世界中发挥作用?也就是说,对营销人员是否有用,同时又能通过监管机构和隐私保护拥护者的审查。

用户隐私法律和平台数据政策侧重于限制可访问数据的业务数量,而不是禁止广告定位或归因等特定行为。这就是为什么苹果的ATT更新破坏了Facebook的广告平台,而亚马逊广告却在后疫情时代电商放缓的时期继续运营。Facebook需要其他企业共享数据,而亚马逊已经将数据集中到一个地方。

如果新的法规要求数据放在一个地方,那么供应商在那里开展业务就是唯一合乎逻辑的做法。

## 跨云协作实际上是如何实现的

一个挑战是,广告技术和数据供应商对技术有深入的理解,但客户往往没有。

去年,一位大饮料品牌的营销人员告诉我,她已经开始在The Trade Desk和沃尔玛的Connect DSP上运行多个广告系列（Campaign）,后者是基于The Trade Desk构建的。
她说,通过ID映射,品牌方可以将特定媒体渠道归因于沃尔玛的销售,并对沃尔玛的客户在访问其他商店或发布商时对其进行再营销。

等等!

这难道不是沃尔玛Connect DSP希望禁止的行为吗?

是的,的确如此。

基于云的用户定向和归因通常无法被审计,也无法增强品牌自身的客户数据。但从营销人员的角度来看,他们仍在使用熟悉的仪表板来采用常见策略。

例如,沃尔玛Connect DSP这样的围墙花园可能会生成一个人群包,可以在TikTok、Roku或Snapchat上对其进行再营销,然后促进购买转化。数据还可能被放入一个Clean Room,在那里ID可以在不暴露个人信息的情况下用于再营销。

作为跨云协作如何真实地运作的另一个例子,可以参考LiveRamp和亚马逊营销云(AMC),后者是由亚马逊广告运营的数据Clean Room。

2月,LiveRamp宣布与亚马逊建立合作伙伴关系,使得LiveRamp的ID解决方案RampID可以"用作将第一方和第三方见解与亚马逊广告在亚马逊营销云中的关联键,以实现测量,并直接在亚马逊DSP内基于RampID激活特定品牌的受众"。

如果你没有完全理解这些行业黑话,也不足为奇 - 而且如果你是营销人员,这种复杂性对你的日常工作影响相对较小。

品牌营销人员不需要知道模算数来解释两方如何能够通过计算得出一个和而不暴露公式中的数字。

对于LiveRamp和AMC来说,情况很复杂。他们不仅仅是像以前的数据上传那样匹配和增强个人资料。

亚马逊广告中加密的受众与RampID图中的加密实例相匹配。亚马逊DSP不知道它代表广告主中的哪个用户去重新定位 - 它只有一个加密的RampID。LiveRamp也不会得知是谁完成了购买,只知道总的转化数量。同时,广告主也不知道它重新定位了谁,也没有数据被添加到其第一方CRM系统中。

但用户级别的再营销和购买转化确实发生了。

广告技术就像一家精致的餐厅,至少目前还能在就餐区保持整洁和优雅,而把脏活累活留在厨房里。

## 潜在缺陷

但回到主要问题 - 跨云协作能否奏效?

好吧,事实是,它确实有效。就在我们谈话时,数十亿营销资金正通过这个系统流动。

然而,也有一些警示。

就在上周,由隐私研究员Wolfie Christl和Alan Toner合著的一份报告发现,LiveRamp有一个相当安全的加密和单向数据处理系统,但"在GDPR下,其中一些措施至少是可以质疑的"。

例如,LiveRamp的客户各有自己的RampID的伪匿名实例。这意味着一个为Hershey’s和Mondelez使用RampID的DSP或身份供应商无法跨客户比对数据。当代理商或广告技术公司代表多个品牌使用谷歌的基于云的数据清洗室Ads Data Hub时,谷歌也设置了类似的屏障。

然而,Christl和Toner指出,一些RampID客户本身就是数据经纪商、DSP 或 SSP,维护着自己的身份系统。他们将伪匿名的RampID整合到结果中,并将这些结果(有时甚至是特定受众)传递给其他客户。

LiveRamp的隐私措施旨在禁止广告主、广告技术公司或媒体重新识别个人。该报告确实承认LiveRamp在这方面做得很好。

但如果法律被解释为禁止跨不同数据库和公司关联个人数据呢?

没有什么能阻止欧洲数据保护机构追究这种解释。

根据一些品牌营销人员(和自夸的新闻稿),品牌可以跨越云基础设施服务和数字媒体平台跟踪和归因消费者ID,而每个平台本身据称都是一个独立的围墙花园。

这意味着协作软件公司应该尽快教育客户有关其隐私框架的工作方式。他们还应该避免过度吹牛。

因为基于云的广告技术是广告主实现后Cookie时代解决方案的最大的希望。但如果数据协作技术供应商存在漏洞的话,他们将成为下一个需要解决的问题。

原文：[Cloud-Based Collaboration Is Ad Tech’s Post-Cookie Lifeline – But Will It Last?](https://www.adexchanger.com/data-exchanges/cloud-based-collaboration-is-ad-techs-post-cookie-lifeline-but-will-it-last/)

## 更多参考

- [AWS Clean rooms介绍 ](https://aws.amazon.com/cn/clean-rooms/)
- [基于AWS Clean rooms的解决方案](https://aws.amazon.com/cn/solutions/advertising-marketing/data-clean-rooms/)
