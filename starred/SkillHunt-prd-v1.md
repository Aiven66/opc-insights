# Skill Hunt — AI Skills 发现平台
## 产品需求文档 PRD v1.0

> **产品代号**: Skill Hunt
> **版本**: v1.0
> **日期**: 2026-05-20
> **产品经理**: 小北Aiven
> **状态**: 🟡 调研完成，待开发

---

## 一、产品概述

### 1.1 一句话定位

**Skill Hunt** 是一个 AI Skills 领域的 Product Hunt —— 每日精选全球最优质的 AI Skills/Agents，发现并投票排名，帮助独立开发者和 AI PM 找到下一个爱不释手的工具。

### 1.2 产品 slogan

> **"Discover Tomorrow's AI Skills Today"**
> 中文：**发现下一个改变你工作流的 AI 技能**

### 1.3 目标用户

| 用户类型 | 画像描述 | 核心需求 |
|---------|---------|---------|
| **AI PM** | 用 AI Agent 做产品的产品经理 | 找灵感、看竞品、发现新工具 |
| **独立开发者** | 用 Skills/Agents 提升效率的工程师 | 发现好用的 Skill、贡献自己的作品 |
| **AI 爱好者** | 关注 AI 工具的自学者 | 了解最新 AI 工具趋势 |
| **企业决策者** | 采购 AI 工具的企业负责人 | 筛选靠谱的 AI 工具 |

### 1.4 核心价值主张

```
Product Hunt 让 SaaS 产品被发现
Skill Hunt 让 AI Skills 被发现
```

---

## 二、账号体系

### 2.1 用户角色

| 角色 | 说明 | 权限 |
|------|------|------|
| **游客** | 未登录用户 | 浏览排行榜（只读） |
| **普通用户** | 注册登录用户 | 浏览 + 投票 + 提交 Skill |
| **管理员** | admin@126.com | 审核 Skill + 管理平台 |

### 2.2 管理员账号

| 项目 | 内容 |
|------|------|
| **账号** | admin@126.com |
| **密码** | admin666 |
| **权限** | 审核所有提交 + 管理所有 Skill |

### 2.3 登录方式

| 场景 | 登录方式 |
|------|---------|
| **国内用户** | 邮箱 + 密码注册/登录 |
| **海外用户** | Google 一键登录 |
| **管理员** | 邮箱 + 密码（admin@126.com / admin666）|

### 2.4 登录页面设计

```
┌──────────────────────────────────────────────────────┐
│                                                       │
│                   🦀 Skill Hunt                       │
│           Discover Tomorrow's AI Skills Today          │
│                                                       │
│         ┌──────────────────────────────────┐        │
│         │  📧 Email Address                  │        │
│         └──────────────────────────────────┘        │
│         ┌──────────────────────────────────┐        │
│         │  🔒 Password                      │        │
│         └──────────────────────────────────┘        │
│                                                       │
│              [      Sign In       ]                  │
│                                                       │
│           ────────── or ───────────                   │
│                                                       │
│         ┌──────────────────────────────────┐        │
│         │  🔵 Continue with Google          │        │
│         └──────────────────────────────────┘        │
│                                                       │
│         Don't have an account? Sign up →              │
│                                                       │
└──────────────────────────────────────────────────────┘
```

---

## 三、界面设计规范

### 3.1 设计风格：Product Hunt 风格

**核心参考**: Product Hunt（全球最著名的 SaaS 产品发现平台）

**设计语言**:
- 干净、简洁、现代
- 卡片式布局，视觉层次清晰
- 投票按钮是最强的交互元素
- 以列表流为主，不是网格

### 3.2 配色方案

#### 浅色模式（Light Mode）

