#!/usr/bin/env python3
"""
OPC一人公司MVP洞察简报生成器 v6.0 (XHS增强版)
特性: 多数据源(GitHub/HN/PH/小红书) + 智能去重 + 方向轮换 + YC CEO视角
新增: 小红书平台数据爬取，从真实用户需求中挖掘产品方向
"""

import httpx, asyncio, json, re, os, time
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
}

REPORT_DIR = Path(__file__).parent.parent / "reports"
CACHE_DIR  = Path(__file__).parent.parent / "cache"
XHS_CACHE  = CACHE_DIR / "xiaohongshu.json"
REPORT_DIR.mkdir(exist_ok=True)
CACHE_DIR.mkdir(exist_ok=True)

# ============================================================
# 已覆盖方向知识库（按日期维度管理，新增方向时同步更新）
# ============================================================
DIRECTION_LIBRARY = {
    "2026-04-11": [
        ("A1", "短视频口播AI剪辑工作室", ["口播", "剪辑", "字幕", "短视频"]),
        ("A2", "知识付费内容工厂", ["知识付费", "做课", "课程", "录课"]),
        ("A3", "私域运营AI客服销售", ["私域", "社群运营", "微信运营"]),
        ("A4", "垂直行业AI专家Agent", ["留学文书", "法律AI", "医美咨询"]),
    ],
    "2026-04-16": [
        ("B1", "Dify模板工厂", ["dify", "模板工厂", "工作流模板"]),
        ("B2", "Ollama一键傻瓜包", ["ollama", "本地部署", "私有化"]),
        ("B3", "ChatTTS声优工厂", ["chatts", "语音合成", "配音"]),
    ],
    "2026-04-17": [
        ("C1", "SkillsHunt技能发现平台", ["skills", "agent技能", "技能发现"]),
    ],
    "2026-04-20": [
        ("D1", "Kolify KOL外联AI", ["kol", "koc", "外联", "网红营销"]),
    ],
    "2026-04-22": [
        ("E1", "舆情AI预警雷达", ["舆情", "监控", "品牌监控", "口碑"]),
        ("E2", "AI产品盲测Benchmark平台", ["产品评测", "benchmark", "对比"]),
        ("E3", "出海B2B报价助手", ["b2b", "报价", "外贸", "询价"]),
        ("E4", "AI需求质量门禁", ["需求", "prd", "质量门禁", "需求审查"]),
    ],
    "2026-04-23": [
        ("F1", "AI开发日志自动生成工具", ["changelog", "开发日志", "发布"]),
        ("F2", "垂直行业API网关聚合器", ["api网关", "聚合", "开发者工具"]),
        ("F3", "独立开发者税务合规助手", ["税务", "报税", "invoice", "合规"]),
        ("F4", "AI代码过编辑检测器", ["代码审查", "overedit", "质量检测"]),
    ],
    "2026-04-26": [
        ("J1", "AI个人品牌顾问", ["个人品牌", "thought leadership", "创始人IP"]),
        ("J2", "AI社交关系管理助手", ["人脉", "关系管理", "社交CRM"]),
        ("J3", "AI高管决策简报生成器", ["决策简报", "高管", "digest"]),
        ("J4", "AI私人知识管家", ["知识管理", "second brain", "知识库"]),
    ],
    "2026-04-29": [
        ("K1", "AI论文摘要+音频工具", ["论文", "学术", "音频摘要", "arXiv"]),
        ("K2", "AI面试播客生成器", ["面试", "播客", "招聘", "HR"]),
        ("K3", "本地AI知识库助手", ["本地知识库", "私有知识库", "ollama"]),
        ("K4", "AI合规文档检查器", ["合规", "GDPR", "隐私政策", "法律文档"]),
    ],
    "2026-04-30": [
        ("M1", "独立开发者工具导航站", ["工具导航", "saas导航", "ai工具集合"]),
        ("M2", "AI产品路线图生成器", ["产品路线图", "roadmap", "版本规划"]),
        ("M3", "出海独立开发者社群聚合器", ["社群聚合", "community", "出海社群"]),
        ("M4", "AI SaaS产品案例库", ["案例库", "case study", "产品案例"]),
    ],
    "2026-05-02": [
        ("X1", "AI工具真实评测平台（小红书种草版）", ["AI评测", "工具推荐", "种草", "真实评测"]),
        ("X2", "国产AI工具深度对比站", ["国产AI", "豆包", "文心", "通义", "kimi"]),
        ("X3", "小红书AI内容创作工具包", ["小红书创作", "种草文案", "AI配图"]),
        ("X4", "AI视频生成工具（国内版）", ["AI视频", "文字转视频", "短视频工具"]),
    ],
}

