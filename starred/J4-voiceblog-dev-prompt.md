# VoiceBlog - 海外个人品牌AI播客工具

## AI编程项目提示词

---

## 📋 项目概述

### 一句话定位

> 把你的文字内容，一键变成你自己声音的播客。

### 核心差异化

- **微信/URL/文档** → **个人克隆声音** → **播客音频 + RSS分发**
- 极简工作流：粘贴链接 → 生成克隆声音播客 → 一键分发到Spotify/Apple Podcast/小宇宙

### 目标用户

- 海外内容创作者（YouTuber/Podcaster/LinkedIn Creator）
- 博客作者想把文章变成播客
- 想做个人品牌但没时间录音的专业人士
- 公众号创作者想把文字内容复用为音频

### 市场选择

- **主攻海外市场**（美国/欧洲为主）
- 避开豆包（字节）免费竞争
- 英文界面，英文产品

---

## 🎯 产品功能清单

### P0 - 核心闭环（必须做）

#### 1. 文章解析
- 输入：微信文章链接 / 任意URL / 纯文本 / PDF / Markdown
- 输出：提取正文内容
- 技术：网页抓取 + 正文提取算法

#### 2. 文本口语化
- 自动将书面语转为更适合听的语气
- 保留核心内容，适当添加过渡语
- 支持英文口语化

#### 3. 声音克隆
- 用户上传5分钟音频样本
- 克隆专属声音
- 支持选择预设声音（男声/女声/不同风格）
- 技术：集成 ElevenLabs API

#### 4. 播客生成
- 文字 → 克隆声音TTS
- 添加背景音乐（可选，多种风格）
- 导出MP3格式
- 生成播客封面图（AI自动生成）

#### 5. 注册登录
- 邮箱注册 + 密码登录
- Google账号登录（可选）
- 忘记密码 + 重置密码
- 管理员账号：admin@126.com / admin123

### P1 - 运营功能

#### 6. 播客管理
- 历史播客列表
- 播放预览
- 下载MP3
- 删除/重新生成

#### 7. 声音管理
- 我的克隆声音
- 上传/重新训练声音
- 预览声音效果

#### 8. RSS订阅
- 生成专属RSS地址
- 支持Spotify/Apple Podcast/小宇宙订阅
- 一键复制订阅链接

### P2 - 增长功能（可选）

#### 9. 多语言翻译
- 中文文章 → 英文播客
- 英文文章 → 中文播客
- 技术：DeepL API

#### 10. 播客分发
- 一键发布到喜马拉雅
- 一键发布到小宇宙
- 一键发布到Spotify

---

## 🎨 界面设计风格

### 整体风格
- **现代极简主义 + 科技感**
- 深色主题为主（类似Notion/Linear风格）
- 大量留白，视觉呼吸感强

### 配色方案

```
主色（Primary）：#6366F1（靛蓝色，代表科技+创造力）
次色（Secondary）：#8B5CF6（紫色，AI/未来感）
强调色（Accent）：#22D3EE（青色，亮点提示）
背景色（Background）：#0F0F14（深黑灰）
卡片背景：#1A1A24（深灰）
文字主色：#FFFFFF（白色）
文字次色：#94A3B8（灰蓝色）
边框色：#2D2D3A（暗灰）
成功色：#10B981（绿色）
警告色：#F59E0B（橙色）
错误色：#EF4444（红色）
```

### 字体规范

```css
/* 英文字体 */
font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;

/* 代码字体 */
font-family: 'JetBrains Mono', 'Fira Code', monospace;

/* 字号 */
h1: 32px / 700
h2: 24px / 600
h3: 20px / 600
body: 16px / 400
small: 14px / 400
caption: 12px / 400
```

### 圆角与间距

```css
/* 圆角 */
border-radius-sm: 8px
border-radius-md: 12px
border-radius-lg: 16px
border-radius-xl: 24px

/* 间距 */
space-xs: 4px
space-sm: 8px
space-md: 16px
space-lg: 24px
space-xl: 32px
space-2xl: 48px
space-3xl: 64px
```

