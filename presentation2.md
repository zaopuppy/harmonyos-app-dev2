# HarmonyOS 应用开发技能

> 让大模型真正理解鸿蒙生态

**主题风格:** Neon Cyber（深海军蓝 + 青色/品红霓虹色）
**文件结构:** 单一 HTML 文件 + 本地字体文件夹

---

## 幻灯片大纲（共 12 页）

### Slide 01: 封面
- 标题：HarmonyOS 应用开发技能
- 副标题：让大模型真正理解鸿蒙生态
- 标签：ArkTS | ArkUI | SDK | HDC
- HarmonyOS 图标（SVG）

---

### Slide 02: 背景 — 大模型对鸿蒙支持有限

**现状分析（两栏卡片）：**
- API 变更剧烈：HarmonyOS SDK API 处于快速迭代期，版本间差异显著
- 代码质量堪忧：类型错误、成员名错误、模块路径错误频发

**问题截图（双栏，悬停放大）：**
- bad-api.png — API 幻觉：`Property 'captureSnapshot' does not exist`
- bad-import.png — Import 错误：`Module path incorrect`

---

### Slide 03: 分类分析 — New in HarmonyOS App Development

**核心问题：** 对一个经验丰富的前端工程师而言，哪些知识是新的？

**五大知识域（卡片概览）：**
| 领域 | 特点 | 策略 |
|------|------|------|
| 工程模板 | IDE 自带，变化剧烈 | ✗ 不解决 |
| ArkTS 语法 | 类型系统差异 | ✓ 编译告警修复 |
| ArkUI 组件 | DSL 语法 | ✓ 编译告警修复 |
| 特有 API | 幻觉重灾区 | ✓ SDK 索引查询 |
| HDC 工具 | 设备调试 | ✓ 命令速查表 |
| 图生码 | 高保真生成 | ✓ 多模态 + 规则映射 |

---

### Slide 04: 工程模板

- 特点：IDE 自带功能，变化剧烈，小众场景，性价比低
- 解决方案：通过 IDE 自动创建或参考其他模块文件结构
- **策略：不解决**

---

### Slide 05: ArkTS 语法差异

**三大差异点：**
1. 严格类型 — 禁用 `any`，禁止动态类型
2. 不可变更新 — 状态修改必须创建新对象
3. 完整标注 — 显式声明所有类型

**代码示例（左右对比）：**

| ✗ ArkTS 不允许 | ✓ 正确写法 |
|----------------|-----------|
| `let data: any;` | `let data: string = 'hello';` |
| `let value: unknown; (value as string).length;` | `if (value instanceof string) { value.length; }` |
| `let obj = {}; obj['key'] = value;` | `let obj: Record<string, number> = {};` |
| `type T = typeof someVar;` | `class B extends A {}` |

**策略：** 提供少样本示例，主要通过编译错误指导解决

---

### Slide 06: ArkUI 组件语法

**说明：** ArkUI 组件语法是一套 DSL，和 ArkTS 完全是两套语法

**代码示例：**
```typescript
@Component
struct AnimatedButton {
  @State scale: number = 1;
  @State opacity: number = 1;

  build() {
    Button('Animated')
      .scale({ x: this.scale, y: this.scale })
      .opacity(this.opacity)
      .animation({ duration: 300, curve: Curve.EaseInOut })
      .onTouch((event: TouchEvent) => {
        if (event.type === TouchType.Down) {
          this.scale = 0.95;
          this.opacity = 0.8;
        } else if (event.type === TouchType.Up) {
          this.scale = 1;
          this.opacity = 1;
        }
      })
  }
}
```

**策略：** 提供少样本示例，主要通过编译错误指导解决

---

### Slide 07: 鸿蒙特有 API

**问题声明：**
- 幻觉重灾区 badge
- 数据：400+ 模块 · 3000+ 类 · 数万+ 成员方法
- 说明：大模型难以准确记忆，代码生成幻觉难以杜绝

**代码对比（左右栏）：**

✗ 幻觉（错误）：
```typescript
Text('截图')
  .fontSize(16)
  .width('100%')
  .padding(12)
  .onClick(() => {
    this.controller.captureSnapshot((err, pixelMap) => {
      if (!err) {
        console.info('Screenshot captured');
      }
    });
  })
// ✗ captureSnapshot 不存在
```

✓ 正确：
```typescript
Text('截图')
  .fontSize(16)
  .width('100%')
  .padding(12)
  .onClick(() => {
    this.controller.webPageSnapshot({ id: 'screenshot' }, (err: Error, result: web_webview.SnapshotResult) => {
      if (!err) {
        console.info('Screenshot captured');
      }
    });
  })
// ✓ 正确方法：webPageSnapshot
```

