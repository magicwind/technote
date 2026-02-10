# 广告行业新闻 - 快速参考

## 最常用命令

### 添加新闻（不推送）
```bash
cd /home/ubuntu/.openclaw/workspace/technote
python3 scripts/ad_news.py add "标题" "内容"
```

### 添加新闻（自动推送）
```bash
cd /home/ubuntu/.openclaw/workspace/technote
python3 scripts/ad_news.py add "标题" "内容" --push
```

### 添加带标签的新闻
```bash
python3 scripts/ad_news.py add "标题" "内容" -t "AI,广告技术"
```

### 列出最近文章
```bash
python3 scripts/ad_news.py list
```

### 手动推送
```bash
cd /home/ubuntu/.openclaw/workspace/technote
git push origin master
```

## 完整文档

详细使用指南：`/home/ubuntu/.openclaw/workspace/technote/docs/AD_NEWS_GUIDE.md`

---

*提示：使用 `python3 scripts/ad_news.py --help` 查看所有选项*
