"""
IndexNow Automated Submission for MyLogoQR.com
Submits all live URLs in sitemap.xml to IndexNow Network (Bing, Yandex, Seznam).
"""

import os
import json
import urllib.request
import xml.etree.ElementTree as ET

HOST = "mylogoqr.com"
KEY = "c7e4a8b2f9d1e3a6c5b8f2d4e7a1b9c3"
KEY_LOCATION = f"https://{HOST}/{KEY}.txt"
WEBSITE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITEMAP_PATH = os.path.join(WEBSITE_DIR, "sitemap.xml")

def get_sitemap_urls():
    tree = ET.parse(SITEMAP_PATH)
    root = tree.getroot()
    urls = []
    for loc in root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
        urls.append(loc.text.strip())
    return urls

def ping_indexnow(urls):
    payload = {
        "host": HOST,
        "key": KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls
    }
    
    data = json.dumps(payload).encode("utf-8")
    endpoints = [
        "https://yandex.com/indexnow",
        "https://api.indexnow.org/IndexNow",
        "https://www.bing.com/indexnow"
    ]
    
    success = False
    for ep in endpoints:
        req = urllib.request.Request(
            ep,
            data=data,
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=12) as response:
                print(f"[IndexNow via {ep}] Status: {response.status} {response.reason}")
                print(f"[IndexNow] Successfully broadcasted {len(urls)} URLs for instant indexing!")
                success = True
                break
        except Exception as e:
            continue
            
    if not success:
        print("[IndexNow Notice] Failed to ping endpoints. Will retry on next build.")
    return success

if __name__ == "__main__":
    urls = get_sitemap_urls()
    print(f"Loaded {len(urls)} URLs from sitemap.xml")
    ping_indexnow(urls)