| 用途 | 色值 | 说明 |
|------|------|------|
| 主色 Primary | #5F6FFF | 科技紫蓝，Product Hunt 风 |
| 强调色 Accent | #DA5E0B | 橙色，投票/点赞按钮 |
| 背景色 Background | #FAFBFC | 极浅灰白 |
| 卡片背景 | #FFFFFF | 白色卡片 |
| 边框色 | #E5E7EB | 浅灰边框 |
| 文字主色 | #1A1A1A | 深黑文字 |
| 文字次色 | #6B7280 | 灰色次要文字 |
| 成功色 | #10B981 | 绿色 |
| 警告色 | #F59E0B | 橙色 |
| 错误色 | #EF4444 | 红色 |

#### 深色模式（Dark Mode）

| 用途 | 色值 | 说明 |
|------|------|------|
| 主色 Primary | #7B85FF | 浅紫蓝 |
| 强调色 Accent | #F97316 | 亮橙色 |
| 背景色 Background | #0D0D0D | 深黑 |
| 卡片背景 | #1A1A1A | 深灰卡片 |
| 边框色 | #2D2D2D | 深灰边框 |
| 文字主色 | #F9FAFB | 白色文字 |
| 文字次色 | #9CA3AF | 灰色次要文字 |

### 3.3 字体规范

| 用途 | 字体 | 大小 | 字重 |
|------|------|------|------|
| Logo/品牌 | Inter | 20px | 700 |
| H1 页面标题 | Inter | 28px | 700 |
| H2 区块标题 | Inter | 18px | 600 |
| H3 卡片标题 | Inter | 15px | 600 |
| Body 正文 | Inter | 14px | 400 |
| 辅助文字 | Inter | 12px | 400 |
| 按钮文字 | Inter | 14px | 500 |

### 3.4 圆角与间距

| 项目 | 规范 |
|------|------|
| 页面最大宽度 | 1200px |
| 页面内边距 | 24px（移动端 16px）|
| 卡片圆角 | 12px |
| 按钮圆角 | 8px |
| 输入框圆角 | 8px |
| 卡片间距 | 16px |
| 元素间距 | 8px |

### 3.5 Product Hunt 核心 UI 元素

```
[投票按钮]
    ▲
   123   ← 投票数
    ▼

[Skill 卡片]
┌─────────────────────────────────────────────────────┐
│ [图标] Skill名称                    ▲ 123          │
│         一句话描述（最多2行）                        │
│         来源平台：skillhub.cn | GitHub              │
│         🏷️ 标签1 标签2 标签3                       │
│         发布于 2小时前 | 👁️ 234views               │
└─────────────────────────────────────────────────────┘
```

### 3.6 多语言支持

| 语言 | 代码 | 说明 |
|------|------|------|
| **中文** | zh-CN | 默认语言（中国用户）|
| **English** | en-US | 海外用户 |

语言切换：页面右上角，图标按钮，点击切换，记住用户选择（localStorage）。

### 3.7 移动端适配

- 响应式断点：mobile < 768px，tablet 768-1024px，desktop > 1024px
- 移动端：单列卡片流，投票按钮固定在卡片右侧
- 触摸优化：按钮最小触控区域 44x44px

---

## 四、功能模块

### 4.1 首页（Home / 排行榜）

**路径**: `/` 或 `/rankings`

**功能**:
- 每日排行榜（默认当天）
- 历史排行榜（可切换日期）
- 分类筛选（All / AI Coding / Content / Productivity / ...）
- 来源筛选（All / skillhub.cn / GitHub / ClawHub / ...）
- 搜索（关键词 + 标签）
- 分页加载（无限滚动 or 分页按钮）

**排行榜卡片**:
```
┌────────────────────────────────────────────────────────┐
│  1️⃣  [图标] Skill名称                                   │
│            一句话描述...                                 │
│            🏷️ AI Coding  🏷️ GitHub                    │
│            ▲ 1,234票    👁️ 2,345浏览    2小时前        │
│            来源：skillhub.cn  作者：张三                  │
└────────────────────────────────────────────────────────┘
```

**顶部导航**:
```
[🦀 Skill Hunt Logo]   [排行榜] [提交Skill] [搜索___]   [🌙/☀️] [中/EN] [登录]
```

