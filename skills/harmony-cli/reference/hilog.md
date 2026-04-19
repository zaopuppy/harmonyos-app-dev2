# hilog 日志工具

## 概述

hilog 是 HarmonyOS 的日志查看工具，用于查看设备端的日志输出。

## 日志级别

| 级别 | 说明 |
|------|------|
| D | Debug |
| I | Info |
| W | Warn |
| E | Error |
| F | Fatal |

## 日志类型

| 类型 | 说明 |
|------|------|
| app | 应用日志 |
| core | 核心日志 |
| init | 初始化日志 |
| hypium | 测试日志 |

## 帮助命令

```bash
hilog -h
```

## 常用命令

### 非阻塞读取（退出）

```bash
hilog -x
```

### 查看指定级别日志

```bash
# 查看 Error 日志
hilog -L E

# 同时查看多个级别
hilog -L D/I/W/E/F
```

### 查看指定类型日志

```bash
# 应用日志
hilog -t app

# 内核日志
hilog -t kernel
```

### 查看指定 domain 日志

```bash
# domain 为 4 位 16 进制数
hilog -D 01B06
```

### 查看指定 TAG 日志

```bash
hilog -T SAMGR
```

### 查看缓冲区行数

```bash
# 查看缓冲区前 n 行
hilog -a 8

# 查看缓冲区后 n 行
hilog -z 8
```

### 查看指定进程日志

```bash
hilog -p <pid>
```

### 正则匹配

```bash
hilog -s "keyword.*pattern"
```

### 保持日志显示

```bash
# 持续读取日志（阻塞）
hilog

# 持续读取并过滤
hilog -L E -T MyApp
```

## 落盘任务

```bash
# 查询落盘任务
hilog -g

# 设置落盘
hilog -G <path>
```

## 日志级别设置

```bash
# 查询日志级别
hilog -l

# 设置应用日志级别
hilog --baselevel <level>

# 设置 domain 日志级别
hilog --domain <domain> <level>
```

## 其他命令

### 查看缓冲区大小

```bash
hilog --buffer
```

### 修改缓冲区大小

```bash
hilog --buffer <size>
```

### 清除日志

```bash
hilog -c
```

### 查询统计

```bash
hilog --stats
```

### 清除统计

```bash
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

### 应用日志

- 日志按 APP 类型和 domain 组合限流
- 超出限制的日志会被丢弃

### 系统日志

- 内核日志采用分区循环缓存机制
- 超出缓冲区会被覆盖

## 使用示例

```bash
# 查看所有日志
hilog

# 只看错误
hilog -L E

# 查看应用和错误
hilog -t app -L E

# 查看特定 TAG
hilog -T MyApp

# 实时过滤
hilog | grep "com.example.app"
```
