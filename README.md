# 🦞 港股打新助手 (HK IPO Assistant)

一个完整的港股打新决策辅助工具，包含实时数据、AI 分析和打新教程。

## ✨ 功能特性

### 📅 新股日历

**实时展示所有港股 IPO 信息**：
- 发行价（价格范围）
- 募资规模
- 认购截止日期
- 上市日期
- 所属行业
- 入场费
- AI 推荐评级（申购/谨慎/不建议）
- 热度指数（🔥数量）

**页面布局**：
- 统计卡片（可认购/建议申购/不建议）
- 正在招股列表
- 认购已截止列表
- 风险提示

### 📊 基本面分析

- 公司概况
- 估值参考
- 保荐人历史表现
- 打新策略建议

### 🤖 AI 打新策略

- AI 综合推荐
- 市场情绪指标
- 风险提示
- 参考依据说明

### 📚 打新课程

- 新手入门
- 申购流程详解
- 甲组 vs 乙组
- 孖展认购流程
- 绿鞋机制详解
- 常见术语表

## 🚀 快速开始

### 安装依赖

```bash
# 安装 Scrapling
python3 -m pip install scrapling --break-system-packages

# 安装 FastAPI
python3 -m pip install fastapi uvicorn --break-system-packages
```

### 启动服务

```bash
# 启动 API 服务
bash scripts/start_hk_ipo_server.sh

# 访问网页
http://localhost:8765
```

### 抓取数据

```bash
# 手动抓取数据
python3 scripts/hk_ipo_pro.py --analyze --output hk_ipo.json --report report.txt

# 查看报告
python3 scripts/hk_ipo_viewer.py
```

## 📁 项目结构

```
scrapling/
├── scripts/
│   ├── hk_ipo_api.py          # FastAPI 后端
│   ├── ipo_calendar.html      # 新股日历页面（首页）
│   ├── hk_ipo_pro_app.html    # 专业版网页
│   ├── hk_ipo_pro.py          # 数据抓取与分析
│   ├── hk_ipo_viewer.py       # 快速查看工具
│   ├── run_hk_ipo.sh          # 定时任务脚本
│   ├── start_hk_ipo_server.sh # 启动服务
│   └── stop_hk_ipo_server.sh  # 停止服务
├── HK_IPO_GUIDE.md            # 完全指南教程
├── GREEN_SHOE_EXPLAINED.md    # 绿鞋机制详解
├── HK_IPO_TOOL.md             # 工具文档
├── PRO_FEATURES.md            # 专业版功能说明
└── SKILL.md                   # 技能说明
```

## 📊 数据源

| 数据源 | 类型 | 说明 |
|--------|------|------|
| 新浪财经 | IPO 列表 | 港股 IPO 数据（招股价、日期等） |
| 老虎社区 | IPO 资讯 | 招股书解读、暗盘表现、市场分析 |
| 手动录入 | 详细数据 | 募资规模、入场费、行业等 |

## 🎯 核心功能

### 新股卡片信息

每张新股卡片包含：

| 字段 | 说明 | 示例 |
|------|------|------|
| 代码 | 港股代码 | 03625 |
| 名称 | 公司中文名 | 上海傅里叶半导体 |
| 英文名 | 公司英文名 | Fourier Semiconductor |
| 发行价 | 价格范围 (HKD) | 40 ~ 50 |
| 募资规模 | 融资金额 (亿) | 20.0 ~ 25.0 |
| 认购截止 | 截止日期 | 2026-03-26 |
| 上市日 | 上市日期 | 2026-03-31 |
| 行业 | 所属行业 | 半导体 |
| 入场费 | 最低认购金额 | HKD 25,000 |
| 推荐评级 | AI 建议 | 申购/谨慎/不建议 |
| 热度指数 | 市场热度 | 🔥🔥🔥 |

### API 端点

| 端点 | 说明 |
|------|------|
| `GET /` | 新股日历页面 |
| `GET /api/latest` | 获取最新数据 |
| `GET /api/analysis` | 获取增强分析 |
| `GET /api/strategy` | 获取打新策略 |
| `GET /api/tutorial` | 获取教程内容 |
| `POST /api/refresh` | 刷新数据 |

## 📖 教程内容

### 基础概念
- 什么是港股打新
- 关键术语（一手、入场费、中签率等）
- 绿鞋机制详解

### 申购流程
```
T-7 日：招股开始
T-4 日：招股截止
T-3 日：公布中签
T-2 日：暗盘交易
T 日：  正式上市
```

### 实战策略
- 基本面策略（胜率 65%）
- 热度策略（胜率 58%）
- 保荐人策略（胜率 62%）
- 行业轮动策略（胜率 55%）
- 综合策略（推荐）

## 📸 页面预览

### 新股日历
- 渐变色标题栏（橙色主题）
- 统计卡片（3 个）
- 新股卡片网格（响应式布局）
- 推荐标签（颜色区分）
- 风险提示

## ⚠️ 风险提示

- 港股打新有破发风险，请谨慎参与
- 不要 All-in 单只股票，分散投资
- 关注暗盘表现，及时止盈止损
- 市场情绪变化快，不要盲目追高
- 本工具仅供参考，不构成投资建议

## 🛠️ 技术栈

- **前端**: HTML + TailwindCSS + JavaScript
- **后端**: FastAPI (Python)
- **爬虫**: Scrapling
- **部署**: 本地运行 / Vercel / Railway

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 联系方式

- 问题反馈：[GitHub Issues](https://github.com/zhulin025/hk-ipo-assistant/issues)
- 仓库地址：[GitHub](https://github.com/zhulin025/hk-ipo-assistant)

---

*最后更新：2026-03-30*
