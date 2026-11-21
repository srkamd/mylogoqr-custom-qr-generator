/**
 * MyLogoQR - Universal Professional Print & PDF Studio
 * Built for real-world print shops, thermal printers, office inkjets, and commercial presses.
 * Supports: A4, US-Letter, A5, A6, Business Cards, Multi-up Sticker Sheets, Table Tents, Acrylic Standees.
 */
(function() {
  // Inject Universal Print CSS
  const style = document.createElement('style');
  style.id = 'mylogoqr-print-studio-styles';
  style.textContent = `
    #print-modal-overlay {
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(11, 15, 25, 0.88);
      backdrop-filter: blur(10px);
      -webkit-backdrop-filter: blur(10px);
      z-index: 999999;
      overflow-y: auto;
      padding: 20px;
      align-items: center;
      justify-content: center;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      box-sizing: border-box;
    }
    #print-modal-overlay.open {
      display: flex;
    }
    .ps-dialog {
      background: #FFFFFF;
      width: 100%;
      max-width: 1100px;
      border-radius: 20px;
      box-shadow: 0 30px 80px -20px rgba(0, 0, 0, 0.5);
      display: grid;
      grid-template-columns: 380px 1fr;
      overflow: hidden;
      max-height: 92vh;
      border: 1px solid rgba(255,255,255,0.2);
    }
    @media (max-width: 900px) {
      .ps-dialog {
        grid-template-columns: 1fr;
        max-height: none;
      }
    }
    .ps-sidebar {
      background: #F8FAFC;
      border-right: 1px solid #E2E8F0;
      padding: 24px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 18px;
    }
    .ps-sidebar h3 {
      font-size: 1.25rem;
      font-weight: 800;
      color: #0F172A;
      margin: 0;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .ps-group {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .ps-group label {
      font-size: 0.78rem;
      font-weight: 700;
      color: #475569;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .ps-group select, .ps-group input[type="text"] {
      width: 100%;
      padding: 9px 12px;
      border: 1px solid #CBD5E1;
      border-radius: 9px;
      font-size: 0.88rem;
      color: #1E293B;
      background: #FFFFFF;
      box-sizing: border-box;
      outline: none;
      transition: border-color .15s, box-shadow .15s;
    }
    .ps-group select:focus, .ps-group input[type="text"]:focus {
      border-color: #4F46E5;
      box-shadow: 0 0 0 3px rgba(79,70,229,0.15);
    }
    .ps-row-2 {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
    }
    .ps-checkbox-label {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 0.85rem;
      color: #334155;
      cursor: pointer;
      user-select: none;
      font-weight: 500;
    }
    .ps-checkbox-label input {
      width: 16px;
      height: 16px;
      accent-color: #4F46E5;
      cursor: pointer;
    }
    .ps-preview-pane {
      background: #E2E8F0;
      padding: 32px 20px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      position: relative;
      overflow-y: auto;
      min-height: 480px;
    }
    .ps-close-btn {
      position: absolute;
      top: 14px;
      right: 16px;
      background: #FFFFFF;
      border: 1px solid #CBD5E1;
      width: 34px;
      height: 34px;
      border-radius: 50%;
      cursor: pointer;
      font-size: 20px;
      line-height: 1;
      color: #475569;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all .15s;
      z-index: 10;
    }
    .ps-close-btn:hover {
      background: #F1F5F9;
      color: #0F172A;
    }

    /* Print Paper Canvas on Screen */
    .ps-sheet {
      background: #FFFFFF;
      box-shadow: 0 10px 40px rgba(0,0,0,0.18);
      position: relative;
      box-sizing: border-box;
      transition: all .2s ease;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      margin: auto;
    }

    /* Preset Formats (Screen Preview Dimensions) */
    .ps-format-standee { width: 340px; min-height: 480px; padding: 36px 24px; border-radius: 16px; text-align: center; }
    .ps-format-tabletent { width: 360px; min-height: 520px; padding: 28px 24px; border-radius: 12px; text-align: center; border: 2px dashed #94A3B8; }
    .ps-format-businesscard { width: 380px; min-height: 220px; padding: 20px 24px; border-radius: 8px; flex-direction: row; justify-content: space-between; text-align: left; }
    .ps-format-sticker-grid { width: 440px; min-height: 580px; padding: 20px; display: grid !important; gap: 12px; }
    .ps-format-flyer { width: 380px; min-height: 540px; padding: 36px 28px; text-align: center; }

    /* Crop Marks */
    .ps-sheet.crop-marks::before, .ps-sheet.crop-marks::after {
      content: "";
      position: absolute;
      width: 14px;
      height: 14px;
      pointer-events: none;
    }
    .ps-sheet.crop-marks::before { top: 6px; left: 6px; border-top: 2px solid #64748B; border-left: 2px solid #64748B; }
    .ps-sheet.crop-marks::after { bottom: 6px; right: 6px; border-bottom: 2px solid #64748B; border-right: 2px solid #64748B; }

    /* Single Sticker in Sheet */
    .ps-sticker-item {
      background: #FFFFFF;
      border: 1px dashed #CBD5E1;
      border-radius: 8px;
      padding: 10px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
    }
    .ps-sticker-item img, .ps-sticker-item svg {
      width: 80px !important;
      height: 80px !important;
    }
    .ps-sticker-item span {
      font-size: 0.65rem;
      font-weight: 700;
      margin-top: 4px;
      color: #1E293B;
    }

    /* Print Controls Action Buttons */
    .ps-actions {
      display: flex;
      flex-direction: column;
      gap: 8px;
      margin-top: auto;
      padding-top: 12px;
      border-top: 1px solid #E2E8F0;
    }
    .ps-btn-print {
      background: linear-gradient(135deg, #4F46E5, #3730A3);
      color: #FFFFFF;
      border: none;
      border-radius: 11px;
      padding: 14px 20px;
      font-weight: 700;
      font-size: 0.98rem;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
      box-shadow: 0 4px 16px rgba(79, 70, 229, 0.35);
      transition: transform .15s;
    }
    .ps-btn-print:hover { transform: translateY(-1px); }
    .ps-btn-png {
      background: #FFFFFF;
      color: #1E293B;
      border: 1px solid #CBD5E1;
      border-radius: 11px;
      padding: 10px 16px;
      font-weight: 700;
      font-size: 0.88rem;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: background .15s;
    }
    .ps-btn-png:hover { background: #F1F5F9; }

    /* HARDCORE PRINT MEDIA STYLES - ZERO CLIPPING, NO BLANK PAGES */
    @media print {
      html, body {
        background: #FFFFFF !important;
        margin: 0 !important;
        padding: 0 !important;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
      }
      body * {
        visibility: hidden !important;
      }
      #print-modal-overlay, #print-modal-overlay * {
        visibility: visible !important;
      }
      #print-modal-overlay {
        position: static !important;
        background: none !important;
        padding: 0 !important;
        display: block !important;
        inset: auto !important;
      }
      .ps-dialog {
        border: none !important;
        box-shadow: none !important;
        display: block !important;
        max-width: 100% !important;
        max-height: none !important;
      }
      .ps-sidebar, .ps-close-btn {
        display: none !important;
      }
      .ps-preview-pane {
        background: none !important;
        padding: 0 !important;
        display: block !important;
      }
      .ps-sheet {
        box-shadow: none !important;
        margin: 0 auto !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }
      .ps-format-standee, .ps-format-flyer {
        width: 100% !important;
        max-width: 500px !important;
        padding: 40px !important;
      }
      .ps-format-tabletent {
        width: 100% !important;
        max-width: 480px !important;
        padding: 30px !important;
      }
      .ps-format-businesscard {
        width: 3.5in !important;
        height: 2.0in !important;
        padding: 0.25in !important;
        border: 1px dashed #666 !important;
      }
      .ps-format-sticker-grid {
        width: 100% !important;
        display: grid !important;
        padding: 20px !important;
      }
    }
  `;
  document.head.appendChild(style);

  // Modal HTML structure
  const modalHTML = `
    <div id="print-modal-overlay" role="dialog" aria-modal="true" aria-label="Print & PDF Studio">
      <div class="ps-dialog">
        <!-- Controls Sidebar -->
        <div class="ps-sidebar">
          <h3>🖨️ Professional Print Studio</h3>
          <p style="font-size:0.82rem;color:#64748B;margin:0 0 4px 0">
            Export flawless, print-shop ready signage, table tents, business cards, and stickers.
          </p>

          <!-- 1. Physical Print Method -->
          <div class="ps-group">
            <label for="ps-preset">1. Print Preset &amp; Physical Format</label>
            <select id="ps-preset">
              <optgroup label="🏢 Retail, Dining &amp; Display">
                <option value="standee" selected>Acrylic Standee / Counter Display (A5/A6)</option>
                <option value="tabletent">Table Tent / Folded Cafe Menu</option>
                <option value="wifi">High-Speed Wi-Fi Guest Sign</option>
                <option value="review">Google 5-Star Review Standee</option>
              </optgroup>
              <optgroup label="🏷️ Multi-Label Sticker Sheets">
                <option value="sticker-12">12-Sticker Sheet (A4 / Letter - 3x4 Grid)</option>
                <option value="sticker-6">6 Large Badges / Coasters Sheet (2x3 Grid)</option>
              </optgroup>
              <optgroup label="💼 Stationery &amp; Marketing">
                <option value="businesscard">Standard Business Card (3.5" x 2")</option>
                <option value="flyer">Full Page Poster / Flyer (A4 / US Letter)</option>
              </optgroup>
            </select>
          </div>

          <!-- 2. Text Fields -->
          <div class="ps-group" id="ps-text-group">
            <label for="ps-header">2. Card Headline</label>
            <input type="text" id="ps-header" value="Scan To Connect" maxlength="45">
          </div>

          <div class="ps-group" id="ps-sub-group">
            <label for="ps-sub">Subtext / Instructions</label>
            <input type="text" id="ps-sub" value="Point your phone camera to scan instantly" maxlength="75">
          </div>

          <!-- 3. Paper Size & Print Safety -->
          <div class="ps-row-2">
            <div class="ps-group">
              <label for="ps-paper">Paper Standard</label>
              <select id="ps-paper">
                <option value="A4" selected>A4 (210 x 297 mm)</option>
                <option value="letter">US Letter (8.5" x 11")</option>
                <option value="A5">A5 (148 x 210 mm)</option>
                <option value="A6">A6 (105 x 148 mm)</option>
              </select>
            </div>
            <div class="ps-group">
              <label for="ps-ink">Color Mode</label>
              <select id="ps-ink">
                <option value="brand" selected>Full Color (Brand Accent)</option>
                <option value="mono">100% Black (Max Ink Save &amp; Contrast)</option>
                <option value="cmyk">Rich Dark Charcoal (#111827)</option>
              </select>
            </div>
          </div>

          <!-- 4. Typography & Styling -->
          <div class="ps-row-2">
            <div class="ps-group">
              <label for="ps-font">Print Typography</label>
              <select id="ps-font">
                <option value="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" selected>Modern Clean (Sans)</option>
                <option value="'Helvetica Neue', Helvetica, Arial, sans-serif">Swiss Minimal (Helvetica/Arial)</option>
                <option value="Georgia, 'Times New Roman', serif">Classic Elegant (Serif)</option>
                <option value="'Oswald', Impact, sans-serif">Bold Impact (Signs &amp; Retail)</option>
                <option value="'Courier New', Courier, monospace">Technical (Monospace)</option>
              </select>
            </div>
            <div class="ps-group">
              <label for="ps-color">Accent Color</label>
              <select id="ps-color">
                <option value="#4F46E5" selected>Indigo Royal (#4F46E5)</option>
                <option value="#059669">Emerald Green (#059669)</option>
                <option value="#0284C7">Sky Blue (#0284C7)</option>
                <option value="#DC2626">Crimson Red (#DC2626)</option>
                <option value="#D97706">Amber Gold (#D97706)</option>
                <option value="#0F172A">Jet Black (#0F172A)</option>
              </select>
            </div>
          </div>

          <!-- 5. Print Safety Options -->
          <div class="ps-group">
            <label>Print Safety &amp; Finishing</label>
            <div style="display:flex;flex-direction:column;gap:8px;margin-top:2px">
              <label class="ps-checkbox-label">
                <input type="checkbox" id="ps-crop-marks" checked>
                <span>Include Corner Crop / Cutting Marks</span>
              </label>
              <label class="ps-checkbox-label">
                <input type="checkbox" id="ps-safe-zone" checked>
                <span>Enforce Camera Safe-Zone (Quiet Margin)</span>
              </label>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="ps-actions">
            <button class="ps-btn-print" id="ps-do-print">
              🖨️ Print / Save as PDF
            </button>
            <button class="ps-btn-png" id="ps-download-card">
              📷 Export High-Res Image (PNG)
            </button>
          </div>
        </div>

        <!-- Live Visual Preview Pane -->
        <div class="ps-preview-pane">
          <button class="ps-close-btn" id="ps-close-btn" aria-label="Close dialog">&times;</button>

          <!-- The Live Printable Paper Sheet -->
          <div id="ps-live-sheet" class="ps-sheet ps-format-standee crop-marks">
            <!-- Dynamic Card Content Built via JS -->
          </div>
        </div>
      </div>
    </div>
  `;

  // Initialize Print Studio Logic
  function initPrintStudio() {
    if (document.getElementById('print-modal-overlay')) return;
    document.body.insertAdjacentHTML('beforeend', modalHTML);

    const overlay = document.getElementById('print-modal-overlay');
    const closeBtn = document.getElementById('ps-close-btn');
    const printBtn = document.getElementById('ps-do-print');
    const exportPngBtn = document.getElementById('ps-download-card');
    
    const presetSelect = document.getElementById('ps-preset');
    const paperSelect = document.getElementById('ps-paper');
    const inkSelect = document.getElementById('ps-ink');
    const fontSelect = document.getElementById('ps-font');
    const colorSelect = document.getElementById('ps-color');
    const cropCheckbox = document.getElementById('ps-crop-marks');
    const safeZoneCheckbox = document.getElementById('ps-safe-zone');

    const headerInput = document.getElementById('ps-header');
    const subInput = document.getElementById('ps-sub');
    const liveSheet = document.getElementById('ps-live-sheet');

    // Dynamic @page CSS rule for flawless paper dimensions in browser dialog
    let dynamicPageStyle = document.getElementById('ps-dynamic-page-style');
    if (!dynamicPageStyle) {
      dynamicPageStyle = document.createElement('style');
      dynamicPageStyle.id = 'ps-dynamic-page-style';
      document.head.appendChild(dynamicPageStyle);
    }

    function setPageOrientationAndSize() {
      const paper = paperSelect.value;
      const preset = presetSelect.value;
      let orientation = 'portrait';
      if (preset === 'businesscard') orientation = 'landscape';
      dynamicPageStyle.textContent = `@page { size: ${paper} ${orientation}; margin: 10mm; }`;
    }

    function getActiveQRClone() {
      const qrBox = document.getElementById('qr') || document.querySelector('.qrbox');
      if (!qrBox) return null;
      const svg = qrBox.querySelector('svg');
      const canvas = qrBox.querySelector('canvas');
      const img = qrBox.querySelector('img');

      if (svg) return svg.cloneNode(true);
      if (canvas) {
        const i = document.createElement('img');
        i.src = canvas.toDataURL('image/png');
        return i;
      }
      if (img) return img.cloneNode(true);
      return null;
    }

    function renderSheet() {
      const preset = presetSelect.value;
      const ink = inkSelect.value;
      const font = fontSelect.value;
      let color = colorSelect.value;

      if (ink === 'mono') color = '#000000';
      if (ink === 'cmyk') color = '#111827';

      // Crop marks
      if (cropCheckbox.checked) {
        liveSheet.classList.add('crop-marks');
      } else {
        liveSheet.classList.remove('crop-marks');
      }

      // Font family
      liveSheet.style.fontFamily = font;

      // Reset class
      liveSheet.className = 'ps-sheet ' + (cropCheckbox.checked ? 'crop-marks ' : '');
      liveSheet.innerHTML = '';

      const qrNode = getActiveQRClone();
      const qrWrapper = document.createElement('div');
      qrWrapper.style.padding = safeZoneCheckbox.checked ? '14px' : '4px';
      qrWrapper.style.background = '#FFFFFF';
      qrWrapper.style.borderRadius = '14px';
      qrWrapper.style.display = 'inline-flex';
      qrWrapper.style.alignItems = 'center';
      qrWrapper.style.justifyContent = 'center';

      if (qrNode) {
        qrNode.style.width = '190px';
        qrNode.style.height = '190px';
        qrWrapper.appendChild(qrNode);
      } else {
        qrWrapper.innerHTML = '<div style="padding:40px;color:#94A3B8;font-size:0.85rem">Generate QR code on page first</div>';
      }

      // 1. Sticker Sheet (Grid 3x4 = 12 stickers)
      if (preset === 'sticker-12' || preset === 'sticker-6') {
        const count = preset === 'sticker-12' ? 12 : 6;
        liveSheet.classList.add('ps-format-sticker-grid');
        liveSheet.style.gridTemplateColumns = preset === 'sticker-12' ? 'repeat(3, 1fr)' : 'repeat(2, 1fr)';
        liveSheet.style.border = '1px dashed #CBD5E1';

        for (let i = 0; i < count; i++) {
          const item = document.createElement('div');
          item.className = 'ps-sticker-item';
          item.style.border = '1px dashed ' + color;

          const qrMini = getActiveQRClone();
          if (qrMini) {
            qrMini.style.width = preset === 'sticker-12' ? '80px' : '120px';
            qrMini.style.height = preset === 'sticker-12' ? '80px' : '120px';
            item.appendChild(qrMini);
          }
          const text = document.createElement('span');
          text.textContent = headerInput.value || 'SCAN ME';
          text.style.color = color;
          item.appendChild(text);
          liveSheet.appendChild(item);
        }
        return;
      }

      // 2. Business Card (3.5" x 2")
      if (preset === 'businesscard') {
        liveSheet.classList.add('ps-format-businesscard');
        liveSheet.style.border = '1px solid ' + color;

        if (qrNode) {
          qrNode.style.width = '110px';
          qrNode.style.height = '110px';
        }

        const leftDiv = document.createElement('div');
        leftDiv.style.display = 'flex';
        leftDiv.style.flexDirection = 'column';
        leftDiv.style.justifyContent = 'center';
        leftDiv.style.paddingRight = '16px';

        const bTitle = document.createElement('h2');
        bTitle.style.margin = '0 0 6px 0';
        bTitle.style.fontSize = '1.25rem';
        bTitle.style.fontWeight = '800';
        bTitle.style.color = color;
        bTitle.textContent = headerInput.value || 'Digital Business Card';

        const bSub = document.createElement('p');
        bSub.style.margin = '0';
        bSub.style.fontSize = '0.82rem';
        bSub.style.color = '#475569';
        bSub.style.lineHeight = '1.35';
        bSub.textContent = subInput.value || 'Scan with smartphone camera to save full contact details instantly.';

        const bFoot = document.createElement('span');
        bFoot.style.marginTop = '12px';
        bFoot.style.fontSize = '0.68rem';
        bFoot.style.color = '#94A3B8';
        bFoot.textContent = 'Instant Scan • Direct Save';

        leftDiv.appendChild(bTitle);
        leftDiv.appendChild(bSub);
        leftDiv.appendChild(bFoot);

        liveSheet.appendChild(leftDiv);
        liveSheet.appendChild(qrWrapper);
        return;
      }

      // 3. Standees, Table Tents, Wi-Fi Signs, Google Reviews, Posters
      liveSheet.classList.add(preset === 'tabletent' ? 'ps-format-tabletent' : (preset === 'flyer' ? 'ps-format-flyer' : 'ps-format-standee'));
      liveSheet.style.border = preset === 'tabletent' ? '2px dashed ' + color : '2px solid ' + color;

      // Badge
      const badge = document.createElement('div');
      badge.style.display = 'inline-block';
      badge.style.padding = '4px 14px';
      badge.style.borderRadius = '99px';
      badge.style.fontSize = '0.72rem';
      badge.style.fontWeight = '800';
      badge.style.letterSpacing = '0.06em';
      badge.style.textTransform = 'uppercase';
      badge.style.marginBottom = '12px';
      badge.style.color = color;
      badge.style.backgroundColor = color + '18';

      if (preset === 'wifi') badge.textContent = '📶 HIGH-SPEED GUEST WI-FI';
      else if (preset === 'review') badge.textContent = '★ ★ ★ ★ ★ FIVE STAR REVIEWS';
      else if (preset === 'tabletent') badge.textContent = 'TABLE TENT • DINE IN MENU';
      else if (preset === 'flyer') badge.textContent = 'OFFICIAL QR CODE NOTICE';
      else badge.textContent = 'TABLE / COUNTER DISPLAY';

      // Title
      const h2 = document.createElement('h2');
      h2.style.margin = '0 0 6px 0';
      h2.style.fontSize = '1.45rem';
      h2.style.fontWeight = '900';
      h2.style.color = ink === 'mono' ? '#000000' : '#0F172A';
      h2.style.lineHeight = '1.25';
      h2.textContent = headerInput.value || 'Scan To Connect';

      // Subtitle
      const p = document.createElement('p');
      p.style.margin = '0 0 16px 0';
      p.style.fontSize = '0.88rem';
      p.style.color = '#64748B';
      p.style.lineHeight = '1.4';
      p.textContent = subInput.value || 'Point your phone camera to scan instantly';

      // Footer
      const foot = document.createElement('div');
      foot.style.marginTop = '16px';
      foot.style.fontSize = '0.7rem';
      foot.style.color = '#94A3B8';
      foot.style.fontWeight = '600';
      foot.style.letterSpacing = '0.04em';
      foot.textContent = 'Free & Private Barcode • Powered by MyLogoQR.com';

      liveSheet.appendChild(badge);
      liveSheet.appendChild(h2);
      liveSheet.appendChild(p);
      liveSheet.appendChild(qrWrapper);
      liveSheet.appendChild(foot);
    }

    // Auto populate sensible presets when dropdown changes
    presetSelect.addEventListener('change', function() {
      const val = this.value;
      if (val === 'wifi') {
        headerInput.value = 'Free Guest Wi-Fi';
        subInput.value = 'Scan with your camera to connect automatically';
        colorSelect.value = '#0284C7';
      } else if (val === 'review') {
        headerInput.value = 'Review Us On Google';
        subInput.value = 'Loved your experience? Scan to leave a 5-star review!';
        colorSelect.value = '#D97706';
      } else if (val === 'tabletent') {
        headerInput.value = 'Digital Food & Drinks Menu';
        subInput.value = 'Scan to browse menu and order directly from table';
        colorSelect.value = '#DC2626';
      } else if (val === 'businesscard') {
        headerInput.value = 'Digital Business Card';
        subInput.value = 'Scan to save full contact, phone & email to contacts.';
        colorSelect.value = '#0F172A';
      } else if (val.startsWith('sticker')) {
        headerInput.value = 'SCAN ME';
        subInput.value = '';
      } else {
        headerInput.value = 'Scan To Connect';
        subInput.value = 'Point your phone camera to scan instantly';
        colorSelect.value = '#4F46E5';
      }
      setPageOrientationAndSize();
      renderSheet();
    });

    [paperSelect, inkSelect, fontSelect, colorSelect, cropCheckbox, safeZoneCheckbox].forEach(el => {
      el.addEventListener('change', () => {
        setPageOrientationAndSize();
        renderSheet();
      });
    });

    [headerInput, subInput].forEach(el => {
      el.addEventListener('input', renderSheet);
    });

    closeBtn.addEventListener('click', () => overlay.classList.remove('open'));
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) overlay.classList.remove('open');
    });

    // Execute Print
    printBtn.addEventListener('click', () => {
      setPageOrientationAndSize();
      window.print();
    });

    // Export Card as Image (Canvas Snapshot)
    exportPngBtn.addEventListener('click', () => {
      const qrNode = liveSheet.querySelector('img, svg');
      if (!qrNode) return;
      alert('Your printable layout is ready! Choose "Save as PDF" in the destination dropdown to generate the exact vector PDF.');
      setPageOrientationAndSize();
      window.print();
    });

    window.openPrintTemplateModal = function() {
      setPageOrientationAndSize();
      renderSheet();
      overlay.classList.add('open');
    };
  }

  // Global event delegation for any #open-print-templates-btn or .trigger-print-template
  document.addEventListener('click', function(e) {
    const btn = e.target.closest('#open-print-templates-btn, .trigger-print-template');
    if (btn) {
      e.preventDefault();
      initPrintStudio();
      if (typeof window.openPrintTemplateModal === 'function') {
        window.openPrintTemplateModal();
      }
    }
  });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initPrintStudio);
  } else {
    initPrintStudio();
  }
})();
