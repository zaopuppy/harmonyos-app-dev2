# HarmonyOS 应用开发技能工具箱

为 LLM Agent 系统提供 ArkTS 语法、ArkUI 组件、API 检查、UT 测试、CLI 工具等开发辅助。

## Skills

| Skill | 用途 |
|-------|------|
| `harmony-arkts` | ArkTS 语法参考，类型系统、类、异步等 |
| `harmony-arkui` | ArkUI 组件语法，布局、列表、动画、手势等 |
| `harmony-template` | 应用/模块模板 |
| `harmony-ut` | 单元测试 |
| `harmony-cli` | 命令行工具：hdc、hilog、hidumper、hitrace、hiperf 等 |
| `harmony-api` | SDK 导入检查与 API 查询 |

## 使用方式

Agent 可直接读取 `skills/<name>/SKILL.md` 获取对应技能指导。

## 环境准备

**在使用本工具箱前，请先在终端中手动执行以下命令检查并配置 PATH。**

### 第一步：检查工具是否可用

```powershell
# PowerShell
where hdc; where hvigorw; where ohpm
```

```bash
# Git Bash / Linux / Mac
which hdc; which hvigorw; which ohpm
```

如果三个命令都找到，说明 PATH 已正确配置，跳过第二步。

### 第二步：配置 PATH（如有命令找不到）

`DEVECO_SDK_HOME` 指向 SDK 根目录（可在 DevEco Studio 安装目录找到）。

**Windows PowerShell：**

```powershell
# 手动设置 DEVECO_SDK_HOME（替换为你的实际路径）
$env:DEVECO_SDK_HOME = "C:\Program Files\Huawei\DevEco Studio\sdk"
$env:DEVECO_HOME = "$env:DEVECO_SDK_HOME\.."
$env:PATH = "$env:DEVECO_SDK_HOME\default\openharmony\toolchains;$env:DEVECO_HOME\tools\node;$env:DEVECO_HOME\tools\ohpm\bin;$env:DEVECO_HOME\tools\hvigor\bin;$env:PATH"

# 再次验证
where hdc; where hvigorw; where ohpm
```

**macOS / Linux / Git Bash：**

```bash
export DEVECO_SDK_HOME=${DEVECO_SDK_HOME:-$(dirname $(dirname $(dirname $(dirname $(dirname $(which hdc))))))}
export DEVECO_HOME=$DEVECO_SDK_HOME/..
export PATH=$DEVECO_SDK_HOME/default/openharmony/toolchains:$DEVECO_HOME/tools/node:$DEVECO_HOME/tools/ohpm/bin:$DEVECO_HOME/tools/hvigor/bin:$PATH

# 再次验证
which hdc; which hvigorw; which ohpm
```

> **建议**：将上述配置加入 Shell 配置文件（`~/.bashrc`、`~/.zshrc`、`$PROFILE`），省去每次手动执行。

## 目录结构

```
├── skills/
│   ├── harmony-arkts/        # ArkTS 语法参考
│   ├── harmony-arkui/        # ArkUI 组件参考
│   ├── harmony-template/    # 项目/模块模板
│   ├── harmony-ut/           # 单元测试
│   ├── harmony-cli/          # CLI 工具
│   │   └── reference/        # 各工具详细文档
│   └── harmony-api/          # SDK 导入检查
│       └── scripts/         # Python 检查脚本
├── docs/
│   └── specs/                # 设计文档
├── CLAUDE.md
└── README.md
```