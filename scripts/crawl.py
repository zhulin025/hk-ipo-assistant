#!/usr/bin/env python3
"""
Scrapling 多页面爬虫脚本
"""

import argparse
import asyncio
import json
import sys
from scrapling.spiders import Spider, Request, Response


def parse_fields(field_args):
    """解析 field 参数"""
    fields = {}
    for field in field_args:
        if '=' not in field:
            print(f"错误：字段格式应为 'name=selector'，收到：{field}", file=sys.stderr)
            sys.exit(1)
        name, selector = field.split('=', 1)
        fields[name.strip()] = selector.strip()
    return fields


class GenericSpider(Spider):
    """通用爬虫类"""
    
    def __init__(self, start_urls, selector, fields, follow_selector, output, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = start_urls
        self.selector = selector
        self.fields = fields
        self.follow_selector = follow_selector
        self.output = output
        self.results = []
    
    async def parse(self, response: Response):
        # 提取列表项
        elements = response.css(self.selector)
        
        for elem in elements:
            item = {}
            for name, selector in self.fields.items():
                if '::attr(' in selector:
                    attr_name = selector.split('::attr(')[1].rstrip(')')
                    base_selector = selector.split('::')[0]
                    matched = elem.css(base_selector)
                    if matched and attr_name in matched.attrib:
                        item[name] = matched.attrib[attr_name]
                    else:
                        item[name] = ''
                else:
                    item[name] = elem.css(selector).get() or ''
            self.results.append(item)
        
        # 跟随下一页
        if self.follow_selector:
            next_page = response.css(self.follow_selector)
            if next_page:
                # next_page 是 Selectors 列表，取第一个元素
                first_elem = next_page[0] if hasattr(next_page, '__getitem__') else next_page
                href = first_elem.attrib.get('href') if hasattr(first_elem, 'attrib') else None
                if href:
                    yield response.follow(href)
    
    def save_results(self):
        if self.output:
            with open(self.output, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, ensure_ascii=False, indent=2)
            print(f"已保存到：{self.output}", file=sys.stderr)
        else:
            print(json.dumps(self.results, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description='Scrapling 多页面爬虫')
    parser.add_argument('--start-url', required=True, help='起始 URL')
    parser.add_argument('--selector', required=True, help='列表项 CSS 选择器')
    parser.add_argument('--field', action='append', default=[], dest='fields',
                        help='字段提取（可多次），格式 name=selector')
    parser.add_argument('--follow', help='下一页链接选择器')
    parser.add_argument('--concurrent', type=int, default=10, help='并发数（默认 10）')
    parser.add_argument('--output', help='输出文件（JSON/JSONL）')
    parser.add_argument('--crawldir', help='断点续爬目录')
    parser.add_argument('--verbose', action='store_true', help='详细输出')
    
    args = parser.parse_args()
    
    # 解析字段
    fields = parse_fields(args.fields) if args.fields else {'text': '::text'}
    
    if args.verbose:
        print(f"起始 URL: {args.start_url}")
        print(f"选择器：{args.selector}")
        print(f"字段：{fields}")
        if args.follow:
            print(f"分页选择器：{args.follow}")
    
    # 创建爬虫
    class_name = 'GenericSpider'
    spider_class = type(class_name, (GenericSpider,), {
        'name': 'generic',
        'concurrent_requests': args.concurrent,
    })
    
    spider = spider_class(
        start_urls=[args.start_url],
        selector=args.selector,
        fields=fields,
        follow_selector=args.follow,
        output=args.output,
        crawldir=args.crawldir if args.crawldir else None,
    )
    
    # 运行爬虫
    try:
        result = spider.start()
        spider.save_results()
        print(f"\n抓取完成，共 {len(spider.results)} 条记录", file=sys.stderr)
    except KeyboardInterrupt:
        print("\n用户中断，进度已保存", file=sys.stderr)
        if args.crawldir:
            print(f"使用 --crawldir {args.crawldir} 可恢复爬取", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"爬取失败：{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
