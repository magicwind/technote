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


def generate_attractive_title(content, date_str):
    """根据文章内容生成吸引人的标题"""
    
    # 提取关键信息
    keywords = []
    
    # 提取公司/平台名称
    companies = re.findall(r'(谷歌|Meta|亚马逊|OpenTable|Grindr|微软|腾讯|百度|阿里|TikTok|YouTube|OpenAI|Anthropic)', content)
    if companies:
        keywords.append(companies[0])
    
    # 提取关键动词和动作
    actions = re.findall(r'(推出|发布|增长|暴增|进军|突破|颠覆|革命|引领|宣布)', content)
    
    # 提取数字亮点
    numbers = re.findall(r'(\d+%|\d+倍|\d+亿)', content)
    
    # 提取产品或概念
    products = re.findall(r'(CTV|AI广告|数字广告|AIGC|大模型|智能投放|AR广告|元宇宙|程序化|ROI)', content)
    
    # 根据星期几选择不同的标题模板
    day_of_week = datetime.strptime(date_str, "%Y-%m-%d").weekday()
    
    templates = [
        # 周一：数据驱动型
        lambda: f"{'、'.join(keywords[:2]) if len(keywords) >= 2 else (keywords[0] if keywords else '数字广告')}{'增长' if '增长' in actions or '暴增' in actions else '动态'}{': ' + numbers[0] if numbers else ''} | 广告营销周报",
        
        # 周二：行业趋势型
        lambda: f"{'、'.join(products[:2]) if len(products) >= 2 else (products[0] if products else 'AI技术')}重塑行业 | 本周营销观察",
        
        # 周三：公司动态型
        lambda: f"{keywords[0] if keywords else '科技巨头'}{''.join(actions[:1]) if actions else ''}{'新'.join(products[:1]) if products else '广告'} | 行业快讯",
        
        # 周四：数字型
        lambda: f"市场{numbers[0] if numbers else '增长'}！{'、'.join(keywords[:2]) if len(keywords) >= 2 else ''}本周热点",
        
        # 周五：综合型
        lambda: f"本周必读：{keywords[0] if keywords else '行业'}{'布局' if keywords else ''}{''.join(products[:1]) if products else '新领域'}",
        
        # 周六：创新型  
        lambda: f"{'AI' if 'AI' in content else '技术'}{'革命' if '革命' in content or '颠覆' in content else '创新'}：{keywords[0] if keywords else '广告'}行业新动向",
        
        # 周日：总结型
        lambda: f"一周精华：{keywords[0] if keywords else ''}{'、'.join(actions[:2]) if actions else '行业'}{'最新' if not actions else ''}动态"
    ]
    
    try:
        title = templates[day_of_week]()
        # 如果标题太短，使用备用方案
        if len(title) < 10:
            title = f"广告营销行业观察 {date_str}"
    except Exception as e:
        title = f"广告营销行业观察 {date_str}"
    
    return title


def slugify(text):
    """将中文或英文标题转换为 URL 友好的 slug"""
    # 移除特殊字符，保留字母数字和连字符
    text = re.sub(r'[^\w\s-]', '', text.lower())
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')[:100]  # 限制长度


def add_news(title_or_content, content=None, tags="ad-news", auto_push=False, auto_title=True):
    """
    添加新闻文章
    
    如果 auto_title=True 且只提供一个参数，则该参数为内容，标题自动生成
    如果 auto_title=False 或提供两个参数，第一个为标题，第二个为内容
    """
    
    # 生成文件名
    date_str = datetime.now().strftime("%Y-%m-%d")
    time_str = datetime.now().strftime("%H:%M:%S")
    
    # 判断参数模式
    if content is None:
        # 只提供了一个参数，作为内容处理
        actual_content = title_or_content
        if auto_title:
            actual_title = generate_attractive_title(actual_content, date_str)
            print(f"🤖 AI生成标题: {actual_title}")
        else:
            actual_title = f"广告营销行业观察 {date_str}"
    else:
        # 提供了两个参数
        if auto_title:
            actual_title = generate_attractive_title(content, date_str)
            print(f"🤖 AI生成标题: {actual_title}")
            print(f"   (忽略用户提供的标题: {title_or_content})")
            actual_content = content
        else:
            actual_title = title_or_content
            actual_content = content
    
    slug = slugify(actual_title)
    
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
title:  "{actual_title}"
date:   {date_str} {time_str} +0800
categories: {tags}
---

{actual_content}

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
        commit_msg = f"Add ad news: {actual_title}"
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
  # 添加新闻（自动生成标题 - 推荐）
  %(prog)s add "今日OpenAI宣布推出新的广告产品..."
  
  # 添加新闻并自动推送
  %(prog)s add "新闻内容..." --push
  
  # 使用自定义标题（不使用AI生成）
  %(prog)s add "自定义标题" "新闻内容" --no-auto-title
  
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
    add_parser.add_argument('content', help='新闻内容（如果使用 --no-auto-title 则为标题）')
    add_parser.add_argument('content2', nargs='?', help='新闻内容（当第一个参数是标题时）')
    add_parser.add_argument('-t', '--tags', default='ad-news', 
                           help='标签（逗号分隔，默认: ad-news）')
    add_parser.add_argument('--push', action='store_true', 
                           help='自动推送到 GitHub')
    add_parser.add_argument('--no-auto-title', action='store_true',
                           help='不使用AI生成标题，使用用户提供的标题')
    
    # list 命令
    list_parser = subparsers.add_parser('list', help='列出最近的文章')
    list_parser.add_argument('-n', '--number', type=int, default=10,
                            help='显示数量（默认: 10）')
    
    args = parser.parse_args()
    
    if args.command == 'add':
        add_news(
            args.content, 
            args.content2, 
            args.tags, 
            args.push,
            not args.no_auto_title
        )
    elif args.command == 'list':
        list_news(args.number)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
