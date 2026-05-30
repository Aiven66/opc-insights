# ClearReel — AI视频去水印工具
## PRD v1.0 | 编程提示词（AI Coding Prompt）

> **产品代号**: ClearReel
> **版本**: v1.0
> **日期**: 2026-05-20
> **产品经理**: 小北Aiven
> **状态**: ✅ 待开发

---

# 角色设定

你是一位经验丰富的全栈工程师，擅长 Next.js 14 + TypeScript + TailwindCSS 开发。你需要根据下面的需求文档，从零开始构建一个完整的 AI 视频去水印工具 ClearReel。

**项目要求**：
- 输出完整、可运行的代码（不写占位符）
- 代码风格：清晰注释 + 模块化拆分
- 移动端优先（响应式设计）
- 真实 API 集成（不走假数据）

---

# 一、产品概述

## 1.1 产品定位

**ClearReel** 是一个极简的 AI 视频去水印在线工具。

- **Slogan**: "Remove watermarks from any video — free & instant"
- **中文含义**: 干净的视频胶片
- **一句话定位**: 专注做 AI 视频去水印的单功能工具
- **目标市场**: 海外用户（ProductHunt 首发）
- **目标用户**: 视频剪辑师、自媒体创作者、商务演示制作者

## 1.2 核心差异

| 竞品问题 | ClearReel 解法 |
|---------|--------------|
| 都要登录/注册 | ✅ 免登录，直接用 |
| 功能太多太重 | ✅ 只做一个功能：去水印 |
| 要付费才能用 | ✅ Freemium：每天免费3次 |
| 效果一般 | ✅ AI 帧间一致性填充 |

## 1.3 关键约束

```
⚠️ 免登录：用户无需注册即可使用，这是核心差异点
⚠️ 视频不上传到服务器：在浏览器本地处理（FFmpeg.wasm）
⚠️ AI 处理在云端：调用 Replicate API 进行 inpainting
⚠️ 隐私优先：视频处理完成后即删除，不持久化存储
```

---

# 二、账号体系

> **注**：ClearReel 是免登录产品，普通用户不需要账号。
> 管理员账号仅用于后台管理（查看使用统计等）。

| 项目 | 内容 |
|------|------|
| **管理员账号** | admin@126.com |
| **管理员密码** | admin666 |
| **普通用户** | 无需登录，直接使用 |
| **登录页面** | `/admin/login`（管理员专用）|

---

# 三、界面设计规范

## 3.1 设计风格：极简专业风

**参考**: Kapwing / Veed.io 的简洁风格，但更聚焦、更轻量

**设计语言**:
- 大面积留白，减少视觉噪音
- 操作流程极简：上传 → 涂抹 → 处理 → 下载
- 以操作为中心，不需要多余导航

## 3.2 配色方案

### 浅色模式（默认，深色模式同步支持）

| 用途 | 色值 | 说明 |
|------|------|------|
| 主色 Primary | #6366F1 | 靛蓝紫，信任感 + AI 感 |
| 辅助色 Secondary | #8B5CF6 | 紫色渐变搭配 |
| 强调色 Accent | #F97316 | 橙色，处理/下载按钮 |
| 背景色 Background | #FAFBFC | 极浅灰白 |
| 卡片背景 | #FFFFFF | 白色卡片 |
| 边框色 | #E5E7EB | 浅灰边框 |
| 文字主色 | #111827 | 深黑文字 |
| 文字次色 | #6B7280 | 灰色次要文字 |
| 成功色 | #10B981 | 绿色 |
| 警告色 | #F59E0B | 橙色 |
| 错误色 | #EF4444 | 红色 |
| 进度条色 | #6366F1 | 靛蓝紫 |

### 深色模式（Dark Mode）

| 用途 | 色值 | 说明 |
|------|------|------|
| 主色 Primary | #818CF8 | 浅靛蓝紫 |
| 强调色 Accent | #FB923C | 亮橙色 |
| 背景色 Background | #0F172A | 深黑 |
| 卡片背景 | #1E293B | 深灰卡片 |
| 文字主色 | #F9FAFB | 白色文字 |
| 文字次色 | #94A3AF | 灰色 |

## 3.3 字体规范

