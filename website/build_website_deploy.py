import os
import zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
WEBSITE_DIR = ROOT
OUTPUT = os.path.join(ROOT, "mylogoqr website 2910.zip")

ALLOWED_EXTENSIONS = {
    ".html", ".css", ".js", ".xml", ".txt", ".jpg", ".jpeg", ".png",
    ".svg", ".webp", ".json"
}
EXCLUDED_DIRS = {".git", "node_modules", ".system_generated", "scripts", "tests", "__pycache__"}
EXCLUDED_FILES = {
    ".gitignore", "Thumbs.db", ".DS_Store", "build_website_deploy.py",
    "build_zip.py", "dev_server.py", "qa_seo_test.js", "README.md", "LICENSE"
}

if os.path.exists(OUTPUT):
    try:
        os.remove(OUTPUT)
    except Exception:
        pass

with zipfile.ZipFile(OUTPUT, "w", zipfile.ZIP_DEFLATED) as archive:
    for current, dirs, files in os.walk(WEBSITE_DIR):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        for filename in files:
            if filename in EXCLUDED_FILES or filename.startswith("."):
                if filename != ".htaccess":
                    continue
            if filename.endswith((".zip", ".log")):
                continue
            extension = os.path.splitext(filename)[1].lower()
            if extension not in ALLOWED_EXTENSIONS and filename.lower() != ".htaccess":
                continue
            source = os.path.join(current, filename)
            relative = os.path.relpath(source, WEBSITE_DIR).replace(os.sep, "/")
            archive.write(source, relative)

with zipfile.ZipFile(OUTPUT) as archive:
    names = archive.namelist()
    required = {"index.html", "chatgpt-privacy.html", ".htaccess", "styles.css", "app.js"}
    missing = required.difference(names)
    if missing:
        raise SystemExit(f"Deployment ZIP is missing required files: {sorted(missing)}")
    print(f"Created: {OUTPUT}")
    print(f"Total Files in ZIP: {len(names)}")
    print(f"Includes ChatGPT privacy notice: {'chatgpt-privacy.html' in names}")
    print(f"Includes .htaccess: {'.htaccess' in names}")
