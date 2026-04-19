# hidumper 系统信息导出工具

## 概述

hidumper 是 HarmonyOS 的系统信息导出工具，用于查询内存、CPU、服务、进程等系统信息。

## 查询内存信息

### 查询整机内存

```bash
hidumper --mem
```

输出包括：
- Total RAM / Free RAM / Used RAM
- 进程内存使用（按 PID 和 Size 排序）
- 按 OOM adjustment 分类
- 按 Category 分类（File-backed, Anonymous, GPU, DMA 等）

### 查询进程内存

```bash
hidumper --mem <pid>
```

### 查询虚拟机堆内存

```bash
hidumper --mem <pid> --show-ashmem   # 显示 ashmem 信息
hidumper --mem <pid> --show-dmabuf   # 显示 dmabuf 信息
```

### 排除系统进程的内存

```bash
hidumper --mem --prune
```

### 查询 JS 堆内存

```bash
# 导出 JS 堆内存
hidumper --mem-jsheap <pid>

# 导出并触发 GC
hidumper --mem-jsheap <pid> --gc

# 导出泄露对象
hidumper --mem-jsheap <pid> --leakobj

# 导出原始数据
hidumper --mem-jsheap <pid> --raw
```

### 查询进程 smaps

```bash
hidumper --mem-smaps <pid>
hidumper --mem-smaps <pid> -v  # 详细模式
```

## 查询 CPU 使用情况

### 查询整机 CPU

```bash
hidumper --cpuusage        # 查看当前 CPU
hidumper --cpuusage 1       # 每秒刷新
```

输出：
- Load average (1min / 5min / 15min)
- Total CPU 使用率
- User Space / Kernel Space / iowait / irq / idle
- 各进程详细使用

### 查询 CPU 频率

```bash
hidumper --cpufreq
```

## 查询系统服务

### 查询服务列表

```bash
hidumper --services
```

### 获取服务详细信息

```bash
hidumper --service <service-name>
```

## 查询进程信息

```bash
hidumper --ps
```

## 查询网络信息

```bash
hidumper --net
```

## 查询存储信息

```bash
hidumper --storage
```

## 查询系统信息

```bash
hidumper --sys
```

## 获取故障日志

### 获取异常退出记录

```bash
hidumper --crashlogs
```

### 获取故障详情

```bash
hidumper --faultlogs
```

## 获取进程间通信信息

```bash
hidumper --ipcrpcs
```

## 导出信息

```bash
hidumper --all          # 导出所有信息
hidumper -s <path>      # 导出到指定路径
```

## ArkUI 基础信息

### 获取应用窗口信息

```bash
hidumper --window <pid>
```

### 获取组件树

```bash
hidumper --inspector <pid>
```

### 获取路由栈

```bash
hidumper --router <pid>
```

## 常用命令示例

```bash
# 查看内存使用前 10 的进程
hidumper --mem | head -30

# 实时监控 CPU
watch hidumper --cpuusage

# 查看特定应用内存
ps | grep <app_name>  # 获取 pid
hidumper --mem <pid>

# 导出完整系统信息
hidumper --all -s /data/local/tmp/dump.zip
```
