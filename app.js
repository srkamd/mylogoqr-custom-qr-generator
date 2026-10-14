// Register PWA Service Worker for offline capabilities
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/service-worker.js')
      .then((reg) => console.log('[Service Worker] Registered successfully:', reg.scope))
      .catch((err) => console.error('[Service Worker] Registration failed:', err));
  });
}

// Preset Logo Badges (Custom SVG vectors wrapped in white borders)
const PRESET_LOGOS = {
  whatsapp: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="64" height="64"><circle cx="12" cy="12" r="11" fill="white" stroke="#e2e8f0" stroke-width="0.75"/><circle cx="12" cy="12" r="9.5" fill="#25D366"/><path d="M12 6.5c-2.76 0-5 2.24-5 5 0 .96.27 1.85.74 2.62l-.78 2.87 2.94-.77c.74.4 1.57.62 2.45.62 2.76 0 5-2.24 5-5s-2.24-5-5-5zm2.84 6.94c-.12.34-.69.66-1 .69-.27.02-.63.13-1.8-.35-1.5-.62-2.45-2.14-2.52-2.24-.07-.1-.6-1-.6-1.92 0-.91.48-1.36.65-1.53.17-.17.38-.21.5-.21.13 0 .25 0 .36.01.12.01.27-.04.42.32.16.38.53 1.29.58 1.39.05.1.08.22.02.35-.06.13-.1.22-.2.34-.1.12-.2.27-.29.36-.1.1-.21.21-.09.42.12.21.52.85 1.11 1.38.76.68 1.4.89 1.6.99.2.1.32.08.44-.06.12-.14.53-.62.68-.83.15-.21.3-.17.5-.1.2.07 1.28.6 1.5.71.22.11.37.17.42.27.05.1.05.58-.07.92z" fill="white"/></svg>`,
  instagram: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="64" height="64"><defs><linearGradient id="ig-grad" x1="0%" y1="100%" x2="100%" y2="0%"><stop offset="0%" stop-color="#fdf497"/><stop offset="5%" stop-color="#fdf497"/><stop offset="30%" stop-color="#fd5949"/><stop offset="60%" stop-color="#d6249f"/><stop offset="100%" stop-color="#285AEB"/></linearGradient></defs><circle cx="12" cy="12" r="11" fill="white" stroke="#e2e8f0" stroke-width="0.75"/><rect x="6" y="6" width="12" height="12" rx="3.5" fill="url(#ig-grad)"/><rect x="7.5" y="7.5" width="9" height="9" rx="2.5" fill="none" stroke="white" stroke-width="1"/><circle cx="12" cy="12" r="1.8" fill="none" stroke="white" stroke-width="1"/><circle cx="14.8" cy="9.2" r="0.45" fill="white"/></svg>`,
  wifi: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="64" height="64"><circle cx="12" cy="12" r="11" fill="white" stroke="#e2e8f0" stroke-width="0.75"/><circle cx="12" cy="12" r="9.5" fill="#3b82f6"/><path d="M12 16.5a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm-3.535-3.536a5 5 0 0 1 7.07 0l-1.06 1.06a3.5 3.5 0 0 0-4.95 0l-1.06-1.06zm-2.122-2.12a8 8 0 0 1 11.314 0l-1.06 1.06a6.5 6.5 0 0 0-9.193 0l-1.06-1.06zm-2.12-2.122a11 11 0 0 1 15.556 0l-1.06 1.06a9.5 9.5 0 0 0-13.435 0l-1.06-1.06z" fill="white"/></svg>`,
  phone: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="64" height="64"><circle cx="12" cy="12" r="11" fill="white" stroke="#e2e8f0" stroke-width="0.75"/><circle cx="12" cy="12" r="9.5" fill="#10b981"/><path d="M15.5 13.7c-.4-.4-.8-.4-1.2 0l-.5.5c-.3.3-.6.4-.9.2a6.4 6.4 0 0 1-2.4-2.4c-.2-.3-.1-.6.2-.9l.5-.5c.4-.4.4-.8 0-1.2l-1.5-1.5c-.4-.4-.8-.4-1.2 0l-.6.6a2 2 0 0 0-.5 1.4c0 1.2.6 2.6 1.8 3.8s2.6 1.8 3.8 1.8c.6 0 1.1-.2 1.4-.5l.6-.6c.4-.4.4-.8 0-1.2l-1.5-1.5z" fill="white"/></svg>`,
  email: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="64" height="64"><circle cx="12" cy="12" r="11" fill="white" stroke="#e2e8f0" stroke-width="0.75"/><circle cx="12" cy="12" r="9.5" fill="#ef4444"/><path d="M6.5 8.5v7c0 .55.45 1 1 1h9c.55 0 1-.45 1-1v-7c0-.55-.45-1-1-1h-9c-.55 0-1 .45-1 1zm9.95.8L12 12.05 7.55 9.3a.5.5 0 0 1 .53-.85L12 10.74l3.92-2.29a.5.5 0 0 1 .53.85z" fill="white"/></svg>`,
  globe: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="64" height="64"><circle cx="12" cy="12" r="11" fill="white" stroke="#e2e8f0" stroke-width="0.75"/><circle cx="12" cy="12" r="9.5" fill="#6366f1"/><path d="M12 5.5a6.5 6.5 0 1 0 0 13 6.5 6.5 0 0 0 0-13zm-2.84 6.5c.08-1.12.39-2.18.88-3.08a5.27 5.27 0 0 0-1.84.88A5.5 5.5 0 0 0 9.16 12zm.98 0h3.72a7.83 7.83 0 0 1-.5 2.5h-2.72a7.83 7.83 0 0 1-.5-2.5zm0-1c.06-1 .23-1.85.5-2.5h2.72c-.27.65-.44 1.5-.5 2.5H10.14zM12 6.5a7.27 7.27 0 0 1 1 .58c.28.66.47 1.48.55 2.42h-3.1c.08-.94.27-1.76.55-2.42.23-.23.57-.43 1-.58zm2.84 5.5h.88c.06-.5.1-1 .1-1.5s-.04-1-.1-1.5h-.88c.08.5.12 1 .12 1.5s-.04 1-.12 1.5zm.3 2.5a5.27 5.27 0 0 0 1.84-.88 5.5 5.5 0 0 0-1.04-2.2 6.64 6.64 0 0 1-.8 3.08zm-1.8 0a7.27 7.27 0 0 1-1 .58 7.37 7.37 0 0 1-1-.58c-.28-.66-.47-1.48-.55-2.42h3.1c-.08.94-.27 1.76-.55 2.42z" fill="white"/></svg>`
};

