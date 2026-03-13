# ArcLink

A CLI tool to export pinned tabs and bookmarks from the Arc Browser to Markdown format.

## Why This Tool?

Arc Browser lacks a built-in export feature for bookmarks. The "Copy All Links" option only copies URLs as a plain string. This tool provides a robust solution by:

- Parsing Arc's internal `StorableSidebar.json` data file
- Exporting all pinned tabs to a well-formatted Markdown file
- Automatically saving to your Downloads folder with timestamps

## Installation

### Via Homebrew (macOS)

```bash
# Add the tap (one-time)
brew tap zokirjonkodirov/arclink

# Install
brew install arclink
```

### Via pip

```bash
pip install arclink
```

### From source

```bash
git clone https://github.com/zokirjonkodirov/ArcLink.git
cd ArcLink/arclink
pip install -e .
```

## Usage

```bash
# Auto-detect Arc data and export to Downloads folder
arclink

# Verbose output
arclink -v

# Specify custom output file
arclink -o my-bookmarks.md

# Manually specify Arc data file location
arclink -d "~/Library/Application Support/Arc/StorableSidebar.json"
```

## Finding Arc Data File

If auto-detection fails, manually locate the file:

### Windows
```
%LOCALAPPDATA%\Packages\TheBrowserCompany.Arc_*\LocalCache\Local\Arc\StorableSidebar.json
```

### macOS
```
~/Library/Application Support/Arc/StorableSidebar.json
```

## Output Format

```markdown
# ARC Browser Saved Links

Exported on: 2026-03-13 11:51:06

## Pinned Tabs

- [enoent.fr](https://enoent.fr/)
- [Jake Wharton](https://jakewharton.com/)
- ...

---

*Total: 172 links*
```

## Notes

- Only exports **pinned tabs** (not ephemeral or unpinned tabs)
- The tool reads data locally - no data is sent anywhere
- Close Arc Browser before exporting to ensure latest data is saved