| 用途 | 字体 | 大小 | 字重 |
|------|------|------|------|
| Logo/品牌 | Inter | 20px | 700 |
| H1 主标题 | Inter | 32px | 700 |
| H2 区块标题 | Inter | 20px | 600 |
| H3 卡片标题 | Inter | 16px | 600 |
| Body 正文 | Inter | 15px | 400 |
| 辅助文字 | Inter | 13px | 400 |
| 按钮文字 | Inter | 15px | 500 |

## 3.4 圆角与间距

| 项目 | 规范 |
|------|------|
| 页面最大宽度 | 1200px（居中）|
| 页面内边距 | 24px（桌面）/ 16px（移动）|
| 卡片圆角 | 16px |
| 按钮圆角 | 12px |
| 输入框圆角 | 10px |
| 上传区圆角 | 20px |
| 元素间距 | 8px |

## 3.5 核心 UI 组件

### 顶部导航栏

```
┌─────────────────────────────────────────────────────────────┐
│  🎬 ClearReel          [🌙/☀️]  [English ▾]   [Admin]      │
└─────────────────────────────────────────────────────────────┘
```

### 首页（主操作区）

```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│              🎬 Remove Watermarks from Any Video              │
│          Free, instant, and no login required.               │
│                                                              │
│   ┌─────────────────────────────────────────────────────┐   │
│   │                                                      │   │
│   │          📁 Drag & drop your video here             │   │
│   │                                                      │   │
│   │               or click to browse                     │   │
│   │                                                      │   │
│   │         Supports MP4, MOV, WebM • Max 500MB          │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                              │
│   Supported formats: MP4 MOV WebM  •  Max file size: 500MB   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 编辑器界面（核心工作区）

```
┌─────────────────────────────────────────────────────────────┐
│  ← Back to Home                          [🌙] [EN]           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   [▶ 原视频] [处理后 ▶]      ▼ Brush: ●○○  size: 40px     │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                                                      │   │
│  │         📺 视频预览区（双滑块对比播放）              │   │
│  │                                                      │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│   [撤销 ↶] [重做 ↷] [清除涂抹]              [处理视频 ▶]    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 处理进度界面

```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│              AI is removing watermarks...                    │
│                                                              │
│   ┌─────────────────────────────────────────────────────┐   │
│   │  ████████████░░░░░░░░░░░░░░░░░░░░░  58%           │   │
│   │                                                      │   │
│   │  Step: Inpainting frame 234 / 400                  │   │
│   │  Estimated time: ~45 seconds remaining              │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 下载界面

```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│   ✨ Your video is ready!                                   │
│                                                              │
│   ┌──────────────────────────────────────────────────────┐   │
│   │                                                      │   │
│   │         📺 视频预览（无水印）                        │   │
│   │                                                      │   │
│   └──────────────────────────────────────────────────────┘   │
│                                                              │
│   [↩ 处理另一个]                        [⬇ Download MP4]   │
│                                                              │
│   ⚠️  Free version: downloaded video has a small           │
│       ClearReel watermark. Upgrade to Pro for clean export.  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 3.6 多语言支持

| 语言 | 代码 | 说明 |
|------|------|------|
| **English** | en-US | 默认语言 |
| **中文** | zh-CN | 中文用户 |

语言切换：导航栏语言选择器，点击切换，记住选择（localStorage）。

## 3.7 移动端适配

- **响应式断点**：mobile < 768px，tablet 768-1024px，desktop > 1024px
- **移动端布局**：
  - 上传区占满屏幕宽度
  - 编辑器单列布局
  - 底部固定下载按钮
- **触摸优化**：画笔工具支持双指缩放

---

# 四、功能模块

## 4.1 首页（Home）

**路径**: `/` 或 `/`

**功能**:
- 品牌展示 + Slogan
- 视频上传区（拖拽 + 点击）
- 格式/大小说明
- 底部 Footer（隐私政策 / 服务条款 / 联系方式）

**状态**:
| 状态 | 说明 |
|------|------|
| 空状态 | 显示上传引导 |
| 拖拽悬停 | 边框高亮 + 背景变化 |
| 上传中 | 进度条 + 取消按钮 |
| 上传完成 | 自动跳转到编辑器 |

## 4.2 编辑器（Editor）

**路径**: `/editor`

**功能**:
1. **视频预览**：双滑块对比（处理前 / 处理后）
2. **画笔工具**：涂抹水印区域
   - 画笔大小：10px / 20px / 40px / 80px
   - 颜色：半透明白色（显示涂抹区域）
   - 撤销 / 重做（最多50步）
   - 清除全部涂抹
