# 🔧 网页调试指南

## 问题诊断步骤

### 1. 打开浏览器控制台

**Chrome/Edge**:
- 按 `F12` 或 `Cmd+Option+I` (Mac) / `Ctrl+Shift+I` (Windows)
- 点击 **Console** 标签

**Safari**:
- 按 `Cmd+Option+I`
- 点击 **Console** 标签

### 2. 查看错误信息

刷新页面后，控制台应该显示：

```
开始加载数据，API_BASE: http://localhost:8765/api
测试 /api/latest...
latest 状态：200
latest 数据：{...}
```

### 3. 常见错误及解决方案

#### 错误 1: `Failed to fetch`
**原因**: API 服务未启动

**解决**:
```bash
bash ~/.openclaw/skills/scrapling/scripts/start_hk_ipo_server.sh
```

#### 错误 2: `CORS policy`
**原因**: 跨域请求被阻止

**解决**: 确保通过 `http://localhost:8765` 访问，不要用 `file://` 打开

#### 错误 3: `404 Not Found`
**原因**: API 路径错误

**解决**: 访问 http://localhost:8765/docs 查看 API 文档

### 4. 测试 API

**浏览器访问**:
- http://localhost:8765/api/latest
- http://localhost:8765/api/analysis
- http://localhost:8765/docs

**命令行测试**:
```bash
curl http://localhost:8765/api/latest | head -100
```

### 5. 检查服务状态

```bash
# 查看进程
ps aux | grep hk_ipo_api

# 查看日志
tail -50 /tmp/hk_ipo_api.log

# 重启服务
bash ~/.openclaw/skills/scrapling/scripts/stop_hk_ipo_server.sh
bash ~/.openclaw/skills/scrapling/scripts/start_hk_ipo_server.sh
```

## 正确的访问方式

✅ **正确**: 在浏览器地址栏输入 `http://localhost:8765`

❌ **错误**: 双击打开 HTML 文件（file:// 协议）

## 快速诊断脚本

```bash
#!/bin/bash
echo "=== 港股打新 API 诊断 ==="
echo ""
echo "1. 检查进程..."
ps aux | grep hk_ipo_api | grep -v grep

echo ""
echo "2. 测试 API..."
curl -s -o /dev/null -w "HTTP 状态码：%{http_code}\n" http://localhost:8765/api/latest

echo ""
echo "3. 查看最新日志..."
tail -10 /tmp/hk_ipo_api.log
```

## 如果还是不行

1. **截图控制台错误** - 发给我看具体的错误信息
2. **检查端口占用** - `lsof -i :8765`
3. **尝试其他浏览器** - Chrome/Edge/Safari
