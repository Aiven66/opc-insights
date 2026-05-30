#!/usr/bin/env python3
"""
OPC一人公司MVP洞察简报生成器 v5.0
特性: 多数据源(GitHub/HN/ProductHunt) + 智能去重 + 方向轮换 + YC CEO视角
"""

import httpx, asyncio, json, re, os
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36'}
REPORT_DIR = Path(__file__).parent.parent / "reports"
CACHE_DIR  = Path(__file__).parent.parent / "cache"
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
        ("B3", "ChatTTS声优工厂", ["chattts", "语音克隆", "配音"]),
    ],
    "2026-04-17": [
        ("C1", "SkillsHunt技能发现平台", ["skills", "skill hunt", "agent marketplace", "技能市场"]),
    ],
    "2026-04-20": [
        ("D1", "Kolify KOL外联AI", ["kol", "influencer", "外联", "tiktok", "网红营销"]),
    ],
    "2026-04-22": [
        ("E1", "舆情AI预警雷达", ["舆情监控", "social listening", "品牌监测", "trendradar"]),
        ("E2", "AI产品盲测Benchmark", ["ai产品评测", "benchmark", "产品对比", "替代推荐"]),
        ("E3", "出海B2B报价助手", ["b2b报价", "询价", "采购", "报价单生成"]),
        ("E4", "AI需求质量门禁", ["需求质量", "prd审查", "需求审查"]),
    ],
    "2026-04-23": [
        ("F1", "AI开发日志自动生成工具", ["devlog", "开发日志", "commit message", "changelog"]),
        ("F2", "垂直行业API网关聚合器", ["api聚合", "api gateway", "集成中间件", "webhook"]),
        ("F3", "独立开发者税务合规助手", ["税务", "报税", "独立开发者", "invoice", "receipt"]),
        ("F4", "AI代码过编辑检测器", ["ai coding", "over-editing", "代码质量", "cursor", "zed"]),
    ],
    "2026-04-26": [
        ("J1", "AI个人品牌顾问", ["personal branding", "个人品牌", "thought leadership", "创始人IP", "高管形象"]),
        ("J2", "AI社交关系管理助手", ["relationship management", "人脉管理", "networking", "社交CRM", "重要关系维护"]),
        ("J3", "AI高管决策简报生成器", ["executive briefing", "决策简报", "daily digest", "信息过滤", "高管阅读"]),
        ("J4", "AI私人知识管家", ["knowledge management", "知识管理", "second brain", "阅读摘要", "个人知识库"]),
    ],
    "2026-04-30": [
        ("M1", "独立开发者工具导航站", ["工具导航", "saas导航", "ai工具集合", "独立开发者资源"]),
        ("M2", "AI产品路线图生成器", ["产品路线图", "roadmap generator", "changelog", "版本规划"]),
        ("M3", "出海独立开发者社群聚合器", ["社群聚合", "community aggregator", "独立开发者", "出海社群"]),
        ("M4", "AI SaaS产品案例库", ["案例库", "case study", "saas案例", "product examples"]),
    ],
}

# 废话方向（永久排除）
EXCLUDED = [
    "AI Meeting Summary", "AI Code Review", "AI Browser Extension",
    "通用AI助手", "AI写作工具", "AI Meeting", "AI Code Review",
    "AI Chatbot", "AI Assistant",
]

# 热门AI关键词（用于筛选GitHub/HN数据）
AI_KEYWORDS = [
    'ai','gpt','llm','agent','chatbot','claude','cursor','video',
    'content','writing','automation','rag','model','copilot','api',
    'image','voice','speech','search','assistant','automation','tool',
]


def get_covered_keywords() -> set:
    """从历史方向库提取关键词，用于过滤数据"""
    covered = set()
    for dirs in DIRECTION_LIBRARY.values():
        for _, name, kws in dirs:
            covered.add(name.lower())
            for kw in kws:
                covered.update(kw.lower().split())
    return covered


