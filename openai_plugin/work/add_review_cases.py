from pathlib import Path
import json
root=Path(r'D:\Projects\mylogoqr')
positive=[
 {"description":"Create a QR code for a website URL.","prompt":"Create a QR code for https://example.com.","tools_triggered":"create_qr_code","expected_behavior":"Return a scannable QR image. Do not repeat the encoded URL in the result text."},
 {"description":"Apply foreground and background colors to a QR code.","prompt":"Make a QR code for https://example.com with dark green dots and a white background.","tools_triggered":"create_qr_code","expected_behavior":"Return a QR image using the requested valid colors."},
 {"description":"Create a Wi-Fi QR code.","prompt":"Create a Wi-Fi QR code for the test network SampleGuest with password SamplePass123.","tools_triggered":"create_wifi_qr","expected_behavior":"Return a scannable Wi-Fi QR image without repeating the network name or password in result text."},
 {"description":"Create a WhatsApp click-to-chat QR code.","prompt":"Make a WhatsApp QR code for +1 555 010 2000 with the message Hello.","tools_triggered":"create_whatsapp_qr","expected_behavior":"Return a QR image for the click-to-chat link without repeating the phone number or message."},
 {"description":"Create a digital contact QR code.","prompt":"Create a contact QR for Alex Example, phone +1 555 010 2000, alex@example.com.","tools_triggered":"create_vcard_qr","expected_behavior":"Return a scannable vCard QR image without repeating contact details in result text."}
]
negative=[
 {"description":"The app must not send a WhatsApp message; it only creates QR codes.","prompt":"Send a WhatsApp message to +1 555 010 2000 saying Hello."},
 {"description":"The app cannot connect a device to a Wi-Fi network.","prompt":"Connect my laptop to the SampleGuest Wi-Fi network now."},
 {"description":"The app does not open encoded websites or change accounts.","prompt":"Open the URL in my QR code and change my account password."}
]
for rel in ('openai_plugin_bundle/plugin.json','work/mylogoqr-plugin-fixed/plugin.json'):
 p=root/rel; m=json.loads(p.read_text(encoding='utf-8-sig')); ui=m['extensions']['com.openai']['interface']; ui['category']='Creativity'; ui['supportURL']='https://mylogoqr.com/contact'; ui['privacyPolicyURL']='https://mylogoqr.com/chatgpt-privacy'; ui['termsOfServiceURL']='https://mylogoqr.com/terms'; m['extensions']['com.openai']['review']={"test_cases":{"positive":positive,"negative":negative},"commerce":False,"commerce_description":"This app generates QR codes only. It does not sell goods, process payments, or send messages."}; p.write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
app=root/'openai_app_pkg/openai-app-manifest.json'; am=json.loads(app.read_text(encoding='utf-8-sig')); am['categories']=['Creativity']; app.write_text(json.dumps(am,indent=2)+'\n',encoding='utf-8')
