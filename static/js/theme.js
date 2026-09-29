(() => {
  let theme;
  try { theme = localStorage.getItem('nq-theme'); } catch {}
  document.documentElement.dataset.bsTheme = ['light', 'dark'].includes(theme) ? theme : (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
})();
