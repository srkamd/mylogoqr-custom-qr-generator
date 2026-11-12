import glob, os

files = glob.glob(r'D:\Projects\mylogoqr\website\**\*.html', recursive=True)
has_tool_card = []
for f in files:
    with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
        c = fp.read()
    if '.tool-card' in c:
        has_tool_card.append(f)

print(f"Files with .tool-card: {len(has_tool_card)}")
for h in has_tool_card:
    print(" ", h.replace(r'D:\Projects\mylogoqr\website\\', ''))
