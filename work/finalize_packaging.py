from pathlib import Path
import json,re
root=Path(r"D:\Projects\mylogoqr")

# Remove hard-coded fallback verification tokens; production must use the portal token.
node_path=root/"openai_app_pkg/server.js"
node=node_path.read_text(encoding="utf-8-sig")
node=node.replace("process.env.OPENAI_CHALLENGE_TOKEN || 'mylogoqr-openai-verification-token'", "process.env.OPENAI_CHALLENGE_TOKEN || ''")
node_path.write_text(node,encoding="utf-8")

# Normalize current metadata links and align the Codex compatibility manifest with the listing.
plugin_path=root/"openai_plugin_bundle/plugin.json"
plugin=json.loads(plugin_path.read_text(encoding="utf-8-sig"))
ui=plugin["extensions"]["com.openai"]["interface"]
ui["supportURL"]="https://mylogoqr.com/contact"
ui["termsOfServiceURL"]="https://mylogoqr.com/terms"
plugin_path.write_text(json.dumps(plugin,indent=2)+"\n",encoding="utf-8")
codex_path=root/"openai_plugin_bundle/.codex-plugin/plugin.json"
codex=json.loads(codex_path.read_text(encoding="utf-8-sig"))
codex["description"]="Design branded QR codes for links, Wi-Fi, WhatsApp, and digital business cards."
codex["mcpServers"]="./.mcp.json"
codex_path.write_text(json.dumps(codex,indent=2)+"\n",encoding="utf-8")

# A complete MCP deployment package, separate from static website hosting.
deploy_note="""MyLogoQR MCP server deployment
================================

This archive is the Vercel project source for the remote MCP endpoint.
Extract it as the root of the existing Vercel project and redeploy that project.
The deployment includes the serverless handler at api/index.py and the route
rewrite in vercel.json.

Before connecting the server in the OpenAI Plugins dashboard, set the Vercel
environment variable OPENAI_CHALLENGE_TOKEN to the exact challenge token shown
for the MCP hostname in the dashboard, then redeploy. Do not place that token
in source files or the plugin ZIP.

The handler exposes create_qr_code, create_wifi_qr, create_vcard_qr, and
create_whatsapp_qr over POST /mcp. Inputs are processed to generate QR images;
QR payload values are not repeated in result text.
"""
(root/"work/MCP-DEPLOY-README.txt").write_text(deploy_note,encoding="utf-8")

# Update the review package with the current clean links.
stage=root/"work/mylogoqr-plugin-fixed"
manifest=json.loads((stage/"plugin.json").read_text(encoding="utf-8-sig"))
ui=manifest["extensions"]["com.openai"]["interface"]
ui["supportURL"]="https://mylogoqr.com/contact"
ui["privacyPolicyURL"]="https://mylogoqr.com/chatgpt-privacy"
ui["termsOfServiceURL"]="https://mylogoqr.com/terms"
(stage/"plugin.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
mcp=json.loads((stage/"mcp.json").read_text(encoding="utf-8-sig"))
mcp["mcpServers"]["mylogoqr"]["url"]="https://mylogoqr-custom-qr-generator.vercel.app/mcp"
(stage/"mcp.json").write_text(json.dumps(mcp,indent=2)+"\n",encoding="utf-8")
