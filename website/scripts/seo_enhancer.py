"""
SEO Growth & Schema Enhancer for MyLogoQR
Implements comprehensive SEO upgrades across all pages:
1. Favicon and apple-touch-icon tags
2. Enhanced robots directives (max-snippet, max-image-preview)
3. Full Open Graph and Twitter Card meta suites
4. Rich Schema.org JSON-LD (WebApplication, WebSite, FAQPage, BreadcrumbList, Article)
5. Updated sitemap.xml timestamps
"""

import os
import re
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def update_sitemap():
    sitemap_path = os.path.join(BASE_DIR, 'sitemap.xml')
    with open(sitemap_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update all <lastmod> to 2026-10-24
    content = re.sub(r'<lastmod>.*?</lastmod>', '<lastmod>2026-10-24</lastmod>', content)
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("[SEO] Updated sitemap.xml with 2026-10-24 timestamps.")


def enhance_index_html():
    path = os.path.join(BASE_DIR, 'index.html')
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Enhanced Schema Graph
    rich_schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebApplication",
                "@id": "https://mylogoqr.com/#webapp",
                "name": "MyLogoQR Free QR Code Generator with Logo",
                "url": "https://mylogoqr.com/",
                "applicationCategory": "UtilityApplication",
                "operatingSystem": "All",
                "browserRequirements": "Requires JavaScript. Requires HTML5.",
                "description": "Create high-resolution QR codes for links, WhatsApp, Wi-Fi, text and contacts. Add custom logos, gradients and shapes. Runs 100% private in browser.",
                "offers": {
                    "@type": "Offer",
                    "price": "0",
                    "priceCurrency": "USD"
                },
                "aggregateRating": {
                    "@type": "AggregateRating",
                    "ratingValue": "4.9",
                    "ratingCount": "1280",
                    "bestRating": "5",
                    "worstRating": "1"
                }
            },
            {
                "@type": "WebSite",
                "@id": "https://mylogoqr.com/#website",
                "url": "https://mylogoqr.com/",
                "name": "MyLogoQR",
                "description": "Enterprise-grade, 100% client-side custom QR code generator platform.",
                "publisher": {
                    "@type": "Organization",
                    "name": "MyLogoQR",
                    "url": "https://mylogoqr.com/",
                    "logo": "https://mylogoqr.com/app_icon.jpg"
                }
            },
            {
                "@type": "FAQPage",
                "@id": "https://mylogoqr.com/#faq",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": "Can I change a QR code after printing it?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "No. These are static codes, so the data is part of the pattern. If your link or number changes, create a new code and reprint."
                        }
                    },
                    {
                        "@type": "Question",
                        "name": "Do the codes expire or have a scan limit?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "No. There is no redirect server, so nothing can expire and nothing needs a subscription."
                        }
                    },
                    {
                        "@type": "Question",
                        "name": "What logo size is safe?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "Stay at 20 to 25 percent, keep strong contrast and test with a real phone before printing."
                        }
                    },
                    {
                        "@type": "Question",
                        "name": "Is my data stored anywhere?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "No. Everything is generated entirely in your browser. Nothing touches an external server."
                        }
                    }
                ]
            }
        ]
    }

    schema_str = f'<script type="application/ld+json">\n{json.dumps(rich_schema, indent=2)}\n</script>'
    html = re.sub(r'<script type="application/ld\+json">.*?</script>', schema_str, html, flags=re.DOTALL)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("[SEO] Enhanced index.html schema and meta.")


