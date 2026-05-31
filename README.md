# 🎯 OPC Insights - AI MVP 产品洞察系统

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![GitHub Stars](https://img.shields.io/github/stars/Aiven66/opc-insights?style=flat-square)
![GitHub Forks](https://img.shields.io/github/forks/Aiven66/opc-insights?style=flat-square)

**YC 视角的 AI 产品方向发现系统 · 每天 6 个可执行的 MVP 方向**

[English](./README_EN.md) · [快速开始](#-快速开始) · [核心方法论](#-核心方法论) · [数据源](#-数据源) · [部署](#-部署)

</div>

---

## 🔥 什么是 OPC Insights？

OPC Insights 是一款**面向独立开发者/一人公司的 AI 产品洞察工具**。

每天自动抓取 **5 大信息源**，应用 **YC 方法论 + 刘小排 MVP 成功公式**，输出 **6 个可执行的产品方向**——每个方向包含：
- ✅ 推荐理由（深度洞察）
- ✅ 竞品分析（谁在收钱）
- ✅ MVP 切入点（1 人 1 周能搞定）
- ✅ 本周行动（具体执行步骤）

它的核心逻辑是 **YC CEO Garry Tan 的方法论**：

> **独立开发者最大的机会 = 大公司不屑做 / 不能做 / 做不好的事情**

不是"做一个比 ChatGPT 更好的 AI"，而是**做一个细分场景下的 AI 工具**。

---

## ⭐ 核心方法论

### 刘小排 MVP 成功公式（7 要素）

| # | 要素 | 说明 |
|---|------|------|
| 1 | **竞品已验证** | 有竞品在收钱（最重要） |
| 2 | **免费+免登录** | 无限生成获取流量 |
| 3 | **极简输入** | 3 秒上手，0 学习成本 |
| 4 | **AI 能力加持** | 蹭热点技术（GPT-4o 等） |
| 5 | **单一功能极致** | 只做一件事，做到行业第一 |
| 6 | **Freemium 变现** | 免费引流，付费增值 $9-29/月 |
| 7 | **全球用户** | 英文界面，美元定价 |

### 市场选择原则

| 类型 | 市场 | 逻辑 |
|------|------|------|
| **C 端产品** | 🌐 海外优先 | 美元定价，用户基数大 |
| **B 端产品** | 🇨🇳 国内优先 | 服务优势，本地化需求 |

---

## 📊 数据源（5 大信息源）

| # | 信息源 | 说明 | 数据量 |
|---|--------|------|--------|
| 1 | **GitHub Trending** | AI 项目热度 + 开源趋势 | ~20 个/天 |
| 2 | **ProductHunt** | 海外 AI 新品发布 | ~10 个/天 |
| 3 | **Twitter/X** | AI 行业热帖 + 产品发布 | ~10 条/天 |
| 4 | **国内平台** | 小红书/B站需求信号 | ~10 条/天 |
| 5 | **AI HOT** | 每日 AI 行业资讯精选 | ~50 条/天 |

---

## 🚀 快速开始

### 环境要求

- Python 3.10+
- 网络连接（抓取 GitHub/API 数据）

### 安装

```bash
# Clone 项目
git clone https://github.com/Aiven66/opc-insights.git
cd opc-insights

# 安装依赖
pip install httpx beautifulsoup4 feedparser requests

# 运行日报
python3 scripts/generate_v10.py
```

### 输出

```
reports/mvp-insights-yc-YYYY-MM-DD.md
```

---

## 📁 项目结构

```
opc-insights/
├── scripts/                    # 洞察日报生成脚本
│   ├── generate_v10.py        # 最新版本（v10.0 深度洞察版）
│   ├── generate_v7.py         # v7.0 全平台版
│   └── OPC_INSIGHTS_SKILL.md  # 技能文档
├── reports/                   # 每日洞察日报
│   └── mvp-insights-yc-*.md   # 每日报告
├── starred/                   # 星标产品方向库（个人使用）
│   ├── README.md              # 索引
│   └── *-prd-v*.md           # PRD 文档
├── .gitignore
├── README.md
└── LICENSE
```

---

## 🔧 自定义配置

### 修改脚本版本

```bash
# 深度洞察版（推荐）：每天 6 个方向，深度分析
python3 scripts/generate_v10.py

# 全平台版：3 个方向 + YC废话检测
python3 scripts/generate_v7.py
```

### 添加新的数据源

编辑 `scripts/generate_v10.py`，在 `fetch_*` 函数中添加新的数据抓取逻辑。

### 修改评分标准

编辑 `generate_deep_insights()` 函数中的评分逻辑和筛选条件。

---

## 📖 延伸阅读

- [YC Startup Ideas](https://www.ycombinator.com/documents) — YC 官方创业指南
- [How to Get Startup Ideas](https://www.youtube.com/watch?v=nvuo2lc0JJ4) — Paul Graham
- [刘小排 Raphael AI](https://www.raphael-ai.com) — MVP 成功案例
- [Indie Hackers](https://www.indiehackers.com) — 独立开发者社区

---

## 🤝 贡献

欢迎提交 Issue 或 PR！

### 如何贡献

1. **Fork** 这个仓库
2. **创建特性分支** (`git checkout -b feature/amazing`)
3. **提交更改** (`git commit -m 'Add amazing feature'`)
4. **推送到分支** (`git push origin feature/amazing`)
5. **创建 Pull Request**

### 报告问题

如果你发现了 bug 或有新功能建议，请提交 [Issue](https://github.com/Aiven66/opc-insights/issues)。

---

## 📝 License

本项目基于 MIT License 开源。

---

## 🙏 致谢

- **YC** — Startup 方法论
- **刘小排 Raphael** — MVP 成功公式
- **ProductHunt** — 产品发现平台
- **GitHub Trending** — 开源项目趋势

---

<div align="center">

**Built with 🦀 by [Aiven](https://github.com/Aiven66)**

如果你觉得这个项目有用，欢迎 ⭐ Star！

</div>
