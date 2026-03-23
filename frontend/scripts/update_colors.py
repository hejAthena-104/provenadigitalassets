#!/usr/bin/env python3
"""
Provena Digital Assets - Color Migration Script
=========================================
Updates hardcoded color values in HTML files to use CSS variables
for better theme support.
"""
import os
import re
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

# Color mappings: old hex -> new CSS variable or hex
# These are for inline styles that can be safely updated
COLOR_MAPPINGS = {
    # Old primary blues -> new primary blue
    '#012c6d': '#0A2FFF',
    '#012c6a': '#0A2FFF',
    '#012c6e': '#0A2FFF',
    '#4184dd': '#0A2FFF',
    '#4184DD': '#0A2FFF',

    # Button background colors
    'background-color: #012c6d': 'background-color: #0A2FFF',
    'background: #012c6d': 'background: #0A2FFF',
    'border-color: #012c6d': 'border-color: #0A2FFF',

    # Dark widget backgrounds - keep dark theme
    '#1D2330': '#1E1E1E',
    '#282E3B': '#181818',
    '#262B38': '#181818',
    '#112b77': '#121212',
}

# Patterns to skip (don't modify these)
SKIP_PATTERNS = [
    'dashboard.webwavedigitaltrading.com',
    'TradingView',
    'coinlib',
    'crypto-widget',
]


def should_skip_line(line):
    """Check if line contains patterns that should not be modified"""
    for pattern in SKIP_PATTERNS:
        if pattern in line:
            return True
    return False


def update_file(filepath):
    """Update colors in a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        original_content = content
        changes = []

        # Apply color mappings
        lines = content.split('\n')
        new_lines = []

        for line in lines:
            new_line = line

            if not should_skip_line(line):
                for old_color, new_color in COLOR_MAPPINGS.items():
                    if old_color.lower() in new_line.lower():
                        # Case-insensitive replacement
                        pattern = re.compile(re.escape(old_color), re.IGNORECASE)
                        count_before = len(pattern.findall(new_line))
                        new_line = pattern.sub(new_color, new_line)
                        if count_before > 0:
                            changes.append(f"{old_color} -> {new_color}")

            new_lines.append(new_line)

        content = '\n'.join(new_lines)

        # Write if changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            # Deduplicate changes
            unique_changes = list(dict.fromkeys(changes))
            return True, unique_changes

        return False, []

    except Exception as e:
        return False, [f"Error: {str(e)}"]


def main():
    """Main function"""
    print()
    print("=" * 80)
    print(f"{Colors.BOLD}{Colors.CYAN}  PROVENA DIGITAL ASSETS - COLOR MIGRATION{Colors.END}")
    print("=" * 80)
    print()
    print("  Updates hardcoded colors to new brand colors.")
    print()
    print(f"  {Colors.YELLOW}Color Changes:{Colors.END}")
    print(f"    - Old Blues (#012c6d, #4184dd) -> Electric Blue (#0A2FFF)")
    print(f"    - Dark backgrounds updated for consistency")
    print()
    print("-" * 80)

    base_dir = Path('.')

    # Find all HTML files
    html_files = list(base_dir.glob('*.html'))

    print(f"\n  Found {Colors.BLUE}{len(html_files)}{Colors.END} HTML file(s)\n")

    print("-" * 80)
    print(f"\n  {Colors.BOLD}Processing files...{Colors.END}\n")

    updated_count = 0
    skipped_count = 0

    for html_file in sorted(html_files):
        success, changes = update_file(html_file)

        if success and changes:
            print(f"  {Colors.GREEN}[OK]{Colors.END} {html_file.name}")
            for change in changes[:3]:
                print(f"       {Colors.CYAN}->{Colors.END} {change}")
            if len(changes) > 3:
                print(f"       {Colors.CYAN}->{Colors.END} ... and {len(changes) - 3} more")
            updated_count += 1
        else:
            print(f"  {Colors.YELLOW}[--]{Colors.END} {html_file.name} (no color changes)")
            skipped_count += 1

    print()
    print("-" * 80)
    print()
    print(f"  {Colors.BOLD}SUMMARY{Colors.END}")
    print(f"  {Colors.GREEN}Updated:{Colors.END}  {updated_count} file(s)")
    print(f"  {Colors.YELLOW}Skipped:{Colors.END}  {skipped_count} file(s)")
    print()

    if updated_count > 0:
        print(f"  {Colors.GREEN}Colors migrated successfully!{Colors.END}")
        print()

    print("=" * 80)
    print()


if __name__ == '__main__':
    main()
