# uitest UI 测试工具

## 概述

uitest 是 HarmonyOS 的 UI 自动化测试工具，支持屏幕截图、布局导出、UI 操作注入等功能。

## 帮助信息

```bash
hdc shell uitest --help
hdc shell uitest help
```

## 命令列表

| 命令 | 说明 |
|------|------|
| `screenCap` | 屏幕截图 |
| `dumpLayout` | 获取布局信息 |
| `start-daemon` | 启动测试进程 |
| `uiRecord` | 录制 UI 操作 |
| `uiInput` | 注入 UI 操作 |

---

## screenCap - 屏幕截图

### 语法

```bash
uitest screenCap [options]
```

### 选项

| 选项 | 说明 |
|------|------|
| `-p <savePath>` | 保存路径 |
| `-d <displayId>` | 指定屏幕（多屏设备） |

### 示例

```bash
# 截图保存到默认路径
hdc shell uitest screenCap

# 保存到指定路径
hdc shell uitest screenCap -p /data/local/tmp/screenshot.png

# 指定屏幕截图
hdc shell uitest screenCap -d 0
```

---

## dumpLayout - 布局导出

获取当前界面的布局信息。

### 语法

```bash
uitest dumpLayout [options]
```

### 选项

| 选项 | 说明 |
|------|------|
| `-p <savePath>` | 保存路径 |
| `-i` | 不合并窗口，过滤节点 |
| `-a` | 包含字体属性 |
| `-b <bundleName>` | 目标窗口的包名 |
| `-w <windowId>` | 目标窗口 ID |
| `-m <true/false>` | 是否合并窗口 |
| `-d <displayId>` | 目标窗口所在屏幕 |
| `-e <attributeName>` | 扩展属性 |

### 示例

```bash
# 导出当前布局到默认路径
hdc shell uitest dumpLayout

# 保存到指定路径
hdc shell uitest dumpLayout -p /data/local/tmp/layout.xml

# 不合并窗口
hdc shell uitest dumpLayout -i

# 包含字体属性
hdc shell uitest dumpLayout -a

# 导出指定应用窗口
hdc shell uitest dumpLayout -b com.example.app

# 导出指定窗口
hdc shell uitest dumpLayout -b com.example.app -w 1

# 添加扩展属性
hdc shell uitest dumpLayout -e bounds
```

---

## start-daemon - 启动测试进程

### 语法

```bash
uitest start-daemon <token>
```

### 示例

```bash
hdc shell uitest start-daemon <token>
```

---

## uiRecord - UI 操作录制

录制 UI 操作序列。

### 子命令

| 子命令 | 说明 |
|--------|------|
| `record` | 录制 UI 事件信息到 CSV 文件 |
| `read` | 打印文件内容到控制台 |

### record 选项

| 选项 | 说明 |
|------|------|
| `-W <true/false>` | 是否保存组件信息（默认 true） |
| `-l` | 每次操作后保存布局信息 |
| `-c <true/false>` | 是否打印 UI 事件到控制台（默认 true） |

### 示例

```bash
# 开始录制
hdc shell uitest uiRecord record

# 不保存组件信息
hdc shell uitest uiRecord record -W false

# 每次操作后保存布局
hdc shell uitest uiRecord record -l

# 不打印到控制台
hdc shell uitest uiRecord record -c false

# 读取录制文件
hdc shell uitest uiRecord read
```

---

## uiInput - UI 操作注入

注入模拟用户操作。

### 子命令

| 子命令 | 说明 |
|--------|------|
| `help` | 显示帮助 |
| `dircFling` | 方向滑动 |
| `click` | 点击 |
| `doubleClick` | 双击 |
| `longClick` | 长按 |
| `swipe` | 滑动 |
| `drag` | 拖拽 |
| `fling` | 快速滑动 |
| `keyEvent` | 按键事件 |
| `inputText` | 输入文本（坐标定位） |
| `text` | 输入文本（聚焦定位） |

### dircFling - 方向滑动

```bash
uitest uiInput dircFling <direction> [velocity] [stepLength]
```

| 参数 | 说明 |
|------|------|
| direction | 方向：0=左, 1=右, 2=上, 3=下 |
| velocity | 速度（200-40000，默认 600） |
| stepLength | 步长 |

### 点击命令

```bash
# 点击
uitest uiInput click <x> <y>

# 双击
uitest uiInput doubleClick <x> <y>

# 长按
uitest uiInput longClick <x> <y>
```

### 滑动/拖拽

```bash
# 滑动
uitest uiInput swipe <from_x> <from_y> <to_x> <to_y> [velocity]

# 拖拽
uitest uiInput drag <from_x> <from_y> <to_x> <to_y> [velocity]

# 快速滑动
uitest uiInput fling <from_x> <from_y> <to_x> <to_y> [velocity] [stepLength]
```

| 参数 | 说明 |
|------|------|
| velocity | 速度（200-40000，默认 600） |

### 按键事件

```bash
uitest uiInput keyEvent <keyID/Back/Home/Power>

uitest uiInput keyEvent <keyID_0> <keyID_1> [keyID_2]
```

常用按键：
- `Back` - 返回键
- `Home` - 主屏键
- `Power` - 电源键

### 文本输入

```bash
# 在指定坐标输入（需先点击输入框）
uitest uiInput inputText <x> <y> <text>

# 在已聚焦位置输入
uitest uiInput text <text>
```

### 示例

```bash
# 点击屏幕中央
hdc shell uitest uiInput click 540 960

# 双击
hdc shell uitest uiInput doubleClick 540 960

# 长按
hdc shell uitest uiInput longClick 540 960

# 上滑
hdc shell uitest uiInput dircFling 2

# 快速上滑
hdc shell uitest uiInput dircFling 2 2000

# 从 (100, 1000) 滑到 (100, 200)
hdc shell uitest uiInput swipe 100 1000 100 200

# 快速滑动
hdc shell uitest uiInput fling 100 1000 100 200 2000

# 按返回键
hdc shell uitest uiInput keyEvent Back

# 按主页键
hdc shell uitest uiInput keyEvent Home

# 输入文本
hdc shell uitest uiInput text "Hello"

# 点击后输入
hdc shell uitest uiInput click 540 960
hdc shell uitest uiInput text "Hello"
```

---

## 常用组合

```bash
# 1. 截图 + 获取布局
hdc shell uitest screenCap -p /data/local/tmp/screen.png
hdc shell "uitest dumpLayout -p /data/local/tmp/layout.xml"

# 2. 获取屏幕坐标后点击
hdc shell "uitest dumpLayout -p /data/local/tmp/layout.xml"
# 分析 XML 找到目标元素坐标
hdc shell uitest uiInput click 540 960

# 3. UI 操作自动化
hdc shell uitest uiInput click 100 500
hdc shell uitest uiInput text "username"
hdc shell uitest uiInput click 100 600
hdc shell uitest uiInput text "password"
hdc shell uitest uiInput click 540 800
```
