# aa 工具 (Ability Assistant)

## 概述

aa（Ability Assistant）是用于启动应用和启动测试用例的工具，为开发者提供基本的应用调试和测试能力。

**前置条件**：需要先获取 hdc 工具并执行 `hdc shell`。

## 命令列表

| 命令 | 描述 |
|------|------|
| `help` | 帮助命令 |
| `start` | 启动应用组件（UIAbility/ServiceAbility） |
| `stop-service` | 停止应用组件 |
| `dump` | (deprecated) 打印应用组件信息 |
| `force-stop` | 通过 bundleName 强制停止进程 |
| `test` | 启动测试框架 |
| `attach` | 进入调试模式 |
| `detach` | 退出调试模式 |
| `appdebug` | 等待调试命令 |
| `process` | 应用调试/调优 |
| `send-memory-level` | onMemoryLevel 回调命令 |

## 帮助命令

```bash
aa help
```

## 启动命令 (start)

启动一个应用组件（UIAbility 或 ServiceAbility）。

### 语法

```bash
# 显式启动 Ability
aa start [-d <deviceId>] -a <abilityName> -b <bundleName> [-m <moduleName>]

# 隐式启动 Ability
aa start [-d <deviceId>] -U <URI> [-A <action>] [-t <type>] [-e <entity>]
```

### 参数

| 参数 | 说明 |
|------|------|
| `-d <deviceId>` | 设备 ID（可选） |
| `-a <abilityName>` | Ability 名称 |
| `-b <bundleName>` | 包名 |
| `-m <moduleName>` | 模块名（可选） |
| `-U <URI>` | URI（隐式启动时使用） |
| `-A <action>` | Action |
| `-t <type>` | 类型 |
| `-e <entity>` | Entity |
| `-c` | 跨端迁移场景 |
| `-D` | 调试模式 |
| `-E` | 显示详细异常信息 |
| `-R` | 开启多线程错误检测 |
| `-S` | 进入应用沙箱 |
| `-W` | 测量 UIAbility 启动耗时 |
| `--pi <key> <value>` | 整型参数 |
| `--pb <key> <bool>` | 布尔参数 |
| `--ps <key> <value>` | 字符串参数 |
| `--wl/-wt/-wh/-ww` | 窗口位置和大小（仅调试签名） |

### 示例

```bash
# 隐式启动浏览器并跳转页面
aa start -A ohos.want.action.viewData -U https://www.example.com

# 带参数启动
aa start -U myscheme://www.test.com:8080/path --pi paramNumber 1 --pb paramBoolean true --ps paramString teststring

# 测量启动耗时
aa start -b com.example.app -a EntryAbility -W
```

### 返回值

成功：`start ability successfully.`
失败：`error: failed to start ability.`

### 错误码

| 错误码 | 说明 |
|--------|------|
| 10103001 | 目标 Ability 可见性校验失败 |
| 10104001 | 指定的 Ability 不存在 |
| 10105001 | Ability 服务连接失败 |
| 10100101 | 获取应用信息失败 |
| 10100102 | 无法拉起 UIExtensionAbility |
| 10103101 | 隐式启动未查找到匹配应用 |
| 10106101 | 上一个 Ability 未启动完成，缓存等待 |
| 10106102 | 设备处于锁屏状态 |
| 10106103 | 目标应用为到期众测应用 |
| 10106105 | 目标应用被管控 |
| 10106106 | 目标应用被 EDM 管控 |

## 停止命令 (stop-service)

```bash
aa stop-service -b <bundleName> -a <abilityName>
```

## 强制停止 (force-stop)

```bash
aa force-stop <bundleName>
```

## 测试命令 (test)

```bash
aa test -b <bundleName> [-p <testPath>]
```

## 调试命令

```bash
# 进入调试模式
aa attach -b <bundleName>

# 退出调试模式
aa detach -b <bundleName>

# 等待调试
aa appdebug -s -b <bundleName>  # 设置等待调试
aa appdebug -c -b <bundleName>  # 取消等待调试
aa appdebug -l                   # 列出等待调试的应用
```

## 应用调试/调优 (process)

```bash
aa process -b <bundleName> -a <abilityName> -p <perf-cmd>
```

## onMemoryLevel 回调 (send-memory-level)

```bash
aa send-memory-level -p <pid> -l <level>
```
