# bm 工具 (Bundle Manager)

## 概述

bm 是 HarmonyOS 的包管理工具，用于应用的安装、卸载、查询等操作。

**前置条件**：需要先获取 hdc 工具并执行 `hdc shell`。

## 命令列表

| 命令 | 描述 |
|------|------|
| `help` | 帮助命令 |
| `install` | 安装应用 |
| `uninstall` | 卸载应用 |
| `dump` | 查询应用信息 |
| `clean` | 清理应用数据 |
| `get` | 获取设备 UDID |
| `quickfix` | 快速修复命令 |
| `dump-shared` | 查询共享库 |
| `dump-dependencies` | 查询共享库依赖 |
| `compile` | AOT 编译命令 |
| `copy-ap` | 拷贝 AP 文件 |
| `dump-overlay` | 查询 overlay 应用信息 |
| `install-plugin` | 安装插件 |
| `uninstall-plugin` | 卸载插件 |

## 安装命令 (install)

```bash
bm install [-h] [-p filePath] [-r] [-w waitingTime] [-s hspDirPath] [-u userId]
```

| 参数 | 说明 |
|------|------|
| `-p` | HAP 包路径 |
| `-r` | 覆盖安装 |
| `-w` | 等待时间（秒） |
| `-s` | HSP 共享库路径 |
| `-u` | 用户 ID |

### 示例

```bash
# 安装 HAP
bm install -p /data/local/tmp/ohos.app.hap

# 覆盖安装
bm install -p /data/local/tmp/ohos.app.hap -r

# 指定用户安装
bm install -p /data/local/tmp/ohos.app.hap -u 100

# 安装共享库
bm install -s xxx.hsp

# 同时安装应用和依赖的共享库
bm install -p aaa.hap -s xxx.hsp yyy.hsp

# 等待安装完成
bm install -p /data/local/tmp/ohos.app.hap -w 180
```

## 卸载命令 (uninstall)

```bash
bm uninstall [-h] [-n bundleName] [-m moduleName] [-k] [-s] [-v versionCode] [-u userId]
```

| 参数 | 说明 |
|------|------|
| `-n` | 包名 |
| `-m` | 模块名 |
| `-k` | 保留用户数据 |
| `-s` | 卸载共享库 |
| `-v` | 指定版本 |

### 示例

```bash
# 卸载应用
bm uninstall -n com.ohos.app

# 指定用户卸载
bm uninstall -n com.ohos.app -u 100

# 卸载模块
bm uninstall -n com.ohos.app -m entry

# 卸载共享库
bm uninstall -n com.ohos.example -s

# 卸载但保留数据
bm uninstall -n com.ohos.app -k
```

## 查询命令 (dump)

```bash
bm dump [-h] [-a] [-g] [-n bundleName] [-s] [-l] [-u userId]
```

| 参数 | 说明 |
|------|------|
| `-a` | 显示所有已安装应用 |
| `-g` | 查询调试签名的应用 |
| `-n` | 包名 |
| `-s` | 查询快捷方式 |
| `-l` | 查询应用名称 |

### 示例

```bash
# 显示所有已安装应用
bm dump -a

# 查询调试签名应用
bm dump -g

# 查询应用详情
bm dump -n com.ohos.app

# 查询应用名称
bm dump -n com.ohos.app -l

# 查询快捷方式
bm dump -s -n com.ohos.app
```

## 清理命令 (clean)

```bash
bm clean [-h] [-c] [-d] [-n bundleName] [-u userId]
```

| 参数 | 说明 |
|------|------|
| `-c` | 清理缓存 |
| `-d` | 清理用户数据 |
| `-n` | 包名 |

### 示例

```bash
# 清理缓存
bm clean -c -n com.ohos.app

# 清理用户数据
bm clean -d -n com.ohos.app
```

## 获取 UDID

```bash
bm get -u
# 返回: udid of current device is :23CADE0C
```

## 快速修复 (quickfix)

```bash
# 查询补丁信息
bm quickfix -q -b com.ohos.app

# 安装补丁
bm quickfix -a -f /data/app/

# 卸载补丁
bm quickfix -r -b com.ohos.app
```

## 共享库查询 (dump-shared)

```bash
# 显示所有共享库
bm dump-shared -a

# 显示共享库详情
bm dump-shared -n com.ohos.lib
```

## 依赖查询 (dump-dependencies)

```bash
bm dump-dependencies -n com.ohos.app -m entry
```

## 编译命令 (compile)

```bash
bm compile [-m mode] [-r bundleName]
```

| 参数 | 说明 |
|------|------|
| `-m` | 编译模式（partial/full） |

```bash
bm compile -m partial com.example.myapplication
```

## 错误码

| 错误码 | 说明 |
|--------|------|
| 301 | 系统账号不存在 |
| 304 | 当前系统账号没有安装 HAP 包 |
| 9568257 | 签名文件 PKcs7 校验失败 |
| 9568258 | releaseType 不匹配 |
| 9568259 | 解析配置文件缺少字段 |
| 9568260 | 安装内部错误 |
| 9568267 | entry 模块已存在 |
| 9568268 | 安装状态错误 |
| 9568269 | 文件路径无效 |
| 9568270 | 安装包名称不正确 |
| 9568276 | 应用已存在 |
| 9568286 | 签名证书类型不匹配 |
| 9568288 | 磁盘空间不足 |
| 9568289 | 权限请求失败 |
| 9568319 | 签名文件异常 |
| 9568320 | 签名文件不存在 |
| 9568321 | 签名文件解析失败 |
| 9568322 | 应用来源不可信 |
| 9568323 | 签名摘要验证失败 |
| 9568324 | 签名完整性校验失败 |
