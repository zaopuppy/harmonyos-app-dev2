# hvigor 构建工具

HarmonyOS 项目构建工具，基于 Hvigor。

## 环境准备

### 查找 hvigorw

```bash
# Windows CMD
where hvigorw

# PowerShell
Get-Command hvigorw

# Git Bash / Linux / Mac
which hvigorw
```

### 找不到时设置 PATH

`DEVECO_SDK_HOME` 指向 SDK 根目录（如 `C:\Program Files\Huawei\DevEco Studio\sdk`）。

| Shell | 设置命令 |
|-------|---------|
| **Git Bash** | `export DEVECO_HOME=$DEVECO_SDK_HOME/.. && export PATH=$DEVECO_HOME/tools/node:$DEVECO_HOME/tools/ohpm/bin:$DEVECO_HOME/tools/hvigor/bin:$PATH` |
| **PowerShell** | `$env:DEVECO_HOME="$env:DEVECO_SDK_HOME\.."; $env:PATH="$env:DEVECO_HOME\tools\node;$env:DEVECO_HOME\tools\ohpm\bin;$env:DEVECO_HOME\tools\hvigor\bin;$env:PATH"` |
| **CMD** | `set DEVECO_HOME=%DEVECO_SDK_HOME%^.. & set PATH=%DEVECO_HOME%\tools\node;%DEVECO_HOME%\tools\ohpm\bin;%DEVECO_HOME%\tools\hvigor\bin;%PATH%` |

## 帮助信息

```
Usage:  hvigorw [taskNames...] <options...>

Options:
  -v, --version                      Shows the version of Hvigor.
  -e, --error                        Sets the log level to error.
  -w, --warn                         Sets the log level to warn.
  -i, --info                         Sets the log level to info.
  -d, --debug                        Sets the log level to debug.
  -c, --config <config>              Sets properties in the hvigor-config.json5 file.
  -p, --prop <value>                 Defines extra properties.
  -m, --mode <string>                Sets the mode in which the command is executed.
  -s, --sync                         Syncs the information in plugin for other platforms.
  --node-home, <string>              Sets the Node.js location.
  --stop-daemon                      Stops the current project's daemon process.
  --stop-daemon-all                  Stops all projects' daemon process.
  --status-daemon                    Shows the daemon process status of the current project.
  --verbose-analyze                  Enables detailed mode for build analysis.
  --watch                            Enables watch mode.
  --hot-compile                      HotReload watch mode to compile.
  --hot-reload-build                 HotReload build
  --max-old-space-size <integer>     Sets the maximum memory size of V8's old memory section.
  --max-semi-space-size <integer>    Sets the maximum memory size of V8's new space memory section.
  --Xmx <integer>                    Sets the maximum JVM heap size, in MB.
  --optimization-strategy <string>   Sets the optimization strategy: memory, performance.
  --enable-build-script-type-check   Enables the build script hvigorfile.ts type check.
  --stacktrace                       Enables the printing of stack traces.
  --no-stacktrace                    Disables the printing of stack traces.
  --type-check                       Enables the build script hvigorfile.ts type check.
  --no-type-check                    Disables the build script hvigorfile.ts type check.
  --parallel                         Enables parallel building mode.
  --no-parallel                      Disables parallel building mode.
  --incremental                      Enables incremental building mode.
  --no-incremental                   Disables incremental building mode.
  --daemon                           Enables building with daemon process.
  --no-daemon                        Disables building with daemon process.
  --generate-build-profile           Enables the generation of BuildProfile.ets files.
  --no-generate-build-profile        Disables the generation of BuildProfile.ets files.
  --analyze                          Enables build analysis.
  --no-analyze                       Disables build analysis.
  --analyze=<analysisMode>           Sets the build analysis mode: normal, advanced, false, ultrafine.
  -h, --help                         Displays help information.

Commands:
  version                            Shows the version of Hvigor.
  tasks                              Shows all available tasks of specific modules.
  taskTree                           Shows all available task trees of specific modules.
  prune                              Cleans up Hvigor cache files and removes unreferenced packages from store.
  collectCoverage                    Generates coverage statistics reports based on instrumentation test data.
```

## 构建示例

### 构建 entry 模块（HAP）

```bash
hvigorw --mode module -p product=default -p module={module_name}@default assembleHap --analyze=normal --parallel --incremental --no-daemon
```

### 构建 har 模块

```bash
hvigorw --mode module -p product=default -p module={module_name}@default assembleHar --analyze=normal --parallel --incremental --no-daemon
```

### 查看所有任务

```bash
hvigorw tasks
```

### 停止所有 daemon

```bash
hvigorw --stop-daemon-all
```

## 常用参数说明

| 参数 | 说明 |
|------|------|
| `--mode module` | 以模块模式构建（用于单模块构建） |
| `-p product=default` | 指定产品为 default |
| `-p module=xxx@default` | 指定模块名，`@default` 表示默认 variant |
| `--analyze=normal` | 启用构建分析（normal/advanced/false/ultrafine） |
| `--parallel` | 启用并行构建 |
| `--incremental` | 启用增量构建（加快构建速度） |
| `--no-daemon` | 不使用后台 daemon（推荐，避免长时间占用大量内存） |
| `--optimization-strategy memory` | 内存优化模式（适合内存较小的机器） |
| `--optimization-strategy performance` | 性能优先模式 |
| `-p product=phone` | 指定产品为 phone |
| `-p buildMode=debug` | 指定调试模式 |
| `-p buildMode=release` | 指定发布模式 |