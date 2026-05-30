#!/usr/bin/env python3
"""
OPC一人公司MVP机会洞察 - YC视角简报生成器 v4.0
立场: YC CEO视角审查
"""

import asyncio
import httpx
import json
from datetime import datetime
from bs4 import BeautifulSoup
from pathlib import Path
from typing import Optional, List

# ============== 配置 ==============
CACHE_DIR = Path.home() / "opc-insights" / "cache"
REPORT_DIR = Path.home() / "opc-insights" / "reports"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
}

# AI关键词
AI_KEYWORDS = ["ai", "gpt", "llm", "chatbot", "nlp", "vision", "image", "video",
    "speech", "voice", "code", "writing", "assistant", "automation", "agent",
    "rag", "claude", "gemini", "copilot", "cursor", "bolt", "llama", "mistral", "qwen",
    "short video", "creator", "content", "course", "knowledge"]


def is_ai_related(title: str, desc: str = "") -> bool:
    text = f"{title} {desc}".lower()
    return any(kw in text for kw in AI_KEYWORDS)


def get_cache(name: str, max_age: int = 6) -> Optional[dict]:
    cache_file = CACHE_DIR / f"{name}.json"
    if cache_file.exists():
        mtime = datetime.fromtimestamp(cache_file.stat().st_mtime)
        age_hours = (datetime.now() - mtime).total_seconds() / 3600
        if age_hours < max_age:
            try:
                return json.load(open(cache_file))
            except:
                pass
    return None


def set_cache(name: str, data: dict):
    json.dump(data, open(CACHE_DIR / f"{name}.json", 'w'), ensure_ascii=False, indent=2)


async def fetch_url(client: httpx.AsyncClient, url: str, timeout: float = 5.0) -> Optional[str]:
    """异步获取URL"""
    try:
        resp = await client.get(url, timeout=timeout, follow_redirects=True)
        return resp.text
    except:
        return None


async def fetch_github_trending(client: httpx.AsyncClient) -> List[dict]:
    """抓取GitHub Trending"""
    print("📦 抓取 GitHub Trending...")
    
    cached = get_cache("github_trending")
    if cached:
        print("  ✓ 缓存命中")
        return cached.get("items", [])
    
    html = await fetch_url(client, "https://github.com/trending")
    items = []
    
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        repos = soup.select('article.Box-row')
        print(f"  ✓ 获取 {len(repos)} 个仓库")
        
        for repo in repos[:25]:
            try:
                title = repo.select_one('h2 a')
                if not title:
                    continue
                full_name = title.get('href', '').strip('/')
                if '/' not in full_name:
                    continue
                
                desc = repo.select_one('p')
                description = desc.text.strip() if desc else ""
                
                if is_ai_related(full_name, description):
                    stars = repo.select_one('a[href$="/stargazers"]')
                    items.append({
                        "name": full_name,
                        "description": description[:100],
                        "stars": stars.text.strip().replace(',', '') if stars else "0",
                        "url": f"https://github.com/{full_name}",
                        "source": "GitHub Trending"
                    })
            except:
                continue
    else:
        print("  → GitHub访问受限，使用推荐列表")
        items = FALLBACK_PROJECTS
    
    set_cache("github_trending", {"items": items})
    print(f"  ✓ 共 {len(items)} 个AI项目")
    return items


