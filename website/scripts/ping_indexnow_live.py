import urllib.request, json

KEY = "c7e4a8b2f9d1e3a6c5b8f2d4e7a1b9c3"
HOST = "mylogoqr.com"

priority_urls = [
    "https://mylogoqr.com/",
    "https://mylogoqr.com/qr-code-types",
    "https://mylogoqr.com/wifi-qr-code-generator",
    "https://mylogoqr.com/whatsapp-qr-code-generator",
    "https://mylogoqr.com/url-qr-code-generator",
    "https://mylogoqr.com/vcard-qr-code-generator",
    "https://mylogoqr.com/google-reviews-qr-code-generator",
    "https://mylogoqr.com/text-qr-code-generator",
    "https://mylogoqr.com/pdf-qr-code-generator",
    "https://mylogoqr.com/instagram-qr-code-generator",
    "https://mylogoqr.com/qr-code-error-correction",
    "https://mylogoqr.com/qr-code-design-guide",
    "https://mylogoqr.com/tools/qr-contrast-checker",
    "https://mylogoqr.com/tools/qr-size-calculator",
    "https://mylogoqr.com/tools/qr-logo-size-checker",
    "https://mylogoqr.com/free-qr-code-generator-comparison",
    "https://mylogoqr.com/blog/how-much-logo-can-a-qr-code-have",
    "https://mylogoqr.com/blog/is-it-safe-to-put-wifi-password-in-qr-code",
    "https://mylogoqr.com/blog/qr-code-with-scan-me-text",
    "https://mylogoqr.com/sitemap.xml",
]

payload = json.dumps({
    "host": HOST,
    "key": KEY,
    "keyLocation": f"https://{HOST}/{KEY}.txt",
    "urlList": priority_urls
}).encode('utf-8')

print("Broadcasting to IndexNow endpoints...")
endpoints = [
    ("Bing / IndexNow Direct", "https://api.indexnow.org/indexnow"),
    ("Bing Direct Endpoint",   "https://www.bing.com/indexnow"),
    ("Yandex Endpoint",        "https://yandex.com/indexnow"),
    ("Naver / Seznam Endpoint", "https://searchadvisor.naver.com/indexnow") # if available
]

for name, api_url in endpoints[:3]:
    try:
        req = urllib.request.Request(
            api_url,
            data=payload,
            headers={
                "Content-Type": "application/json; charset=utf-8",
                "User-Agent": "MyLogoQR-IndexNow-Client/1.0"
            },
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=15) as res:
            print(f"  {name}: {res.status} {res.reason}")
    except Exception as e:
        print(f"  {name}: {e}")
