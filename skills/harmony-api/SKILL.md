---
name: harmony-api
description: HarmonyOS SDK 导入检查与 API 查询。适用场景：1）鸿蒙/ArkTS 代码生成后检查 import 语句是否正确；2）鸿蒙应用编译报错修复，排查 import 错误或 API 不存在等问题。触发关键词：import 检查、修复编译错误、API not found、@ohos 模块、@kit member、does this API exist、check imports、验证 API。
---

# HarmonyOS SDK Import & API Checker

检查 OpenHarmony/ArkTS 项目中的 `import` 语句和 API 成员调用是否存在于 SDK 中，并提供智能推荐。

## 工作原理

### 1. SDK 索引构建

首次运行（或缓存失效时），脚本扫描 SDK 目录中的 `.d.ts` 文件：
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
# 设置环境变量（Windows PowerShell）
$env:DEVECO_SDK_HOME = "c:\Program Files\Huawei\DevEco Studio\sdk\default"

# 或者让脚本自动从 hdc 路径推导 SDK_HOME（推荐）
# 确保 hdc 在 PATH 或 SDK toolchains 目录中

# 检查项目（或单个文件）
python check_sdk_imports.py --path /your/project --verbose

# 检查单个源文件
python check_sdk_imports.py --path ./src/Entry.ets

# 指定 SDK 路径
python check_sdk_imports.py --path /your/project --sdk-home "c:\Program Files\Huawei\DevEco Studio\sdk\default"

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
SDK: c:\Program Files\Huawei\DevEco Studio\sdk\default
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