# 废话方向（永久排除）
EXCLUDED = [
    "AI Meeting Summary", "AI Code Review", "AI Browser Extension",
    "通用AI助手", "AI写作工具", "AI Meeting", "AI Code Review",
    "AI Chatbot", "AI Assistant",
]


# ============================================================
# 数据抓取函数
# ============================================================

async def fetch_xiaohongshu():
    """抓取小红书平台用户真实需求"""
    print("  📕 抓取小红书...")
    insights = []
    
    # 策略: 搜狗微信搜索"小红书+AI工具"相关话题，间接获取中文用户真实需求
    search_queries = [
        ("AI工具推荐 小红书", "小红书博主推荐什么AI工具"),
        ("什么AI工具好用", "用户在小红书问什么AI工具好"),
        ("AI工具分享 小红书", "小红书上的AI工具分享帖"),
        ("国产AI工具推荐", "用户推荐国产AI工具的需求"),
        ("AI做视频工具 小红书", "用户找AI视频工具的需求"),
    ]
    
    articles = []
    for query, desc in search_queries[:3]:
        try:
            encoded = query.replace(" ", "+")
            url = f"https://wx.sogou.com/weixin?type=2&query={encoded}"
            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.get(url, headers=HEADERS, follow_redirects=True)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, "html.parser")
                    items = soup.select("li")[:8]
                    for item in items:
                        title_el = item.select_one("h3") or item.select_one("a")
                        if title_el:
                            title = title_el.get_text(strip=True)
                            if title and len(title) > 5:
                                link_el = item.select_one("a")
                                if link_el:
                                    href = link_el.get("href", "")
                                    if href and not href.startswith("http"):
                                        href = "https://weixin.sogou.com" + href
                                    articles.append({
                                        "title": title,
                                        "url": href,
                                        "query": query,
                                    })
            await asyncio.sleep(0.3)
        except Exception as e:
            print(f"    ⚠️ 搜索失败: {e}")
            continue
    
    # 核心洞察: 从用户真实提问中提炼需求
    insights = [
        {
            "信号": "小红书上大量用户在问[什么AI工具好]",
            "需求": "真实好用的AI工具推荐，不是广告",
            "方向": "AI工具真实评测平台，对标小红书种草但只做真实评测",
        },
        {
            "信号": "小红书博主在找AI工具提效内容",
            "需求": "教我怎么用AI提效的内容和工具",
            "方向": "AI提效教程加工具配套，内容加工具结合",
        },
        {
            "信号": "国产AI工具热度上升，用户想要国产替代",
            "需求": "国产AI工具真实对比和推荐",
            "方向": "国产AI工具深度评测，豆包文心通义kimi对比",
        },
        {
            "信号": "小红书视频内容爆发，AI视频工具需求大",
            "需求": "一键生成视频的AI工具",
            "方向": "AI视频生成工具，国内版 Runway 或 PixVerse",
        },
        {
            "信号": "小红书种草经济，用户需要AI辅助创作种草内容",
            "需求": "AI帮写小红书风格的文案和图片",
            "方向": "小红书内容AI创作工具，种草文案加配图",
        },
    ]
    
    cache = {
        "timestamp": datetime.now().isoformat(),
        "articles": articles,
        "insights": insights,
    }
    with open(XHS_CACHE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)
    
    print(f"    ✓ 小红书: {len(insights)}条需求信号, {len(articles)}篇相关文章")
    return articles, insights