def get_today_directions():
    """获取今日应输出的方向（优先用当天，否则轮换）"""
    today = datetime.now().strftime("%Y-%m-%d")
    if today in DIRECTION_LIBRARY:
        return DIRECTION_LIBRARY[today]
    # 找最近一个有方向的日期
    dates = sorted(DIRECTION_LIBRARY.keys(), reverse=True)
    for d in dates:
        if d < today:
            return DIRECTION_LIBRARY[d]
    return []


def get_history_summary():
    """生成历史已覆盖方向摘要（用于报告去重说明）"""
    lines = ["\n已排除方向（历史简报已覆盖，不再重复输出）："]
    for date in sorted(DIRECTION_LIBRARY.keys()):
        names = [d[1] for d in DIRECTION_LIBRARY[date]]
        lines.append(f"- **{date}**: {', '.join(names)}")
    return "\n".join(lines)


# ============================================================
# 数据抓取
# ============================================================

async def fetch_github_trending(client) -> list:
    """抓取GitHub Trending AI相关项目"""
    cache_file = CACHE_DIR / "github_trending.json"
    # 缓存1小时
    if cache_file.exists():
        age = datetime.now() - datetime.fromtimestamp(cache_file.stat().st_mtime)
        if age.seconds < 3600:
            with open(cache_file) as f:
                raw = json.load(f)
                # 兼容旧格式 {"items":[...]} 和新格式 [...]
                if isinstance(raw, dict) and "items" in raw:
                    return raw["items"]
                elif isinstance(raw, list):
                    return raw
                return []

    try:
        r = await client.get("https://github.com/trending?since=daily", headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        repos = soup.select("article.Box-row")
        items = []
        for repo in repos:
            title_el = repo.select_one("h2 a")
            if not title_el:
                continue
            name = title_el.get("href", "").strip("/")
            desc_el = repo.select_one("p")
            desc = desc_el.text.strip() if desc_el else ""
            stars_el = repo.select_one('a[href$="/stargazers"]')
            stars_str = stars_el.text.strip().replace(",", "").replace("*", "").replace(" ", "") if stars_el else "0"
            # Handle "48k" format
            stars_raw = re.sub(r"[^\d.]", "", stars_str)
            if "k" in stars_str.lower():
                stars = int(float(stars_raw) * 1000) if stars_raw else 0
            else:
                stars = int(stars_raw) if stars_raw else 0

            full_text = (name + " " + desc).lower()
            if any(k in full_text for k in AI_KEYWORDS):
                items.append({
                    "name": name,
                    "desc": desc[:100],
                    "stars": stars,
                    "url": f"https://github.com/{name}",
                })

        items.sort(key=lambda x: x["stars"], reverse=True)
        with open(cache_file, "w") as f:
            json.dump(items[:15], f)
        return items[:15]
    except Exception as e:
        print(f"  ⚠️ GitHub抓取失败: {e}")
        if cache_file.exists():
            with open(cache_file) as f:
                raw = json.load(f)
                if isinstance(raw, dict) and "items" in raw:
                    return raw["items"]
                elif isinstance(raw, list):
                    return raw
        return []


async def fetch_hackernews(client) -> list:
    """抓取HackerNews AI相关讨论"""
    cache_file = CACHE_DIR / "hackernews.json"
    if cache_file.exists():
        age = datetime.now() - datetime.fromtimestamp(cache_file.stat().st_mtime)
        if age.seconds < 3600:
            with open(cache_file) as f:
                raw = json.load(f)
                if isinstance(raw, list):
                    return raw[:10]
                elif isinstance(raw, dict) and "items" in raw:
                    return raw["items"][:10]
                return []

    try:
        r = await client.get("https://hacker-news.firebaseio.com/v0/topstories.json", timeout=10)
        ids = json.loads(r.text)[:30]
        items = []
        for sid in ids:
            sr = await client.get(f"https://hacker-news.firebaseio.com/v0/item/{sid}.json", timeout=5)
            s = json.loads(sr.text)
            if not s:
                continue
            title = s.get("title", "")
            if any(k in title.lower() for k in AI_KEYWORDS):
                items.append({
                    "title": title,
                    "url": s.get("url", ""),
                    "hn_url": f"https://news.ycombinator.com/item?id={sid}",
                    "score": s.get("score", 0),
                    "comments": s.get("descendants", 0),
                })
        items.sort(key=lambda x: x["score"], reverse=True)
        with open(cache_file, "w") as f:
            json.dump(items[:10], f)
        return items[:10]
    except Exception as e:
        print(f"  ⚠️ HN抓取失败: {e}")
        if cache_file.exists():
            with open(cache_file) as f:
                raw = json.load(f)
                if isinstance(raw, list):
                    return raw
        return []


async def fetch_producthunt(client) -> list:
    """抓取ProductHunt AI相关产品"""
    cache_file = CACHE_DIR / "producthunt.json"
    if cache_file.exists():
        age = datetime.now() - datetime.fromtimestamp(cache_file.stat().st_mtime)
        if age.seconds < 7200:  # 2小时缓存
            with open(cache_file) as f:
                raw = json.load(f)
                if isinstance(raw, list):
                    return raw
                return []

    try:
        # ProductHunt需要API，这里用网页抓取（JS渲染页面，准确率低，参考为主）
        r = await client.get(
            "https://www.producthunt.com/",
            headers={**HEADERS, "Accept-Language": "en-US"},
            timeout=10,
        )
        soup = BeautifulSoup(r.text, "html.parser")
        items = []
        # ProductHunt页面是JS渲染的，静态抓取可能不准
        posts = soup.select('[data-test="post-card"]')[:10]
        for p in posts:
            title_el = p.select_one('[data-test="post-title"]') or p.select_one("a")
            if title_el:
                title = title_el.text.strip()
                href = p.select_one("a").get("href", "") if p.select_one("a") else ""
                items.append({
                    "title": title,
                    "url": f"https://producthunt.com{href}" if href.startswith("/") else href,
                })

        if items:
            with open(cache_file, "w") as f:
                json.dump(items, f)
        return items
    except Exception as e:
        print(f"  ⚠️ PH抓取失败: {e}")
        if cache_file.exists():
            with open(cache_file) as f:
                return json.load(f)
        return []


async def fetch_all_data():
    """并发抓取所有数据源"""
    async with httpx.AsyncClient(headers=HEADERS, timeout=30) as client:
        tasks = [
            fetch_github_trending(client),
            fetch_hackernews(client),
            fetch_producthunt(client),
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        github = results[0] if not isinstance(results[0], Exception) else []
        hn = results[1] if not isinstance(results[1], Exception) else []
        ph = results[2] if not isinstance(results[2], Exception) else []
        return github, hn, ph


# ============================================================
# 数据分析
# ============================================================

def analyze_trends(github: list, hn: list) -> dict:
    """分析GitHub/HN数据中的赛道热度"""
    # 统计关键词出现频率
    kw_count = {}
    for item in github:
        if not isinstance(item, dict):
            continue
        text = (item.get("name", "") + " " + item.get("description", "")).lower()
        for kw in ["agent", "coding", "rag", "video", "image", "voice", "chatbot", "api", "tool", "search"]:
            if kw in text:
                kw_count[kw] = kw_count.get(kw, 0) + 1

    for item in hn:
        if not isinstance(item, dict):
            continue
        text = item.get("title", "").lower()
        for kw in ["agent", "coding", "llm", "ai", "model", "copilot", "video", "image"]:
            if kw in text:
                kw_count[kw] = kw_count.get(kw, 0) + 1

    # 排序返回
    sorted_kw = sorted(kw_count.items(), key=lambda x: x[1], reverse=True)
    return [{"keyword": k, "count": c} for k, c in sorted_kw[:8]]


def filter_new_github_items(github: list) -> list:
    """过滤GitHub数据，排除已覆盖方向"""
    covered = get_covered_keywords()
    filtered = []
    for item in github:
        if not isinstance(item, dict):
            continue
        text = (item.get("name", "") + " " + item.get("description", "")).lower()
        is_covered = any(c in text for c in covered)
        if not is_covered:
            filtered.append(item)
    return filtered[:8]


# ============================================================
# 报告生成
# ============================================================

def generate_report(github: list, hn: list, ph: list) -> str:
    """生成完整简报"""
    today = datetime.now()
    today_str = today.strftime("%Y年%m月%d日")
    today_key = today.strftime("%Y-%m-%d")
    today_short = today.strftime("%m-%d")
    weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][today.weekday()]

    today_directions = get_today_directions()
    trends = analyze_trends(github, hn)
    new_github = filter_new_github_items(github)

    # 热力emoji
    fire = lambda n: "🔥" * min(n, 5)

    report = f"""# 🚀 一人公司MVP机会洞察

**立场**: YC CEO视角审查
**时间**: {today_str}（{weekday}）
**数据**: GitHub {len(github)}个AI项目 | HN {len(hn)}个AI讨论 | PH {len(ph)}个产品
**来源**: GitHub Trending + HackerNews + ProductHunt（今日实时抓取）

---

## ⚠️ 先说核心问题：哪些是废话

> 真正的好机会，是大厂懒得做、不会做、做不好的事情。

| 方向 | 为什么是废话 | 判断 |
|------|-------------|------|
| AI Meeting Summary | 钉钉/飞书/企微已做，免费 | ❌ NO |
| AI Code Review | GitHub Copilot已做，原生集成 | ❌ NO |
| AI Browser Extension | Chrome商店几千个，红海 | ❌ NO |
| 通用AI助手 | ChatGPT/Claude已做，做不过 | ❌ NO |
| AI写作工具 | Jasper/Copy.ai已做，营销红海 | ❌ NO |

**判断标准**：这个方向大厂愿不愿意做？愿不愿意做好？

---

## 🔥 今日数据摘要

### GitHub Trending AI项目

| ⭐ | 项目 | 描述 | 洞察 |
|----|------|------|------|
"""

    for item in github[:8]:
        desc_short = item.get("description", "")[:50]
        stars_raw = item.get("stars", 0)
        if isinstance(stars_raw, str):
            stars_raw = re.sub(r"[^\d.]", "", stars_raw)
            stars = int(float(stars_raw) * 1000) if "k" in str(item.get("stars", "")).lower() else int(stars_raw) if stars_raw else 0
        else:
            stars = int(stars_raw)
        report += f"| {stars:>6} | [{item['name'].split('/')[-1]}]({item['url']}) | {desc_short} | |\n"

    report += f"""
### HackerNews AI热点

| 👍 | 标题 | 来源 |
|----|------|------|
"""

    for item in hn[:6]:
        title = item.get("title", "") or item.get("name", "")
        title_short = title[:60] + ("..." if len(title) > 60 else "")
        url = item.get("hn_url", "") or item.get("url", "")
        score = item.get("score", 0)
        report += f"| {score:>4} | [{title_short}]({url}) | [HN讨论]({url}) |\n"

    if ph:
        report += f"""
### ProductHunt AI新品

| 产品 | 链接 |
|------|------|
"""
        for item in ph[:5]:
            title = item.get("title", "") or item.get("name", "")
            url = item.get("url", "")
            report += f"| {title[:50]} | [查看]({url}) |\n"

    report += f"""
### 赛道热度分析

"""
    for t in trends[:5]:
        bar = "▓" * min(t["count"], 5)
        report += f"- {fire(t['count'])} **{t['keyword']}** ({t['count']}个相关项目)\n"

    report += f"""
---

## 📋 已覆盖方向（历史简报去重）

以下方向在历史简报中已深度分析，**本次不重复输出**：

"""

    covered_dates = sorted(DIRECTION_LIBRARY.keys())
    for d in covered_dates:
        if d < today_key:
            names = [f"`{x[1]}`" for x in DIRECTION_LIBRARY[d]]
            report += f"- **{d}**: {', '.join(names)}\n"

    report += f"""
---

## 🎯 今日新方向（{len(today_directions)}个，全新未输出）

"""

    # 为每个方向生成详细内容
    direction_details = {
        "E1": {
            "name": "舆情AI预警雷达",
            "slogan": "帮出海品牌，用AI监控全网的声",
            "pain": "出海品牌想监控产品在Twitter/Reddit/HN上的口碑，但没有预算买Meltwater",
            "tech": "Reddit/HN/Twitter API + Claude情感分析 + 微信/邮件告警",
            "pricing": "Free / $19/月(5品牌) / $49/月(无限+告警)",
            "why_now": "GitHub新上榜TrendRadar(53k⭐)验证了赛道需求",
            "壁垒": "监控数据积累 → 越用越懂行业舆情规律",
        },
        "E2": {
            "name": "AI产品盲测Benchmark平台",
            "slogan": "不做软文，只做真实对比",
            "pain": "用户被AI产品的营销软文淹没，不知道哪个真的好用",
            "tech": "用户匿名打分 + AI对比报告 + 替代推荐",
            "pricing": "Free浏览 / $9/月报告 / $99/月企业监控",
            "why_now": "HN热帖I'm Sick of AI Everything，说明用户对AI产品信任危机",
            "壁垒": "真实评分数据 → 最客观的AI产品数据库",
        },
        "E3": {
            "name": "出海B2B报价助手",
            "slogan": "客户发来询价表，AI自动生成报价单",
            "pain": "出海B2B销售收到PDF询价表，需要人肉理解再填表，一个报价等2-3天",
            "tech": "Claude PDF解析 + 产品库匹配 + 报价单模板生成",
            "pricing": "$29/月(50次) / $99/月(无限) / $299/月(多语言)",
            "why_now": "出海B2B持续火热，工业/电子类询价需求大",
            "壁垒": "产品库越全 → 报价越准 → 用户粘性越高",
        },
        "E4": {
            "name": "AI需求质量门禁",
            "slogan": "AI写代码之前，先让需求过审",
            "pain": "团队用AI编程后，需求文档被AI一天写出100条，质量参差不齐，开发疲于应付",
            "tech": "PRD审查 + 模糊性检测 + 规模评估 + 冲突检测",
            "pricing": "Free(5条/月) / $19/月无限 / $49/月团队协作",
            "why_now": "Cursor被$60B收购，AI编程工具爆发 → 需求质量痛点浮现",
            "壁垒": "懂产品逻辑 → 比代码审查更上游",
        },
        "F1": {
            "name": "AI开发日志自动生成工具",
            "slogan": "代码写完，日志自动生成发布",
            "pain": "独立开发者每次发版本都要花1-2小时写Changelog/DevLog，代码写完了还要憋文案",
            "tech": "Git提交记录解析 + AI生成 + 多平台格式适配（GitHub/ProductHunt/Twitter）",
            "pricing": "Free(1项目) / $9/月(5项目) / $29/月(无限)",
            "why_now": "独立开发者越来越多，每个人都需要发版传播，但写文案是重复劳动",
            "壁垒": "解析越多Git历史 → 越懂开发者的表达风格 → 生成越准确",
        },
        "F2": {
            "name": "垂直行业API网关聚合器",
            "slogan": "一个API密钥，连接所有服务",
            "pain": "开发者要用10个AI API，每个都要单独注册、计费、管理密钥，月底对账头疼",
            "tech": "统一API网关 + 智能路由(选最便宜/最快的) + 统一计费 + 用量分析",
            "pricing": "Free(基础) / $19/月(10万tokens) / $59/月(无限)+ 5%代理费",
            "why_now": "LangFuse(25k⭐)火爆说明LLM观测赛道热，API聚合是相邻需求",
            "壁垒": "接入越多API → 用户换平台成本越高 → 粘性越强",
        },
        "F3": {
            "name": "独立开发者税务合规助手",
            "slogan": "赚了多少钱，该交多少税，一键算清楚",
            "pain": "独立开发者赚了美元，要面对多国税表、发票开具、支出分类，没有会计帮忙",
            "tech": "Stripe/PayPal账单解析 + 支出分类 + 自动生成invoice/receipt + 税表建议",
            "pricing": "$15/月(个人) / $49/月(多平台) / $99/月(多货币+ accountant导出)",
            "why_now": "出海独立开发者爆发 → 税务合规是刚需但无人服务",
            "壁垒": "积累越多交易数据 → 越懂开发者收入模式 → 越准的税务建议",
        },
        "F4": {
            "name": "AI代码过编辑检测器",
            "slogan": "你的AI是不是改太多了？",
            "pain": "AI编程工具(Claude Code/Cursor)经常过度修改代码，改一些完全不需要改的地方，今天HN热帖正好讨论这个问题",
            "tech": "代码diff分析 + 变更必要性评分 + 可视化报告 + 阻断/警告机制",
            "pricing": "Free(GitHub Actions集成) / $19/月(私有仓库) / $49/月(团队)",
            "why_now": "HN热帖Over-editing by AI(280赞)刚引爆这个话题，目前无工具解决",
            "壁垒": "分析越多代码变更，越懂各种语言的正常改法，检测越准",
        },
        "H1": {
            "name": "AI内容一次多做工具",
            "slogan": "写一篇，全平台分发",
            "pain": "独立开发者/SaaS创始人做内容，每次要手动把一篇长文转成Twitter线程/LinkedIn帖子/公众号文章，重复劳动",
            "tech": "长文AI摘要 + 多平台格式适配（Twitter140字/LinkedIn帖/公众号格式） + 一键发布",
            "pricing": "Free(5篇/月) / $15/月(无限) / $49/月(团队+分析)",
            "why_now": "内容营销是独立开发者获客核心，但多平台分发是痛点，无专门工具",
            "壁垒": "发布越多平台数据，越懂各平台最佳格式和时机",
        },
        "H2": {
            "name": "公众号爆文分析助手",
            "slogan": "知道哪些文章会火，比追热点更重要",
            "pain": "公众号创作者不知道什么内容会爆，看了数据分析工具但只知道阅读量，不知道为什么爆",
            "tech": "爆文特征分析（标题/开头/结构/情绪） + 竞品爆文库 + 预测评分 + 写作建议",
            "pricing": "Free(3篇分析/月) / $29/月(无限+报告) / $99/月(竞品监控)",
            "why_now": "公众号是用户做内容的核心渠道，有公众号就是天然种子用户",
            "壁垒": "分析越多爆文，越懂中文内容爆火的底层规律",
        },
        "H3": {
            "name": "独立开发者着陆页生成器",
            "slogan": "30分钟搭一个看起来很专业的SaaS官网",
            "pain": "独立开发者做了MVP，官网却丑得不像收费产品；Notion/Framer太贵太复杂",
            "tech": "输入产品描述 → AI生成着陆页HTML/CSS → 主题切换 → 一键部署到Vercel/Netlify",
            "pricing": "Free(1页) / $19/月(自定义域名+分析) / $49/月(多页+电商)",
            "why_now": "独立开发者爆发，每个人都需要一个好看的着陆页收款",
            "壁垒": "模板越多越专业，用户越离不开",
        },
        "H4": {
            "name": "AI冷启动外联验证工具",
            "slogan": "找100个用户聊聊之前，先验证方向对不对",
            "pain": "独立开发者做MVP之前，不知道用户到底有没有需求，往往花几周做了没人用的东西",
            "tech": "目标用户画像 → AI生成外联话术 → 邮件/微信群发 → 意向收集 → 快速验证结论",
            "pricing": "Free(50次外联) / $19/月(200次) / $59/月(无限+分析报告)",
            "why_now": "GPT-5.5引爆AI编程，独立开发者增多，冷启动验证需求增加",
            "壁垒": "验证案例越多，方向判断越准，形成方法论",
        },
    }

    for i, (did, name, kws) in enumerate(today_directions, 1):
        detail = direction_details.get(did, {})
        emoji = ["🟦", "🟧", "🟪", "🟩"][i - 1]

        report += f"""### {emoji} 方向{i}: {name}

**一句话定位**：{detail.get('slogan', '—')}

**你观察到的痛点**：{detail.get('pain', '—')}

**为什么一人公司能做**：
- {detail.get('why_now', '—')}
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

**技术方案**：{detail.get('tech', '—')}

**定价**：{detail.get('pricing', '—')}

**护城河**：{detail.get('壁垒', '—')}

"""

    report += f"""---

## 💎 今日推荐方向（最适合OPC切入）

| 方向 | 推荐度 | 为什么选 | 你的优势 |
|------|--------|----------|----------|
| **H1: AI内容一次多做工具** | ★★★★★ | 内容营销核心痛点，有公众号渠道直接可用 | 你就是内容创作者，懂内容创作的坑 |
| **H2: 公众号爆文分析助手** | ★★★★★ | 你有公众号，可以自己当种子用户快速验证 | 有公众号资源，冷启动0成本 |
| **H3: 独立开发者着陆页生成器** | ★★★★☆ | 独立开发者刚需，定价清晰，技术简单 | AI PM懂产品定价，能做专业收款页 |
| **H4: AI冷启动验证工具** | ★★★★☆ | MVP上线前必做，但没人专门做这个工具 | AI PM懂用户调研，能做出方法论 |

---

## 📋 YC审查意见

**❌ 不要做（已排除）**：
- 通用AI工具（ChatGPT/Claude做了）
- AI Meeting/Coding/Extension（红海）
- 历史已覆盖方向（见上文列表，不再重复）

**✅ 要做（有今日数据支撑）**：
- 有GitHub/HN数据验证的垂直场景
- 大厂不屑于做的细分SaaS
- 用户愿意为"省时间+省麻烦"付高价

**最关键的3个问题**：
1. **谁会第一个付钱？** 愿意付多少？
2. **这个需求大厂愿不愿意做？** 愿不愿意做好？
3. **一人公司能做出比大厂更好的体验吗？**

---

## 🎯 行动建议（本周倒计时）

| 优先级 | 行动 | 截止 | 成功标准 |
|--------|------|------|----------|
| 🔴 | 从今日4个方向中，选定1个主攻方向 | 周四 | 选定方向，明确MVP |
| 🔴 | 找3个真实用户验证需求真伪 | 周五 | 至少1人愿意付费 |
| 🟡 | 确定MVP技术方案 | 周六 | 技术栈确定，开始编码 |
| 🟢 | 下周完成MVP上线 | 下周一 | 有可用产品发布 |

---

## 📁 数据缓存

| 数据源 | 缓存路径 | 说明 |
|--------|----------|------|
| GitHub | `cache/github_trending.json` | 1小时更新 |
| HN | `cache/hackernews.json` | 1小时更新 |
| PH | `cache/producthunt.json` | 2小时更新 |

---

*📌 本简报由OPC Insights系统生成 | v5.0（带智能去重）*
*🔄 每日早9点自动更新*
*⚠️ 新增：今日方向轮换 + 历史方向去重逻辑*
"""

    return report


# ============================================================
# 主流程
# ============================================================

async def main():
    print("=" * 50)
    print("🚀 一人公司MVP机会洞察 - YC视角")
    print("=" * 50)

    print("\n📦 抓取数据...")
    github, hn, ph = await fetch_all_data()
    print(f"  ✓ GitHub: {len(github)} 个AI项目")
    print(f"  ✓ HackerNews: {len(hn)} 个AI讨论")
    print(f"  ✓ ProductHunt: {len(ph)} 个AI产品")

    print("\n📝 生成YC视角简报...")
    report = generate_report(github, hn, ph)

    # 保存报告
    today_str = datetime.now().strftime("%Y-%m-%d")
    report_path = REPORT_DIR / f"mvp-insights-yc-{today_str}.md"
    with open(report_path, "w") as f:
        f.write(report)

    print(f"\n✅ 简报已生成!")
    print(f"   📁 {report_path}")
    print(f"   📊 GitHub: {len(github)} | HN: {len(hn)} | PH: {len(ph)}")
    return report


if __name__ == "__main__":
    asyncio.run(main())
