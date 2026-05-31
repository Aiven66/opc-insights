# 🎯 OPC Insights - AI MVP 产品洞察系统

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![GitHub Stars](https://img.shields.io/github/stars/Aiven66/opc-insights?style=flat-square)
![Version](https://img.shields.io/badge/version-v11.0-blue.svg)

**YC 视角的 AI 产品方向发现系统 · 每天 6 个可执行的 MVP 方向 · 产品11问深度评估**

[快速开始](#-快速开始) · [每日洞察日报](#-每日洞察日报) · [产品11问评估](#-产品11问深度评估) · [核心方法论](#-核心方法论) · [数据源](#-数据源)

</div>

---

## 🔥 什么是 OPC Insights？

OPC Insights 是面向**独立开发者/一人公司**的 AI 产品洞察工具，每天自动发现可商业化的 MVP 产品方向。

**两大核心功能**：

| 功能 | 说明 | 运行 |
|------|------|------|
| 📅 **每日洞察日报** | 5大信息源 × 6个MVP方向 × 深度分析 | `python3 scripts/generate_v10.py` |
| 🎯 **产品11问评估** | 11维度深度分析 × 综合评分 × 行动建议 | `python3 scripts/product_11_questions.py` |

---

## 🚀 快速开始

### 安装

```bash
git clone https://github.com/Aiven66/opc-insights.git
cd opc-insights
pip install -r requirements.txt
```

### 方式一：每日洞察日报

```bash
# 生成今日洞察日报（每天6个MVP方向）
python3 scripts/generate_v10.py

# 输出: reports/mvp-insights-yc-YYYY-MM-DD.md
```

### 方式二：产品11问评估

```bash
# 自动评估（使用默认分析）
python3 scripts/product_11_questions.py --auto "产品名称" "一句话定位"

# 分析星标产品
python3 scripts/product_11_questions.py --starred "H3-PostAI"

# 交互式评估
python3 scripts/product_11_questions.py
# → 输入产品名称和定位
# → 逐一回答11问（或直接回车使用默认评估）
# → 生成 starred/*-11问-YYYY-MM-DD.md

# 输出: starred/*-11问-YYYY-MM-DD.md
```

---

## 📅 每日洞察日报

### 输出示例

每天自动采集 **5大信息源**，输出 **6个MVP产品方向**：

```
🦀 OPC MVP深度洞察日报 | 2026-05-31

📊 今日信息源
  GitHub Trending: 19个AI项目
  ProductHunt: 10个新品
  Twitter/X: AI产品热帖
  国内平台: 小红书/B站需求信号
  AI HOT: 60条动态

🎯 今日6个MVP产品方向
  1. PostAI（AI社媒文案生成器） 4.70/5 🌐海外 C端
  2. CleanVoice（AI音频去噪） 4.70/5 🌐海外 C端
  3. UpscaleAI（AI图片放大） 4.70/5 🌐海外 C端
  4. TaxFlow（出海税务合规） 4.55/5 🇨🇳国内 B端
  5. QuoteBot（B2B报价助手） 4.55/5 🇨🇳国内 B端
  6. WeChatSEO（公众号SEO） 4.55/5 🇨🇳国内 B端
```

### 每个方向包含

- 📍 **推荐理由** — 深度洞察和信号分析
- 🔍 **竞品分析** — 定价/问题/空白
- 💡 **MVP切入点** — 功能/技术/定价
- ⚡ **本周行动** — 具体执行步骤

---

## 🎯 产品11问深度评估

### 11问框架

| # | 问题 | 权重 | 核心目的 |
|---|------|------|---------|
| 1 | 产品要解决什么问题？ | 20% | 痛点真实性 |
| 2 | 为谁解决这些问题？ | 15% | 目标用户 |
| 3 | 有多少人真的需要？ | 10% | 市场规模 |
| 4 | 目前有哪些解决方案？ | 15% | 竞品分析 |
| 5 | 我们的解决方案是什么？ | 20% | 差异化定位 |
| 6 | 怎么判断第一阶段成功？ | 5% | 成功指标 |
| 7 | 现在做的时机合适吗？ | 5% | 时机判断 |
| 8 | 成功的必要条件是哪些？ | 5% | 关键路径 |
| 9 | 有哪些重要原则？ | 3% | 价值观对齐 |
| 10 | 怎样完成冷启动？ | 2% | 增长飞轮 |
| 11 | 优先验证哪些价值点？ | 0% | 验证优先级 |

### 综合评分

| 评分 | 结论 | 行动 |
|------|------|------|
| ⭐⭐⭐⭐⭐ (4.5-5.0) | 强烈推荐 | 立刻开始MVP |
| ⭐⭐⭐⭐☆ (3.5-4.4) | 推荐 | 可以开始 |
| ⭐⭐⭐☆☆ (2.5-3.4) | 观望 | 继续调研 |
| ⭐⭐☆☆☆ (1.5-2.4) | 不推荐 | 重新思考 |

### 使用示例

```bash
# 评估一个新想法
python3 scripts/product_11_questions.py --auto "VoiceBlog" "语音转播客，一键生成个人品牌内容"

# 分析星标产品
python3 scripts/product_11_questions.py --starred "N4-cleanvoice"
```

---

## ⭐ 核心方法论

### 刘小排 MVP 成功公式（7要素）

| # | 要素 | 权重 | 说明 |
|---|------|------|------|
| 1 | 竞品已验证 | 20% | 有竞品在收钱（最重要） |
| 2 | 免费+免登录 | 15% | 无限生成获取流量 |
| 3 | 极简输入 | 15% | 3秒上手，0学习成本 |
| 4 | AI能力加持 | 15% | 蹭热点技术 |
| 5 | 单一功能极致 | 15% | 只做一件事 |
| 6 | Freemium变现 | 10% | $9-29/月 |
| 7 | 全球用户 | 10% | 英文界面，美元定价 |

### 市场选择原则

| 类型 | 市场 | 逻辑 |
|------|------|------|
| C端产品 | 🌐 海外优先 | 美元定价，用户基数大 |
| B端产品 | 🇨🇳 国内优先 | 服务优势，本地化需求 |

---

## 📊 数据源（5大信息源）

| # | 信息源 | 数据量 |
|---|--------|--------|
| 1 | **GitHub Trending** | ~20个项目/天 |
| 2 | **ProductHunt** | ~10个产品/天 |
| 3 | **Twitter/X** | ~10条热帖/天 |
| 4 | **国内平台** | ~10条需求/天 |
| 5 | **AI HOT** | ~60条动态/天 |

---

## 📁 项目结构

```
opc-insights/
├── scripts/
│   ├── generate_v10.py              # 每日洞察日报生成器（v10.0）
│   ├── product_11_questions.py        # 产品11问评估工具（v1.1）✅ 新增
│   └── OPC_INSIGHTS_SKILL.md         # 技能文档
├── reports/                          # 每日洞察日报
│   └── mvp-insights-yc-*.md
├── starred/                          # 星标产品库（个人使用）
│   ├── README.md                    # 索引
│   └── *-11问-*.md                  # 11问评估报告 ✅ 新增
├── .github/workflows/                # GitHub Actions
│   └── daily-insights.yml           # 自动生成日报
├── README.md                         # 本文件
├── requirements.txt
└── LICENSE
```

---

## 🔧 自定义配置

### 修改评分标准

编辑 `scripts/generate_v10.py` 中的 `generate_deep_insights()` 函数。

### 添加新数据源

编辑 `scripts/generate_v10.py` 中的 `fetch_*` 函数。

### 修改11问答案

编辑 `scripts/product_11_questions.py` 中的 `AUTO_ANSWERS` 字典。

---

## 🤝 贡献

欢迎提交 Issue 或 PR！

```bash
# Fork 后
git clone https://github.com/YOUR_USERNAME/opc-insights.git
cd opc-insights

# 创建分支
git checkout -b feature/amazing

# 提交
git commit -m 'Add amazing feature'
git push origin feature/amazing

# 提 PR
```

---

## 📝 License

MIT License · 2026 · Aiven

---

<div align="center">

**Built with 🦀 by [Aiven](https://github.com/Aiven66)**

⭐ Star 支持一下！

</div>
