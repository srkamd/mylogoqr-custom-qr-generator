from pathlib import Path
root = Path(r"D:\Projects\mylogoqr")
for relative in ("api/index.py", "openai_app_pkg/server.py"):
    p=root/relative
    s=p.read_text(encoding="utf-8-sig")
    s=s.replace(
        '        elif name == "create_wifi_qr":\n            ssid = args.get("ssid", "")',
        '        elif name == "create_wifi_qr":\n            ssid = args.get("ssid", "")\n            if not isinstance(ssid, str) or not ssid.strip():\n                return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32602, "message": "ssid is required."}}'
    )
    s=s.replace(
        '        elif name == "create_whatsapp_qr":\n            phone = "".join(filter(str.isdigit, str(args.get("phone", ""))))',
        '        elif name == "create_whatsapp_qr":\n            phone = "".join(filter(str.isdigit, str(args.get("phone", ""))))\n            if not phone:\n                return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32602, "message": "A phone number with country code is required."}}'
    )
    s=s.replace(
        '            co = args.get("company", "")\n            payload = f"BEGIN:VCARD',
        '            co = args.get("company", "")\n            if not str(fn).strip() or not str(ph).strip():\n                return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32602, "message": "firstName and phone are required for a vCard."}}\n            payload = f"BEGIN:VCARD'
    )
    p.write_text(s,encoding="utf-8")