async def fetch_hackernews(client: httpx.AsyncClient) -> List[dict]:
    """抓取HackerNews"""
    print("📦 抓取 HackerNews...")
    
    cached = get_cache("hackernews")
    if cached:
        print("  ✓ 缓存命中")
        return cached.get("items", [])
    
    items = []
    try:
        resp = await fetch_url(client, "https://hacker-news.firebaseio.com/v0/topstories.json")
        if resp:
            top_ids = json.loads(resp)[:25]
            print(f"  → 获取 {len(top_ids)} 个故事ID")
            
            for story_id in top_ids:
                try:
                    story_resp = await fetch_url(client, 
                        f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json")
                    if story_resp:
                        story = json.loads(story_resp)
                        if is_ai_related(story.get('title', '')):
                            items.append({
                                "name": story.get('title', ''),
                                "description": story.get('text', '')[:150] if story.get('text') else '',
                                "url": story.get('url', ''),
                                "score": story.get('score', 0),
                                "source": "HackerNews"
                            })
                except:
                    continue
    except Exception as e:
        print(f"  ✗ {e}")
    
    set_cache("hackernews", {"items": items})
    print(f"  ✓ 获取 {len(items)} 个AI讨论")
    return items


FALLBACK_PROJECTS = [
    {"name": "ollama/ollama", "description": "本地运行Llama、Mistral等大模型", "stars": "48k", "url": "https://github.com/ollama/ollama", "source": "推荐"},
    {"name": "2noise/ChatTTS", "description": "开源生成式语音模型", "stars": "20k", "url": "https://github.com/2noise/ChatTTS", "source": "推荐"},
    {"name": "continuedev/continue", "description": "GPT-4代码助手", "stars": "13k", "url": "https://github.com/continuedev/continue", "source": "推荐"},
    {"name": "ggerganov/llama.cpp", "description": "纯C/C++实现的LLaMA推理", "stars": "60k", "url": "https://github.com/ggerganov/llama.cpp", "source": "推荐"},
    {"name": "dify-ai/dify", "description": "开源LLM应用平台", "stars": "35k", "url": "https://github.com/dify-ai/dify", "source": "推荐"},
]


# ============== YC视角分析 ==============

# 这些是废话方向（大厂已做或红海）
BULLSHIT_DIRECTIONS = [
    {
        "name": "AI Meeting Summary",
        "why": "钉钉、飞书、企业微信已经做了，而且是免费的",
        "verdict": "❌ NO"
    },
    {
        "name": "AI Code Review",
        "why": "GitHub Copilot已经做了，GitHub原生集成",
        "verdict": "❌ NO"
    },
    {
        "name": "AI Browser Extension",
        "why": "Chrome商店几千个，红海市场",
        "verdict": "❌ NO"
    },
    {
        "name": "通用AI助手",
        "why": "ChatGPT、Claude已经做了，做不过",
        "verdict": "❌ NO"
    },
    {
        "name": "AI写作工具",
        "why": "Jasper、Copy.ai已经做了，营销文案红海",
        "verdict": "❌ NO"
    },
]


def analyze_trending_items(items: List[dict]) -> dict:
    """分析趋势项目，识别机会"""
    
    # 分类统计
    categories = {
        "coding_agent": 0,
        "content_creator": 0,
        "education": 0,
        "productivity": 0,
        "vertical": 0,
    }
    
    opportunities = []
    
    for item in items:
        name = item.get('name', '').lower()
        desc = item.get('description', '').lower()
        text = f"{name} {desc}"
        
        # 检测类别
        if any(kw in text for kw in ['agent', 'coding', 'code', 'dev']):
            categories["coding_agent"] += 1
        if any(kw in text for kw in ['video', 'content', 'creator', 'tutor', 'course']):
            categories["content_creator"] += 1
        if any(kw in text for kw in ['tutor', 'learn', 'education', 'student']):
            categories["education"] += 1
        if any(kw in text for kw in ['meeting', 'calendar', 'schedule', 'task']):
            categories["productivity"] += 1
        if any(kw in text for kw in ['legal', 'medical', 'finance', 'real estate', 'industry']):
            categories["vertical"] += 1
        
        # 识别垂直行业机会
        vertical_keywords = {
            "留学文书": ["study abroad", "university", "application", "文书"],
            "法律合同": ["contract", "legal", "agreement", "合同"],
            "医疗健康": ["medical", "health", "clinic", "医疗"],
            "金融投研": ["finance", "investment", "stock", "金融"],
            "短视频创作": ["video", "short", "creator", "clip", "视频"],
            "知识付费": ["course", "knowledge", "education", "付费"],
            "私域运营": ["community", "engagement", "私域", "社群"],
        }
        
        for vertical, keywords in vertical_keywords.items():
            if any(kw in text for kw in keywords):
                opportunities.append({
                    "item": item,
                    "vertical": vertical,
                    "keywords": [k for k in keywords if k in text]
                })
    
    return {
        "categories": categories,
        "opportunities": opportunities[:5],  # 最多5个垂直机会
    }


def generate_yc_report(github_items: List, hn_items: List) -> str:
    """生成YC视角的简报"""
    
    today = datetime.now().strftime("%Y-%m%d")
    today_cn = datetime.now().strftime("%Y年%m月%d日")
    
    # 排序
    def parse_stars(s):
        s = str(s).replace('k', '').replace('.', '')
        try:
            return int(s) * 1000 if 'k' in str(s).lower() else int(s)
        except:
            return 0
    
    sorted_github = sorted(github_items, key=lambda x: parse_stars(x.get('stars', '')), reverse=True)
    sorted_hn = sorted(hn_items, key=lambda x: x.get('score', 0), reverse=True) if hn_items else []
    
    # 分析趋势
    analysis = analyze_trending_items(sorted_github)
    
    report = f"""# 🚀 一人公司MVP机会洞察

**立场**: YC CEO视角审查
**时间**: {today_cn}
**数据**: GitHub Trending {len(sorted_github)}个 | HN {len(sorted_hn)}个

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

## 🔥 今日趋势分析

### 赛道热度

"""

    # 赛道热度
    cats = analysis["categories"]
    hot_tracks = sorted(cats.items(), key=lambda x: x[1], reverse=True)
    for track, count in hot_tracks[:5]:
        heat = "🔥" * min(count, 5)
        track_name = {
            "coding_agent": "AI Coding Agent",
            "content_creator": "内容创作工具",
            "education": "教育科技",
            "productivity": "效率工具",
            "vertical": "垂直行业",
        }.get(track, track)
        report += f"- {heat} **{track_name}** ({count}个相关项目)\n"

    report += """
### 垂直行业机会（值得深挖）

"""
    
    if analysis["opportunities"]:
        for opp in analysis["opportunities"]:
            item = opp["item"]
            stars = item.get('stars', '-')
            report += f"**{opp['vertical']}** - {item['name']} ⭐{stars}\n"
            report += f"- {item['description'][:60]}...\n"
            report += f"- [链接]({item['url']})\n\n"
    else:
        report += "_暂无明显垂直行业机会，继续观察_\n\n"

    report += """---

## 🎯 真正值得切入的方向（4个）

### 方向1: 短视频口播的"AI剪辑工作室"

**你观察到的痛点：**
- 口播博主录一条10分钟视频，前期+剪辑+发布要2-3小时
- 写脚本最难，剪视频最费时间
- 一个人做账号，根本忙不过来

**为什么一人公司能做：**
- 不是通用剪辑工具，而是"口播博主专用"
- 深度集成：脚本生成 → 视频剪辑 → 字幕生成 → 多平台发布
- 大厂不会为这个细分场景做定制

**MVP功能（按优先级）：**

| 功能 | 为什么做 | 节省时间 |
|------|---------|---------|
| 音频转文字+智能分段 | 最痛点 | 1小时/天 |
| 自动生成3种标题+封面语 | 提高点击率 | 30分钟 |
| 一键提取金句片段 | 分发其他平台 | 30分钟 |
| 多平台草稿箱同步 | 减少重复操作 | 20分钟 |

**变现路径：**
- 免费：基础转录
- $9.9/月：无限转录+标题生成
- $29.9/月：全功能+多平台发布

**护城河：** 博主的工作流数据 = 最懂这个行业的AI

---

### 方向2: 知识付费的"内容印钞机"

**你观察到的痛点：**
- 知识IP想变现，但做课太累
- 一门课要录几十个小时，根本没时间
- 做了课不知道怎么卖

**为什么一人公司能做：**
- 懂内容创作者的痛
- 能做"内容→课程"的自动化流水线
- 大厂做的是平台，不是服务

**MVP功能：**

```
输入：一篇公众号文章 or 一段录音
     ↓
AI自动：
  - 提取核心观点和案例
  - 生成课程大纲（20-30节）
  - 生成每节讲稿（1500字左右）
  - 生成配套PPT大纲
  - 生成引流文案
     ↓
输出：一门完整的录播课素材包
```

**变现路径：**
- $99/次：完整课程素材包
- $299/月：无限生成+导师答疑
- 代运营：帮做课+发布+推广，抽成

**关键洞察：** 不是卖工具，是卖"时间"。帮博主从100小时→5小时做出一门课。

---

### 方向3: 私域运营的"AI客服+销售"

**你观察到的痛点：**
- 私域群里要不断发内容、维护用户
- 客服回复慢，用户流失
- 不知道什么时间发、怎么发效果最好

**为什么一人公司能做：**
- 深度理解私域运营套路
- 能做"人+AI"的混合服务
- 大厂做的是通用客服，不懂私域

**MVP功能（知识付费/电商私域群）：**

1. 根据用户消息，生成个性化回复
2. 自动发早报/晚报（结合时事热点）
3. 识别高意向用户，推送给真人跟进
4. 分析最佳发消息时间
5. 生成朋友圈文案（带配图建议）

**变现路径：**
- 按群数量：¥299/月/群
- 按用户数：¥999/月/500人

**护城河：** 运营SOP = 行业Know-how

---

### 方向4: 垂直行业的"AI专家Agent"

**核心逻辑：** 不是通用AI，而是"懂你行业的AI"

| 行业 | 痛点 | AI能做什么 |
|------|------|----------|
| 律所 | 合同审查慢 | AI初筛+标注风险点 |
| 医美 | 咨询转化低 | AI预问诊+方案生成 |
| 留学中介 | 文书重复劳动 | AI文书初稿+润色 |
| 猎头 | 候选人匹配 | AI简历解析+推荐理由 |
| 民宿 | 点评回复 | AI生成个性化回复 |

**为什么一人公司能做：**
- 大厂不做细分行业的深度定制
- 需要行业经验，不是纯技术

**推荐从留学中介切入：**
- 痛点强：文书是最大瓶颈
- 付费意愿高：留学中介客单价几万
- 壁垒清晰：懂留学=懂申请=懂文书

**变现路径：**
- SaaS订阅：¥999/月/账号
- 按文书数量：¥50/份
- 私有化部署：¥5万/家

---

## 💎 最高ROI的方向组合

| 组合 | 推荐度 | 时机 | 用户 | 壁垒 | 你的优势 |
|------|--------|------|------|------|----------|
| **A: 短视频创作者工具包** | ★★★★★ | 短视频仍是最大增量 | 口播博主、知识IP、微课讲师 | 工作流数据+行业理解 | AI PM懂产品，内容创作者背景，可自己当种子用户 |
| **B: 知识付费内容工厂** | ★★★★☆ | 知识付费进入下半场 | 想变现但没时间的知识IP | 做课SOP+AI内容质量 | 做过公众号内容，懂内容创作的坑，能做真实交付 |
| **C: 私域运营自动化** | ★★★☆☆ | 私域越来越卷，需要差异化 | 知识付费/电商/本地生活商家 | 运营SOP | 有微信生态资源，懂运营套路 |

---

## 📋 YC审查意见

**❌ 不要做：**
- AI Meeting Summary（钉钉做了）
- AI Code Review（GitHub做了）
- AI Browser Extension（红海）
- 任何"通用"的东西

**✅ 要做：**
- 垂直场景的深度解决方案
- 大厂不屑于做的脏活累活
- 有人愿意为"省时间"付高价

**最关键的问题：**
1. 你在解决谁的具体问题？
2. 他们现在怎么解决的？
3. 为什么他们愿意切换到你的方案？

---

## 🎯 行动建议（本周必须完成）

**第一步：选方向（明天）**
- [ ] 短视频口播工具 —— 技术门槛低，快速MVP
- [ ] 知识付费内容工厂 —— 变现快，客单价高
- [ ] 留学文书Agent —— 细分赛道，竞争少

**第二步：找10个真实用户聊（3天内）**
- 问：你现在怎么做这个？
- 问：你愿意付多少钱解决？
- 问：如果只能保留1个功能，是什么？

**第三步：做最小的MVP（2周内）**
- 不用做完整产品
- 先用现有工具拼一个"人工+AI"的流程
- 验证有人真的愿意付钱

---

*📌 本简报由OPC Insights系统生成*
*🔄 每日早9点自动更新*
"""

    return report


async def main():
    print("\n" + "="*50)
    print("🚀 一人公司MVP机会洞察 - YC视角")
    print("="*50 + "\n")
    
    async with httpx.AsyncClient(headers=HEADERS) as client:
        # 并发抓取
        github_task = fetch_github_trending(client)
        hn_task = fetch_hackernews(client)
        
        github_items, hn_items = await asyncio.gather(github_task, hn_task)
    
    print("\n📝 生成YC视角简报...")
    report = generate_yc_report(github_items, hn_items)
    
    today_str = datetime.now().strftime("%Y-%m-%d")
    report_file = REPORT_DIR / f"mvp-insights-yc-{today_str}.md"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ 简报已生成!")
    print(f"   📁 {report_file}")
    print(f"   📊 GitHub: {len(github_items)} | HN: {len(hn_items)}")
    
    return report


if __name__ == "__main__":
    asyncio.run(main())
