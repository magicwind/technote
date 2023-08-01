---
layout: post
title:  "在AutoLayout下动态调整TextView的高度"
date:   2014-07-28 23:02:04
categories: iOS
---

在开启了AutoLayout的Story Board和xib中，如果需要动态调整UITextView的高度的话，需要一些小技巧。方法如下：

1.  禁用UITextView的滚动。

    两种方法： 1) 在Story Board或xib里取消钩选`scrolling enabled`。 2) 在代码中设置`[TextView setScrollEnabled:NO];`。

2.  创建一个UITextView并连接到IBOutlet textView(CTRL+拖拽控件到m文件)。

3.  创建一个临时的UITextView的高度约束，设置约束的值为默认高度，再连接到IBOutlet textViewHeightConstraint。

4.  当你向UITextView设置文本内容后，你需要先计算UITextView的内容高度再将该高度设置为高度约束的值。

示例代码如下：

{% highlight objective-c %}
[self.textView setText:song.lyrics];

CGSize sizeThatFitsTextView = [self.textView sizeThatFits:CGSizeMake(TextView.frame.size.width, MAXFLOAT)];

self.textViewHeightConstraint.constant = ceilf(sizeThatFitsTextView.height); 
{% endhighlight %}

测试环境：　iOS 7.1.2, Xcode 5.1.1

参考文档：　[AutoLayout with Dynamic UITextView height](http://imnotyourson.com/autolayout-with-dynamic-uitextview-height/)
