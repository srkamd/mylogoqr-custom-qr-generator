
import zipfile, os, sys
from pathlib import Path

src = Path(r'D:\Projects\mylogoqr\website')
out = Path(r'D:\Projects\mylogoqr\website\deploy\mylogoqr-hostinger-production-v21-blogs-added.zip')

SKIP_DIRS = {'.git', 'deploy', 'scripts', '__pycache__', 'node_modules', '.github'}
SKIP_FILES = {'.gitignore', '.gitattributes'}

errors = []
count = 0

with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
    for root, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for file in files:
            if file in SKIP_FILES or file.endswith('.py'):
                continue
            fp = Path(root) / file
            arcname = fp.relative_to(src)
            try:
                zf.write(fp, arcname)
                count += 1
            except Exception as e:
                errors.append(f"SKIP {fp}: {e}")

size_mb = out.stat().st_size / (1024*1024)
print(f"v21 ZIP created: {out.name}")
print(f"Files: {count} | Size: {size_mb:.2f} MB")
if errors:
    print(f"Skipped {len(errors)} files:")
    for e in errors[:5]:
        print(f"  {e}")
else:
    print("ALL PASSED - no errors")
