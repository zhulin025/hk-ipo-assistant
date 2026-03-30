# Scrapling 网页抓取技能

使用 Scrapling 框架进行自适应网页抓取。支持 HTTP 请求、反反爬、浏览器自动化和分布式爬取。

## 安装

```bash
python3 -m pip install scrapling --break-system-packages
```

## 核心功能

### 1. 简单抓取（HTTP 请求）

```bash
python3 ~/.openclaw/skills/scrapling/scripts/fetch.py \
  --url "https://example.com" \
  --selector ".product" \
  --field "title=h2::text" \
  --field "price=.price::text"
```

### 2. 反反爬模式（绕过 Cloudflare）

```bash
python3 ~/.openclaw/skills/scrapling/scripts/fetch.py \
  --url "https://protected-site.com" \
  --stealth \
  --headless \
  --selector ".content"
```

### 3. 动态渲染（浏览器自动化）

```bash
python3 ~/.openclaw/skills/scrapling/scripts/fetch.py \
  --url "https://spa-site.com" \
  --dynamic \
  --wait-selector ".loaded-content" \
  --selector ".item"
```

### 4. 完整爬虫（多页面）

```bash
python3 ~/.openclaw/skills/scrapling/scripts/crawl.py \
  --start-url "https://example.com" \
  --selector ".product" \
  --field "name=h2::text" \
  --field "link=a@href" \
  --follow ".next a" \
  --output products.json
```

## 🌐 网页应用

**访问地址**: http://localhost:8765

**功能**：
- 📊 市场概览（实时新股数据）
- 📈 数据分析（历史趋势、行业分布、保荐人统计）
- 🎯 打新策略（4 种策略详解）
- 📚 新手教程（从开户到实战）
- ⏰ 提醒事项（申购/中签/上市提醒）

**启动服务**：
```bash
bash ~/.openclaw/skills/scrapling/scripts/start_hk_ipo_server.sh
```

**停止服务**：
```bash
bash ~/.openclaw/skills/scrapling/scripts/stop_hk_ipo_server.sh
```

**API 文档**: http://localhost:8765/docs

---

## 脚本说明

### hk_ipo_pro.py - 港股打新专业版（推荐 ⭐⭐⭐）

**完整功能**：多数据源 + 数据分析 + 报告生成

```bash
# 完整抓取 + 分析 + 生成报告
python3 ~/.openclaw/skills/scrapling/scripts/hk_ipo_pro.py --analyze --output hk_ipo.json --report report.txt

# 查看详细报告
python3 ~/.openclaw/skills/scrapling/scripts/hk_ipo_viewer.py

# 只看统计摘要
python3 ~/.openclaw/skills/scrapling/scripts/hk_ipo_viewer.py --stats
```

**定时任务**：
- 每周一至周五 9:00 自动执行
- 数据保存到 `/tmp/hk_ipo/`
- 飞书自动推送日报摘要

**手动执行定时脚本**：
```bash
bash ~/.openclaw/skills/scrapling/scripts/run_hk_ipo.sh
```

**输出格式**：
```json
{
  "timestamp": "2026-03-30T09:53:39",
  "data": {
    "sina": [
      {"code": "688813", "name": "泰金新能", "list_date": "2026-03-31", "issue_price": "26.28"}
    ],
    "laohu8": [
      {"title": "口腔护理品牌「参半」母公司冲击港股 IPO", "link": "https://..."}
    ]
  }
}
```

---

### fetch.py - 单页面抓取

**参数**：
- `--url` (必需): 目标 URL
- `--selector` (必需): CSS 选择器
- `--field`: 字段提取（可多次），格式 `name=selector`
- `--stealth`: 启用反反爬模式
- `--dynamic`: 启用浏览器动态渲染
- `--headless`: 无头模式
- `--wait-selector`: 等待元素出现
- `--adaptive`: 启用自适应选择器（网站改版后自动调整）
- `--output`: 输出文件（JSON）
- `--proxy`: 代理地址

### crawl.py - 多页面爬取

**参数**：
- `--start-url` (必需): 起始 URL
- `--selector` (必需): 列表项选择器
- `--field`: 字段提取（可多次）
- `--follow`: 下一页链接选择器
- `--concurrent`: 并发数（默认 10）
- `--output`: 输出文件（JSON/JSONL）
- `--crawldir`: 断点续爬目录

## 选择器语法

支持 Scrapy 风格的伪元素：

- `.class` - 类选择器
- `#id` - ID 选择器
- `tag` - 标签选择器
- `::text` - 提取文本
- `::attr(name)` - 提取属性
- `xpath('//div')` - XPath 选择器

## 输出格式

**默认输出**（stdout）：
```json
[
  {"title": "产品 1", "price": "$99"},
  {"title": "产品 2", "price": "$199"}
]
```

**带 --output**：保存到文件

## 示例

### 抓取 Quotes to Scrape

```bash
python3 ~/.openclaw/skills/scrapling/scripts/fetch.py \
  --url "https://quotes.toscrape.com/" \
  --selector ".quote" \
  --field "text=.text::text" \
  --field "author=.author::text" \
  --field "tags=.tag::text"
```

### 绕过 Cloudflare

```bash
python3 ~/.openclaw/skills/scrapling/scripts/fetch.py \
  --url "https://nopecha.com/demo/cloudflare" \
  --stealth \
  --headless \
  --selector "#padded_content a"
```

### 动态网站（等待加载）

```bash
python3 ~/.openclaw/skills/scrapling/scripts/fetch.py \
  --url "https://example-spa.com" \
  --dynamic \
  --wait-selector ".loaded" \
  --selector ".item" \
  --field "title=h2::text"
```

## 注意事项

1. **自适应模式**：`--adaptive` 会在网站改版后自动调整选择器，但极端改版可能失效
2. **浏览器模式**：`--dynamic` 或 `--stealth` 会启动浏览器，资源消耗较大
3. **并发限制**：大规模爬取时设置 `--concurrent` 避免被封
4. **代理支持**：使用 `--proxy` 参数配置代理（格式：`http://user:pass@host:port`）

## 调试

**交互式 Shell**：
```bash
scrapling shell https://example.com
```

**查看选择器匹配**：
```bash
python3 ~/.openclaw/skills/scrapling/scripts/fetch.py \
  --url "https://example.com" \
  --selector ".product" \
  --verbose
```