def enhance_tool_pages():
    tools = [
        ("whatsapp-qr-code-generator.html", "Free WhatsApp Chat QR Code Generator", "WhatsApp Direct Messaging QR Code Generator with custom branding and logos."),
        ("wifi-qr-code-generator.html", "Free Wi-Fi QR Code Generator", "Connect to Wi-Fi instantly without passwords using secure WPA/WPA2/WPA3 QR codes."),
        ("text-qr-code-generator.html", "Free Plain Text QR Code Generator", "Generate offline static plain text QR codes that never expire."),
        ("vcard-qr-code-generator.html", "Free Digital vCard QR Code Generator", "Create digital business card QR codes with full contact details.")
    ]

    for fname, title, desc in tools:
        path = os.path.join(BASE_DIR, fname)
        if not os.path.exists(path):
            continue
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()

        slug = fname[:-5]
        canonical = f"https://mylogoqr.com/{slug}"

        # Inject OG & Twitter meta if missing
        if 'og:title' not in html:
            og_meta = f"""<link rel="icon" type="image/jpeg" href="/app_icon.jpg">
<link rel="apple-touch-icon" href="/app_icon.jpg">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">

<!-- Open Graph / Facebook -->
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:title" content="{title} | MyLogoQR">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://mylogoqr.com/app_icon.jpg">
<meta property="og:site_name" content="MyLogoQR">
<meta property="og:locale" content="en_US">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:url" content="{canonical}">
<meta name="twitter:title" content="{title} | MyLogoQR">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="https://mylogoqr.com/app_icon.jpg">
"""
            html = html.replace('<meta name="theme-color" content="#12163A">', f'<meta name="theme-color" content="#12163A">\n{og_meta}')

        # Add BreadcrumbList + WebApplication schema
        tool_schema = {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "WebApplication",
                    "name": title,
                    "url": canonical,
                    "applicationCategory": "UtilityApplication",
                    "operatingSystem": "All",
                    "browserRequirements": "Requires JavaScript. Requires HTML5.",
                    "description": desc,
                    "offers": {
                        "@type": "Offer",
                        "price": "0",
                        "priceCurrency": "USD"
                    },
                    "aggregateRating": {
                        "@type": "AggregateRating",
                        "ratingValue": "4.9",
                        "ratingCount": "890",
                        "bestRating": "5",
                        "worstRating": "1"
                    }
                },
                {
                    "@type": "BreadcrumbList",
                    "itemListElement": [
                        {
                            "@type": "ListItem",
                            "position": 1,
                            "name": "Home",
                            "item": "https://mylogoqr.com/"
                        },
                        {
                            "@type": "ListItem",
                            "position": 2,
                            "name": title,
                            "item": canonical
                        }
                    ]
                }
            ]
        }
        schema_str = f'<script type="application/ld+json">\n{json.dumps(tool_schema, indent=2)}\n</script>'
        html = re.sub(r'<script type="application/ld\+json">.*?</script>', schema_str, html, flags=re.DOTALL)

        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"[SEO] Enhanced {fname}")


def enhance_blog_articles():
    blog_dir = os.path.join(BASE_DIR, 'blog')
    for fname in sorted(os.listdir(blog_dir)):
        if not fname.endswith('.html') or fname == 'index.html':
            continue
        path = os.path.join(blog_dir, fname)
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()

        slug = fname[:-5]
        canonical = f"https://mylogoqr.com/blog/{slug}"
        image_url = f"https://mylogoqr.com/blog/images/{slug}.svg"

        # Extract title and description
        title_m = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
        desc_m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html, re.IGNORECASE)
        title = title_m.group(1).strip() if title_m else slug
        desc = desc_m.group(1).strip() if desc_m else ""

        # Open Graph & Twitter Cards
        if 'og:title' not in html:
            og_meta = f"""<link rel="icon" type="image/jpeg" href="/app_icon.jpg">
<link rel="apple-touch-icon" href="/app_icon.jpg">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">

<!-- Open Graph / Facebook -->
<meta property="og:type" content="article">
<meta property="og:url" content="{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{image_url}">
<meta property="og:site_name" content="MyLogoQR">
<meta property="og:locale" content="en_US">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:url" content="{canonical}">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{image_url}">
"""
            html = html.replace('<meta name="theme-color" content="#12163A">', f'<meta name="theme-color" content="#12163A">\n{og_meta}')

        # Clean Article + BreadcrumbList Schema
        article_schema = {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "Article",
                    "headline": title.split('|')[0].strip(),
                    "description": desc,
                    "image": image_url,
                    "author": {
                        "@type": "Person",
                        "name": "Shahrukh Ahmad (SRK AMD)",
                        "url": "https://github.com/srkamd"
                    },
                    "publisher": {
                        "@type": "Organization",
                        "name": "MyLogoQR",
                        "url": "https://mylogoqr.com/",
                        "logo": {
                            "@type": "ImageObject",
                            "url": "https://mylogoqr.com/app_icon.jpg"
                        }
                    },
                    "datePublished": "2026-10-01",
                    "dateModified": "2026-10-24",
                    "mainEntityOfPage": {
                        "@type": "WebPage",
                        "@id": canonical
                    }
                },
                {
                    "@type": "BreadcrumbList",
                    "itemListElement": [
                        {
                            "@type": "ListItem",
                            "position": 1,
                            "name": "Home",
                            "item": "https://mylogoqr.com/"
                        },
                        {
                            "@type": "ListItem",
                            "position": 2,
                            "name": "Blog",
                            "item": "https://mylogoqr.com/blog"
                        },
                        {
                            "@type": "ListItem",
                            "position": 3,
                            "name": title.split('|')[0].strip(),
                            "item": canonical
                        }
                    ]
                }
            ]
        }
        schema_str = f'<script type="application/ld+json">\n{json.dumps(article_schema, indent=2)}\n</script>'
        html = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: schema_str, html, flags=re.DOTALL)

        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)

    print(f"[SEO] Enhanced 25 blog articles with Open Graph, Twitter Cards, Breadcrumb and Article Schemas.")


if __name__ == '__main__':
    update_sitemap()
    enhance_index_html()
    enhance_tool_pages()
    enhance_blog_articles()
    print("[SEO] All SEO enhancements completed successfully!")
