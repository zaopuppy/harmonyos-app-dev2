# hiperf 性能分析工具

## 概述

hiperf 是 HarmonyOS 的 CPU 性能采样工具，用于性能分析和函数热点分析。

## 帮助信息

```bash
hiperf --help
hiperf help <command>
```

## 全局选项

```bash
--debug              显示调试日志
--hilog             使用 hilog 而非文件记录日志
--logpath <path>     指定日志文件路径
--verbose            显示调试日志
--nodebug            禁用调试日志
```

## list 命令 - 列出支持的事件

```bash
hiperf list
hiperf list hw           # 硬件事件
hiperf list sw           # 软件事件
hiperf list tp           # tracepoint 事件
hiperf list cache        # 硬件缓存事件
hiperf list raw          # 原始 PMU 事件
```

**硬件事件：**
- `hw-cpu-cycles` - CPU 时钟周期
- `hw-instructions` - 指令数
- `hw-cache-references` - 缓存引用
- `hw-cache-misses` - 缓存未命中
- `hw-branch-instructions` - 分支指令
- `hw-branch-misses` - 分支预测失败
- `hw-bus-cycles` - 总线周期

## record 命令 - 采样记录

```bash
hiperf record [options]
```

**常用选项：**

| 选项 | 说明 |
|------|------|
| `-p <pid1>[,pid2]...` | 目标进程 ID |
| `-t <tid1>[,tid2]...` | 目标线程 ID |
| `-a` | 全系统采样（所有进程/线程） |
| `-d <sec>` | 采样时长（默认 10000 秒） |
| `-f <freq>` | 采样频率（默认 4000/秒） |
| `-e <event>` | 性能事件（默认 hw-cpu-cycles） |
| `-o <file>` | 输出文件（默认 /data/local/tmp/perf.data） |
| `-g` | 事件分组 |
| `--period <num>` | tracepoint 事件采样周期 |

**过滤选项：**

| 选项 | 说明 |
|------|------|
| `--exclude-tid <tid>` | 排除指定线程 |
| `--exclude-thread <name>` | 按线程名排除 |
| `--exclude-process <name>` | 按进程名排除（需配合 -a） |
| `--exclude-hiperf` | 不记录 hiperf 自身事件 |
| `--no-inherit` | 不跟踪子进程 |
| `--offcpu` | 跟踪被调度出 CPU 的线程 |

**CPU 限制：**

```bash
-c <cpuid>[,cpuid]...     # 指定 CPU
--cpu-limit <percent>     # 最大 CPU 使用率（1-100%，默认 25%）
```

**分支过滤：**

```bash
-j <filter>               # 分支栈采样
# filter: any, any_call, any_ret, ind_call, ind_jmp, cond, call
```

**示例：**

```bash
# 采样进程 10 秒
hiperf record -p 1234 -d 10 -o /data/local/tmp/perf.data

# 全系统采样
hiperf record -a -d 10

# 指定采样频率
hiperf record -p 1234 -f 1000 -d 10

# 多事件采样
hiperf record -p 1234 -e hw-cpu-cycles,hw-instructions -d 10

# 按应用包名采样
hiperf record --app com.example.myapp -d 10

# 排除 hiperf 自身
hiperf record -p 1234 --exclude-hiperf -d 10
```

## stat 命令 - 计数器统计

```bash
hiperf stat [options]
```

**常用选项：**

| 选项 | 说明 |
|------|------|
| `-p <pid>` | 目标进程 ID |
| `-a` | 全系统统计 |
| `-d <sec>` | 统计时长（默认 10000 秒） |
| `-e <event>` | 性能事件 |
| `-i <ms>` | 打印间隔（毫秒） |
| `--per-core` | 每个 CPU 核心单独统计 |
| `--per-thread` | 每个线程单独统计 |

**应用启动统计：**

```bash
--app <package_name>      # 统计应用启动
--restart                 # 统计应用重启
--chkms <millisec>        # 查询应用启动间隔（1-200ms，默认 10ms）
```

**输出控制：**

```bash
--verbose                 # 详细报告
--dumpoptions            # 打印命令选项
-o <file>                 # 输出文件（默认 /data/local/tmp/perf_stat.txt）
```

**控制接口：**

```bash
--control prepare         # 准备计数
--control start           # 开始计数
--control stop            # 停止计数
```

**示例：**

```bash
# 统计进程 CPU
hiperf stat -d 10 -p 1745

# 统计多个进程
hiperf stat -d 10 -p 1745,1910

# 每秒打印
hiperf stat -d 10 -p 1745 -i 1000

# 全系统统计
hiperf stat -a -d 10

# 每核心统计
hiperf stat -a --per-core -d 10

# 应用启动统计
hiperf stat --app com.example.app --restart
```

## dump 命令 - 导出数据

```bash
hiperf dump [options]
```

**选项：**

| 选项 | 说明 |
|------|------|
| `--head` | 只导出头部和属性 |
| `-d` | 只导出数据段 |
| `-f` | 只导出特性 |
| `-i <file>` | 输入文件（默认 perf.data） |
| `--elf <file>` | 导出 ELF 文件 |
| `--proto <file>` | 从 protobuf 导出 |
| `--export <index>` | 导出用户栈数据 |
| `-o <file>` | 输出文件名 |

**示例：**

```bash
hiperf dump -i /data/local/tmp/perf.data
hiperf dump --head -i /data/local/tmp/perf.data
```

## report 命令 - 分析报告

```bash
hiperf report [options]
```

**符号选项：**

```bash
--symbol-dir <dir>        # 符号文件目录
```

**输出选项：**

```bash
--json                    # JSON 格式输出
--proto                   # protobuf 格式
```

**显示选项：**

```bash
-s / --call-stack         # 显示调用栈
--limit-percent <num>     # 只显示超过指定热度的内容
--call-stack-limit-percent <num>  # 调用栈热度限制
--branch                 # 显示分支的源地址而非 IP 地址
```

**排序选项：**

```bash
--sort <key1>[,key2]...   # 排序关键词
--<keys> <name>[,...]     # 选择显示的关键词
# 可选关键词: comms, pids, tids, dsos, funcs, from_dsos, from_funcs
```

**diff 选项：**

```bash
--diff <target file>      # 与目标文件对比
```

**示例：**

```bash
# 基本报告
hiperf report -i /data/local/tmp/perf.data

# 调用栈报告
hiperf report -i /data/local/tmp/perf.data -s

# JSON 格式
hiperf report -i /data/local/tmp/perf.data --json

# 按函数排序
hiperf report -i /data/local/tmp/perf.data --sort funcs

# 显示超过 5% 热度的内容
hiperf report --limit-percent 5
```

## 完整示例

```bash
# 1. CPU 热点分析
hiperf record -p $(pidof com.example.app) -d 10 -o perf.data
hiperf report -i perf.data -s

# 2. 应用启动性能
hiperf stat --app com.example.app --restart -d 30

# 3. 多事件分析
hiperf record -p 1234 -e hw-cpu-cycles,hw-instructions -d 10 -o perf.data
hiperf report -i perf.data
```

## 注意事项

- 需要设备 root 权限
- 非 root 模式下无法加载内核符号
- 采样频率不宜过高（建议 1000Hz）
