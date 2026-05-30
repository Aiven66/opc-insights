#!/usr/bin/env python3
"""
OPC一人公司MVP洞察日报生成器 v8.0（刘小排公式版）
==============================================
5大信息源:
  1. GitHub Trending   - 开源AI项目星星数排名
  2. Twitter/X         - AI产品热帖（中文翻译）
  3. 国内平台         - 小红书/抖音/B站需求信号
  4. ProductHunt       - 海外AI新品发布
  5. AI HOT            - 中文AI行业精选动态（aihot.virxact.com）

筛选标准: 刘小排成功案例公式（5个必须）
  1. 极简功能（只做一件事）
  2. AI能力加持（蹭热点AI能力）
  3. 面向海外（美元定价）
  4. 竞品已验证（有竞品在收钱）
  5. 低成本MVP（1人1周能搞定）
"""

import httpx, asyncio, json, re, time
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

REPORT_DIR = Path(__file__).parent.parent / "reports"
CACHE_DIR  = Path(__file__).parent.parent / "cache"
REPORT_DIR.mkdir(exist_ok=True)
CACHE_DIR.mkdir(exist_ok=True)

# ─────────────────────────────────────────────
# 刘小排成功公式7要素评分权重（v9.0）
# ─────────────────────────────────────────────
FORMULA_WEIGHTS = {
    "免费+免登录": 0.15,
    "极简输入":    0.15,
    "AI能力加持": 0.15,
    "单一功能极致": 0.15,
    "Freemium变现": 0.10,
    "全球用户":   0.10,
    "竞品已验证": 0.20,
}

def score_direction(direction):
    """对方向按刘小排公式打分，返回(总分, 分项得分)"""
    scores = direction.get("formula_scores", {})
    total = sum(scores.get(k, 0) * w for k, w in FORMULA_WEIGHTS.items())
    return total, scores

def rating_from_score(score):
    if score >= 4.0: return "★★★★★"
    if score >= 3.0: return "★★★★☆"
    if score >= 2.0: return "★★★☆☆"
    return "★★☆☆☆"


# ─────────────────────────────────────────────
# ① GitHub Trending
# ─────────────────────────────────────────────
async def fetch_github():
    print("  [1/4] 📦 GitHub Trending...")
    projects = []
    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get(
                "https://github.com/trending?since=daily",
                headers=HEADERS
            )
            soup = BeautifulSoup(resp.text, "html.parser")
            for item in soup.select("article.Box-row")[:20]:
                try:
                    title_el = item.select_one("h2 a")
                    if not title_el:
                        continue
                    href = title_el.get("href", "").strip("/")
                    stars_el = item.select_one("a.Link--muted")
                    stars_str = stars_el.get_text(strip=True).replace(",", "") if stars_el else "0"
                    stars_m = re.findall(r"([\d,]+)", stars_str)
                    stars = int(stars_m[0].replace(",", "")) if stars_m else 0
                    desc_el = item.select_one("p")
                    lang_el = item.select_one("span[itemprop='programmingLanguage']")
                    projects.append({
                        "name": href,
                        "url": f"https://github.com/{href}",
                        "stars": stars,
                        "desc": desc_el.get_text(strip=True) if desc_el else "",
                        "lang": lang_el.get_text(strip=True) if lang_el else "",
                    })
                except Exception:
                    continue
    except Exception as e:
        print(f"    ⚠️ {e}")
    projects.sort(key=lambda x: x["stars"], reverse=True)
    _cache("github", projects)
    print(f"    ✓ {len(projects)} 个项目")
    return projects


# ─────────────────────────────────────────────
# ② Twitter/X
# ─────────────────────────────────────────────
async def fetch_twitter():
    print("  [2/4] 🐦 Twitter/X...")
    tweets = []
    
    nitter_instances = [
        "https://nitter.net/search?q=AI+tool+product&f=tweets",
        "https://nitter.privacydev.net/search?q=AI+app+launch&f=tweets",
        "https://nitter.poast.org/search?q=AI+saas+launch&f=tweets",
    ]
    
    for instance in nitter_instances:
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.get(instance, headers=HEADERS, follow_redirects=True)
                if resp.status_code == 200 and len(resp.text) > 5000:
                    soup = BeautifulSoup(resp.text, "html.parser")
                    for item in soup.select(".timeline-item")[:10]:
                        text_el = item.select_one(".tweet-content")
                        if text_el:
                            text = text_el.get_text(strip=True)
                            if len(text) > 20:
                                tweets.append({"en": text, "zh": _translate_tweet(text)})
                    if tweets:
                        break
        except Exception:
            continue
    
    if not tweets:
        tweets = [{"en": "Twitter数据获取中...", "zh": "（暂无数据）"}]
    
    _cache("twitter", tweets)
    print(f"    ✓ {len(tweets)} 条热帖")
    return tweets


# ─────────────────────────────────────────────
# ③ 国内平台
# ─────────────────────────────────────────────
async def fetch_domestic():
    print("  [3/4] 📱 国内平台...")
    result = {}
    
    # B站AI工具热榜
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.get(
                "https://api.bilibili.com/x/web-interface/ranking/v2?rid=36&type=all",
                headers=HEADERS
            )
            data = r.json().get("data", {}).get("list", [])[:10]
            result["bilibili"] = [
                {"title": f"[{item.get('tname','')}] {item.get('title','')[:40]}", "label": item.get('tname','')}
                for item in data
                if "AI" in item.get("title","") or "人工智能" in item.get("title","") or "工具" in item.get("title","")
            ]
    except Exception:
        result["bilibili"] = [{"title": "B站数据获取失败（备用数据）", "label": "AI工具"}]
    
    result["xiaohongshu"] = []
    _cache("domestic", result)
    print(f"    ✓ 小红书:{len(result['xiaohongshu'])}条 | B站:{len(result['bilibili'])}条")
    return result


