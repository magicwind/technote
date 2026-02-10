#!/usr/bin/env python3
"""
广告行业新闻管理工具
用于添加、列出和管理 technote 仓库中的广告新闻文章
"""

import os
import sys
import argparse
from datetime import datetime
from pathlib import Path
import subprocess
import re

REPO_DIR = Path(__file__).parent.parent
POSTS_DIR = REPO_DIR / "_posts"


def slugify(text):
    """将中文或英文标题转换为 URL 友好的 slug"""
    # 移除特殊字符，保留字母数字和连字符
    text = re.sub(r'[^\w\s-]', '', text.lower())
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')[:100]  # 限制长度


def add_news(title, content, tags="ad-news", auto_push=False):
    """添加新闻文章"""
    
    # 生成文件名
    date_str = datetime.now().strftime("%Y-%m-%d")
    time_str = datetime.now().strftime("%H:%M:%S")
    slug = slugify(title)
    
    # 如果slug为空（纯中文标题），使用时间戳
    if not slug:
        slug = datetime.now().strftime("%H%M%S")
    
    filename = f"{date_str}-{slug}.md"
    filepath = POSTS_DIR / filename
    
    # 确保 _posts 目录存在
    POSTS_DIR.mkdir(exist_ok=True)
    
    # 生成文章内容
    post_content = f"""---
layout: post
title:  "{title}"
date:   {date_str} {time_str} +0800
categories: {tags}
---

{content}

---
*来源: 每日广告行业观察*  
*发布时间: {date_str}*
"""
    
    # 写入文件
    filepath.write_text(post_content, encoding='utf-8')
    print(f"✅ 新闻文章已创建: {filename}")
    print(f"📁 位置: {filepath}")
    
    # Git 操作
    try:
        os.chdir(REPO_DIR)
        
        # 配置 git
        subprocess.run(['git', 'config', 'user.name', 'Ad News Bot'], 
                      check=False, capture_output=True)
        subprocess.run(['git', 'config', 'user.email', 'bot@technote.local'], 
                      check=False, capture_output=True)
        
        # 添加文件
        subprocess.run(['git', 'add', str(filepath)], check=True)
        
        # 提交
        commit_msg = f"Add ad news: {title}"
        subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
        print(f"📝 已提交到本地 Git")
        
        # 推送（如果指定）
        if auto_push:
            result = subprocess.run(['git', 'push', 'origin', 'master'], 
                                   capture_output=True, text=True)
            if result.returncode == 0:
                print(f"🚀 已推送到 GitHub")
            else:
                print(f"⚠️  推送失败: {result.stderr}")
                print(f"💡 手动推送: cd {REPO_DIR} && git push origin master")
        else:
            print(f"\n💡 推送到 GitHub:")
            print(f"   cd {REPO_DIR} && git push origin master")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Git 操作失败: {e}")
        sys.exit(1)
    
    return filename


def list_news(limit=10):
    """列出最近的新闻文章"""
    posts = sorted(POSTS_DIR.glob("*.md"), reverse=True)
    
    print(f"\n📰 最近 {limit} 篇文章:")
    print("-" * 80)
    
    for i, post in enumerate(posts[:limit], 1):
        # 读取文件获取标题
        content = post.read_text(encoding='utf-8')
        title_match = re.search(r'^title:\s*"(.+)"', content, re.MULTILINE)
        title = title_match.group(1) if title_match else post.stem
        
        date_match = re.search(r'^date:\s*(.+)', content, re.MULTILINE)
        date = date_match.group(1) if date_match else "未知日期"
        
        print(f"{i}. [{post.name}]")
        print(f"   标题: {title}")
        print(f"   日期: {date}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description='广告行业新闻管理工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 添加新闻
  %(prog)s add "OpenAI发布新产品" "今日OpenAI宣布推出..."
  
  # 添加新闻并自动推送
  %(prog)s add "标题" "内容" --push
  
  # 添加新闻并指定标签
  %(prog)s add "标题" "内容" -t "AI,广告技术,新闻"
  
  # 列出最近的文章
  %(prog)s list
  
  # 列出最近20篇文章
  %(prog)s list -n 20
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # add 命令
    add_parser = subparsers.add_parser('add', help='添加新闻文章')
    add_parser.add_argument('title', help='新闻标题')
    add_parser.add_argument('content', help='新闻内容')
    add_parser.add_argument('-t', '--tags', default='ad-news', 
                           help='标签（逗号分隔，默认: ad-news）')
    add_parser.add_argument('--push', action='store_true', 
                           help='自动推送到 GitHub')
    
    # list 命令
    list_parser = subparsers.add_parser('list', help='列出最近的文章')
    list_parser.add_argument('-n', '--number', type=int, default=10,
                            help='显示数量（默认: 10）')
    
    args = parser.parse_args()
    
    if args.command == 'add':
        add_news(args.title, args.content, args.tags, args.push)
    elif args.command == 'list':
        list_news(args.number)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
