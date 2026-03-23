#!/usr/bin/env python3
"""
Provena Digital Assets - HTML Theme Updater
=====================================
Propagates theme CSS/JS links and theme toggle button to all HTML pages.
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

# CSS links to add after existing CSS
CSS_LINKS = '''
    <!-- Provena Digital Assets Theme System -->
    <link href="css/theme-variables.css" rel="stylesheet">
    <link href="css/provena-theme.css" rel="stylesheet">'''

# Theme toggle button HTML
THEME_TOGGLE_HTML = '''
                                    <!-- Theme Toggle Button -->
                                    <li class="theme-toggle-wrapper">
                                        <button id="theme-toggle" class="theme-toggle-btn" aria-label="Toggle dark/light mode" title="Toggle theme">
                                            <svg class="sun-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:none;">
                                                <circle cx="12" cy="12" r="5"></circle>
                                                <line x1="12" y1="1" x2="12" y2="3"></line>
                                                <line x1="12" y1="21" x2="12" y2="23"></line>
                                                <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
                                                <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
                                                <line x1="1" y1="12" x2="3" y2="12"></line>
                                                <line x1="21" y1="12" x2="23" y2="12"></line>
                                                <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
                                                <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
                                            </svg>
                                            <svg class="moon-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                                <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
                                            </svg>
                                        </button>
                                    </li>
'''

# JS link to add
JS_LINK = '    <script src="js/theme-toggle.js"></script>'

# Files to skip (already updated or special files)
SKIP_FILES = ['index.html', 'login.html', 'register.html', 'general5445.html']


def update_file(filepath):
    """Update a single HTML file with theme components"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        original_content = content
        changes = []

        # 1. Add CSS links if not already present
        if 'theme-variables.css' not in content:
            # Find where to insert CSS (after css/style.css)
            css_pattern = r'(<link[^>]*href=["\']css/style\.css["\'][^>]*>)'
            if re.search(css_pattern, content):
                content = re.sub(css_pattern, r'\1' + CSS_LINKS, content)
                changes.append('Added theme CSS links')
            else:
                # Try alternate pattern - after any style.css reference
                css_pattern2 = r'(<link[^>]*style\.css[^>]*>)'
                if re.search(css_pattern2, content):
                    content = re.sub(css_pattern2, r'\1' + CSS_LINKS, content, count=1)
                    changes.append('Added theme CSS links')

        # 2. Add theme toggle button if not already present
        if 'theme-toggle' not in content:
            # Find the navigation area - look for Google Translate script end
            # Pattern: end of google translate script block, then insert before </ul>
            toggle_pattern = r'(doGTranslate\(this\);\s*}\s*[^<]*</script>\s*<div id="google_translate_element2"></div>\s*</div>)'
            if re.search(toggle_pattern, content, re.DOTALL):
                content = re.sub(toggle_pattern, r'\1' + THEME_TOGGLE_HTML, content, count=1)
                changes.append('Added theme toggle button')
            else:
                # Alternative: look for end of language selector area
                alt_pattern = r'(select[^>]*onchange="doGTranslate[^"]*"[^>]*>.*?</select>\s*<div id="google_translate_element2"></div>\s*</div>)'
                match = re.search(alt_pattern, content, re.DOTALL)
                if match:
                    insert_pos = match.end()
                    content = content[:insert_pos] + THEME_TOGGLE_HTML + content[insert_pos:]
                    changes.append('Added theme toggle button')

        # 3. Add JS link if not already present
        if 'theme-toggle.js' not in content:
            # Insert after functions.js
            js_pattern = r'(<script src="js/functions\.js"></script>)'
            if re.search(js_pattern, content):
                content = re.sub(js_pattern, r'\1\n' + JS_LINK, content)
                changes.append('Added theme toggle JS')

        # Write changes if any
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, changes

        return False, []

    except Exception as e:
        return False, [f"Error: {str(e)}"]


def main():
    """Main function"""
    print()
    print("=" * 80)
    print(f"{Colors.BOLD}{Colors.CYAN}  PROVENA DIGITAL ASSETS - HTML THEME UPDATER{Colors.END}")
    print("=" * 80)
    print()
    print("  This script adds theme CSS/JS links and toggle button to all HTML pages.")
    print()
    print("-" * 80)

    base_dir = Path('.')

    # Find all HTML files
    html_files = list(base_dir.glob('*.html'))

    # Filter out files to skip
    html_files = [f for f in html_files if f.name not in SKIP_FILES]

    print(f"\n  Found {Colors.BLUE}{len(html_files)}{Colors.END} HTML file(s) to update")
    print(f"  (Skipping: {', '.join(SKIP_FILES)})\n")

    print("-" * 80)
    print(f"\n  {Colors.BOLD}Processing files...{Colors.END}\n")

    updated_count = 0
    skipped_count = 0
    error_count = 0

    for html_file in sorted(html_files):
        success, changes = update_file(html_file)

        if success and changes:
            print(f"  {Colors.GREEN}[OK]{Colors.END} {html_file.name}")
            for change in changes:
                print(f"       {Colors.CYAN}->{Colors.END} {change}")
            updated_count += 1
        elif changes and 'Error' in str(changes):
            print(f"  {Colors.RED}[ERR]{Colors.END} {html_file.name}")
            print(f"       {changes[0]}")
            error_count += 1
        else:
            print(f"  {Colors.YELLOW}[--]{Colors.END} {html_file.name} (already updated or no changes needed)")
            skipped_count += 1

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
        print(f"  {Colors.GREEN}Theme components added successfully!{Colors.END}")
        print()
        print(f"  {Colors.BOLD}What was added:{Colors.END}")
        print("    - CSS links for theme-variables.css and provena-theme.css")
        print("    - Theme toggle button in navigation")
        print("    - JavaScript for theme switching")
        print()

    print("=" * 80)
    print()


if __name__ == '__main__':
    main()
