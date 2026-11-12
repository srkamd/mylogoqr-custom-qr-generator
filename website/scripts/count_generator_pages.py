import glob

pattern = ":root{--ink:#0A0F1D;--ink2:#1E293B;--ink3:#475569;--bg:#F8FAFC;--card:#fff;--line:#E2E8F0;"
files = glob.glob(r'D:\Projects\mylogoqr\website\**\*.html', recursive=True)

matching = []
for f in files:
    with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
        c = fp.read()
    if pattern in c:
        matching.append(f)

print(f"Total files with exact generator style block: {len(matching)}")
print("Sample files:")
for m in matching[:15]:
    print(" ", m.replace(r'D:\Projects\mylogoqr\website\\', ''))
