---
name: harmony-cli
description: |
  HarmonyOS 命令行工具，用于设备调试、编译构建、截图、安装应用、查看日志、性能分析、获取系统信息等。
  当用户说"截图"、"截屏"、"安装应用"、"卸载应用"、"查看日志"、"查看内存"、"查看CPU"、
  "性能分析"、"抓trace"、"查看设备信息"、"系统参数"、"编译"、"构建"、"打包"、
  "hvigorw"、"assembleHap"、"assembleHar"等场景时触发。
  支持 hdc, hvigorw, hilog, hidumper, hitrace, hiperf, aa, bm, param, uitest 等工具。
  详细命令参数请查阅 reference/ 目录对应文档。
---

# HarmonyOS 命令行工具

提供 HarmonyOS 常用命令行工具的快速索引。

## 环境准备

### 设置 DEVECO_SDK_HOME / DEVECO_HOME / PATH

**在使用任何工具前先执行此步骤。** 优先使用环境变量，若无则从 `hdc` 路径推导。

hdc 位于 `$DEVECO_SDK_HOME/default/openharmony/toolchains/hdc`，可用以下命令推导：

| Shell | 设置命令 |
|-------|---------|
| **PowerShell** | `if (-not $env:DEVECO_SDK_HOME) { $hdcPath = (Get-Command hdc).Source; $env:DEVECO_SDK_HOME = (Split-Path (Split-Path (Split-Path $hdcPath -Parent) -Parent) -Parent) }; $env:DEVECO_HOME = "$env:DEVECO_SDK_HOME\.."; $env:PATH = "$env:DEVECO_HOME\tools\node;$env:DEVECO_HOME\tools\ohpm\bin;$env:DEVECO_HOME\tools\hvigor\bin;$env:PATH"` |
| **Git Bash** | `export DEVECO_SDK_HOME=${DEVECO_SDK_HOME:-$(dirname $(dirname $(which hdc))))} && export DEVECO_HOME=$DEVECO_SDK_HOME/.. && export PATH=$DEVECO_HOME/tools/node:$DEVECO_HOME/tools/ohpm/bin:$DEVECO_HOME/tools/hvigor/bin:$PATH` |
| **CMD** | `if "%DEVECO_SDK_HOME%"=="" for /f "delims=" %%i in ('where hdc') do set "DEVECO_SDK_HOME=%%~dpi..\.." && set DEVECO_HOME=%DEVECO_SDK_HOME%.. && set PATH=%DEVECO_HOME%\tools\node;%DEVECO_HOME%\tools\ohpm\bin;%DEVECO_HOME%\tools\hvigor\bin;%PATH%` |

> **重要**：不要硬编码任何路径（如 `C:\Program Files\...`）。所有路径必须通过环境变量或命令推导获取。

### 检查工具是否可用

```bash
where hdc        # Windows CMD
Get-Command hdc  # PowerShell
which hdc        # Git Bash / Linux / Mac
```

---

## 命令执行规则

### hdc shell 引号规则

**所有 `hdc shell` 命令必须用引号包裹**，防止当前 shell 错误处理特殊字符：

```bash
# 正确写法
hdc shell "hilog -L E"
hdc shell 'hidumper --mem'

# 错误写法（当前 shell 会尝试解析）
hdc shell hilog -L E          # 会失败
```

### 单引号、双引号、转义符规则

#### 双引号 `"..."`（内层）

| 特殊字符 | 行为 |
|---------|------|
| `\$` | 转义，美元符不展开 |
| `\\` | 转义反斜杠 |
| `` \` `` | 转义反引号 |
| `\"` | 转义双引号本身 |
| `\$` | 转义美元符 |
| `\n`, `\t` | 转义换行、制表 |

```bash
# 示例
hdc shell "param get \$var"           # 防止变量展开
hdc shell "echo \"hello\""             # 输出带引号的字符串
hdc shell "ls /data | grep \"app\""   # grep 模式含引号
```

#### 单引号 `'...'`（最简单）

单引号内**所有字符都不解释**，包括 `\`、`$`、反引号 `"` 等。

| 特殊字符 | 行为 |
|---------|------|
| 所有字符 | 原样保留 |
| `''` | 单引号本身无法在单引号内出现 |

```bash
# 示例 - 单引号最安全
hdc shell 'param get sys.bootevent'   # 原样传递
hdc shell 'hilog -T $TAG'             # $TAG 不会展开
hdc shell 'echo "hello"'              # 引号原样传递
```

#### 连续单引号技巧

需要在单引号内插入单引号时，用 `'\''`（结束单引号 + 转义单引号 + 开始单引号）：

```bash
# 输出: hello'world
hdc shell 'echo hello'\''world'

# 命令含单引号的场景
hdc shell 'param set key value'\''s'
```

#### 反斜杠转义 `\`

