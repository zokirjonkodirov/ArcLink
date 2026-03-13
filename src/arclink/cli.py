#!/usr/bin/env python3
"""CLI interface for ArcLink."""

import sys
from pathlib import Path

import click

from arclink import get_arc_data_path, export_to_markdown


@click.command()
@click.option(
    "-o", "--output",
    help="Output Markdown file path (default: ~/Downloads/arc_bookmarks_TIMESTAMP.md)",
    type=click.Path(path_type=Path)
)
@click.option(
    "-d", "--data-file",
    help="Path to StorableSidebar.json (auto-detected if not specified)",
    type=click.Path(path_type=Path)
)
@click.option(
    "-v", "--verbose",
    is_flag=True,
    help="Enable verbose output"
)
def main(output: Path | None, data_file: Path | None, verbose: bool):
    """Export ARC Browser saved links to Markdown file."""
    data_path = data_file
    
    if data_path is None:
        if verbose:
            click.echo("Auto-detecting Arc data file location...")
        data_path = get_arc_data_path()
        
        if data_path is None:
            click.echo("Error: Could not find Arc data file.", err=True)
            click.echo("\nPlease specify the path manually:", err=True)
            click.echo("  macOS: ~/Library/Application Support/Arc/StorableSidebar.json", err=True)
            click.echo("  Windows: %LOCALAPPDATA%\\Packages\\TheBrowserCompany.Arc_*\\LocalCache\\Local\\Arc\\StorableSidebar.json", err=True)
            sys.exit(1)
    
    if not data_path.exists():
        click.echo(f"Error: File not found: {data_path}", err=True)
        sys.exit(1)
    
    try:
        output_path = export_to_markdown(data_path, output, verbose)
        click.echo(f"Successfully exported to: {output_path}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
