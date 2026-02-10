#!/bin/bash
# 添加广告行业新闻的脚本
# 使用方法: ./add_ad_news.sh "标题" "内容" ["标签1,标签2"]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
POSTS_DIR="$REPO_DIR/_posts"

# 检查参数
if [ $# -lt 2 ]; then
    echo "使用方法: $0 \"标题\" \"内容\" [\"标签1,标签2\"]"
    echo "示例: $0 \"OpenAI发布新产品\" \"今日OpenAI宣布...\" \"AI,广告技术\""
    exit 1
fi

TITLE="$1"
CONTENT="$2"
TAGS="${3:-ad-news}"

# 生成日期和文件名
DATE=$(date +%Y-%m-%d)
TIME=$(date +%H:%M:%S)
SLUG=$(echo "$TITLE" | iconv -t ascii//TRANSLIT | sed -r 's/[^a-zA-Z0-9]+/-/g' | sed -r 's/^-+\|-+$//g' | tr A-Z a-z)
FILENAME="${DATE}-${SLUG}.md"
FILEPATH="${POSTS_DIR}/${FILENAME}"

# 创建文章
cat > "$FILEPATH" << EOF
---
layout: post
title:  "${TITLE}"
date:   ${DATE} ${TIME} +0800
categories: ${TAGS}
---

${CONTENT}

---
*来源: 每日广告行业观察*
*发布时间: ${DATE}*
EOF

echo "✅ 新闻文章已创建: ${FILENAME}"
echo "📁 位置: ${FILEPATH}"

# Git 操作
cd "$REPO_DIR"

# 配置 git（如果需要）
git config user.name "Ad News Bot" 2>/dev/null || true
git config user.email "bot@technote.local" 2>/dev/null || true

# 添加并提交
git add "$FILEPATH"
git commit -m "Add ad news: ${TITLE}"

echo "📝 已提交到本地 Git"
echo ""
echo "💡 使用以下命令推送到 GitHub:"
echo "   cd $REPO_DIR && git push origin master"
