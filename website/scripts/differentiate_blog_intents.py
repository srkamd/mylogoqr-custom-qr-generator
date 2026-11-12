import os, re

differentiations = {
    "blog/best-free-qr-code-generator-with-logo-no-sign-up.html": {
        "title": "Best Free QR Code Generator with Logo: Free vs Paid Comparison | MyLogoQR",
        "desc": "Independent comparison of free QR code generators with logo: hidden fees, trial expiry traps, scan limits, and how to verify truly free static QR tools."
    },
    "blog/custom-qr-code-generator-with-logo-guide.html": {
        "title": "Branded QR Code Design: Colors, Gradients & Module Shapes Guide | MyLogoQR",
        "desc": "How to design custom branded QR codes with your business colors, linear and radial gradients, custom module shapes, and high-contrast logo embedding."
    },
    "blog/how-to-turn-your-logo-into-a-qr-code.html": {
        "title": "How to Turn Your Logo into a QR Code (Step-by-Step Tutorial) | MyLogoQR",
        "desc": "Step-by-step tutorial: how to turn any PNG or SVG logo into a scannable QR code. Safe sizing (under 30%), transparent padding, and instant testing."
    },
    "blog/qr-code-with-logo-not-scanning-troubleshooting.html": {
        "title": "QR Code with Logo Not Scanning? 9 Fixes That Work | MyLogoQR",
        "desc": "QR code with logo not scanning? Follow the 9 proven fixes in order: logo size, Level H error correction, contrast ratio, quiet zones, and print resolution."
    },
    "blog/custom-qr-codes-with-logos-and-frames-guide.html": {
        "title": "QR Code Error Correction & Frames: Technical Architecture Guide | MyLogoQR",
        "desc": "Deep technical guide to QR code error correction: Reed-Solomon polynomial math, Galois Field GF(2^8), and frame designs that preserve camera scanning."
    }
}

for rel_path, data in differentiations.items():
    p = os.path.join(r"D:\Projects\mylogoqr\website", rel_path)
    if not os.path.exists(p):
        print(f"File not found: {p}")
        continue
    with open(p, "r", encoding="utf-8") as f:
        c = f.read()
    
    # Replace title
    c = re.sub(r'<title>.*?</title>', f'<title>{data["title"]}</title>', c)
    # Replace description
    c = re.sub(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'].*?["\']', f'<meta name="description" content="{data["desc"]}">', c)
    
    with open(p, "w", encoding="utf-8") as f:
        f.write(c)
    print(f"Differentiated intent for {rel_path}")