单个字符前加 `\` 表示该字符不解释：

```bash
# 示例
hdc shell "ls /data\|grep app"       # 管道符不展开
hdc shell "echo \$PATH"               # 变量不展开
hdc shell "echo \\n"                  # 输出 \n 原样
```

### 不同 Shell 的特殊处理

| Shell | 推荐引号 | 注意事项 |
|-------|---------|---------|
| **Git Bash** | 双引号 `"..."` | `$` `` ` `` `\` 需要转义；`` ` `` 无法转义，用单引号 |
| **PowerShell** | 单引号 `'...'` | `$` 在单引号内不展开；双引号内 `$` 会展开 |
| **CMD** | 双引号 `"..."` | `^` 是转义符；`%` 是变量符需 `%%` 转义 |

```bash
# === Git Bash ===
hdc shell "hilog -T \$MY_TAG"                    # 变量不展开
hdc shell 'param set key value'                  # 单引号最安全
hdc shell "echo hello\\n"                         # 输出 hello\n

# === PowerShell ===
hdc shell 'hilog -T $MY_TAG'                     # 单引号内 $ 不展开
hdc shell "param set key \$val"                   # 双引号内 \$ 防止展开
hdc shell 'ls /data | grep "app"'                # 双引号管道OK

# === CMD ===
hdc shell "hilog -T mytag"                        # 基本直接用
hdc shell "echo %%var%%"                          # 变量需双 %
```

### 常见错误与修正

| 错误写法 | 正确写法 | 原因 |
|---------|---------|------|
| `hdc shell "ls /data|grep app"` | `hdc shell "ls /data \| grep app"` | 管道符被当前 shell 解析 |
| `hdc shell "param get $key"` | `hdc shell 'param get $key'` 或 `hdc shell "param get \$key"` | 变量在本地展开 |
| `hdc shell 'it's not found'` | `hdc shell 'it'\''s not found'` 或 `hdc shell "it'S not found"` | 单引号内无法直接放单引号 |
| `hdc shell "echo "$var""` | `hdc shell 'echo '$var''` 或 `hdc shell "echo \$var"` | 嵌套引号问题 |

### hdc shell 命令限制

**可用命令：** `ls`, `cd`, `cat`, `grep`, `awk`, `sed`, `find`, `ps`, `top`, `kill`, `mkdir`, `rm`, `cp`, `mv`, `chmod`, `pwd`, `echo`, `test` 等基础命令

**不可用：** `python`, `node`, `bash脚本`, `管道组合`（需要用引号包裹整个命令让设备端执行）

```bash
# 错误 - 设备端没有 python
hdc shell "python /data/local/tmp/script.py"

# 正确 - 使用设备端已有命令
hdc shell "cat /data/local/tmp/log.txt | grep error"  # 设备端支持管道
```

### Windows 文件传输

`hdc file send/recv` 在 Windows 下需要根据当前 shell 选择正确执行方式：

#### Git Bash 环境

Git Bash 会错误转换 hdc 的设备路径（如 `/data/...` 被转换成 `C:/Program Files/Git/...`）。

```bash
# 错误 - Git Bash 会转换路径
hdc file recv /data/local/tmp/screen.png ./screen.png
# 错误: path:C:/Program Files/Git/data/local/tmp/screen.png

# 正确 - 使用 cmd //c 执行（推荐）
cmd //c "hdc file recv /data/local/tmp/screen.png C:\temp\screen.png"

# 也可以使用 PowerShell（但需要处理执行策略）
powershell -ExecutionPolicy Bypass -Command "hdc file recv /data/local/tmp/screen.png C:\temp\screen.png"
```

#### PowerShell 环境

PowerShell 环境下也可能遇到执行策略问题：

```bash
# 推荐使用 cmd //c
cmd //c "hdc file recv /data/local/tmp/screen.png C:\temp\screen.png"

# 或强制绕过执行策略
powershell -ExecutionPolicy Bypass -Command "hdc file recv /data/local/tmp/screen.png C:\temp\screen.png"
```

#### CMD 环境

CMD 环境可以直接使用：

```bash
cmd /c "hdc file recv /data/local/tmp\screen.png .\screen.png"
```

---

## 命令索引表

