#!/usr/bin/env python3
"""
ArcLink - Export Arc Browser pinned tabs to Markdown
A standalone CLI tool (no dependencies beyond Python stdlib).
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


def get_arc_data_path() -> Path | None:
    """Auto-detect Arc Browser's StorableSidebar.json location."""
    home = Path.home()
    
    if sys.platform == "darwin":
        arc_path = home / "Library" / "Application Support" / "Arc" / "StorableSidebar.json"
        if arc_path.exists():
            return arc_path
    elif sys.platform == "win32":
        local_app_data = os.environ.get("LOCALAPPDATA")
        if local_app_data:
            packages_path = Path(local_app_data) / "Packages"
            if packages_path.exists():
                for folder in packages_path.glob("TheBrowserCompany.Arc_*"):
                    arc_path = folder / "LocalCache" / "Local" / "Arc" / "StorableSidebar.json"
                    if arc_path.exists():
                        return arc_path
    
    return None


def extract_items_array(items: list) -> dict[str, dict]:
    """Extract ID -> item mapping from items array."""
    id_map = {}
    current_id = None
    
    for item in items:
        if isinstance(item, str):
            current_id = item
        elif isinstance(item, dict) and current_id:
            id_map[current_id] = item
    
    return id_map


def extract_bookmark_from_item(item: dict) -> tuple[str, str] | None:
    """Extract bookmark title and URL from an item."""
    data = item.get("data", {})
    
    if "tab" in data:
        tab_data = data["tab"]
        url = tab_data.get("savedURL", "")
        title = tab_data.get("savedTitle", "Untitled")
        if url:
            url = url.replace("\\/", "/")
            return (title, url)
    
    return None


def parse_arc_bookmarks(data: dict) -> dict[str, list[tuple[str, str]]]:
    """Parse Arc bookmarks from StorableSidebar.json."""
    result = {}
    
    if "sidebar" not in data:
        return result
    
    sidebar = data["sidebar"]
    containers = sidebar.get("containers", [])
    
    for container in containers:
        if "items" not in container:
            continue
        
        items = container["items"]
        items_map = extract_items_array(items)
        
        space_bookmarks = {}
        
        for item_id, item in items_map.items():
            bookmark = extract_bookmark_from_item(item)
            if bookmark:
                title, url = bookmark
                parent_id = item.get("parentID")
                
                if parent_id and parent_id in items_map:
                    parent = items_map[parent_id]
                    parent_title = parent.get("title") or "Default"
                else:
                    parent_title = "Pinned"
                
                if parent_title not in space_bookmarks:
                    space_bookmarks[parent_title] = []
                space_bookmarks[parent_title].append((title, url))
        
        if space_bookmarks:
            result["Pinned Tabs"] = []
            for folder, bookmarks in space_bookmarks.items():
                for bm in bookmarks:
                    result["Pinned Tabs"].append(bm)
    
    return result


def format_markdown(bookmarks: dict[str, list[tuple[str, str]]]) -> str:
    """Format bookmarks as Markdown."""
    lines = []
    lines.append("# ARC Browser Saved Links")
    lines.append(f"\nExported on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    total = 0
    
    for space_name, items in bookmarks.items():
        if not items:
            continue
        
        lines.append(f"## {space_name}\n")
        
        for title, url in items:
            lines.append(f"- [{title}]({url})")
            total += 1
        
        lines.append("")
    
    lines.append(f"---\n")
    lines.append(f"*Total: {total} links*")
    
    return "\n".join(lines)


def export_to_markdown(data_path: Path, output_path: Path | None = None, verbose: bool = False) -> Path:
    """Export Arc bookmarks to Markdown file."""
    if verbose:
        print(f"Reading Arc data from: {data_path}")
    
    with open(data_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    content = content.replace("\\", "\\\\")
    
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        try:
            content = content.replace("\\\\", "\\")
            data = json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse Arc data file: {e}")
    
    bookmarks = parse_arc_bookmarks(data)
    
    if not bookmarks:
        raise ValueError("No bookmarks found in Arc data file")
    
    if verbose:
        print(f"Found {len(bookmarks)} spaces with bookmarks")
    
    md_content = format_markdown(bookmarks)
    
    if output_path is None:
        downloads = Path.home() / "Downloads"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = downloads / f"arc_bookmarks_{timestamp}.md"
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    
    if verbose:
        print(f"Exported to: {output_path}")
    
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Export ARC Browser saved links to Markdown file",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  arclink                      # Auto-detect Arc data and export to Downloads
  arclink -v                   # Verbose output
  arclink -o custom.md         # Specify output file
  arclink -d /path/to/StorableSidebar.json  # Specify Arc data file
        """
    )
    
    parser.add_argument("-o", "--output", help="Output Markdown file path", type=Path)
    parser.add_argument("-d", "--data-file", help="Path to StorableSidebar.json", type=Path)
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    
    args = parser.parse_args()
    
    data_path = args.data_file
    
    if data_path is None:
        if args.verbose:
            print("Auto-detecting Arc data file location...")
        data_path = get_arc_data_path()
        
        if data_path is None:
            print("Error: Could not find Arc data file.", file=sys.stderr)
            print("\nPlease specify the path manually:", file=sys.stderr)
            print("  macOS: ~/Library/Application Support/Arc/StorableSidebar.json", file=sys.stderr)
            print("  Windows: %LOCALAPPDATA%\\Packages\\TheBrowserCompany.Arc_*\\LocalCache\\Local\\Arc\\StorableSidebar.json", file=sys.stderr)
            sys.exit(1)
    
    if not data_path.exists():
        print(f"Error: File not found: {data_path}", file=sys.stderr)
        sys.exit(1)
    
    try:
        output_path = export_to_markdown(data_path, args.output, args.verbose)
        print(f"Successfully exported to: {output_path}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
