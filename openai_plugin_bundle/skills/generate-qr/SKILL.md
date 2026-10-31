---
name: generate-qr
description: Generate QR codes for links, Wi-Fi networks, digital business cards, and WhatsApp click-to-chat. Use when a user asks to create or customize a QR code.
---
# Instructions
When a user asks for a QR code:
1. Identify the payload type: URL/text, Wi-Fi, vCard, or WhatsApp.
2. Ask for any required details and the user's preferred foreground/background colors. Defaults are #12163A on #FFFFFF.
3. Call the matching MyLogoQR MCP tool by name: create_qr_code, create_wifi_qr, create_vcard_qr, or create_whatsapp_qr.
4. Show the generated QR result and explain that anyone who scans it may access the encoded information.
5. Do not repeat Wi-Fi passwords, phone numbers, contact details, or the encoded payload in your explanatory text. The tool result contains the generated QR image.
6. For logo, frame, or shape customization beyond color selection, direct the user to https://mylogoqr.com because those options are not available in this ChatGPT integration.