// Global App State
const state = {
  dataType: 'url',
  dotsStyle: 'square',
  cornersSquareStyle: 'square',
  cornersDotStyle: 'square',
  
  fgType: 'solid',
  fgColor: '#4f46e5',
  gradientStart: '#6366f1',
  gradientEnd: '#06b6d4',
  gradientAngle: 0,
  
  bgColor: '#ffffff',
  bgTransparent: false,
  
  eyeSquareColor: '#4f46e5',
  eyeDotColor: '#4f46e5',
  
  logoUrl: null,
  logoScale: 0.2,
  logoMargin: 5,
  logoHideDots: true,
  
  frameStyle: 'none',
  frameText: 'SCAN ME',
  frameFont: 'Outfit',
  frameColor: '#4f46e5',
  frameTextColor: '#ffffff',
  
  exportSize: 1000
};

// Reference variables
let qrCode = null;
let debounceTimeout = null;

// Initialize components and listeners
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initAccordions();
  initPresetLogos();
  setupEventListeners();
  handlePSEO();
  generateQRCode();
  lucide.createIcons();
});

// Theme Management
function initTheme() {
  const themeToggle = document.getElementById('theme-toggle');
  const lightIcon = document.getElementById('theme-icon-light');
  const darkIcon = document.getElementById('theme-icon-dark');
  
  if (!themeToggle) {
    document.documentElement.classList.remove('dark');
    return;
  }
  
  // Set default theme from localStorage or system preference
  if (localStorage.getItem('theme') === 'light' || 
      (!localStorage.getItem('theme') && !window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.documentElement.classList.remove('dark');
    if (lightIcon) lightIcon.classList.remove('hidden');
    if (darkIcon) darkIcon.classList.add('hidden');
  } else {
    document.documentElement.classList.add('dark');
    if (lightIcon) lightIcon.classList.add('hidden');
    if (darkIcon) darkIcon.classList.remove('hidden');
  }

  themeToggle.addEventListener('click', () => {
    if (document.documentElement.classList.contains('dark')) {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
      lightIcon.classList.remove('hidden');
      darkIcon.classList.add('hidden');
    } else {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
      lightIcon.classList.add('hidden');
      darkIcon.classList.remove('hidden');
    }
    // Update preview composition background/borders in case canvas uses transparency
    debouncedGenerate();
  });
}

// Accordion Management
function initAccordions() {
  const triggers = document.querySelectorAll('.accordion-trigger');
  
  triggers.forEach(trigger => {
    trigger.addEventListener('click', () => {
      const targetId = trigger.getAttribute('data-target');
      const targetContent = document.getElementById(targetId);
      const chevron = trigger.querySelector('.accordion-chevron');
      
      const isOpen = targetContent.classList.contains('open');
      
      // Close all accordions (optional: single expand mode)
      // For this app, we will let them expand independently, but close others to keep it clean.
      triggers.forEach(t => {
        const id = t.getAttribute('data-target');
        const content = document.getElementById(id);
        const c = t.querySelector('.accordion-chevron');
        if (id !== targetId && content.classList.contains('open')) {
          content.classList.remove('open');
          c.classList.remove('rotate');
        }
      });

      if (isOpen) {
        targetContent.classList.remove('open');
        chevron.classList.remove('rotate');
      } else {
        targetContent.classList.add('open');
        chevron.classList.add('rotate');
      }
    });
  });

  // Open first accordion by default
  const firstAccordion = document.getElementById('acc-colors');
  if (firstAccordion) {
    firstAccordion.classList.add('open');
    document.querySelector('[data-target="acc-colors"] .accordion-chevron').classList.add('rotate');
  }
}

// Preset Logo Badges
function initPresetLogos() {
  const badges = document.querySelectorAll('.preset-badge');
  badges.forEach(badge => {
    badge.addEventListener('click', () => {
      const presetType = badge.getAttribute('data-preset');
      
      // Toggle active states
      badges.forEach(b => b.classList.remove('active'));
      
      if (presetType) {
        badge.classList.add('active');
        // Convert SVG content to clean Data URL
        const svgContent = PRESET_LOGOS[presetType];
        state.logoUrl = `data:image/svg+xml;utf8,${encodeURIComponent(svgContent)}`;
        
        // Show remove button
        document.getElementById('logo-remove-btn').classList.remove('hidden');
        document.getElementById('upload-label').textContent = `Preset: ${presetType.toUpperCase()}`;
      } else {
        state.logoUrl = null;
        document.getElementById('logo-remove-btn').classList.add('hidden');
        document.getElementById('upload-label').textContent = 'PNG, JPG, SVG up to 5MB';
      }
      
      generateQRCode();
    });
  });

  // Logo Remove Button
  document.getElementById('logo-remove-btn').addEventListener('click', () => {
    state.logoUrl = null;
    document.getElementById('logo-upload').value = '';
    document.getElementById('logo-remove-btn').classList.add('hidden');
    document.getElementById('upload-label').textContent = 'PNG, JPG, SVG up to 5MB';
    badges.forEach(b => b.classList.remove('active'));
    generateQRCode();
  });
}

// Input Handlers and Validation
function setupEventListeners() {
  
  // Tab Switcher
  const tabs = document.querySelectorAll('#data-tabs button');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      
      state.dataType = tab.getAttribute('data-tab');
      
      // Hide all panes
      const panes = document.querySelectorAll('.tab-pane');
      panes.forEach(pane => pane.classList.add('hidden'));
      
      // Show selected pane
      document.getElementById(`tab-${state.dataType}`).classList.remove('hidden');
      
      generateQRCode();
    });
  });

  // Wi-Fi Password Toggle
  const togglePassBtn = document.getElementById('wifi-toggle-pass');
  const wifiPassInput = document.getElementById('wifi-pass');
  togglePassBtn.addEventListener('click', () => {
    const isPass = wifiPassInput.type === 'password';
    wifiPassInput.type = isPass ? 'text' : 'password';
    togglePassBtn.innerHTML = isPass ? '<i data-lucide="eye-off" class="h-4 w-4"></i>' : '<i data-lucide="eye" class="h-4 w-4"></i>';
    lucide.createIcons();
  });

  // Debounced input change listeners for all text inputs
  const inputsToDebounce = [
    'url-input', 'wa-phone', 'wa-message', 'wifi-ssid', 'wifi-pass', 'wifi-enc', 
    'text-input', 'vc-first', 'vc-last', 'vc-phone', 'vc-email', 'vc-org', 'vc-title', 
    'vc-url', 'vc-adr', 'frame-text'
  ];
  
  inputsToDebounce.forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.addEventListener('input', debouncedGenerate);
      el.addEventListener('change', debouncedGenerate);
    }
  });

  // Color inputs synchronization
  syncColorInput('fg-color', 'fg-color-text');
  syncColorInput('gradient-color-1', 'gradient-text-1');
  syncColorInput('gradient-color-2', 'gradient-text-2');
  syncColorInput('bg-color', 'bg-color-text');
  syncColorInput('eye-square-color', 'eye-square-text');
  syncColorInput('eye-dot-color', 'eye-dot-text');
  syncColorInput('frame-color', 'frame-color-text');
  syncColorInput('frame-text-color', 'frame-text-color-text');

  // Solid vs Gradient toggle
  const fgTypeSelect = document.getElementById('fg-type');
  fgTypeSelect.addEventListener('change', () => {
    state.fgType = fgTypeSelect.value;
    const solidCont = document.getElementById('fg-solid-container');
    const gradCont = document.getElementById('fg-gradient-container');
    
    if (state.fgType === 'solid') {
      solidCont.classList.remove('hidden');
      gradCont.classList.add('hidden');
    } else {
      solidCont.classList.add('hidden');
      gradCont.classList.remove('hidden');
    }
    generateQRCode();
  });

  // Gradient Angle Slider
  const angleSlider = document.getElementById('gradient-angle');
  angleSlider.addEventListener('input', () => {
    state.gradientAngle = parseInt(angleSlider.value);
    document.getElementById('gradient-angle-val').textContent = `${state.gradientAngle}°`;
    generateQRCode();
  });

  // Transparent Background Toggle
  const bgTransCheckbox = document.getElementById('bg-transparent');
  bgTransCheckbox.addEventListener('change', () => {
    state.bgTransparent = bgTransCheckbox.checked;
    document.getElementById('bg-color').disabled = state.bgTransparent;
    document.getElementById('bg-color-text').disabled = state.bgTransparent;
    generateQRCode();
  });

  // Shapes Selects
  document.getElementById('dots-style').addEventListener('change', (e) => {
    state.dotsStyle = e.target.value;
    generateQRCode();
  });
  document.getElementById('corners-square-style').addEventListener('change', (e) => {
    state.cornersSquareStyle = e.target.value;
    generateQRCode();
  });
  document.getElementById('corners-dot-style').addEventListener('change', (e) => {
    state.cornersDotStyle = e.target.value;
    generateQRCode();
  });

  // Logo Custom Upload
  document.getElementById('logo-upload').addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
      // Security Check: Validate MIME type to ensure it is actually an image
      if (!file.type.startsWith('image/')) {
        alert("Security Alert: Only valid image files are allowed.");
        return;
      }
      
      if (file.size > 5 * 1024 * 1024) {
        alert("File is too large. Max size is 5MB.");
        return;
      }
      
      const reader = new FileReader();
      reader.onload = (event) => {
        state.logoUrl = event.target.result;
        document.getElementById('upload-label').textContent = file.name;
        document.getElementById('logo-remove-btn').classList.remove('hidden');
        
        // Deselect any presets
        document.querySelectorAll('.preset-badge').forEach(b => b.classList.remove('active'));
        
        generateQRCode();
      };
      
      reader.onerror = (err) => {
        console.error("FileReader Security Audit Error: ", err);
        alert("Could not load image securely. Please check the file formatting.");
      };
      
      reader.readAsDataURL(file);
    }
  });

  // Logo size & margin sliders
  const logoSizeSlider = document.getElementById('logo-size-slider');
  logoSizeSlider.addEventListener('input', () => {
    state.logoScale = parseFloat(logoSizeSlider.value) / 100;
    document.getElementById('logo-size-val').textContent = `${logoSizeSlider.value}%`;
    generateQRCode();
  });
  
  const logoMarginSlider = document.getElementById('logo-margin-slider');
  logoMarginSlider.addEventListener('input', () => {
    state.logoMargin = parseInt(logoMarginSlider.value);
    document.getElementById('logo-margin-val').textContent = `${logoMarginSlider.value}px`;
    generateQRCode();
  });

  document.getElementById('logo-hide-dots').addEventListener('change', (e) => {
    state.logoHideDots = e.target.checked;
    generateQRCode();
  });

  // Frame Customizations
  document.getElementById('frame-style').addEventListener('change', (e) => {
    state.frameStyle = e.target.value;
    const frameOptions = document.getElementById('frame-options-container');
    if (state.frameStyle === 'none') {
      frameOptions.classList.add('hidden');
    } else {
      frameOptions.classList.remove('hidden');
    }
    generateQRCode();
  });
  
  document.getElementById('frame-font').addEventListener('change', (e) => {
    state.frameFont = e.target.value;
    generateQRCode();
  });

  // Resolution slider
  const sizeSlider = document.getElementById('export-size-slider');
  sizeSlider.addEventListener('input', () => {
    state.exportSize = parseInt(sizeSlider.value);
    document.getElementById('export-size-val').textContent = `${state.exportSize} x ${state.exportSize} px`;
    debouncedGenerate(); // Debounce canvas compositions on resolution slider changes
  });

  // Export Trigger Buttons
  document.getElementById('btn-download-png').addEventListener('click', () => downloadAs('png'));
  document.getElementById('btn-download-svg').addEventListener('click', () => downloadAs('svg'));
  document.getElementById('btn-download-pdf').addEventListener('click', () => downloadAs('pdf'));
  document.getElementById('btn-copy-clipboard').addEventListener('click', copyToClipboard);
}

