# hidumper 系统信息导出工具

## 概述

hidumper 是 HarmonyOS 的系统信息导出工具，用于查询内存、CPU、服务、进程等系统信息。

## 帮助信息

```bash
hidumper --help              # 显示帮助
hidumper --mem --help       # 内存帮助（需要指定 pid）
```

## 内存信息 (--mem)

```bash
# 整机内存
hidumper --mem

# 进程内存
hidumper --mem <pid>

# JS 堆内存
hidumper --mem-jsheap <pid>              # 导出 JS 堆
hidumper --mem-jsheap <pid> --gc         # 导出并触发 GC
hidumper --mem-jsheap <pid> --leakobj    # 导出泄露对象
hidumper --mem-jsheap <pid> --raw        # 导出原始数据

# 进程 smaps
hidumper --mem-smaps <pid>
hidumper --mem-smaps <pid> -v            # 详细模式

# 虚拟机堆内存选项
hidumper --mem <pid> --show-ashmem       # 显示 ashmem
hidumper --mem <pid> --show-dmabuf       # 显示 dmabuf

# 排除系统进程
hidumper --mem --prune
```

**输出内容：**
- Total RAM / Free RAM / Used RAM
- 进程内存使用（按 PID 和 Size 排序）
- 按 OOM adjustment 分类
- 按 Category 分类（File-backed, Anonymous, GPU, DMA 等）

## CPU 信息

```bash
# CPU 使用率
hidumper --cpuusage             # 查看当前
hidumper --cpuusage 1           # 每秒刷新

# CPU 频率
hidumper --cpufreq
```

**--cpuusage 输出：**
- Load average (1min / 5min / 15min)
- Total CPU 使用率
- User Space / Kernel Space / iowait / irq / idle
- 各进程详细使用

## 系统服务

```bash
# 服务列表
hidumper --services

# 服务详情
hidumper --service <service-name>
```

## 进程信息

```bash
# 进程列表
hidumper --ps

# 应用窗口信息
hidumper --window <pid>

# 组件树
hidumper --inspector <pid>

# 路由栈
hidumper --router <pid>
```

## 网络和存储

```bash
# 网络信息
hidumper --net

# 存储信息
hidumper --storage
```

## 系统信息

```bash
# 系统信息
hidumper --sys
```

## 故障日志

```bash
# 异常退出记录
hidumper --crashlogs

# 故障详情
hidumper --faultlogs
```

## 进程间通信

```bash
# IPC RPCS 信息
hidumper --ipcrpcs
```

## 导出功能

```bash
# 导出所有信息
hidumper --all

# 导出到指定路径
hidumper --all -s <path>

# 指定路径导出
hidumper -s <path>
```

## 常用命令示例

```bash
# 查看内存使用前 10 的进程
hidumper --mem | head -30

# 实时监控 CPU
watch hidumper --cpuusage

# 查看特定应用内存
ps | grep <app_name>              # 获取 pid
hidumper --mem <pid>

# 导出完整系统信息
hidumper --all -s /data/local/tmp/dump.zip

# 查看 JS 堆并触发 GC
hidumper --mem-jsheap <pid> --gc

# 查看进程 smaps 详情
hidumper --mem-smaps <pid> -v
```