### 按钮样式

```css
/* 主要按钮 */
background: #6366F1
color: white
padding: 12px 24px
border-radius: 8px
font-weight: 600
transition: all 0.2s

/* 次要按钮 */
background: transparent
border: 1px solid #2D2D3A
color: #94A3B8
padding: 12px 24px
border-radius: 8px

/* 幽灵按钮 */
background: transparent
color: #6366F1
padding: 12px 24px
```

---

## 📱 响应式设计

### PC端（桌面）
- 最大宽度：1200px，居中显示
- 侧边栏导航（可折叠）
- 三栏布局：侧边栏 + 主内容 + 详情面板

### 平板端（Tablet）
- 断点：768px - 1024px
- 侧边栏收起为图标模式
- 两栏布局

### 移动端（Mobile）
- 断点：< 768px
- 底部导航栏
- 单栏布局
- 全屏模态框

---

## 📄 页面结构

### 1. Landing Page（首页）

```
┌─────────────────────────────────────────────┐
│  LOGO        Features  Pricing  Login      │  ← 导航栏
├─────────────────────────────────────────────┤
│                                             │
│        Turn Your Words Into                 │
│        Your Voice Podcast                   │  ← Hero标题
│                                             │
│   Paste a link. Clone your voice.          │
│   Launch your podcast in minutes.          │  ← 副标题
│                                             │
│        [ Get Started Free ]                 │  ← CTA按钮
│                                             │
│   ┌───────────────────────────────────┐     │
│   │  🔗 Paste article URL here...    │     │  ← 输入框
│   └───────────────────────────────────┘     │
│                                             │
├─────────────────────────────────────────────┤
│                                             │
│   How It Works                              │
│   ┌─────┐  ┌─────┐  ┌─────┐               │
│   │  1  │→ │  2  │→ │  3  │               │
│   │ Paste│  │Clone│  │Export│              │
│   │ Link │  │Voice│  │Podcast│             │
│   └─────┘  └─────┘  └─────┘               │
│                                             │
├─────────────────────────────────────────────┤
│                                             │
│   Features                                   │
│   ┌─────────────────────────────────────┐  │
│   │ 🎙️ Voice Cloning                    │  │
│   │ Your voice. Your brand.             │  │
│   └─────────────────────────────────────┘  │
│   ┌─────────────────────────────────────┐  │
│   │ 🔗 URL Parsing                      │  │
│   │ Paste any link. We handle the rest. │  │
│   └─────────────────────────────────────┘  │
│   ┌─────────────────────────────────────┐  │
│   │ 📡 RSS Distribution                 │  │
│   │ One click to Spotify & Apple.      │  │
│   └─────────────────────────────────────┘  │
│                                             │
├─────────────────────────────────────────────┤
│                                             │
│   Pricing                                    │
│   ┌────────┐ ┌────────┐ ┌────────┐        │
│   │  Free  │ │ Creator │ │  Pro   │        │
│   │  $0    │ │  $9/mo  │ │ $29/mo │        │
│   └────────┘ └────────┘ └────────┘        │
│                                             │
├─────────────────────────────────────────────┤
│   © 2026 VoiceBlog. All rights reserved.   │
└─────────────────────────────────────────────┘
```

### 2. Dashboard（控制台）

```
┌─────────────────────────────────────────────┐
│ ☰  VoiceBlog                    [+] New   👤 │
├─────────┬───────────────────────────────────┤
│          │                                   │
│ 📊 Home │   Welcome back, [Name]            │
│          │                                   │
│ 🎙️ My   │   Recent Podcasts                 │
│ Podcasts │   ┌──────────────────────────┐   │
│          │   │ 🎵 Podcast #1  - 5:32     │   │
│ 🎤 My    │   │ Today, 10:30 AM          │   │
│ Voices   │   │ ▶️  ▶️ Download  🗑️      │   │
│          │   └──────────────────────────┘   │
│ ⚙️       │   ┌──────────────────────────┐   │
│ Settings │   │ 🎵 Podcast #2  - 8:15     │   │
│          │   │ Yesterday, 3:45 PM        │   │
│          │   │ ▶️  ▶️ Download  🗑️      │   │
│          │   └──────────────────────────┘   │
│          │                                   │
│          │   [ Create New Podcast → ]        │
└─────────┴───────────────────────────────────┘
```

