/**
 * MyLogoQR - Smart Android App Banner
 * Promotes the official Google Play store app with non-intrusive dismissible UI
 */
(function() {
  if (localStorage.getItem('hide_smart_banner') === '1') return;

  const style = document.createElement('style');
  style.textContent = `
    #smart-app-banner {
      display: none;
      position: fixed;
      bottom: 20px;
      left: 50%;
      transform: translateX(-50%);
      width: calc(100% - 32px);
      max-width: 440px;
      background: #0B0F19;
      border: 1px solid rgba(255, 255, 255, 0.16);
      box-shadow: 0 16px 40px -8px rgba(0, 0, 0, 0.65), 0 0 0 1px rgba(255, 255, 255, 0.08);
      border-radius: 18px;
      padding: 12px 14px;
      z-index: 99999;
      align-items: center;
      gap: 12px;
      color: #FFFFFF;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      animation: bannerSlideUp 0.35s cubic-bezier(0.16, 1, 0.3, 1);
    }
    @keyframes bannerSlideUp {
      from { transform: translate(-50%, 60px); opacity: 0; }
      to { transform: translate(-50%, 0); opacity: 1; }
    }
    .sab-icon {
      width: 44px;
      height: 44px;
      border-radius: 11px;
      box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
      flex-shrink: 0;
      object-fit: cover;
    }
    .sab-info {
      flex: 1;
      min-width: 0;
    }
    .sab-title {
      font-weight: 700;
      font-size: 0.92rem;
      color: #FFFFFF;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      margin-bottom: 2px;
    }
    .sab-desc {
      font-size: 0.74rem;
      color: #94A3B8;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .sab-star {
      color: #F59E0B;
      font-weight: 700;
    }
    .sab-action {
      background: linear-gradient(135deg, #10B981, #059669);
      color: #FFFFFF !important;
      font-weight: 700;
      font-size: 0.82rem;
      padding: 8px 16px;
      border-radius: 10px;
      text-decoration: none !important;
      white-space: nowrap;
      box-shadow: 0 4px 12px rgba(16, 185, 129, 0.35);
      transition: transform .15s ease, filter .15s ease;
      display: inline-flex;
      align-items: center;
    }
    .sab-action:hover {
      transform: translateY(-1px);
      filter: brightness(1.08);
    }
    .sab-close {
      background: none;
      border: none;
      color: #94A3B8;
      cursor: pointer;
      font-size: 20px;
      line-height: 1;
      padding: 4px;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: color .15s;
    }
    .sab-close:hover {
      color: #FFFFFF;
    }
    @media print {
      #smart-app-banner {
        display: none !important;
      }
    }
  `;
  document.head.appendChild(style);

  const bannerHTML = `
    <div id="smart-app-banner" role="complementary" aria-label="Mobile app banner">
      <button class="sab-close" id="close-smart-app-banner" aria-label="Close banner">&times;</button>
      <img src="/app_icon.jpg" alt="MyLogoQR Icon" class="sab-icon">
      <div class="sab-info">
        <div class="sab-title">MyLogoQR App</div>
        <div class="sab-desc">
          <span class="sab-star">★ 4.9</span> &bull; <span>Free &bull; No Ads</span>
        </div>
      </div>
      <a href="https://play.google.com/store/apps/details?id=com.mylogoqr.app" target="_blank" rel="noopener noreferrer" class="sab-action">
        GET APP
      </a>
    </div>
  `;

  function initBanner() {
    if (document.getElementById('smart-app-banner')) return;
    document.body.insertAdjacentHTML('beforeend', bannerHTML);

    const banner = document.getElementById('smart-app-banner');
    const closeBtn = document.getElementById('close-smart-app-banner');

    // Show banner after 2 seconds
    setTimeout(() => {
      if (localStorage.getItem('hide_smart_banner') !== '1') {
        banner.style.display = 'flex';
      }
    }, 1800);

    closeBtn.addEventListener('click', () => {
      banner.style.display = 'none';
      localStorage.setItem('hide_smart_banner', '1');
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initBanner);
  } else {
    initBanner();
  }
})();
