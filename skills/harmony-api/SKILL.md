---
name: harmony-api
description: HarmonyOS SDK 导入检查、API 查询与编译错误定位。适用场景：1）鸿蒙/ArkTS 代码生成后检查 import 语句是否正确；2）鸿蒙应用编译报错修复，尤其是 `Property 'X' does not exist on type 'Y'`、成员名写错、API 不存在、想确认 `@ohos` / `@kit` 模块的正确类型路径、成员列表或函数签名时。触发关键词：import 检查、修复编译错误、ArkTS Compiler Error、Property does not exist on type、API not found、@ohos 模块、@kit member、does this API exist、check imports、验证 API。
---

# HarmonyOS SDK Import & API Checker

检查 OpenHarmony/ArkTS 项目中的 `import` 语句和 API 成员调用是否存在于 SDK 中，并提供智能推荐。

## 前提：确定 DEVECO_SDK_HOME

`DEVECO_SDK_HOME` 指向 SDK 的**根目录**（包含 `default/` 子目录的那一层），典型值：
- Windows: `C:\Program Files\Huawei\DevEco Studio\sdk`

脚本按以下顺序定位 SDK（与 `find_sdk_home` 函数逻辑一致）：

**1. 优先读取环境变量 `DEVECO_SDK_HOME`**

```powershell
# 验证当前会话中是否已设置
echo $env:DEVECO_SDK_HOME
```

若未设置，请在系统环境变量中配置。

**2. 若未设置环境变量，从 `hdc` 路径自动推导**

`hdc` 位于 `$DEVECO_SDK_HOME/default/openharmony/toolchains/hdc`。脚本在 PATH 中搜索 `hdc`，找到后剥离该后缀即可得到 `DEVECO_SDK_HOME`。DevEco Studio 安装后**不会**自动将 `hdc` 加入 PATH，需要用户手动添加。

**3. 均未找到时报错退出**

```
Error: DEVECO_SDK_HOME not set and hdc not found in PATH
```

此时请设置 `DEVECO_SDK_HOME` 环境变量，或将 `hdc` 所在目录加入 PATH，也可用 `--sdk-home` 参数临时指定。

## 工作原理

### 1. SDK 索引构建

首次运行（或缓存失效时），脚本扫描以下 `.d.ts` 文件目录：
- `$DEVECO_SDK_HOME/default/openharmony/ets/api`
- `$DEVECO_SDK_HOME/default/openharmony/ets/arkts`
- `$DEVECO_SDK_HOME/default/openharmony/ets/component`
- `$DEVECO_SDK_HOME/default/openharmony/ets/kits`
- `$DEVECO_SDK_HOME/default/hms/etc/api`
- `$DEVECO_SDK_HOME/default/hms/etc/kits`

### 2. 源码解析

扫描 `.ts` / `.ets` 文件，提取所有 `import` 语句及其后续的成员访问：
```typescript
import Ability from '@ohos.app.ability.Ability';
Ability.onConfigurationUpdate(config);  // 检测到成员访问 Ability#onConfigurationUpdate
```

### 3. 验证查询

| 状态 | 含义 |
|------|------|
| `✓` | 模块/类/成员存在于 SDK |
| `✗ MODULE_NOT_FOUND` | 模块文件不存在 |
| `✗ CLASS_NOT_FOUND` | 类不在该模块中 |
| `✗ MEMBER_NOT_FOUND` | 方法/属性不存在于该类 |

## 使用方式

在 `skills/harmony-api/scripts/` 目录下执行：

```bash
# 检查项目（或单个文件）
python check_sdk_imports.py --path /your/project --verbose

# 检查单个源文件
python check_sdk_imports.py --path ./src/Entry.ets

# 临时指定 SDK 路径（不依赖环境变量）
python check_sdk_imports.py --path /your/project --sdk-home "C:\Program Files\Huawei\DevEco Studio\sdk"

# 强制重建索引
python check_sdk_imports.py --path /your/project --rebuild-index

# JSON 输出（便于 CI 集成）
python check_sdk_imports.py --path /your/project --json
```

## 查询模式

不扫描文件，直接查询 SDK 中的模块、类、成员或嵌套类：

```bash
# 查询模块 → 列出所有类
python check_sdk_imports.py --query "@ohos.web.webview"

# 列出嵌套类的所有成员
python check_sdk_imports.py --query "@ohos.web.webview.webview.WebviewController"

# 查询成员是否存在
python check_sdk_imports.py --query "@ohos.web.webview.webview.WebviewController#refresh"

# 搜索成员名称（模糊查询）
python check_sdk_imports.py --query "WebviewController"
```

**查询格式：**
- `@ohos.XXX` — 列出该模块下所有类
- `@ohos.XXX.ClassName` — 列出该类所有成员
- `@ohos.XXX.Namespace.ClassName` — 列出嵌套类（如 namespace 中的类）的成员
- `@ohos.XXX#member` — 查询特定成员是否存在
- 任意关键词 — 搜索模块名或成员名