3. **播放控制**：播放 / 暂停 / 进度条 / 全屏
4. **帧导航**：拖动时间轴精确定位水印帧
5. **处理按钮**：触发 AI 去水印

**操作流程**:
```
1. 播放视频 → 找到有水印的帧
2. 用画笔涂抹水印区域（可以涂抹多帧）
3. 点击"处理视频"
4. 等待 AI 处理（实时进度条）
5. 预览处理效果
6. 下载结果
```

## 4.3 处理进度页（Processing）

**路径**: `/processing`

**功能**:
- 实时进度条（百分比 + 步骤说明）
- 预计剩余时间
- 取消处理按钮
- 完成自动跳转下载页

**进度步骤说明**:
```
1. "Uploading frames..." (0-20%)
2. "AI analyzing watermark areas..." (20-40%)
3. "Removing watermarks frame by frame..." (40-90%)
4. "Generating clean video..." (90-100%)
```

## 4.4 下载页（Download）

**路径**: `/download`

**功能**:
- 处理后视频预览播放
- 下载按钮（MP4 格式）
- 分享功能（复制链接）
- 处理另一个视频（返回首页）
- Freemium 提示（免费版带水印）

## 4.5 管理后台（Admin）

**路径**: `/admin/login`（登录）| `/admin/dashboard`（看板）

**登录页设计**:
```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│                    🎬 ClearReel Admin                    │
│                                                          │
│         ┌─────────────────────────────────┐             │
│         │  📧 Email Address                 │             │
│         └─────────────────────────────────┘             │
│         ┌─────────────────────────────────┐             │
│         │  🔒 Password                     │             │
│         └─────────────────────────────────┘             │
│                                                          │
│              [      Sign In       ]                     │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

**管理后台功能**:
- **使用统计**：今日 / 本周 / 本月处理次数
- **API 调用统计**：已使用次数 / 配额
- **收入概览**：订阅用户数 + 收入
- **最近处理记录**：时间、用户、状态

## 4.6 多语言切换

**支持语言**：English（默认）、中文

**切换方式**：导航栏下拉选择，localStorage 持久化

---

# 五、技术架构

## 5.1 技术栈

| 层级 | 技术选型 | 说明 |
|------|---------|------|
| **前端框架** | Next.js 14 + TypeScript | App Router |
| **UI 组件库** | TailwindCSS + Radix UI | 无需 shadcn（轻量）|
| **视频前端处理** | FFmpeg.wasm | 浏览器内视频处理 |
| **AI 去水印** | Replicate API (LaMa/LaMa-Inpainting) | 云端 AI 处理 |
| **支付** | Stripe Checkout | 订阅制支付 |
| **数据库** | Supabase (PostgreSQL) | 使用统计 + 用户订阅 |
| **认证** | Supabase Auth | 仅管理员用 |
| **部署** | Vercel（前端）+ Railway（可选）|  |
| **域名** | clearreel.io / clearreel.ai | 待注册 |

## 5.2 数据库设计

### users 表（仅管理员，普通用户不注册）

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role VARCHAR(50) DEFAULT 'user',  -- 'admin' | 'user'
  stripe_customer_id VARCHAR(255),  -- Stripe 客户 ID
  plan VARCHAR(50) DEFAULT 'free',  -- 'free' | 'pro' | 'business'
  stripe_subscription_id VARCHAR(255),
  daily_free_uses INTEGER DEFAULT 0,
  last_free_reset_date DATE,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### usage_logs 表（使用记录）

```sql
CREATE TABLE usage_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  session_id VARCHAR(255),          -- 匿名会话 ID（Cookie）
  action VARCHAR(50),                -- 'upload' | 'process' | 'download'
  video_duration_seconds INTEGER,
  watermark_frames INTEGER,
  processing_time_ms INTEGER,
  status VARCHAR(50),                -- 'success' | 'failed' | 'cancelled'
  created_at TIMESTAMP DEFAULT NOW()
);
```

### pricing_plans 表（定价方案）

```sql
CREATE TABLE pricing_plans (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(50) NOT NULL,        -- 'free' | 'pro' | 'business'
  price_monthly INTEGER,             -- 美元（分），0 = 免费
  price_yearly INTEGER,
  max_daily_free INTEGER DEFAULT 3,
  max_video_minutes INTEGER,         -- 每次最大时长（分钟）
  has_watermark BOOLEAN DEFAULT true,
  max_quality VARCHAR(20),          -- '720p' | '1080p' | '4k'
  batch_size INTEGER DEFAULT 1,      -- 批量处理数量
  api_access BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT NOW()
);
```

## 5.3 API 接口设计

### 认证接口（仅管理员）

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/auth/admin/login` | POST | 管理员登录 |
| `/api/auth/admin/logout` | POST | 管理员退出 |
| `/api/auth/admin/me` | GET | 获取管理员信息 |

