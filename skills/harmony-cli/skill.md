---
name: harmony-cli
description: HarmonyOS 命令行工具 - hdc, hilog, hidumper, hitrace 等
---

# HarmonyOS 命令行工具

提供 HarmonyOS 常用命令行工具的参考。

## 环境准备

### 检查工具是否可用

使用 `which`（Linux/Mac）或 `where`（Windows）检查工具是否可用：

```bash
# Linux/Mac
which hdc

# Windows PowerShell
where hdc
```

### 环境变量设置

**前提**：正确设置 `DEVECO_SDK_HOME` 或 `hdc` 在 `$PATH` 中。

**方式一**：设置 `DEVECO_SDK_HOME`

```bash
# Linux/Mac (bash)
export DEVECO_HOME=$DEVECO_SDK_HOME/..
export PATH=$DEVECO_HOME/tools/node:$PATH
export PATH=$DEVECO_HOME/tools/ohpm/bin:$PATH
export PATH=$DEVECO_HOME/tools/hvigor/bin:$PATH

# Windows PowerShell
$env:DEVECO_HOME = "$env:DEVECO_SDK_HOME\.."
$env:PATH = "$env:DEVECO_HOME\tools\node;$env:PATH"
$env:PATH = "$env:DEVECO_HOME\tools\ohpm\bin;$env:PATH"
$env:PATH = "$env:DEVECO_HOME\tools\hvigor\bin;$env:PATH"
```

**方式二**：确保 hdc 在 PATH 中

hdc 通常位于：`$DEVECO_SDK_HOME/default/openharmony/toolchains/hdc`

---

## hdc 命令

hdc（HarmonyOS Device Connector）是命令行调试工具，用于与设备交互、数据传输、日志查看和应用安装。

### 全局命令

```bash
hdc -h [verbose]      # 打印帮助
hdc -v/version         # 打印版本
hdc -l[0-6]            # 设置日志级别
hdc -t connectkey       # 连接指定设备
hdc checkserver         # 检查版本
```

### 会话命令

```bash
# 设备列表
hdc list targets [-v]           # 列出所有设备，-v 详细信息

# 连接设备
hdc tconn key [-remove]        # TCP 连接
hdc tconn 192.168.0.100:10178  # TCP 连接示例
hdc tconn COM5,921600          # UART 连接

# 服务控制
hdc start [-r]                 # 启动服务，-r 重启
hdc kill [-r]                  # 终止服务
hdc -s [ip:]port               # 设置监听端口
```

### 设备命令

```bash
# 文件系统
hdc target mount                # 挂载 /system 为读写
hdc target boot                # 重启设备
hdc target boot -bootloader     # 重启到 bootloader
hdc target boot -recovery       # 重启到 recovery

# 权限
hdc smode [-r]                 # 提权，-r 取消权限

# 调试模式
hdc tmode usb                  # USB 调试模式
hdc tmode port [port]         # TCP 调试模式
hdc tmode port close           # 关闭 TCP
```

### 文件传输

```bash
# 发送文件到设备
hdc file send [option] local remote

# 从设备接收文件
hdc file recv [option] remote local

# 选项：
# -a: 保持目标文件时间戳
# -sync: 仅更新新文件
# -z: 压缩传输
# -m: 模式同步
# -cwd: 指定工作目录
# -b: 发送到调试应用目录
```

**示例**：
```bash
hdc file send /local/app.hap /data/local/tmp/app.hap
hdc file recv /data/local/tmp/log.txt /local/log.txt
hdc file send -b /local/config.xml /data/data/com.example/config.xml
```

### 端口转发

```bash
hdc fport ls                     # 列出转发任务
hdc fport rm taskstr            # 删除任务
hdc fport tcp:8710 tcp:8710    # 正向转发
hdc fport rport tcp:8710 tcp:8710  # 反向转发
```

### 应用管理

```bash
# 安装应用
hdc install [-r|-s|-cwd] src
# -r: 替换安装
# -s: 安装共享 bundle
# -cwd: 指定工作目录

# 卸载应用
hdc uninstall [-k] [-s] package
# -k: 保留数据和缓存
# -s: 卸载共享 bundle
```

