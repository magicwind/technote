---
layout: post
title:  "五分钟看懂ES6的Generator新特性"
categories: javascript
---
## Generator的作用
generator是ES6规范引入的新特性，在最新版的Firefox和NodeJS 0.11版本已经提供了实现。
在我看，Generator主要提供以下新功能：
1. 可以更有效率的表示定长或者不定长度的数组。
2. 提供了一种中段函数执行的方法。

我们先来看个例子：
{% highlight javascript %}
function foo(x) {
    while(true) {
        x = x * 2;
        yield x;
    }
}
{% endhighlight %}
当你调用`foo`，会返回一个Generator对象。该对象有一个`next`方法。
{% highlight javascript %}
var g = foo(2);
g.next(); // -> 4
g.next(); // -> 8
g.next(); // -> 16
{% endhighlight %}
`yield`在程序里的作用就是中断函数执行，并返回yield后面的值。

当调用foo(2)后，`yield`后面的指变成4，直到next()执行后才返回。

然后继续执行while里的`x = x * 2`，`yield`后面的值变成8。剩下的以此类推。

可以看出foo函数表示的是一个以2为底的幂函数的集合，该集合长度没有限制。

一般不会直接调用next函数来取值，而采用新的语法`for of`像迭代器一样来使用Generator。
{% highlight javascript %}
for (var num of foo(5)) {
    // foo返回一个Generator，然后不断调用next()直到Generator停止。
    // ps: foo函数在这个例子里不会停止，这是一个特例。
}
{% endhighlight %}

当然一个函数中也可以出现多个yield关键字。看下面这个例子：
{% highlight javascript %}
function bar(x) {
    x++;
    var y = yield x;
    yield y/2;
}

var g = bar(1);
g.next(); // -> 2
g.send(8); // -> 4
{% endhighlight %}
执行`next`后，函数停在`var y = yield x;`，直到`send(8)`执行后，y被赋值成8，再返回8/2作为send的返回值。

可以发现，send的作用是先赋值再调用next。

## 语法
上面的例子可以运行在Firefox里，但是Generator正式的语法是在函数名前增加个星号。比如：`function *bar(x) {}`，但是把星号写在function后面也是允许的，个人建议前面一种写法，比较符合语法原意。

## Generator的应用
Generator在NodeJS的[co](https://github.com/tj/co)组件里得到了运用，可以避免过多的callback。

然后基于co，下一代的NodeJS Web框架[koa](https://github.com/koajs/koa)应运而生。