### 4.2 Skill 详情页

**路径**: `/skill/[slug]`

**功能**:
- Skill 封面图 + 名称 + 描述
- 投票按钮 + 当前票数
- 详细信息：
  - 来源平台（skillhub.cn / GitHub / ClawHub）
  - 作者信息
  - 发布时间
  - 标签
  - 功能描述（完整）
  - 安装/使用说明（Markdown）
  - 相关截图
- 相关推荐（同标签/同平台）
- 评论/讨论区

### 4.3 提交 Skill（Submit）

**路径**: `/submit`

**条件**: 需登录，未登录点击跳转登录页

**表单字段**:
```
┌─────────────────────────────────────────────────────┐
│  Submit a New Skill                                  │
│                                                      │
│  Skill名称 * [________________]                     │
│  一句话描述 * [________________]（最多80字）       │
│                                                      │
│  来源平台 * [▼ 选择平台]                             │
│          - skillhub.cn                               │
│          - GitHub                                    │
│          - ClawHub                                   │
│          - DeskHub                                   │
│          - 其他                                      │
│                                                      │
│  来源链接 * [________________]（原始Skill页面URL）   │
│                                                      │
│  图标/封面 [上传图片]（可选，最大2MB）               │
│                                                      │
│  详细描述 * [富文本编辑器]（支持Markdown）           │
│                                                      │
│  标签 * [添加标签]（最多5个）                       │
│                                                      │
│  安装说明 [富文本编辑器]（可选）                     │
│                                                      │
│  [预览]  [提交审核]                                  │
└─────────────────────────────────────────────────────┘
```

**审核状态说明**:
| 状态 | 说明 | 用户可见性 |
|------|------|-----------|
| pending | 等待审核 | 提交者可见，平台不可见 |
| approved | 审核通过 | 所有人可见 |
| rejected | 审核拒绝 | 提交者可见，附拒绝原因 |

### 4.4 管理后台（Admin）

**路径**: `/admin`

**条件**: 仅 admin@126.com 可访问，普通用户无法进入

**功能模块**:

#### 4.4.1 待审核列表

```
┌──────────────────────────────────────────────────────────┐
│  🛡️ 管理后台 — Skill审核                                  │
├──────────────────────────────────────────────────────────┤
│  [待审核 12] [已通过 45] [已拒绝 8] [全部列表]           │
├──────────────────────────────────────────────────────────┤
│  #001  一个Skill名称                                     │
│         提交者：user@example.com                          │
│         来源：skillhub.cn                                 │
│         提交时间：2026-05-20 10:30                        │
│         [查看详情] [通过] [拒绝]                          │
├──────────────────────────────────────────────────────────┤
│  #002  另一个Skill名称                                    │
│         ...                                              │
└──────────────────────────────────────────────────────────┘
```

**审核操作**:
- **通过**: 将 Skill 发布到排行榜，设置状态为 approved
- **拒绝**: 填写拒绝原因（必填），设置状态为 rejected
- **查看详情**: 弹出 Skill 完整信息模态框

#### 4.4.2 排行榜管理

- 设置首页置顶 Skill（最多3个）
- 编辑/删除已发布 Skill
- 查看投票统计

#### 4.4.3 用户管理

- 查看注册用户列表
- 禁用/启用用户
- 查看用户提交的 Skill

### 4.5 用户中心

**路径**: `/profile` 或 `/dashboard`

**功能**:
- 个人资料（头像、名称、简介）
- 我提交的 Skill（带审核状态标签）
- 我投票的 Skill
- 账号设置

### 4.6 搜索

**路径**: `/search?q=关键词`

**功能**:
- 关键词搜索（名称 + 描述 + 标签）
- 筛选：来源平台、分类标签、日期范围
- 搜索结果排序：最新 / 最热 / 最多投票

---

## 五、数据来源

### 5.1 第一期数据源：腾讯 SkillHub

