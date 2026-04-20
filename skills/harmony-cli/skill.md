---
name: harmony-cli
description: |
  HarmonyOS 命令行工具，用于设备调试、截图、安装应用、查看日志、性能分析、获取系统信息等。
  当用户说"截图"、"截屏"、"安装应用"、"卸载应用"、"查看日志"、"查看内存"、"查看CPU"、
  "性能分析"、"抓trace"、"查看设备信息"、"系统参数"等场景时触发。
  支持 hdc, hilog, hidumper, hitrace, hiperf, aa, bm, param, uitest 等工具。
  详细命令参数请查阅 reference/ 目录对应文档。
---

# HarmonyOS 命令行工具

提供 HarmonyOS 常用命令行工具的快速索引。

## 环境准备

```bash
# 检查 hdc 是否可用
where hdc        # Windows
which hdc        # Linux/Mac

# hdc 通常位于 DevEco Studio/sdk/default/openharmony/toolchains/
```

---

## Windows Git Bash 注意事项

**问题**：`hdc file recv` 使用相对路径（如 `./file.txt`）时，Git Bash 会把路径转换成 `C:/Program Files/Git/...`

**解决**：始终使用**绝对路径**或先 `cd` 到目标目录

```bash
# 错误示例（Git Bash 下）
hdc file recv /data/local/tmp/log.txt ./log.txt

# 正确示例
hdc file recv /data/local/tmp/log.txt /c/users/yourname/log.txt
# 或
cd /c/users/yourname
hdc file recv /data/local/tmp/log.txt ./log.txt
```

---

## 命令索引表

| 命令 | 功能 | 使用场景 |
|------|------|----------|
| **hdc** | 设备连接管理 | |
| `hdc list targets` | 列出已连接设备 | 检查设备是否正常连接 |
| `hdc tconn <ip>:8710` | TCP 连接设备 | 远程调试设备 |
| `hdc install <path>` | 安装应用 | 部署 HAP 到设备 |
| `hdc uninstall <pkg>` | 卸载应用 | 移除已安装应用 |
| `hdc file send <src> <dst>` | 发送文件到设备 | 传输配置文件/资源 |
| `hdc file recv <src> <dst>` | 从设备拉取文件 | 获取日志/截图 |
| `hdc hilog` | 查看设备日志 | 调试应用、查看崩溃日志 |
| `hdc shell <cmd>` | 执行 shell 命令 | 设备端操作 |
| `hdc smode` | 提权（root） | 需要 root 权限的操作 |
| `hdc bugreport <path>` | 获取完整故障报告 | 收集调试信息 |
| **hilog** | 日志查看 | |
| `hilog -L E` | 查看 Error 日志 | 快速定位错误 |
| `hilog -T <tag>` | 按标签过滤 | 查看特定模块日志 |
| `hilog -D <domain>` | 按 domain 过滤 | 查看特定域日志 |
| `hilog -x` | 非阻塞退出 | 保持日志同时退出 |
| **hidumper** | 系统信息 | |
| `hidumper --mem` | 整机内存 | 排查内存泄漏 |
| `hidumper --mem <pid>` | 进程内存 | 特定应用内存分析 |
| `hidumper --cpuusage` | CPU 使用率 | 性能监控 |
| `hidumper --services` | 服务列表 | 查看系统服务状态 |
| `hidumper --ps` | 进程列表 | 查看运行中的进程 |
| `hidumper --all -s <path>` | 导出所有信息 | 完整系统诊断 |
| **hitrace** | 性能跟踪 | |
| `hitrace -t <sec> <tags>` | 捕获 trace | 分析 UI 性能、卡顿分析 |
| `hitrace -l` | 列出可用标签 | 查看支持的 trace 标签 |
| **hiperf** | CPU 性能分析 | |
| `hiperf record -p <pid> -d <sec>` | 采样记录 | 函数热点分析 |
| `hiperf stat -p <pid> -d <sec>` | 统计 | CPU 计数器统计 |
| **aa** | Ability 管理 | |
| `aa start -b <pkg> -a <ability>` | 启动应用 | 启动指定 Ability |
| `aa force-stop <pkg>` | 强制停止 | 终止应用进程 |
| `aa dump -n <pkg>` | 打印信息 | 调试 Ability |
| **bm** | 包管理 | |
| `bm install -p <path>` | 安装应用 | 通过 bm 安装 |
| `bm uninstall -n <pkg>` | 卸载应用 | 通过 bm 卸载 |
| `bm dump -a` | 列出已安装应用 | 查看所有应用 |
| `bm dump -n <pkg>` | 应用详情 | 查看应用信息 |
| `bm clean -c -n <pkg>` | 清理缓存 | 清理应用缓存 |
| **param** | 系统参数 | |
| `param ls` | 列出系统参数 | 查看所有参数 |
| `param get <name>` | 获取参数值 | 查询指定参数 |
| `param set <name> <value>` | 设置参数 | 修改系统参数 |
| `param dump` | 导出参数 | 导出系统参数 |
| **uitest** | UI 测试 | |
| `uitest screenCap` | 屏幕截图 | 获取当前屏幕快照 |
| `uitest dumpLayout` | 布局导出 | 获取界面布局信息 |
| `uitest uiInput click <x> <y>` | 点击 | 模拟点击操作 |
| `uitest uiInput swipe` | 滑动 | 模拟滑动操作 |
| `uitest uiInput text` | 文本输入 | 模拟文本输入 |

