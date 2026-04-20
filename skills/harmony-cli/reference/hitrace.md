# hitrace 跟踪工具

## 概述

hitrace 是 HarmonyOS 的跟踪工具，用于捕获系统 trace 进行性能分析。

## 帮助信息

```bash
hitrace --help
```

## 可用标签

```bash
hitrace -l
```

常用标签：
| 标签 | 说明 |
|------|------|
| app | APP 模块 |
| ace | ACE 开发框架 |
| ark | ARK 模块 |
| graphic | 图形模块 |
| binder | Binder 内核信息 |
| window | 窗口管理器 |
| ability | Ability 管理器 |
| rpc | RPC 和 IPC |
| sched | CPU 调度 |
| freq | CPU 频率 |
| memory | 内存 |
| power | 电源管理 |
| init | 初始化 |
| webview | WebView |

## 核心选项

```bash
# 捕获指定时长 trace（默认 5 秒）
hitrace -t <seconds>

# 缓冲区大小（默认 18432 KB）
hitrace -b <size KB>

# 指定输出文件
hitrace -o <filename>

# 压缩
hitrace -z
```

## 录制模式

```bash
# 开始录制
hitrace --trace_begin -b <size> <tags>

# 停止录制并导出
hitrace --trace_dump

# 停止录制不导出
hitrace --trace_finish_nodump

# 长时间录制任务
hitrace --record --trace_begin -b <size> <tags>
```

## 输出格式

```bash
# 文本格式（默认）
hitrace --text

# 二进制原始格式
hitrace --raw
```

## 时钟类型

```bash
hitrace --trace_clock boot      # 启动时钟（默认）
hitrace --trace_clock global     # 全局时钟
htrace --trace_clock mono        # 单调时钟
hitrace --trace_clock uptime     # 运行时间
hitrace --trace_clock perf       # 性能计数器
```

## Trace 级别

```bash
# 设置级别
hitrace --trace_level D         # Debug
hitrace --trace_level I         # Info
hitrace --trace_level C         # Critical
hitrace --trace_level M         # Commercial

# 查询级别
hitrace --get_level
```

## 缓冲区选项

```bash
# 设置缓冲区大小
hitrace -b <size>                # KB

# 缓冲区满时覆盖
hitrace --overwrite              # 覆盖旧数据（默认丢弃）
```

## 后台服务模式

```bash
# 启用快照模式
hitrace --start_bgsrv

# 触发 dump 任务
hitrace --dump_bgsrv

# 停止后台服务
hitrace --stop_bgsrv
```

## Raw 模式选项

```bash
# Raw 模式文件大小（默认 102400 KB）
hitrace --file_size <size KB>
```

## 使用示例

```bash
# 捕获 10 秒 app 和 graphic 标签
hitrace -t 10 -b 204800 app graphic -o trace.ftrace

# 捕获 30 秒并压缩
hitrace -t 30 -b 409600 app ace ark -z

# 录制模式
hitrace --trace_begin -b 204800 app graphic
# ... 执行用户操作 ...
hitrace --trace_dump -o trace.ftrace

# 按进程 ID 跟踪
hitrace -t 10 app -b 204800 -p <pid>

# 使用 perf 时钟
hitrace -t 10 --trace_clock perf app graphic

# 覆盖模式（保留最新数据）
hitrace -t 10 --overwrite app graphic
```

## 输出文件

录制模式下：
- 文本格式：`/data/log/hitrace/record_trace_*.ftrace`
- 二进制格式：`/data/log/hitrace/record_trace_*.sys`
