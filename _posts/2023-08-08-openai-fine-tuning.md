---
layout: post
title:  "如何微调大模型?"
categories: openai
---

# 微调
学习如何为您的应用定制模型。

## 简介
微调使您通过提供以下功能从API可用的模型中获得更多优势：
1. 比提示设计更高质量的结果
2. 能够在提示中容纳的示例之外进行训练
3. 由于提示较短而节省令牌
4. 请求延迟更低

GPT-3已在开放互联网上的大量文本上进行了预训练。当给出一个只有几个例子的提示时，它通常可以直观地了解您试图执行的任务，并生成一个合理的完成。这通常被称为“少数样本学习”。

通过在提示中容纳的许多更多示例上训练，微调改善了少数样本学习，让您在许多任务上取得更好的效果。一旦模型被微调，您将不再需要在提示中提供示例。这节省了成本，并实现了更低延迟的请求。

从高层次来看，微调涉及以下步骤：

1. 准备和上传训练数据
2. 训练一个新的微调模型
3. 使用您的微调模型

## 哪些模型可以进行微调？

微调目前仅适用于以下基本模型：davinci、curie、babbage和ada。这些是不进行任何指令后训练的原始模型（例如text-davinci-003）。您还可以继续微调一个已经微调过模型，以添加额外的数据，而无需从头开始。

## 安装
我们推荐使用OpenAI的命令行界面（CLI）。要安装它，请运行

`pip install --upgrade openai`

（以下指令适用于0.9.4及更高版本。此外，OpenAI CLI需要python 3。）

通过在您的shell初始化脚本（例如.bashrc、zshrc等）中添加以下行或在微调命令之前在命令行中运行它，设置您的OPENAI_API_KEY环境变量：

```bash
export OPENAI_API_KEY="<OPENAI_API_KEY>"
```

## 准备训练数据

训练数据是您教GPT-3您想让它说什么的方式。

您的数据必须是JSONL文档，其中每一行都是一个提示完成对，对应一个训练示例。您可以使用我们的CLI数据准备工具轻松将您的数据转换为此文件格式。
```jsonl
{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
...
```
为微调设计您的提示和完成与为我们的基本模型（Davinci、Curie、Babbage、Ada）使用设计您的提示不同。特别是，虽然基本模型的提示通常包括多个示例（“少数样本学习”），但对于微调，每个训练示例通常由单个输入示例及其关联输出组成，无需给出详细指令或在同一提示中包括多个示例。

