from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import qrcode
import io
import base64
import os
import uvicorn

app = FastAPI(title="MyLogoQR OpenAI App & MCP Server", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENAI_CHALLENGE_TOKEN = os.getenv("OPENAI_CHALLENGE_TOKEN", "mylogoqr-openai-verification-token")

HTML_DASHBOARD = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MyLogoQR — OpenAI App & MCP Backend</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #0B0F19;
            --card-bg: rgba(22, 27, 46, 0.75);
            --border: rgba(255, 255, 255, 0.08);
            --accent: #6366F1;
            --accent-glow: rgba(99, 102, 241, 0.35);
            --teal: #14B8A6;
            --text-main: #F8FAFC;
            --text-muted: #94A3B8;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: var(--bg);
            background-image: 
                radial-gradient(at 15% 15%, rgba(99, 102, 241, 0.18) 0px, transparent 50%),
                radial-gradient(at 85% 85%, rgba(20, 184, 166, 0.15) 0px, transparent 50%);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 24px;
        }
        .container {
            max-width: 780px;
            width: 100%;
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 24px;
            backdrop-filter: blur(20px);
            padding: 40px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5), 0 0 40px var(--accent-glow);
        }
        .badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 14px;
            border-radius: 9999px;
            background: rgba(20, 184, 166, 0.15);
            border: 1px solid rgba(20, 184, 166, 0.4);
            color: #2DD4BF;
            font-size: 0.85rem;
            font-weight: 700;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            margin-bottom: 20px;
        }
        .pulse-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #2DD4BF;
            box-shadow: 0 0 10px #2DD4BF;
            animation: pulse 1.8s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.4; transform: scale(0.85); }
        }
        h1 {
            font-size: 2.2rem;
            font-weight: 800;
            background: linear-gradient(135deg, #FFFFFF 30%, #A5B4FC 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 12px;
        }
        p.subtitle {
            color: var(--text-muted);
            font-size: 1.05rem;
            line-height: 1.6;
            margin-bottom: 28px;
        }
        .links-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
            margin-bottom: 32px;
        }
        .link-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 16px;
            transition: all 0.2s ease;
            text-decoration: none;
            color: inherit;
            display: block;
        }
        .link-card:hover {
            background: rgba(99, 102, 241, 0.1);
            border-color: rgba(99, 102, 241, 0.5);
            transform: translateY(-2px);
        }
        .link-card .label {
            font-size: 0.8rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 4px;
        }
        .link-card .val {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.95rem;
            color: #A5B4FC;
            font-weight: 600;
        }
        .tester-box {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 28px;
        }
        .tester-box h3 {
            font-size: 1.1rem;
            margin-bottom: 12px;
            color: #E2E8F0;
        }
        .input-row {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
        }
        input[type="text"] {
            flex: 1;
            min-width: 200px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 10px;
            padding: 12px 16px;
            color: white;
            font-size: 0.95rem;
            outline: none;
        }
        input[type="text"]:focus {
            border-color: var(--accent);
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.25);
        }
        button.btn-test {
            background: linear-gradient(135deg, #6366F1, #4F46E5);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 12px 24px;
            font-weight: 700;
            font-size: 0.95rem;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        button.btn-test:hover {
            box-shadow: 0 8px 20px -4px rgba(99, 102, 241, 0.6);
            transform: translateY(-1px);
        }
        #qr-result {
            margin-top: 20px;
            display: none;
            text-align: center;
        }
        #qr-result img {
            border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.4);
            border: 4px solid white;
            max-width: 180px;
        }
        .cta-row {
            display: flex;
            gap: 16px;
            flex-wrap: wrap;
            align-items: center;
            justify-content: space-between;
            padding-top: 16px;
            border-top: 1px solid var(--border);
        }
        .btn-website {
            background: linear-gradient(135deg, #14B8A6, #0D9488);
            color: white;
            padding: 14px 28px;
            border-radius: 12px;
            text-decoration: none;
            font-weight: 700;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            transition: all 0.2s;
        }
        .btn-website:hover {
            box-shadow: 0 8px 20px -4px rgba(20, 184, 166, 0.5);
            transform: translateY(-2px);
        }
        .footer-note {
            font-size: 0.85rem;
            color: var(--text-muted);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="badge">
            <div class="pulse-dot"></div>
            OpenAI App & MCP Backend Active
        </div>
        <h1>MyLogoQR AI Engine</h1>
        <p class="subtitle">
            This serverless endpoint connects <strong>MyLogoQR</strong> with <strong>ChatGPT, OpenAI Agents, and Claude</strong> using the Model Context Protocol (MCP).
        </p>

        <div class="links-grid">
            <div class="link-card">
                <div class="label">MCP Endpoint (For ChatGPT)</div>
                <div class="val">/mcp</div>
            </div>
            <a href="/docs" class="link-card">
                <div class="label">API Documentation</div>
                <div class="val">/docs &rarr;</div>
            </a>
            <a href="/health" class="link-card">
                <div class="label">Health Status</div>
                <div class="val">/health &rarr;</div>
            </a>
        </div>

        <div class="tester-box">
            <h3>⚡ Instant QR Code Generator Test</h3>
            <div class="input-row">
                <input type="text" id="qr-input" value="https://mylogoqr.com" placeholder="Enter URL or text...">
                <button class="btn-test" onclick="testQR()">Generate Test QR</button>
            </div>
            <div id="qr-result">
                <img id="qr-img" src="" alt="Generated QR">
                <p style="margin-top: 8px; font-size: 0.85rem; color: #94A3B8;">Generated instantly by Python Backend</p>
            </div>
        </div>

        <div class="cta-row">
            <div>
                <div style="font-weight: 700; color: #F8FAFC;">Looking for the official web app?</div>
                <div class="footer-note">Custom logos, high-res downloads, and custom frame styles.</div>
            </div>
            <a href="https://mylogoqr.com" target="_blank" class="btn-website">
                Visit MyLogoQR.com &rarr;
            </a>
        </div>
    </div>

    <script>
        async function testQR() {
            const val = document.getElementById('qr-input').value.trim();
            if(!val) return alert('Please enter some text or URL');
            const res = await fetch('/generate?text=' + encodeURIComponent(val));
            const data = await res.json();
            if(data && data.qr_base64) {
                document.getElementById('qr-img').src = data.qr_base64;
                document.getElementById('qr-result').style.display = 'block';
            }
        }
    </script>
</body>
</html>
"""

def generate_qr_base64(text: str, fill_color: str = "#12163A", back_color: str = "#FFFFFF") -> str:
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=3,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{img_str}"

@app.get("/")
@app.get("/api")
@app.get("/api/index.py")
def home(request: Request):
    accept = request.headers.get("accept", "")
    if "text/html" in accept:
        return HTMLResponse(content=HTML_DASHBOARD)
    return {
        "status": "online",
        "app": "MyLogoQR OpenAI App & MCP Server",
        "version": "1.0.0",
        "mcp_endpoint": "/mcp",
        "health_check": "/health",
        "docs": "/docs",
        "website": "https://mylogoqr.com"
    }

@app.get("/generate")
def direct_generate(text: str = "https://mylogoqr.com", color: str = "#12163A", bg: str = "#FFFFFF"):
    """Quick testing API to generate QR code directly."""
    b64 = generate_qr_base64(text, fill_color=color, back_color=bg)
    return {"status": "success", "text": text, "qr_base64": b64}

@app.get("/.well-known/openai-apps-challenge", response_class=PlainTextResponse)
def openai_challenge():
    """Domain verification token for OpenAI App Directory."""
    return OPENAI_CHALLENGE_TOKEN

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "app": "MyLogoQR OpenAI App (MCP Server)",
        "version": "1.0.0",
        "website": "https://mylogoqr.com"
    }

# -------------------------------------------------------------
# MCP JSON-RPC Protocol Endpoint
# -------------------------------------------------------------
class MCPRequest(BaseModel):
    jsonrpc: str = "2.0"
    id: Optional[Any] = None
    method: str
    params: Optional[Dict[str, Any]] = None

@app.post("/mcp")
def handle_mcp(req: MCPRequest):
    if req.method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req.id,
            "result": {
                "tools": [
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
                        "description": "Generates a Wi-Fi QR code for smartphones to scan and connect instantly without typing passwords.",
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
            }
        }

    if req.method == "tools/call":
        params = req.params or {}
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
            title = f"Wi-Fi Network ({ssid})"
        elif name == "create_whatsapp_qr":
            phone = "".join(filter(str.isdigit, str(args.get("phone", ""))))
            msg = args.get("message", "")
            payload = f"https://wa.me/{phone}" + (f"?text={msg}" if msg else "")
            title = f"WhatsApp Chat ({phone})"
        elif name == "create_vcard_qr":
            fn = args.get("firstName", "")
            ln = args.get("lastName", "")
            ph = args.get("phone", "")
            em = args.get("email", "")
            co = args.get("company", "")
            payload = f"BEGIN:VCARD\\nVERSION:3.0\\nN:{ln};{fn}\\nFN:{fn} {ln}\\nTEL:{ph}\\nEMAIL:{em}\\nORG:{co}\\nEND:VCARD"
            title = f"Contact: {fn} {ln}"
        else:
            raise HTTPException(status_code=404, detail=f"Tool {name} not found")

        data_url = generate_qr_base64(payload, fill_color=dark, back_color=light)

        return {
            "jsonrpc": "2.0",
            "id": req.id,
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": f"### ✅ QR Code Created: {title}\\n\\nScan with your phone camera:\\n\\n![QR Code]({data_url})\\n\\n---\\n*Created with [MyLogoQR](https://mylogoqr.com)*"
                    }
                ]
            }
        }

    return {"jsonrpc": "2.0", "id": req.id, "result": {"status": "ok"}}

@app.api_route("/{full_path:path}", methods=["GET", "POST"])
def catch_all(request: Request, full_path: str):
    accept = request.headers.get("accept", "")
    if "text/html" in accept and request.method == "GET":
        return HTMLResponse(content=HTML_DASHBOARD)
    return {
        "status": "online",
        "app": "MyLogoQR OpenAI App & MCP Server",
        "version": "1.0.0",
        "received_path": full_path,
        "mcp_endpoint": "/mcp",
        "health_check": "/health",
        "docs": "/docs",
        "website": "https://mylogoqr.com",
        "headers": dict(request.headers)
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)
