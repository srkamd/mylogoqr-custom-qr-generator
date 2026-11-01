// MyLogoQR Professional Chrome Extension - Main Popup Controller

let currentMode = "url";
let primaryColor = "#0f172a";
let dotStyle = "rounded";
let centerLogoEnabled = true;
let customLogoData = null;
const defaultLogoUrl = chrome.runtime.getURL("icons/mylogoqr_center.png");

// Initialize QR Code Styling Engine
let qrCode = null;

function initQRCode(initialData) {
  qrCode = new QRCodeStyling({
    width: 280,
    height: 280,
    type: "svg",
    data: initialData || "https://mylogoqr.com",
    image: centerLogoEnabled ? defaultLogoUrl : "",
    dotsOptions: {
      color: primaryColor,
      type: dotStyle
    },
    cornersSquareOptions: {
      color: primaryColor,
      type: "extra-rounded"
    },
    cornersDotOptions: {
      color: primaryColor,
      type: "dot"
    },
    backgroundOptions: {
      color: "#ffffff"
    },
    imageOptions: {
      crossOrigin: "anonymous",
      margin: 6,
      imageSize: 0.28,
      hideBackgroundDots: true
    },
    qrOptions: {
      errorCorrectionLevel: "Q"
    }
  });

  const container = document.getElementById("qr-container");
  container.innerHTML = "";
  qrCode.append(container);
}

function updateQR() {
  if (!qrCode) return;
  const data = getFormattedData();
  const imageSource = centerLogoEnabled ? (customLogoData || defaultLogoUrl) : "";

  qrCode.update({
    data: data || "https://mylogoqr.com",
    image: imageSource,
    dotsOptions: {
      color: primaryColor,
      type: dotStyle
    },
    cornersSquareOptions: {
      color: primaryColor,
      type: dotStyle === "square" ? "square" : "extra-rounded"
    },
    cornersDotOptions: {
      color: primaryColor,
      type: dotStyle === "square" ? "square" : "dot"
    }
  });
}

function getFormattedData() {
  if (currentMode === "url") {
    const val = document.getElementById("url-input").value.trim();
    return val || "https://mylogoqr.com";
  } else if (currentMode === "text") {
    return document.getElementById("text-input").value.trim() || "MyLogoQR Free Studio";
  } else if (currentMode === "wifi") {
    const ssid = document.getElementById("wifi-ssid").value.trim();
    const enc = document.getElementById("wifi-enc").value;
    const pass = document.getElementById("wifi-pass").value;
    if (!ssid) return "WIFI:S:MyWiFi;T:WPA;P:password;;";
    return `WIFI:S:${ssid};T:${enc};P:${pass};;`;
  } else if (currentMode === "whatsapp") {
    let phone = document.getElementById("wa-phone").value.replace(/[^0-9]/g, "");
    const msg = encodeURIComponent(document.getElementById("wa-msg").value.trim());
    if (!phone) phone = "15551234567";
    return `https://wa.me/${phone}${msg ? "?text=" + msg : ""}`;
  } else if (currentMode === "vcard") {
    const fn = document.getElementById("vcard-fn").value.trim() || "John Doe";
    const tel = document.getElementById("vcard-tel").value.trim();
    const email = document.getElementById("vcard-email").value.trim();
    return `BEGIN:VCARD\nVERSION:3.0\nFN:${fn}\nTEL:${tel}\nEMAIL:${email}\nEND:VCARD`;
  }
  return "https://mylogoqr.com";
}

function showToast(text) {
  const toast = document.getElementById("toast-msg");
  toast.innerText = text;
  toast.style.display = "block";
  setTimeout(() => {
    toast.style.display = "none";
  }, 2500);
}