| 命令 | 功能 | 使用场景 |
|------|------|----------|
| **hdc** | 设备连接管理 | |
| `hdc list targets` | 列出已连接设备 | 检查设备是否正常连接 |
| `hdc tconn <ip>:8710` | TCP 连接设备 | 远程调试设备 |
| `hdc install <path>` | 安装应用 | 部署 HAP 到设备 |
| `hdc uninstall -k <pkg>` | 卸载应用 | 移除已安装应用（-k 保留数据） |
| `hdc file send <src> <dst>` | 发送文件到设备 | 传输配置文件/资源 |
| `hdc file recv <src> <dst>` | 从设备拉取文件 | 获取日志/截图（本地用绝对路径） |
| `hdc hilog` | 查看设备日志 | 调试应用、查看崩溃日志 |
| `hdc shell <cmd>` | 执行 shell 命令 | 设备端操作（必须引号包裹） |
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
| `ps -ef` | 进程列表 | 查看运行中的进程 |
| `hidumper --all -s <path>` | 导出所有信息 | 完整系统诊断 |
| **hitrace** | 性能跟踪 | |
| `hitrace -t <sec> <tags>` | 捕获 trace | 分析 UI 性能、卡顿分析 |
| `hitrace -l` | 列出可用标签 | 查看支持的 trace 标签 |
| **hiperf** | CPU 性能分析 | |
| `hiperf record -p <pid> -d <sec>` | 采样记录 | 函数热点分析 |
| `hiperf stat -p <pid> -d <sec>` | 统计 | CPU 计数器统计 |
| **aa** | Ability 管理 | |
| `aa start -b <pkg> -a <ability>` | 启动应用 | 需先查询 Ability 名称 |
| `aa force-stop <pkg>` | 强制停止 | 终止应用进程 |
| `aa dump -n <pkg>` | 查询 Ability | 查看应用所有 Ability |
| `aa dump -a` | 查询所有 Ability | 列出设备上所有 Ability |
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
| `uitest screenCap -p <path>` | 屏幕截图 | 获取当前屏幕快照 |
| `uitest dumpLayout -p <path>` | 布局导出 | 获取界面布局信息 |
| `uitest uiInput click <x> <y>` | 点击 | 模拟点击操作 |
| `uitest uiInput swipe` | 滑动 | 模拟滑动操作 |
| `uitest uiInput text <content>` | 文本输入 | 模拟文本输入 |
| **hvigorw** | 构建工具 | |
| `hvigorw tasks` | 查看所有任务 | 查看模块可用构建任务 |
| `hvigorw --mode module -p product=default -p module={module_name}@default assembleHap --analyze=normal --parallel --incremental --no-daemon` | 构建 HAP | entry 模块构建 |
| `hvigorw --mode module -p product=default -p module={module_name}@default assembleHar --analyze=normal --parallel --incremental --no-daemon` | 构建 HAR | har 模块构建 |
| `hvigorw --stop-daemon-all` | 停止 daemon | 停止所有 hvigor daemon |

---

## 快速执行命令

### 截图

```bash
# 截图（设备端）
hdc shell "uitest screenCap -p /data/local/tmp/screen.png"

# 拉取到本地（Windows 下使用 cmd //c）
cmd //c "hdc file recv /data/local/tmp/screen.png C:\temp\screen.png"
```

### 应用启动

**必须先查询 Ability 名称**，否则会启动失败：

```bash
# 1. 查询应用的所有 Ability
hdc shell "bm dump -n com.example.app" 2>&1 | grep '"name":'
# 或
hdc shell "aa dump -a" 2>&1 | grep -A10 "com.example.app"

# 2. 根据查询结果，使用正确的 ability 名称启动
hdc shell "aa start -b com.example.app -a MainAbility"
```

**常见错误**：`fail: unknown option` 或启动无反应，通常是 ability 名称不正确。

### 日志查看

```bash
hdc hilog                                    # 实时日志（阻塞）
hdc shell "hilog -L E -T MyApp"             # 错误+标签过滤
hdc shell "hilog -x -L E"                    # 非阻塞查看错误
```

### 系统信息

```bash
hdc shell "hidumper --mem"                   # 整机内存
hdc shell "hidumper --cpuusage"               # CPU 使用率
hdc shell "hidumper --services"              # 服务列表
hdc shell "ps -ef"                           # 进程列表
```

### 性能分析

```bash
hdc shell "hitrace -t 10 -b 204800 app graphic"   # 抓 trace 10秒
hdc shell "hiperf record -p <pid> -d 10 -o /data/local/tmp/perf.data"
hdc shell "hiperf stat -p <pid> -d 10"
```

### 设备状态

```bash
hdc list targets
hdc bugreport /data/local/tmp/bug.zip
```

### 系统参数

```bash
hdc shell "param ls"
hdc shell "param get sys.bootevent"
hdc shell "param set debug.test 1"
```

### 构建（hvigorw）

```bash
# 构建 entry 模块（HAP）
hvigorw --mode module -p product=default -p module={module_name}@default assembleHap --analyze=normal --parallel --incremental --no-daemon

# 构建 har 模块
hvigorw --mode module -p product=default -p module={module_name}@default assembleHar --analyze=normal --parallel --incremental --no-daemon

# 查看所有可用任务
hvigorw tasks

# 停止所有 daemon（构建卡住时使用）
hvigorw --stop-daemon-all
```

---

## 详细文档索引

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
| `reference/hvigor.md` | hvigor 构建工具：环境配置、构建命令、常用参数 |