// Bidirectional binding for Color Pickers & Hex Texts
function syncColorInput(pickerId, textId) {
  const picker = document.getElementById(pickerId);
  const textInput = document.getElementById(textId);

  picker.addEventListener('input', () => {
    textInput.value = picker.value;
    updateColorState(pickerId, picker.value);
  });

  textInput.addEventListener('change', () => {
    let val = textInput.value.trim();
    if (!val.startsWith('#')) val = '#' + val;
    // Check if valid hex
    if (/^#[0-9A-F]{6}$/i.test(val)) {
      picker.value = val;
      updateColorState(pickerId, val);
    } else {
      textInput.value = picker.value; // revert
    }
  });
}

function updateColorState(pickerId, value) {
  switch (pickerId) {
    case 'fg-color': state.fgColor = value; break;
    case 'gradient-color-1': state.gradientStart = value; break;
    case 'gradient-color-2': state.gradientEnd = value; break;
    case 'bg-color': state.bgColor = value; break;
    case 'eye-square-color': state.eyeSquareColor = value; break;
    case 'eye-dot-color': state.eyeDotColor = value; break;
    case 'frame-color': state.frameColor = value; break;
    case 'frame-text-color': state.frameTextColor = value; break;
  }
  generateQRCode();
}

function debouncedGenerate() {
  clearTimeout(debounceTimeout);
  debounceTimeout = setTimeout(generateQRCode, 100);
}