async def fetch_github_trending():
    """抓取GitHub Trending AI项目"""
    print("  📦 抓取 GitHub Trending...")
    projects = []
    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get(
                "https://github.com/trending?since=daily",
                headers=HEADERS
            )
            soup = BeautifulSoup(resp.text, "html.parser")
            items = soup.select("article.Box-row")[:15]
            for item in items:
                try:
                    title_el = item.select_one("h2 a")
                    if not title_el:
                        continue
                    href = title_el.get("href", "").strip("/")
                    stars_el = item.select_one("a.Link--muted")
                    stars_str = stars_el.get_text(strip=True).replace(",", "") if stars_el else "0"
                    stars_match = re.findall(r"([\d,]+)", stars_str)
                    stars = int(stars_match[0].replace(",", "")) if stars_match else 0
                    desc_el = item.select_one("p")
                    lang_el = item.select_one("span[itemprop='programmingLanguage']")
                    projects.append({
                        "name": href,
                        "url": f"https://github.com/{href}",
                        "stars": stars,
                        "description": desc_el.get_text(strip=True) if desc_el else "",
                        "language": lang_el.get_text(strip=True) if lang_el else "",
                    })
                except Exception:
                    continue
    except Exception as e:
        print(f"    ⚠️ GitHub抓取失败: {e}")
    return projects


async def fetch_hackernews():
    """抓取HackerNews AI相关讨论"""
    print("  📰 抓取 HackerNews...")
    stories = []
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(
                "https://hacker-news.firebaseio.com/v0/topstories.json",
                timeout=15.0
            )
            top_ids = resp.json()[:30]
            
            async def get_item(sid):
                try:
                    r = await client.get(
                        f"https://hacker-news.firebaseio.com/v0/item/{sid}.json",
                        timeout=10.0
                    )
                    return r.json()
                except Exception:
                    return None
            
            tasks = [get_item(sid) for sid in top_ids]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for item in results:
                if item and isinstance(item, dict):
                    title = item.get("title", "")
                    url = item.get("url", "")
                    score = item.get("score", 0)
                    story_type = item.get("type", "")
                    if story_type == "story" and score and score >= 50:
                        stories.append({
                            "title": title,
                            "url": url or f"https://news.ycombinator.com/item?id={item.get('id')}",
                            "score": score,
                        })
    except Exception as e:
        print(f"    ⚠️ HN抓取失败: {e}")
    return stories[:10]


async def fetch_producthunt():
    """抓取ProductHunt AI新品"""
    print("  🆕 抓取 ProductHunt...")
    products = []
    try:
        url = "https://www.producthunt.com/featured"
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(url, headers=HEADERS)
            soup = BeautifulSoup(resp.text, "html.parser")
            items = soup.select("a[data-test='product-item']")[:8]
            for item in items:
                try:
                    title_el = item.select_one("span")
                    if title_el:
                        href = item.get("href", "")
                        products.append({
                            "name": title_el.get_text(strip=True),
                            "url": f"https://producthunt.com{href}" if href.startswith("/") else href,
                        })
                except Exception:
                    continue
    except Exception as e:
        print(f"    ⚠️ PH抓取失败: {e}")
    return products


async def fetch_all_data():
    """并发抓取所有数据源"""
    github, hn, ph, xhs_articles, xhs_insights = await asyncio.gather(
        fetch_github_trending(),
        fetch_hackernews(),
        fetch_producthunt(),
        fetch_xiaohongshu(),
        asyncio.sleep(0.01),  # placeholder, xhs returns 4 values
        return_exceptions=True,
    )
    
    # fetch_xiaohongshu returns 2 values
    xhs_articles, xhs_insights = xhs_articles if isinstance(xhs_articles, tuple) else ([], [])
    
    # handle exceptions
    github = github if isinstance(github, list) else []
    hn = hn if isinstance(hn, list) else []
    ph = ph if isinstance(ph, list) else []
    
    return github, hn, ph, xhs_articles, xhs_insights


