import json, re

with open(r'D:\Projects\mylogoqr\website\index.html', 'r', encoding='utf-8') as f:
    c = f.read()

scripts = re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', c, re.DOTALL)
for i, s in enumerate(scripts):
    try:
        json.loads(s.strip())
        print(f"Script {i}: VALID")
    except Exception as e:
        print(f"Script {i}: INVALID - {e}")
        lines = s.split('\n')
        # Print around error
        for line_num, l in enumerate(lines):
            print(f"{line_num+1:3d}: {l}")