---

## 快速执行命令

直接执行（使用 `Bash` 工具）：

```bash
# === 截图 ===
# 注意：Windows 下请用绝对路径替换 ./xxx
hdc shell "screenshot /data/local/tmp/screenshot.png"
hdc file recv /data/local/tmp/screenshot.png <本地绝对路径>/screenshot.png
hdc shell uitest screenCap -p /data/local/tmp/screen.png

# === 应用管理 ===
hdc install /local/app.hap
hdc uninstall com.example.app

# === 日志查看 ===
hdc hilog                              # 实时日志
hdc shell "hilog -L E -T MyApp"       # 错误日志+标签过滤

# === 系统信息 ===
hdc shell "hidumper --mem"            # 内存
hdc shell "hidumper --cpuusage"       # CPU

# === 性能分析 ===
hdc shell "hitrace -t 10 app graphic"  # 抓 trace 10秒
hdc shell "hiperf record -p <pid> -d 10 -o /data/local/tmp/perf.data"

# === 设备状态 ===
hdc list targets                       # 连接列表
hdc bugreport /data/local/tmp/bug.zip  # 故障报告

# === 系统参数 ===
hdc shell param ls
hdc shell param get <name>
hdc shell param set <name> <value>
```

---

## 详细文档索引

需要更详细的命令参数说明时，查阅：

| 文档 | 内容 |
|------|------|
| `reference/hdc.md` | hdc 完整命令、连接场景、错误码 |
| `reference/hilog.md` | hilog 日志级别、过滤选项、落盘任务 |
| `reference/hidumper.md` | 内存分析、JS堆、进程信息 |
| `reference/hitrace.md` | trace 标签、录制模式、时钟类型 |
| `reference/hiperf.md` | 采样事件、record/stat 命令 |
| `reference/aa-tool.md` | aa start/stop/dump/attach 命令 |
| `reference/bm-tool.md` | bm install/uninstall/dump/clean 命令 |
| `reference/param.md` | 系统参数查看/设置/等待 |
| `reference/uitest.md` | UI 测试：截图、布局、点击、滑动、输入 |

---

## 常用组合

```bash
# 1. 应用调试完整流程
hdc list targets                      # 确认连接
hdc install /local/app.hap           # 安装
hdc shell "hilog -T MyApp"           # 查看日志
hdc uninstall com.example.app         # 卸载

# 2. 性能问题排查
hdc shell "hidumper --cpuusage"      # CPU
hdc shell "hidumper --mem"           # 内存
hdc shell "hitrace -t 10 app ace ark graphic"  # trace
hdc shell "hiperf record -p <pid> -d 10 -o /data/local/tmp/perf.data"

# 3. 设备诊断
hdc bugreport /data/local/tmp/bug.zip
hdc shell "hidumper --all -s /data/local/tmp/dump.zip"
```
