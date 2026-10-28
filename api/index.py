from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, HTMLResponse, JSONResponse
import qrcode
import io
import base64
import os
import json
import re
import urllib.parse

app = FastAPI(title="MyLogoQR MCP Server", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENAI_CHALLENGE_TOKEN = os.getenv("OPENAI_CHALLENGE_TOKEN", "")


def escape_wifi_value(value: str) -> str:
    return re.sub(r'([\\;,:"])', r'\\\1', str(value))


def escape_vcard_value(value: str) -> str:
    text = str(value).replace('\\', '\\\\').replace('\r\n', '\n').replace('\r', '\n')
    text = text.replace('\n', '\\n').replace(',', '\\,').replace(';', '\\;')
    return text


def generate_qr_base64(text: str, fill_color: str = "#12163A", back_color: str = "#FFFFFF") -> str:
    qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=3)
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buffered.getvalue()).decode("utf-8")


MCP_TOOLS = [
    {
        "name": "create_qr_code",
        "description": "Generates a custom styled QR code for any URL or text with custom brand colors.",
        "annotations": {
            "readOnlyHint": True,
            "destructiveHint": False,
            "openWorldHint": False
        },
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "URL or text to encode"},
                "darkColor": {"type": "string", "description": "Hex color for QR dots (e.g. #008170)"},
                "lightColor": {"type": "string", "description": "Hex color for background (e.g. #FFFFFF)"},
                "label": {"type": "string", "description": "Optional title for the QR code"}
            },
            "required": ["text"]
        }
    },
    {
        "name": "create_wifi_qr",
        "description": "Generates a Wi-Fi QR code for smartphones to scan and connect instantly.",
        "annotations": {
            "readOnlyHint": True,
            "destructiveHint": False,
            "openWorldHint": False
        },
        "inputSchema": {
            "type": "object",
            "properties": {
                "ssid": {"type": "string", "description": "Network SSID Name"},
                "password": {"type": "string", "description": "Wi-Fi password"},
                "encryption": {"type": "string", "enum": ["WPA", "WEP", "nopass"], "default": "WPA"},
                "darkColor": {"type": "string", "description": "Hex color code"}
            },
            "required": ["ssid"]
        }
    },
    {
        "name": "create_whatsapp_qr",
        "description": "Generates a click-to-chat WhatsApp QR code with optional pre-filled message.",
        "annotations": {
            "readOnlyHint": True,
            "destructiveHint": False,
            "openWorldHint": False
        },
        "inputSchema": {
            "type": "object",
            "properties": {
                "phone": {"type": "string", "description": "Phone number with country code"},
                "message": {"type": "string", "description": "Optional pre-filled message"},
                "darkColor": {"type": "string", "description": "Hex color code"}
            },
            "required": ["phone"]
        }
    },
    {
        "name": "create_vcard_qr",
        "description": "Generates a digital business card (vCard) QR code with contact info.",
        "annotations": {
            "readOnlyHint": True,
            "destructiveHint": False,
            "openWorldHint": False
        },
        "inputSchema": {
            "type": "object",
            "properties": {
                "firstName": {"type": "string", "description": "First name"},
                "lastName": {"type": "string", "description": "Last name"},
                "phone": {"type": "string", "description": "Phone number"},
                "email": {"type": "string", "description": "Email address"},
                "company": {"type": "string", "description": "Company name"}
            },
            "required": ["firstName", "phone"]
        }
    }
]


def handle_mcp_request(body: dict) -> dict:
    req_id = body.get("id")
    method = body.get("method", "")
    params = body.get("params") or {}

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": "mylogoqr", "version": "1.0.0"}
            }
        }

    if method in ("notifications/initialized", "initialized"):
        return {"jsonrpc": "2.0", "id": req_id, "result": {}}

    if method == "ping":
        return {"jsonrpc": "2.0", "id": req_id, "result": {}}

    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": MCP_TOOLS}}

    if method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        dark = args.get("darkColor", "#12163A")
        light = args.get("lightColor", "#FFFFFF")

        if name == "create_qr_code":
            payload = args.get("text", "")
            title = "QR code"
        elif name == "create_wifi_qr":
            ssid = args.get("ssid", "")
            if not isinstance(ssid, str) or not ssid.strip():
                return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32602, "message": "ssid is required."}}
            pwd = args.get("password", "")
            enc = args.get("encryption", "WPA")
            payload = f"WIFI:S:{escape_wifi_value(ssid)};T:{enc};P:{escape_wifi_value(pwd)};;"
            title = "Wi-Fi QR code"
        elif name == "create_whatsapp_qr":
            phone = "".join(filter(str.isdigit, str(args.get("phone", ""))))
            if not phone:
                return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32602, "message": "A phone number with country code is required."}}
            msg = args.get("message", "")
            payload = f"https://wa.me/{phone}" + (f"?text={urllib.parse.quote(msg, safe='')}" if msg else "")
            title = "WhatsApp QR code"
        elif name == "create_vcard_qr":
            fn = args.get("firstName", "")
            ln = args.get("lastName", "")
            ph = args.get("phone", "")
            em = args.get("email", "")
            co = args.get("company", "")
            if not str(fn).strip() or not str(ph).strip():
                return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32602, "message": "firstName and phone are required for a vCard."}}
            payload = f"BEGIN:VCARD\nVERSION:3.0\nN:{escape_vcard_value(ln)};{escape_vcard_value(fn)}\nFN:{escape_vcard_value(fn)} {escape_vcard_value(ln)}\nTEL:{escape_vcard_value(ph)}\nEMAIL:{escape_vcard_value(em)}\nORG:{escape_vcard_value(co)}\nEND:VCARD"
            title = "Contact QR code"
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Unknown tool: {name}"}}

        if not isinstance(payload, str) or not payload.strip():
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32602, "message": "A non-empty QR value is required."}}
        if len(payload.encode("utf-8")) > 2000:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32602, "message": "QR content is too long. Use 2000 UTF-8 bytes or fewer."}}
        color_pattern = r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$"
        if not isinstance(dark, str) or not re.fullmatch(color_pattern, dark):
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32602, "message": "darkColor must be a 3- or 6-digit hex color."}}
        if not isinstance(light, str) or not re.fullmatch(color_pattern, light):
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32602, "message": "lightColor must be a 3- or 6-digit hex color."}}

        data_url = generate_qr_base64(payload, fill_color=dark, back_color=light)
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "content": [{"type": "text", "text": f"QR Code Created: {title}\n\n![QR]({data_url})\n\nBy MyLogoQR"}]
            }
        }

    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Unknown method: {method}"}}


