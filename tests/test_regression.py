"""
MyLogoQR Comprehensive Regression Test Suite
Validates all routes, clean URLs, file integrity, SEO meta tags, sitemap, and robots.txt.
"""

import unittest
import urllib.request
import urllib.error
import re
import os
import xml.etree.ElementTree as ET

BASE_URL = "http://127.0.0.1:8080"
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_all_routes():
    routes = [
        "/",
        "/whatsapp-qr-code-generator",
        "/wifi-qr-code-generator",
        "/text-qr-code-generator",
        "/vcard-qr-code-generator",
        "/how-to-use",
        "/about",
        "/contact",
        "/privacy",
        "/chatgpt-privacy",
        "/terms",
        "/faq",
        "/author",
        "/disclaimer",
        "/cookie-policy",
        "/blog"
    ]
    blog_dir = os.path.join(PROJECT_DIR, 'blog')
    for fname in sorted(os.listdir(blog_dir)):
        if fname.endswith('.html') and fname != 'index.html':
            slug = fname[:-5]
            routes.append(f"/blog/{slug}")
    return routes


STATIC_ASSETS = [
    "/styles.css",
    "/app.js",
    "/manifest.json",
    "/robots.txt",
    "/sitemap.xml",
    "/service-worker.js",
    "/app_icon.jpg"
]


class TestMyLogoQRRegression(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.routes = get_all_routes()

    def fetch_url(self, path):
        url = BASE_URL + path
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) TestRunner/1.0'}
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            content = resp.read().decode('utf-8', errors='replace')
            return resp.status, content

    def test_all_routes_return_200(self):
        for route in self.routes:
            with self.subTest(route=route):
                status, content = self.fetch_url(route)
                self.assertEqual(status, 200, f"Route {route} returned HTTP {status}")
                self.assertGreater(len(content), 500, f"Route {route} returned empty or truncated body")

    def test_all_static_assets_return_200(self):
        for asset in STATIC_ASSETS:
            with self.subTest(asset=asset):
                status, content = self.fetch_url(asset)
                self.assertEqual(status, 200, f"Asset {asset} returned HTTP {status}")
                self.assertGreater(len(content), 20, f"Asset {asset} returned empty body")

    def test_clean_urls_enforced_in_html(self):
        for route in self.routes:
            with self.subTest(route=route):
                _, content = self.fetch_url(route)
                raw_html_links = re.findall(r'href="([^"]+\.html)"', content)
                internal_raw = [
                    link for link in raw_html_links 
                    if not link.startswith('http') and not link.startswith('//')
                ]
                self.assertEqual(
                    internal_raw, [],
                    f"Route {route} contains raw .html link references: {internal_raw}"
                )

    def test_seo_meta_tags_present(self):
        for route in self.routes:
            with self.subTest(route=route):
                _, content = self.fetch_url(route)
                # 1. Title tag
                title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
                self.assertIsNotNone(title_match, f"Route {route} is missing <title>")
                title = title_match.group(1).strip()
                self.assertGreater(len(title), 10, f"Route {route} title is too short: '{title}'")

                # 2. Meta description
                desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=(["\'])(.*?)\1', content, re.IGNORECASE)
                self.assertIsNotNone(desc_match, f"Route {route} is missing <meta name='description'>")
                desc = desc_match.group(2).strip()
                self.assertGreater(len(desc), 30, f"Route {route} description is too short: '{desc}'")

                # 3. Canonical tag
                canonical_match = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']', content, re.IGNORECASE)
                self.assertIsNotNone(canonical_match, f"Route {route} is missing canonical link tag")
                canonical = canonical_match.group(1).strip()
                self.assertTrue(canonical.startswith('https://mylogoqr.com'), f"Invalid canonical {canonical}")

    def test_sitemap_xml_integrity(self):
        sitemap_path = os.path.join(PROJECT_DIR, 'sitemap.xml')
        self.assertTrue(os.path.exists(sitemap_path), "sitemap.xml does not exist")
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

        locs = [elem.text.strip() for elem in root.findall('.//ns:loc', namespace)]
        self.assertEqual(len(locs), len(self.routes), f"Expected {len(self.routes)} mapped URLs, found {len(locs)}")

        for route in self.routes:
            expected_url = f"https://mylogoqr.com{route}" if route != "/" else "https://mylogoqr.com/"
            self.assertIn(expected_url, locs, f"Route {route} missing from sitemap.xml")

    def test_robots_txt_integrity(self):
        robots_path = os.path.join(PROJECT_DIR, 'robots.txt')
        self.assertTrue(os.path.exists(robots_path), "robots.txt does not exist")
        with open(robots_path, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn('User-agent: *', content)
        self.assertIn('Allow: /', content)
        self.assertIn('Sitemap: https://mylogoqr.com/sitemap.xml', content)


if __name__ == '__main__':
    unittest.main(verbosity=2)

