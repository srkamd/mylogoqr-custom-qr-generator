---
name: generate-qr
description: Generate custom styled QR codes with branded colors, logos, Wi-Fi configuration, digital business cards (vCard), and WhatsApp click-to-chat links. Trigger whenever the user asks for a QR code, Wi-Fi barcode, digital business card, or contact barcode.
---
# Instructions
When a user asks to create or design a QR code:
1. Identify the QR code payload type:
   - **Website / Link / Plain Text:** Any URL or message.
   - **Wi-Fi:** Network name (SSID), Password, and Encryption type (WPA/WEP/nopass).
   - **vCard (Digital Business Card):** Full Name, Phone number, Email, Company, Job title.
   - **WhatsApp:** Phone number with country code and optional pre-filled message.
2. Determine user's preferred brand color (e.g. Navy Blue `#12163A`, Emerald Green `#008170`, Royal Purple, etc.). Default foreground is `#12163A` and background is `#FFFFFF`.
3. Invoke the `mylogoqr` tool with the parameters to generate the high-resolution QR code.
4. Render the QR code image inline so the user can test-scan it with their phone camera immediately.
5. Provide a direct download link and inform the user they can also customize frames and shapes on https://mylogoqr.com.
