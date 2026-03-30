#!/usr/bin/env python3
"""
港股打新数据抓取脚本
- 新浪财经：IPO 列表数据
- 老虎社区：IPO 资讯
"""

import argparse
import json
from datetime import datetime
from scrapling.fetchers import Fetcher, StealthyFetcher


def fetch_sina_data():
    """抓取新浪财经打新数据"""
    print("正在抓取新浪财经打新数据...")
    
    try:
        page = Fetcher.get('http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/dxsy/index.phtml')
        rows = page.css('table.list_table tr')[1:]  # 跳过表头
        
        results = []
        for row in rows:
            tds = row.css('td')
            if len(tds) >= 10:
                code = tds[0].css('::text').get() or ''
                if code:  # 过滤空行
                    results.append({
                        'code': code,
                        'apply_code': tds[1].css('::text').get() or '',
                        'name': tds[2].css('a::text').get() or '',
                        'list_date': tds[3].css('::text').get() or '',
                        'winning_ratio': tds[6].css('::text').get() or '',
                        'change_pct': tds[7].css('::text').get() or '',
                        'issue_price': tds[9].css('::text').get() or '',
                        'source': 'sina',
                    })
        
        print(f"✅ 新浪财经：{len(results)} 条记录")
        return results
    except Exception as e:
        print(f"❌ 新浪财经抓取失败：{e}")
        return []


def fetch_laohu_data():
    """抓取老虎社区 IPO 资讯"""
    print("正在抓取老虎社区 IPO 资讯...")
    
    try:
        page = StealthyFetcher.fetch(
            'https://www.laohu8.com/subject/theme/bbff91dc17c14a06a84c8b103cf4e290',
            headless=True
        )
        
        links = page.css('a[href*="/post/"]')
        articles = []
        
        for link in links:
            text = link.css('::text').get()
            href = link.attrib.get('href', '')
            
            # 过滤掉短文本
            if text and len(text.strip()) > 10:
                articles.append({
                    'title': text.strip()[:150],
                    'link': f'https://www.laohu8.com{href}' if href.startswith('/') else href,
                    'source': 'laohu8',
                })
        
        # 去重
        seen = set()
        unique_articles = []
        for art in articles:
            if art['link'] not in seen:
                seen.add(art['link'])
                unique_articles.append(art)
        
        print(f"✅ 老虎社区：{len(unique_articles)} 篇资讯")
        return unique_articles
    except Exception as e:
        print(f"❌ 老虎社区抓取失败：{e}")
        return []


def main():
    parser = argparse.ArgumentParser(description='港股打新数据抓取')
    parser.add_argument('--sina', action='store_true', help='只抓取新浪财经')
    parser.add_argument('--laohu', action='store_true', help='只抓取老虎社区')
    parser.add_argument('--output', help='输出文件（JSON）')
    parser.add_argument('--verbose', action='store_true', help='详细输出')
    
    args = parser.parse_args()
    
    # 默认两个都抓
    if not args.sina and not args.laohu:
        args.sina = True
        args.laohu = True
    
    result = {
        'timestamp': datetime.now().isoformat(),
        'data': {}
    }
    
    if args.sina:
        result['data']['sina'] = fetch_sina_data()
    
    if args.laohu:
        result['data']['laohu8'] = fetch_laohu_data()
    
    # 输出
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n📁 已保存到：{args.output}")
    else:
        print("\n" + "="*60)
        print("抓取结果预览:")
        print("="*60)
        
        if 'sina' in result['data']:
            print(f"\n📊 新浪财经 ({len(result['data']['sina'])} 条):")
            for item in result['data']['sina'][:5]:
                print(f"  {item['code']} {item['name']} - 发行价：{item['issue_price']} 中签率：{item['winning_ratio']}%")
        
        if 'laohu8' in result['data']:
            print(f"\n📰 老虎社区 ({len(result['data']['laohu8'])} 篇):")
            for i, art in enumerate(result['data']['laohu8'][:5], 1):
                print(f"  {i}. {art['title']}")
        
        print("\n" + "="*60)


if __name__ == '__main__':
    main()
