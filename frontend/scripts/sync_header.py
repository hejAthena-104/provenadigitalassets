#!/usr/bin/env python3
"""
Provena Digital Assets - Header Sync Script
======================================
Copies the header design from index.html to all other pages
to ensure consistent navigation across the site.
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

# Pages to update (in root directory)
TARGET_PAGES = [
    'about-us.html',
    'affiliate.html',
    'agent-franchise.html',
    'aml.html',
    'bonds.html',
    'contact.html',
    'crypto.html',
    'faq.html',
    'faqs.html',
    'forex.html',
    'goldasset.html',
    'insights.html',
    'legals.html',
    'newcrypto.html',
    'oilandgas.html',
    'ourteam.html',
    'privacy.html',
    'realestate.html',
    'risk-disclosure.html',
    'stocks.html',
    'terms.html',
    'transactions.html',
]

def extract_header(source_file):
    """Extract header section from source file"""
    try:
        with open(source_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Find header section: from <header id="header" to </header>
        pattern = r'(<header\s+id="header"[^>]*>.*?</header>)'
        match = re.search(pattern, content, re.DOTALL)

        if match:
            return match.group(1)
        return None
    except Exception as e:
        print(f"  {Colors.RED}Error reading source: {e}{Colors.END}")
        return None


def update_page(filepath, new_header):
    """Update a single page with the new header"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        original = content

        # Find and replace the header section
        pattern = r'<header\s+id="header"[^>]*>.*?</header>'

        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, new_header, content, flags=re.DOTALL)
        else:
            # No header found
            return False, "No header found"

        # Write if changed
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, "Updated"

        return False, "No changes needed"

    except Exception as e:
        return False, f"Error: {str(e)}"


def main():
    print()
    print("=" * 80)
    print(f"{Colors.BOLD}{Colors.CYAN}  PROVENA DIGITAL ASSETS - HEADER SYNC{Colors.END}")
    print("=" * 80)
    print()
    print("  Copies header design from index.html to all other pages.")
    print()
    print("-" * 80)

    base_dir = Path('.')
    source_file = base_dir / 'index.html'

    # Extract header from source
    print(f"\n  {Colors.BOLD}Extracting header from index.html...{Colors.END}")

    new_header = extract_header(source_file)

    if not new_header:
        print(f"  {Colors.RED}Failed to extract header from index.html{Colors.END}")
        return

    header_lines = new_header.count('\n')
    print(f"  {Colors.GREEN}[OK]{Colors.END} Header extracted ({header_lines} lines)")

    # Filter to only existing files
    files_to_update = [f for f in TARGET_PAGES if (base_dir / f).exists()]

    print(f"\n  Found {Colors.BLUE}{len(files_to_update)}{Colors.END} page(s) to update\n")
    print("-" * 80)
    print(f"\n  {Colors.BOLD}Updating pages...{Colors.END}\n")

    updated_count = 0
    skipped_count = 0
    error_count = 0

    for filename in sorted(files_to_update):
        filepath = base_dir / filename
        success, message = update_page(filepath, new_header)

        if success:
            print(f"  {Colors.GREEN}[OK]{Colors.END} {filename}")
            updated_count += 1
        elif "No changes" in message:
            print(f"  {Colors.YELLOW}[--]{Colors.END} {filename} (already up to date)")
            skipped_count += 1
        else:
            print(f"  {Colors.RED}[!!]{Colors.END} {filename} - {message}")
            error_count += 1

    print()
    print("-" * 80)
    print()
    print(f"  {Colors.BOLD}SUMMARY{Colors.END}")
    print(f"  {Colors.GREEN}Updated:{Colors.END}  {updated_count} file(s)")
    print(f"  {Colors.YELLOW}Skipped:{Colors.END}  {skipped_count} file(s)")
    if error_count > 0:
        print(f"  {Colors.RED}Errors:{Colors.END}   {error_count} file(s)")
    print()

    if updated_count > 0:
        print(f"  {Colors.GREEN}Header synced successfully!{Colors.END}")
        print()

    print("=" * 80)
    print()


if __name__ == '__main__':
    main()