// Compile Inputs into Core Format
function compileData() {
  switch (state.dataType) {
    case 'url':
      return document.getElementById('url-input').value.trim() || 'https://google.com';
    
    case 'whatsapp':
      const phone = document.getElementById('wa-phone').value.trim();
      const msg = document.getElementById('wa-message').value.trim();
      const cleanPhone = phone.replace(/\D/g, ''); // keep only numbers
      if (!cleanPhone) return 'https://wa.me/';
      return `https://wa.me/${cleanPhone}${msg ? '?text=' + encodeURIComponent(msg) : ''}`;
    
    case 'wifi':
      const ssid = document.getElementById('wifi-ssid').value.trim() || 'WiFi-SSID';
      const pass = document.getElementById('wifi-pass').value.trim();
      const enc = document.getElementById('wifi-enc').value;
      if (enc === 'nopass') {
        return `WIFI:S:${ssid};T:nopass;;`;
      }
      return `WIFI:S:${ssid};T:${enc};P:${pass};;`;
    
    case 'text':
      return document.getElementById('text-input').value || 'Hello, craft your QR code!';
    
    case 'vcard':
      const first = document.getElementById('vc-first').value.trim();
      const last = document.getElementById('vc-last').value.trim();
      const tel = document.getElementById('vc-phone').value.trim();
      const email = document.getElementById('vc-email').value.trim();
      const org = document.getElementById('vc-org').value.trim();
      const title = document.getElementById('vc-title').value.trim();
      const url = document.getElementById('vc-url').value.trim();
      const adr = document.getElementById('vc-adr').value.trim();
      
      return `BEGIN:VCARD
VERSION:3.0
N:${last};${first};;;
FN:${first} ${last}
ORG:${org}
TITLE:${title}
TEL;TYPE=CELL:${tel}
EMAIL:${email}
URL:${url}
ADR;TYPE=WORK:;;${adr};;;;
END:VCARD`;
  }
  return '';
}

