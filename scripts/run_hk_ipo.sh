#!/bin/bash
# 港股打新数据定时抓取脚本
# 用于 cron 定时任务调用

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="/tmp/hk_ipo"
DATE=$(date +%Y%m%d)

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 执行抓取和分析
python3 "$SCRIPT_DIR/hk_ipo_pro.py" \
    --analyze \
    --output "$OUTPUT_DIR/hk_ipo_${DATE}.json" \
    --report "$OUTPUT_DIR/hk_ipo_${DATE}.txt" \
    2>&1 | tee "$OUTPUT_DIR/hk_ipo_${DATE}.log"

# 更新最新数据链接
cp "$OUTPUT_DIR/hk_ipo_${DATE}.json" "$OUTPUT_DIR/latest.json"
cp "$OUTPUT_DIR/hk_ipo_${DATE}.txt" "$OUTPUT_DIR/latest_report.txt"

echo "=========================================="
echo "✅ 港股打新数据抓取完成"
echo "📁 数据文件：$OUTPUT_DIR/hk_ipo_${DATE}.json"
echo "📄 报告文件：$OUTPUT_DIR/hk_ipo_${DATE}.txt"
echo "📊 最新数据：$OUTPUT_DIR/latest.json"
echo "=========================================="
