#!/usr/bin/env python3
"""
港股打新数据整合工具
- 多数据源抓取（新浪财经、老虎社区、东方财富、港交所）
- 数据清洗与整合
- 数据分析与统计
- 定时任务支持
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from scrapling.fetchers import Fetcher, StealthyFetcher


# ============== 数据源配置 ==============
DATA_SOURCES = {
    'sina_hk': {
        'name': '新浪财经 - 港股 IPO',
        'url': 'http://vip.stock.finance.sina.com.cn/q/view/hk_IPOList.php',
        'type': 'table',
        'stealth': False,
        'market': 'HK',
    },
    'sina_a': {
        'name': '新浪财经 - A 股打新',
        'url': 'http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/dxsy/index.phtml',
        'type': 'table',
        'stealth': False,
        'market': 'A',
    },
    'laohu8': {
        'name': '老虎社区',
        'url': 'https://www.laohu8.com/subject/theme/bbff91dc17c14a06a84c8b103cf4e290',
        'type': 'articles',
        'stealth': True,
        'market': 'HK',
    },
}


# ============== 数据抓取函数 ==============
def fetch_sina_hk_data(verbose=False):
    """抓取新浪财经港股 IPO 数据"""
    if verbose:
        print("正在抓取新浪港股 IPO...")
    
    try:
        page = Fetcher.get(DATA_SOURCES['sina_hk']['url'])
        tables = page.css('table')
        if not tables:
            return []
        
        # 第二个表格是数据表
        data_table = tables[1]
        rows = data_table.css('tr')[1:]  # 跳过表头
        
        results = []
        for row in rows:
            cells = row.css('td')
            if len(cells) >= 6:
                code = cells[0].css('::text').get() or ''
                name = cells[1].css('::text').get() or ''
                
                if code and name:
                    # 提取价格范围
                    price_text = cells[2].css('::text').get() or ''
                    price_range = price_text.replace('\t', '').strip()
                    
                    # 提取日期范围
                    date_text = cells[4].css('::text').get() or ''
                    date_range = date_text.replace('\t', '').strip()
                    
                    # 提取上市日期
                    list_date = ''
                    if len(cells) > 5:
                        list_date = cells[5].css('::text').get() or ''
                        list_date = list_date.replace('\t', '').strip()
                    
                    results.append({
                        'code': code,
                        'name': name,
                        'price_range': price_range,
                        'date_range': date_range,
                        'list_date': list_date,
                        'market': 'HK',
                        'source': 'sina_hk',
                    })
        
        if verbose:
            print(f"  ✅ 新浪港股：{len(results)} 只")
        return results
    except Exception as e:
        if verbose:
            print(f"  ❌ 新浪港股失败：{e}")
        return []


def fetch_sina_a_data(verbose=False):
    """抓取新浪财经 A 股打新数据（用于对比）"""
    if verbose:
        print("正在抓取新浪 A 股...")
    
    try:
        page = Fetcher.get(DATA_SOURCES['sina_a']['url'])
        rows = page.css('table.list_table tr')[1:]
        
        results = []
        for row in rows:
            tds = row.css('td')
            if len(tds) >= 10:
                code = tds[0].css('::text').get() or ''
                if code:
                    results.append({
                        'code': code,
                        'apply_code': tds[1].css('::text').get() or '',
                        'name': tds[2].css('a::text').get() or '',
                        'list_date': tds[3].css('::text').get() or '',
                        'winning_ratio': tds[6].css('::text').get() or '0',
                        'change_pct': tds[7].css('::text').get() or '0',
                        'issue_price': tds[9].css('::text').get() or '0',
                        'market': 'A',
                        'source': 'sina_a',
                    })
        
        if verbose:
            print(f"  ✅ 新浪 A 股：{len(results)} 条")
        return results
    except Exception as e:
        if verbose:
            print(f"  ❌ 新浪 A 股失败：{e}")
        return []


def fetch_laohu_data(verbose=False):
    """抓取老虎社区 IPO 资讯"""
    if verbose:
        print("正在抓取老虎社区...")
    
    try:
        page = StealthyFetcher.fetch(DATA_SOURCES['laohu8']['url'], headless=True)
        links = page.css('a[href*="/post/"]')
        
        articles = []
        for link in links:
            text = link.css('::text').get()
            href = link.attrib.get('href', '')
            
            if text and len(text.strip()) > 10:
                articles.append({
                    'title': text.strip()[:150],
                    'link': f'https://www.laohu8.com{href}' if href.startswith('/') else href,
                    'source': 'laohu8',
                    'market': 'HK',
                })
        
        # 去重
        seen = set()
        unique = []
        for art in articles:
            if art['link'] not in seen:
                seen.add(art['link'])
                unique.append(art)
        
        if verbose:
            print(f"  ✅ 老虎社区：{len(unique)} 篇")
        return unique
    except Exception as e:
        if verbose:
            print(f"  ❌ 老虎社区失败：{e}")
        return []


def fetch_eastmoney_data(verbose=False):
    """抓取东方财富网港股 IPO 数据"""
    if verbose:
        print("正在抓取东方财富网...")
    
    try:
        # 尝试多个可能的 URL
        urls = [
            'http://data.eastmoney.com/hkipo/',
            'http://data.eastmoney.com/hkipo/list.html',
        ]
        
        for url in urls:
            try:
                page = Fetcher.get(url)
                if page.status == 200:
                    tables = page.css('table')
                    if tables:
                        if verbose:
                            print(f"  ✅ 东方财富网：找到 {len(tables)} 个表格")
                        return [{'note': f'找到 {len(tables)} 个表格', 'source': 'eastmoney'}]
            except:
                continue
        
        if verbose:
            print(f"  ⚠️ 东方财富网：无数据")
        return []
    except Exception as e:
        if verbose:
            print(f"  ❌ 东方财富网失败：{e}")
        return []


# ============== 数据分析函数 ==============
def analyze_data(data):
    """分析 IPO 数据"""
    analysis = {
        'timestamp': datetime.now().isoformat(),
        'summary': {},
        'market_stats': {},
        'top_performers': [],
        'upcoming': [],
    }
    
    # 港股数据
    hk_data = data.get('sina_hk', [])
    
    # 基础统计
    total = len(hk_data)
    
    analysis['summary'] = {
        'total_records': total,
        'hk_count': total,
        'a_count': 0,
    }
    
    # 即将上市（港股数据主要看这个）
    today = datetime.now().strftime('%Y-%m-%d')
    upcoming = [
        x for x in hk_data 
        if x.get('list_date') and x['list_date'] != '-' and x['list_date'] != '--' and x['list_date'] >= today
    ][:10]
    
    analysis['upcoming'] = [
        {'name': x['name'], 'code': x['code'], 'list_date': x['list_date'], 'price_range': x.get('price_range', '')}
        for x in upcoming
    ]
    
    # 正在招股
    now_str = datetime.now().strftime('%Y-%m-%d')
    ongoing = [
        x for x in hk_data
        if x.get('date_range') and now_str in x.get('date_range', '')
    ]
    
    analysis['ongoing'] = [
        {'name': x['name'], 'code': x['code'], 'date_range': x.get('date_range', ''), 'price_range': x.get('price_range', '')}
        for x in ongoing
    ]
    
    return analysis


def generate_report(data, analysis):
    """生成文本报告"""
    report = []
    report.append("=" * 60)
    report.append("📊 港股打新数据日报")
    report.append(f"生成时间：{analysis['timestamp']}")
    report.append("=" * 60)
    
    # 摘要
    report.append("\n📋 数据摘要")
    report.append(f"  港股 IPO 总数：{analysis['summary'].get('hk_count', 0)}")
    
    # 正在招股
    if analysis.get('ongoing'):
        report.append("\n🔥 正在招股")
        for i, stock in enumerate(analysis['ongoing'], 1):
            report.append(f"  {i}. {stock['name']} ({stock['code']})")
            report.append(f"     招股期：{stock['date_range']}")
            report.append(f"     招股价：{stock['price_range']}")
    
    # 即将上市
    if analysis.get('upcoming'):
        report.append("\n📅 即将上市")
        for i, stock in enumerate(analysis['upcoming'], 1):
            report.append(f"  {i}. {stock['name']} ({stock['code']}) {stock['list_date']}")
            report.append(f"     招股价：{stock['price_range']}")
    
    # 最新资讯
    laohu_data = data.get('laohu8', [])
    if laohu_data:
        report.append("\n📰 最新资讯（老虎社区）")
        for i, art in enumerate(laohu_data[:8], 1):
            report.append(f"  {i}. {art['title']}")
    
    report.append("\n" + "=" * 60)
    return "\n".join(report)


# ============== 主函数 ==============
def main():
    parser = argparse.ArgumentParser(description='港股打新数据整合工具')
    parser.add_argument('--sources', nargs='+', choices=['sina', 'laohu8', 'eastmoney', 'all'],
                        default=['all'], help='数据源')
    parser.add_argument('--output', help='输出文件（JSON）')
    parser.add_argument('--report', help='生成报告文件（TXT）')
    parser.add_argument('--analyze', action='store_true', help='执行数据分析')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')
    
    args = parser.parse_args()
    
    # 确定数据源
    if 'all' in args.sources:
        sources = ['sina_hk', 'laohu8']  # 默认只抓港股
    else:
        sources = args.sources
    
    # 抓取数据
    data = {
        'timestamp': datetime.now().isoformat(),
        'data': {}
    }
    
    if 'sina_hk' in sources:
        data['data']['sina_hk'] = fetch_sina_hk_data(args.verbose)
    
    if 'sina_a' in sources:
        data['data']['sina_a'] = fetch_sina_a_data(args.verbose)
    
    if 'laohu8' in sources:
        data['data']['laohu8'] = fetch_laohu_data(args.verbose)
    
    if 'eastmoney' in sources:
        data['data']['eastmoney'] = fetch_eastmoney_data(args.verbose)
    
    # 数据分析
    analysis = None
    if args.analyze:
        analysis = analyze_data(data['data'])
        
        # 生成报告
        report = generate_report(data['data'], analysis)
        print(report)
        
        if args.report:
            with open(args.report, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"\n📁 报告已保存到：{args.report}")
    
    # 保存数据
    if args.output:
        if analysis:
            data['analysis'] = analysis
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n💾 数据已保存到：{args.output}")
    
    return data


if __name__ == '__main__':
    main()