// Generate the QR code using qr-code-styling and composite the frame
async function generateQRCode() {
  const content = compileData();
  
  // Base configuration options
  const qrOptions = {
    width: state.exportSize,
    height: state.exportSize,
    type: "canvas",
    data: content,
    image: state.logoUrl || undefined,
    margin: 10,
    qrOptions: {
      typeNumber: 0,
      mode: "Byte",
      errorCorrectionLevel: "Q" // Robust level allowing logo coverage
    },
    dotsOptions: {
      type: state.dotsStyle,
      color: state.fgType === 'solid' ? state.fgColor : undefined,
      gradient: state.fgType !== 'solid' ? {
        type: state.fgType,
        rotation: (state.gradientAngle * Math.PI) / 180,
        colorStops: [
          { offset: 0, color: state.gradientStart },
          { offset: 1, color: state.gradientEnd }
        ]
      } : undefined
    },
    backgroundOptions: {
      color: state.bgTransparent ? "rgba(0,0,0,0)" : state.bgColor,
    },
    imageOptions: {
      hideBackgroundDots: state.logoHideDots,
      imageSize: state.logoScale,
      margin: state.logoMargin,
      crossOrigin: "anonymous"
    },
    cornersSquareOptions: {
      type: state.cornersSquareStyle,
      color: state.eyeSquareColor || undefined
    },
    cornersDotOptions: {
      type: state.cornersDotStyle,
      color: state.eyeDotColor || undefined
    }
  };

  // Re-instantiate or Update the styling instance
  if (!qrCode) {
    qrCode = new QRCodeStyling(qrOptions);
  } else {
    qrCode.update(qrOptions);
  }

  // Render to offscreen DOM div to extract the generated canvas
  const renderDiv = document.getElementById('hidden-qr-render');
  renderDiv.innerHTML = '';
  qrCode.append(renderDiv);

  // Use the promise-based raw data retrieval to ensure async logo image loading has completed
  try {
    const blob = await qrCode.getRawData("png");
    const img = new Image();
    img.src = URL.createObjectURL(blob);
    img.onload = () => {
      drawComposition(img);
      URL.revokeObjectURL(img.src);
    };
    img.onerror = (e) => {
      console.error("Failed to load QR image blob: ", e);
      URL.revokeObjectURL(img.src);
    };
  } catch (err) {
    console.error("Error generating QR composition: ", err);
  }
}

// Composition function to draw frames around the generated QR Code Canvas
function drawComposition(qrImage) {
  const canvas = document.getElementById('qr-composition-canvas');
  const ctx = canvas.getContext('2d');
  
  const S = state.exportSize;
  let W = S;
  let H = S;
  
  // Calculate margins based on selected frame layouts
  let padX = 0;
  let padY = 0;
  
  switch (state.frameStyle) {
    case 'none':
      W = S;
      H = S;
      break;
    case 'classic':
      W = Math.round(S * 1.16);
      H = Math.round(S * 1.34);
      padX = Math.round(S * 0.08);
      padY = Math.round(S * 0.08);
      break;
    case 'header':
      W = Math.round(S * 1.16);
      H = Math.round(S * 1.34);
      padX = Math.round(S * 0.08);
      padY = Math.round(S * 0.18);
      break;
    case 'pill':
      W = Math.round(S * 1.16);
      H = Math.round(S * 1.25);
      padX = Math.round(S * 0.08);
      padY = Math.round(S * 0.06);
      break;
    case 'border':
      W = Math.round(S * 1.16);
      H = Math.round(S * 1.25);
      padX = Math.round(S * 0.08);
      padY = Math.round(S * 0.08);
      break;
  }

  // Set composition resolution
  canvas.width = W;
  canvas.height = H;

  // Clear Canvas and Draw Background Card
  ctx.clearRect(0, 0, W, H);
  
  if (!state.bgTransparent) {
    ctx.fillStyle = state.bgColor;
    if (state.frameStyle !== 'none') {
      // Draw rounded card shell
      drawRoundedRect(ctx, 0, 0, W, H, S * 0.04, true, false);
    } else {
      ctx.fillRect(0, 0, W, H);
    }
  }

  // Draw core QR Code
  ctx.drawImage(qrImage, padX, padY, S, S);

  // If No Frame layout is active, stop here
  if (state.frameStyle === 'none') return;

  // Draw Custom CTA Frames
  ctx.font = `bold ${Math.round(S * 0.075)}px "${state.frameFont}"`;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  
  const frameText = state.frameText || 'SCAN ME';

  switch (state.frameStyle) {
    case 'classic': {
      // Draw solid banner at bottom
      const rectY = padY + S + Math.round(S * 0.02);
      const rectH = Math.round(S * 0.16);
      ctx.fillStyle = state.frameColor;
      drawRoundedRect(ctx, padX, rectY, S, rectH, S * 0.02, true, false);
      
      // Draw CTA text inside banner
      ctx.fillStyle = state.frameTextColor;
      ctx.fillText(frameText, W / 2, rectY + rectH / 2 + Math.round(S * 0.005));
      break;
    }
    
    case 'header': {
      // Draw solid banner at top
      const rectY = Math.round(S * 0.08);
      const rectH = Math.round(S * 0.16);
      ctx.fillStyle = state.frameColor;
      drawRoundedRect(ctx, padX, rectY, S, rectH, S * 0.02, true, false);
      
      // Draw CTA text inside banner
      ctx.fillStyle = state.frameTextColor;
      ctx.fillText(frameText, W / 2, rectY + rectH / 2 + Math.round(S * 0.005));
      break;
    }
    
    case 'pill': {
      // Draw capsule rounded pill at the bottom
      const pillW = Math.round(S * 0.7);
      const pillH = Math.round(S * 0.12);
      const pillX = Math.round((W - pillW) / 2);
      const pillY = padY + S + Math.round(S * 0.03);
      
      ctx.fillStyle = state.frameColor;
      drawRoundedRect(ctx, pillX, pillY, pillW, pillH, pillH / 2, true, false);
      
      ctx.font = `bold ${Math.round(S * 0.05)}px "${state.frameFont}"`;
      ctx.fillStyle = state.frameTextColor;
      ctx.fillText(frameText, W / 2, pillY + pillH / 2 + Math.round(S * 0.003));
      break;
    }
    
    case 'border': {
      // Draw thick framing border line
      const bOffset = Math.round(S * 0.03);
      const bX = padX - bOffset;
      const bY = padY - bOffset;
      const bSize = S + bOffset * 2;
      const bWidth = Math.round(S * 0.015);
      
      ctx.strokeStyle = state.frameColor;
      ctx.lineWidth = bWidth;
      ctx.strokeRect(bX, bY, bSize, bSize);
      
      // Draw text badge cutting the bottom border line
      const lW = Math.round(S * 0.55);
      const lH = Math.round(S * 0.095);
      const lX = Math.round((W - lW) / 2);
      const lY = padY + S - Math.round(lH / 2) + bOffset;
      
      // Fill label box with background color to mask underlying border line
      ctx.fillStyle = state.bgTransparent ? '#ffffff' : state.bgColor;
      ctx.fillRect(lX, lY, lW, lH);
      ctx.strokeRect(lX, lY, lW, lH);
      
      // Draw CTA text centered inside label border box
      ctx.font = `bold ${Math.round(S * 0.045)}px "${state.frameFont}"`;
      ctx.fillStyle = state.frameTextColor;
      ctx.fillText(frameText, W / 2, lY + lH / 2 + Math.round(S * 0.003));
      break;
    }
  }
}

