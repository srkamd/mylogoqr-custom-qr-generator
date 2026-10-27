import express from 'express';
import cors from 'cors';
import QRCode from 'qrcode';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;
const OPENAI_CHALLENGE_TOKEN = process.env.OPENAI_CHALLENGE_TOKEN || 'mylogoqr-openai-verification-token';
const BASE_URL = process.env.BASE_URL || `http://localhost:${PORT}`;

app.use(cors({ origin: '*' }));
app.use(express.json());

// -------------------------------------------------------------
// 1. OpenAI Domain Verification Challenge Endpoint
// -------------------------------------------------------------
app.get('/.well-known/openai-apps-challenge', (req, res) => {
  res.type('text/plain').send(OPENAI_CHALLENGE_TOKEN);
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    app: 'MyLogoQR OpenAI App & MCP Server',
    version: '1.0.0',
    uptime: process.uptime(),
    timestamp: new Date().toISOString()
  });
});

// -------------------------------------------------------------
// 2. Core QR Code Generation Engine
// -------------------------------------------------------------
async function generateQrData({ text, darkColor = '#12163A', lightColor = '#FFFFFF', errorCorrectionLevel = 'H', width = 600 }) {
  // Generate SVG string
  const svg = await QRCode.toString(text, {
    type: 'svg',
    errorCorrectionLevel,
    margin: 3,
    color: {
      dark: darkColor,
      light: lightColor
    }
  });

  // Generate Base64 PNG Data URL
  const dataUrl = await QRCode.toDataURL(text, {
    errorCorrectionLevel,
    margin: 3,
    width,
    color: {
      dark: darkColor,
      light: lightColor
    }
  });

  return { svg, dataUrl };
}

// -------------------------------------------------------------
// 3. MCP (Model Context Protocol) Server Endpoints
// -------------------------------------------------------------

const TOOLS_MANIFEST = [
  {
    name: 'create_qr_code',
    description: 'Generates a custom styled QR code for any website URL or plain text with customizable brand colors and high error-correction.',
    inputSchema: {
      type: 'object',
      properties: {
        text: {
          type: 'string',
          description: 'The destination URL or text to encode (e.g. https://mybusiness.com)'
        },
        darkColor: {
          type: 'string',
          description: 'Hex color code for the QR code foreground/dots (default: #12163A, or any brand color like #008170)'
        },
        lightColor: {
          type: 'string',
          description: 'Hex color code for the background (default: #FFFFFF)'
        },
        label: {
          type: 'string',
          description: 'Optional human-readable label or title for the QR code'
        }
      },
      required: ['text']
    }
  },
  {
    name: 'create_wifi_qr',
    description: 'Generates a Wi-Fi connection QR code that smartphones can instantly scan to connect without typing passwords.',
    inputSchema: {
      type: 'object',
      properties: {
        ssid: {
          type: 'string',
          description: 'Wi-Fi Network Name (SSID)'
        },
        password: {
          type: 'string',
          description: 'Wi-Fi Password'
        },
        encryption: {
          type: 'string',
          enum: ['WPA', 'WEP', 'nopass'],
          description: 'Security encryption type (default: WPA)'
        },
        hidden: {
          type: 'boolean',
          description: 'Whether the network is hidden (default: false)'
        },
        darkColor: {
          type: 'string',
          description: 'Hex color code (default: #008170)'
        }
      },
      required: ['ssid']
    }
  },
  {
    name: 'create_vcard_qr',
    description: 'Generates a digital business card (vCard) QR code that adds contact details to the user phone address book in one scan.',
    inputSchema: {
      type: 'object',
      properties: {
        firstName: { type: 'string' },
        lastName: { type: 'string' },
        organization: { type: 'string' },
        title: { type: 'string' },
        phone: { type: 'string' },
        email: { type: 'string' },
        url: { type: 'string' },
        darkColor: { type: 'string' }
      },
      required: ['firstName', 'phone']
    }
  },
  {
    name: 'create_whatsapp_qr',
    description: 'Generates a click-to-chat WhatsApp QR code with optional pre-filled message.',
    inputSchema: {
      type: 'object',
      properties: {
        phone: {
          type: 'string',
          description: 'Phone number with international country code without plus sign (e.g. 923001234567)'
        },
        message: {
          type: 'string',
          description: 'Optional pre-filled message (e.g. Hi, I want to book an appointment)'
        },
        darkColor: {
          type: 'string',
          description: 'Hex color code (default: #25D366)'
        }
      },
      required: ['phone']
    }
  }
];

