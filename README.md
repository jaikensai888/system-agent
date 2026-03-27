# System Agent

Claude Code 技能集合，用于系统管理和维护任务。

## 包含技能

### c-clear

C 盘空间清理助手，扫描分析文件夹大小并提供优化建议。

**触发场景：**
- 用户想清理 C 盘或释放磁盘空间
- 用户询问磁盘占用或大文件夹
- 用户提到清理缓存、临时文件、垃圾文件
- 系统磁盘空间不足

**使用方式：**
```
/c-clear
```

**功能：**
- 扫描 `AppData\Local` 目录，分析各文件夹占用
- 分类建议（安全清理 / 需用户决定 / 切勿清理）
- 执行清理前需用户确认
- 支持清理 npm/pnpm/uv 缓存、临时文件、updater 文件夹等

---

### desktop-clear

桌面整理助手，帮助分类和整理桌面文件。

**触发场景：**
- 用户想整理桌面
- 用户想清理桌面杂乱文件
- 用户想按类别组织桌面文件

**使用方式：**
```
/desktop-clear
```

## 目录结构

```
system-agent/
├── .claude/
│   ├── settings.local.json      # 本地设置
│   └── skills/
│       ├── c-clear/
│       │   ├── SKILL.md         # 技能说明
│       │   └── scripts/
│       │       └── list_folder_sizes.py  # 文件夹扫描脚本
│       └── desktop-clear/
│           └── SKILL.md
├── .gitignore
└── README.md
```

## 使用方法

1. 将此仓库克隆到本地
2. 在 Claude Code 中，技能会自动加载
3. 使用 `/c-clear` 或 `/desktop-clear` 命令调用对应技能

## 技能开发

参考 [skill-creator](https://github.com/anthropics/claude-code) 了解如何创建自定义技能。

### 技能规范

每个技能包含：
- `SKILL.md` - 技能说明文件（必需）
- `scripts/` - 可执行脚本（可选）
- `references/` - 参考文档（可选）
- `assets/` - 资源文件（可选）

## 许可证

MIT License
