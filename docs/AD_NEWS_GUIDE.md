# 广告行业新闻管理系统

## 概述

这是一个用于收集、整理和发布每日广告行业新闻的自动化系统。新闻文章会被发布到 Jekyll 博客，并自动同步到 GitHub Pages。

## 快速开始

### 1. 添加新闻

最简单的方式：

```bash
cd /home/ubuntu/.openclaw/workspace/technote
python3 scripts/ad_news.py add "新闻标题" "新闻内容"
```

### 2. 推送到 GitHub

添加新闻后，系统会自动提交到本地 Git。你需要手动推送或使用 `--push` 参数：

```bash
# 方式1：手动推送
cd /home/ubuntu/.openclaw/workspace/technote
git push origin main

# 方式2：添加时自动推送
python3 scripts/ad_news.py add "标题" "内容" --push
```

## 详细使用

### Python 工具 (推荐)

**基本用法：**
```bash
python3 scripts/ad_news.py add "标题" "内容"
```

**带标签：**
```bash
python3 scripts/ad_news.py add "标题" "内容" -t "AI,广告技术,营销"
```

**自动推送：**
```bash
python3 scripts/ad_news.py add "标题" "内容" --push
```

**列出最近文章：**
```bash
python3 scripts/ad_news.py list        # 默认10篇
python3 scripts/ad_news.py list -n 20  # 指定数量
```

**查看帮助：**
```bash
python3 scripts/ad_news.py --help
python3 scripts/ad_news.py add --help
```

### Bash 脚本

```bash
./scripts/add_ad_news.sh "标题" "内容" "标签1,标签2"
```

## 文章格式

每篇文章会自动生成以下格式：

```markdown
---
layout: post
title:  "文章标题"
date:   2026-02-10 05:28:17 +0800
categories: ad-news
---

文章内容...

---
*来源: 每日广告行业观察*  
*发布时间: 2026-02-10*
```

## 文件结构

```
technote/
├── _posts/                    # 文章目录
│   └── YYYY-MM-DD-slug.md    # 文章文件
├── scripts/                   # 脚本目录
│   ├── ad_news.py            # Python 工具
│   └── add_ad_news.sh        # Bash 脚本
└── docs/
    └── AD_NEWS_GUIDE.md      # 本文档
```

## 工作流程

1. **收集新闻** - 从各种来源收集广告行业新闻
2. **创建文章** - 使用工具创建 Jekyll 格式的文章
3. **本地提交** - 自动提交到本地 Git 仓库
4. **推送远程** - 推送到 GitHub
5. **自动发布** - GitHub Pages 自动构建并发布

## 标签建议

常用标签：
- `ad-news` - 广告行业新闻（默认）
- `ad-tech` - 广告技术
- `marketing` - 营销
- `privacy` - 隐私保护
- `AI` - 人工智能
- `data` - 数据分析
- `programmatic` - 程序化广告
- `social-media` - 社交媒体

使用逗号分隔多个标签：`"AI,ad-tech,marketing"`

## 示例

### 示例 1：简单新闻

```bash
python3 scripts/ad_news.py add \
  "Google Ads 推出新的隐私功能" \
  "Google 今日宣布在 Google Ads 平台推出新的隐私保护功能，帮助广告主在遵守 GDPR 的同时优化广告投放效果。"
```

### 示例 2：详细文章

```bash
python3 scripts/ad_news.py add \
  "2026年程序化广告趋势报告" \
  "根据最新发布的行业报告，2026年程序化广告市场将呈现以下趋势：

1. **AI驱动优化** - 机器学习算法将更深入地应用于广告投放优化
2. **隐私优先** - 无Cookie解决方案成为主流
3. **视频广告增长** - 视频广告支出预计增长35%
4. **零售媒体崛起** - 零售媒体网络成为新的增长点

这些趋势将重塑整个广告行业的格局。" \
  -t "programmatic,ad-tech,trends" \
  --push
```

### 示例 3：公司动态

```bash
python3 scripts/ad_news.py add \
  "Meta 推出 Advantage+ 购物广告增强功能" \
  "Meta 今日宣布对其 Advantage+ 购物广告产品进行重大升级，新增了以下功能：
  
- 自动化创意生成
- 智能预算分配
- 跨平台归因优化
- 实时效果监测

这些功能将帮助电商广告主提升ROI最多可达40%。" \
  -t "social-media,e-commerce,AI"
```

## 注意事项

1. **内容质量** - 确保新闻内容准确、有价值
2. **标题清晰** - 使用简洁明了的标题
3. **标签一致** - 保持标签使用的一致性
4. **及时推送** - 定期推送到 GitHub 以保持同步
5. **版权注意** - 注意新闻来源和版权问题

## 故障排除

### 推送失败

如果推送失败，检查：
1. SSH 密钥是否正确配置
2. 是否有网络连接
3. 是否有仓库的写权限

```bash
# 测试 SSH 连接
ssh -T git@github.com

# 查看 Git 状态
cd /home/ubuntu/.openclaw/workspace/technote
git status
```

### 文件名问题

如果标题包含特殊字符，系统会自动处理。纯中文标题会使用时间戳作为文件名。

## 自动化建议

可以结合 OpenClaw 的 cron 功能设置定时任务：

```bash
# 每天早上9点检查新闻
# 在 HEARTBEAT.md 或 cron 中配置
```

## 联系与支持

- 仓库：https://github.com/magicwind/technote
- 本地路径：/home/ubuntu/.openclaw/workspace/technote

---

*最后更新：2026-02-10*
