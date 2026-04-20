# aa 工具 (Ability Assistant)

## 概述

aa（Ability Assistant）是用于启动应用和启动测试用例的工具，为开发者提供基本的应用调试和测试能力。

## 帮助信息

```bash
aa help
aa start -h
aa <command> -h
```

## 命令列表

| 命令 | 说明 |
|------|------|
| `help` | 显示帮助 |
| `start` | 启动应用组件 |
| `stop-service` | 停止服务 |
| `dump` | 打印应用组件信息 |
| `force-stop` | 强制停止进程 |
| `attach` | 进入调试模式 |
| `detach` | 退出调试模式 |
| `test` | 启动测试框架 |
| `appdebug` | 等待调试命令 |
| `process` | 应用调试/调优 |
| `send-memory-level` | 内存级别回调 |

## start 命令 - 启动应用

### 语法

```bash
aa start [options]
```

### 显式启动

```bash
aa start -a <ability-name> -b <bundle-name> [-m <module-name>]
```

### 隐式启动

```bash
aa start [-U <URI>] [-A <action>] [-t <type>] [-e <entity>]
```

### 选项

| 选项 | 说明 |
|------|------|
| `-h, --help` | 显示帮助 |
| `-d <device-id>` | 设备 ID |
| `-a <ability-name>` | Ability 名称 |
| `-b <bundle-name>` | 包名 |
| `-m <module-name>` | 模块名 |
| `-p <perf-cmd>` | 性能命令 |
| `-D` | 调试模式 |
| `-E` | 显示详细异常 |
| `-S` | 进入应用沙箱 |
| `-N` | 支持多实例 |
| `-C` | 跨设备迁移 |
| `-R` | 开启多线程错误检测 |
| `-c` | 跨端迁移场景 |
| `-s <mode>` | 窗口模式（仅 FA 模式） |
| `-W` | 测量 UIAbility 启动耗时 |
| `-A <action-name>` | Action 名称（隐式启动） |
| `-U <URI>` | URI（隐式启动） |
| `-e <entity>` | Entity |
| `-t <mime-type>` | MIME 类型 |
| `--ps <key> <value>` | 字符串参数 |
| `--pi <key> <value>` | 整型参数 |
| `--pb <key> <value>` | 布尔参数 |
| `--psn <key>` | 字符串参数（无值） |
| `--wl <left>` | 窗口左坐标（仅调试签名） |
| `--wt <top>` | 窗口上坐标（仅调试签名） |
| `--wh <height>` | 窗口高度（仅调试签名） |
| `--ww <width>` | 窗口宽度（仅调试签名） |

### 示例

```bash
# 启动 EntryAbility
aa start -b com.example.app -a EntryAbility

# 启动带模块名
aa start -b com.example.app -a EntryAbility -m entry

# 测量启动耗时
aa start -b com.example.app -a EntryAbility -W

# 调试模式启动
aa start -b com.example.app -a EntryAbility -D

# 隐式启动浏览器
aa start -A ohos.want.action.viewData -U https://www.example.com

# 带参数启动
aa start -U myscheme://www.test.com:8080/path \
  --pi paramNumber 1 \
  --pb paramBoolean true \
  --ps paramString teststring

# 指定窗口位置和大小
aa start -b com.example.app -a EntryAbility \
  --wl 100 --wt 100 --wh 500 --ww 500
```

### 返回值

- 成功：`start ability successfully.`
- 失败：`error: failed to start ability.`

### 错误码

| 错误码 | 说明 |
|--------|------|
| 10103001 | Ability 可见性校验失败 |
| 10104001 | Ability 不存在 |
| 10105001 | Ability 服务连接失败 |
| 10100101 | 获取应用信息失败 |
| 10100102 | 无法拉起 UIExtensionAbility |
| 10103101 | 隐式启动未找到匹配应用 |
| 10106101 | 上一个 Ability 未启动完成 |
| 10106102 | 设备处于锁屏状态 |
| 10106103 | 目标应用为到期众测应用 |
| 10106105 | 目标应用被管控 |
| 10106106 | 目标应用被 EDM 管控 |

## stop-service 命令

```bash
aa stop-service -b <bundle-name> -a <ability-name>
```

## force-stop 命令

```bash
# 按包名强制停止
aa force-stop <bundle-name>

# 示例
aa force-stop com.example.app
```

## dump 命令

```bash
# 打印应用信息
aa dump -n <bundle-name>
```

## attach 命令 - 调试模式

```bash
# 进入调试模式
aa attach -b <bundle-name>

# 退出调试模式
aa detach -b <bundle-name>
```

## appdebug 命令 - 等待调试

```bash
# 设置等待调试
aa appdebug -s -b <bundle-name>

# 取消等待调试
aa appdebug -c -b <bundle-name>

# 列出等待调试的应用
aa appdebug -l
```

## test 命令 - 测试框架

```bash
aa test -b <bundle-name> [-p <testPath>]
```

## process 命令 - 调试/调优

```bash
aa process -b <bundle-name> -a <ability-name> -p <perf-cmd>
```

## send-memory-level 命令

```bash
aa send-memory-level -p <pid> -l <level>
```
