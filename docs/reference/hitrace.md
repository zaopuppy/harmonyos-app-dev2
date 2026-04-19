# hitrace 跟踪工具

## 概述

hitrace 是 HarmonyOS 的跟踪工具，用于捕获系统 trace 进行性能分析。

## 帮助命令

```bash
hitrace -h
```

## 列出可用标签

```bash
hitrace -l
```

常用标签：
- `app` - APP 模块
- `ace` - ACE 开发框架
- `ark` - ARK 模块
- `graphic` - 图形模块
- `binder` - Binder 内核信息
- `window` - 窗口管理器
- `ability` - Ability 管理器
- `rpc` - RPC 和 IPC
- `sched` - CPU 调度
- `freq` - CPU 频率
- `memory` - 内存
- `power` - 电源管理

## 常用命令

### 捕获指定时长 trace（文本格式）

```bash
hitrace -t 10 -b 204800 app
```

参数：
- `-t N` - 捕获时长（秒），默认 5 秒
- `-b N` - 缓冲区大小（KB），默认 18432 KB
- `app` - 要捕获的标签

### 捕获指定时长 trace（二进制格式）

```bash
hitrace -t 10 -b 204800 app --raw
```

输出文件：`/data/log/hitrace/record_trace_*.sys`

### 快照模式捕获

```bash
# 文本格式
hitrace -t 10 -b 204800 app -o /data/local/tmp/test.ftrace

# 二进制格式
hitrace -t 10 -b 204800 app --raw
```

### 录制模式（长时间）

```bash
# 开始录制
hitrace --trace_begin -b 204800 app graphic

# 停止录制并导出
hitrace --trace_dump

# 停止录制不导出
hitrace --trace_finish_nodump
```

### 压缩 trace

```bash
hitrace -t 10 -b 204800 app -z
```

### 输出到文件

```bash
hitrace -t 10 -b 204800 app -o /data/local/tmp/trace.ftrace
```

## trace 时钟类型

```bash
hitrace --trace_clock boot    # 启动时钟（默认）
hitrace --trace_clock mono    # 单调时钟
hitrace --trace_clock uptime  # 运行时间
hitrace --trace_clock perf    # 性能计数器
```

## 设置 trace 级别

```bash
# 设置级别
hitrace --trace_level D    # Debug
hitrace --trace_level I    # Info
hitrace --trace_level C    # Critical
hitrace --trace_level M    # Commercial

# 查询级别
hitrace --get_level
```

## 缓冲区选项

- `-b N` / `--buffer_size N` - 设置缓冲区大小
- `--overwrite` - 缓冲区满时覆盖旧数据（默认丢弃旧数据）

## 输出格式

- `--text` - 文本格式（默认）
- `--raw` - 二进制原始格式

## 文件名说明

录制模式下生成的文件：
- 文本格式：`/data/log/hitrace/record_trace_*.ftrace`
- 二进制格式：`/data/log/hitrace/record_trace_*.sys`

## 常见问题

### 错误码 1

权限不足，需要确保设备已 root 或有相应权限。

### 不支持 category

设备不支持指定的 trace 类别，使用 `hitrace -l` 查看支持的标签。

### 错误码 1004

缓冲区大小设置不当，尝试减小缓冲区大小。

## 使用示例

```bash
# 捕获 10 秒 app 和 graphic 标签的 trace
hitrace -t 10 -b 204800 app graphic -o trace.ftrace

# 长时间录制 UI 和动画
hitrace --trace_begin -b 409600 window animation ace
# ... 执行用户操作 ...
hitrace --trace_dump -o ui_trace.ftrace

# 压缩并导出
hitrace -t 10 app graphic -z -o trace.zip
```