### 视频处理接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/process/upload` | POST | 上传视频片段（分片上传）|
| `/api/process/start` | POST | 开始 AI 处理（返回 job_id）|
| `/api/process/status/[jobId]` | GET | 查询处理状态 |
| `/api/process/result/[jobId]` | GET | 获取处理结果 |
| `/api/process/cancel/[jobId]` | POST | 取消处理 |

### Freemium 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/usage/check` | GET | 检查当日剩余免费次数 |
| `/api/usage/record` | POST | 记录一次使用（免费用户）|

### 订阅接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/subscription/checkout` | POST | 创建 Stripe Checkout Session |
| `/api/subscription/portal` | POST | 创建 Stripe Customer Portal |
| `/api/webhooks/stripe` | POST | Stripe Webhook 回调 |

### 管理后台接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/admin/stats` | GET | 统计数据（总使用量 / 收入等）|
| `/api/admin/usage-logs` | GET | 使用记录列表 |

---

# 六、定价方案

## 6.1 套餐设计

| 套餐 | 月付 | 年付（8折）| 每日免费次数 | 单次最大时长 | 输出质量 | 水印 | 批量 |
|------|------|-----------|------------|------------|---------|------|------|
| **Free** | $0 | $0 | 3次 | 1分钟 | 720p | 有 | ❌ |
| **Pro** | $15 | $144 | 无限 | 5分钟 | 1080p | 无 | ❌ |
| **Business** | $49 | $470 | 无限 | 30分钟 | 4K | 无 | 5个/批 |
| **Enterprise** | $199 | — | 无限 | 不限 | 4K | 无 | 不限 |

## 6.2 Freemium 逻辑

```
用户访问 → 检查 localStorage session_id
         → 检查今日免费次数（从 API 获取）
         → 未超限 → 允许处理
         → 已超限 → 弹出升级弹窗
```

---

# 七、MVP 开发里程碑（14天）

```
Day 1-2:   项目初始化 + 首页上传区 + FFmpeg.wasm 集成
Day 3-4:   编辑器界面 + 画笔涂抹工具 + 视频预览播放
Day 5-6:   Replicate API 集成 + 处理进度界面
Day 7-8:   下载页面 + Freemium 逻辑
Day 9-10:  Stripe 支付集成 + 订阅流程
Day 11:    管理后台登录 + 看板
Day 12:    移动端适配 + 多语言（EN/ZH）
Day 13:    深色模式 + 样式细节优化
Day 14:    服务条款 + 隐私政策 + Vercel 部署测试
```

---

# 八、代码规范

## 8.1 项目结构

```
clearreel/
├── app/
│   ├── page.tsx                    # 首页（上传区）
│   ├── editor/page.tsx            # 编辑器
│   ├── processing/page.tsx         # 处理进度
│   ├── download/page.tsx          # 下载页
│   ├── admin/
│   │   ├── login/page.tsx          # 管理员登录
│   │   └── dashboard/page.tsx     # 管理看板
│   └── api/
│       ├── process/
│       │   ├── start/route.ts
│       │   ├── status/[jobId]/route.ts
│       │   └── result/[jobId]/route.ts
│       ├── usage/
│       │   ├── check/route.ts
│       │   └── record/route.ts
│       ├── subscription/
│       │   ├── checkout/route.ts
│       │   └── portal/route.ts
│       └── webhooks/
│           └── stripe/route.ts
├── components/
│   ├── VideoUploader.tsx          # 拖拽上传组件
│   ├── VideoEditor.tsx            # 编辑器主组件
│   ├── BrushTool.tsx              # 画笔涂抹工具
│   ├── VideoPreview.tsx           # 视频预览（双滑块）
│   ├── ProcessingStatus.tsx       # 处理进度
│   ├── DownloadSection.tsx        # 下载区域
│   ├── PricingModal.tsx           # 升级弹窗
│   ├── ThemeToggle.tsx            # 深浅色切换
│   ├── LanguageSwitcher.tsx       # 语言切换
│   └── Navigation.tsx            # 顶部导航
├── lib/
│   ├── ffmpeg.ts                  # FFmpeg.wasm 封装
│   ├── replicate.ts               # Replicate API 调用
│   ├── stripe.ts                  # Stripe SDK 封装
│   ├── supabase.ts                # Supabase 客户端
│   └── utils.ts                   # 工具函数
├── hooks/
│   ├── useVideoEditor.ts          # 编辑器状态管理
│   ├── useProcessing.ts           # 处理状态管理
│   └── useLanguage.ts             # 语言切换
├── i18n/
│   ├── en.json                    # 英文文案
│   └── zh.json                   # 中文文案
├── public/
│   └── favicon.ico
├── styles/
│   └── globals.css                # Tailwind + 自定义
├── .env.local                    # 环境变量
├── tailwind.config.ts
├── next.config.ts
└── package.json
```

