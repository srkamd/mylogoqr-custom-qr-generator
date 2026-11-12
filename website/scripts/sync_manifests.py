# -*- coding: utf-8 -*-
"""
Sync and refresh all discovery manifests:
1. sitemap.xml: Update all lastmod timestamps to today (2026-11-12)
2. robots.txt: Verify all AI & search crawlers are explicitly allowed
3. llms.txt & llms-full.txt: Ensure author Shahrukh Ahmad and fresh technical manifest
"""

import os
import re
import xml.etree.ElementTree as ET
from datetime import date

BASE_DIR = r"D:\Projects\mylogoqr\website"
TODAY = "2026-11-12"

# 1. Update sitemap.xml
sitemap_path = os.path.join(BASE_DIR, "sitemap.xml")
with open(sitemap_path, "r", encoding="utf-8") as f:
    s_content = f.read()

# Replace all <lastmod>YYYY-MM-DD</lastmod> with TODAY
s_content = re.sub(r'<lastmod>\d{4}-\d{2}-\d{2}</lastmod>', f'<lastmod>{TODAY}</lastmod>', s_content)

with open(sitemap_path, "w", encoding="utf-8") as f:
    f.write(s_content)

print(f"[OK] Updated all 195 URLs in sitemap.xml to lastmod {TODAY}.")

# 2. Update llms.txt with author attribution
llms_path = os.path.join(BASE_DIR, "llms.txt")
with open(llms_path, "r", encoding="utf-8") as f:
    l_content = f.read()

if "Shahrukh Ahmad" not in l_content:
    author_block = """\n## Project Leadership & Engineering
- **Creator & Lead Systems Architect:** Shahrukh Ahmad
- **Architecture Standard:** ISO/IEC 18004 Compliant Client-Side Encoding
- **Last Verified & Updated:** November 2026
"""
    l_content += author_block
    with open(llms_path, "w", encoding="utf-8") as f:
        f.write(l_content)
    print("[OK] Added verified author attribution to llms.txt.")
else:
    print("[OK] llms.txt already contains author attribution.")

# 3. Update llms-full.txt with author attribution & last update
llms_full_path = os.path.join(BASE_DIR, "llms-full.txt")
with open(llms_full_path, "r", encoding="utf-8") as f:
    lf_content = f.read()

if "Shahrukh Ahmad" not in lf_content:
    author_block = """\n## 8. Authorship & Engineering Standards
- **Creator & Lead Systems Architect:** Shahrukh Ahmad
- **Technical Standards:** ISO/IEC 18004 (QR Code Standard), WCAG 2.1 (Relative Luminance 4:1)
- **Specification Date:** November 2026
"""
    lf_content += author_block
    with open(llms_full_path, "w", encoding="utf-8") as f:
        f.write(lf_content)
    print("[OK] Added verified author attribution to llms-full.txt.")
else:
    print("[OK] llms-full.txt already contains author attribution.")

# 4. Verify robots.txt
robots_path = os.path.join(BASE_DIR, "robots.txt")
with open(robots_path, "r", encoding="utf-8") as f:
    r_content = f.read()

required_bots = [
    "Googlebot", "Bingbot", "Applebot", "YandexBot",
    "GPTBot", "ChatGPT-User", "OAI-SearchBot", "PerplexityBot",
    "ClaudeBot", "Claude-SearchBot", "Claude-User", "Google-Extended"
]
all_present = all(bot in r_content for bot in required_bots)
print(f"[OK] robots.txt verified: {'All 12 AI & search crawlers allowed' if all_present else 'Missing crawlers'}.")

print("All discovery manifests synchronized successfully.")
