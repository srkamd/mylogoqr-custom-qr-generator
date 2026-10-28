from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, HTMLResponse, JSONResponse
import qrcode
import io
import base64
import os
import json
import traceback

app = FastAPI(title="MyLogoQR MCP Server", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENAI_CHALLENGE_TOKEN = os.getenv("OPENAI_CHALLENGE_TOKEN", "mylogoqr-openai-verification-token")


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
            title = args.get("label", payload)
        elif name == "create_wifi_qr":
            ssid = args.get("ssid", "")
            pwd = args.get("password", "")
            enc = args.get("encryption", "WPA")
            payload = f"WIFI:S:{ssid};T:{enc};P:{pwd};;"
            title = f"Wi-Fi: {ssid}"
        elif name == "create_whatsapp_qr":
            phone = "".join(filter(str.isdigit, str(args.get("phone", ""))))
            msg = args.get("message", "")
            payload = f"https://wa.me/{phone}" + (f"?text={msg}" if msg else "")
            title = f"WhatsApp: {phone}"
        elif name == "create_vcard_qr":
            fn = args.get("firstName", "")
            ln = args.get("lastName", "")
            ph = args.get("phone", "")
            em = args.get("email", "")
            co = args.get("company", "")
            payload = f"BEGIN:VCARD\nVERSION:3.0\nN:{ln};{fn}\nFN:{fn} {ln}\nTEL:{ph}\nEMAIL:{em}\nORG:{co}\nEND:VCARD"
            title = f"Contact: {fn} {ln}"
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Unknown tool: {name}"}}

        data_url = generate_qr_base64(payload, fill_color=dark, back_color=light)
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "content": [{"type": "text", "text": f"QR Code Created: {title}\n\n![QR]({data_url})\n\nBy MyLogoQR"}]
            }
        }

    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Unknown method: {method}"}}


# ---- Single universal endpoint ----
# Vercel rewrites ALL paths to /api/index.py, so FastAPI always sees path = /api/index.py
# We MUST handle everything in one catch-all.

@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD"])
async def handler(request: Request, full_path: str = ""):
    # --- POST = MCP JSON-RPC (always try) ---
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

    # --- GET: check query params for special paths ---
    qs = str(request.url)

    if "openai-apps-challenge" in qs:
        return PlainTextResponse(OPENAI_CHALLENGE_TOKEN)

    if "health" in qs or full_path.endswith("health"):
        return JSONResponse({"status": "healthy", "app": "MyLogoQR MCP Server", "version": "1.0.0"})

    if "generate" in qs:
        text = request.query_params.get("text", "https://mylogoqr.com")
        color = request.query_params.get("color", "#12163A")
        bg = request.query_params.get("bg", "#FFFFFF")
        b64 = generate_qr_base64(text, fill_color=color, back_color=bg)
        return JSONResponse({"status": "success", "text": text, "qr_base64": b64})

    # --- Browser HTML dashboard ---
    accept = request.headers.get("accept", "")
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

    # --- JSON API info ---
    return JSONResponse({
        "status": "online",
        "app": "MyLogoQR MCP Server",
        "version": "1.0.0",
        "protocol": "MCP JSON-RPC 2024-11-05",
        "mcp_endpoint": "/mcp",
        "tools": ["create_qr_code", "create_wifi_qr", "create_whatsapp_qr", "create_vcard_qr"],
        "website": "https://mylogoqr.com"
    })
