
import urllib.request, json

KEY = "c7e4a8b2f9d1e3a6c5b8f2d4e7a1b9c3"
HOST = "mylogoqr.com"

new_urls = [
    "https://mylogoqr.com/blog/how-much-logo-can-a-qr-code-have",
    "https://mylogoqr.com/blog/is-it-safe-to-put-wifi-password-in-qr-code",
    "https://mylogoqr.com/blog/qr-code-with-scan-me-text",
    "https://mylogoqr.com/sitemap.xml",
]

payload = json.dumps({
    "host": HOST,
    "key": KEY,
    "keyLocation": f"https://{HOST}/{KEY}.txt",
    "urlList": new_urls
}).encode('utf-8')

for engine, url in [
    ("Bing",    "https://api.indexnow.org/indexnow"),
    ("Yandex",  "https://yandex.com/indexnow"),
]:
    try:
        req = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=15) as r:
            print(f"{engine}: {r.status} {r.reason}")
    except Exception as e:
        print(f"{engine}: ERROR - {e}")