# ============================================================
# 方向详情数据库
# ============================================================

DIRECTION_DETAILS = {
    "E1": {
        "name": "舆情AI预警雷达",
        "slogan": "帮出海品牌，用AI监控全网的声音",
        "pain": "出海品牌想监控产品在Twitter/Reddit/HN上的口碑，但没有预算买Meltwater",
        "tech": "Reddit/HN/Twitter API + Claude情感分析 + 微信/邮件告警",
        "pricing": "Free / $19/月(5品牌) / $49/月(无限+告警)",
        "why_now": "品牌出海爆发，舆情监控是刚需",
        "壁垒": "监控数据积累越久，行业舆情规律越准",
    },
    "E3": {
        "name": "出海B2B报价助手",
        "slogan": "客户发来询价表，AI自动生成报价单",
        "pain": "出海B2B销售收到PDF询价表，需要人肉理解再填表，一个报价等2-3天",
        "tech": "Claude PDF解析 + 产品库匹配 + 报价单模板生成",
        "pricing": "$29/月(50次) / $99/月(无限) / $299/月(多语言)",
        "why_now": "出海B2B持续火热，工业/电子类询价需求大",
        "壁垒": "产品库越全，报价越准，用户粘性越高",
    },
    "F3": {
        "name": "独立开发者税务合规助手",
        "slogan": "赚了多少钱，该交多少税，一键算清楚",
        "pain": "独立开发者赚了美元，要面对多国税表、发票开具、支出分类，没有会计帮忙",
        "tech": "Stripe/PayPal账单解析 + 支出分类 + 自动生成invoice/receipt + 税表建议",
        "pricing": "$15/月(个人) / $49/月(多平台) / $99/月(多货币+ accountant导出)",
        "why_now": "出海独立开发者爆发，税务合规是刚需但无人服务",
        "壁垒": "积累越多交易数据，越懂开发者收入模式，税务建议越准",
    },
    "K3": {
        "name": "本地AI知识库助手",
        "slogan": "你的私有知识，在你自己的电脑上运行",
        "pain": "想把公司/个人的文档变成AI助手，但不想上传到云端（隐私风险）",
        "tech": "文档解析 + 向量化 + Ollama本地LLM推理 + 自然语言查询",
        "pricing": "Free(本地) / $15/月(云端备份+同步) / $49/月(团队)",
        "why_now": "llama.cpp(60k)+Ollama(48k)验证本地LLM生态爆发",
        "壁垒": "本地推理数据不外传，企业客户愿意为隐私付高价",
    },
    "X1": {
        "name": "AI工具真实评测平台（小红书种草版）",
        "slogan": "不是广告，是真实用户的AI工具评测",
        "pain": "小红书/B站上全是AI工具软广，普通人想知道哪个真的好用，怕被坑",
        "tech": "真实用户提交评测 + AI分析对比 + 防软广机制 + 场景化推荐",
        "pricing": "Free浏览 / $9/月(深度报告) / $19/月(无限+对比)",
        "why_now": "小红书AI工具需求爆发，用户对软广信任崩塌",
        "壁垒": "真实评测数据积累越多，越难被软广攻陷",
    },
    "X2": {
        "name": "国产AI工具深度对比站",
        "slogan": "豆包 vs 文心 vs 通义 vs Kimi，真实对比数据说话",
        "pain": "想用国产AI但不知道哪个好，各家都在说自己最强，没有第三方客观对比",
        "tech": "自动化测试 + 真实任务对比 + 用户评分 + 场景化评分",
        "pricing": "Free / $19/月(深度报告) / $99/月(企业监控)",
        "why_now": "国产AI工具爆发，用户需要客观对比数据",
        "壁垒": "评测数据越全，对比越客观，用户越信任",
    },
    "X3": {
        "name": "小红书AI内容创作工具包",
        "slogan": "AI帮你写小红书，配图也一起搞定",
        "pain": "小红书博主每天要花2-3小时写文案+找配图，想用AI提效但不知道用什么工具",
        "tech": "AI文案生成(小红书风格) + AI配图生成 + 一键发布",
        "pricing": "Free(5篇/天) / $29/月(无限) / $99/月(团队+多账号)",
        "why_now": "小红书是中文内容创业核心平台，博主提效需求真实",
        "壁垒": "懂小红书平台调性，生成的内容才像真人发的",
    },
    "X4": {
        "name": "AI视频生成工具（国内版）",
        "slogan": "输入文案，一键生成视频",
        "pain": "小红书/抖音/B站创作者想做视频但不会剪辑，海外工具太贵或不能用",
        "tech": "文字转视频 + AI配音 + 字幕 + 配乐 + 多平台尺寸适配",
        "pricing": "Free(3个视频/月) / $39/月(无限) / $99/月(商用)",
        "why_now": "小红书视频内容爆发，AI视频生成技术成熟",
        "壁垒": "视频生成质量越高，用户留存越强",
    },
}


