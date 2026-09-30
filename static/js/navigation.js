(() => {
  const header = document.querySelector('.site-header');
  const navigation = document.querySelector('#primary-navigation');
  const toggle = document.querySelector('#navigation-toggle');
  const languageDropdown = document.querySelector('#language-dropdown');
  const summary = languageDropdown.querySelector('summary');
  const mobile = matchMedia('(max-width: 1100px)');

  const setNavigation = open => {
    navigation.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? toggle.dataset.closeLabel : toggle.dataset.openLabel);
  };

  toggle.hidden = false;
  header.classList.add('navigation-ready');
  toggle.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') !== 'true';
    languageDropdown.open = false;
    setNavigation(open);
  });

  languageDropdown.addEventListener('toggle', () => {
    if (languageDropdown.open && mobile.matches) setNavigation(false);
  });

  document.addEventListener('click', event => {
    if (!languageDropdown.contains(event.target)) languageDropdown.open = false;
    if (!header.contains(event.target)) setNavigation(false);
  });

  document.addEventListener('keydown', event => {
    if (event.key !== 'Escape') return;
    if (languageDropdown.open) {
      languageDropdown.open = false;
      summary.focus();
      event.preventDefault();
    } else if (toggle.getAttribute('aria-expanded') === 'true') {
      setNavigation(false);
      toggle.focus();
      event.preventDefault();
    }
  });

  document.addEventListener('focusin', event => {
    if (!languageDropdown.contains(event.target)) languageDropdown.open = false;
    if (!header.contains(event.target)) setNavigation(false);
  });

  navigation.addEventListener('click', event => {
    if (event.target.closest('a')) setNavigation(false);
  });

  mobile.addEventListener('change', () => {
    const focusInsideNavigation = navigation.contains(document.activeElement);
    setNavigation(false);
    languageDropdown.open = false;
    if (mobile.matches && focusInsideNavigation) toggle.focus();
    if (!mobile.matches && document.activeElement === toggle) summary.focus();
  });
})();
