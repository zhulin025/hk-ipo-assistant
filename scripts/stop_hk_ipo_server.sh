#!/bin/bash
# 停止港股打新网页服务

PID_FILE="/tmp/hk_ipo_api.pid"

if [ ! -f "$PID_FILE" ]; then
    echo "⚠️  服务未运行"
    exit 0
fi

PID=$(cat "$PID_FILE")
if ps -p $PID > /dev/null 2>&1; then
    echo "⏹️  停止服务 (PID: $PID)..."
    kill $PID
    rm "$PID_FILE"
    echo "✅ 服务已停止"
else
    echo "⚠️  进程不存在，清理 PID 文件"
    rm "$PID_FILE"
fi
