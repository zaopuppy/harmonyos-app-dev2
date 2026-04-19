# HarmonyOS Skills 项目设计

## 概述

为 LLM Agent 提供 HarmonyOS 应用开发辅助的技能工具箱。

## 设计原则

1. **Markdown 优先**：所有 skill 为标准 markdown，跨平台兼容
2. **零耦合**：每个 skill 独立目录
3. **统一前缀**：`harmony-` 前缀避免命名冲突
4. **通用 prompt**：不依赖特定 Agent 工具

## 目录结构

```
harmonyos-app-dev/
├── docs/specs/                    # 设计文档
├── skills/
│   ├── harmony-arkts/            # ArkTS 语法
│   ├── harmony-arkui/            # ArkUI 组件
│   ├── harmony-template/          # 模板
│   ├── harmony-ut/               # 单元测试
│   └── harmony-devtools/         # 开发者工具
├── CLAUDE.md
└── .claude/settings.json
```

## Skills 定义

| Skill | 描述 |
|-------|------|
| harmony-arkts | ArkTS 语言语法、类型系统、并发等 |
| harmony-arkui | ArkUI 组件库、布局、动画等 |
| harmony-template | 项目模板、模块模板 |
| harmony-ut | 单元测试框架、测试用例编写 |
| harmony-devtools | DevEco Studio、调试工具使用 |
