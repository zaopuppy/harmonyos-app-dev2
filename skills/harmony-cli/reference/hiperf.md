# hiperf 性能分析工具

## 概述

hiperf 是 HarmonyOS 的性能采样工具，用于 CPU 性能分析和函数热点分析。

## 帮助命令

```bash
hiperf --help
```

## 列出支持的事件

```bash
hiperf list
```

硬件事件：
- `hw-cpu-cycles` - CPU 时钟周期
- `hw-instructions` - 指令数
- `hw-cache-references` - 缓存引用
- `hw-cache-misses` - 缓存未命中
- `hw-branch-instructions` - 分支指令
- `hw-branch-misses` - 分支预测失败
- `hw-bus-cycles` - 总线周期

## record 命令（采样记录）

### 基本语法

```bash
hiperf record -p <pid> -d <duration> -o <output>
```

### 参数

| 参数 | 说明 |
|------|------|
| `-p <pid>` | 进程 ID |
| `-d <duration>` | 采样时长（秒） |
| `-f <freq>` | 采样频率 |
| `-s <type>` | 符号类型（fp/dwarf/stack） |
| `-e <events>` | 性能事件 |
| `-o <file>` | 输出文件 |

### 示例

```bash
# 采样进程
hiperf record -p 1234 -s fp -f 1000 -d 10 -o /data/local/tmp/perf.data

# 按应用包名采样
hiperf record --app com.example.myapp -d 10 -s dwarf --period 1000

# 采样多个事件
hiperf record -p 1234 -e hw-cpu-cycles,hw-instructions -d 10
```

## stat 命令（计数器统计）

### 基本语法

```bash
hiperf stat -d <duration> -p <pid>
```

### 示例

```bash
# 统计进程 CPU
hiperf stat -d 10 -p 1745

# 统计多个进程
hiperf stat -d 10 -p 1745,1910

# 指定事件和间隔
hiperf stat -d 10 -p 1745 -e hw-cpu-cycles,hw-instructions -i 3000
```

### 输出

```
count  name                    coverage
8,986,523  hw-cpu-cycles       1.598409 GHz
1,283,596  hw-instructions     7.001053 cycles per instruction
```

## dump 命令

导出 perf.data 内容：

```bash
hiperf dump -i <perf.data>
```

## report 命令

分析采样数据：

```bash
hiperf report -i <perf.data>
```

## 常用命令示例

```bash
# CPU 热点分析
hiperf record -p $(pidof com.example.app) -d 10 -o perf.data
hiperf report -i perf.data

# 按应用采样
hiperf record --app com.example.app -d 10 -s dwarf -o perf.data

# 统计 CPU 使用
hiperf stat -d 10 -p $(pidof com.example.app)
```

## 注意事项

- 需要设备 root 权限
- 非 root 模式下无法加载内核符号
- 采样频率不宜过高（建议 1000Hz）