**URL**: https://skillhub.cn/

**采集策略**:
1. **排行榜数据**: 采集 skillhub.cn 的官方排行榜（TOP 50）
2. **Skill 详情**: 采集每个 Skill 的名称、描述、作者、安装量、标签
3. **增量同步**: 每日自动采集一次增量更新
4. **数据存储**: 存入本地数据库（SQLite / PostgreSQL）

**数据字段映射**:

| skillhub.cn 字段 | Skill Hunt 字段 | 说明 |
|-----------------|---------------|------|
| skill_name | name | Skill 名称 |
| description | tagline | 一句话描述 |
| author | author | 作者 |
| install_count | installs | 安装量 |
| tags | tags | 标签数组 |
| category | category | 分类 |
| icon_url | icon | 图标 URL |
| source_url | source_url | 原始链接 |
| platform | source = 'skillhub' | 数据来源 |

### 5.2 第二期数据源（规划中）

| 数据源 | URL | 优先级 | 说明 |
|--------|-----|--------|------|
| **ClawHub** | clawhub.deskclaw.me | P1 | 海外 Agent Skills |
| **DeskHub** | skills.deskclaw.me | P1 | DeskClaw Skills |
| **GitHub Topics** | github.com/topics/agent | P2 | GitHub 上的 Agent 项目 |
| **OpenClaw Skills** | github.com/open-agents/sid | P2 | OpenClaw 官方 Skills |

### 5.3 数据采集频率

| 数据类型 | 频率 | 说明 |
|---------|------|------|
| 排行榜数据 | 每日 1 次 | 定时任务 |
| Skill 详情 | 每周 1 次 | 增量更新 |
| 用户提交 | 实时 | 人工审核 |

---

## 六、技术架构

### 6.1 技术栈

| 层级 | 技术选型 | 说明 |
|------|---------|------|
| **前端框架** | Next.js 14 + TypeScript | App Router |
| **UI 组件库** | TailwindCSS + shadcn/ui | Product Hunt 风格 |
| **状态管理** | Zustand + React Query | 全局状态 + 服务端状态 |
| **后端框架** | Next.js API Routes | 无缝前后端集成 |
| **数据库** | Supabase (PostgreSQL) | 免费 + 稳定 |
| **认证** | Supabase Auth | 邮箱 + Google OAuth |
| **文件存储** | Supabase Storage | Skill 图标/封面 |
| **数据采集** | Python 爬虫 + Cron | skillhub.cn 数据采集 |
| **部署** | Vercel（前端）+ Railway（后端/爬虫）| 免费额度够用 |

### 6.2 数据库设计

#### users 表

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255),
  full_name VARCHAR(255),
  avatar_url TEXT,
  bio TEXT,
  auth_provider VARCHAR(50) DEFAULT 'email', -- 'email' | 'google'
  role VARCHAR(50) DEFAULT 'user',          -- 'admin' | 'user'
  locale VARCHAR(10) DEFAULT 'zh-CN',         -- 'zh-CN' | 'en-US'
  theme VARCHAR(10) DEFAULT 'light',          -- 'light' | 'dark'
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

#### skills 表

