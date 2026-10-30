import os
import shutil

ROOT = r"D:\Projects\mylogoqr"
WEBSITE_DIR = os.path.join(ROOT, "website")
OPENAI_DIR = os.path.join(ROOT, "openai_plugin")
MOBILE_DIR = os.path.join(ROOT, "mobile_app")

os.makedirs(WEBSITE_DIR, exist_ok=True)
os.makedirs(OPENAI_DIR, exist_ok=True)
os.makedirs(MOBILE_DIR, exist_ok=True)

# 1. Directories to move to openai_plugin
OPENAI_DIRS = [
    "api", ".well-known", "openai", "openai_app_pkg", "openai_plugin_bundle", "public"
]
for d in OPENAI_DIRS:
    src = os.path.join(ROOT, d)
    dst = os.path.join(OPENAI_DIR, d)
    if os.path.exists(src):
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.move(src, dst)
        print(f"[Moved Dir -> openai_plugin] {d}")

# 2. Files to move to openai_plugin
OPENAI_FILES = [
    "vercel.json", "requirements.txt", "mylogoqr-reviewer-walkthrough.mp4",
    "mylogoqr-plugin-fixed-final.zip", "mylogoqr-plugin-fixed-v2.zip",
    "mylogoqr-deploy-guide.md"
]
for f in OPENAI_FILES:
    src = os.path.join(ROOT, f)
    dst = os.path.join(OPENAI_DIR, f)
    if os.path.exists(src):
        shutil.move(src, dst)
        print(f"[Moved File -> openai_plugin] {f}")

# 3. Directory to move to website
if os.path.exists(os.path.join(ROOT, "blog")):
    src = os.path.join(ROOT, "blog")
    dst = os.path.join(WEBSITE_DIR, "blog")
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.move(src, dst)
    print("[Moved Dir -> website] blog")

# 4. Files to move to website
# All .html, .css, .js, .xml, .txt, image previews, .htaccess, manifest.json
WEBSITE_EXTENSIONS = {".html", ".css", ".xml", ".txt", ".json", ".htaccess"}
IMAGE_NAMES = {
    "app_icon.jpg", "profile.jpg", "url_preview.jpg", "whatsapp_preview.jpg",
    "wifi_preview.jpg", "text_preview.jpg", "vcard_preview.jpg"
}
SPECIAL_WEB_FILES = {"app.js", "service-worker.js", ".htaccess", "ads.txt", "robots.txt", "sitemap.xml", "manifest.json"}

for item in os.listdir(ROOT):
    item_path = os.path.join(ROOT, item)
    if os.path.isfile(item_path):
        ext = os.path.splitext(item)[1].lower()
        if (
            ext == ".html" or
            item in SPECIAL_WEB_FILES or
            item in IMAGE_NAMES or
            (ext in WEBSITE_EXTENSIONS and item not in OPENAI_FILES)
        ):
            dst = os.path.join(WEBSITE_DIR, item)
            shutil.move(item_path, dst)
            print(f"[Moved File -> website] {item}")

# 5. Mobile App README and template setup
mobile_readme = os.path.join(MOBILE_DIR, "README.md")
with open(mobile_readme, "w", encoding="utf-8") as f:
    f.write("""# MyLogoQR Mobile App

This folder is reserved specifically for the MyLogoQR Mobile Application (Android / iOS / PWA / Flutter).

## Options for Mobile App Deployment:
1. **Trusted Web Activity (TWA) / Android Studio Wrapper**:
   - Packages `https://mylogoqr.com` into a native Google Play Store `.aab` / `.apk`.
   - Native splash screen, push notifications, offline service worker caching.
2. **Flutter / React Native Native Client**:
   - Offline QR Code generation, camera scanner, saved QR code history.
""")
print("[Created] mobile_app/README.md")

print("\n=== Organization Completed Successfully! ===")