---

### Slide 08: SDK 索引方案

**说明：** 轻量 SDK 索引（索引耗时 <1s），提供 API 的实时查询

**工作原理：**
1. 扫描 SDK 的 .d.ts 类型定义文件
2. 解析模块路径、类成员、方法签名
3. 构建可查询的索引数据库
4. 提供命令行查询接口

**索引范围：**
- `@ohos.*` — 系统 API
- `@kit.*` — ArkUI 套件
- `@system.*` — 系统能力
- `@hms.*` — HMS 套件

**查询示例：**
```bash
$ python check_sdk_imports.py --query "WebviewController"
[✓] @ohos.web.webview.webview.WebviewController
[✓] @kit.ArkWeb.webview.WebviewController
```

**策略：** 轻量 SDK 索引 + 实时 API 查询 + 智能纠错推荐

---

### Slide 09: 查询效果演示

**左栏 — 查询类的所有成员：**
```bash
$ python check_sdk_imports.py --query "@ohos.web.webview.webview.WebviewController"
[✓] WebviewController [ets/api/@ohos.web.webview.d.ts:3579]
  → constructor
  → initializeWebEngine
  → setActiveWebEngineVersion
  → getActiveWebEngineVersion
  → setHttpDns
  → setWebDebuggingAccess
  → forward
  → backward
  → clearHistory
  → ...
```

**右栏 — 智能纠错推荐：**
```bash
$ python check_sdk_imports.py --query "WebviewController#captureSnapshot"
[✗] WebviewController#captureSnapshot
    member 'captureSnapshot' not found
Did you mean:
  → webPageSnapshot
  → snapshot
  → getBitmap
```

**说明：** Levenshtein 编辑距离 + 前缀匹配 + 语义上下文，综合相关度排序推荐

---

### Slide 10: HDC 开发者工具

**说明：** 轻量自动化验证的基石。辅助自动化验证（编译后安装，分析 crash 等）

**常用命令：**
| 命令 | 说明 |
|------|------|
| `hdc shell` | 进入设备 shell |
| `hdc install app.hap` | 安装应用包 |
| `hdc file send local remote` | 推送文件到设备 |
| `hdc shell bm dump -a` | 查看已安装应用 |
| `hdc shell pidof com.example` | 获取进程 PID |
| `hdc shell hilog -r` | 查看实时日志 |

**策略：** 提供常用命令，作为知识库的补充

---

### Slide 11: 图生码 (高保真生成)

**说明：** 传统交付是高保真 + 详细标注，文本模型无法直接处理

**核心流程：** UI 截图 → 结构化描述 → 代码生成

**两种方案对比：**

| 方案 | 描述 | 优缺点 |
|------|------|--------|
| 方案一 | 多模态预处理 | ✓ 门槛低，✗ 精度差 |
| 方案二 | 规则映射转换 | ✓ 精度高，✗ 流程复杂 |

**方案一详解：**
- 多模态模型做预处理
- 转为描述数据后大模型生成
- 优点：门槛低
- 缺点：精确度差

**方案二详解：**
- 通过原始高保真交付件的结构化数据
- 经过规则映射转换后结合代码生成
- 优点：精度高
- 缺点：流程复杂，高保真的前期调整需要花不少时间

**策略：** 多模态预处理（门槛低）或规则映射（精度高），结合场景选择

---

### Slide 12: 总结 — HarmonyOS 技能体系

| 领域 | 策略 | 状态 |
|------|------|------|
| 🏗️ 工程模板 | IDE 自动处理 | ✓ |
| 📝 ArkTS 语法 | 编译告警驱动 | ✓ |
| 🎨 ArkUI 组件 | 编译告警驱动 | ✓ |
| 🔍 特有 API | SDK 索引查询 | ✓ |
| 🔧 HDC 工具 | 命令速查 | ✓ |
| 🎯 图生码 | 多模态/规则映射 | ✓ |
| 🤖 目标 | 大模型自动修复 | — |

**愿景：** 让大模型真正理解鸿蒙生态

---

## 技术信息

**字体：**
- Display: Clash Display（本地 woff2）
- Body: Satoshi（本地 woff2）

**导航方式：**
- 方向键 / 空格键
- 滚轮 / 触摸滑动
- 右侧导航点

**图片：**
- bad-api.png（需放置在 HTML 同级目录）
- bad-import.png（需放置在 HTML 同级目录）

**依赖：** 无外部依赖，完全离线可用
