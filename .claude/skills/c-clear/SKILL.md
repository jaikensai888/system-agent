---
name: c-clear
description: C盘空间清理助手，扫描分析文件夹大小并提供优化建议。触发场景：(1) 用户想清理C盘或释放磁盘空间；(2) 用户询问磁盘占用或大文件夹；(3) 用户提到清理缓存、临时文件、垃圾文件；(4) 系统磁盘空间不足；(5) 使用 /c-clear 命令。
---

# C-Clear: C盘空间清理

## 工作流程

### 1. 扫描分析

运行脚本扫描 AppData\Local 目录：

```bash
python "$SKILL_DIR/scripts/list_folder_sizes.py" "C:\Users\$USERNAME\AppData\Local" -o "$SKILL_DIR/size_report.md"
```

然后读取报告进行分析。

### 2. 分类建议

扫描完成后，将文件夹分为以下类别：

**安全清理（通常安全，但仍需确认）：**
| 文件夹 | 说明 |
|--------|------|
| `npm-cache` | Node.js 包缓存 |
| `pip\cache` | Python 包缓存 |
| `Temp` | 临时文件 |
| `*-updater` | 各软件的旧更新文件 |
| `pnpm-cache` | pnpm 缓存 |
| `CrashDumps` | 崩溃转储文件 |

**需用户决定：**
| 文件夹 | 说明 |
|--------|------|
| `uv` | Python 包管理器缓存（清理后可能需重新下载包） |
| `Downloaded Installations` | 下载的安装程序 |
| `Microsoft` | Windows/Office 缓存（部分子文件夹可清理） |
| `JianyingPro` | 剪映缓存 |
| `DingTalk` / `DingTalk_*` | 钉钉缓存 |

**切勿清理：**
- `Packages` - Windows 应用数据
- `Programs` - 已安装程序
- `Google` - Chrome 数据（书签、密码等）
- `AnkiProgramFiles` - Anki 数据

### 3. 用户确认

**重要：** 执行任何清理前，必须使用 `AskUserQuestion` 工具向用户展示清理计划并获得明确确认。

### 4. 执行清理（确认后）

| 目标 | 命令 |
|------|------|
| npm cache | `npm cache clean --force` |
| pip cache | `pip cache purge` |
| uv cache | `uv cache clean` |
| Temp 文件 | `rm -rf "C:/Users/$USERNAME/AppData/Local/Temp/*"` |
| pnpm cache | `pnpm store prune` |
| updater 文件夹 | `rm -rf "C:/Users/$USERNAME/AppData/Local/xxx-updater"` |

## 示例

```
用户: /c-clear

Agent:
📊 **磁盘占用摘要**
AppData\Local 总计: 61.54 GB

🗑️ **建议清理:**
- npm-cache: 6.66 GB
- pip cache: 4.26 GB
- uv cache: 10.75 GB
- Temp files: 208.87 MB
- Updater 文件夹: ~2.5 GB

**可释放空间: ~24 GB**

[通过 AskUserQuestion 展示选项]

用户选择: npm-cache, pip cache, Temp files

Agent:
✓ 已清理 npm cache: 6.66 GB
✓ 已清理 pip cache: 4.26 GB
✓ 已清理 Temp files: 200 MB

**共释放: ~11 GB**
```

## 安全原则

1. **绝不未经确认删除** - 始终先询问
2. **说明删除内容** - 让用户理解影响
3. **警告潜在副作用** - 如"清理 uv 缓存后 Python 包可能需重新下载"
4. **优先保守选项** - 从明显安全的清理开始
5. **提供预估节省空间** - 帮助用户优先级排序
