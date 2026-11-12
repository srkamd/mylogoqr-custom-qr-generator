import glob, json, re, os

base_dir = r'D:\Projects\mylogoqr\website'
files = glob.glob(os.path.join(base_dir, '**', '*.html'), recursive=True)

valid_count = 0
invalid_count = 0
schema_types_found = set()

for f in files:
    with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
        c = fp.read()
    
    scripts = re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', c, re.DOTALL)
    for s in scripts:
        s_clean = s.strip()
        if not s_clean:
            continue
        try:
            data = json.loads(s_clean)
            valid_count += 1
            if isinstance(data, dict):
                if "@type" in data:
                    schema_types_found.add(data["@type"])
                if "@graph" in data:
                    for item in data["@graph"]:
                        if isinstance(item, dict) and "@type" in item:
                            schema_types_found.add(item["@type"])
        except Exception as e:
            invalid_count += 1
            rel_name = os.path.relpath(f, base_dir)
            print(f"JSON-LD error in {rel_name}: {e}")

print("=" * 60)
print(f"Total valid JSON-LD scripts: {valid_count}")
print(f"Total invalid JSON-LD scripts: {invalid_count}")
print(f"Schema types found: {sorted(list(schema_types_found))}")
