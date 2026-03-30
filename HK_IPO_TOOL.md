# 🦞 港股打新工具 - 完整文档

## 📋 功能概览

| 功能 | 状态 | 说明 |
|------|------|------|
| 多数据源抓取 | ✅ | 新浪财经、老虎社区、东方财富 |
| 数据分析 | ✅ | 涨跌幅统计、中签率分析 |
| 报告生成 | ✅ | 每日自动生成文本报告 |
| 定时任务 | ✅ | 工作日 9:00 自动执行 |
| 飞书推送 | ✅ | 自动推送日报摘要 |

---

## 🚀 快速开始

### 1. 手动抓取数据

```bash
# 完整版（推荐）
python3 ~/.openclaw/skills/scrapling/scripts/hk_ipo_pro.py --analyze --output hk_ipo.json --report report.txt

# 快速版
python3 ~/.openclaw/skills/scrapling/scripts/hk_ipo_viewer.py
```

### 2. 查看报告

```bash
# 查看完整报告
python3 ~/.openclaw/skills/scrapling/scripts/hk_ipo_viewer.py

# 只看统计
python3 ~/.openclaw/skills/scrapling/scripts/hk_ipo_viewer.py --stats
```

### 3. 手动执行定时任务

```bash
bash ~/.openclaw/skills/scrapling/scripts/run_hk_ipo.sh
```

---

## 📊 数据源

| 数据源 | 类型 | 更新频率 | 数据质量 |
|--------|------|----------|----------|
| 新浪财经 | IPO 列表 | 实时 | ⭐⭐⭐⭐ |
| 老虎社区 | IPO 资讯 | 实时 | ⭐⭐⭐⭐⭐ |
| 东方财富 | IPO 数据 | 实时 | ⭐⭐⭐ |

---

## 📈 数据分析维度

### 市场统计
- 平均涨跌幅
- 最大涨幅/跌幅
- 平均中签率
- 新股数量统计

### 排行榜
- 表现最佳新股（Top 5）
- 即将上市新股
- 热门 IPO 资讯

---

## ⏰ 定时任务配置

**Cron 表达式**: `0 9 * * 1-5`（周一至周五 9:00）

**执行内容**:
1. 抓取所有数据源
2. 执行数据分析
3. 生成报告文件
4. 飞书推送摘要

**文件位置**:
- 数据：`/tmp/hk_ipo/hk_ipo_YYYYMMDD.json`
- 报告：`/tmp/hk_ipo/hk_ipo_YYYYMMDD.txt`
- 最新：`/tmp/hk_ipo/latest.json` / `latest_report.txt`

---

## 📁 输出示例

### JSON 数据结构

```json
{
  "timestamp": "2026-03-30T10:21:32",
  "data": {
    "sina": [
      {
        "code": "688813",
        "name": "泰金新能",
        "list_date": "2026-03-31",
        "issue_price": "26.28",
        "winning_ratio": "0.02",
        "change_pct": "0.00"
      }
    ],
    "laohu8": [
      {
        "title": "口腔护理品牌「参半」母公司冲击港股 IPO",
        "link": "https://www.laohu8.com/post/..."
      }
    ]
  },
  "analysis": {
    "summary": {
      "total_records": 40,
      "hk_count": 40
    },
    "market_stats": {
      "avg_change_pct": 224.66,
      "max_gain": 692.95,
      "avg_winning_ratio": 0.03
    },
    "top_performers": [...],
    "upcoming": [...]
  }
}
```

### 文本报告

```
============================================================
📊 港股打新数据日报
生成时间：2026-03-30T10:21:32
============================================================

📋 数据摘要
  总记录数：40
  港股数量：40

📈 市场统计
  平均涨跌幅：224.66%
  最大涨幅：692.95%
  平均中签率：0.03%

🏆 表现最佳新股
  1. 沐曦股份 (688802) +692.95% 发行价：104.66
  ...

📅 即将上市新股
  1. 泰金新能 (688813) 2026-03-31 发行价：26.28
  ...

📰 最新资讯
  1. 口腔护理品牌「参半」母公司冲击港股 IPO
  ...
```

---

## 🔧 高级用法

### 自定义数据源

```bash
# 只抓取新浪财经
python3 hk_ipo_pro.py --sources sina --output sina.json

# 只抓取老虎社区
python3 hk_ipo_pro.py --sources laohu8 --output laohu.json

# 抓取多个数据源
python3 hk_ipo_pro.py --sources sina laohu8 --output combined.json
```

### 修改定时任务

查看当前任务：
```bash
openclaw cron list
```

修改执行时间（例如改为每天 8:30）：
```bash
openclaw cron update <job_id> --schedule "30 8 * * *"
```

---

## 📝 待优化项

1. **更多数据源**
   - [ ] 港交所披露易（需要处理验证码）
   - [ ] 阿斯达克财经
   - [ ] 智通财经

2. **数据分析增强**
   - [ ] 历史数据对比
   - [ ] 保荐人胜率统计
   - [ ] 行业分布分析

3. **提醒功能**
   - [ ] 申购截止提醒
   - [ ] 公布中签提醒
   - [ ] 上市首日提醒

---

## 📞 故障排查

### 数据抓取失败

**问题**: 新浪财经返回 0 条数据
**解决**: 检查网络连接，网站可能临时维护

**问题**: 老虎社区超时
**解决**: StealthyFetcher 启动浏览器较慢，耐心等待

### 定时任务未执行

**检查任务状态**:
```bash
openclaw cron list
```

**手动触发**:
```bash
openclaw cron run <job_id>
```

---

*最后更新：2026-03-30*
