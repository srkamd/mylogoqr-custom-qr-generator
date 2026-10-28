# MyLogoQR ChatGPT Plugin Launch Checklist

This project has two separate deployments: the public static website and the remote MCP service. Do not upload the MCP source bundle to the same static website host.

## 1. Publish the website

Upload and extract `mylogoqr_website_deploy.zip` to the root of the existing MyLogoQR website. It includes `chatgpt-privacy.html`, the sitemap entry, and the Apache clean-URL rules. Confirm that `https://mylogoqr.com/chatgpt-privacy` opens after deployment.

## 2. Update the MCP service on Vercel

Use `mylogoqr_mcp_vercel_deploy.zip` to update the source of the existing Vercel project serving `https://mylogoqr-custom-qr-generator.vercel.app/mcp`. The package contains the serverless MCP handler and its Vercel routing configuration. Set `OPENAI_CHALLENGE_TOKEN` in Vercel to the exact value shown by the OpenAI Plugins dashboard, then redeploy. Never put that token into a ZIP or source file.

The revised server no longer repeats QR payload text in result headings, validates inputs and colors, escapes Wi-Fi and vCard fields, and URL-encodes WhatsApp messages.

## 3. Upload the plugin package

Upload `mylogoqr-plugin-fixed-final.zip` to the MyLogoQR draft using **Upload new version**. Its root `mcp.json` uses the supported `streamable-http` transport and the live MCP hostname. It declares the `Creativity` category and includes five positive and three negative review cases.

After upload, open **MCPs**, connect the server, complete the domain challenge, scan the tools again, and resolve any findings. The owner must provide a reviewer-accessible video walkthrough URL in review details; no video URL is included in the package.

## 4. Before review/publication

- Verify the privacy notice and MCP endpoint are publicly reachable over HTTPS.
- Confirm the Vercel challenge variable matches the dashboard token.
- Test all four QR tools using sample data; do not use real Wi-Fi credentials or personal contact details in reviewer demos.
- Supply the required video walkthrough and submit for review only after the portal findings are clear.
- Approval and publication are separate; this project does not claim the plugin is live.