## 8.2 环境变量

```env
# Supabase
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=

# Replicate
REPLICATE_API_TOKEN=

# Stripe
STRIPE_SECRET_KEY=
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=
STRIPE_WEBHOOK_SECRET=
STRIPE_PRO_PRICE_ID=
STRIPE_BUSINESS_PRICE_ID=
STRIPE_ENTERPRISE_PRICE_ID=

# App
NEXT_PUBLIC_APP_URL=https://clearreel.io
```

## 8.3 关键实现要求

### 视频处理流程（核心）

```typescript
// 用户操作流程（必须实现）
async function handleVideoProcessing(video: File, mask: MaskData) {
  // 1. 用 FFmpeg.wasm 提取视频帧
  const frames = await extractFrames(video, mask.frameRange)

  // 2. 调用 Replicate API 逐帧去水印
  const processedFrames = []
  for (const frame of frames) {
    const result = await replicate.inpainting(frame, mask.coordinates)
    processedFrames.push(result)
    // 更新进度
    onProgress(processedFrames.length / frames.length)
  }

  // 3. 用 FFmpeg.wasm 合成视频
  const outputVideo = await compileVideo(processedFrames)

  // 4. 生成下载链接（本地 Blob URL）
  return URL.createObjectURL(outputVideo)
}
```

### Freemium 检查（必须实现）

```typescript
// 检查用户是否可以使用免费处理
async function checkFreeUsage(sessionId: string): Promise<{
  canUse: boolean
  remaining: number
  showUpgradeModal: boolean
}> {
  // 1. 查数据库当日使用次数
  const usage = await getDailyUsage(sessionId)

  if (usage.count < FREE_DAILY_LIMIT) {
    return { canUse: true, remaining: FREE_DAILY_LIMIT - usage.count, showUpgradeModal: false }
  } else {
    return { canUse: false, remaining: 0, showUpgradeModal: true }
  }
}
```

---

# 九、合规要求

## 9.1 服务条款（必须页面）

路径：`/terms`

内容：
- 明确禁止使用 ClearReel 去除盗版/非法内容的水印
- 视频仅在处理期间临时存储，处理完成后即删除
- 用户需确保拥有视频的使用权

## 9.2 隐私政策（必须页面）

路径：`/privacy`

内容：
- 不收集用户个人信息（除订阅用户）
- 视频不上传到永久服务器
- GDPR 合规

## 9.3 免责声明

每个处理后的视频底部添加：
- Free 版：视频右下角有 ClearReel 小水印（20px，白色半透明）
- Pro+ 版：完全无水印

---

# 十、输出要求

## 10.1 代码输出

- 每个文件独立输出完整代码
- 不写 TODO / placeholder
- 包含中文注释（方便理解）
- TypeScript 类型完整

## 10.2 输出顺序

```
第一步：项目初始化（package.json + next.config.ts + tailwind.config.ts）
第二步：全局样式（globals.css）
第三步：工具函数（lib/）
第四步：组件（components/）
第五步：页面（app/）
第六步：API Routes（app/api/）
第七步：环境变量说明（.env.example）
```

## 10.3 文件路径

所有文件输出到：`~/clearreel/` 目录下

---

*ClearReel PRD v1.0 | 生成于 2026-05-20*
