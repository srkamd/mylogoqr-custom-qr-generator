import os
import zipfile

os.chdir(os.path.dirname(os.path.abspath(__file__)))

zip_path = 'mylogoqr_production_build.zip'
if os.path.exists(zip_path):
    os.remove(zip_path)

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk('.'):
        if any(ignored in root for ignored in ['.git', 'node_modules', '.system_generated', 'tests', 'scripts']):
            continue
        for file in files:
            if file == zip_path or file.endswith('.py') or file.endswith('.log') or file.startswith('Screenshot'):
                continue
            ext = os.path.splitext(file)[1].lower()
            name = file.lower()
            is_valid = (
                ext in ['.html', '.css', '.js', '.xml', '.txt', '.jpg', '.png', '.json', '.svg', '.webp', '.md'] or
                name in ['.htaccess', 'license']
            )
            if is_valid:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, '.')
                # Unix forward slash path separator
                archive_name = rel_path.replace('\\', '/')
                zipf.write(full_path, archive_name)

print("ZIP build complete!")
with zipfile.ZipFile(zip_path, 'r') as zipf:
    names = zipf.namelist()
    print(f"Total files in ZIP: {len(names)}")
    blog_count = len([n for n in names if n.startswith('blog/')])
    print(f"Total files in blog/ directory: {blog_count}")
    has_backslash = any('\\' in n for n in names)
    print(f"Any Windows backslashes: {has_backslash}")