// Canvas Rounded Rectangle Helper
function drawRoundedRect(ctx, x, y, width, height, radius, fill = false, stroke = false) {
  ctx.beginPath();
  ctx.moveTo(x + radius, y);
  ctx.lineTo(x + width - radius, y);
  ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
  ctx.lineTo(x + width, y + height - radius);
  ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
  ctx.lineTo(x + radius, y + height);
  ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
  ctx.lineTo(x, y + radius);
  ctx.quadraticCurveTo(x, y, x + radius, y);
  ctx.closePath();
  if (fill) ctx.fill();
  if (stroke) ctx.stroke();
}

// Clipboard Copy Logic (Copies PNG representation)
async function copyToClipboard() {
  const canvas = document.getElementById('qr-composition-canvas');
  const btn = document.getElementById('btn-copy-clipboard');
  const copyText = document.getElementById('copy-text');
  const copyIcon = document.getElementById('copy-icon');

  try {
    const blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/png'));
    if (!blob) throw new Error("Could not construct Blob from canvas");
    
    await navigator.clipboard.write([
      new ClipboardItem({ 'image/png': blob })
    ]);
    
    // UI Feedback
    copyText.textContent = "Copied!";
    copyIcon.setAttribute('data-lucide', 'check');
    btn.classList.add('bg-emerald-500/10', 'border-emerald-500/30', 'text-emerald-500');
    lucide.createIcons();

    setTimeout(() => {
      copyText.textContent = "Copy Image to Clipboard";
      copyIcon.setAttribute('data-lucide', 'copy');
      btn.classList.remove('bg-emerald-500/10', 'border-emerald-500/30', 'text-emerald-500');
      lucide.createIcons();
    }, 2000);

  } catch (err) {
    console.error("Clipboard copy error:", err);
    alert("Unable to copy to clipboard automatically in this browser. Try right-clicking the image or downloading instead.");
  }
}

