import re

INDEX_PATH = r"D:\Projects\mylogoqr\website\index.html"

with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    c = f.read()

# Update Title
c = re.sub(r'<title>.*?</title>', '<title>QR Code Generator with Logo | MyLogoQR</title>', c)

# Update Meta Description
c = re.sub(
    r'<meta[^>]+name=["\']description["\'][^>]+content=["\'].*?["\']',
    '<meta name="description" content="Free QR code generator with logo. No sign-up, no expiry, high-res PNG & SVG.">',
    c
)

# Update OG Title
c = re.sub(
    r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\'].*?["\']',
    '<meta property="og:title" content="QR Code Generator with Logo | MyLogoQR">',
    c
)

# Update OG Description
c = re.sub(
    r'<meta[^>]+property=["\']og:description["\'][^>]+content=["\'].*?["\']',
    '<meta property="og:description" content="Free QR code generator with logo. No sign-up, no expiry, high-res PNG & SVG.">',
    c
)

with open(INDEX_PATH, 'w', encoding='utf-8') as f:
    f.write(c)

print("index.html title & description optimized for Naver (<40 chars title, <80 chars desc) and Google!")
