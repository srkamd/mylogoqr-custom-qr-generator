/**
 * MyLogoQR - Printable PDF & Display Standee Templates
 * Generates ready-to-print A4 / US-Letter Table Tents, Acrylic Standees, Wi-Fi Signs, and Google Review Cards.
 */
(function() {
  // Styles for modal and print media
  const style = document.createElement('style');
  style.textContent = `
    #print-modal-overlay {
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(11, 15, 25, 0.85);
      backdrop-filter: blur(8px);
      z-index: 100000;
      overflow-y: auto;
      padding: 24px 16px;
      align-items: center;
      justify-content: center;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    #print-modal-overlay.open {
      display: flex;
    }
    .print-modal-dialog {
      background: #FFFFFF;
      width: 100%;
      max-width: 860px;
      border-radius: 20px;
      box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.4);
      display: grid;
      grid-template-columns: 340px 1fr;
      overflow: hidden;
      max-height: 90vh;
    }
    @media (max-width: 768px) {
      .print-modal-dialog {
        grid-template-columns: 1fr;
        max-height: none;
      }
    }
    .print-controls {
      background: #F8FAFC;
      border-right: 1px solid #E2E8F0;
      padding: 24px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    .print-controls h3 {
      font-size: 1.15rem;
      font-weight: 800;
      color: #0F172A;
      margin: 0;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .print-controls label {
      font-size: 0.82rem;
      font-weight: 700;
      color: #475569;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      display: block;
      margin-bottom: 6px;
    }
    .print-controls input, .print-controls select {
      width: 100%;
      padding: 10px 12px;
      border: 1px solid #CBD5E1;
      border-radius: 10px;
      font-size: 0.9rem;
      color: #1E293B;
      background: #FFFFFF;
      box-sizing: border-box;
      outline: none;
      transition: border-color .15s;
    }
    .print-controls input:focus, .print-controls select:focus {
      border-color: #4F46E5;
    }
    .print-preview-pane {
      background: #F1F5F9;
      padding: 28px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      position: relative;
      overflow-y: auto;
    }
    .close-print-modal {
      position: absolute;
      top: 14px;
      right: 16px;
      background: rgba(0,0,0,0.06);
      border: none;
      width: 32px;
      height: 32px;
      border-radius: 50%;
      cursor: pointer;
      font-size: 18px;
      color: #475569;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: background .15s;
    }
    .close-print-modal:hover {
      background: rgba(0,0,0,0.12);
    }
    /* The Live Printable Card */
    #printable-template-target {
      background: #FFFFFF;
      width: 340px;
      min-height: 440px;
      border-radius: 18px;
      padding: 32px 24px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.08);
      border: 1px solid #E2E8F0;
      text-align: center;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: space-between;
      box-sizing: border-box;
      position: relative;
    }
    .template-card-header {
      width: 100%;
    }
    .template-badge {
      display: inline-block;
      padding: 4px 12px;
      border-radius: 99px;
      font-size: 0.72rem;
      font-weight: 800;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      margin-bottom: 8px;
    }
    .template-title {
      font-size: 1.35rem;
      font-weight: 900;
      color: #0F172A;
      margin: 0 0 6px 0;
      line-height: 1.25;
    }
    .template-subtitle {
      font-size: 0.86rem;
      color: #64748B;
      margin: 0;
      line-height: 1.4;
    }
    .template-qr-frame {
      padding: 16px;
      background: #FFFFFF;
      border: 2px solid #E2E8F0;
      border-radius: 16px;
      box-shadow: 0 4px 14px rgba(0,0,0,0.04);
      margin: 18px 0;
      display: flex;
      align-items: center;
      justify-content: center;
      max-width: 220px;
      max-height: 220px;
    }
    .template-qr-frame img, .template-qr-frame canvas, .template-qr-frame svg {
      width: 180px !important;
      height: 180px !important;
      display: block;
    }
    .template-footer {
      font-size: 0.72rem;
      color: #94A3B8;
      font-weight: 600;
      letter-spacing: 0.03em;
    }

    /* Print Media Query */
    @media print {
      body * {
        visibility: hidden !important;
      }
      #printable-template-target, #printable-template-target * {
        visibility: visible !important;
      }
      #printable-template-target {
        position: fixed !important;
        left: 50% !important;
        top: 50% !important;
        transform: translate(-50%, -50%) !important;
        width: 100% !important;
        max-width: 460px !important;
        min-height: 580px !important;
        border: 2px solid #000 !important;
        box-shadow: none !important;
        padding: 48px 36px !important;
        page-break-inside: avoid !important;
      }
      .template-title {
        font-size: 1.8rem !important;
        color: #000 !important;
      }
      .template-subtitle {
        font-size: 1.05rem !important;
        color: #333 !important;
      }
      .template-qr-frame {
        max-width: 280px !important;
        max-height: 280px !important;
        border: 2px solid #000 !important;
      }
      .template-qr-frame img, .template-qr-frame canvas, .template-qr-frame svg {
        width: 240px !important;
        height: 240px !important;
      }
    }
  `;
  document.head.appendChild(style);

  // Modal HTML structure
  const modalHTML = `
    <div id="print-modal-overlay">
      <div class="print-modal-dialog">
        <div class="print-controls">
          <h3>📄 Print PDF Template</h3>
          <p style="font-size:0.84rem;color:#64748B;margin:0 0 8px 0">
            Export a high-resolution print card for table tents, acrylic stands, or desk displays.
          </p>

          <div>
            <label for="tpl-select">Template Style</label>
            <select id="tpl-select">
              <option value="standee">Acrylic Standee / Counter Display</option>
              <option value="table">Table Tent / Cafe Menu</option>
              <option value="wifi">Wi-Fi Guest Sign</option>
              <option value="review">Google Review 5-Star Card</option>
              <option value="minimal">Minimalist Modern Frame</option>
            </select>
          </div>

          <div>
            <label for="tpl-header">Headline</label>
            <input type="text" id="tpl-header" value="Scan To Connect" maxlength="40">
          </div>

          <div>
            <label for="tpl-sub">Subtext / Instructions</label>
            <input type="text" id="tpl-sub" value="Point your phone camera to scan instantly" maxlength="65">
          </div>

          <div>
            <label for="tpl-color">Theme Accent</label>
            <select id="tpl-color">
              <option value="#4F46E5">Indigo Royal (#4F46E5)</option>
              <option value="#059669">Emerald Green (#059669)</option>
              <option value="#0284C7">Sky Blue (#0284C7)</option>
              <option value="#DC2626">Crimson Red (#DC2626)</option>
              <option value="#0F172A">Jet Black (#0F172A)</option>
            </select>
          </div>

          <button id="do-print-btn" style="margin-top:auto;background:linear-gradient(135deg,#4F46E5,#4338CA);color:#fff;border:none;border-radius:12px;padding:12px 18px;font-weight:700;font-size:0.95rem;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;gap:8px;box-shadow:0 4px 14px rgba(79,70,229,0.35);transition:transform .15s">
            🖨️ Print / Save as PDF
          </button>
        </div>

        <div class="print-preview-pane">
          <button class="close-print-modal" id="close-print-modal" aria-label="Close dialog">&times;</button>
          
          <div id="printable-template-target">
            <div class="template-card-header">
              <div class="template-badge" id="tpl-badge-elem" style="background:rgba(79,70,229,0.1);color:#4F46E5">MyLogoQR</div>
              <h2 class="template-title" id="tpl-title-elem">Scan To Connect</h2>
              <p class="template-subtitle" id="tpl-sub-elem">Point your phone camera to scan instantly</p>
            </div>

            <div class="template-qr-frame" id="tpl-qr-dest">
              <!-- Cloned QR will be injected here -->
            </div>

            <div class="template-footer">
              Free &amp; Private Barcode &bull; Powered by MyLogoQR.com
            </div>
          </div>
        </div>
      </div>
    </div>
  `;

  // Append overlay once DOM is loaded
  function initPrintModal() {
    if (document.getElementById('print-modal-overlay')) return;
    document.body.insertAdjacentHTML('beforeend', modalHTML);

    const overlay = document.getElementById('print-modal-overlay');
    const closeBtn = document.getElementById('close-print-modal');
    const printBtn = document.getElementById('do-print-btn');
    const tplSelect = document.getElementById('tpl-select');
    const headerInput = document.getElementById('tpl-header');
    const subInput = document.getElementById('tpl-sub');
    const colorSelect = document.getElementById('tpl-color');

    const badgeElem = document.getElementById('tpl-badge-elem');
    const titleElem = document.getElementById('tpl-title-elem');
    const subElem = document.getElementById('tpl-sub-elem');
    const qrDest = document.getElementById('tpl-qr-dest');
    const cardTarget = document.getElementById('printable-template-target');

    function updatePreview() {
      const mode = tplSelect.value;
      const color = colorSelect.value;
      
      badgeElem.style.color = color;
      badgeElem.style.backgroundColor = color + '1A'; // 10% opacity hex

      if (mode === 'standee') {
        badgeElem.textContent = 'TABLE / COUNTER DISPLAY';
        cardTarget.style.border = '2px solid ' + color;
      } else if (mode === 'table') {
        badgeElem.textContent = 'TABLE TENT &bull; DINE IN';
        cardTarget.style.border = '2px dashed ' + color;
      } else if (mode === 'wifi') {
        badgeElem.textContent = '📶 HIGH SPEED GUEST WI-FI';
        cardTarget.style.border = '2px solid ' + color;
      } else if (mode === 'review') {
        badgeElem.textContent = '★ ★ ★ ★ ★ FIVE STARS';
        cardTarget.style.border = '2px solid #F59E0B';
        badgeElem.style.color = '#B45309';
        badgeElem.style.backgroundColor = '#FEF3C7';
      } else {
        badgeElem.textContent = 'SCAN ME';
        cardTarget.style.border = '1px solid #CBD5E1';
      }

      titleElem.textContent = headerInput.value || 'Scan To Connect';
      subElem.textContent = subInput.value || 'Point camera to view';
    }

    tplSelect.addEventListener('change', function() {
      if (this.value === 'wifi') {
        headerInput.value = 'Free Guest Wi-Fi';
        subInput.value = 'Scan with camera to connect automatically';
      } else if (this.value === 'review') {
        headerInput.value = 'Review Us On Google';
        subInput.value = 'Loved your experience? Scan to leave a 5-star review!';
      } else if (this.value === 'table') {
        headerInput.value = 'Digital Food & Drinks Menu';
        subInput.value = 'Scan to browse menu and order directly';
      } else {
        headerInput.value = 'Scan To Connect';
        subInput.value = 'Point your phone camera to scan instantly';
      }
      updatePreview();
    });

    headerInput.addEventListener('input', updatePreview);
    subInput.addEventListener('input', updatePreview);
    colorSelect.addEventListener('change', updatePreview);

    closeBtn.addEventListener('click', () => {
      overlay.classList.remove('open');
    });

    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) overlay.classList.remove('open');
    });

    printBtn.addEventListener('click', () => {
      window.print();
    });

    // Global trigger function
    window.openPrintTemplateModal = function() {
      // Find current QR in DOM
      const qrBox = document.getElementById('qr') || document.querySelector('.qrbox');
      qrDest.innerHTML = '';
      if (qrBox) {
        const svg = qrBox.querySelector('svg');
        const canvas = qrBox.querySelector('canvas');
        const img = qrBox.querySelector('img');
        if (svg) {
          qrDest.appendChild(svg.cloneNode(true));
        } else if (canvas) {
          const imgElem = document.createElement('img');
          imgElem.src = canvas.toDataURL('image/png');
          qrDest.appendChild(imgElem);
        } else if (img) {
          qrDest.appendChild(img.cloneNode(true));
        } else {
          qrDest.innerHTML = '<p style="color:#64748B;font-size:0.8rem">Generate a QR code first</p>';
        }
      }
      updatePreview();
      overlay.classList.add('open');
    };

    // Attach to any element with id "open-print-templates-btn" or class "trigger-print-template"
    document.querySelectorAll('#open-print-templates-btn, .trigger-print-template').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        window.openPrintTemplateModal();
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initPrintModal);
  } else {
    initPrintModal();
  }
})();