```sql
CREATE TABLE skills (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  slug VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255) NOT NULL,
  tagline VARCHAR(255) NOT NULL,             -- 一句话描述（≤80字）
  description TEXT,                           -- 详细描述（Markdown）
  icon_url TEXT,
  cover_url TEXT,
  source VARCHAR(50) NOT NULL,                -- 'skillhub' | 'github' | 'clawhub' | 'deskhub' | 'user'
  source_url TEXT,                            -- 原始链接
  author_name VARCHAR(255),
  author_url TEXT,
  category VARCHAR(100),
  tags TEXT[],                                -- PostgreSQL 数组
  install_count INTEGER DEFAULT 0,
  status VARCHAR(50) DEFAULT 'pending',       -- 'pending' | 'approved' | 'rejected'
  rejection_reason TEXT,
  submitted_by UUID REFERENCES users(id),    -- 提交者（NULL 表示采集数据）
  verified BOOLEAN DEFAULT false,             -- 是否官方认证
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

#### votes 表

```sql
CREATE TABLE votes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  skill_id UUID REFERENCES skills(id) ON DELETE CASCADE,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(skill_id, user_id)                  -- 每人每 Skill 只能投一票
);
```

#### daily_rankings 表

```sql
CREATE TABLE daily_rankings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  skill_id UUID REFERENCES skills(id) ON DELETE CASCADE,
  ranking_date DATE NOT NULL,
  votes_count INTEGER DEFAULT 0,
  views_count INTEGER DEFAULT 0,
  rank_position INTEGER,                      -- 当天排名（1-N）
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(skill_id, ranking_date)
);
```

### 6.3 API 接口设计

#### 认证接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/auth/register` | POST | 邮箱注册 |
| `/api/auth/login` | POST | 邮箱登录 |
| `/api/auth/google` | GET | Google OAuth 跳转 |
| `/api/auth/google/callback` | GET | Google OAuth 回调 |
| `/api/auth/logout` | POST | 退出登录 |
| `/api/auth/me` | GET | 获取当前用户信息 |

#### Skills 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/skills` | GET | 获取 Skills 列表（支持筛选/分页）|
| `/api/skills/[slug]` | GET | 获取 Skill 详情 |
| `/api/skills/submit` | POST | 提交新 Skill（需登录）|
| `/api/skills/[slug]/vote` | POST | 投票（需登录）|
| `/api/skills/[slug]/vote` | DELETE | 取消投票（需登录）|
| `/api/rankings` | GET | 获取排行榜（支持日期筛选）|

#### Admin 接口（需 admin 权限）

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/admin/skills` | GET | 获取所有 Skill（含待审核）|
| `/api/admin/skills/[id]/approve` | POST | 审核通过 |
| `/api/admin/skills/[id]/reject` | POST | 审核拒绝 |
| `/api/admin/stats` | GET | 统计数据 |

#### 爬虫接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/crawl/skillhub` | POST | 手动触发 skillhub.cn 采集（仅管理员）|
| `/api/crawl/status` | GET | 查看采集状态 |

### 6.4 前端页面路由

```
app/
├── page.tsx                    # 首页 / 排行榜
├── skill/[slug]/page.tsx      # Skill 详情页
├── submit/page.tsx            # 提交 Skill
├── search/page.tsx            # 搜索页
├── profile/page.tsx           # 用户中心
├── admin/
│   └── page.tsx               # 管理后台（admin 专属）
├── auth/
│   ├── login/page.tsx         # 登录页
│   ├── register/page.tsx      # 注册页
│   └── callback/google/page.tsx  # Google OAuth 回调
└── api/                       # API Routes（同上）
```

---

## 七、定价方案

### 7.1 Freemium 模式

| 套餐 | 价格 | 功能 |
|------|------|------|
| **Free** | $0 | 浏览 + 投票；每月可提交 1 个 Skill |
| **Pro** | $5/月 | 无限提交 Skill；无广告；优先审核 |
| **Team** | $15/月 | 5个账号；团队管理；数据分析 |

### 7.2 收入来源

1. **订阅收入**: Pro + Team 套餐
2. **推荐佣金**: Skill 安装/购买抽佣
3. **企业定制**: 企业版私有化部署

---

## 八、里程碑

### Phase 1：MVP（4周）

```
Week 1: 基础建设
  □ 项目初始化（Next.js + Supabase）
  □ 登录/注册（邮箱 + Google）
  □ 首页排行榜 UI
  □ Skill 详情页
  □ 投票功能

Week 2: 采集 + 审核
  □ skillhub.cn 数据采集脚本
  □ 管理员审核后台
  □ 提交 Skill 表单

Week 3: 完善功能
  □ 搜索 + 筛选
  □ 用户中心
  □ 多语言切换
  □ 主题切换（Light/Dark）

Week 4: 上线 + 冷启动
  □ 部署到 Vercel
  □ ProductHunt 发布
  □ 腾讯云开发者社区推广
  □ 收集反馈 + 迭代
```

