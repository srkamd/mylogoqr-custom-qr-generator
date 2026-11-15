/**
 * MyLogoQR - Instant Full-Page Multi-Language Translation Engine
 * Translates 100% of the website's words (headings, paragraphs, buttons, tabs, forms, and FAQs)
 * Supports: English, Spanish, Portuguese, Russian, Italian, Urdu, Arabic, French, German
 */
(function() {
  // Inject hidden Google Translate container
  if (!document.getElementById('google_translate_element')) {
    const div = document.createElement('div');
    div.id = 'google_translate_element';
    div.style.display = 'none';
    document.body.appendChild(div);
  }

  // Load Google Translate API script
  if (!window.google || !window.google.translate) {
    window.googleTranslateElementInit = function() {
      new google.translate.TranslateElement({
        pageLanguage: 'en',
        includedLanguages: 'es,pt,ru,it,ur,ar,fr,de',
        autoDisplay: false
      }, 'google_translate_element');
    };

    const s = document.createElement('script');
    s.type = 'text/javascript';
    s.src = '//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
    s.async = true;
    document.head.appendChild(s);
  }

  // Global translation trigger function
  window.translatePage = function(langCode) {
    if (!langCode || langCode === 'en' || langCode === '/') {
      // Clear cookies and restore English
      document.cookie = 'googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
      document.cookie = 'googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; domain=' + window.location.hostname + '; path=/;';
      localStorage.removeItem('preferred_lang');
      window.location.reload();
      return;
    }

    // Standardize langCode (e.g. '/es/' -> 'es')
    langCode = langCode.replace(/\//g, '').trim();

    localStorage.setItem('preferred_lang', langCode);
    document.cookie = 'googtrans=/en/' + langCode + '; path=/;';
    document.cookie = 'googtrans=/en/' + langCode + '; domain=' + window.location.hostname + '; path=/;';

    const combo = document.querySelector('.goog-te-combo');
    if (combo) {
      combo.value = langCode;
      combo.dispatchEvent(new Event('change'));
    } else {
      window.location.reload();
    }
  };

  // Sync select dropdown state with current translation
  document.addEventListener('DOMContentLoaded', function() {
    const savedLang = localStorage.getItem('preferred_lang');
    if (savedLang) {
      const select = document.getElementById('lang-switcher') || document.querySelector('.lang-picker select');
      if (select) {
        for (let i = 0; i < select.options.length; i++) {
          if (select.options[i].value.replace(/\//g, '') === savedLang) {
            select.selectedIndex = i;
            break;
          }
        }
      }
    }
  });
})();
