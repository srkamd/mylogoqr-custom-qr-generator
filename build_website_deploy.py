import os
import zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
OUTPUT = os.path.join(ROOT, "mylogoqr_website_deploy.zip")
ALLOWED_EXTENSIONS = {
    ".html", ".css", ".js", ".xml", ".txt", ".jpg", ".jpeg", ".png",
    ".svg", ".webp", ".json"
}
EXCLUDED_DIRS = {
    ".git", "node_modules", ".system_generated", "tests", "scripts", "work",
    "openai_app_pkg", "openai_plugin_bundle", "fazier_screenshots", "outputs"
}
EXCLUDED_FILES = {
    "build_zip.py", "build_website_deploy.py", "qa_seo_test.js", "requirements.txt",
    "README.md", "LICENSE", "vercel.json"
}

with zipfile.ZipFile(OUTPUT, "w", zipfile.ZIP_DEFLATED) as archive:
    for current, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        for filename in files:
            if filename in EXCLUDED_FILES or filename.startswith("Screenshot"):
                continue
            if filename.endswith((".log", ".zip", ".py")):
                continue
            extension = os.path.splitext(filename)[1].lower()
            if extension not in ALLOWED_EXTENSIONS and filename.lower() != ".htaccess":
                continue
            source = os.path.join(current, filename)
            relative = os.path.relpath(source, ROOT).replace(os.sep, "/")
            archive.write(source, relative)

with zipfile.ZipFile(OUTPUT) as archive:
    names = archive.namelist()
    required = {"index.html", "chatgpt-privacy.html", ".htaccess", "styles.css", "app.js"}
    missing = required.difference(names)
    if missing:
        raise SystemExit(f"Deployment ZIP is missing required files: {sorted(missing)}")
    if any(name.startswith(("openai_app_pkg/", "openai_plugin_bundle/")) for name in names):
        raise SystemExit("Deployment ZIP unexpectedly contains MCP source files")
    print(f"Created: {OUTPUT}")
    print(f"Files: {len(names)}")
    print(f"Includes ChatGPT privacy notice: {'chatgpt-privacy.html' in names}")
    print(f"Includes .htaccess: {'.htaccess' in names}")