// Setup Event Handlers
document.addEventListener("DOMContentLoaded", () => {
  // Check if context menu data exists
  chrome.storage.local.get(["contextQrData"], (res) => {
    let initialUrl = "https://mylogoqr.com";

    if (res.contextQrData) {
      initialUrl = res.contextQrData;
      chrome.storage.local.remove(["contextQrData"]);
      document.getElementById("url-input").value = initialUrl;
      initQRCode(initialUrl);
    } else {
      // Query active browser tab
      if (chrome.tabs && chrome.tabs.query) {
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
          if (tabs && tabs[0] && tabs[0].url && !tabs[0].url.startsWith("chrome://")) {
            initialUrl = tabs[0].url;
          }
          document.getElementById("url-input").value = initialUrl;
          initQRCode(initialUrl);
        });
      } else {
        document.getElementById("url-input").value = initialUrl;
        initQRCode(initialUrl);
      }
    }
  });

  // Current tab button click
  document.getElementById("btn-current-tab").addEventListener("click", () => {
    if (chrome.tabs && chrome.tabs.query) {
      chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        if (tabs && tabs[0] && tabs[0].url) {
          document.getElementById("url-input").value = tabs[0].url;
          updateQR();
          showToast("Loaded current tab URL!");
        }
      });
    }
  });

  // Mode switching tabs
  const tabBtns = document.querySelectorAll(".tab-btn");
  tabBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      tabBtns.forEach((b) => b.classList.remove("active"));
      document.querySelectorAll(".panel").forEach((p) => p.classList.remove("active"));

      btn.classList.add("active");
      currentMode = btn.getAttribute("data-tab");
      document.getElementById(`panel-${currentMode}`).classList.add("active");
      updateQR();
    });
  });

  // Live input listening
  const allInputs = document.querySelectorAll(".main-input, .main-textarea, .main-select");
  allInputs.forEach((input) => {
    input.addEventListener("input", () => {
      updateQR();
    });
  });

  // Color Swatches
  const swatches = document.querySelectorAll(".swatch");
  swatches.forEach((sw) => {
    sw.addEventListener("click", () => {
      swatches.forEach((s) => s.classList.remove("active"));
      sw.classList.add("active");
      primaryColor = sw.getAttribute("data-color");
      document.getElementById("custom-color-picker").value = primaryColor;
      updateQR();
    });
  });

  // Custom color picker
  const customColor = document.getElementById("custom-color-picker");
  customColor.addEventListener("input", (e) => {
    primaryColor = e.target.value;
    swatches.forEach((s) => s.classList.remove("active"));
    updateQR();
  });

  // Dot Style selector
  document.getElementById("dot-style-select").addEventListener("change", (e) => {
    dotStyle = e.target.value;
    updateQR();
  });

  // Center logo checkbox toggle
  document.getElementById("center-logo-toggle").addEventListener("change", (e) => {
    centerLogoEnabled = e.target.checked;
    updateQR();
  });

  // Custom Logo Upload
  const logoUpload = document.getElementById("custom-logo-input");
  logoUpload.addEventListener("change", (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        customLogoData = event.target.result;
        centerLogoEnabled = true;
        document.getElementById("center-logo-toggle").checked = true;
        updateQR();
        showToast("Custom logo applied!");
      };
      reader.readAsDataURL(file);
    }
  });

  // Download PNG (High-Res 1024x1024)
  document.getElementById("btn-download-png").addEventListener("click", () => {
    if (!qrCode) return;
    qrCode.download({
      name: "mylogoqr_code",
      extension: "png"
    });
    showToast("PNG downloaded!");
  });

  // Download SVG (Vector)
  document.getElementById("btn-download-svg").addEventListener("click", () => {
    if (!qrCode) return;
    qrCode.download({
      name: "mylogoqr_vector",
      extension: "svg"
    });
    showToast("Vector SVG downloaded!");
  });

  // Copy to Clipboard
  document.getElementById("btn-copy-clip").addEventListener("click", async () => {
    if (!qrCode) return;
    try {
      const blob = await qrCode.getRawData("png");
      if (blob) {
        await navigator.clipboard.write([
          new ClipboardItem({ "image/png": blob })
        ]);
        showToast("QR copied to clipboard!");
      }
    } catch (err) {
      console.error("Clipboard copy failed:", err);
      showToast("PNG download ready instead!");
      qrCode.download({ name: "mylogoqr_code", extension: "png" });
    }
  });
});