// Download Handler: PNG, SVG, PDF
async function downloadAs(format) {
  const canvas = document.getElementById('qr-composition-canvas');
  const filename = `qrcraft_${state.dataType}_qr`;

  switch (format) {
    case 'png': {
      const dataUrl = canvas.toDataURL('image/png');
      const link = document.createElement('a');
      link.download = `${filename}.png`;
      link.href = dataUrl;
      link.click();
      break;
    }
    
    case 'svg': {
      // If no outer frame is active, retrieve direct native vector SVG from the library
      if (state.frameStyle === 'none') {
        try {
          // Temporarily toggle type to SVG to get true vector details
          qrCode.update({ type: "svg" });
          const svgBlob = await qrCode.getRawData("svg");
          
          const link = document.createElement('a');
          link.download = `${filename}.svg`;
          link.href = URL.createObjectURL(svgBlob);
          link.click();
          
          // Revert back to canvas rendering mode for composition
          qrCode.update({ type: "canvas" });
          generateQRCode();
        } catch (e) {
          console.error("SVG download error:", e);
        }
      } else {
        // Construct composite vector SVG including frame shapes and text
        try {
          qrCode.update({ type: "svg" });
          const qrSvgBlob = await qrCode.getRawData("svg");
          const qrSvgText = await qrSvgBlob.text();
          
          // Parse inner elements from raw QR SVG
          const parser = new DOMParser();
          const qrDoc = parser.parseFromString(qrSvgText, "image/svg+xml");
          const qrSvgElement = qrDoc.documentElement;
          const qrSvgInner = qrSvgElement.innerHTML;
          
          // Construct composite SVG XML String
          const S = state.exportSize;
          let W = S;
          let H = S;
          let padX = 0;
          let padY = 0;
          
          switch (state.frameStyle) {
            case 'classic': W = Math.round(S * 1.16); H = Math.round(S * 1.34); padX = Math.round(S * 0.08); padY = Math.round(S * 0.08); break;
            case 'header': W = Math.round(S * 1.16); H = Math.round(S * 1.34); padX = Math.round(S * 0.08); padY = Math.round(S * 0.18); break;
            case 'pill': W = Math.round(S * 1.16); H = Math.round(S * 1.25); padX = Math.round(S * 0.08); padY = Math.round(S * 0.06); break;
            case 'border': W = Math.round(S * 1.16); H = Math.round(S * 1.25); padX = Math.round(S * 0.08); padY = Math.round(S * 0.08); break;
          }

          let svgXml = `<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">`;
          
          // Background Card Shape
          if (!state.bgTransparent) {
            svgXml += `<rect width="${W}" height="${H}" rx="${Math.round(S * 0.04)}" fill="${state.bgColor}"/>`;
          }
          
          // QR Inner Vector Content
          svgXml += `<g transform="translate(${padX}, ${padY})">${qrSvgInner}</g>`;
          
          const textVal = state.frameText || 'SCAN ME';
          
          // Frame Vector Overlays
          if (state.frameStyle === 'classic') {
            const rectY = padY + S + Math.round(S * 0.02);
            const rectH = Math.round(S * 0.16);
            svgXml += `<rect x="${padX}" y="${rectY}" width="${S}" height="${rectH}" rx="${Math.round(S * 0.02)}" fill="${state.frameColor}"/>`;
            svgXml += `<text x="${W / 2}" y="${rectY + rectH / 2}" fill="${state.frameTextColor}" font-family="${state.frameFont}, sans-serif" font-size="${Math.round(S * 0.075)}" font-weight="bold" text-anchor="middle" dominant-baseline="central">${textVal}</text>`;
          } else if (state.frameStyle === 'header') {
            const rectY = Math.round(S * 0.08);
            const rectH = Math.round(S * 0.16);
            svgXml += `<rect x="${padX}" y="${rectY}" width="${S}" height="${rectH}" rx="${Math.round(S * 0.02)}" fill="${state.frameColor}"/>`;
            svgXml += `<text x="${W / 2}" y="${rectY + rectH / 2}" fill="${state.frameTextColor}" font-family="${state.frameFont}, sans-serif" font-size="${Math.round(S * 0.075)}" font-weight="bold" text-anchor="middle" dominant-baseline="central">${textVal}</text>`;
          } else if (state.frameStyle === 'pill') {
            const pillW = Math.round(S * 0.7);
            const pillH = Math.round(S * 0.12);
            const pillX = Math.round((W - pillW) / 2);
            const pillY = padY + S + Math.round(S * 0.03);
            svgXml += `<rect x="${pillX}" y="${pillY}" width="${pillW}" height="${pillH}" rx="${Math.round(pillH / 2)}" fill="${state.frameColor}"/>`;
            svgXml += `<text x="${W / 2}" y="${pillY + pillH / 2}" fill="${state.frameTextColor}" font-family="${state.frameFont}, sans-serif" font-size="${Math.round(S * 0.05)}" font-weight="bold" text-anchor="middle" dominant-baseline="central">${textVal}</text>`;
          } else if (state.frameStyle === 'border') {
            const bOffset = Math.round(S * 0.03);
            const bX = padX - bOffset;
            const bY = padY - bOffset;
            const bSize = S + bOffset * 2;
            const bWidth = Math.round(S * 0.015);
            svgXml += `<rect x="${bX}" y="${bY}" width="${bSize}" height="${bSize}" fill="none" stroke="${state.frameColor}" stroke-width="${bWidth}"/>`;
            
            const lW = Math.round(S * 0.55);
            const lH = Math.round(S * 0.095);
            const lX = Math.round((W - lW) / 2);
            const lY = padY + S - Math.round(lH / 2) + bOffset;
            svgXml += `<rect x="${lX}" y="${lY}" width="${lW}" height="${lH}" fill="${state.bgTransparent ? '#ffffff' : state.bgColor}" stroke="${state.frameColor}" stroke-width="${bWidth}"/>`;
            svgXml += `<text x="${W / 2}" y="${lY + lH / 2}" fill="${state.frameTextColor}" font-family="${state.frameFont}, sans-serif" font-size="${Math.round(S * 0.045)}" font-weight="bold" text-anchor="middle" dominant-baseline="central">${textVal}</text>`;
          }
          
          svgXml += `</svg>`;
          
          const svgOutputBlob = new Blob([svgXml], { type: "image/svg+xml;charset=utf-8" });
          const link = document.createElement('a');
          link.download = `${filename}.svg`;
          link.href = URL.createObjectURL(svgOutputBlob);
          link.click();
          
          qrCode.update({ type: "canvas" });
          generateQRCode();
        } catch (e) {
          console.error("Composite SVG generation error:", e);
        }
      }
      break;
    }
    
    case 'pdf': {
      // Initialize jsPDF with the exact pixel bounds of the composition canvas
      const { jsPDF } = window.jspdf;
      
      const pdf = new jsPDF({
        orientation: canvas.width > canvas.height ? 'landscape' : 'portrait',
        unit: 'px',
        format: [canvas.width, canvas.height]
      });
      
      pdf.addImage(canvas.toDataURL('image/png'), 'PNG', 0, 0, canvas.width, canvas.height);
      pdf.save(`${filename}.pdf`);
      break;
    }
  }
}

