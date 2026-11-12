import glob
import os

files = glob.glob(r'D:\Projects\mylogoqr\website\**\*.html', recursive=True)
print(f'Scanning {len(files)} files...')

queries = [
    'Editorial Team',
    'IT Infrastructure Team',
    'Messaging Team',
    'Verified E-E-A-T',
    'Verified EEAT',
    '100% scan reliability',
    'GF(28)',
    '22+',
    '20+',
    '32+',
    '36+'
]

for q in queries:
    matched = []
    for f in files:
        with open(f, 'r', encoding='utf-8') as fp:
            c = fp.read()
        if q.lower() in c.lower():
            rel = os.path.relpath(f, r'D:\Projects\mylogoqr\website')
            matched.append(rel)
    print(f'=== Query "{q}": {len(matched)} files ===')
    for m in matched[:10]:
        print(f'  - {m}')