### 3. Create Podcast（创建播客）

```
┌─────────────────────────────────────────────┐
│ ← Back         Create New Podcast           │
├─────────────────────────────────────────────┤
│                                             │
│  Step 1: Add Content                        │
│  ┌───────────────────────────────────────┐  │
│  │  🔗 Paste URL or type text...        │  │
│  │                                       │  │
│  │  Or upload: [PDF] [Markdown]         │  │
│  └───────────────────────────────────────┘  │
│                                             │
│  Step 2: Choose Voice                      │
│  ┌───────────────────────────────────────┐  │
│  │  ○ My Cloned Voice (Sarah)  🎤        │  │
│  │  ○ Preset: Professional Male  🧑       │  │
│  │  ○ Preset: Friendly Female  👩        │  │
│  │                                       │  │
│  │  [Train New Voice →]                  │  │
│  └───────────────────────────────────────┘  │
│                                             │
│  Step 3: Customize                         │
│  ┌───────────────────────────────────────┐  │
│  │  Background Music: [None ▼]           │  │
│  │  Speed: [1.0x ▼]                      │  │
│  │  Include Timestamps: [✓]              │  │
│  └───────────────────────────────────────┘  │
│                                             │
│        [ Generate Podcast ]                 │
│                                             │
└─────────────────────────────────────────────┘
```

### 4. Voice Cloning（声音克隆）

```
┌─────────────────────────────────────────────┐
│ ← Back         My Voices                   │
├─────────────────────────────────────────────┤
│                                             │
│  Your Cloned Voices                         │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │ 🎤 My Voice (Sarah)                 │    │
│  │    Cloned: 2024-03-15               │    │
│  │    Quality: Excellent                │    │
│  │    [▶ Preview] [✏️ Retrain] [🗑️]   │    │
│  └─────────────────────────────────────┘    │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │ 🎤 Clone New Voice                   │    │
│  │                                     │    │
│  │  1. Record or upload 5 min audio    │    │
│  │  2. Name your voice                 │    │
│  │  3. Wait for training (~10 min)     │    │
│  │                                     │    │
│  │  [Start Cloning →]                   │    │
│  └─────────────────────────────────────┘    │
│                                             │
│  Tip: For best results, record in a         │
│  quiet environment with clear speech.       │
│                                             │
└─────────────────────────────────────────────┘
```

### 5. 注册/登录页面