# ─────────────────────────────────────────────
# ④ ProductHunt
# ─────────────────────────────────────────────
async def fetch_producthunt():
    print("  [4/4] 🆕 ProductHunt...")
    items = []
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            r = await client.get(
                "https://www.producthunt.com/frontend/graphql",
                headers={**HEADERS, "Content-Type": "application/json"},
                json={
                    "operationName": "ProductShowcases",
                    "variables": json.dumps({"cursor": None, "first": 20}),
                    "query": """query ProductShowcases { productShowcases(first: 20) { edges { node { name tagline url votesCount { count } topics { name } } } } }"""
                }
            )
            data = r.json()
            edges = (data.get("data", {}) or {}).get("productShowcases", {}) or {}
            if isinstance(edges, dict):
                edges = edges.get("edges", [])
            for e in edges:
                n = e.get("node", {})
                items.append({
                    "name": n.get("name", ""),
                    "url": n.get("url", ""),
                    "votes": n.get("votesCount", {}).get("count", 0),
                    "topics": [t.get("name","") for t in n.get("topics", [])],
                })
    except Exception:
        pass
    
    if not items:
        items = [{"name": "ProductHunt数据获取中", "url": "#", "votes": 0, "topics": []}]
    
    items.sort(key=lambda x: x.get("votes", 0), reverse=True)
    _cache("producthunt", items)
    print(f"    ✓ {len(items)} 个产品")
    return items


# ─────────────────────────────────────────────
# ⑤ AI HOT
# ─────────────────────────────────────────────
async def fetch_aihot():
    print("  [5/5] 🔥 AI HOT（中文AI行业动态）...")
    items = []
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            r = await client.get(
                "https://aihot.virxact.com/api/public/items?mode=selected&take=50",
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=15.0
            )
            d = r.json()
            items = d.get("items", [])
    except Exception as e:
        print(f"    ⚠️ AI HOT获取失败: {e}")
    
    _cache("aihot", items)
    print(f"    ✓ {len(items)} 条AI HOT动态")
    return items


# ─────────────────────────────────────────────
# 工具函数
# ─────────────────────────────────────────────
def _cache(key, data):
    path = CACHE_DIR / f"{key}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def _bar(score, max_score=5):
    full = min(int(score), 5)
    return "█" * full + "░" * (5 - full)

_TRANSLATIONS = {
    "I built": "我做了", "launched": "发布了", "made": "做了",
    "AI": "AI", "tool": "工具", "product": "产品",
    "month": "月", "year": "年", "users": "用户",
    "new": "新", "free": "免费", "open": "开源",
    "million": "百万", "thousand": "千", "k": "k",
    "dollars": "美元", "$": "$", "MRR": "月收入",
}

def _translate_tweet(text):
    result = text
    for en, zh in _TRANSLATIONS.items():
        result = result.replace(en, zh)
    if len(result) > 120:
        result = result[:120] + "..."
    return result


# ─────────────────────────────────────────────
# AI HOT 精选构建
# ─────────────────────────────────────────────
def _build_aihot_section(aihot):
    # 优先看有产品发布的条目
    important = []
    tools = []
    for item in aihot:
        cat = item.get("category", "")
        title = item.get("title", "")
        if cat in ("ai-products","industry") or any(x in title for x in ["发布","上线","新功能","产品"]):
            important.append(item)
        elif cat == "ai-tools":
            tools.append(item)
    
    lines = ["## 5️⃣ 信息源⑤: AI HOT 中文精选动态\n\n"]
    if important:
        lines.append("### 🔥 重要产品发布\n\n")
        for item in important[:10]:
            cat = item.get("category","")
            title = item.get("title","")[:75]
            source = item.get("source","")[:20]
            pub = item.get("publishedAt","")[:10]
            lines.append(f"- **{title}** [{pub} {source}]\n")
    
    if tools:
        lines.append("\n### 🛠️ AI工具动态\n\n")
        for item in tools[:8]:
            title = item.get("title","")[:75]
            source = item.get("source","")[:20]
            lines.append(f"- {title} [{source}]\n")
    
    lines.append("\n**💡 AI HOT洞察**:\n")
    lines.append("- AI工具发布节奏加快，注意最新功能带来的教程需求\n")
    lines.append("- 独立开发者工具持续热门（Claude Code/Cursor等）\n")
    lines.append("- 音频/视频类工具热度上升\n\n")
    
    return "".join(lines)


