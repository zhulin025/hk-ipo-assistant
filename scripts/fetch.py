#!/usr/bin/env python3
"""
Scrapling 单页面抓取脚本
"""

import argparse
import json
import sys
from scrapling.fetchers import Fetcher, StealthyFetcher, DynamicFetcher


def parse_fields(field_args):
    """解析 field 参数，返回字段名和选择器的字典"""
    fields = {}
    for field in field_args:
        if '=' not in field:
            print(f"错误：字段格式应为 'name=selector'，收到：{field}", file=sys.stderr)
            sys.exit(1)
        name, selector = field.split('=', 1)
        fields[name.strip()] = selector.strip()
    return fields


def extract_item(element, fields):
    """从单个元素中提取字段"""
    item = {}
    for name, selector in fields.items():
        # 处理伪元素
        if '::text' in selector:
            value = element.css(selector).get()
        elif '::attr(' in selector:
            attr_name = selector.split('::attr(')[1].rstrip(')')
            value = element.css(selector.replace(f'::attr({attr_name})', f'::attr({attr_name})')).get()
            if value is None:
                # 尝试直接用 attrib
                base_selector = selector.split('::')[0]
                elem = element.css(base_selector)
                if elem and attr_name in elem.attrib:
                    value = elem.attrib[attr_name]
        else:
            value = element.css(selector).get()
        item[name] = value or ''
    return item


def main():
    parser = argparse.ArgumentParser(description='Scrapling 单页面抓取')
    parser.add_argument('--url', required=True, help='目标 URL')
    parser.add_argument('--selector', required=True, help='CSS 选择器')
    parser.add_argument('--field', action='append', default=[], dest='fields',
                        help='字段提取（可多次），格式 name=selector')
    parser.add_argument('--stealth', action='store_true', help='启用反反爬模式')
    parser.add_argument('--dynamic', action='store_true', help='启用浏览器动态渲染')
    parser.add_argument('--headless', action='store_true', help='无头模式')
    parser.add_argument('--wait-selector', help='等待元素出现的 CSS 选择器')
    parser.add_argument('--adaptive', action='store_true', help='启用自适应选择器')
    parser.add_argument('--output', help='输出文件（JSON）')
    parser.add_argument('--proxy', help='代理地址')
    parser.add_argument('--verbose', action='store_true', help='详细输出')
    
    args = parser.parse_args()
    
    # 选择 fetcher
    if args.dynamic:
        fetcher = DynamicFetcher
    elif args.stealth:
        fetcher = StealthyFetcher
    else:
        fetcher = Fetcher
    
    # 构建参数
    fetch_kwargs = {}
    if args.headless:
        fetch_kwargs['headless'] = True
    if args.wait_selector:
        fetch_kwargs['wait_selector'] = args.wait_selector
    if args.adaptive:
        fetch_kwargs['adaptive'] = True
    if args.proxy:
        fetch_kwargs['proxy'] = args.proxy
    
    # 抓取页面
    if args.verbose:
        print(f"正在抓取：{args.url}")
    
    try:
        # Fetcher 用 get/other methods, StealthyFetcher/DynamicFetcher 用 fetch
        if fetcher == Fetcher:
            page = fetcher.get(args.url, **fetch_kwargs)
        else:
            page = fetcher.fetch(args.url, **fetch_kwargs)
    except Exception as e:
        print(f"抓取失败：{e}", file=sys.stderr)
        sys.exit(1)
    
    if args.verbose:
        print(f"抓取成功，状态码：{page.status}")
    
    # 解析字段
    fields = parse_fields(args.fields) if args.fields else {'text': '::text'}
    
    # 提取数据
    elements = page.css(args.selector)
    if not elements:
        print(f"警告：未找到匹配的元素（选择器：{args.selector}）", file=sys.stderr)
        if args.verbose:
            print(f"页面内容预览：{page.text[:500]}")
    
    results = []
    for elem in elements:
        item = extract_item(elem, fields)
        results.append(item)
    
    # 输出
    output_json = json.dumps(results, ensure_ascii=False, indent=2)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output_json)
        print(f"已保存到：{args.output}")
    else:
        print(output_json)


if __name__ == '__main__':
    main()
