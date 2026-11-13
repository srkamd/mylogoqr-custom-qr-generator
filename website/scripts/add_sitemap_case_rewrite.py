with open(r'D:\Projects\mylogoqr\website\.htaccess', 'r', encoding='utf-8') as f:
    c = f.read()

target = '  # 301 Redirect old / malformed crawler URLs to 200 OK endpoints'

rule = '''  # Normalize sitemap and robots case-insensitively (e.g. SITEMAP.XML -> sitemap.xml)
  RewriteRule ^sitemap\.xml$ sitemap.xml [NC,L]
  RewriteRule ^robots\.txt$ robots.txt [NC,L]

  # 301 Redirect old / malformed crawler URLs to 200 OK endpoints'''

if target in c:
    c = c.replace(target, rule, 1)
    with open(r'D:\Projects\mylogoqr\website\.htaccess', 'w', encoding='utf-8') as f:
        f.write(c)
    print("Added case-insensitive sitemap and robots rewrite to .htaccess!")
else:
    print("Target not found in .htaccess")
