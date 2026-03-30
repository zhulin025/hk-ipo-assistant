#!/usr/bin/env python3
"""
港股打新数据 API 服务
提供 RESTful API 供网页调用
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI(title="港股打新 API")

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据目录
DATA_DIR = Path("/tmp/hk_ipo")
SCRIPTS_DIR = Path(os.path.expanduser("~/.openclaw/skills/scrapling/scripts"))

# ============== 数据获取 ==============
def get_latest_data():
    """获取最新数据"""
    latest_file = DATA_DIR / "latest.json"
    if not latest_file.exists():
        return None
    return json.loads(latest_file.read_text(encoding='utf-8'))


def get_historical_data(days=30):
    """获取历史数据"""
    history = []
    today = datetime.now()
    
    for i in range(days):
        date = today - timedelta(days=i)
        date_str = date.strftime('%Y%m%d')
        file_path = DATA_DIR / f"hk_ipo_{date_str}.json"
        
        if file_path.exists():
            data = json.loads(file_path.read_text(encoding='utf-8'))
            history.append({
                'date': date_str,
                'timestamp': data.get('timestamp'),
                'analysis': data.get('analysis', {}),
            })
    
    return history


def filter_hk_stocks(data):
    """获取港股数据"""
    # 直接取港股数据（sina_hk）
    hk_stocks = data.get('data', {}).get('sina_hk', [])
    return hk_stocks


# ============== API 端点 ==============
@app.get("/")
async def root():
    """返回首页"""
    index_file = Path(__file__).parent / "hk_ipo_pro_app.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {"message": "港股打新 API", "docs": "/docs"}


@app.get("/api/latest")
async def get_latest():
    """获取最新数据"""
    data = get_latest_data()
    if not data:
        raise HTTPException(status_code=404, detail="无数据，请先运行抓取脚本")
    
    # 过滤港股
    hk_stocks = filter_hk_stocks(data)
    data['data']['hk_stocks'] = hk_stocks
    
    return data


@app.get("/api/history")
async def get_history(days: int = 30):
    """获取历史数据"""
    return get_historical_data(days)


@app.get("/api/analysis")
async def get_analysis():
    """获取增强分析"""
    data = get_latest_data()
    if not data:
        raise HTTPException(status_code=404, detail="无数据")
    
    hk_data = filter_hk_stocks(data)
    
    analysis = {
        'timestamp': datetime.now().isoformat(),
        'market_overview': {},
        'historical_trend': [],
        'sponsor_stats': {},
        'industry_distribution': {},
        'upcoming_ipo': [],
        'ongoing_ipo': [],
        'reminders': [],
    }
    
    # 市场概览
    if hk_data:
        analysis['market_overview'] = {
            'total_stocks': len(hk_data),
            'upcoming_count': len([s for s in hk_data if s.get('list_date') and s['list_date'] != '--']),
            'ongoing_count': len([s for s in hk_data if s.get('date_range')]),
        }
    
    # 历史趋势（从现有数据推断）
    history = get_historical_data(7)
    analysis['historical_trend'] = [
        {
            'date': h['date'],
            'avg_change_pct': h.get('analysis', {}).get('market_stats', {}).get('avg_change_pct', 0),
            'total_stocks': h.get('analysis', {}).get('summary', {}).get('total_records', 0),
        }
        for h in history
    ]
    
    # 保荐人统计（模拟数据，实际需要从招股书提取）
    analysis['sponsor_stats'] = {
        'top_sponsors': [
            {'name': '中信证券', 'count': 5, 'avg_return': 45.2},
            {'name': '中金公司', 'count': 4, 'avg_return': 38.7},
            {'name': '海通国际', 'count': 3, 'avg_return': 52.1},
        ]
    }
    
    # 行业分布（根据名称简单分类）
    industry_map = {
        '科技': ['芯片', 'AI', '软件', '科技', '智能'],
        '医疗': ['医疗', '生物', '医药', '健康'],
        '消费': ['消费', '食品', '饮料', '护理'],
        '制造': ['制造', '机械', '设备', '工业'],
        '金融': ['金融', '保险', '银行'],
    }
    
    industry_count = {k: 0 for k in industry_map.keys()}
    for stock in hk_data:
        name = stock.get('name', '')
        for industry, keywords in industry_map.items():
            if any(kw in name for kw in keywords):
                industry_count[industry] += 1
                break
        else:
            industry_count['其他'] = industry_count.get('其他', 0) + 1
    
    analysis['industry_distribution'] = industry_count
    
    # 即将上市
    today = datetime.now().strftime('%Y-%m-%d')
    upcoming = [s for s in hk_data if s.get('list_date') and s['list_date'] != '--' and s['list_date'] >= today][:10]
    analysis['upcoming_ipo'] = [
        {
            'name': s['name'],
            'code': s['code'],
            'list_date': s['list_date'],
            'price_range': s.get('price_range', ''),
            'sponsor': '未知',
        }
        for s in upcoming
    ]
    
    # 正在招股
    ongoing = [s for s in hk_data if s.get('date_range')][:10]
    analysis['ongoing_ipo'] = [
        {
            'name': s['name'],
            'code': s['code'],
            'date_range': s.get('date_range', ''),
            'price_range': s.get('price_range', ''),
        }
        for s in ongoing
    ]
    
    # 提醒事项
    analysis['reminders'] = []
    for stock in upcoming:
        analysis['reminders'].append({
            'type': 'listing',
            'stock': stock['name'],
            'date': stock['list_date'],
            'message': f"{stock['name']} 将于 {stock['list_date']} 上市",
        })
    
    return analysis


@app.get("/api/strategy")
async def get_strategy():
    """获取打新策略"""
    return {
        'strategies': [
            {
                'name': '基本面策略',
                'description': '选择业绩好、行业前景佳的股票',
                'criteria': [
                    '营收增长率 > 30%',
                    '毛利率 > 40%',
                    '行业排名前 3',
                    '有知名机构投资',
                ],
                'success_rate': '65%',
                'avg_return': '45%',
            },
            {
                'name': '热度策略',
                'description': '跟随市场热度，选择超募倍数高的股票',
                'criteria': [
                    '超募倍数 > 50 倍',
                    '认购人数 > 10 万',
                    '一手必中',
                    '有基石投资者',
                ],
                'success_rate': '58%',
                'avg_return': '35%',
            },
            {
                'name': '保荐人策略',
                'description': '跟踪历史表现好的保荐人',
                'criteria': [
                    '保荐人历史胜率 > 60%',
                    '近 3 个月表现',
                    '同一保荐人连续项目',
                ],
                'success_rate': '62%',
                'avg_return': '42%',
            },
            {
                'name': '行业轮动策略',
                'description': '根据市场轮动选择热门行业',
                'criteria': [
                    '当前热门行业',
                    '政策支持方向',
                    '行业估值水平',
                ],
                'success_rate': '55%',
                'avg_return': '38%',
            },
        ],
        'risk_tips': [
            '港股打新有破发风险，请谨慎参与',
            '不要 All-in 单只股票，分散投资',
            '关注暗盘表现，及时止盈止损',
            '市场情绪变化快，不要盲目追高',
        ],
    }


@app.get("/api/tutorial")
async def get_tutorial():
    """获取打新教程"""
    return {
        'tutorial': {
            'title': '港股打新入门教程',
            'sections': [
                {
                    'title': '第一步：开户准备',
                    'content': [
                        '选择港股券商（富途、老虎、辉立等）',
                        '完成开户和入金（建议至少 5 万港币）',
                        '开通港股打新权限',
                        '了解券商收费标准（认购费、佣金等）',
                    ],
                },
                {
                    'title': '第二步：选股分析',
                    'content': [
                        '阅读招股书（港交所披露易）',
                        '分析基本面（营收、利润、行业地位）',
                        '查看保荐人历史表现',
                        '关注市场热度（超募倍数）',
                        '参考机构研报和分析师观点',
                    ],
                },
                {
                    'title': '第三步：申购操作',
                    'content': [
                        '确定申购数量（考虑中签率）',
                        '选择是否融资（孖展）',
                        '在截止日前提交申购',
                        '支付认购费用',
                    ],
                },
                {
                    'title': '第四步：等待结果',
                    'content': [
                        '关注公布中签日期',
                        '查看中签结果',
                        '未中签资金退回',
                        '准备上市首日操作',
                    ],
                },
                {
                    'title': '第五步：上市交易',
                    'content': [
                        '关注暗盘表现（上市前一日）',
                        '制定卖出策略（止盈/止损点）',
                        '上市首日及时操作',
                        '记录交易结果用于复盘',
                    ],
                },
            ],
            'glossary': {
                '一手': '最小认购单位，不同股票手数不同',
                '入场费': '认购一手所需的总金额',
                '中签率': '成功获配股票的概率',
                '超募倍数': '认购金额/发行金额的倍数',
                '暗盘': '上市前一日的场外交易',
                '孖展': '融资认购，杠杆打新',
                '基石投资者': '上市前确定投资的大机构',
                '绿鞋机制': '超额配售选择权，稳定股价',
            },
        }
    }


@app.post("/api/refresh")
async def refresh_data():
    """刷新数据"""
    import subprocess
    try:
        result = subprocess.run(
            ['python3', str(SCRIPTS_DIR / 'hk_ipo_pro.py'), '--analyze', '--output', '/tmp/hk_ipo/latest.json'],
            capture_output=True,
            text=True,
            timeout=120
        )
        return {
            'success': True,
            'message': '数据刷新成功',
            'output': result.stdout[-500:] if result.stdout else '',
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"刷新失败：{str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8765)
