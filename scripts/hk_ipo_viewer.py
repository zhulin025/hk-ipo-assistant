#!/usr/bin/env python3
"""
快速查看港股打新报告
"""

import json
import sys
from pathlib import Path

LATEST_REPORT = "/tmp/hk_ipo/latest_report.txt"
LATEST_DATA = "/tmp/hk_ipo/latest.json"


def show_report():
    """显示最新报告"""
    report_path = Path(LATEST_REPORT)
    if not report_path.exists():
        print("❌ 报告文件不存在，请先运行抓取脚本")
        print(f"   运行：python3 ~/.openclaw/skills/scrapling/scripts/hk_ipo_pro.py --analyze")
        return
    
    print(report_path.read_text(encoding='utf-8'))


def show_stats():
    """显示统计摘要"""
    data_path = Path(LATEST_DATA)
    if not data_path.exists():
        print("❌ 数据文件不存在")
        return
    
    data = json.loads(data_path.read_text(encoding='utf-8'))
    
    print("\n📊 数据摘要")
    print(f"  抓取时间：{data.get('timestamp', 'N/A')}")
    
    analysis = data.get('analysis', {})
    summary = analysis.get('summary', {})
    print(f"  总记录数：{summary.get('total_records', 0)}")
    print(f"  港股数量：{summary.get('hk_count', 0)}")
    
    stats = analysis.get('market_stats', {})
    if stats:
        print(f"\n📈 市场统计")
        if 'avg_change_pct' in stats:
            print(f"  平均涨跌幅：{stats['avg_change_pct']:.2f}%")
        if 'max_gain' in stats:
            print(f"  最大涨幅：{stats['max_gain']:.2f}%")
        if 'avg_winning_ratio' in stats:
            print(f"  平均中签率：{stats['avg_winning_ratio']:.2f}%")


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == '--stats':
            show_stats()
        elif sys.argv[1] == '--help':
            print("用法：python3 hk_ipo_viewer.py [选项]")
            print("\n选项:")
            print("  (无)     显示完整报告")
            print("  --stats  显示统计摘要")
            print("  --help   显示帮助")
        else:
            show_report()
    else:
        show_report()


if __name__ == '__main__':
    main()
