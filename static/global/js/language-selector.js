const LANGUAGE_STORAGE_KEY = 'preferredLanguage';

const normalizeLanguage = (language) => {
  if (!language) return 'pt-br';
  const lower = language.toLowerCase();
  if (lower.startsWith('pt')) return 'pt-br';
  return 'en';
};

const getPreferredLanguage = () => {
  const stored = localStorage.getItem(LANGUAGE_STORAGE_KEY);
  if (stored && stored !== 'auto') return stored;
  return normalizeLanguage(navigator.language);
};

const getTargetUrl = (menu, language) => {
  if (language === 'pt-br') return menu.dataset.ptUrl;
  if (language === 'en') return menu.dataset.enUrl;
  return null;
};

const showActiveLanguage = (menu, selection, focus = false) => {
  const languageSwitcher = document.querySelector('#bd-language');
  if (!languageSwitcher) return;
  const labelMap = {
    auto: menu.dataset.labelAuto || 'Language: Auto',
    'pt-br': menu.dataset.labelPt || 'Language: PT',
    en: menu.dataset.labelEn || 'Language: EN',
  };

  const items = menu.querySelectorAll('[data-language]');
  items.forEach((element) => {
    element.classList.remove('active');
    element.setAttribute('aria-pressed', 'false');
  });

  const target = menu.querySelector(`[data-language="${selection}"]`);
  if (target) {
    target.classList.add('active');
    target.setAttribute('aria-pressed', 'true');
    languageSwitcher.setAttribute('aria-label', labelMap[selection] || selection);
  }

  if (focus) {
    languageSwitcher.focus();
  }
};

const updateLabel = (menu, selection) => {
  const label = document.getElementById('language-label');
  if (!label) return;
  const labelMap = {
    auto: menu.dataset.labelAuto || 'Language: Auto',
    'pt-br': menu.dataset.labelPt || 'Language: PT',
    en: menu.dataset.labelEn || 'Language: EN',
  };
  if (selection === 'auto') {
    label.textContent = labelMap.auto;
  } else if (selection === 'pt-br') {
    label.textContent = labelMap['pt-br'];
  } else {
    label.textContent = labelMap.en;
  }
};

const applyLanguageSelection = (menu) => {
  const selection = localStorage.getItem(LANGUAGE_STORAGE_KEY) || 'auto';
  const currentLanguage = menu.dataset.currentLanguage;
  const targetLanguage = selection === 'auto' ? getPreferredLanguage() : selection;

  updateLabel(menu, selection);
  showActiveLanguage(menu, selection);

  if (currentLanguage === targetLanguage) return;

  const targetUrl = getTargetUrl(menu, targetLanguage);
  if (targetUrl) {
    window.location.assign(targetUrl);
  }
};

const initLanguageSelector = () => {
  const menu = document.querySelector('[data-current-language][data-pt-url][data-en-url]');
  if (!menu) return;

  menu.querySelectorAll('[data-language]').forEach((item) => {
    item.addEventListener('click', (event) => {
      event.preventDefault();
      const language = item.dataset.language;
      if (!language) return;

      localStorage.setItem(LANGUAGE_STORAGE_KEY, language);
      updateLabel(menu, language);
      showActiveLanguage(menu, language, true);

      const targetLanguage = language === 'auto' ? getPreferredLanguage() : language;
      const targetUrl = getTargetUrl(menu, targetLanguage);
      if (targetUrl) {
        window.location.assign(targetUrl);
      }
    });
  });

  applyLanguageSelection(menu);
};

document.addEventListener('DOMContentLoaded', initLanguageSelector);
