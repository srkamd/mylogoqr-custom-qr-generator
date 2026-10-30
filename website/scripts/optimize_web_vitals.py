"""
Apply Core Web Vitals & Speed Optimization across all HTML files and .htaccess
1. Eliminates CLS (Cumulative Layout Shift) by reserving min-height:320px and aspect-ratio:1/1 on .qrbox
2. Sets explicit width="120" height="36" on Fazier badge image
3. Injects browser caching (mod_expires + Cache-Control 1 year) and GZIP compression into .htaccess
"""

import os
import re

WEBSITE_DIR = r"D:\Projects\mylogoqr\website"
HTACCESS_PATH = os.path.join(WEBSITE_DIR, ".htaccess")

# 1. Update HTML files
updated_html = 0
for root, dirs, files in os.walk(WEBSITE_DIR):
    if "tests" in root or "scripts" in root:
        continue
    for f in files:
        if not f.endswith(".html") or f.startswith("google41b2cdf"):
            continue

        fpath = os.path.join(root, f)
        with open(fpath, "r", encoding="utf-8") as fp:
            c = fp.read()

        modified = False

        # Fix .qrbox CLS
        old_qrbox = ".qrbox{background:#fff;border-radius:20px;padding:14px;display:grid;place-items:center;box-shadow:0 10px 30px rgba(15,23,42,.08);border:1px solid var(--line)}"
        new_qrbox = ".qrbox{background:#fff;border-radius:20px;padding:14px;display:grid;place-items:center;min-height:320px;aspect-ratio:1/1;box-shadow:0 10px 30px rgba(15,23,42,.08);border:1px solid var(--line)}"
        if old_qrbox in c:
            c = c.replace(old_qrbox, new_qrbox)
            modified = True

        # Fix Fazier badge width/height
        old_fazier = 'width="120" alt="Fazier badge" />'
        new_fazier = 'width="120" height="36" alt="Fazier badge" />'
        if old_fazier in c:
            c = c.replace(old_fazier, new_fazier)
            modified = True

        if modified:
            with open(fpath, "w", encoding="utf-8") as fp:
                fp.write(c)
            updated_html += 1

print(f"Updated CLS and image dimensions across {updated_html} HTML files.")

# 2. Update styles.css if present
styles_path = os.path.join(WEBSITE_DIR, "styles.css")
if os.path.exists(styles_path):
    with open(styles_path, "r", encoding="utf-8") as fp:
        sc = fp.read()
    if ".qrbox" in sc and "aspect-ratio" not in sc:
        sc = sc.replace(".qrbox {", ".qrbox {\n  min-height: 320px;\n  aspect-ratio: 1 / 1;")
        with open(styles_path, "w", encoding="utf-8") as fp:
            fp.write(sc)
        print("Updated styles.css with .qrbox min-height & aspect-ratio.")

# 3. Update .htaccess with Speed & Caching rules
if os.path.exists(HTACCESS_PATH):
    with open(HTACCESS_PATH, "r", encoding="utf-8") as fp:
        ht = fp.read()

    speed_rules = """
# ----------------------------------------------------------------------
# Core Web Vitals & Speed Optimization
# ----------------------------------------------------------------------

# 1. Enable GZIP & Deflate Compression
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css text/javascript application/javascript application/x-javascript application/json application/xml image/svg+xml
</IfModule>

# 2. Leverage Browser Caching (1 Year for Static Assets)
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresDefault "access plus 1 month"
  ExpiresByType image/jpg "access plus 1 year"
  ExpiresByType image/jpeg "access plus 1 year"
  ExpiresByType image/png "access plus 1 year"
  ExpiresByType image/svg+xml "access plus 1 year"
  ExpiresByType image/webp "access plus 1 year"
  ExpiresByType image/x-icon "access plus 1 year"
  ExpiresByType text/css "access plus 1 year"
  ExpiresByType text/javascript "access plus 1 year"
  ExpiresByType application/javascript "access plus 1 year"
  ExpiresByType font/woff2 "access plus 1 year"
</IfModule>

# 3. Cache-Control Headers
<IfModule mod_headers.c>
  <FilesMatch "\.(ico|jpe?g|png|gif|svg|webp|css|js|woff2)$">
    Header set Cache-Control "max-age=31536000, public"
  </FilesMatch>
</IfModule>
"""

    if "Core Web Vitals & Speed Optimization" not in ht:
        ht = speed_rules + "\n" + ht
        with open(HTACCESS_PATH, "w", encoding="utf-8") as fp:
            fp.write(ht)
        print("Updated .htaccess with GZIP compression and 1-Year browser caching.")

print("All Core Web Vitals optimizations successfully applied!")