**示例**：
```bash
hdc install /local/app.hap
hdc install -r /local/app.hap
hdc uninstall com.example.app
hdc uninstall -k com.example.app
```

### 调试命令

```bash
# 查看日志
hdc hilog [-h|parse]
hdc hilog                          # 实时查看日志
hdc hilog -h                       # 详细帮助

# 执行 shell 命令
hdc shell [-b bundlename] [COMMAND]
hdc shell ls /data/log
hdc shell "ls -la"

# 获取设备信息
hdc bugreport [FILE]               # 获取设备完整信息

# 调试进程
hdc jpid                           # 列出 JDWP 进程
hdc track-jpid [-a|-p]            # 跟踪调试进程
```

### 安全命令

```bash
hdc keygen FILE                    # 生成公私钥对
```

---

## hilog 日志工具

设备端日志查看工具。

```bash
# 实时查看日志
hdc shell hilog

# 查看帮助
hdc shell hilog -h

# 按级别过滤
hdc shell hilog -L E               # 只看 Error
hdc shell hilog -L D/I/W/E/F       # 多级别

# 按标签过滤
hdc shell hilog -T MyApp

# 按 domain 过滤
hdc shell hilog -D 01B06

# 缓冲区
hdc shell hilog -a 8               # 前 n 行
hdc shell hilog -z 8                # 后 n 行

# 保持日志（非阻塞退出）
hdc shell hilog -x
```

---

## hidumper 系统信息

系统信息导出工具。

```bash
hdc shell hidumper --help          # 查看帮助

# 内存信息
hdc shell hidumper --mem           # 整机内存
hdc shell hidumper --mem <pid>     # 进程内存

# CPU 使用
hdc shell hidumper --cpuusage      # CPU 使用率
hdc shell hidumper --cpufreq       # CPU 频率

# 系统服务
hdc shell hidumper --services      # 服务列表
hdc shell hidumper --service <name>  # 服务详情

# 进程信息
hdc shell hidumper --ps            # 进程列表

# 导出所有信息
hdc shell hidumper --all -s /data/local/tmp/dump.zip
```

---

## hitrace 跟踪工具

性能跟踪采样工具。

```bash
# 查看帮助
hdc shell hitrace -h

# 列出可用标签
hdc shell hitrace -l

# 捕获 trace（10 秒）
hdc shell hitrace -t 10 -b 204800 app graphic

# 输出到文件
hdc shell hitrace -t 10 -b 204800 app -o /data/local/tmp/trace.ftrace

# 压缩
hdc shell hitrace -t 10 -b 204800 app -z
```

常用标签：`app`、`graphic`、`ace`、`ark`、`window`、`ability`、`binder`

---

## hiperf 性能分析

CPU 性能采样工具。

```bash
# 列出支持的事件
hdc shell hiperf list

# 采样记录
hdc shell hiperf record -p <pid> -d 10 -o /data/local/tmp/perf.data

# 统计
hdc shell hiperf stat -d 10 -p <pid>
```

---

## aa 工具（Ability 管理）

```bash
# 通过 hdc shell 执行
hdc shell aa -h                    # 帮助
hdc shell aa start -b <bundle> -a <ability>  # 启动
hdc shell aa force-stop <bundle>    # 强制停止
hdc shell aa dump -n <bundle>       # 打印信息
```

---

## bm 工具（包管理）

```bash
hdc shell bm -h                     # 帮助
hdc shell bm install -p <path>      # 安装
hdc shell bm uninstall -n <bundle>   # 卸载
hdc shell bm dump -a                 # 列出已安装应用
hdc shell bm dump -n <bundle>       # 应用详情
hdc shell bm clean -c -n <bundle>   # 清理缓存
```

---

## 参考文档

更多工具详情请参考 `reference/` 目录：
- `reference/hdc.md`
- `reference/aa-tool.md`
- `reference/bm-tool.md`
- `reference/hilog.md`
- `reference/hidumper.md`
- `reference/hitrace.md`
- `reference/hiperf.md`
