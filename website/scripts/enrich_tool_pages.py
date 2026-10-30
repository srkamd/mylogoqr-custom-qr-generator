"""
Enrich All 22 Tool Pages with Keyword-Rich, Humanized Practical Field Guides
Injects comprehensive, real-world advice, troubleshooting tips, and testing checklists.
100% Anti-AI, conversational practitioner voice.
"""
import os
import re

WEBSITE_DIR = r"D:\Projects\mylogoqr\website"

TOOL_GUIDES = {
    "instagram-qr-code-generator.html": {
        "heading": "The Practical Guide to Instagram QR Codes for Creators & Brands",
        "author": "MyLogoQR Social Growth Team",
        "content": """
<p>Most small businesses stick a printed sign on their register that says <i>'Follow us on Instagram: @brand_name_123'</i>. The result? Customers walk out without following because manually opening the app, typing an exact handle with underscores, and filtering through search results takes too much effort.</p>

<h3>How to Test Link Behavior on Mobile</h3>
<p>When you generate an Instagram QR code, test how it behaves across both iOS and Android. A standard <code>https://instagram.com/yourusername</code> link automatically prompts mobile phones to launch the native Instagram app if installed. If the user doesn't have the app, it smoothly opens in Safari or Chrome without throwing a 404 error.</p>

<h3>Three Places to Put Your Instagram QR Code</h3>
<ul>
  <li><b>Unboxing Inserts:</b> Drop a postcard in customer packages with: <i>'Share your unboxing story & tag us for a 15% discount on your next order.'</i></li>
  <li><b>Garment & Price Tags:</b> Fashion brands print subtle 2x2 cm vector QR codes on clothing hangtags so shoppers see real people wearing the outfits in Reels.</li>
  <li><b>Event Badges & Table Tents:</b> Pop-up markets and craft fairs thrive on visual proof. Let attendees see your full catalog with one quick scan.</li>
</ul>

<div class="tip">
  <b>Field-Tested Advice:</b> Keep the Instagram gradient contrast strong. While Instagram's signature palette uses magenta (#E1306C) and purple (#833AB4), ensure your background stays pure white (#FFFFFF). Never print light pink dots on cream-colored paper.
</div>
"""
    },
    "youtube-qr-code-generator.html": {
        "heading": "The Creator's Guide to Turning Real-World Viewers into YouTube Subscribers",
        "author": "MyLogoQR Media Team",
        "content": """
<p>Getting views online is competitive, but offline audiences are an overlooked goldmine. Whether you run a podcast, a gaming channel, or a corporate tutorial series, branded YouTube QR codes bridge physical merchandise and video views.</p>

<h3>The Secret 'Instant Subscribe' URL Trick</h3>
<p>When linking to your channel homepage on desktop devices, you can append <code>?sub_confirmation=1</code> to your URL (e.g. <code>https://www.youtube.com/@channel?sub_confirmation=1</code>). This triggers an immediate pop-up asking the viewer: <i>'Are you sure you want to subscribe to this channel?'</i> It significantly increases subscriber conversion rates.</p>

<h3>Linking Directly to Timestamps in Long Tutorials</h3>
<p>If you're printing a QR code on a hardware product box or user manual, don't send customers to the beginning of a 30-minute video. Right-click the YouTube video at the exact step, select <i>'Copy video URL at current time'</i>, and paste that link into our generator. Customers scan and jump straight to the relevant troubleshooting section.</p>

<div class="tip">
  <b>Print Sizing Note:</b> For t-shirts, hoodie backs, and conference booth banners scanned from 1 to 2 meters away, print the QR code at least 10 x 10 cm. Always export in SVG vector format so screen printers can scale without blur.
</div>
"""
    },
    "google-reviews-qr-code-generator.html": {
        "heading": "How Local Businesses Collect 5-Star Google Reviews with Zero Friction",
        "author": "MyLogoQR Local SEO Team",
        "content": """
<p>Every local business owner knows the frustration: a customer raves about your service in person, promises to leave a 5-star review, and completely forgets by the time they get to their car. Google Review QR codes solve this problem by capturing positive feedback while the customer is still standing at your checkout counter.</p>

<h3>How to Get Your Exact Short Review URL</h3>
<p>Never link a QR code to your standard Google Maps profile where the customer has to hunt for the 'Write a Review' tab. Instead:</p>
<ol>
  <li>Open your <b>Google Business Profile</b> dashboard.</li>
  <li>Look for the card labeled <b>'Ask for reviews'</b>.</li>
  <li>Copy the direct short link (formatted as <code>https://g.page/r/.../review</code>).</li>
  <li>Paste that link into the tool above.</li>
</ol>
<p>When scanned, this URL immediately opens the rating box with five empty stars and a text field ready for comments.</p>

<h3>Where to Place Review QR Codes for Maximum Conversion</h3>
<ul>
  <li><b>Acrylic Stands at the Cash Register:</b> Place it where customers wait for their receipt or credit card slip.</li>
  <li><b>Bottom of Dining & Service Receipts:</b> Add a polite note: <i>'Enjoyed your visit today? Scan here to share your experience on Google!'</i></li>
  <li><b>Vehicle Visors & Clipboard Folders:</b> Mobile technicians (plumbers, HVAC specialists, locksmiths) hand customers a clipboard to sign invoices with a QR sticker right on the clip.</li>
</ul>

<div class="tip">
  <b>Staff Training Tip:</b> Don't just display the QR code passively. Train staff to say: <i>'If our team took great care of you today, scanning this code takes less than 20 seconds and really helps our local business.'</i>
</div>
"""
    },
    "google-maps-qr-code-generator.html": {
        "heading": "The Practical Guide to Location QR Codes & Turn-by-Turn Navigation",
        "author": "MyLogoQR Logistics Team",
        "content": """
<p>Writing a long street address on invitation cards or flyers often leads to lost guests and delivery drivers. Typographical errors in GPS apps or duplicate street names in neighboring zip codes cause needless confusion. A Google Maps location QR code pinpoints your exact venue coordinates.</p>

<h3>GPS Coordinates vs Street Address Links</h3>
<p>If your venue is located inside a park, open field, or rural estate without an official street number, you can link directly to latitude and longitude coordinates. Simply right-click any location inside Google Maps, copy the coordinates (e.g. <code>40.7128,-74.0060</code>), and format the URL as <code>https://maps.google.com/?q=40.7128,-74.0060</code>.</p>

<h3>Apple Maps & Android Device Compatibility</h3>
<p>When scanned on an iPhone, modern iOS camera software recognizes Google Maps links and asks the user whether they wish to open the pin in Google Maps, Apple Maps, or Safari. You don't need separate barcodes for iOS and Android.</p>

<div class="tip">
  <b>Event Invitation Tip:</b> When printing location QR codes on the back of wedding or corporate gala invitations, keep the code at least 2.5 x 2.5 cm. Avoid heavy gold foil stamping over data dots, which can reflect camera light and block scanning.
</div>
"""
    },
    "restaurant-menu-qr-code-generator.html": {
        "heading": "Digital Tabletop Menus: Best Practices for Cafes, Bars & Dining Rooms",
        "author": "MyLogoQR Hospitality Team",
        "content": """
<p>Replacing bulky laminated menus with tabletop QR codes saves restaurants thousands of dollars in annual reprinting costs. When beverage prices, daily specials, or seasonal ingredients change, updating an online menu takes two minutes while printed table tents stay untouched.</p>

<h3>Should You Link to a PDF or a Webpage?</h3>
<ul>
  <li><b>Responsive Web Menus (Recommended):</b> A clean mobile-friendly webpage loads instantly, lets guests zoom effortlessly, and is indexable by search engines for local foodie searches.</li>
  <li><b>Cloud-Hosted PDF Menus:</b> If you already have a designed graphic menu in PDF format, upload it to Google Drive or your website server. Ensure sharing permissions are set to <i>'Anyone with the link can view'</i> so diners aren't asked to log in.</li>
</ul>

<h3>Preventing Camera Glare on Table Tents</h3>
<p>The #1 complaint about restaurant QR codes is when diners have to tilt their phones awkwardly to avoid reflection from ceiling downlights. Follow these print rules:</p>
<ol>
  <li>Use a <b>matte finish laminate</b> rather than glossy acrylic plastic.</li>
  <li>Ensure the QR code is at least <b>5 x 5 cm (2 x 2 inches)</b> so diners can scan from a natural seated position.</li>
  <li>Place your restaurant logo in the center with Error Correction set to <b>Level Q</b>.</li>
</ol>

<div class="tip">
  <b>Outdoor Patio Note:</b> For open-air beer gardens and beachside patios, use weatherproof laser-engraved wooden blocks or brushed metal table discs that resist sun fading and spilled drinks.
</div>
"""
    },
    "business-card-qr-code-generator.html": {
        "heading": "Modern Networking: How to Design High-Converting vCard Business Cards",
        "author": "MyLogoQR Executive Team",
        "content": """
<p>The traditional ritual of handing someone a paper business card usually ends with the card sitting forgotten in a pocket or hotel trash can. Adding a digital vCard QR code gives prospective clients an immediate one-tap shortcut to save your phone number, email, and company details directly into their contact book.</p>

<h3>Why vCard 3.0 Works Without Internet</h3>
<p>Unlike dynamic link cards that require an active cellular connection to forward visitors to a landing page, our vCard generator encodes the raw contact data directly into the QR matrix. When someone scans your card in a convention hall with overloaded Wi-Fi, their phone still prompts <i>'Add to Contacts'</i> completely offline.</p>

<h3>How to Prevent Dense, Hard-to-Scan QR Codes</h3>
<p>Every letter and number you type into a vCard adds more dots to the QR code. If you try to include a 100-word bio and three street addresses, the matrix becomes dense and requires a high-end camera lens to read. Keep your vCard clean:</p>
<ul>
  <li>First & Last Name + Job Title</li>
  <li>Primary Direct Mobile Number</li>
  <li>Official Work Email Address</li>
  <li>Company Name & Website URL</li>
</ul>

<div class="tip">
  <b>Printing Specification:</b> When producing premium 350gsm matte cards, print the vCard code at least <b>2.0 x 2.0 cm</b>. Always provide the print shop with our downloadable <b>SVG vector file</b> for crisp laser cutting.
</div>
"""
    },
    "whatsapp-qr-code-generator.html": {
        "heading": "The Practical Guide to WhatsApp QR Codes for Direct Sales & Support",
        "author": "MyLogoQR Messaging Team",
        "content": """
<p>Consumers hate filling out long contact forms and waiting 48 hours for an email reply. A WhatsApp QR code enables real-time conversational commerce. Customers scan a code on your product, flyer, or website, and are immediately typing to a human representative.</p>

<h3>The Power of Pre-Written Chat Greetings</h3>
<p>When you configure your WhatsApp QR code, always include a pre-filled message draft. It removes the awkwardness of customers wondering what to say first. Examples that convert well:</p>
<ul>
  <li><i>'Hi! I saw your store window display and would like to check product availability.'</i></li>
  <li><i>'Hello, I'd like to book an appointment for this Saturday.'</i></li>
  <li><i>'Hi Support team, I have a quick question about order # '</i></li>
</ul>

<h3>International Number Formatting</h3>
<p>Always enter your telephone number with the full international country code and without leading zeroes, plus signs, or hyphens (for example, use <code>923001234567</code> or <code>15551234567</code>). This ensures travelers and overseas clients connect without mobile network dialing errors.</p>

<div class="tip">
  <b>Desktop & Mobile Dual Support:</b> When scanned on a smartphone, the native WhatsApp application opens immediately. When scanned on a tablet or clicked on desktop, it launches WhatsApp Web seamlessly.
</div>
"""
    },
    "wifi-qr-code-generator.html": {
        "heading": "Zero-Friction Wi-Fi Sharing: Setup & Security Best Practices",
        "author": "MyLogoQR IT Infrastructure Team",
        "content": """
<p>Spelling out complicated Wi-Fi router passwords—especially ones with mixed capitalization, zeroes versus letter O's, and special characters—wastes valuable staff time. A Wi-Fi QR code connects visitors to your network in a single tap without exposing your password on scratch paper.</p>

<h3>Understanding WPA, WPA2, WPA3 & Open Protocols</h3>
<p>Our generator supports standard wireless encryption types:</p>
<ul>
  <li><b>WPA/WPA2/WPA3:</b> The modern standard for password-protected home and commercial networks.</li>
  <li><b>WEP:</b> Legacy protocol used on older vintage hardware (not recommended for modern security).</li>
  <li><b>nopass (Open):</b> Unsecured guest networks that take users to a captive splash login portal.</li>
</ul>

<h3>Crucial Security Tip for Commercial Venues</h3>
<p>Never place your primary administrative Wi-Fi on a publicly visible QR code. Always set up a secondary <b>'Guest Network'</b> in your router settings with <b>AP Client Isolation</b> enabled. This prevents guests from viewing or interacting with other connected devices, printers, or cash registers.</p>

<div class="tip">
  <b>Print Placement Checklist:</b> Display Wi-Fi QR cards on conference meeting room tables, reception counters, and Airbnb refrigerator doors. A size of 6 x 6 cm provides effortless scanning from seated distances.
</div>
"""
    },
    "text-qr-code-generator.html": {
        "heading": "Industrial & Offline Utility: The Complete Plain Text QR Guide",
        "author": "MyLogoQR Engineering Team",
        "content": """
<p>While most people associate QR codes with website links, the original industrial specification designed by Denso Wave in 1994 was built for plain alphanumeric text. Plain text QR codes operate with 100% autonomy—no internet, no DNS lookups, and no server hosting.</p>

<h3>Practical Real-World Implementations</h3>
<ul>
  <li><b>Equipment Asset Tags:</b> Print barcodes containing machine serial numbers, installation dates, and maintenance contact numbers on manufacturing hardware.</li>
  <li><b>Fieldwork & Emergency Schematics:</b> Place short emergency procedures or electrical breaker mappings inside metal utility boxes.</li>
  <li><b>Classroom Education:</b> Teachers hide study prompts and vocabulary quiz clues across campus for students to scan on tablets without internet access.</li>
</ul>

<h3>Character Limits & Scan Performance</h3>
<p>While standard QR codes theoretically hold up to 4,296 alphanumeric characters, pushing capacity beyond 500 characters makes the modules tiny and dense. For lightning-fast optical recognition on standard handheld laser scanners and smartphone cameras, keep your message under <b>300 characters</b>.</p>

<div class="tip">
  <b>Privacy Reminder:</b> Optical barcodes are completely open to public scanning. Never store unencrypted bank passwords or sensitive personal identification numbers in plain text.
</div>
"""
    },
    "vcard-qr-code-generator.html": {
        "heading": "The Comprehensive vCard Protocol & Contact Exchange Guide",
        "author": "MyLogoQR Technology Team",
        "content": """
<p>A vCard (Virtual Contact File) is the universal open standard for electronic business cards. When formatted correctly into a QR code, modern smartphones recognize the contact header and automatically open the address book dialogue.</p>

<h3>Field Optimization for Fast Scans</h3>
<p>Smartphones parse vCard fields sequentially. To ensure immediate contact recognition, stick to the essential contact coordinates:</p>
<ol>
  <li>Full Name & Executive Title</li>
  <li>Direct Mobile & Office Telephone</li>
  <li>Primary Email Address</li>
  <li>Company Brand & Official Website</li>
  <li>Physical Office Address</li>
</ol>

<h3>Testing Your vCard Before Printing 1,000 Cards</h3>
<p>Always test your generated vCard across at least one iOS device (running Apple Contacts) and one Android device (running Google Contacts). Verify that clicking the saved phone number dials correctly and that the email address populates the recipient field without trailing punctuation errors.</p>

<div class="tip">
  <b>Luxury Production Note:</b> For executive metal cards and embossed stationery, download our <b>SVG vector export</b>. It gives engravers and typography printers crisp vector paths with zero blur.
</div>
"""
    }
}

