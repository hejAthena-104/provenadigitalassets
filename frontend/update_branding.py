#!/usr/bin/env python3
"""
Provena Digital Assets Branding Updater
=================================
Update branding from "Webwave Digital Trading" to "Provena Digital Assets"
across all frontend HTML files.

IMPORTANT: Dashboard URLs (dashboard.webwavedigitaltrading.com) are PRESERVED
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

# ============================================================================
# BRANDING REPLACEMENTS
# Order matters - longer/more specific strings should come first
# ============================================================================

BRAND_REPLACEMENTS = [
    # Main brand name - all variations
    ('Webwave Digital Trading', 'Provena Digital Assets'),
    ('WEBWAVE DIGITAL TRADING', 'PROVENA DIGITAL ASSETS'),
    ('webwave digital trading', 'Provena Digital Assets'),
    ('Webwave Digital Tradings', 'Provena Digital Assets'),  # Handle typos
    ('WebWave Digital Trading', 'Provena Digital Assets'),

    # Partial matches (for copyright, etc.)
    ('Webwave Digital', 'Provena'),
    ('WEBWAVE DIGITAL', 'PROVENA'),
    ('webwave digital', 'Provena'),

    # Short form
    ('Webwave', 'Provena'),
    ('WEBWAVE', 'PROVENA'),
]

# ============================================================================
# CONTENT PARAPHRASING
# Original marketing text -> New paraphrased versions
# ============================================================================

CONTENT_REPLACEMENTS = [
    # Meta descriptions
    (
        'Using our Artificial Intelligence technology, you can now learn, trade, and earn money. Intent on providing the most innovative investment solution with virtual risk assessment.',
        'Harness the power of advanced AI technology to discover, invest, and grow your wealth. Committed to delivering cutting-edge investment solutions with comprehensive risk management.'
    ),
    (
        'Using our Artificial Intelligence Techology, you can now learn, trade, and earn money. Intent on providing the most innovative investment solution with virtual risk assessment.',
        'Harness the power of advanced AI technology to discover, invest, and grow your wealth. Committed to delivering cutting-edge investment solutions with comprehensive risk management.'
    ),
    (
        'Learn, Trade and Earn Using our Artificial Intelligence Techology Today. Geared at offering the most advanced investment solution with proper virtual risk assessment.',
        'Discover smart investment opportunities powered by artificial intelligence. Experience sophisticated portfolio management with professional risk assessment tools.'
    ),

    # Hero/Main taglines
    (
        'Learn Trade and Earn With Us',
        'Invest Smarter. Grow Faster.'
    ),
    (
        'Learn, Trade, and Earn',
        'Invest Smarter. Grow Faster.'
    ),
    (
        'Learn, Trade and Earn',
        'Invest Smarter. Grow Faster.'
    ),

    # Company descriptions
    (
        'An A.I Trading company devoted to your financial success',
        'Your trusted partner in AI-driven investment growth'
    ),
    (
        'AI-Powered Digital Trading Platform',
        'AI-Powered Investment Platform'
    ),
    (
        'ARTIFICIAL INTELLIGENCE TRADING COMPANY',
        'AI-POWERED INVESTMENT PLATFORM'
    ),
    (
        'The Revolution In Management',
        'Transforming Investment Management'
    ),

    # About page content
    (
        'Webwave Digital Trading is a company engaged in Artificial Intelligence Trading',
        'Provena Digital Assets leverages advanced artificial intelligence for sophisticated trading operations'
    ),
    (
        'At Webwave Digital Trading, we are committed',
        'At Provena Digital Assets, we are committed'
    ),
    (
        'Webwave Digital Trading has been providing',
        'Provena Digital Assets has been providing'
    ),
]

# ============================================================================
# PATTERNS TO PRESERVE (not replace)
# ============================================================================

PRESERVE_PATTERNS = [
    'dashboard.webwavedigitaltrading.com',
    'https://dashboard.webwavedigitaltrading.com',
]


def should_skip_line(line, old_text):
    """Check if this line should be skipped for replacement"""
    # Preserve dashboard URLs
    for pattern in PRESERVE_PATTERNS:
        if pattern in line:
            return True
    return False


def update_file(filepath, dry_run=False):
    """Update branding in a single HTML file"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        original_content = content
        changes_made = []

        # Apply brand replacements line by line to preserve dashboard URLs
        lines = content.split('\n')
        new_lines = []

        for line in lines:
            new_line = line

            for old_text, new_text in BRAND_REPLACEMENTS:
                if old_text in new_line:
                    # Check if line contains preserved patterns
                    if not should_skip_line(new_line, old_text):
                        count_before = new_line.count(old_text)
                        new_line = new_line.replace(old_text, new_text)
                        if count_before > 0:
                            changes_made.append(f"Brand: {old_text} -> {new_text}")

            new_lines.append(new_line)

        content = '\n'.join(new_lines)

        # Apply content paraphrasing (these are larger blocks, safe to replace globally)
        for old_content, new_content in CONTENT_REPLACEMENTS:
            if old_content in content:
                content = content.replace(old_content, new_content)
                changes_made.append(f"Content: Paraphrased text block")

        # Check if any changes were made
        if content != original_content:
            if not dry_run:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)

            # Deduplicate changes for reporting
            unique_changes = list(dict.fromkeys(changes_made))
            return True, unique_changes

        return False, []

    except Exception as e:
        return False, [f"Error: {str(e)}"]


