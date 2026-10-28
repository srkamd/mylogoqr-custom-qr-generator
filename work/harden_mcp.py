from pathlib import Path
root = Path(r"D:\Projects\mylogoqr")
for relative in ("api/index.py", "openai_app_pkg/server.py"):
    path = root / relative
    src = path.read_text(encoding="utf-8-sig")
    src = src.replace(
        "def escape_wifi_value(value: str) -> str:\n    return re.sub(r'([\\\\;,:\"])', r'\\\\\\1', str(value))\n\n\n",
        "def escape_wifi_value(value: str) -> str:\n    return re.sub(r'([\\\\;,:\"])', r'\\\\\\1', str(value))\n\n\ndef escape_vcard_value(value: str) -> str:\n    text = str(value).replace('\\\\', '\\\\\\\\').replace('\\r\\n', '\\n').replace('\\r', '\\n')\n    text = text.replace('\\n', '\\\\n').replace(',', '\\\\,').replace(';', '\\\\;')\n    return text\n\n\n"
    )
    src = src.replace(
        'payload = f"BEGIN:VCARD\\nVERSION:3.0\\nN:{ln};{fn}\\nFN:{fn} {ln}\\nTEL:{ph}\\nEMAIL:{em}\\nORG:{co}\\nEND:VCARD"',
        'payload = f"BEGIN:VCARD\\nVERSION:3.0\\nN:{escape_vcard_value(ln)};{escape_vcard_value(fn)}\\nFN:{escape_vcard_value(fn)} {escape_vcard_value(ln)}\\nTEL:{escape_vcard_value(ph)}\\nEMAIL:{escape_vcard_value(em)}\\nORG:{escape_vcard_value(co)}\\nEND:VCARD"'
    )
    target = '        data_url = generate_qr_base64(payload, fill_color=dark, back_color=light)'
    validation = '''        if not isinstance(payload, str) or not payload.strip():
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32602, "message": "A non-empty QR value is required."}}
        if len(payload.encode("utf-8")) > 2000:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32602, "message": "QR content is too long. Use 2000 UTF-8 bytes or fewer."}}
        color_pattern = r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$"
        if not isinstance(dark, str) or not re.fullmatch(color_pattern, dark):
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32602, "message": "darkColor must be a 3- or 6-digit hex color."}}
        if not isinstance(light, str) or not re.fullmatch(color_pattern, light):
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32602, "message": "lightColor must be a 3- or 6-digit hex color."}}

'''
    if target not in src:
        raise SystemExit(f"Expected QR generation line not found in {relative}")
    src = src.replace(target, validation + target)
    path.write_text(src, encoding="utf-8")

# Alternate Node server response should not echo sensitive QR payloads.
node_path = root / "openai_app_pkg/server.js"
node = node_path.read_text(encoding="utf-8-sig")
if "**Payload:**" in node:
    raise SystemExit("Payload preview remains in Node server response")
node_path.write_text(node, encoding="utf-8")
