import os
import zipfile
import shutil

WEBSITE_DIR = r"D:\Projects\mylogoqr\website"
DEPLOY_DIR = os.path.join(WEBSITE_DIR, "deploy")
os.makedirs(DEPLOY_DIR, exist_ok=True)

v25_zip = os.path.join(DEPLOY_DIR, "mylogoqr-hostinger-production-v25-all-verified.zip")
latest_zip = os.path.join(DEPLOY_DIR, "mylogoqr-hostinger-production-latest.zip")

for p in [v25_zip, latest_zip]:
    if os.path.exists(p):
        try:
            os.remove(p)
        except Exception:
            pass

print("Building v25 release with all client JS assets included...")
with zipfile.ZipFile(v25_zip, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
    for root, dirs, files in os.walk(WEBSITE_DIR):
        rel_root = os.path.relpath(root, WEBSITE_DIR)
        parts = rel_root.split(os.sep)
        
        # Skip development, git, and deployment folders (EXCEPT client scripts)
        if any(ignored in parts for ignored in ['.git', 'node_modules', '.system_generated', 'tests', 'deploy', 'marketing_ads', 'releases']):
            continue

        is_scripts_dir = (parts[0] == 'scripts')
            
        for file in files:
            # If inside scripts/, only allow .js files (client-side libraries like print-templates.js)
            if is_scripts_dir:
                if not file.endswith('.js'):
                    continue
            else:
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
shutil.copy2(v25_zip, latest_zip)

file_size_mb = os.path.getsize(v25_zip) / (1024 * 1024)
print(f"Successfully generated {v25_zip} ({file_size_mb:.2f} MB)")

# Verify keys & client scripts inside zip
with zipfile.ZipFile(v25_zip, 'r') as zipf:
    names = zipf.namelist()
    critical_files = [
        "scripts/print-templates.js",
        "scripts/smart-app-banner.js",
        "scripts/jsqr.min.js",
        "app.js",
        "theme.js",
        "index.html",
        "4740fd8e98cc418196fa8075e9cd8878.txt",
        "sitemap.xml",
        "robots.txt",
        ".htaccess"
    ]
    all_ok = True
    for k in critical_files:
        if k in names:
            print(f" [PASS] {k}")
        else:
            print(f" [FAIL] MISSING: {k}")
            all_ok = False
            
    print(f"Total files in v25 zip: {len(names)}")
    print(f"Status: {'ALL PASS' if all_ok else 'FAILED'}")
