@echo off
title MyLogoQR Local Live Preview Server
cd /d "%~dp0"
echo Starting MyLogoQR Local Preview Server on Port 8080...
start http://localhost:8080/
python dev_server.py
pause
