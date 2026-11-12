import re

with open(r'D:\Projects\mylogoqr\website\wifi-qr-code-generator.html', 'r', encoding='utf-8') as f:
    c = f.read()

print('Byline matches:')
for m in re.finditer(r'<div class="by">.*?</div>', c, re.DOTALL):
    print(repr(m.group(0)))

print('Footer author matches:')
for m in re.finditer(r'<a href="/author".*?</a>', c):
    print(repr(m.group(0)))

print('Tool counts:')
for m in re.finditer(r'\b\d+\+?\s*(?:tools|generators)', c, re.IGNORECASE):
    print(repr(m.group(0)))
