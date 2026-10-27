"""
MyLogoQR Unit Test Suite
Validates core QR encoding logic, data transformations, sanitization, and algorithms.
"""

import unittest
import re
import urllib.parse


def compile_url(url_input):
    clean = url_input.strip() if url_input else ''
    return clean or 'https://mylogoqr.com'


def compile_whatsapp(phone, message):
    clean_phone = re.sub(r'\D', '', phone) if phone else ''
    if not clean_phone:
        return 'https://wa.me/'
    msg = message.strip() if message else ''
    if msg:
        return f"https://wa.me/{clean_phone}?text={urllib.parse.quote(msg)}"
    return f"https://wa.me/{clean_phone}"


def escape_wifi_string(s):
    if not s:
        return ''
    # Escape special characters per ZXing standard: \ ; , : "
    return re.sub(r'([\\;,:\"])', r'\\\1', str(s))


def compile_wifi(ssid, password, encryption):
    clean_ssid = escape_wifi_string(ssid.strip() if ssid else '')
    clean_pass = escape_wifi_string(password.strip() if password else '')
    enc = encryption.strip() if encryption else 'WPA'
    if enc == 'nopass':
        return f"WIFI:S:{clean_ssid};T:nopass;;"
    return f"WIFI:T:{enc};S:{clean_ssid};P:{clean_pass};;"


def compile_vcard(first, last, phone, email, org, title, url, adr):
    fn = f"{first.strip()} {last.strip()}".strip()
    return (
        "BEGIN:VCARD\n"
        "VERSION:3.0\n"
        f"N:{last.strip()};{first.strip()};;;\n"
        f"FN:{fn}\n"
        f"ORG:{org.strip()}\n"
        f"TITLE:{title.strip()}\n"
        f"TEL;TYPE=CELL:{phone.strip()}\n"
        f"EMAIL:{email.strip()}\n"
        f"URL:{url.strip()}\n"
        f"ADR;TYPE=WORK:;;{adr.strip()};;;;\n"
        "END:VCARD"
    )


def calculate_relative_luminance(hex_color):
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join([c*2 for c in hex_color])
    r = int(hex_color[0:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:6], 16) / 255.0

    def adjust(channel):
        return channel / 12.92 if channel <= 0.03928 else ((channel + 0.055) / 1.055) ** 2.4

    return 0.2126 * adjust(r) + 0.7152 * adjust(g) + 0.0722 * adjust(b)


def calculate_contrast_ratio(hex1, hex2):
    lum1 = calculate_relative_luminance(hex1)
    lum2 = calculate_relative_luminance(hex2)
    brightest = max(lum1, lum2)
    darkest = min(lum1, lum2)
    return (brightest + 0.05) / (darkest + 0.05)


class TestMyLogoQRUnits(unittest.TestCase):

    def test_url_compilation(self):
        self.assertEqual(compile_url('https://example.com/test?q=1'), 'https://example.com/test?q=1')
        self.assertEqual(compile_url('   https://portfolio.dev   '), 'https://portfolio.dev')
        self.assertEqual(compile_url(''), 'https://mylogoqr.com')
        self.assertEqual(compile_url('   '), 'https://mylogoqr.com')

    def test_whatsapp_compilation(self):
        # International formatting and non-digits stripping
        self.assertEqual(compile_whatsapp('+92 (300) 123-4567', 'Hello!'), 'https://wa.me/923001234567?text=Hello%21')
        self.assertEqual(compile_whatsapp('1-800-555-0199', ''), 'https://wa.me/18005550199')
        self.assertEqual(compile_whatsapp('', 'test'), 'https://wa.me/')
        self.assertEqual(compile_whatsapp('923001234567', 'Special chars: & = ?'), 'https://wa.me/923001234567?text=Special%20chars%3A%20%26%20%3D%20%3F')

    def test_wifi_escaping_and_compilation(self):
        # Normal WPA
        self.assertEqual(
            compile_wifi('Office_WiFi', 'SecretPass123', 'WPA'),
            'WIFI:T:WPA;S:Office_WiFi;P:SecretPass123;;'
        )
        # Nopass / Open network
        self.assertEqual(
            compile_wifi('Guest_Open', '', 'nopass'),
            'WIFI:S:Guest_Open;T:nopass;;'
        )
        # Special characters escaping: semicolon, colon, backslash, quote
        self.assertEqual(
            compile_wifi('Office;Net:2', 'Pass;Word"123\\:', 'WPA'),
            'WIFI:T:WPA;S:Office\\;Net\\:2;P:Pass\\;Word\\"123\\\\\\:;;'
        )

    def test_vcard_compilation(self):
        vcard = compile_vcard(
            first='Shahrukh',
            last='Ahmad',
            phone='+1234567890',
            email='srk@example.com',
            org='MyLogoQR',
            title='Founder & Engineer',
            url='https://mylogoqr.com',
            adr='123 Tech Blvd, Suite 100'
        )
        self.assertTrue(vcard.startswith('BEGIN:VCARD\nVERSION:3.0'))
        self.assertTrue(vcard.endswith('END:VCARD'))
        self.assertIn('FN:Shahrukh Ahmad', vcard)
        self.assertIn('N:Ahmad;Shahrukh;;;', vcard)
        self.assertIn('ORG:MyLogoQR', vcard)
        self.assertIn('TITLE:Founder & Engineer', vcard)
        self.assertIn('TEL;TYPE=CELL:+1234567890', vcard)
        self.assertIn('EMAIL:srk@example.com', vcard)
        self.assertIn('URL:https://mylogoqr.com', vcard)
        self.assertIn('ADR;TYPE=WORK:;;123 Tech Blvd, Suite 100;;;;', vcard)

    def test_accessibility_contrast_ratios(self):
        # Slate Ink vs Pure White (Primary text contrast)
        contrast_body = calculate_contrast_ratio('#0A0F1D', '#FFFFFF')
        self.assertGreaterEqual(contrast_body, 7.0, f"Contrast {contrast_body:.2f} must exceed WCAG AAA 7:1")

        # Dark theme background vs White text
        contrast_dark = calculate_contrast_ratio('#080C1A', '#FFFFFF')
        self.assertGreaterEqual(contrast_dark, 15.0)

        # Primary brand indigo #4F46E5 on white
        contrast_brand = calculate_contrast_ratio('#4F46E5', '#FFFFFF')
        self.assertGreaterEqual(contrast_brand, 4.5, "Primary button contrast must meet WCAG AA 4.5:1")


if __name__ == '__main__':
    unittest.main(verbosity=2)
