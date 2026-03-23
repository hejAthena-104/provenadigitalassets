#!/usr/bin/env python3
"""
Provena Digital Assets - Navigation & Structure Fix Script
=====================================================
Fixes HTML structure issues across all pages:
1. Malformed stylesheet links
2. Navigation structure (properly close ul before non-list elements)
3. Ensures theme toggle is in correct position
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

# Main pages to fix (in root directory)
MAIN_PAGES = [
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
    'investmentplan.html',
    'legals.html',
    'login.html',
    'newcrypto.html',
    'oilandgas.html',
    'ourteam.html',
    'privacy.html',
    'realestate.html',
    'register.html',
    'risk-disclosure.html',
    'stocks.html',
    'terms.html',
    'transactions.html',
]

# Theme toggle HTML to insert
THEME_TOGGLE_HTML = '''<li class="theme-toggle-wrapper">
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
</ul>'''


def fix_stylesheet_link(content):
    """Fix malformed stylesheet link"""
    # Pattern: href="general5445.html?id=" followed by digits and >
    pattern = r'href="general5445\.html\?id="\s*(\d+)>'
    replacement = r'href="general5445.html?id=\1">'

    new_content, count = re.subn(pattern, replacement, content)
    return new_content, count > 0


def fix_navigation_structure(content):
    """
    Fix navigation structure:
    1. Find the My Account dropdown closing </li></ul></li>
    2. Add theme toggle and close the main nav <ul> properly
    3. Move styles, scripts, divs outside the ul
    """
    changes_made = []

    # Check if theme toggle already exists correctly positioned
    if '<li class="theme-toggle-wrapper">' in content and '</ul>\n</nav>' in content:
        return content, []

    # Pattern to find the My Account dropdown end and what follows
    # Looking for: </ul></li> followed by <style or similar inside nav

    # First, let's check if theme toggle is incorrectly placed (after non-li elements inside ul)
    # We need to restructure so theme toggle comes right after My Account, then </ul>

    # Find the My Account dropdown section
    my_account_pattern = r'(<li class="dropdown"><a href="#">My Account</a>\s*<ul class="dropdown-menu">.*?</ul>\s*</li>)'

    match = re.search(my_account_pattern, content, re.DOTALL)
    if not match:
        return content, []

    my_account_end = match.end()

    # Check what comes after My Account
    after_my_account = content[my_account_end:my_account_end + 2000]

    # If there's a <style immediately after (inside the ul), we need to restructure
    if re.match(r'\s*<style', after_my_account):
        changes_made.append("Restructured navigation (moved styles/scripts outside ul)")

        # Find where </ul>\n</nav> is
        nav_end_match = re.search(r'</ul>\s*</nav>', content[my_account_end:], re.DOTALL)
        if nav_end_match:
            # Get everything between my_account_end and </ul></nav>
            middle_content = content[my_account_end:my_account_end + nav_end_match.start()]

            # Extract styles
            styles = re.findall(r'<style[^>]*>.*?</style>', middle_content, re.DOTALL)

            # Extract the parent_cont div (translation)
            parent_cont = re.search(r'<div class="parent_cont">.*?</div>\s*</div>', middle_content, re.DOTALL)
            parent_cont_html = parent_cont.group(0) if parent_cont else ''

            # Extract scripts (but not external script includes)
            scripts = re.findall(r'<script[^>]*>.*?</script>', middle_content, re.DOTALL)

            # Check if theme toggle already exists in middle
            has_toggle = '<li class="theme-toggle-wrapper">' in middle_content

            # Build new structure
            new_middle = '\n'

            # Add theme toggle if not present
            if not has_toggle:
                new_middle += THEME_TOGGLE_HTML
                changes_made.append("Added theme toggle to navigation")
            else:
                # Extract existing toggle
                toggle_match = re.search(r'<li class="theme-toggle-wrapper">.*?</li>', middle_content, re.DOTALL)
                if toggle_match:
                    new_middle += toggle_match.group(0) + '\n</ul>'

            # Add the non-list elements outside the ul
            new_middle += '\n<!-- Language Selector -->\n'
            for style in styles:
                new_middle += style + '\n'
            if parent_cont_html:
                new_middle += parent_cont_html + '\n'
            for script in scripts:
                new_middle += script + '\n'

            # Replace the middle section
            new_content = (
                content[:my_account_end] +
                new_middle +
                '\n</nav>' +
                content[my_account_end + nav_end_match.end():]
            )

            return new_content, changes_made

    # If structure is already somewhat OK, just ensure theme toggle exists
    if '<li class="theme-toggle-wrapper">' not in content:
        # Add theme toggle before </ul></nav>
        content = re.sub(
            r'(</ul>\s*</nav>)',
            THEME_TOGGLE_HTML.replace('</ul>', '') + '\n\\1',
            content,
            count=1
        )
        changes_made.append("Added theme toggle")

    return content, changes_made


def ensure_theme_css_js(content):
    """Ensure theme CSS and JS are included in head/body"""
    changes = []

    # Check for theme CSS
    if 'theme-variables.css' not in content:
        # Add after style.css
        content = re.sub(
            r'(href="css/style\.css"[^>]*>)',
            r'\1\n    <!-- Provena Digital Assets Theme System -->\n    <link href="css/theme-variables.css" rel="stylesheet">\n    <link href="css/provena-theme.css" rel="stylesheet">',
            content,
            count=1
        )
        changes.append("Added theme CSS links")

    # Check for theme JS
    if 'theme-toggle.js' not in content:
        # Add before </body>
        content = re.sub(
            r'(</body>)',
            '    <script src="js/theme-toggle.js"></script>\n\\1',
            content,
            count=1
        )
        changes.append("Added theme JS")

    return content, changes


def fix_file(filepath):
    """Fix a single HTML file"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        original = content
        all_changes = []

        # Fix 1: Stylesheet link
        content, fixed = fix_stylesheet_link(content)
        if fixed:
            all_changes.append("Fixed malformed stylesheet link")

        # Fix 2: Navigation structure
        content, nav_changes = fix_navigation_structure(content)
        all_changes.extend(nav_changes)

        # Fix 3: Ensure theme CSS/JS
        content, theme_changes = ensure_theme_css_js(content)
        all_changes.extend(theme_changes)

        # Write if changed
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, all_changes

        return False, []

    except Exception as e:
        return False, [f"Error: {str(e)}"]


