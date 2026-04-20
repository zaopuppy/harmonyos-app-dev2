# param 系统参数工具

## 概述

param 是 HarmonyOS 的系统参数管理工具，用于查看、设置、等待系统参数。

**前置条件**：需要先获取 hdc 工具并执行 `hdc shell param`。

## 命令列表

| 命令 | 描述 |
|------|------|
| `param ls` | 列出系统参数 |
| `param get` | 获取参数值 |
| `param set` | 设置参数值 |
| `param wait` | 等待参数变化 |
| `param dump` | 导出所有参数 |
| `param shell` | Shell 模式 |
| `param save` | 保存持久化参数 |

## 查看参数 (ls)

```bash
# 列出所有参数
param ls

# 递归列出（显示层级）
param ls -r

# 列出指定参数
param ls <name>
```

## 获取参数 (get)

```bash
# 获取单个参数值
param get <name>

# 示例
param getpersist sys.hilogutable
param get lready.bootevent.sys.bootevent
```

## 设置参数 (set)

```bash
# 设置参数值
param set <name> <value>

# 示例
param set debug.atrace 1
param set persist.hilogd.enabled true
```

**注意**：部分参数需要 root 权限或重启后才生效。

## 等待参数 (wait)

```bash
# 等待参数变化
param wait <name> [value] [timeout]

# 等待参数变为指定值
param wait <name> <value>

# 带超时等待（秒）
param wait <name> <value> 30

# 示例
param wait sys.bootevent 1 60
```

## 导出参数 (dump)

```bash
# 导出所有参数
param dump

# 详细导出
param dump verbose
```

## Shell 模式 (shell)

```bash
# 进入交互模式
param shell

# 按命名空间筛选
param shell -p <name>

# 按用户筛选
param shell -u <username>

# 按组筛选
param shell -g <groupname>
```

## 保存参数 (save)

```bash
# 保存所有持久化参数到工作区
param save
```

## 常用参数示例

```bash
# 查看所有日志相关参数
param ls | grep -i log

# 查看启动事件参数
param ls | grep -i boot

# 查看调试参数
param ls | grep -i debug

# 等待设备启动完成
param wait sys.bootevent 1 300
```

## 常见使用场景

| 场景 | 命令 |
|------|------|
| 查看设备是否启动完成 | `param get lready.bootevent.sys.bootevent` |
| 查看日志级别 | `param ls \| grep -i log` |
| 开启调试模式 | `param set debug.atrace 1` |
| 查看 Hildi 状态 | `param ls \| grep -i Hildi` |
| 等待系统服务启动 | `param wait sys.bootevent 1 600` |
