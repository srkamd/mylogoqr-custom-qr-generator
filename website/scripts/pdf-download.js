/**
 * MyLogoQR - Direct Instant PDF Downloader
 * Downloads a high-resolution, vector-crisp printable A4 PDF file of the active QR code.
 */
(function() {
  // Ensure jsPDF library is loaded
  if (!window.jspdf) {
    const s = document.createElement('script');
    s.src = '/scripts/jspdf.umd.min.js';
    s.async = true;
    document.head.appendChild(s);
  }

  window.downloadQRCodePDF = function(customFileName) {
    const qrBox = document.getElementById('qr') || document.querySelector('.qrbox');
    if (!qrBox) {
      alert('QR code container not found.');
      return;
    }

    const canvas = qrBox.querySelector('canvas');
    const img = qrBox.querySelector('img');
    let dataUrl = '';
    if (canvas) {
      dataUrl = canvas.toDataURL('image/png');
    } else if (img) {
      dataUrl = img.src;
    }

    if (!dataUrl) {
      alert('Please wait for the QR code to finish generating.');
      return;
    }

    if (window.jspdf && window.jspdf.jsPDF) {
      try {
        const { jsPDF } = window.jspdf;
        // Standard A4 portrait: 210mm x 297mm
        const doc = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' });

        // Outer styling card
        doc.setFillColor(248, 250, 252);
        doc.roundedRect(15, 15, 180, 267, 6, 6, 'F');
        doc.setDrawColor(226, 232, 240);
        doc.setLineWidth(0.8);
        doc.roundedRect(15, 15, 180, 267, 6, 6, 'S');

        // Brand Header
        doc.setFont("helvetica", "bold");
        doc.setFontSize(22);
        doc.setTextColor(18, 22, 58);
        doc.text("MyLogoQR", 105, 36, { align: "center" });

        doc.setFont("helvetica", "normal");
        doc.setFontSize(10.5);
        doc.setTextColor(100, 116, 139);
        doc.text("High-Resolution Vector-Quality QR Code | 100% Free & Permanent", 105, 43, { align: "center" });

        // QR Code Box (130mm x 130mm, centered at x=40, y=55)
        doc.setFillColor(255, 255, 255);
        doc.roundedRect(30, 52, 150, 150, 4, 4, 'F');
        doc.setDrawColor(203, 213, 225);
        doc.setLineWidth(0.5);
        doc.roundedRect(30, 52, 150, 150, 4, 4, 'S');

        doc.addImage(dataUrl, 'PNG', 40, 62, 130, 130);

        // Scan Instructions Callout
        doc.setFont("helvetica", "bold");
        doc.setFontSize(13);
        doc.setTextColor(79, 70, 229);
        doc.text("SCAN WITH ANY SMARTPHONE CAMERA", 105, 222, { align: "center" });

        doc.setFont("helvetica", "normal");
        doc.setFontSize(9.5);
        doc.setTextColor(100, 116, 139);
        doc.text("Point your device camera at the QR code above to open immediately.", 105, 229, { align: "center" });

        // Footer info
        doc.setFontSize(8.5);
        doc.setTextColor(148, 163, 184);
        doc.text("Generated at https://mylogoqr.com  -  Never Expires  -  No Registration", 105, 270, { align: "center" });

        const fileName = customFileName || ('mylogoqr-code-' + Date.now() + '.pdf');
        doc.save(fileName);
      } catch (err) {
        console.error("PDF generation error:", err);
        // Fallback to Print Studio modal
        if (typeof window.openPrintTemplateModal === 'function') {
          window.openPrintTemplateModal();
        } else {
          window.print();
        }
      }
    } else {
      // If jsPDF is still loading, fallback to print studio
      if (typeof window.openPrintTemplateModal === 'function') {
        window.openPrintTemplateModal();
      } else {
        window.print();
      }
    }
  };

  // Global event delegation for #btn-download-pdf and .trigger-download-pdf
  document.addEventListener('click', function(e) {
    const btn = e.target.closest('#btn-download-pdf, .trigger-download-pdf');
    if (btn) {
      e.preventDefault();
      window.downloadQRCodePDF();
    }
  });
})();
