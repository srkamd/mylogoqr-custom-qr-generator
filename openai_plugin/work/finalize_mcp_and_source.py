from pathlib import Path
import re
root = Path(r"D:\Projects\mylogoqr")

# Strip the encoded payload preview from the alternate Node server response.
node_path = root / "openai_app_pkg/server.js"
node = node_path.read_text(encoding="utf-8-sig")
node, count = re.subn(r"- \*\*Payload:\*\* .*?\\n", "", node)
if not count:
    raise SystemExit("Expected payload preview was not found in server.js")
node_path.write_text(node, encoding="utf-8")

# Keep the duplicate Vercel function in sync with the patched source.
(root / "openai_app_pkg/api/index.py").write_bytes((root / "api/index.py").read_bytes())

# Ensure the legacy manifest points at the reachable MCP service and truthful privacy page.
manifest_path = root / "openai_app_pkg/openai-app-manifest.json"
import json
manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
manifest["short_description"] = "Create branded QR codes for links, Wi-Fi, contacts, and WhatsApp."
manifest["long_description"] = "Create QR codes inside ChatGPT for links, Wi-Fi, WhatsApp, and digital business cards. Customize foreground and background colors. Inputs are sent to the MyLogoQR service for QR generation."
manifest["privacy_policy_url"] = "https://mylogoqr.com/chatgpt-privacy"
manifest["transport"] = {"type": "streamable-http", "endpoint": "https://mylogoqr-custom-qr-generator.vercel.app/mcp"}
manifest["categories"] = ["Design & Creative"]
manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

# Ensure the policy route is cached for offline visits.
sw_path = root / "service-worker.js"
sw = sw_path.read_text(encoding="utf-8-sig")
if "mylogoqr-cache-v6" not in sw:
    raise SystemExit("Expected cache version update not present")
if "'/chatgpt-privacy.html'" not in sw:
    raise SystemExit("Expected ChatGPT privacy route is not cached")