def main():
    print()
    print("=" * 80)
    print(f"{Colors.BOLD}{Colors.CYAN}  PROVENA DIGITAL ASSETS - PAGE STRUCTURE FIX{Colors.END}")
    print("=" * 80)
    print()
    print("  Fixes HTML structure issues across all pages:")
    print(f"    {Colors.BLUE}•{Colors.END} Malformed stylesheet links")
    print(f"    {Colors.BLUE}•{Colors.END} Navigation ul/li structure")
    print(f"    {Colors.BLUE}•{Colors.END} Theme toggle positioning")
    print(f"    {Colors.BLUE}•{Colors.END} Theme CSS/JS includes")
    print()
    print("-" * 80)

    base_dir = Path('.')

    # Filter to only existing files
    files_to_fix = [f for f in MAIN_PAGES if (base_dir / f).exists()]

    print(f"\n  Found {Colors.BLUE}{len(files_to_fix)}{Colors.END} page(s) to process\n")
    print("-" * 80)
    print(f"\n  {Colors.BOLD}Processing files...{Colors.END}\n")

    fixed_count = 0
    skipped_count = 0

    for filename in sorted(files_to_fix):
        filepath = base_dir / filename
        success, changes = fix_file(filepath)

        if success and changes:
            print(f"  {Colors.GREEN}[OK]{Colors.END} {filename}")
            for change in changes[:3]:
                print(f"       {Colors.CYAN}→{Colors.END} {change}")
            if len(changes) > 3:
                print(f"       {Colors.CYAN}→{Colors.END} ... and {len(changes) - 3} more")
            fixed_count += 1
        else:
            print(f"  {Colors.YELLOW}[--]{Colors.END} {filename} (no changes needed)")
            skipped_count += 1

    print()
    print("-" * 80)
    print()
    print(f"  {Colors.BOLD}SUMMARY{Colors.END}")
    print(f"  {Colors.GREEN}Fixed:{Colors.END}    {fixed_count} file(s)")
    print(f"  {Colors.YELLOW}Skipped:{Colors.END}  {skipped_count} file(s)")
    print()

    if fixed_count > 0:
        print(f"  {Colors.GREEN}Page structure fixes applied successfully!{Colors.END}")
        print()

    print("=" * 80)
    print()


if __name__ == '__main__':
    main()
