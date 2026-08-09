const fs = require('fs');
const path = require('path');

const dirPath = __dirname;

const filesToCheck = [
  'index.html',
  'whatsapp-qr-code-generator.html',
  'wifi-qr-code-generator.html',
  'text-qr-code-generator.html',
  'vcard-qr-code-generator.html',
  'about.html',
  'contact.html',
  'privacy.html',
  'terms.html',
  'styles.css',
  'app.js',
  '.htaccess',
  'sitemap.xml',
  'robots.txt',
  'ads.txt'
];

let failed = false;
console.log('==================================================');
console.log('         MYLOGOQR AUTOMATED QA & SEO TEST          ');
console.log('==================================================\n');

// 1. Check file existence
console.log('Step 1: Checking file presence...');
filesToCheck.forEach(file => {
  const filePath = path.join(dirPath, file);
  if (fs.existsSync(filePath)) {
    console.log(`[PASS] Found file: ${file}`);
  } else {
    console.error(`[FAIL] Missing file: ${file}`);
    failed = true;
  }
});
console.log('');

// 2. Validate HTML content (SEO checks & Ad slots)
console.log('Step 2: Performing SEO Meta & Ads checks on HTML...');
const htmlFiles = filesToCheck.filter(f => f.endsWith('.html'));

htmlFiles.forEach(file => {
  const filePath = path.join(dirPath, file);
  if (!fs.existsSync(filePath)) return;

  const content = fs.readFileSync(filePath, 'utf8');
  console.log(`\nValidating file: ${file}`);

  // Title tag
  const titleMatch = content.match(/<title>([^<]+)<\/title>/i);
  if (titleMatch) {
    console.log(`  [PASS] Title: "${titleMatch[1].trim()}"`);
  } else {
    console.error(`  [FAIL] Title tag not found!`);
    failed = true;
  }

  // Meta description
  const metaDesc = content.match(/<meta\s+name="description"\s+content="([^"]+)"/i);
  if (metaDesc) {
    console.log(`  [PASS] Description: "${metaDesc[1].trim()}"`);
  } else {
    console.error(`  [FAIL] Meta description tag not found!`);
    failed = true;
  }

  // Canonical tag
  const canonical = content.match(/<link\s+rel="canonical"\s+href="([^"]+)"/i);
  if (canonical) {
    console.log(`  [PASS] Canonical Link: ${canonical[1]}`);
  } else {
    console.error(`  [FAIL] Canonical Link tag not found!`);
    failed = true;
  }

  // JSON-LD Schema (for tools)
  const isTool = file === 'index.html' || file.includes('generator');
  if (isTool) {
    if (content.includes('application/ld+json')) {
      console.log(`  [PASS] Structured Data JSON-LD Schema found.`);
    } else {
      console.error(`  [FAIL] Structured Data Schema is missing!`);
      failed = true;
    }
  }

  // Ads banners check
  const adsCount = (content.match(/class="adsbygoogle"/g) || []).length;
  const expectedAds = isTool ? 3 : 2; // Generator files have Header, Sidebar, Footer. Secondary have Header, Footer.
  if (adsCount >= expectedAds) {
    console.log(`  [PASS] Found ${adsCount} AdSense slot placeholders (Expected >= ${expectedAds}).`);
  } else {
    console.error(`  [FAIL] Only found ${adsCount} AdSense slots! Expected at least ${expectedAds}.`);
    failed = true;
  }

  // Check for .html inside links
  const htmlLinks = content.match(/href="[^"]+\.html"/gi);
  if (!htmlLinks) {
    console.log(`  [PASS] No raw .html file references found in links (Clean URLs enforced).`);
  } else {
    console.error(`  [FAIL] Found raw .html extension in links: ${htmlLinks.join(', ')}`);
    failed = true;
  }
});
console.log('');

// 3. Sitemap & robots check
console.log('Step 3: Checking Sitemap & Robots index routes...');
const robotsPath = path.join(dirPath, 'robots.txt');
if (fs.existsSync(robotsPath)) {
  const robotsText = fs.readFileSync(robotsPath, 'utf8');
  if (robotsText.includes('Sitemap: https://mylogoqr.com/sitemap.xml')) {
    console.log('[PASS] robots.txt successfully references sitemap.xml');
  } else {
    console.error('[FAIL] robots.txt does not reference the correct sitemap.xml');
    failed = true;
  }
}

const sitemapPath = path.join(dirPath, 'sitemap.xml');
if (fs.existsSync(sitemapPath)) {
  const sitemapText = fs.readFileSync(sitemapPath, 'utf8');
  const countUrls = (sitemapText.match(/<loc>/g) || []).length;
  if (countUrls === 9) {
    console.log(`[PASS] sitemap.xml maps exactly ${countUrls} clean URL routes.`);
  } else {
    console.error(`[FAIL] sitemap.xml has ${countUrls} mapped URLs, expected 9!`);
    failed = true;
  }
}

console.log('\n==================================================');
if (failed) {
  console.error('     QA & SEO VALIDATION STATUS: FAILED ❌        ');
  console.log('==================================================');
  process.exit(1);
} else {
  console.log('     QA & SEO VALIDATION STATUS: PASSED OK ✅     ');
  console.log('==================================================');
  process.exit(0);
}
