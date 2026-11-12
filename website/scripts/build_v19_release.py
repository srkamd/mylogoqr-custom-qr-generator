import os
import zipfile
import shutil

WEBSITE_DIR = r"D:\Projects\mylogoqr\website"
DEPLOY_DIR = os.path.join(WEBSITE_DIR, "deploy")
os.makedirs(DEPLOY_DIR, exist_ok=True)

v19_zip = os.path.join(DEPLOY_DIR, "mylogoqr-hostinger-production-v19-all-fixed.zip")
latest_zip = os.path.join(DEPLOY_DIR, "mylogoqr-hostinger-production-latest.zip")

for p in [v19_zip, latest_zip]:
    if os.path.exists(p):
        os.remove(p)

print("Building v19 production deployment zip with internal linking mesh...")
with zipfile.ZipFile(v19_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(WEBSITE_DIR):
        rel_root = os.path.relpath(root, WEBSITE_DIR)
        
        # Skip development and build folders
        if any(ignored in rel_root.split(os.sep) for ignored in ['.git', 'node_modules', '.system_generated', 'tests', 'scripts', 'deploy', 'marketing_ads', 'releases']):
            continue
            
        for file in files:
            if file.endswith('.py') or file.endswith('.log') or file.endswith('.zip') or file.startswith('Screenshot'):
                continue
            ext = os.path.splitext(file)[1].lower()
            name = file.lower()
            is_valid = (
                ext in ['.html', '.css', '.js', '.xml', '.txt', '.jpg', '.png', '.json', '.svg', '.webp', '.md'] or
                name in ['.htaccess', 'license']
            )
            if is_valid:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, WEBSITE_DIR)
                archive_name = rel_path.replace('\\', '/')
                zipf.write(full_path, archive_name)

# Copy to latest
shutil.copy2(v19_zip, latest_zip)

file_size_mb = os.path.getsize(v19_zip) / (1024 * 1024)
print(f"Successfully generated {v19_zip} ({file_size_mb:.2f} MB)")

# Verification
with zipfile.ZipFile(v19_zip, 'r') as zipf:
    names = zipf.namelist()
    print(f"Total files in v19 ZIP: {len(names)}")
    must_have = [
        ".htaccess",
        "index.html",
        "og-image.png",
        "wifi-qr-code-generator.html",
        "vcard-qr-code-generator.html",
        "whatsapp-qr-code-generator.html",
        "upi-payment-qr-code-generator.html",
        "free-qr-code-generator-comparison.html",
        "qr-code-error-correction.html",
        "tools/qr-contrast-checker.html",
        "tools/qr-size-calculator.html",
        "tools/qr-logo-size-checker.html"
    ]
    all_ok = True
    for item in must_have:
        if item in names:
            print(f" [PASS] {item}")
        else:
            print(f" [FAIL] MISSING: {item}")
            all_ok = False
            
    print(f"Verification status: {'ALL PASSED' if all_ok else 'SOME FAILED'}")