// Switch tab inline without a full page reload for instant UI response (0ms transitions)
function switchTabInline(type) {
  state.dataType = type;
  
  // Update H1 & Subtitle
  const titleEl = document.getElementById('hero-title');
  const subtitleEl = document.getElementById('hero-subtitle');
  
  const contentMap = {
    url: {
      title: "Free URL Link QR Code Generator",
      subtitle: "Create beautiful, customized QR codes for any website URL with logo overlays and custom frames.",
      docTitle: "Free URL Link QR Code Generator | Custom Logo & Frames | MyLogoQR"
    },
    whatsapp: {
      title: "Free WhatsApp QR Code Generator",
      subtitle: "Create customized WhatsApp chat QR codes with pre-filled text and brand icon overlays instantly.",
      docTitle: "Free WhatsApp Chat QR Code Generator | Custom Logo | MyLogoQR"
    },
    wifi: {
      title: "Secure Wi-Fi QR Code Generator",
      subtitle: "Create scanner QR codes for instant home and office network access. Scan to join without typing passwords.",
      docTitle: "Secure Wi-Fi Scanner QR Code Generator | Custom Logo | MyLogoQR"
    },
    text: {
      title: "Plain Text QR Code Generator",
      subtitle: "Convert plain text notes, messages, and raw data strings into highly customized styled QR codes instantly.",
      docTitle: "Custom Plain Text QR Code Generator | Custom Colors | MyLogoQR"
    },
    vcard: {
      title: "Business Card vCard QR Generator",
      subtitle: "Generate smart contact details QR codes for business cards, resumes, and corporate networking.",
      docTitle: "Professional Contact vCard QR Code Generator | MyLogoQR"
    }
  };
  
  if (contentMap[type]) {
    if (titleEl) titleEl.textContent = contentMap[type].title;
    if (subtitleEl) subtitleEl.textContent = contentMap[type].subtitle;
    document.title = contentMap[type].docTitle;
  }
  
  // Set tab button active styling
  const tabs = document.querySelectorAll('#data-tabs button');
  tabs.forEach(tab => {
    tab.classList.remove('active', 'text-indigo-500');
    if (tab.getAttribute('data-tab') === type) {
      tab.classList.add('active', 'text-indigo-500');
    }
  });

  // Hide all panes
  const panes = document.querySelectorAll('.tab-pane');
  panes.forEach(pane => pane.classList.add('hidden'));
  
  // Show selected pane
  const activePane = document.getElementById(`tab-${type}`);
  if (activePane) {
    activePane.classList.remove('hidden');
  }

  // Load preset logo
  document.querySelectorAll('.preset-badge').forEach(b => b.classList.remove('active'));
  if (type === 'whatsapp') {
    const waPreset = document.querySelector('[data-preset="whatsapp"]');
    if (waPreset) {
      waPreset.classList.add('active');
      const svgContent = PRESET_LOGOS['whatsapp'];
      state.logoUrl = `data:image/svg+xml;utf8,${encodeURIComponent(svgContent)}`;
      document.getElementById('logo-remove-btn').classList.remove('hidden');
      document.getElementById('upload-label').textContent = 'Preset: WHATSAPP';
    }
  } else if (type === 'wifi') {
    const wifiPreset = document.querySelector('[data-preset="wifi"]');
    if (wifiPreset) {
      wifiPreset.classList.add('active');
      const svgContent = PRESET_LOGOS['wifi'];
      state.logoUrl = `data:image/svg+xml;utf8,${encodeURIComponent(svgContent)}`;
      document.getElementById('logo-remove-btn').classList.remove('hidden');
      document.getElementById('upload-label').textContent = 'Preset: WIFI';
    }
  } else if (type === 'vcard') {
    const globePreset = document.querySelector('[data-preset="globe"]');
    if (globePreset) {
      globePreset.classList.add('active');
      const svgContent = PRESET_LOGOS['globe'];
      state.logoUrl = `data:image/svg+xml;utf8,${encodeURIComponent(svgContent)}`;
      document.getElementById('logo-remove-btn').classList.remove('hidden');
      document.getElementById('upload-label').textContent = 'Preset: GLOBE';
    }
  } else {
    // Clear logo for others on dynamic switch
    state.logoUrl = '';
    document.getElementById('logo-remove-btn').classList.add('hidden');
    document.getElementById('upload-label').textContent = 'Drag & drop or click to upload';
  }

  generateQRCode();
}

// Programmatic SEO Router
// Intercepts nav clicks, logo link resets, and browser back/forward buttons (Popstate).
// Instead of page reloads, it changes DOM structures, meta tags, and browser paths instantly.
// ==================================================
function handlePSEO() {
  const path = window.location.pathname.toLowerCase();
  let type = 'url';
  
  if (path.includes('whatsapp-qr-code-generator')) {
    type = 'whatsapp';
  } else if (path.includes('wifi-qr-code-generator')) {
    type = 'wifi';
  } else if (path.includes('vcard-qr-code-generator')) {
    type = 'vcard';
  } else if (path.includes('text-qr-code-generator')) {
    type = 'text';
  } else {
    type = 'url'; // Default to URL generator on / or any other index root
  }

  // Switch to correct tab inline on initial load
  switchTabInline(type);

  // Intercept tab button clicks for SPA navigation (0ms delay)
  const tabs = document.querySelectorAll('#data-tabs button');
  tabs.forEach(tab => {
    const newTab = tab.cloneNode(true);
    tab.parentNode.replaceChild(newTab, tab);
    
    newTab.addEventListener('click', (e) => {
      e.preventDefault();
      const targetTab = newTab.getAttribute('data-tab');
      let targetUrl = '/';
      if (targetTab === 'whatsapp') targetUrl = 'whatsapp-qr-code-generator';
      else if (targetTab === 'wifi') targetUrl = 'wifi-qr-code-generator';
      else if (targetTab === 'text') targetUrl = 'text-qr-code-generator';
      else if (targetTab === 'vcard') targetUrl = 'vcard-qr-code-generator';
      
      // Update history state without reload
      if (window.location.pathname !== targetUrl && (targetUrl !== '/' || window.location.pathname !== '/' && window.location.pathname !== '/index.html')) {
        history.pushState({ tab: targetTab }, '', targetUrl);
        switchTabInline(targetTab);
      }
    });
  });

  // Intercept logo brand link clicks for SPA page resets
  document.querySelectorAll('.brand-logo-link').forEach(link => {
    link.addEventListener('click', (e) => {
      const hasGenerator = document.getElementById('data-tabs') !== null;
      if (hasGenerator) {
        e.preventDefault();
        if (window.location.pathname !== '/' && window.location.pathname !== '/index.html') {
          history.pushState({ tab: 'url' }, '', '/');
          switchTabInline('url');
        }
      }
    });
  });
}

// Listen to popstate event for back/forward buttons
window.addEventListener('popstate', () => {
  const path = window.location.pathname.toLowerCase();
  let type = 'url';
  if (path.includes('whatsapp-qr-code-generator')) {
    type = 'whatsapp';
  } else if (path.includes('wifi-qr-code-generator')) {
    type = 'wifi';
  } else if (path.includes('vcard-qr-code-generator')) {
    type = 'vcard';
  } else if (path.includes('text-qr-code-generator')) {
    type = 'text';
  }
  switchTabInline(type);
});