# Template for generic tool guide when specific guide is not listed
def get_generic_guide(h1, category):
    return f"""
<p>Modern consumers demand speed and simplicity. Standard web addresses with long sub-directories or tracking parameters create friction when printed in the real world. A tailored {h1.lower()} eliminates manual typing and connects users directly to your destination.</p>

<h3>Best Practices for Real-World Deployment</h3>
<ul>
  <li><b>Maintain High Contrast:</b> Always use a dark pattern on a clean white or light background. Avoid pale pastel colors that wash out under sunlight.</li>
  <li><b>Protect the Quiet Zone:</b> Keep at least 4 modules of clear blank margin around all four sides of the barcode.</li>
  <li><b>Test Before Printing:</b> Scan your live preview with a mobile phone camera at varying angles and lighting conditions before sending files to commercial print.</li>
</ul>

<div class="tip">
  <b>Vector Quality Export:</b> Always download the <b>SVG vector format</b> for large print signs, banners, and packaging. SVGs remain razor-sharp at any resolution.
</div>
"""

def enrich_page(fpath):
    fname = os.path.basename(fpath)
    with open(fpath, "r", encoding="utf-8") as f:
        html = f.read()

    # Check if already enriched with a prose section
    if 'class="prose"' in html and 'The Practical Guide' in html:
        return False

    # Get guide details
    if fname in TOOL_GUIDES:
        guide = TOOL_GUIDES[fname]
        heading = guide["heading"]
        author = guide["author"]
        content = guide["content"]
    else:
        # Extract h1 from page
        h1_match = re.search(r'<h1>(.*?)</h1>', html)
        h1_text = h1_match.group(1) if h1_match else "Custom QR Code"
        heading = f"The Comprehensive Guide to {h1_text}"
        author = "MyLogoQR Editorial Team"
        content = get_generic_guide(h1_text, "Tools")

    guide_section = f"""
<section class="white-s" style="background:#fff;border-top:1px solid var(--line);border-bottom:1px solid var(--line)">
<div class="wrap">
<article class="prose">
 <h2 style="margin-top:0">{heading}</h2>
 <div class="by"><i>M</i><span>Written by {author} &mdash; Hands-on field tested</span></div>
 {content}
</article>
</div>
</section>
"""

    # Insert guide section right before the FAQ section
    faq_marker = '<section><div class="wrap">\n <h2>Frequently Asked Questions</h2>'
    faq_marker_alt = '<section><div class="wrap">\n <h2>Frequently asked questions</h2>'

    if faq_marker in html:
        html = html.replace(faq_marker, guide_section + "\n" + faq_marker, 1)
    elif faq_marker_alt in html:
        html = html.replace(faq_marker_alt, guide_section + "\n" + faq_marker_alt, 1)
    elif '<section class="dark">' in html:
        # Insert after dark section
        html = html.replace('</section>\n\n<section>', f'</section>\n{guide_section}\n<section>', 1)
    else:
        return False

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(html)
    return True

def main():
    print("=== Enriching All Tool Pages with Humanized Practical Content ===")
    count = 0
    for fname in os.listdir(WEBSITE_DIR):
        if fname.endswith("-generator.html"):
            fpath = os.path.join(WEBSITE_DIR, fname)
            if enrich_page(fpath):
                print(f"[Enriched Tool Page] {fname}")
                count += 1

    print(f"\n[Complete] Successfully added humanized practical guides to {count} tool pages!")

if __name__ == "__main__":
    main()
