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
import json

REPO_DIR = Path(__file__).parent.parent
POSTS_DIR = REPO_DIR / "_posts"


def slugify(text):
    """将中文或英文标题转换为 URL 友好的 slug"""
    # 移除特殊字符，保留字母数字和连字符
    text = re.sub(r'[^\w\s-]', '', text.lower())
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')[:100]  # 限制长度


def generate_title_with_ai(content):
    """使用 AI 根据内容生成吸引人的标题"""
    try:
        from datetime import datetime
        
        # 移除测试相关文字
        content = re.sub(r'测试\d*[:：]?\s*', '', content)
        
        # 使用正则表达式提取关键信息
        # 提取公司名、产品名、数字等关键元素
        
        # 常见的广告营销关键词
        keywords = []
        
        # 提取公司名称
        companies = re.findall(r'(谷歌|Google|Meta|Facebook|亚马逊|Amazon|OpenAI|微软|Microsoft|苹果|Apple|腾讯|阿里巴巴|Alibaba|字节跳动|ByteDance|百度|Baidu|TikTok|Instagram|YouTube)', content)
        if companies:
            keywords.append(companies[0])
        
        # 提取关键动词
        actions = re.findall(r'(推出|发布|宣布|启动|上线|升级|革新|展示|测试|应用)', content[:200])
        if actions and actions[0] != '测试':
            keywords.append(actions[0])
        
        # 提取产品类型关键词
        products = re.findall(r'(AI广告|AR广告|视频广告|展示广告|搜索广告|信息流广告|程序化广告|AI|人工智能|机器学习|AR|VR|平台|广告|营销|技术|解决方案|工具|系统|产品|服务)', content[:300])
        if products:
            # 优先选择更具体的词
            for p in products:
                if len(p) > 2:
                    keywords.append(p)
                    break
            else:
                keywords.append(products[0])
        
        # 提取数字亮点
        numbers = re.findall(r'(\d+%|\d+倍)', content)
        if numbers:
            keywords.append(f"提升{numbers[0]}")
        
        # 生成标题
        if len(keywords) >= 2:
            # 有足够的关键词，组合生成标题
            patterns = [
                f"{keywords[0]}{keywords[1]}{keywords[2] if len(keywords) > 2 else ''}",
                f"{keywords[0]}：{keywords[1]}{keywords[2] if len(keywords) > 2 else ''}新突破",
                f"{keywords[0]}{keywords[1]}，{keywords[2] if len(keywords) > 2 else '行业震动'}"
            ]
            
            # 使用日期作为种子保证每天不同
            pattern_index = datetime.now().day % len(patterns)
            title = patterns[pattern_index]
            
        else:
            # 关键词不足，使用通用模板
            date_suffix = datetime.now().strftime("%m月%d日")
            templates = [
                f"广告营销行业动态 {date_suffix}",
                f"今日营销科技看点 {date_suffix}",
                f"广告技术前沿 {date_suffix}"
            ]
            title = templates[datetime.now().day % len(templates)]
        
        # 限制长度
        if len(title) > 30:
            title = title[:27] + "..."
        
        print(f"🤖 生成的标题: {title}")
        return title
        
    except Exception as e:
        print(f"⚠️  标题生成失败: {e}")
        # 返回默认标题
        from datetime import datetime
        return f"广告营销资讯 {datetime.now().strftime('%m.%d')}"


def add_news(title, content, tags="ad-news", auto_push=False, auto_title=False):
    """添加新闻文章"""
    
    # 如果启用自动生成标题
    if auto_title:
        ai_title = generate_title_with_ai(content)
        if ai_title:
            title = ai_title
    
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
  # 添加新闻（自动生成标题）
  %(prog)s add "今日OpenAI宣布推出新的广告产品..."
  
  # 添加新闻并自动推送
  %(prog)s add "今日广告行业的重大新闻是..." --push
  
  # 使用自定义标题（不使用AI生成）
  %(prog)s add "我的标题" "新闻内容" --no-auto-title
  
  # 添加新闻并指定标签
  %(prog)s add "新闻内容" -t "AI,广告技术,新闻"
  
  # 列出最近的文章
  %(prog)s list
  
  # 列出最近20篇文章
  %(prog)s list -n 20
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # add 命令
    add_parser = subparsers.add_parser('add', help='添加新闻文章')
    add_parser.add_argument('title', nargs='?', default='AUTO', help='新闻标题（默认: 自动生成）')
    add_parser.add_argument('content', help='新闻内容')
    add_parser.add_argument('-t', '--tags', default='ad-news', 
                           help='标签（逗号分隔，默认: ad-news）')
    add_parser.add_argument('--push', action='store_true', 
                           help='自动推送到 GitHub')
    add_parser.add_argument('--no-auto-title', action='store_true',
                           help='禁用自动生成标题（使用指定的标题）')
    
    # list 命令
    list_parser = subparsers.add_parser('list', help='列出最近的文章')
    list_parser.add_argument('-n', '--number', type=int, default=10,
                            help='显示数量（默认: 10）')
    
    args = parser.parse_args()
    
    if args.command == 'add':
        # 确定是否使用自动生成标题
        auto_title = (args.title == 'AUTO') or (not args.no_auto_title)
        title = args.title if args.title != 'AUTO' else '临时标题'
        add_news(title, args.content, args.tags, args.push, auto_title)
    elif args.command == 'list':
        list_news(args.number)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
