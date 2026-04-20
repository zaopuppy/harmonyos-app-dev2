# hilog 日志工具

## 概述

hilog 是 HarmonyOS 的日志查看工具，用于查看设备端的日志输出。

## 帮助信息

```bash
hilog --help
```

## 日志级别

| 级别 | 长格式 | 说明 |
|------|--------|------|
| D | DEBUG | 调试 |
| I | INFO | 信息 |
| W | WARN | 警告 |
| E | ERROR | 错误 |
| F | FATAL | 致命 |

## 日志类型

| 类型 | 说明 |
|------|------|
| app | 应用日志 |
| core | 核心日志 |
| init | 初始化日志 |
| kmsg | 内核日志（不能与其他类型组合） |
| only_prerelease | 仅预发布日志 |

## 核心选项

```bash
# 无选项 - 阻塞读取，持续打印日志
hilog

# 非阻塞读取，缓冲区日志打印完后退出
hilog -x

# 显示前 n 行
hilog -a <n>

# 显示后 n 行
hilog -z <n>
```

## 过滤选项

```bash
# 按级别过滤（可组合）
hilog -L E                    # 只看 Error
hilog -L D/I/W/E/F           # 多级别
hilog -L ^E                   # 排除 Error

# 按类型过滤
hilog -t app                  # 只看应用日志
hilog -t app,core             # 应用+核心
hilog -t ^kmsg                # 排除内核日志

# 按 domain 过滤（最多 5 个）
hilog -D 01B06                # 单个 domain
hilog -D 01B06,02A07          # 多个 domain

# 按标签过滤（最多 10 个）
hilog -T MyApp                # 单个标签
hilog -T Tag1,Tag2,Tag3       # 多个标签

# 按进程 ID 过滤（最多 5 个）
hilog -P 1234,5678

# 正则匹配
hilog -e "keyword.*pattern"
```

## 输出格式

```bash
# 彩色输出（按级别着色）
hilog -v color

# 时间格式
hilog -v time           # 本地时间（默认）
hilog -v epoch          # 1970/1/1 至今
hilog -v monotonic      # 启动后 CPU 时间

# 时间精度
hilog -v msec           # 毫秒（默认）
hilog -v usec           # 微秒
hilog -v nsec           # 纳秒

# 其他格式选项
hilog -v year           # 显示年份
hilog -v zone           # 显示时区
hilog -v wrap           # 换行不重复前缀
hilog -v long           # 显示所有元数据

# 组合示例
hilog -v color -v time -v msec -v year -v zone
```

## 落盘任务

```bash
# 查询落盘任务
hilog -g

# 设置落盘
hilog -G <path>
```

## 缓冲区管理

```bash
# 查询缓冲区大小
hilog -g

# 设置缓冲区大小（64K-16M）
hilog -G 1M

# 清除日志
hilog -r                    # 清除所有
hilog -r -t app            # 只清除应用日志
```

## 日志级别设置

```bash
# 查询日志级别
hilog -l

# 设置应用日志基础级别
hilog --baselevel <level>

# 设置 domain 日志级别
hilog --domain <domain> <level>
```

## 统计信息

```bash
# 查询统计
hilog --stats

# 清除统计
hilog --clear-stats
```

## 日志格式

```
MM-DD HH:MM:SS.mmm  PID  TID  Level Domain/TAG: Message
```

示例：
```
11-15 16:04:54.981  5687  5687 I A01B06/common/KG: MetaBalls-MetaBallRenderer --> pressTime = 0
```

## 超限机制

- **应用日志**：按 APP 类型和 domain 组合限流，超出限制被丢弃
- **系统日志**：内核日志采用分区循环缓存，超出缓冲区被覆盖

## 使用示例

```bash
# 实时查看所有日志
hilog

# 只看错误
hilog -L E

# 彩色错误日志
hilog -L E -v color

# 特定标签+实时
hilog -T MyApp

# 应用错误+时间戳
hilog -t app -L E -v time -v msec

# 过滤多个标签
hilog -T Tag1,Tag2,Tag3

# 排除某级别
hilog -L ^D,^I

# 导出到文件
hilog -G /data/log/hilog.txt
```
