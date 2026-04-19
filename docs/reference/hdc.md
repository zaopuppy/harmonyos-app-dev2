# hdc (HarmonyOS Device Connector)

## 概述

hdc（HarmonyOS Device Connector）是提供给开发人员的命令行调试工具，用于与设备进行交互调试、数据传输、日志查看以及应用安装等操作。该工具支持在 Windows/Linux/MacOS 系统上运行。

### 组件架构

hdc 包含三部分：
- **客户端（client）**：运行在电脑端的进程，执行 hdc 命令时启动，命令结束后自动退出
- **服务器（server）**：运行在电脑端的后台服务进程，管理客户端和设备端守护进程之间的数据交互
- **守护程序（daemon）**：运行在调试设备端的进程，响应服务器发来的请求

默认监听电脑端的 8710 端口，可通过环境变量 `OHOS_HDC_SERVER_PORT` 自定义（范围 1~65535）。

## 环境准备

### 获取方式

1. **通过 DevEco Studio**：hdc 默认安装在 `DevEco Studio/sdk/default/openharmony/toolchains` 路径下
2. **通过 Command Line Tools**：安装在 `Command Line Tools/sdk/default/openharmony/toolchains` 路径下

### 环境变量配置

**Windows**：将 hdc.exe 所在目录添加到系统环境变量 Path，重启电脑。

**Linux/MacOS**：
```bash
# 根据 shell 类型选择
vi ~/.bashrc  # 如果输出为 bin/bash
vi ~/.zshrc   # 如果输出为 /bin/zsh

# 添加 PATH
export PATH={DevEco Studio}/sdk/default/openharmony/toolchains:$PATH

# 使配置生效
source ~/.bashrc  # 或 source ~/.zshrc
```

## 连接场景

### USB 连接

1. 使用 USB 线连接设备
2. 在设备设置 > 系统 > 开发者选项中开启 USB 调试

### TCP 连接

1. 先通过 USB 连接设备
2. 获取设备 IP 地址
3. 开启设备网络调试： `hdc tconn <设备IP>:8710`
4. 断开 USB，使用 `hdc list targets` 验证连接

### 远程连接

支持通过 `-t` 参数指定目标设备。

## 命令列表

### 查询命令

| 命令 | 说明 |
|------|------|
| `hdc list targets` | 查询已连接的设备 |
| `hdc -t <设备ID> list targets` | 连接指定设备 |
| `hdc wait` | 等待设备正常连接 |
| `hdc -v` | 查询 hdc 版本号 |

### 应用管理

| 命令 | 说明 |
|------|------|
| `hdc install <hap路径>` | 安装应用 |
| `hdc uninstall <包名>` | 卸载应用 |

### 文件传输

| 命令 | 说明 |
|------|------|
| `hdc file send <本地路径> <设备路径>` | 发送文件到设备 |
| `hdc file recv <设备路径> <本地路径>` | 从设备接收文件 |

### Shell 命令

| 命令 | 说明 |
|------|------|
| `hdc shell` | 进入交互模式 |
| `hdc shell <命令>` | 执行单条命令 |

### 端口转发

| 命令 | 说明 |
|------|------|
| `hdc fport list` | 查询端口转发任务 |
| `hdc fport lrp <本机端口> <设备端口>` | 创建正向转发 |
| `hdc fport rlp <设备端口> <本机端口>` | 创建反向转发 |
| `hdc fport delete <任务ID>` | 删除端口转发 |

### 服务进程管理

| 命令 | 说明 |
|------|------|
| `hdc start` | 启动服务 |
| `hdc kill` | 终止服务 |

### 设备操作

| 命令 | 说明 |
|------|------|
| `hdc hilog` | 打印设备日志 |
| `hdc shell ps -p` | 显示应用进程 PID |
| `hdc shell pidof <应用名>` | 获取应用 PID |
| `hdc reboot` | 重启设备 |

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

### hdc 无法运行

1. 确认环境变量已配置
2. 重启电脑使环境变量生效
3. 检查 hdc 版本与设备系统配套

### 中文文件名乱码

使用 `-b` 参数进行 base64 编码传输：
```bash
hdc file send -b <本地路径> <设备路径>
```
