---
name: desktop-clear
description: Organize and clean up the user's desktop by categorizing files, suggesting organization strategies, and moving files to appropriate folders. Use when the user wants to tidy their desktop, organize desktop files, or clean up workspace clutter.
---

# Desktop-Clear: Desktop Organization Tool

## Overview

Desktop-Clear is a skill for organizing and cleaning up the Windows desktop. It scans desktop files, categorizes them by type/extension, suggests organization strategies, and helps move files to appropriate folders with user confirmation.

**Core principle:** Always get user confirmation before moving or deleting any files.

## When to Use

Use this skill when:
- User wants to organize or tidy their desktop
- User says their desktop is cluttered or messy
- User wants to move desktop files to proper locations
- User asks to clean up workspace

## Workflow

### Step 1: Scan Desktop

First, list all files on the desktop with their details:

```bash
ls -la "C:/Users/jaike/Desktop"
```

For a more detailed analysis including file sizes:
```bash
find "C:/Users/jaike/Desktop" -maxdepth 1 -type f -exec ls -lh {} \;
```

### Step 2: Categorize Files

After scanning, categorize files into groups:

**Common Categories:**
| Category | Extensions/Filenames | Suggested Target |
|----------|---------------------|------------------|
| Images | .png, .jpg, .jpeg, .gif, .bmp, .webp, .svg | `Pictures/Desktop/` |
| Documents | .pdf, .doc, .docx, .xls, .xlsx, .ppt, .pptx, .txt, .md | `Documents/Desktop/` |
| Archives | .zip, .rar, .7z, .tar, .gz | `Downloads/Archives/` |
| Code | .js, .py, .ts, .html, .css, .json, .xml | `Documents/Code/` or project folder |
| Installers | .exe, .msi, .dmg | `Downloads/Installers/` |
| Videos | .mp4, .mkv, .avi, .mov | `Videos/Desktop/` |
| Audio | .mp3, .wav, .flac, .aac | `Music/Desktop/` |
| Shortcuts | .lnk, .url | Keep on desktop or organize |
| Screenshots | Screenshot*, screen-*, *.png (from Screenshots) | `Pictures/Screenshots/` |

### Step 3: Present Organization Plan

**IMPORTANT:** Before executing any file operations, present the plan to the user.

Use the `AskUserQuestion` tool:

```
Questions:
1. "How would you like to organize your desktop?"
   Options:
   - "By file type (Images, Documents, etc.)"
   - "By date (Today, This Week, Older)"
   - "Move all to a dated folder"
   - "Custom organization"

2. "Which categories would you like to organize?"
   Options:
   - "Images -> Pictures/Desktop/"
   - "Documents -> Documents/Desktop/"
   - "Archives -> Downloads/Archives/"
   - "Installers -> Downloads/Installers/"
   - Multi-select: true
```

### Step 4: Create Target Folders (if needed)

```bash
# Create organization folders
mkdir -p "C:/Users/jaike/Pictures/Desktop"
mkdir -p "C:/Users/jaike/Documents/Desktop"
mkdir -p "C:/Users/jaike/Downloads/Archives"
mkdir -p "C:/Users/jaike/Downloads/Installers"
mkdir -p "C:/Users/jaike/Videos/Desktop"
mkdir -p "C:/Users/jaike/Music/Desktop"
mkdir -p "C:/Users/jaike/Pictures/Screenshots"
```

### Step 5: Execute File Moves (only after confirmation)

Move files based on user's selection:

**Images:**
```bash
mv "C:/Users/jaike/Desktop"/*.png "C:/Users/jaike/Pictures/Desktop/" 2>/dev/null
mv "C:/Users/jaike/Desktop"/*.jpg "C:/Users/jaike/Pictures/Desktop/" 2>/dev/null
mv "C:/Users/jaike/Desktop"/*.jpeg "C:/Users/jaike/Pictures/Desktop/" 2>/dev/null
```

**Documents:**
```bash
mv "C:/Users/jaike/Desktop"/*.pdf "C:/Users/jaike/Documents/Desktop/" 2>/dev/null
mv "C:/Users/jaike/Desktop"/*.docx "C:/Users/jaike/Documents/Desktop/" 2>/dev/null
mv "C:/Users/jaike/Desktop"/*.txt "C:/Users/jaike/Documents/Desktop/" 2>/dev/null
```

**Archives:**
```bash
mv "C:/Users/jaike/Desktop"/*.zip "C:/Users/jaike/Downloads/Archives/" 2>/dev/null
mv "C:/Users/jaike/Desktop"/*.rar "C:/Users/jaike/Downloads/Archives/" 2>/dev/null
```

**Installers:**
```bash
mv "C:/Users/jaike/Desktop"/*.exe "C:/Users/jaike/Downloads/Installers/" 2>/dev/null
```

## Alternative Organization Strategies

### By Date
Create dated folders and sort files by modification time:

```bash
# Create dated folder
TODAY=$(date +%Y-%m-%d)
mkdir -p "C:/Users/jaike/Desktop/Archived_$TODAY"

# Move older files (example: files not modified in 7 days)
find "C:/Users/jaike/Desktop" -maxdepth 1 -type f -mtime +7 -exec mv {} "C:/Users/jaike/Desktop/Archived_$TODAY/" \;
```

### Quick Sweep (move everything to one folder)
```bash
TODAY=$(date +%Y-%m-%d)
mkdir -p "C:/Users/jaike/Documents/Desktop_Backup_$TODAY"
mv "C:/Users/jaike/Desktop"/* "C:/Users/jaike/Documents/Desktop_Backup_$TODAY/" 2>/dev/null
```

## Example Usage

```
User: /desktop-clear

Agent:
1. Scanning desktop files...
2. Found 23 files on desktop

📊 **Desktop Analysis**
- Images: 8 files (screenshots, photos)
- Documents: 5 files (PDFs, Word docs)
- Archives: 3 files (ZIPs)
- Installers: 2 files (EXEs)
- Shortcuts: 3 files
- Other: 2 files

[Presents organization options via AskUserQuestion]

User selects: Images, Documents, Archives

Agent:
Proceeding with organization...
✓ Moved 8 images to Pictures/Desktop/
✓ Moved 5 documents to Documents/Desktop/
✓ Moved 3 archives to Downloads/Archives/

**Desktop now has 5 items remaining (shortcuts + other)**
```

## Special File Detection

**Screenshots:** Detect by filename pattern
```bash
# Screenshots often have names like: Screenshot_2024-01-15.png
find "C:/Users/jaike/Desktop" -maxdepth 1 -type f -name "Screenshot*" -o -name "screen-*"
```

**Downloads on Desktop:** Check if files came from browser downloads
- Files with recent access time and browser-like names

## Safety Guidelines

1. **NEVER delete files without explicit confirmation**
2. **Preserve desktop shortcuts** - These are often important (`.lnk` files)
3. **Don't move system files** - Skip hidden files, system files
4. **Create backup folders** - When in doubt, move to a dated backup folder
5. **Report what was moved** - Always summarize actions taken
6. **Handle errors gracefully** - Some files may be in use or protected

## Files to Skip

- `.lnk` files (shortcuts) - ask before moving
- Hidden files (starting with `.`)
- System files
- Files currently in use (will error, handle gracefully)
- `$RECYCLE.BIN`, `desktop.ini`, `Thumbs.db`

## Error Handling

If move fails:
1. Report which file failed
2. Check if file is in use: `lsof` or similar
3. Suggest manual move for problematic files
4. Continue with other files