### Phase 2：增长（8周）

- 接入 ClawHub / DeskHub 数据源
- 开发 Newsletter（每周精选）
- 开发 API（供第三方调用）
- 开发 Slack/Discord 机器人推送

---

## 九、竞品分析

### 9.1 全球竞品

| 竞品 | URL | 月访问量 | 问题 |
|------|-----|---------|------|
| **Product Hunt** | producthunt.com | 500万 | 不是专门做 Skills 的，是全品类 |
| **SaaSHub** | saashub.com | 50万 | 做 SaaS 工具，不是 AI Skills |
| **AlternativeTo** | alternativeto.net | 800万 | 太大了，没有 AI Skills 垂直 |

### 9.2 国内竞品

| 竞品 | URL | 说明 |
|------|-----|------|
| **腾讯 SkillHub** | skillhub.cn | 最大的中文 Skills 平台，但没有投票/发现机制 |
| **扣子（Coze）** | coze.cn | 做 Bot，不是 Skills 聚合 |
| **Dify** | dify.ai | 做工作流，没有 Skills 聚合 |

### 9.3 核心竞品问题

```
Product Hunt：太大了，全品类，AI Skills 只是其中一小块
SaaSHub：同样是全品类，AI Skills 展示深度不够
腾讯 SkillHub：没有投票/发现机制，只是技能库
扣子/Coze：做 Bot 平台，不是 Skills 发现平台
```

### 9.4 Skill Hunt 的机会

```
✅ 垂直定位：只做 AI Skills 领域，比 Product Hunt 更专注
✅ 投票机制：Product Hunt 核心机制，我们直接复用
✅ 中英双语：覆盖全球用户
✅ 数据聚合：skillhub.cn + ClawHub + DeskHub + GitHub
✅ 极简体验：不做大而全，只做 Skills 发现这一件事
```

---

## 十、风险与合规

### 10.1 风险

| 风险 | 概率 | 影响 | 应对 |
|------|------|------|------|
| skillhub.cn 反爬 | 中 | 高 | 遵守 robots.txt，控制频率；接口尽量走 API |
| 数据版权 | 中 | 中 | 只采集公开信息，不存储原始 Skill 代码 |
| 用户增长慢 | 高 | 中 | 冷启动用采集数据填充，积累投票氛围 |
| 竞品抄袭 | 低 | 中 | 快速迭代，保持先发优势 |

### 10.2 合规

- 尊重各平台版权，数据仅用于展示引用
- 用户提交需审核，违规内容不发布
- GDPR 合规（欧盟用户数据保护）
- 隐私政策：明确数据使用范围

---

## 十一、附录

### 11.1 术语表

| 术语 | 说明 |
|------|------|
| **Skill** | AI Agent 的技能包/扩展，一个 Skill = 一套工作流/提示词 |
| **Skill Hunt** | 本产品名称 |
| **投票** | 用户对 Skill 的认可行为，类似 Product Hunt 的 upvote |
| **Rankings** | 每日排行榜，按投票数排序 |
| **Submit** | 用户提交新 Skill 到平台审核 |

### 11.2 竞品参考

- **Product Hunt**: https://producthunt.com — 核心参考，UI/UX 全面学习
- **Hacker News**: https://news.ycombinator.com — 极简排行榜风格
- **Reddit**: https://reddit.com — 社区讨论风格

### 11.3 参考资料

- 腾讯 SkillHub：https://skillhub.cn/ （第一期数据源）
- ClawHub：clawhub.deskclaw.me （第二期数据源）
- DeskHub：skills.deskclaw.me （第三期数据源）

---

*文档版本：v1.0 | 最后更新：2026-05-20*
