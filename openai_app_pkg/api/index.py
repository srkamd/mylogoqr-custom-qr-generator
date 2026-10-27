from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
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

@app.get("/")
def home():
    return {
        "status": "online",
        "app": "MyLogoQR OpenAI App & MCP Server",
        "version": "1.0.0",
        "mcp_endpoint": "/mcp",
        "health_check": "/health",
        "docs": "/docs"
    }

@app.get("/.well-known/openai-apps-challenge", response_class=PlainTextResponse)
def openai_challenge():
    """Domain verification token for OpenAI App Directory."""
    return OPENAI_CHALLENGE_TOKEN

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "app": "MyLogoQR OpenAI App (MCP Server)",
        "version": "1.0.0"
    }

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
                        "text": f"### ✅ QR Code Created: {title}\n\nScan with your phone camera:\n\n![QR Code]({data_url})\n\n---\n*Created with [MyLogoQR](https://mylogoqr.com)*"
                    }
                ]
            }
        }

    return {"jsonrpc": "2.0", "id": req.id, "result": {"status": "ok"}}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)
