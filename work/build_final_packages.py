from pathlib import Path
import json, zipfile

root=Path(r"D:\Projects\mylogoqr")
# Rebuild static website package from final source.
exec(compile((root/"build_website_deploy.py").read_text(encoding="utf-8-sig"), "build_website_deploy.py", "exec"), {"__file__": str(root/"build_website_deploy.py")})

# Build source ZIP for the existing Vercel MCP deployment.
mcp_out=root/"mylogoqr_mcp_vercel_deploy.zip"
with zipfile.ZipFile(mcp_out,"w",zipfile.ZIP_DEFLATED) as z:
    for rel in ("vercel.json","requirements.txt","api/index.py"):
        z.write(root/rel,rel)
    z.write(root/"work/MCP-DEPLOY-README.txt","README-DEPLOY.txt")
with zipfile.ZipFile(mcp_out) as z:
    names=set(z.namelist())
    assert {"vercel.json","requirements.txt","api/index.py","README-DEPLOY.txt"} <= names
    config=json.loads(z.read("vercel.json"))
    assert config["rewrites"][0]["destination"]=="/api/index.py"
    source=z.read("api/index.py").decode("utf-8")
    assert "title = \"QR code\"" in source and "title = \"Wi-Fi QR code\"" in source
    assert "OPENAI_CHALLENGE_TOKEN = os.getenv(\"OPENAI_CHALLENGE_TOKEN\", \"\")" in source

# Build Agent Plugins ZIP: portable manifest + single remote MCP + skill and icons.
stage=root/"work/mylogoqr-plugin-fixed"
plugin_out=root/"mylogoqr-plugin-fixed-final.zip"
with zipfile.ZipFile(plugin_out,"w",zipfile.ZIP_DEFLATED) as z:
    for p in stage.rglob("*"):
        if p.is_file():
            z.write(p,p.relative_to(stage).as_posix())
with zipfile.ZipFile(root/"mylogoqr_website_deploy.zip") as z:
    names=set(z.namelist())
    assert {"index.html","chatgpt-privacy.html","sitemap.xml",".htaccess","styles.css","app.js"} <= names
    assert "vercel.json" not in names and not any(n.startswith(("api/","openai_app_pkg/","openai_plugin_bundle/")) for n in names)
    assert "https://mylogoqr.com/chatgpt-privacy" in z.read("sitemap.xml").decode("utf-8")

with zipfile.ZipFile(plugin_out) as z:
    names=set(z.namelist())
    assert {"plugin.json","mcp.json","skills/generate-qr/SKILL.md","assets/icon.png","assets/logo.png"} <= names
    assert ".mcp.json" not in names and not any(n.startswith(".codex-plugin/") for n in names)
    manifest=json.loads(z.read("plugin.json"))
    mcp=json.loads(z.read("mcp.json"))
    assert "mcpServers" not in manifest
    assert mcp["mcpServers"]["mylogoqr"]["type"]=="streamable-http"
    assert len(mcp["mcpServers"])==1
    ui=manifest["extensions"]["com.openai"]["interface"]
    assert ui["category"]=="Creativity"
    review=manifest["extensions"]["com.openai"]["review"]["test_cases"]
    assert len(review["positive"])==5 and len(review["negative"])==3
    assert ui["privacyPolicyURL"]=="https://mylogoqr.com/chatgpt-privacy"
print(f"MCP deploy ZIP: {mcp_out} ({mcp_out.stat().st_size} bytes)")
print(f"Plugin ZIP: {plugin_out} ({plugin_out.stat().st_size} bytes)")


