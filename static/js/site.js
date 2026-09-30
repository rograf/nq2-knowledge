(() => {
  const button = document.querySelector('#theme-toggle');
  const updateLabel = () => {
    const label = document.documentElement.dataset.bsTheme === 'dark' ? button.dataset.lightLabel : button.dataset.darkLabel;
    button.setAttribute('aria-label', label);
    button.title = label;
  };
  button.hidden = false;
  updateLabel();
  button.addEventListener('click', () => {
    const theme = document.documentElement.dataset.bsTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.dataset.bsTheme = theme;
    try { localStorage.setItem('nq-theme', theme); } catch {}
    updateLabel();
  });
  const box = document.querySelector('[data-search-url]');
  if (!box) return;
  box.hidden = false;
  const input = box.querySelector('input');
  const results = box.querySelector('#search-results');
  const status = box.querySelector('#search-status');
  const normalize = text => text.toLocaleLowerCase(document.documentElement.lang).normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/ł/g, 'l');
  let index;
  let request = 0;
  input.addEventListener('input', async () => {
    const current = ++request;
    const query = normalize(input.value.trim());
    results.replaceChildren();
    status.textContent = '';
    if (query.length < 2) return;
    try {
      status.textContent = box.dataset.searching;
      if (!index) {
        const response = await fetch(box.dataset.searchUrl);
        if (!response.ok) throw new Error('Search unavailable');
        index = await response.json();
      }
      if (current !== request) return;
      const words = query.split(/\s+/);
      const matches = index.filter(page => words.every(word => normalize(`${page.title} ${page.description} ${page.content}`).includes(word))).slice(0, 12);
      status.textContent = matches.length ? `${box.dataset.results} ${matches.length}` : box.dataset.noResults;
      for (const page of matches) {
        const li = document.createElement('li');
        const link = document.createElement('a');
        link.href = page.url;
        link.textContent = page.title;
        const subtitle = document.createElement('small');
        subtitle.textContent = `${page.section} · ${page.description}`;
        link.append(subtitle);
        li.append(link);
        results.append(li);
      }
    } catch {
      if (current === request) status.textContent = box.dataset.unavailable;
    }
  });
})();