# ─────────────────────────────────────────────
# 报告生成 v9.0（刘小排7要素公式版）
# ─────────────────────────────────────────────
def generate_report(github, twitter, domestic, ph, aihot):
    today = datetime.now()

    # 关键词热度
    keywords = {}
    for p in github[:10]:
        text = f"{p['name']} {p['desc']}".lower()
        for kw in ["agent","assistant","ai","tool","code","video","voice","image","3d","clone"]:
            if kw in text:
                keywords[kw] = keywords.get(kw, 0) + 2
    for item in aihot:
        title = item.get("title","").lower()
        for kw in ["launch","release","agent","video","voice","image","3d","ai tool","product"]:
            if kw in title:
                keywords[kw] = keywords.get(kw, 0) + 1.5
    top_kw = sorted(keywords.items(), key=lambda x: -x[1])[:12]

    r = ""

    # 封面
    r += f"""# 🦀 OPC一人公司MVP洞察日报

**时间**: {today.strftime("%Y年%m月%d日 %A")}
**版本**: v9.0 刘小排7要素公式版 | 5大信息源
**筛选标准**: 竞品已验证 + 可商业化 + 1人1周MVP
**参照案例**: Raphael AI(3M月活) / AnyVoice(3秒克隆) / Fast3D(免费免登录) / Morisot(一墙好图)

---

## 📊 5大信息源完整数据

| # | 信息源 | 数据量 | 质量评估 |
|---|--------|--------|---------|
| 1 | 📦 **GitHub Trending** | {len(github)} 个AI项目 | **{sum(1 for p in github if p.get("stars",0)>10000)}个高星项目** |
| 2 | 🐦 **Twitter/X** | {len(twitter)} 条热帖 | {"数据正常" if len(twitter)>1 else "数据偏少"} |
| 3 | 📱 **国内平台** | B站{len(domestic.get('bilibili',[]))}条 | {"数据正常" if domestic.get('bilibili') else "暂无数据"} |
| 4 | 🆕 **ProductHunt** | {len(ph)} 个产品 | {"数据正常" if len(ph)>1 else "数据偏少"} |
| 5 | 🔥 **AI HOT** | {len(aihot)} 条精选 | **{sum(1 for i in aihot if i.get("category") in ("ai-products","industry"))}个产品发布** |

---

## 🎯 刘小排4个成功案例参照

| 产品 | 网址 | 核心功能 | 核心指标 | 成功要素 |
|------|------|---------|---------|---------|
| **Raphael AI** | raphael.app | 免费文生图+AI修改 | 3M月活/4.9分/1530张/分钟 | 免费无限+免登录+Seedream 5.0 |
| **AnyVoice** | anyvoice.net | 3秒声音克隆 | 被影视自媒体大量使用 | 3秒速度+名人声音库 |
| **Fast3D** | fast3d.io | 图/文→3D模型 | 15万月活 | 免费免登录+多格式+秒级 |
| **Morisot** | morisot.ai | 一句含糊→一墙好图 | 批量生成+极简 | 含糊输入+批量出图+创意感 |

---

## 🎯 刘小排成功公式7要素

| # | 要素 | 权重 | 说明 |
|---|------|------|------|
| 1 | **免费+免登录** | 15% | 无限生成获取流量（参考：Raphael 3M用户） |
| 2 | **极简输入** | 15% | 3秒上手，0学习成本（参考：AnyVoice 3秒克隆） |
| 3 | **AI能力加持** | 15% | 蹭热点技术（文生图/声音克隆/3D/视频） |
| 4 | **单一功能极致** | 15% | 只做一件事，做到行业第一（参考：Fast3D只做3D） |
| 5 | **Freemium变现** | 10% | 免费引流，付费增值（$9-29/月，参考竞品定价） |
| 6 | **全球用户** | 10% | 英文界面，美元定价（不做中文版） |
| 7 | **竞品已验证** | 20% | 有竞品在收钱（最重要！先验证再入场） |

---

"""

    # 1. GitHub
    r += f"""## 📦 信息源①: GitHub Trending AI项目（全部）

| ⭐ | 今日↑ | 项目 | 语言 | 描述 |
|----|-------|------|------|------|
"""
    for p in github:
        s = p.get("stars", 0)
        t = p.get("todayStars", 0)
        n = p.get("name", "")
        d = p.get("desc", "")[:55]
        l = p.get("lang", "") or "-"
        flag = "⭐⭐" if s > 10000 else ("⭐" if s > 5000 else "")
        r += f"| {s:>7,} | +{t:>4} | {flag}[{n}]({p.get('url','')}) | {l} | {d} |\n"

    r += """
**💡 GitHub洞察**:
"""
    for p in github[:5]:
        s = p.get("stars",0)
        if s > 10000:
            n = p.get("name","")
            d = p.get("desc","")[:65]
            r += f"- **{n}** ({s:,}★) → {d}\n"

    # 2. Twitter
    r += f"""
## 🐦 信息源②: Twitter/X AI产品热帖

| # | 🐦 英文原文 | 🇨🇳 中文翻译 |
|---|------------|-------------|
"""
    for i, t in enumerate(twitter[:6], 1):
        en = t.get("en","")[:80]
        zh = t.get("zh","")
        r += f"| {i} | {en}... | {zh} |\n"

    # 3. 国内平台
    bili = domestic.get("bilibili", [])
    r += f"""
## 📱 信息源③: 国内平台（B站）

| # | 内容 | 标签 |
|---|------|------|
"""
    for i, note in enumerate(bili, 1):
        r += f"| {i} | **{note.get('title','')}** | {note.get('label','')} |\n"
    if not bili:
        r += "| 1 | （暂无数据） | - |\n"

    # 4. ProductHunt
    r += f"""
## 🆕 信息源④: ProductHunt AI新品

| # | 产品名 | 得票 | 方向 |
|---|--------|------|------|
"""
    for i, p in enumerate(ph, 1):
        name = p.get("name","")[:45]
        votes = p.get("votes",0)
        topics = "/".join(p.get("topics",[])[:2])
        r += f"| {i} | {name} | {votes}票 | {topics} |\n"
    if len(ph) <= 1:
        r += "| 1 | （数据获取失败） | 0票 | - |\n"

    # 5. AI HOT
    cats_count = {}
    for i in aihot:
        c = i.get("category","unknown")
        cats_count[c] = cats_count.get(c, 0) + 1

    r += f"""
## 🔥 信息源⑤: AI HOT 中文精选动态（全部50条）

**分类统计**: {dict(cats_count)}

### 🔥 重要产品发布（ai-products / industry）

| # | 日期 | 来源 | 标题 |
|---|------|------|------|
"""
    prod_items = [i for i in aihot if i.get("category") in ("ai-products","industry")]
    for i, item in enumerate(prod_items, 1):
        pub = item.get("publishedAt","")[:10]
        src = item.get("source","")[:20]
        t = item.get("title","")[:65]
        r += f"| {i} | {pub} | {src} | {t} |\n"

    r += """
### 💡 AI工具动态（tip）

| # | 标题 | 来源 |
|---|------|------|
"""
    tip_items = [i for i in aihot if i.get("category") == "tip"][:8]
    for i, item in enumerate(tip_items, 1):
        src = item.get("source","")[:22]
        t = item.get("title","")[:70]
        r += f"| {i} | {t} | {src} |\n"

    # MVP方向
    r += _build_opportunities(github, aihot)

    # 关键词热度
    r += f"""
---

## 🗺️ 关键词热度综合排名

| 热度条 | 关键词 | 得分 |
|--------|--------|------|
"""
    for kw, score in top_kw:
        r += f"| {_bar(score)} | **{kw}** | {score:.1f} |\n"

    r += f"""
---

*📌 OPC Insights v9.0 刘小排7要素公式版*
*🔄 5大信息源: GitHub({len(github)}) + Twitter({len(twitter)}) + B站({len(bili)}) + PH({len(ph)}) + AI HOT({len(aihot)})*
*📅 {today.strftime("%Y-%m-%d %H:%M:%S")}*
"""
    return r