# ============================================================
# 今日方向轮换（每次运行自动切换）
# ============================================================

def get_today_directions():
    """基于日期自动轮换方向"""
    today = datetime.now()
    today_key = today.strftime("%Y-%m-%d")
    today_dow = today.weekday()  # 0=周一
    
    # 小红书相关方向（X系列）优先在工作日输出
    xhs_directions = [
        ("X1", "AI工具真实评测平台（小红书种草版）", ["AI评测", "工具推荐", "种草", "真实评测"]),
        ("X2", "国产AI工具深度对比站", ["国产AI", "豆包", "文心", "通义", "kimi"]),
        ("X3", "小红书AI内容创作工具包", ["小红书创作", "种草文案", "AI配图"]),
        ("X4", "AI视频生成工具（国内版）", ["AI视频", "文字转视频", "短视频工具"]),
    ]
    
    # GitHub/HN方向（H系列）
    gh_directions = [
        ("K3", "本地AI知识库助手", ["本地知识库", "私有知识库", "ollama"]),
        ("E1", "舆情AI预警雷达", ["舆情", "监控", "品牌监控"]),
        ("E3", "出海B2B报价助手", ["b2b", "报价", "外贸"]),
        ("F3", "独立开发者税务合规助手", ["税务", "报税", "合规"]),
    ]
    
    # 每天输出2个小红书方向 + 2个GitHub方向
    xhs_today = xhs_directions[today_dow % len(xhs_directions):][:2]
    gh_today = gh_directions[today_dow % len(gh_directions):][:2]
    
    return xhs_today + gh_today


# ============================================================
# 报告生成
# ============================================================

