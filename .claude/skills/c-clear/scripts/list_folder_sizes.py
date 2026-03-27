#!/usr/bin/env python3
"""列出指定目录下所有文件夹的大小"""

import os
from pathlib import Path


def get_folder_size(folder_path):
    """计算文件夹的总大小（包括所有子文件夹和文件）"""
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(filepath)
                except (OSError, PermissionError):
                    pass
    except (OSError, PermissionError):
        pass
    return total_size


def format_size(size_bytes):
    """将字节数格式化为可读的字符串"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def list_folder_sizes(directory, output_md=None):
    """列出目录下所有文件夹的大小

    Args:
        directory: 要扫描的目录
        output_md: 输出的 markdown 文件路径，None 则不输出
    """
    target_dir = Path(directory)

    if not target_dir.exists():
        print(f"错误: 目录不存在 - {directory}")
        return

    if not target_dir.is_dir():
        print(f"错误: 路径不是目录 - {directory}")
        return

    print(f"\n正在扫描: {directory}")
    print("-" * 80)

    folder_sizes = []

    # 获取所有子文件夹
    try:
        for item in target_dir.iterdir():
            if item.is_dir():
                print(f"正在计算: {item.name}...", end='\r')
                size = get_folder_size(item)
                folder_sizes.append((item.name, size))
    except PermissionError as e:
        print(f"权限错误: {e}")
        return

    # 按大小排序（从大到小）
    folder_sizes.sort(key=lambda x: x[1], reverse=True)

    # 打印结果
    print(" " * 80, end='\r')  # 清除进度提示
    print(f"{'文件夹名称':<50} {'大小':>15}")
    print("-" * 80)

    total_size = 0
    for name, size in folder_sizes:
        # 截断过长的名称
        display_name = name[:47] + '...' if len(name) > 50 else name
        print(f"{display_name:<50} {format_size(size):>15}")
        total_size += size

    print("-" * 80)
    print(f"{'总计':<50} {format_size(total_size):>15}")
    print(f"\n共 {len(folder_sizes)} 个文件夹")

    # 输出 Markdown 文件
    if output_md:
        write_markdown(directory, folder_sizes, total_size, output_md)


def write_markdown(directory, folder_sizes, total_size, output_path):
    """将结果写入 Markdown 文件"""
    from datetime import datetime

    md_content = f"""# 文件夹大小统计

**扫描目录:** `{directory}`

**扫描时间:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**总计:** {format_size(total_size)} ({len(folder_sizes)} 个文件夹)

---

| 序号 | 文件夹名称 | 大小 |
|:----:|:-----------|-----:|
"""

    for idx, (name, size) in enumerate(folder_sizes, 1):
        # 转义 Markdown 特殊字符
        escaped_name = name.replace('|', '\\|').replace('`', '\\`')
        md_content += f"| {idx} | {escaped_name} | {format_size(size)} |\n"

    md_content += f"""---

## 统计摘要

- **总大小:** {format_size(total_size)}
- **文件夹数量:** {len(folder_sizes)}
- **最大文件夹:** {folder_sizes[0][0]} ({format_size(folder_sizes[0][1])})
- **最小文件夹:** {folder_sizes[-1][0]} ({format_size(folder_sizes[-1][1])})
"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(md_content)

    print(f"\nMarkdown 文件已保存: {output_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="列出目录下所有文件夹的大小并生成 Markdown 报告"
    )
    parser.add_argument(
        "target_dir",
        help="要扫描的目标目录路径"
    )
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="输出的 Markdown 文件路径（可选，不指定则不输出文件）"
    )

    args = parser.parse_args()
    list_folder_sizes(args.target_dir, args.output)