// MCP Tools List Handler
app.post('/mcp', async (req, res) => {
  const { jsonrpc, id, method, params } = req.body || {};

  if (method === 'tools/list') {
    return res.json({
      jsonrpc: '2.0',
      id,
      result: {
        tools: TOOLS_MANIFEST
      }
    });
  }

  if (method === 'tools/call') {
    const { name, arguments: args } = params || {};

    try {
      let qrText = '';
      let darkColor = args.darkColor || '#12163A';
      let lightColor = args.lightColor || '#FFFFFF';
      let description = '';

      if (name === 'create_qr_code') {
        qrText = args.text;
        description = `QR Code for: ${args.label || args.text}`;
      } else if (name === 'create_wifi_qr') {
        const enc = args.encryption || 'WPA';
        const pass = args.password || '';
        const hid = args.hidden ? 'H:true;' : '';
        qrText = `WIFI:S:${args.ssid};T:${enc};P:${pass};${hid};`;
        darkColor = args.darkColor || '#008170';
        description = `Wi-Fi QR Code for network "${args.ssid}"`;
      } else if (name === 'create_vcard_qr') {
        qrText = [
          'BEGIN:VCARD',
          'VERSION:3.0',
          `N:${args.lastName || ''};${args.firstName || ''};;;`,
          `FN:${args.firstName || ''} ${args.lastName || ''}`.trim(),
          args.organization ? `ORG:${args.organization}` : '',
          args.title ? `TITLE:${args.title}` : '',
          args.phone ? `TEL;TYPE=CELL:${args.phone}` : '',
          args.email ? `EMAIL:${args.email}` : '',
          args.url ? `URL:${args.url}` : '',
          'END:VCARD'
        ].filter(Boolean).join('\n');
        description = `Digital vCard QR Code for ${args.firstName} ${args.lastName || ''}`;
      } else if (name === 'create_whatsapp_qr') {
        const cleanPhone = args.phone.replace(/[^0-9]/g, '');
        const encodedMsg = args.message ? `?text=${encodeURIComponent(args.message)}` : '';
        qrText = `https://wa.me/${cleanPhone}${encodedMsg}`;
        darkColor = args.darkColor || '#25D366';
        description = `WhatsApp Click-to-Chat QR Code for ${args.phone}`;
      } else {
        return res.status(404).json({
          jsonrpc: '2.0',
          id,
          error: { code: -32601, message: `Tool "${name}" not found.` }
        });
      }

      const { svg, dataUrl } = await generateQrData({
        text: qrText,
        darkColor,
        lightColor,
        width: 800
      });

      // Deliver both structured data and interactive markdown preview
      return res.json({
        jsonrpc: '2.0',
        id,
        result: {
          content: [
            {
              type: 'text',
              text: `### ✅ ${description}\n\nScan with any smartphone camera:\n\n![Generated QR Code](${dataUrl})\n\n---\n**Details:**\n- **Payload:** \`${qrText.length > 80 ? qrText.substring(0, 80) + '...' : qrText}\`\n- **Color Scheme:** Foreground: \`${darkColor}\` | Background: \`${lightColor}\`\n\n*Created with [MyLogoQR](https://mylogoqr.com) - Custom Branded QR Studio.*`
            },
            {
              type: 'resource',
              resource: {
                uri: `data:image/svg+xml;utf8,${encodeURIComponent(svg)}`,
                mimeType: 'image/svg+xml',
                name: 'qrcode.svg'
              }
            }
          ]
        }
      });
    } catch (err) {
      return res.status(500).json({
        jsonrpc: '2.0',
        id,
        error: { code: -32000, message: err.message || 'Failed to generate QR code.' }
      });
    }
  }

  // Fallback for unrecognized JSON-RPC methods
  return res.json({
    jsonrpc: '2.0',
    id,
    result: { status: 'ok', info: 'MyLogoQR MCP Server is running' }
  });
});

// Direct REST endpoint for web or external API testing
app.post('/api/generate-qr', async (req, res) => {
  try {
    const { text, darkColor, lightColor, errorCorrectionLevel, width } = req.body;
    if (!text) return res.status(400).json({ error: 'Text/URL is required' });

    const result = await generateQrData({ text, darkColor, lightColor, errorCorrectionLevel, width });
    res.json({ success: true, ...result });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.listen(PORT, () => {
  console.log(`=======================================================`);
  console.log(`  MyLogoQR OpenAI App & MCP Server listening on port ${PORT}`);
  console.log(`  Health Check:   ${BASE_URL}/health`);
  console.log(`  MCP Endpoint:   ${BASE_URL}/mcp`);
  console.log(`  Challenge URL:  ${BASE_URL}/.well-known/openai-apps-challenge`);
  console.log(`=======================================================`);
});
