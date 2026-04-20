# hdc (HarmonyOS Device Connector)

## 概述

hdc（HarmonyOS Device Connector）是命令行调试工具，用于与设备交互、数据传输、日志查看和应用安装。支持 Windows/Linux/MacOS。

## 架构

- **客户端（client）**：电脑端进程，执行 hdc 命令时启动，命令结束后自动退出
- **服务器（server）**：电脑端后台服务，管理客户端和设备端守护进程之间的数据交互
- **守护程序（daemon）**：设备端进程，响应服务器请求

默认监听电脑端 8710 端口，可通过环境变量 `OHOS_HDC_SERVER_PORT` 自定义。

## 帮助信息

```bash
hdc --help              # 简短帮助
hdc -h verbose         # 详细帮助
```

## 全局命令

| 命令 | 说明 |
|------|------|
| `hdc -h [verbose]` | 打印帮助 |
| `hdc -v` | 打印版本 |
| `hdc -l[0-6]` | 设置日志级别 |
| `hdc -t <connectkey>` | 连接指定设备 |
| `hdc checkserver` | 检查版本 |

## 会话命令（服务端）

```bash
# 设备列表
hdc list targets [-v]           # -v 详细信息

# 连接设备
hdc tconn <key> [-remove]       # TCP 连接
hdc tconn <ip>:8710             # TCP 连接示例
hdc tconn COM5,921600           # UART 连接（可指定波特率）

# 服务控制
hdc start [-r]                  # 启动服务，-r 重启
hdc kill [-r]                   # 终止服务，-r 重启
hdc -s [ip:]port                # 设置监听端口
```

**连接示例：**
```bash
hdc tconn 192.168.0.100:8710        # TCP
hdc tconn 192.168.0.100:10178       # TCP 指定端口
hdc tconn COM5,921600               # UART
hdc tconn COM5                      # UART 默认波特率
```

## 设备命令

```bash
# 文件系统
hdc target mount                 # 挂载 /system 为读写
hdc target boot                  # 重启设备
hdc target boot -bootloader      # 重启到 bootloader
hdc target boot -recovery        # 重启到 recovery
hdc target boot <MODE>           # 重启到指定模式

# 权限
hdc smode [-r]                  # 提权，-r 取消权限

# 调试模式
hdc tmode usb                   # USB 调试模式
hdc tmode port [port]           # TCP 调试模式
hdc tmode port close            # 关闭 TCP

# 等待设备
hdc wait                        # 等待设备可用
```

## 文件传输

```bash
# 发送文件到设备
hdc file send [option] <local> <remote>

# 从设备接收文件
hdc file recv [option] <remote> <local>
```

**选项：**

| 选项 | 说明 |
|------|------|
| `-a` | 保持目标文件时间戳 |
| `-sync` | 仅更新新文件 |
| `-z` | 压缩传输 |
| `-m` | 模式同步 |
| `-cwd <dir>` | 指定工作目录 |
| `-b` | 发送到调试应用目录 |

**示例：**
```bash
hdc file send /local/app.hap /data/local/tmp/app.hap
hdc file recv /data/local/tmp/log.txt /local/log.txt
hdc file send -b /local/config.xml /data/data/com.example/config.xml
hdc file send -sync /local/*.hap /data/local/tmp/
```

## 端口转发

```bash
hdc fport ls                     # 列出转发任务
hdc fport rm <taskstr>          # 删除任务
hdc fport tcp:<local> tcp:<remote>   # 正向转发
hdc rport tcp:<remote> tcp:<local>   # 反向转发
```

**节点格式：**
- `tcp:<port>`
- `localfilesystem:<unix domain socket>`
- `localreserved:<unix domain socket>`
- `localabstract:<unix domain socket>`

**示例：**
```bash
hdc fport tcp:8710 tcp:8710
hdc fport tcp:9222 tcp:9222
hdc rport tcp:9222 tcp:9222
```

## 应用管理

```bash
# 安装应用
hdc install [-r|-s|-cwd] <src>

# 卸载应用
hdc uninstall [-k] [-s] <package>
```

**选项：**
- `-r`: 替换安装
- `-s`: 安装共享 bundle
- `-cwd`: 指定工作目录
- `-k`: 保留数据和缓存

**示例：**
```bash
hdc install /local/app.hap
hdc install -r /local/app.hap
hdc uninstall com.example.app
hdc uninstall -k com.example.app
```

## 调试命令

```bash
# 查看日志
hdc hilog [-h|parse]            # 显示帮助
hdc hilog                        # 实时查看日志

# 执行 shell 命令
hdc shell [-b <bundlename>] [COMMAND]
hdc shell ls /data/log
hdc shell "ls -la"

# 获取设备信息
hdc bugreport [FILE]             # 获取完整故障报告

# 调试进程
hdc jpid                         # 列出 JDWP 进程
hdc track-jpid [-a|-p]          # 跟踪调试进程
```

## 安全命令

```bash
hdc keygen <FILE>                # 生成公私钥对
```

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `OHOS_HDC_SERVER_PORT` | 服务器监听端口 | 8710 |
| `OHOS_HDC_LOG_LEVEL` | 日志级别 | 2 |
| `OHOS_HDC_HEARTBEAT` | 心跳间隔（秒） | - |
| `OHOS_HDC_CMD_RECORD` | 命令录制 | - |
| `OHOS_HDC_ENCRYPT_CHANNEL` | 加密通道 | - |

## 错误码

| 错误码 | 说明 |
|--------|------|
| E000001 | hdc 版本太低 |
| E000002 | 设备未授权 |
| E000003 | 设备端用户未授权 |
| E000004 | 通信连接不稳定 |
| E001000 | tmode 不支持设置 USB 调试 |
| E001001 | 命令未知 |
| E001003 | USB 连接异常 |
| E001005 | 设备未知或断连 |
| E001104 | tconn 命令 IP 地址非法 |
| E002101 | 服务器进程无法结束 |
| E002105 | 命令不支持 |
| E003001 | 指定的包名非法 |
| E005003 | 文件传输缺少参数 |
| E005005 | 创建目录失败 |
| E006001 | 安装包路径非法 |

## 常见问题

### 设备无法识别

1. 检查 USB 线是否支持数据传输
2. 确认设备开发者选项已开启
3. 尝试更换 USB 端口或线缆

### 中文文件名乱码

使用 `-b` 参数进行 base64 编码传输：
```bash
hdc file send -b <本地路径> <设备路径>
```

### TCP 连接步骤

1. 先通过 USB 连接设备
2. 获取设备 IP 地址
3. 开启设备网络调试：`hdc tconn <设备IP>:8710`
4. 断开 USB，使用 `hdc list targets` 验证连接
