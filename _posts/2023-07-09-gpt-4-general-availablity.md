---
layout: post
title:  "GPT-4 API正式发布和Completions API中废弃了旧模型"
categories: gpt
---

GPT-3.5 Turbo，DALL·E和Whisper API也已发布，我们正在发布Completions API的旧模型的废弃计划，这些模型将在2024年初退役。

从今天开始，所有付费API客户都可以访问GPT-4。在3月，我们推出了ChatGPT API，而在本月初，我们发布了对基于聊天的模型的第一次更新。我们设想未来基于聊天的模型可以支持任何用例。今天，我们正在宣布对Completions API的旧模型的废弃计划，并建议用户采用Chat Completions API。

## GPT-4 API普遍可用性

GPT-4是我们最有能力的模型。自3月以来，数百万开发者已经请求访问GPT-4 API，而利用GPT-4的创新产品的范围每天都在增长。今天，所有现有的有成功支付历史的API开发者都可以访问具有8K上下文的GPT-4 API。我们计划在本月底向新开发者开放访问权限，然后根据计算可用性开始提高速率限制。

基于这些模型对生产规模使用的稳定性和准备情况，我们还将GPT-3.5 Turbo，DALL·E和Whisper API普遍可用。我们正在努力为GPT-4和GPT-3.5 Turbo安全地启用微调，并期望今年晚些时候提供此功能。

## 从文本补全转向聊天补全

我们在3月引入了Chat Completions API，现在它占据了我们API GPT使用的97%。

最初的Completions API是在2020年6月引入的，用于提供与我们的语言模型交互的自由形式文本提示。我们已经了解到，我们通常可以通过更结构化的提示接口提供更好的结果。基于聊天的范式已被证明是强大的，能够处理大多数以前的用例和新的对话需求，同时提供更高的灵活性和特异性。特别是，Chat Completions API的结构化接口（例如，系统消息，函数调用）和多轮对话能力使开发者能够构建对话体验和广泛的完成任务。它还有助于降低提示注入攻击的风险，因为用户提供的内容可以从指令中结构化地分离出来。

*文本总结* 
```
系统(System)
将此消息总结为最多10个字。

用户(User)
木星是太阳系中离太阳第五远和最大的行星。它是一个气体巨大行星，质量是太阳的千分之一，但是是太阳系中所有其他行星总和的两倍半。木星是夜空中肉眼可见的最亮的物体之一，自记录历史以前就为古代文明所知。它以罗马神木星命名。从地球上看，木星可以足够明亮，以至于其反射的光可以投射出可见的阴影，平均而言，它是夜空中继月亮和金星之后的第三亮的自然物体。

助手(Assistant)
木星：最大的行星，夜晚肉眼可见。
```

*代码完成*
```
System
Complete the following code.

User
def fibonacci(num):

Assistant
if num == 0:
    return 0
elif num == 1:
    return 1
else:
    fib = [0, 1]
    for i in range(2, num + 1):
          fib.append(fib[i-1] + fib[i-2])
    return fib[num]
```

*Few-shot learning*
```
System
You translate corporate jargon into plain English.

User
New synergies will help drive top-line growth.

Assistant
Working well together will make more money.

User
Let’s circle back when we have more bandwidth to touch base on opportunities for increased leverage.

Assistant
When we’re less busy, let’s talk about how to do better.

User
This late pivot means we don’t have time to boil the ocean for the client deliverable.

Assistant
Because of this sudden change, we don’t have enough time to complete the entire project for the client.
```

我们计划继续投入大部分平台努力在这个方向，因为我们相信它将为开发者提供越来越有能力和易于使用的体验。我们正在努力快速关闭Chat Completions API的最后几个剩余的缺口，例如完成令牌的对数概率和增加可操纵性以减少响应的“聊天性”。

## 废弃Completions API中的旧模型

作为我们在Chat Completions API中增加投资和我们优化计算能力的努力的一部分，6个月后，我们将退役使用Completions API的一些旧模型。虽然这个API将保持可访问，但我们将从今天开始在我们的开发者文档中将其标记为“遗留”。我们计划将未来的模型和产品改进集中在Chat Completions API上，并且没有计划公开发布使用Completions API的新模型。