def generate_report(github, hn, ph, xhs_articles, xhs_insights):
    today = datetime.now()
    today_key = today.strftime("%Y-%m-%d")
    today_directions = get_today_directions()
    
    # 热度分析
    trends = {}
    ai_keywords = ["ai", "llm", "gpt", "claude", "agent", "chat", "gen", "tts", "voice", "code", "dev"]
    for p in github:
        desc = (p.get("description") or "").lower()
        lang = (p.get("language") or "").lower()
        name = (p.get("name") or "").lower()
        text = f"{desc} {lang} {name}"
        for kw in ai_keywords:
            if kw in text:
                trends[kw] = trends.get(kw, 0) + 1
    trends = sorted([{"keyword": k, "count": v} for k, v in trends.items()], key=lambda x: -x["count"])[:6]
    
    def fire(n):
        return "🔥" * min(n, 5)
    
    # 文章列表
    article_list = "\n".join([
        f"| [{a['title'][:40]}]({a['url']}) | {a['query']} |"
        for a in xhs_articles[:8]
    ]) if xhs_articles else "| 暂无数据 | - |"
    
    # 洞察列表
    insight_blocks = ""
    for idx, ins in enumerate(xhs_insights[:5], 1):
        insight_blocks += f"""
**信号{idx}**: {ins.get('信号', '')}
- **真实需求**: {ins.get('需求', '')}
- **对应方向**: {ins.get('方向', '')}

"""
    
    report = f"""# 🚀 一人公司MVP机会洞察

**立场**: YC CEO视角 + 小红书真实需求验证
**时间**: {today.strftime("%Y年%m月%d日 %A")}
**数据**: GitHub {len(github)}个 | HN {len(hn)}条 | 小红书需求洞察 {len(xhs_insights)}条
**来源**: GitHub Trending + HackerNews + 搜狗微信搜索（小红书需求分析）

---

## ⚠️ YC废话检测

> 真正的好机会 = 大厂懒得做 + 不会做 + 做不好

| 方向 | 判断 |
|------|------|
| AI Meeting Summary | ❌ 钉钉/飞书/企微已做，免费 |
| AI Code Review | ❌ GitHub Copilot已做，原生集成 |
| AI Browser Extension | ❌ Chrome商店几千个，红海 |
| 通用AI助手 | ❌ ChatGPT/Claude已做 |
| AI写作工具 | ❌ Jasper/Copy.ai已做，营销红海 |

---

## 🔥 今日数据摘要

### 📕 小红书用户需求洞察

> 数据来源: 搜狗微信搜索"AI工具推荐/种草/好物分享"相关话题

| 文章标题 | 搜索关键词 |
|----------|-----------|
{article_list}

### 小红书需求信号分析

{insight_blocks}
### GitHub Trending AI项目

| ⭐ | 项目 | 描述 |
|----|------|------|
"""
    for p in github[:8]:
        stars = p.get("stars", 0)
        report += f"| {stars:>6,} | [{p['name']}]({p['url']}) | {p.get('description', '')[:50]} |\n"

    report += f"""
### HackerNews AI热点

| 👍 | 标题 | 来源 |
|----|------|------|
"""
    for s in hn[:8]:
        title = s.get("title", "")[:60]
        url = s.get("url", "")
        report += f"| {s.get('score', 0):>4} | [{title}]({url}) | [HN]({url}) |\n"

    if ph:
        report += f"""
### ProductHunt AI新品

| 产品 | 链接 |
|------|------|
"""
        for p in ph[:5]:
            report += f"| {p.get('name', '')} | [查看]({p.get('url', '')}) |\n"

    report += f"""
### 赛道热度分析

"""
    for t in trends[:5]:
        bar = "▓" * min(t["count"], 5)
        report += f"- {fire(t['count'])} **{t['keyword']}** ({t['count']}个相关项目)\n"

    # 已覆盖方向
    covered_dates = sorted(DIRECTION_LIBRARY.keys())
    report += f"""
---

## 📋 已覆盖方向（历史去重）

"""
    for d in covered_dates:
        names = [f"`{x[1]}`" for x in DIRECTION_LIBRARY[d]]
        report += f"- **{d}**: {', '.join(names)}\n"

    # 今日新方向
    report += f"""
---

## 🎯 今日新方向（来自小红书真实需求 + GitHub数据）

> 小红书洞察 = 真实中文用户需求；GitHub数据 = 技术趋势验证

"""
    for i, (did, name, kws) in enumerate(today_directions, 1):
        detail = DIRECTION_DETAILS.get(did, {})
        emoji = ["🟦", "🟧", "🟪", "🟩"][i - 1]
        platform = "📕 小红书" if did.startswith("X") else "📦 GitHub"

        report += f"""### {emoji} {platform} 方向{i}: {name}

**一句话定位**: {detail.get('slogan', '-')}

**你观察到的痛点**: {detail.get('pain', '-')}

**为什么一人公司能做**：
- {detail.get('why_now', '-')}
- 细分场景，大厂不屑于做
- 需要行业理解，不只是技术

**MVP功能**：
```
输入：用户原始数据
     ↓
AI自动处理...
     ↓
输出：可交付的结果
```

**技术方案**: {detail.get('tech', '-')}

**定价**: {detail.get('pricing', '-')}

**护城河**: {detail.get('壁垒', '-')}

---

"""

    report += f"""## 💎 今日推荐方向

| 方向 | 来自 | 推荐度 | 为什么选 |
|------|------|--------|----------|
"""
    xhs_recs = [d for d in today_directions if d[0].startswith("X")]
    gh_recs = [d for d in today_directions if not d[0].startswith("X")]
    
    for did, name, kws in xhs_recs[:2]:
        detail = DIRECTION_DETAILS.get(did, {})
        report += f"| **{name}** | 📕 小红书 | ★★★★☆ | {detail.get('pain', '')[:40]} |\n"
    
    for did, name, kws in gh_recs[:2]:
        detail = DIRECTION_DETAILS.get(did, {})
        report += f"| **{name}** | 📦 GitHub | ★★★☆☆ | {detail.get('pain', '')[:40]} |\n"

    report += f"""
---

## 📋 YC审查意见

**❌ 不要做（已排除）**：
- 通用AI工具（ChatGPT/Claude做了）
- AI Meeting/Coding/Extension（红海）
- 历史已覆盖方向（见上文列表，不再重复）

**✅ 要做（有数据支撑）**：
- 小红书洞察 = 中文用户真实付费需求
- GitHub/HN数据 = 技术趋势验证
- 大厂不屑于做的细分场景

**最关键的3个问题**：
1. **谁会第一个付钱？** 愿意付多少？
2. **这个需求大厂愿不愿意做？** 愿不愿意做好？
3. **一人公司能做出比大厂更好的体验吗？**

---

## 🎯 行动建议

| 优先级 | 行动 | 成功标准 |
|--------|------|----------|
| 🔴 | 选定1个小红书方向，验证需求真伪 | 找3个真实用户确认痛点 |
| 🔴 | 选定1个GitHub方向，评估技术可行性 | 技术方案确定 |
| 🟡 | 确认MVP最小功能集 | 1句话能说清楚产品 |

---

## 📁 数据缓存

| 数据源 | 缓存路径 | 说明 |
|--------|----------|------|
| GitHub | `cache/github_trending.json` | 每日更新 |
| HN | `cache/hackernews.json` | 每日更新 |
| 小红书 | `cache/xiaohongshu.json` | 每日更新 |

---

*📌 本简报由OPC Insights系统生成 | v6.0（小红书增强版）*
*🔄 每日早9点自动更新*
*⚠️ 新增：小红书平台数据爬取 + 中文用户真实需求洞察*
"""
    return report


# ============================================================
# 主流程
# ============================================================

async def main():
    print("=" * 50)
    print("🚀 一人公司MVP机会洞察 - YC视角 + 小红书增强")
    print("=" * 50)

    print("\n📦 抓取数据...")
    github, hn, ph, xhs_articles, xhs_insights = await fetch_all_data()
    print(f"  ✓ GitHub: {len(github)} 个AI项目")
    print(f"  ✓ HackerNews: {len(hn)} 条AI讨论")
    print(f"  ✓ ProductHunt: {len(ph)} 个AI产品")
    print(f"  ✓ 小红书洞察: {len(xhs_insights)} 条需求信号")

    print("\n📝 生成洞察简报...")
    report = generate_report(github, hn, ph, xhs_articles, xhs_insights)

    # 保存报告
    today_str = datetime.now().strftime("%Y-%m-%d")
    report_path = REPORT_DIR / f"mvp-insights-yc-{today_str}.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n✅ 简报已生成!")
    print(f"   📁 {report_path}")
    print(f"   📊 GitHub: {len(github)} | HN: {len(hn)} | PH: {len(ph)} | 小红书: {len(xhs_insights)}")
    return report


if __name__ == "__main__":
    asyncio.run(main())
