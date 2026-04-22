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