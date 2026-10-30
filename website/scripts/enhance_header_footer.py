"""
Enhance Header Navigation (Professional word) and Footer Description across all HTML files
"""
import os
import re

WEBSITE_DIR = r"D:\Projects\mylogoqr\website"

OLD_NAV_ITEM = r'<li><a href="/qr-code-types"[^>]*>.*?</a></li>'
NEW_NAV_ITEM = r'<li><a href="/qr-code-types" style="color:var(--p);font-weight:600">Generators</a></li>'

OLD_FOOTER_P = r'<p>\s*Free,\s*private\s*QR\s*code\s*generator\s*with\s*custom\s*logos,\s*gradients\s*and\s*shapes\.?\s*</p>'
NEW_FOOTER_P = (
    r'<p style="font-size:0.92rem;line-height:1.65;color:#94A3B8;max-width:320px;margin-top:8px">'
    r'The leading free, client-side custom QR code generator for creators, businesses, and designers. '
    r'Create high-resolution vector barcodes with custom logos, gradient styling, and 100% private data security.'
    r'</p>'
)

updated_count = 0
for root, dirs, files in os.walk(WEBSITE_DIR):
    if "tests" in root or "scripts" in root:
        continue
    for fname in files:
        if fname.endswith(".html"):
            fpath = os.path.join(root, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()

            modified = False

            # Replace nav item
            if "qr-code-types" in content:
                content = re.sub(OLD_NAV_ITEM, NEW_NAV_ITEM, content)
                modified = True

            # Replace footer description
            if re.search(OLD_FOOTER_P, content, re.IGNORECASE):
                content = re.sub(OLD_FOOTER_P, NEW_FOOTER_P, content, flags=re.IGNORECASE)
                modified = True

            if modified:
                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(content)
                rel = os.path.relpath(fpath, WEBSITE_DIR)
                print(f"[Enhanced Header & Footer] {rel}")
                updated_count += 1

print(f"\n[Complete] Successfully enhanced {updated_count} HTML files!")