# ─────────────────────────────────────────────
# 星标库读取（用于去重）
# ─────────────────────────────────────────────
def _load_starred_products():
    """从starred/README.md读取已星标的产品名"""
    starred = []
    readme_path = Path(__file__).parent.parent / "starred" / "README.md"
    if not readme_path.exists():
        return starred
    with open(readme_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if "|" not in line:
                continue
            parts = [p.strip() for p in line.split("|")]
            for p in parts:
                # 匹配中文产品名关键词
                keywords = [
                    "缩略图","播客摘要","声音克隆","背景音","放大","去水印",
                    "克隆","文案","广告视频","批量生成","舆情","报价",
                    "税务","KOL","私域","竞品监控","定价","IPFlow",
                    "SoloOS","AICompare","DevGrowth","融资"
                ]
                for kw in keywords:
                    if kw in p and len(p) > 4 and p not in starred:
                        starred.append(p)
                        break
    return starred


# ─────────────────────────────────────────────
# MVP方向输出（刘小排7要素公式）v9.1 去重版
# ─────────────────────────────────────────────
def _build_opportunities(github, aihot):
    """从今日数据中提取候选方向 + 固定推荐方向（含星标库去重）"""

    # 读取星标库
    starred = _load_starred_products()
    print(f"    📌 已星标产品: {len(starred)}个，将自动去重")

    # 从GitHub中提取可商业化项目（排除开发者框架）
    github_candidates = []
    excluded_patterns = [
        "cpp","llm","model","framework","cli","sdk","lib",
        "server","kernel","runtime","compiler","wasm","api-gateway",
        "protocol","engine","database","cache"
    ]
    for p in github:
        name = p.get("name","").lower()
        desc = p.get("desc","").lower()
        stars = p.get("stars",0)
        if any(x in name for x in excluded_patterns):
            continue
        if stars > 3000 and any(x in desc for x in ["tool","app","generator","maker","creator","assistant","studio","tts","voice","clone","video","image","3d"]):
            github_candidates.append({
                "name": p["name"],
                "stars": stars,
                "desc": p["desc"],
                "url": p["url"],
            })

    # 从AI HOT提取产品发布信号
    hot_signals = []
    for item in aihot:
        cat = item.get("category","")
        if cat in ("ai-products","industry"):
            hot_signals.append({
                "title": item.get("title",""),
                "source": item.get("source",""),
                "pub": item.get("publishedAt","")[:10],
            })

    # 固定推荐方向（星标库 + 今日新增）
    recommended = [
        {
            "id": "H3", "emoji": "🟨", "platform": "🌍 海外版",
            "title": "AI社媒文案生成器（PostAI）",
            "starred_keywords": ["文案", "PostAI", "社媒"],
            "slogan": "Your ideas, viral posts — generated in seconds",
            "formula_scores": {
                "免费+免登录": 5, "极简输入": 5, "AI能力加持": 5,
                "单一功能极致": 5, "Freemium变现": 4, "全球用户": 5, "竞品已验证": 4,
            },
            "pain": "每天发Twitter/LinkedIn，不知道写什么；写一条要1-2小时",
            "mvp": "输入你今天做了什么/产品/话题 → AI生成5条Twitter+3条LinkedIn文案",
            "pricing": "Free(10次/天) / $9/月(无限) / $29/月(批量+数据分析)",
            "competitors": "Buffer($6/月,无AI), Jasper($49/月,太贵), Copy.ai($49/月)",
            "competitor_verdict": "✅ 有竞品在收钱；Jasper太贵，Buffer无AI = 中间空白",
            "data_source": "GitHub无直接信号；推特高频需求场景",
            "why": "最简单MVP（GPT-4o纯文字）；$9/月用户无压力；Twitter创作者全球数亿",
            "action": "今天：GPT-4o文案效果验证 → 本周：Next.js 3页MVP → 快速上线",
        },
        {
            "id": "H1", "emoji": "🟪", "platform": "🌍 海外版",
            "title": "AI视频缩略图生成器（ThumbAI）",
            "starred_keywords": ["缩略图", "ThumbAI"],
            "slogan": "Turn any video into a clickable thumbnail in seconds",
            "formula_scores": {
                "免费+免登录": 4, "极简输入": 5, "AI能力加持": 5,
                "单一功能极致": 5, "Freemium变现": 4, "全球用户": 5, "竞品已验证": 4,
            },
            "pain": "YouTube/TikTok创作者想做吸引人的缩略图，但不会设计",
            "mvp": "输入YouTube URL → AI分析视频 → 生成3种风格缩略图 → 下载",
            "pricing": "Free(3次/天) / $9/月(无限) / $29/月(批量)",
            "competitors": "Thumbnail Blaster($49/年,无AI), Canva($12.99/月,模板)",
            "competitor_verdict": "✅ 有竞品在收钱，但无AI生成能力；缩略图+AI = 差异化",
            "data_source": "星标库已有",
            "why": "YouTube创作者全球5亿+；GPT-Image-2已可生成；1人1周能搞定",
            "action": "本周：GPT-Image-2 API确认 → 下周：Next.js MVP → ProductHunt",
        },
        {
            "id": "H2", "emoji": "🟫", "platform": "🌍 海外版",
            "title": "AI播客摘要（PodAI）",
            "starred_keywords": ["播客摘要", "PodAI"],
            "slogan": "Turn hours of audio into minutes of insights",
            "formula_scores": {
                "免费+免登录": 4, "极简输入": 5, "AI能力加持": 5,
                "单一功能极致": 5, "Freemium变现": 4, "全球用户": 5, "竞品已验证": 4,
            },
            "pain": "想听播客但没时间（2小时太长）；内容创作者需要参考资料",
            "mvp": "输入播客/YouTube URL → Whisper转录 → AI摘要 → 3分钟看完",
            "pricing": "Free(5次/月) / $12/月(无限) / $39/月(团队)",
            "competitors": "Otter.ai($20/月), Descript($24/月), Snipd($9.99/月)",
            "competitor_verdict": "✅ 多个竞品在收钱；Otter偏会议、Descript偏编辑，无专注播客摘要",
            "data_source": "星标库已有",
            "why": "Whisper已解决转录；GPT-4o摘要成熟；全球播客听众超5亿",
            "action": "本周：Whisper API确认 → 下周：MVP → ProductHunt",
        },
        {
            "id": "N1", "emoji": "🟦", "platform": "🌍 海外版",
            "title": "设备端AI声音克隆（VoiceClone）",
            "starred_keywords": ["声音克隆", "VoiceClone"],
            "slogan": "Clone any voice in 3 seconds — on your device",
            "formula_scores": {
                "免费+免登录": 5, "极简输入": 5, "AI能力加持": 5,
                "单一功能极致": 4, "Freemium变现": 4, "全球用户": 5, "竞品已验证": 4,
            },
            "pain": "用户想克隆声音做内容，但不想上传音频（隐私顾虑）",
            "mvp": "上传30秒音频 → 3秒克隆 → 输入文字生成语音（设备端运行，不上传）",
            "pricing": "Free(3个克隆) / $12/月(无限) / $29/月(团队)",
            "competitors": "AnyVoice($9-29), ElevenLabs($5-22), Resemble.ai($49)",
            "competitor_verdict": "✅ 多个竞品在收钱，声音克隆需求已被验证",
            "data_source": "GitHub: SuperTonic 6,977★设备端TTS",
            "why": "AnyVoice 3秒克隆已验证速度需求；设备端 = 隐私差异化",
            "action": "本周：Swift+SuperTonic调研 → 下周：iOS App → TestFlight",
        },
        {
            "id": "N4", "emoji": "🟧", "platform": "🌍 海外版",
            "title": "AI音频去背景音（CleanVoice）",
            "starred_keywords": ["背景音", "CleanVoice", "去噪"],
            "slogan": "Remove background noise from audio in seconds",
            "formula_scores": {
                "免费+免登录": 5, "极简输入": 5, "AI能力加持": 5,
                "单一功能极致": 5, "Freemium变现": 4, "全球用户": 5, "竞品已验证": 4,
            },
            "pain": "播客主在咖啡厅录音有噪音；视频创作者需要干净音轨",
            "mvp": "上传音频 → AI去除背景噪音/回声/呼吸声 → 下载干净音频",
            "pricing": "Free(3次/天) / $9/月(无限) / $29/月(批量)",
            "competitors": "Adobe Podcast(免费但需注册), Veed.io($9/月), Cleanvoice AI($11/月)",
            "competitor_verdict": "✅ 多个竞品在收钱；免登录+极简 = 差异化",
            "data_source": "星标库已有（已完成11问调研）",
            "why": "Cleanvoice AI月入百万验证市场；免登录是核心差异化；7天MVP",
            "action": "本周：Replicate音频去噪API测试 → 下周：MVP开发 → ProductHunt",
        },
        {
            "id": "N5", "emoji": "🟩", "platform": "🌍 海外版",
            "title": "AI图片放大无损（UpscaleAI）",
            "starred_keywords": ["放大", "UpscaleAI", "无损"],
            "slogan": "Upscale any image 4x or 8x — in seconds",
            "formula_scores": {
                "免费+免登录": 5, "极简输入": 5, "AI能力加持": 5,
                "单一功能极致": 5, "Freemium变现": 4, "全球用户": 5, "竞品已验证": 4,
            },
            "pain": "微信截图太小放大就糊；旧照片想修复高清",
            "mvp": "上传小图 → AI放大4x/8x → 下载高清不失真",
            "pricing": "Free(3次/天) / $9/月(无限) / $29/月(商用)",
            "competitors": "Upscayl(需下载), Let's Enhance($12/月), Pixelcut(有限制)",
            "competitor_verdict": "✅ 多个竞品在收钱；免登录+极简 = 差异化",
            "data_source": "星标库已有",
            "why": "需求极广（每个人都有小图要放大）；Real-ESRGAN API成熟；3-5天MVP",
            "action": "本周：Replicate Real-ESRGAN测试 → 下周：MVP → ProductHunt",
        },
        {
            "id": "N3", "emoji": "🟪", "platform": "🌍 海外版",
            "title": "AI图片批量生成器（BatchAI）",
            "starred_keywords": ["批量生成", "BatchAI", "批量"],
            "slogan": "One idea, a wall of images — pick the best",
            "formula_scores": {
                "免费+免登录": 5, "极简输入": 5, "AI能力加持": 5,
                "单一功能极致": 4, "Freemium变现": 4, "全球用户": 5, "竞品已验证": 3,
            },
            "pain": "博主/设计师做内容配图，1张1张生成太慢，没有批量感",
            "mvp": "输入一句话主题 → AI批量生成10-20张 → ZIP打包下载",
            "pricing": "Free(10张/天) / $9/月(无限) / $29/月(高清+商用)",
            "competitors": "Leonardo.ai(免费需登录), Midjourney($10/月需Discord)",
            "competitor_verdict": "⚠️ Leonardo有批量但要登录；无登录+批量 = 差异化空白",
            "data_source": "AI HOT: Krea 2.0专业版发布；Morisot已验证批量方向",
            "why": "Morisot验证了批量+含糊输入需求；Raphael公式迁移到图片场景",
            "action": "本周：Replicate批量API调研 → 下周：Next.js MVP → ProductHunt",
        },
        {
            "id": "N2", "emoji": "🟫", "platform": "🌍 海外版",
            "title": "电商AI广告视频生成器（AdGen）",
            "starred_keywords": ["广告视频", "AdGen", "电商"],
            "slogan": "Turn any product into a viral ad video in 60 seconds",
            "formula_scores": {
                "免费+免登录": 4, "极简输入": 4, "AI能力加持": 5,
                "单一功能极致": 4, "Freemium变现": 4, "全球用户": 5, "竞品已验证": 3,
            },
            "pain": "独立电商卖家想做广告视频，但不会剪辑、雇人太贵",
            "mvp": "粘贴亚马逊/Shopify产品链接 → AI提取卖点 → 生成15/30/60秒广告视频",
            "pricing": "Free(3个/月) / $19/月(无限) / $49/月(批量)",
            "competitors": "Runway($15/月), HeyGen($15/月), Synthesia($29/月)",
            "competitor_verdict": "✅ 有竞品在收钱，但价格贵、门槛高；独立卖家缺平价工具",
            "data_source": "AI HOT: Runway Agent一键生成广告(05-15)；可灵Kling戛纳大会",
            "why": "Runway Agent已验证广告需求；$19/月卖家无压力；可灵/Runway API可用",
            "action": "本周：Replicate API（Runway/可灵）成本调研 → 下周：MVP → ProductHunt",
        },
        {
            "id": "N6", "emoji": "🟩", "platform": "🌍 海外版",
            "title": "AI图片去水印（WatermarkRemover）",
            "starred_keywords": ["去水印", "WatermarkRemover", "水印"],
            "slogan": "Remove watermarks from images in seconds",
            "formula_scores": {
                "免费+免登录": 5, "极简输入": 5, "AI能力加持": 5,
                "单一功能极致": 5, "Freemium变现": 4, "全球用户": 5, "竞品已验证": 3,
            },
            "pain": "下载的图片有水印想用于PPT/文档",
            "mvp": "上传图片 → 涂抹水印区域 → AI智能填充 → 下载",
            "pricing": "Free(3次/天) / $9/月(无限) / $29/月(批量)",
            "competitors": "Inpaint($10/月), Cleanup.pictures(有限制)",
            "competitor_verdict": "⚠️ 有竞品但体验不够极简",
            "data_source": "星标库已有",
            "why": "需求真实；LAMA inpainting API成熟；注意版权合规",
            "action": "本周：Replicate inpainting测试 → 合规条款准备",
        },
        {
            "id": "N7", "emoji": "🟦", "platform": "🌍 海外版",
            "title": "AI视频去水印（VideoWatermarkRemover）",
            "starred_keywords": ["视频去水印", "VideoWatermarkRemover"],
            "slogan": "Remove watermarks from videos in seconds",
            "formula_scores": {
                "免费+免登录": 4, "极简输入": 4, "AI能力加持": 5,
                "单一功能极致": 5, "Freemium变现": 4, "全球用户": 5, "竞品已验证": 3,
            },
            "pain": "视频创作者需要干净素材用于二次创作",
            "mvp": "上传视频 → 涂抹水印区域 → AI逐帧处理 → 下载",
            "pricing": "Free(3次/天) / $15/月(无限) / $49/月(批量)",
            "competitors": "Kapwing($16/月), InVideo($15/月)",
            "competitor_verdict": "⚠️ 有竞品但体验不够极简；技术复杂度高",
            "data_source": "星标库已有",
            "why": "需求真实但技术复杂；建议放在最后做",
            "action": "待定（技术复杂度高，10-14天MVP）",
        },
        {
            "id": "NEW1", "emoji": "🆕", "platform": "🌍 海外版",
            "title": "Grok Imagine图像生成器（蹭Elon热点）",
            "starred_keywords": ["Grok", "Imagine", "图像生成"],
            "slogan": "Generate stunning images with Grok — free",
            "formula_scores": {
                "免费+免登录": 5, "极简输入": 5, "AI能力加持": 5,
                "单一功能极致": 4, "Freemium变现": 4, "全球用户": 5, "竞品已验证": 4,
            },
            "pain": "Midjourney需订阅且要Discord；DALL-E有额度限制",
            "mvp": "输入prompt → Grok Imagine生成 → 下载图片",
            "pricing": "Free(无限) / $16/月(X Premium+)",
            "competitors": "Midjourney($10/月), DALL-E(额度制), Stable Diffusion(免费)",
            "competitor_verdict": "✅ Grok已正式发布，Elon Musk背书",
            "data_source": "AI HOT 05-17: Grok Imagine图像生成正式发布",
            "why": "Grok品牌背书；可能有免登录免费版；蹭Elon流量",
            "action": "确认Grok Imagine API可用性 → 评估是否可做套壳",
        },
        {
            "id": "NEW2", "emoji": "🆕", "platform": "🌍 海外版",
            "title": "Notion模板/插件市场（蹭Notion CLI热点）",
            "starred_keywords": ["Notion", "模板", "插件"],
            "slogan": "Discover the best Notion templates — curated daily",
            "formula_scores": {
                "免费+免登录": 4, "极简输入": 4, "AI能力加持": 3,
                "单一功能极致": 3, "Freemium变现": 4, "全球用户": 5, "竞品已验证": 4,
            },
            "pain": "Notion用户不知道去哪找好模板",
            "mvp": "Notion模板发现+分类+评分+直接复制",
            "pricing": "Free(浏览) / $9/月(高级模板)",
            "competitors": "Notion Templates, Thomas Frank, Notion VIP",
            "competitor_verdict": "✅ 有竞品在收钱，但无AI推荐功能",
            "data_source": "AI HOT 05-16: Notion推出开发者平台及CLI工具",
            "why": "Notion用户超3000万；开发者平台 = 更多模板需求",
            "action": "评估Notion API限制 → Notion官方模板市场竞争",
        },
    ]

    # 计算总分并排序
    for rec in recommended:
        total, scores = score_direction(rec)
        rec["total_score"] = total
        rec["scores"] = scores
    recommended.sort(key=lambda x: -x["total_score"])

    lines = []

    # GitHub可商业化候选
    if github_candidates:
        lines.append("## 📦 GitHub可商业化项目（工具类+高星）\n\n")
        lines.append("| 项目 | ⭐ | 描述 |\n|------|----|------|\n")
        for p in github_candidates[:8]:
            lines.append(f"| [{p['name']}]({p['url']}) | {p['stars']:,}★ | {p['desc'][:60]} |\n")
        lines.append("\n")

    # AI HOT产品发布信号
    if hot_signals:
        lines.append("## 🔥 AI HOT产品发布信号\n\n")
        lines.append("| 标题 | 日期 | 来源 |\n|------|------|------|\n")
        for p in hot_signals[:10]:
            lines.append(f"| {p['title'][:70]} | {p['pub']} | {p['source'][:20]} |\n")
        lines.append("\n")

    # ── 筛选结果总览（标记星标状态）─────────────────────
    lines.append("---\n\n## 🎯 今日方向筛选结果（刘小排7要素公式）\n\n")
    lines.append(f"**📌 星标库已去重**：已过滤 {len(starred)} 个已星标产品\n\n")

    lines.append("### ✅ 通过筛选 + 星标库去重后（真正的新方向）\n\n")
    lines.append("| # | 方向 | 评分 | 状态 | 竞品验证 |\n")
    lines.append("|---|------|------|------|----------|\n")

    # 新方向（不在星标库中）
    for rec in recommended:
        is_new = True
        for s in starred:
            if any(kw in s for kw in rec.get("starred_keywords", [])):
                is_new = False
                break
        if is_new and rec["total_score"] >= 3.5:
            verdict = rec["competitor_verdict"]
            lines.append(f"| {rec['id']} | **{rec['title']}** {rating_from_score(rec['total_score'])} | {rec['total_score']:.2f}/5 | 🆕 新增 | {verdict[:35]} |\n")

    lines.append("\n### 📦 星标库已有方向（继续推进）\n\n")
    lines.append("| # | 方向 | 评分 | 状态 |\n")
    lines.append("|---|------|------|------|\n")

    # 已星标（已在starred库中）
    for rec in recommended:
        for s in starred:
            if any(kw in s for kw in rec.get("starred_keywords", [])):
                lines.append(f"| {rec['id']} | **{rec['title']}** {rating_from_score(rec['total_score'])} | {rec['total_score']:.2f}/5 | ✅ 已星标 |\n")
                break

    lines.append("\n### ❌ 未通过筛选的方向\n\n")
    lines.append("| 方向 | 评分 | 原因 |\n|------|------|------|\n")
    # 排除GitHub开发者框架
    for p in github:
        name = p.get("name","")
        excluded = any(x in name.lower() for x in ["cpp","llm","model","framework","cli","sdk","lib","server","kernel","runtime","compiler"])
        if excluded:
            stars = p.get("stars",0)
            lines.append(f"| {name} | 1.5/5 | 开发者框架，不是用户产品 |\n")
    # 排除AI HOT大厂产品
    for sig in hot_signals:
        t = sig.get("title","")
        if any(x in t for x in ["OpenAI","Google","Microsoft","Meta","Anthropic"]):
            lines.append(f"| {t[:40]} | 2.0/5 | 大厂产品，独立开发者无机会 |\n")

    lines.append("\n---\n\n## 🔥 今日最佳机会（详细分析）\n\n")

    # 详细分析（评分最高的3个）
    for rec in recommended[:3]:
        s = rec["scores"]
        fs = rec["formula_scores"]
        lines.append(f"""### {rec['emoji']} {rec['id']} {rec['title']}

**一句话定位**: {rec['slogan']}

**刘小排7要素评分**:

| 要素 | 评分 | 说明 |
|------|------|------|
| 免费+免登录 | {s.get('免费+免登录',0)}/5 | {"✅ 符合" if s.get('免费+免登录',0)>=4 else "⚠️ 部分符合"} |
| 极简输入 | {s.get('极简输入',0)}/5 | {"✅ 符合" if s.get('极简输入',0)>=4 else "⚠️ 部分符合"} |
| AI能力加持 | {s.get('AI能力加持',0)}/5 | {"✅ 符合" if s.get('AI能力加持',0)>=4 else "⚠️ 部分符合"} |
| 单一功能极致 | {s.get('单一功能极致',0)}/5 | {"✅ 符合" if s.get('单一功能极致',0)>=4 else "⚠️ 部分符合"} |
| Freemium变现 | {s.get('Freemium变现',0)}/5 | {"✅ 符合" if s.get('Freemium变现',0)>=4 else "⚠️ 部分符合"} |
| 全球用户 | {s.get('全球用户',0)}/5 | {"✅ 符合" if s.get('全球用户',0)>=4 else "⚠️ 部分符合"} |
| 竞品已验证 | {s.get('竞品已验证',0)}/5 | {"✅ 有竞品在收钱" if s.get('竞品已验证',0)>=4 else "⚠️ 无竞品或竞品不收钱"} |

**加权总分**: {rec['total_score']:.2f}/5.0 {rating_from_score(rec['total_score'])}

**真实痛点**: {rec['pain']}

**竞品分析**:
- 竞品：{rec['competitors']}
- 判断：{rec['competitor_verdict']}

**MVP设计**:
{rec['mvp']}

**定价策略**:
{rec['pricing']}

**数据来源**: {rec['data_source']}

**为什么能做**:
{rec['why']}

**本周行动**:
{rec['action']}

---

""")

    # 本周行动建议
    top3 = "\n".join([f"🥇 {r['title']}（{r['total_score']:.2f}/5）→ {r['action'].split('→')[0].strip()}" for r in recommended[:3]])
    lines.append(f"""## 💡 本周行动建议

```
优先级排序（按刘小排7要素评分）：

{top3}

继续推进（星标库已有）：
→ ThumbAI / PodAI / PostAI

不推荐：
→ GitHub开发者框架（无用户产品）
→ 大厂产品衍生（无机会）
→ 灰色地带产品（道德/法律风险）
```
""")

    return "".join(lines)


# ─────────────────────────────────────────────
# 主流程
# ─────────────────────────────────────────────
async def main():
    print("=" * 60)
    print("🚀 OPC MVP洞察日报 v9.1 — 刘小排7要素公式版")
    print("  筛选标准: 竞品已验证 + 可商业化 + 1人1周MVP")
    print("  参照案例: Raphael AI(3M月活) / AnyVoice(3秒克隆) / Fast3D / Morisot")
    print("  v9.1 新增：星标库自动去重")
    print("=" * 60)

    github, twitter, domestic, ph, aihot = await asyncio.gather(
        fetch_github(),
        fetch_twitter(),
        fetch_domestic(),
        fetch_producthunt(),
        fetch_aihot(),
    )

    print("\n📝 生成洞察报告...")
    report = generate_report(github, twitter, domestic, ph, aihot)

    today_str = datetime.now().strftime("%Y-%m-%d")
    report_path = REPORT_DIR / f"mvp-insights-yc-{today_str}.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n✅ 报告已生成: {report_path}")
    print(f"   📦 GitHub:{len(github)} | 🐦 Twitter:{len(twitter)} | 📱 国内:{sum(len(v) for v in domestic.values())} | 🆕 PH:{len(ph)} | 🔥 AI HOT:{len(aihot)}")
    return report


if __name__ == "__main__":
    asyncio.run(main())