@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD"])
async def handler(request: Request, full_path: str = ""):
    # 1. POST is ALWAYS handled as MCP JSON-RPC
    if request.method == "POST":
        try:
            raw = await request.body()
            if raw:
                body = json.loads(raw.decode("utf-8"))
                if isinstance(body, dict) and "method" in body:
                    result = handle_mcp_request(body)
                    return JSONResponse(result)
        except Exception as e:
            return JSONResponse({
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": f"Parse error: {str(e)}"}
            }, status_code=200)

    # 2. Check original requested URL using Vercel headers or ASGI scope
    headers = dict(request.headers)
    req_path = (
        headers.get("x-matched-path")
        or headers.get("x-vercel-matched-path")
        or headers.get("x-original-url")
        or headers.get("x-forwarded-uri")
        or request.scope.get("raw_path", b"").decode("utf-8", errors="ignore")
        or str(request.url.path)
    )

    # 3. Domain verification for OpenAI challenge (MUST be plain text!)
    if "openai-apps-challenge" in req_path:
        return PlainTextResponse(OPENAI_CHALLENGE_TOKEN)

    # 4. Health endpoint
    if "health" in req_path:
        return JSONResponse({"status": "healthy", "app": "MyLogoQR MCP Server", "version": "1.0.0"})

    # 5. Direct QR test generation
    if "generate" in req_path:
        text = request.query_params.get("text", "https://mylogoqr.com")
        color = request.query_params.get("color", "#12163A")
        bg = request.query_params.get("bg", "#FFFFFF")
        b64 = generate_qr_base64(text, fill_color=color, back_color=bg)
        return JSONResponse({"status": "success", "text": text, "qr_base64": b64})

    # 6. Browser HTML dashboard
    accept = headers.get("accept", "")
    if "text/html" in accept:
        return HTMLResponse(content="""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>MyLogoQR MCP Server</title>
<style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:system-ui;background:#0B0F19;color:#F8FAFC;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:24px}.c{max-width:600px;background:rgba(22,27,46,.75);border:1px solid rgba(255,255,255,.08);border-radius:20px;padding:36px;backdrop-filter:blur(20px);box-shadow:0 25px 50px rgba(0,0,0,.5)}.b{display:inline-flex;align-items:center;gap:8px;padding:5px 12px;border-radius:999px;background:rgba(20,184,166,.15);border:1px solid rgba(20,184,166,.4);color:#2DD4BF;font-size:.8rem;font-weight:700;letter-spacing:.5px;text-transform:uppercase;margin-bottom:16px}.dot{width:8px;height:8px;border-radius:50%;background:#2DD4BF;box-shadow:0 0 10px #2DD4BF;animation:p 1.8s infinite}@keyframes p{0%,100%{opacity:1}50%{opacity:.4}}h1{font-size:1.8rem;font-weight:800;margin-bottom:8px}p{color:#94A3B8;line-height:1.6;margin-bottom:20px}.g{display:grid;gap:12px;margin-bottom:20px}.card{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);border-radius:12px;padding:14px}.card .l{font-size:.75rem;color:#94A3B8;text-transform:uppercase;letter-spacing:.5px;margin-bottom:2px}.card .v{font-family:monospace;color:#A5B4FC;font-weight:600}a.btn{display:inline-block;background:linear-gradient(135deg,#14B8A6,#0D9488);color:#fff;padding:12px 24px;border-radius:10px;text-decoration:none;font-weight:700;margin-top:8px}</style>
</head><body><div class="c">
<div class="b"><div class="dot"></div>MCP Server Online</div>
<h1>MyLogoQR AI Engine</h1>
<p>Serverless MCP backend for ChatGPT, Codex &amp; Claude. Generates branded QR codes via AI tools.</p>
<div class="g">
<div class="card"><div class="l">MCP Endpoint</div><div class="v">POST /mcp</div></div>
<div class="card"><div class="l">Tools Available</div><div class="v">create_qr_code, create_wifi_qr, create_whatsapp_qr, create_vcard_qr</div></div>
<div class="card"><div class="l">Protocol</div><div class="v">MCP JSON-RPC 2024-11-05</div></div>
</div>
<a class="btn" href="https://mylogoqr.com" target="_blank">Visit MyLogoQR.com &rarr;</a>
</div></body></html>""")

    # 7. Fallback API status
    return JSONResponse({
        "status": "online",
        "app": "MyLogoQR MCP Server",
        "version": "1.0.0",
        "protocol": "MCP JSON-RPC 2024-11-05",
        "mcp_endpoint": "/mcp",
        "tools": ["create_qr_code", "create_wifi_qr", "create_whatsapp_qr", "create_vcard_qr"],
        "website": "https://mylogoqr.com"
    })

