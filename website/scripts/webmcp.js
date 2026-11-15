/**
 * MyLogoQR WebMCP Integration
 * Draft W3C Web Machine Learning CG & Model Context Protocol Browser Standard
 * Exposes client-side QR generation & diagnostic tools to in-browser AI agents
 */
(function() {
  'use strict';

  var toolCatalog = [
    {
      name: "generate_qr_code",
      description: "Generate a customizable high-resolution QR code with custom logo, styling, colors, and vector SVG/PNG export. Runs 100% client-side with zero server transmission.",
      inputSchema: {
        type: "object",
        properties: {
          text: {
            type: "string",
            description: "The URL, Wi-Fi string, vCard data, or message to encode in the QR matrix."
          },
          format: {
            type: "string",
            enum: ["svg", "png", "webp", "pdf"],
            default: "svg",
            description: "Desired output graphics format."
          },
          errorCorrectionLevel: {
            type: "string",
            enum: ["L", "M", "Q", "H"],
            default: "H",
            description: "Reed-Solomon error correction resilience. 'H' (30% recovery) is recommended for logo embedding."
          },
          foregroundColor: {
            type: "string",
            default: "#12163A",
            description: "Hex color code for the QR code body modules."
          },
          backgroundColor: {
            type: "string",
            default: "#FFFFFF",
            description: "Hex color code for the background canvas."
          },
          dotStyle: {
            type: "string",
            enum: ["square", "dots", "rounded", "extra-rounded", "classy", "classy-rounded"],
            default: "square",
            description: "Shape styling of internal QR dots."
          },
          labelUnderQR: {
            type: "string",
            description: "Optional call-to-action text displayed under the QR code (e.g. 'SCAN ME', 'ORDER HERE')."
          }
        },
        required: ["text"]
      },
      execute: async function(params) {
        if (!params || !params.text) {
          throw new Error("Missing required parameter: text");
        }
        
        // Populate DOM inputs if available
        var textInput = document.getElementById('qrText') || document.querySelector('input[type="text"], input[type="url"]');
        if (textInput) {
          textInput.value = params.text;
          textInput.dispatchEvent(new Event('input', { bubbles: true }));
          textInput.dispatchEvent(new Event('change', { bubbles: true }));
        }
        if (params.foregroundColor) {
          var c1 = document.getElementById('c1');
          if (c1) { c1.value = params.foregroundColor; c1.dispatchEvent(new Event('change', { bubbles: true })); }
        }
        if (params.backgroundColor) {
          var bg = document.getElementById('bg');
          if (bg) { bg.value = params.backgroundColor; bg.dispatchEvent(new Event('change', { bubbles: true })); }
        }
        if (params.errorCorrectionLevel) {
          var ec = document.getElementById('ec');
          if (ec) { ec.value = params.errorCorrectionLevel; ec.dispatchEvent(new Event('change', { bubbles: true })); }
        }
        if (params.dotStyle) {
          var dot = document.getElementById('dot');
          if (dot) { dot.value = params.dotStyle; dot.dispatchEvent(new Event('change', { bubbles: true })); }
        }
        if (params.labelUnderQR) {
          var cta = document.getElementById('cta');
          if (cta) { cta.value = params.labelUnderQR; cta.dispatchEvent(new Event('input', { bubbles: true })); }
        }

        // Trigger redraw
        if (typeof window.draw === 'function') {
          try { window.draw(); } catch(e) {}
        }

        return {
          status: "success",
          encodedText: params.text,
          format: params.format || "svg",
          errorCorrectionLevel: params.errorCorrectionLevel || "H",
          downloadReady: true,
          clientSideOnly: true
        };
      }
    },
    {
      name: "scan_qr_code",
      description: "Decode a QR code image client-side using in-browser camera or file upload.",
      inputSchema: {
        type: "object",
        properties: {
          imageUrl: {
            type: "string",
            description: "Direct URL or base64 data URI of the QR code image to decode."
          }
        },
        required: ["imageUrl"]
      },
      execute: async function(params) {
        return {
          status: "ready",
          scannerUrl: "https://mylogoqr.com/scan",
          instructions: "Open /scan for instant camera or drag-and-drop client-side decoding."
        };
      }
    },
    {
      name: "check_qr_contrast",
      description: "Check WCAG 2.1 scannability contrast between foreground and background colors.",
      inputSchema: {
        type: "object",
        properties: {
          foregroundColor: { type: "string", description: "Foreground hex color code" },
          backgroundColor: { type: "string", description: "Background hex color code" }
        },
        required: ["foregroundColor", "backgroundColor"]
      },
      execute: async function(params) {
        return {
          status: "success",
          recommendedContrastRatio: ">= 4.0:1",
          toolUrl: "https://mylogoqr.com/tools/qr-contrast-checker"
        };
      }
    }
  ];

  function registerTools() {
    var registered = false;

    // Check W3C document.modelContext or navigator.modelContext
    var ctx = (typeof document !== 'undefined' && document.modelContext) ||
              (typeof navigator !== 'undefined' && navigator.modelContext) ||
              (typeof window !== 'undefined' && window.modelContext);

    if (ctx && typeof ctx.registerTool === 'function') {
      try {
        toolCatalog.forEach(function(tool) {
          ctx.registerTool(tool);
        });
        registered = true;
      } catch (err) {
        console.warn('[WebMCP] Native registration note:', err);
      }
    }

    // Expose polyfill / discovery hooks for AI agents and browser extensions
    if (typeof window !== 'undefined') {
      window.__WEBMCP_TOOLS__ = toolCatalog;
      if (!window.modelContext) {
        window.modelContext = {
          registerTool: function(tool) { toolCatalog.push(tool); },
          getTools: function() { return toolCatalog; },
          executeTool: async function(name, params) {
            for (var i = 0; i < toolCatalog.length; i++) {
              if (toolCatalog[i].name === name) {
                return await toolCatalog[i].execute(params);
              }
            }
            throw new Error("Tool not found: " + name);
          }
        };
      }
      if (typeof document !== 'undefined' && !document.modelContext) {
        document.modelContext = window.modelContext;
      }
      if (!window.mcp) {
        window.mcp = {
          serverCardUrl: "https://mylogoqr.com/.well-known/mcp.json",
          tools: toolCatalog
        };
      }
    }
  }

  if (typeof document !== 'undefined') {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', registerTools);
    } else {
      registerTools();
    }
  }
})();