有关如何为各种任务准备训练数据的更详细指导，请参考我们[准备数据集](https://platform.openai.com/docs/guides/fine-tuning/preparing-your-dataset)的最佳实践。

您拥有的训练示例越多越好。我们建议至少有几百个示例。总的来说，我们发现数据集大小每增加一倍都会导致模型质量的线性提高。

### CLI数据准备工具

我们开发了一个工具，用于验证、提供建议并重新格式化您的数据：

`openai tools fine_tunes.prepare_data -f <LOCAL_FILE>`

此工具接受不同的格式，唯一的要求是它们必须包含提示和完成列/键。您可以传递**CSV、TSV、XLSX、JSON**或**JSONL**文件，它将在引导您完成建议更改的过程后将输出保存为准备进行微调的JSONL文件。

## 创建一个微调模型

以下假设您已经按照上述指导准备了训练数据。

使用OpenAI CLI开始您的微调工作：

`openai api fine_tunes.create -t <TRAIN_FILE_ID_OR_PATH> -m <BASE_MODEL>`

其中BASE_MODEL是您开始的基本模型的名称（ada、babbage、curie或davinci）。您可以使用[后缀参数](https://platform.openai.com/docs/guides/fine-tuning/customize-your-model-name)自定义微调模型的名称。

执行上述命令会做几件事情：

1. 使用files API上传文件（或使用已经上传的文件）
2. 创建微调作业
3. 流式传输事件，直到工作完成（这通常需要几分钟，但如果队列中有很多工作或您的数据集很大，则可能需要几小时）

每个微调工作都是从基本模型开始的，默认为curie。模型的选择会影响模型的性能和运行微调模型的成本。您的模型可以是：ada、babbage、curie或davinci。

在您开始微调作业后，可能需要一些时间才能完成。您的工作可能会排在我们系统上的其他工作之后，根据模型和数据集的大小，训练我们的模型可能需要几分钟或几小时。如果由于任何原因事件流被中断，您可以通过运行以下命令恢复它：

`openai api fine_tunes.follow -i <YOUR_FINE_TUNE_JOB_ID>`

当工作完成时，它应显示微调模型的名称。

除了创建微调作业，您还可以列出现有作业，检索作业状态或取消作业。

```
# 列出所有创建的微调
openai api fine_tunes.list

# 检索微调的状态。结果对象包括
# 工作状态（可能是pending、running、succeeded或failed之一）
# 和其他信息
openai api fine_tunes.get -i <YOUR_FINE_TUNE_JOB_ID>

# 取消工作
openai api fine_tunes.cancel -i <YOUR_FINE_TUNE_JOB_ID>
```

## 使用微调模型
当工作成功后，fine_tuned_model字段将填充模型的名称。您现在可以将此模型指定为我们的Completions API的参数，并使用Playground向其发出请求。

在您的工作首次完成后，您的模型可能需要几分钟才能准备好处理请求。如果对您的模型的完成请求超时，可能是因为您的模型仍在加载。如果发生这种情况，请在几分钟后重试。

您可以通过将模型名称作为完成请求的model参数传递来开始发出请求：

OpenAI CLI:

```
openai api completions.create -m <FINE_TUNED_MODEL> -p <YOUR_PROMPT>
```

cURL:
```curl
curl https://api.openai.com/v1/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": YOUR_PROMPT, "model": FINE_TUNED_MODEL}'
```

Python:
```python
import openai
openai.Completion.create(
    model=FINE_TUNED_MODEL,
    prompt=YOUR_PROMPT)
```

Node.js:
```nodejs
const response = await openai.createCompletion({
  model: FINE_TUNED_MODEL
  prompt: YOUR_PROMPT,
});
```

您可以继续在这些针对微调模型的请求上使用所有其他[Completions](https://platform.openai.com/docs/api-reference/completions)参数，例如temperature、frequency_penalty、presence_penalty等。

## 删除微调模型

要删除一个微调模型，您必须被指定为您组织内的“所有者”。

OpenAI CLI:
```
openai api models.delete -i <FINE_TUNED_MODEL>
```

cURL:
```
curl -X "DELETE" https://api.openai.com/v1/models/<FINE_TUNED_MODEL> \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

Python:
```
import openai
openai.Model.delete(FINE_TUNED_MODEL)
```

# 准备您的数据集

微调是一种强大的技术，用于创建特定于您用例的新模型。**在微调模型之前，我们强烈建议阅读以下您用例的最佳实践和具体指导方针。**

## 数据格式化

要微调模型，您需要一组训练示例，每个示例都由单个输入（“提示”）和其关联输出（“完成”）组成。这与使用我们的基本模型显著不同，在那里您可能在单个提示中输入详细说明或多个示例。

  - 每个提示应以固定分隔符结尾，以通知模型提示何时结束，完成何时开始。通常效果良好的简单分隔符是`\n\n###\n\n`。分隔符不应出现在任何提示的其他地方。

  - 由于我们的标记化，每个完成应以空格开始，这将大多数单词与前导空格标记化。

  - 每个完成都应以固定的停止序列结尾，以通知模型完成何时结束。停止序列可以是`\n`、`###`或任何不出现在任何完成中的其他令牌。

  - 对于推断，您应该以与创建训练数据集时相同的方式格式化提示，包括相同的分隔符。还要指定相同的停止序列以正确截断完成。

## 一般最佳实践

微调的性能随着更多高质量示例的增加而提高。要微调一个比使用我们的基本模型与高质量提示的表现更好的模型，您应该提供至少几百个高质量示例，理想情况下由人类专家审核。从那里开始，性能倾向于随着示例数量加倍而线性增加。增加示例数量通常是提高性能的最佳和最可靠的方法。

分类器是最容易上手的模型。对于分类问题，我们建议使用ada，该模型通常倾向于在微调后的性能只比更有能力的模型稍差一点，同时速度明显更快且更便宜。

如果您是在现有数据集上微调而不是从头开始编写提示，请务必人工审查数据以排除冒犯或不准确的内容（如果可能的话），或者尽可能审查数据集的许多随机样本（如果数据集很大）。

(未完待续)