**重要约定：**
- `#` 只用于**成员存在性查询**，不是用来查询类本身。
- 查询嵌套类本身时，使用点号路径：`@ohos.XXX.Namespace.ClassName`
- 如果搜索结果同时出现：
  - `@ohos.web.webview.webview.WebviewController`
  - `@ohos.web.webview.webview#WebviewController`
  
  前者是**嵌套类的规范路径**，后者是“`WebviewController` 是 namespace `webview` 的一个成员”的表示。要继续查成员列表或函数签名时，优先使用前者。

## 编译报错处理流程

遇到这类错误时，不要直接猜 API 名称，按下面顺序排查：

```text
4 ERROR: 10505001 ArkTS Compiler Error
Error Message: Property 'captureSnapshot' does not exist on type 'WebviewController'.
At File: E:/workspace/arktsapi/entry/src/main/ets/pages/Index.ets:123:31
```

### 1. 先查类型的完整路径

```bash
python check_sdk_imports.py --query "WebviewController"
```

示例输出：

```text
[✓] @ohos.web.webview.webview.WebviewController [C:/Program Files/Huawei/DevEco Studio/sdk/default/openharmony/ets/api/@ohos.web.webview.d.ts:3579]
[✓] @ohos.web.webview.webview#WebviewController [C:/Program Files/Huawei/DevEco Studio/sdk/default/openharmony/ets/api/@ohos.web.webview.d.ts:28]
[✓] @kit.ArkWeb.webview.WebviewController [C:/Program Files/Huawei/DevEco Studio/sdk/default/openharmony/ets/kits/@kit.ArkWeb.d.ts]
```

选择结果时遵循以下规则：
- 优先选择**类定义本身**，通常会带类定义所在的行号，例如 `:3579`
- 对 `@ohos.web.webview.webview#WebviewController` 这种 `#` 结果，把它当成 namespace 成员提示，不要把它当成类的规范路径
- 如果同时有 `@ohos` 和 `@kit` 结果，结合用户代码里的 import 来源选择对应路径

### 2. 再查该类型的全部成员

```bash
python check_sdk_imports.py --query "@ohos.web.webview.webview.WebviewController"
```

然后在成员列表里找最接近的真实 API：

```text
[✓] @ohos.web.webview.webview.WebviewController [C:/Program Files/Huawei/DevEco Studio/sdk/default/openharmony/ets/api/@ohos.web.webview.d.ts:3579]
[✓] constructor
[✓] accessStep
[✓] forward
[✓] backward
...
[✓] webPageSnapshot
...
```

上面的报错里，`captureSnapshot` 不存在，但成员列表里可以发现真正的接口是 `webPageSnapshot`。

### 3. 如果需要精确函数签名，直接查看 `.d.ts` 定义文件

拿第 1 步或第 2 步输出中的文件路径与行号，直接打开 SDK 定义文件：

```text
C:/Program Files/Huawei/DevEco Studio/sdk/default/openharmony/ets/api/@ohos.web.webview.d.ts
```

重点查看：
- 参数列表
- 返回值类型
- 重载签名
- 是否是实例方法 / 静态方法 / namespace 成员

对于 `Property 'X' does not exist on type 'Y'` 这类错误，依次执行上述三步即可定位正确 API。

## 失败推荐

检查失败时（如 typo），自动推荐最可能需要的 API：

```
[✗] @ohos.app.ability.Ability.Ability#onConfigurationUpdates (member 'onConfigurationUpdates' not found)
    Did you mean:
      → @ohos.app.ability.Ability.Ability.onConfigurationUpdate (Levenshtein dist=1)
      → @ohos.app.ability.EnvironmentCallback.EnvironmentCallback.onConfigurationUpdated (Levenshtein dist=1)
```

**匹配算法：** 综合 Levenshtein 编辑距离、前缀匹配和语义上下文相关度。

**关闭推荐：**
```bash
python check_sdk_imports.py --path /your/project --no-recommend
```

## 输出示例

```
=== OpenHarmony SDK Import & API Check ===
SDK: c:\Program Files\Huawei\DevEco Studio\sdk
Path: ./my_project
Imports checked: 12, Member accesses: 8

[✓] @ohos.app.ability.Ability
[✓] @ohos.app.ability.Ability.Ability#onConfigurationUpdate
[✗] @ohos.app.ability.Ability.Ability#onConfigurationUpdates (member 'onConfigurationUpdates' not found)
    Did you mean:
      → @ohos.app.ability.Ability.Ability.onConfigurationUpdate (Levenshtein dist=1)
      → @ohos.app.ability.EnvironmentCallback.EnvironmentCallback.onConfigurationUpdated (Levenshtein dist=1)
[✗] @ohos.nonexistent.Module  (module not found)

Summary: 7 passed, 2 failed
```

Exit code：0 = 全部通过，1 = 存在错误。

## 文件结构

```
skills/harmony-api/
├── SKILL.md                    # 本文件
└── scripts/
    ├── check_sdk_imports.py    # CLI 主入口
    ├── sdk_indexer.py          # SDK 索引构建与加载
    ├── ts_parser.py            # TypeScript/ETS 源码解析
    ├── report.py               # 格式化输出
    └── recommender.py          # 失败推荐算法
```

## 索引缓存

索引文件 `.sdk_index.json` 位于脚本所在目录。当 SDK 文件比索引新时，自动重建索引。

## 运行测试

```bash
python tests/test_nested_class_indexing.py
```
