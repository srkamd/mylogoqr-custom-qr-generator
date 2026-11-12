import os

changes = {
    "wifi-qr-code-generator.html": (
        "<h1>Secure Wi-Fi QR Code Generator</h1>",
        "<h1>WiFi QR Code Generator with Logo</h1>"
    ),
    "whatsapp-qr-code-generator.html": (
        "<h1>Direct WhatsApp Chat QR Code Generator</h1>",
        "<h1>WhatsApp QR Code Generator with Logo</h1>"
    ),
    "vcard-qr-code-generator.html": (
        "<h1>Digital vCard Business Card QR Code Generator</h1>",
        "<h1>vCard QR Code Generator with Logo</h1>"
    )
}

for fname, (old_h1, new_h1) in changes.items():
    p = os.path.join(r"D:\Projects\mylogoqr\website", fname)
    with open(p, "r", encoding="utf-8") as f:
        c = f.read()
    if old_h1 in c:
        c = c.replace(old_h1, new_h1, 1)
        with open(p, "w", encoding="utf-8") as f:
            f.write(c)
        print(f"Updated H1 in {fname}")
    else:
        print(f"Old H1 not found in {fname}")
