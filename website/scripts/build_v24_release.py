import os
import zipfile
import shutil

WEBSITE_DIR = r"D:\Projects\mylogoqr\website"
DEPLOY_DIR = os.path.join(WEBSITE_DIR, "deploy")
os.makedirs(DEPLOY_DIR, exist_ok=True)

v24_zip = os.path.join(DEPLOY_DIR, "mylogoqr-hostinger-production-v24-all-verified.zip")
latest_zip = os.path.join(DEPLOY_DIR, "mylogoqr-hostinger-production-latest.zip")

for p in [v24_zip, latest_zip]:
    if os.path.exists(p):
        try:
            os.remove(p)
        except Exception:
            pass

print("Building v24 release with all search engine verification keys...")
with zipfile.ZipFile(v24_zip, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
    for root, dirs, files in os.walk(WEBSITE_DIR):
        rel_root = os.path.relpath(root, WEBSITE_DIR)
        
        # Skip development, git, and deployment folders
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
shutil.copy2(v24_zip, latest_zip)

file_size_mb = os.path.getsize(v24_zip) / (1024 * 1024)
print(f"Successfully generated {v24_zip} ({file_size_mb:.2f} MB)")

# Verify keys inside zip
with zipfile.ZipFile(v24_zip, 'r') as zipf:
    names = zipf.namelist()
    keys_to_check = [
        "53b1e8e51c61c4293568556486f802ea5fe08224ac2130c99dfb9818f8e57a7d.txt",
        "c7e4a8b2f9d1e3a6c5b8f2d4e7a1b9c3.txt",
        "naver11af2f26df510189c340e7a42dc6003a.html",
        "theme.js",
        ".htaccess",
        "robots.txt",
        "sitemap.xml",
        "index.html"
    ]
    all_ok = True
    for k in keys_to_check:
        if k in names:
            print(f" [PASS] {k}")
        else:
            print(f" [FAIL] MISSING: {k}")
            all_ok = False
            
    print(f"Status: {'ALL PASS' if all_ok else 'FAILED'}")
