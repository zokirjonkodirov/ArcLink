# ARC Browser Saved Links Exporter

A CLI tool to export pinned tabs and bookmarks from the Arc Browser to Markdown format.

## Why This Tool?

Arc Browser lacks a built-in export feature for bookmarks. The "Copy All Links" option only copies URLs as a plain string. This tool provides a robust solution by:

- Parsing Arc's internal `StorableSidebar.json` data file
- Exporting all pinned tabs to a well-formatted Markdown file
- Automatically saving to your Downloads folder with timestamps
- Preserving folder structure where possible

## Requirements

- Python 3.8+

## Installation

```bash
# Clone or download this repository
git clone <repo-url>
cd arcimport

# Or just use the script directly
python3 arc-export.py
```

## Usage

```bash
# Auto-detect Arc data and export to Downloads folder
python3 arc-export.py

# Verbose output - shows what's happening
python3 arc-export.py -v

# Specify custom output file
python3 arc-export.py -o my-bookmarks.md

# Manually specify Arc data file location
python3 arc-export.py -d "C:\Users\You\AppData\Local\Packages\TheBrowserCompany.Arc_ttt1ap7aakyb4\LocalCache\Local\Arc\StorableSidebar.json"
```

## Finding Arc Data File

If auto-detection fails, manually locate the file:

### Windows
```
%LOCALAPPDATA%\Packages\TheBrowserCompany.Arc_*\LocalCache\Local\Arc\StorableSidebar.json
```
Or press Win+R and paste the path above.

### macOS
```
~/Library/Application Support/Arc/StorableSidebar.json
```
Press Cmd+Shift+G in Finder and paste the path.

## Output Format

The exported Markdown file looks like:

```markdown
# ARC Browser Saved Links

Exported on: 2026-03-13 11:51:06

- [enoent.fr](https://enoent.fr/)
- [Jake Wharton](https://jakewharton.com/)
- [overreacted — A blog by Dan Abramov](https://overreacted.io/)
- ...

---

*Total: 172 links*
```

## Notes

- Only exports **pinned tabs** (not ephemeral or unpinned tabs)
- The tool reads data locally - no data is sent anywhere
- Close Arc Browser before exporting to ensure latest data is saved
- On Windows, the folder name after `TheBrowserCompany.Arc_` may vary (contains a hash)