def count_occurrences(base_dir):
    """Count occurrences of old branding across all files"""
    counts = {}

    for html_file in base_dir.glob('*.html'):
        try:
            with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            for old_text, _ in BRAND_REPLACEMENTS:
                if old_text in content:
                    counts[old_text] = counts.get(old_text, 0) + content.count(old_text)
        except:
            pass

    return counts


def main():
    """Main function"""
    print()
    print("=" * 80)
    print(f"{Colors.BOLD}{Colors.CYAN}  PROVENA DIGITAL ASSETS BRANDING UPDATER{Colors.END}")
    print("=" * 80)
    print()
    print(f"  {Colors.RED}OLD:{Colors.END} Webwave Digital Trading")
    print(f"  {Colors.GREEN}NEW:{Colors.END} Provena Digital Assets")
    print()
    print(f"  {Colors.YELLOW}NOTE:{Colors.END} Dashboard URLs will be PRESERVED")
    print(f"        (dashboard.webwavedigitaltrading.com remains unchanged)")
    print()
    print("-" * 80)

    base_dir = Path('.')

    # Find all HTML files
    html_files = list(base_dir.glob('*.html'))

    # Add files from subdirectories
    for subdir in ['htdocs_error', 'preview']:
        subdir_path = base_dir / subdir
        if subdir_path.exists():
            html_files.extend(subdir_path.glob('*.html'))

    print(f"\n  Found {Colors.BLUE}{len(html_files)}{Colors.END} HTML file(s)\n")

    # Pre-scan for occurrences
    print(f"  {Colors.CYAN}Pre-scan Results:{Colors.END}")
    counts = count_occurrences(base_dir)
    for text, count in sorted(counts.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"    - '{text}': {count} occurrences")
    print()

    print("-" * 80)
    print(f"\n  {Colors.BOLD}Processing files...{Colors.END}\n")

    updated_count = 0
    skipped_count = 0
    error_count = 0
    all_changes = []

    for html_file in sorted(html_files):
        relative_path = str(html_file)
        success, changes = update_file(html_file)

        if success and changes:
            print(f"  {Colors.GREEN}[OK]{Colors.END} {relative_path}")
            for change in changes[:2]:
                print(f"       {Colors.CYAN}->{Colors.END} {change[:60]}...")
            if len(changes) > 2:
                print(f"       {Colors.CYAN}->{Colors.END} ... and {len(changes) - 2} more changes")
            updated_count += 1
            all_changes.extend(changes)
        elif changes and 'Error' in changes[0]:
            print(f"  {Colors.RED}[ERR]{Colors.END} {relative_path}")
            print(f"       {changes[0]}")
            error_count += 1
        else:
            print(f"  {Colors.YELLOW}[--]{Colors.END} {relative_path} (no changes)")
            skipped_count += 1

    print()
    print("-" * 80)
    print()
    print(f"  {Colors.BOLD}SUMMARY{Colors.END}")
    print(f"  {Colors.GREEN}Updated:{Colors.END}  {updated_count} file(s)")
    print(f"  {Colors.YELLOW}Skipped:{Colors.END}  {skipped_count} file(s)")
    if error_count > 0:
        print(f"  {Colors.RED}Errors:{Colors.END}   {error_count} file(s)")
    print(f"  {Colors.BLUE}Total changes:{Colors.END} {len(all_changes)} replacements")
    print()

    if updated_count > 0:
        print(f"  {Colors.GREEN}Branding updated successfully!{Colors.END}")
        print()
        print(f"  {Colors.BOLD}What was changed:{Colors.END}")
        print("    - Company name: Webwave Digital Trading -> Provena Digital Assets")
        print("    - All name variations (uppercase, lowercase, mixed)")
        print("    - Marketing taglines (paraphrased)")
        print("    - Meta descriptions (paraphrased)")
        print()
        print(f"  {Colors.BOLD}What was preserved:{Colors.END}")
        print("    - Dashboard URLs (dashboard.webwavedigitaltrading.com)")
        print("    - API endpoints and form actions")
        print("    - Team member information")
        print()
        print(f"  {Colors.BOLD}Next steps:{Colors.END}")
        print("    1. Run the HTML updater script to add theme toggle")
        print("    2. Test the website locally")
        print("    3. Verify dashboard login still works")
        print()

    print("=" * 80)
    print()


if __name__ == '__main__':
    main()
