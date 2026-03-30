#!/bin/bash
# 启动港股打新网页服务

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="/tmp/hk_ipo_api.pid"

# 检查是否已在运行
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p $PID > /dev/null 2>&1; then
        echo "✅ 港股打新 API 已在运行 (PID: $PID)"
        echo "🌐 访问地址：http://localhost:8765"
        exit 0
    fi
fi

# 启动服务
echo "🚀 启动港股打新 API 服务..."
cd "$SCRIPT_DIR"
nohup python3 hk_ipo_api.py > /tmp/hk_ipo_api.log 2>&1 &
echo $! > "$PID_FILE"

# 等待服务启动
sleep 3

# 检查服务状态
if ps -p $(cat "$PID_FILE") > /dev/null 2>&1; then
    echo "✅ 服务启动成功！"
    echo "🌐 访问地址：http://localhost:8765"
    echo "📊 API 文档：http://localhost:8765/docs"
    echo "📁 日志文件：/tmp/hk_ipo_api.log"
    echo ""
    echo "停止服务：bash $0 stop"
else
    echo "❌ 服务启动失败，请检查日志："
    tail -20 /tmp/hk_ipo_api.log
fi
