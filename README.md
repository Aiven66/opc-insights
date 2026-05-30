# 🎯 OPC Insights - AI MVP 产品洞察系统

> YC 视角的 AI 产品方向发现系统，每日自动抓取 GitHub Trending + HackerNews + ProductHunt + AI HOT，输出可执行的产品方向建议。

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 📌 什么是 OPC Insights？

OPC Insights 是一款**面向独立开发者/一人公司的 AI 产品洞察工具**。

它的核心逻辑是 YC CEO Garry Tan 的方法论：

> **独立开发者最大的机会 = 大公司不屑做 / 不能做 / 做不好的事情**

不是"做一个比 ChatGPT 更好的 AI"，而是"做一个细分场景下的 AI 工具"。

---

## 🧠 方法论：刘小排 MVP 成功公式

| # | 要素 | 权重 | 说明 |
|---|------|------|------|
| 1 | 竞品已验证 | 20% | 有竞品在收钱（最重要）|
| 2 | 免费+免登录 | 15% | 无限生成获取流量 |
| 3 | 极简输入 | 15% | 3 秒上手，0 学习成本 |
| 4 | AI 能力加持 | 15% | 蹭热点技术 |
| 5 | 单一功能极致 | 15% | 只做一件事，做到行业第一 |
| 6 | Freemium 变现 | 10% | 免费引流，付费增值 $9-29/月 |
| 7 | 全球用户 | 10% | 英文界面，美元定价 |

---

## 📊 数据源（5 大信息源）

| # | 信息源 | 说明 |
|---|--------|------|
| 1 | GitHub Trending | 抓取 AI 项目热度 |
| 2 | HackerNews | 技术社区讨论热点 |
| 3 | ProductHunt | 产品发布趋势 |
| 4 | B站/国内平台 | 国内 AI 产品动态 |
| 5 | AI HOT (aihot.virxact.com) | 每日 AI 行业资讯精选 |

---

## 🚀 快速开始

### 环境要求

- Python 3.10+
- 网络连接（抓取 GitHub/API 数据）

### 安装依赖

```bash
cd ~/opc-insights
pip install httpx feedparser requests
```

### 运行日报

```bash
python3 scripts/generate_v7.py
```

输出文件：`reports/mvp-insights-yc-YYYY-MM-DD.md`

---

## 📁 项目结构

```
opc-insights/
├── scripts/              # 洞察日报生成脚本
│   ├── generate_v7.py    # 最新版本（v7.0）
│   └── OPC_INSIGHTS_SKILL.md  # 技能文档
├── reports/              # 每日洞察日报
│   └── mvp-insights-yc-*.md
└── starred/              # 星标产品方向库
    ├── README.md          # 索引
    └── *-prd-v*.md       # PRD 文档
```

---

## 🎯 星标产品库（已验证方向）

| # | 产品 | 方向 | 推荐度 | 状态 |
|---|------|------|--------|------|
| 001 | ArticleShort | 文章转视频脚本 | ★★★★★ | 🟡 待验证 |
| 002 | WeChatSEO | 微信搜索优化 | ★★★★★ | 🟡 待验证 |
| 003 | AI日报Pro | AI 行业情报订阅 | ★★★★★ | 🔴 调研中 |
| 004 | VoiceBeautify | 音频声音美化 | ★★★★★ | 🟡 待验证 |
| 005 | CleanVoice | 播客去噪 | ★★★★☆ | 🟡 待验证 |
| 006 | ThumbAI | 视频缩略图生成 | ★★★★☆ | 🟡 待验证 |
| 007 | PostAI | 社媒文案生成 | ★★★★☆ | 🟡 待验证 |
| 008 | WatchDog | 出海竞品监控 | ★★★★★ | 🔴 调研中 |

---

## 🔄 使用流程

```
每日早上 9:00（自动）
    │
    ▼
运行 generate_v7.py
    │
    ├── 抓取 5 大信息源
    ├── 应用 7 要素评分
    ├── 去重 + 废话检测
    │
    ▼
输出今日洞察报告
    │
    ├── 今日最大信号
    ├── 通过筛选的新方向
    ├── 继续推进的星标方向
    └── 本周行动建议
    │
    ▼
人工筛选 + 决策
    │
    ▼
选方向 → 产品 11 问验证 → PRD → MVP
```

---

## 📖 延伸阅读

- [YC Startup Ideas](https://www.ycombinator.com/documents) — YC 官方创业指南
- [How to Get Startup Ideas](https://www.youtube.com/watch?v=nvuo2lc0JJ4) — Paul Graham
- [刘小排 Raphael AI](https://www.raphael-ai.com) — MVP 成功案例

---

## 🤝 贡献

欢迎提交 Issue 或 PR！

如果你发现了有趣的 AI 产品方向，或者有改进建议，欢迎联系我。

---

## 📝 License

MIT License

---

> **Built with 🦀 by Aiven**
> 公众号：AI小北学AI