从2024年1月4日开始，旧的完成模型将不再可用，并将被以下模型替换：
```
旧模型                 新模型
ada                   ada-002
babbage               babbage-002
curie                 curie-002
davinci               davinci-002

davinci-instruct-bete
curie-instruct-beta
text-ada-001
text-babbage-001
text-curie-001
text-davinci-001
text-davinci-002
text-davinci-003
--> gpt-3.5-turbo-instruct
```
使用基础GPT-3模型的稳定模型名称（ada，babbage，curie，davinci）的应用程序将在2024年1月4日自动升级到上面列出的新模型。在未来几周内，通过在API调用中指定以下模型名称，新模型也将可供早期测试：ada-002，babbage-002，curie-002，davinci-002。

使用其他旧完成模型（如text-davinci-003）的开发者将需要在2024年1月4日之前手动升级他们的集成，通过在他们的API请求的“模型”参数中指定gpt-3.5-turbo-instruct。gpt-3.5-turbo-instruct是一个InstructGPT风格的模型，训练方式类似于text-davinci-003。这个新模型是Completions API中的替换模型，并将在未来几周内可供早期测试。

希望在2024年1月4日之后继续使用他们的微调模型的开发者将需要在新的基础GPT-3模型（ada-002，babbage-002，curie-002，davinci-002）或新模型（gpt-3.5-turbo，gpt-4）上微调替代模型。一旦今年晚些时候提供了这个功能，我们将给予以前微调过旧模型的用户GPT-3.5 Turbo和GPT-4微调的优先访问权。我们承认，迁移离基于您自己数据的微调模型是具有挑战性的。我们将为以前微调过模型的用户提供支持，使这个过渡尽可能顺利。
在未来几周内，我们将联系最近使用过这些旧模型的开发者，并在新的完成模型准备好进行早期测试后提供更多信息。

## 废弃旧的嵌入模型

旧的嵌入模型的用户（例如，text-search-davinci-doc-001）将需要在2024年1月4日之前迁移到text-embedding-ada-002。我们在2022年12月发布了text-embedding-ada-002，并发现它比以前的模型更有能力和成本效益。今天，text-embedding-ada-002占据了所有嵌入API使用的99.9%。

我们认识到这对使用那些旧模型的开发者来说是一个重大的改变。我们并不轻易做出淘汰这些模型的决定。我们将承担用户使用这些新模型重新嵌入内容的财务成本。我们将在未来几天内与受影响的用户取得联系。

旧模型
```
code-search-ada-code-001
code-search-ada-text-001	
code-search-babbage-code-001	
code-search-babbage-text-001	
text-search-ada-doc-001	
text-search-ada-query-001	
text-search-babbage-doc-001	
text-search-babbage-query-001	
text-search-curie-doc-001	
text-search-curie-query-001	
text-search-davinci-doc-001	
text-search-davinci-query-001	
text-similarity-ada-001	
text-similarity-babbage-001	
text-similarity-curie-001	
text-similarity-davinci-001
```
新模型
text-embedding-ada-002

## 废弃Edits API
Edits API及其关联模型的用户（例如，text-davinci-edit-001或code-davinci-edit-001）将需要在2024年1月4日之前迁移到GPT-3.5 Turbo。Edits API beta是一个早期的探索性API，旨在使开发者能够根据指令返回提示的编辑版本。我们在开发gpt-3.5-turbo和Chat Completions API时考虑了来自Edits API的反馈，现在可以用于同样的目的。

```
System
Apply the change requested by the user to the code.

User
def fibonacci(num):
    if num <= 1:
        return num
    else:
        return fibonacci(num-1) + fibonacci(num-2)
print(fibonacci(10))

User
Rename the function to fib.

Assistant
def fib(num):
    if num <= 1:
        return num
    else:
        return fib(num-1) + fib(num-2)
print(fib(10))
```