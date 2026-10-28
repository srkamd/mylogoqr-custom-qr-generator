MyLogoQR MCP server deployment
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