```
┌─────────────────────────────────────────────┐
│                                             │
│              VoiceBlog                      │
│                                             │
│   ┌─────────────────────────────────────┐   │
│   │  Email                              │   │
│   │  ┌─────────────────────────────┐   │   │
│   │  │ your@email.com               │   │   │
│   │  └─────────────────────────────┘   │   │
│   │                                     │   │
│   │  Password                           │   │
│   │  ┌─────────────────────────────┐   │   │
│   │  │ •••••••••••                  │   │   │
│   │  └─────────────────────────────┘   │   │
│   │                                     │   │
│   │  [        Sign In        ]         │   │
│   │                                     │   │
│   │  ─────── or ───────                │   │
│   │                                     │   │
│   │  [  Continue with Google  ]        │   │
│   │                                     │   │
│   │  Don't have an account? Sign up    │   │
│   └─────────────────────────────────────┘   │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 🔐 权限系统

### 用户角色

| 角色 | 权限 |
|------|------|
| **Admin** | 所有功能 + 用户管理 + 数据查看 |
| **User** | 正常播客创建和管理 |
| **Guest** | 只读功能，需要登录 |

### 管理员账号
- 邮箱：admin@126.com
- 密码：admin123

---

## 🛠 技术栈建议

### 前端
```
框架: Next.js 14 (App Router)
UI: TailwindCSS + shadcn/ui
状态管理: Zustand
表单: React Hook Form + Zod
动画: Framer Motion
图标: Lucide React
```

### 后端
```
框架: Next.js API Routes
数据库: Supabase (PostgreSQL)
认证: Supabase Auth
存储: Cloudflare R2 (音频文件)
实时: Supabase Realtime
```

### AI服务
```
TTS + 声音克隆: ElevenLabs API
文本口语化: Claude API (Anthropic)
网页解析: Firecrawl / Jina AI Reader
翻译: DeepL API
```

### 部署
```
主机: Vercel
CDN: Cloudflare
数据库: Supabase
对象存储: Cloudflare R2
```

---

## 📦 数据库设计

### users（用户表）
```sql
id: UUID PRIMARY KEY
email: VARCHAR UNIQUE NOT NULL
password_hash: VARCHAR
name: VARCHAR
avatar_url: VARCHAR
subscription_tier: ENUM('free', 'creator', 'pro', 'agency')
subscription_expires_at: TIMESTAMP
created_at: TIMESTAMP
updated_at: TIMESTAMP
```

### podcasts（播客表）
```sql
id: UUID PRIMARY KEY
user_id: UUID REFERENCES users
title: VARCHAR
source_url: VARCHAR
source_type: ENUM('url', 'text', 'pdf', 'markdown')
content: TEXT
audio_url: VARCHAR
duration_seconds: INTEGER
voice_id: VARCHAR
background_music: VARCHAR
cover_image_url: VARCHAR
rss_feed_id: VARCHAR
status: ENUM('processing', 'completed', 'failed')
created_at: TIMESTAMP
```

### voices（声音表）
```sql
id: UUID PRIMARY KEY
user_id: UUID REFERENCES users
name: VARCHAR
elevenlabs_voice_id: VARCHAR
audio_sample_url: VARCHAR
quality: ENUM('training', 'excellent', 'good', 'poor')
status: ENUM('training', 'ready', 'failed')
trained_at: TIMESTAMP
created_at: TIMESTAMP
```

### subscriptions（订阅表）
```sql
id: UUID PRIMARY KEY
user_id: UUID REFERENCES users
tier: ENUM('free', 'creator', 'pro', 'agency')
status: ENUM('active', 'cancelled', 'past_due')
current_period_start: TIMESTAMP
current_period_end: TIMESTAMP
stripe_subscription_id: VARCHAR
stripe_customer_id: VARCHAR
```

---

## ⚠️ 开发注意事项

### 1. API密钥管理
- 所有API密钥存放在环境变量
- 禁止硬编码在代码中
- 使用 .env.local 文件

### 2. 音频处理
- 音频文件存储在Cloudflare R2
- 生成时显示进度条
- 支持后台处理

### 3. 错误处理
- 所有API调用加 try-catch
- 显示友好的错误提示
- 记录错误日志

### 4. 移动端适配
- 按钮足够大（至少44px）
- 输入框适配键盘
- 支持横屏模式

### 5. 性能优化
- 图片懒加载
- 音频流式传输
- 页面SSR/SSG混合

---

## 📋 MVP交付清单

### 必须交付
- [ ] Landing Page（首页）
- [ ] 用户注册/登录
- [ ] 管理员后台（admin@126.com / admin123）
- [ ] 文章URL解析
- [ ] 文本口语化
- [ ] ElevenLabs声音克隆
- [ ] 播客生成 + MP3下载
- [ ] 播客列表管理

### 可选交付
- [ ] RSS订阅生成
- [ ] 背景音乐
- [ ] 多语言翻译
- [ ] 播客分发

---

## 🚀 快速启动命令

```bash
# 1. 克隆项目
git clone [repo-url]
cd voiceblog

# 2. 安装依赖
npm install

# 3. 复制环境变量
cp .env.example .env.local

# 4. 配置环境变量
# ELEVENLABS_API_KEY=your_key
# ANTHROPIC_API_KEY=your_key
# SUPABASE_URL=your_url
# SUPABASE_ANON_KEY=your_key

# 5. 启动开发服务器
npm run dev

# 6. 打开 http://localhost:3000
```
