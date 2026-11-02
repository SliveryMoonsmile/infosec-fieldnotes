(() => {
  'use strict';
  const themeButton = document.querySelector('.theme-toggle');
  function applyTheme(theme) {
    document.documentElement.dataset.theme = theme;
    themeButton?.setAttribute('aria-label', `Switch to ${theme === 'light' ? 'dark' : 'light'} theme`);
  }
  try { applyTheme(localStorage.getItem('fieldnotes-theme') || 'dark'); } catch { applyTheme('dark'); }
  themeButton?.addEventListener('click', () => {
    const theme = document.documentElement.dataset.theme === 'light' ? 'dark' : 'light';
    applyTheme(theme);
    try { localStorage.setItem('fieldnotes-theme', theme); } catch { /* Private browsing may block storage. */ }
  });
  const menu = document.querySelector('.menu-toggle');
  function closeMenu() { document.body.classList.remove('nav-open'); menu?.setAttribute('aria-expanded', 'false'); }
  menu?.addEventListener('click', () => {
    const opened = document.body.classList.toggle('nav-open');
    menu.setAttribute('aria-expanded', String(opened));
  });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeMenu(); });
  document.querySelector('main')?.addEventListener('click', closeMenu);
  document.querySelectorAll('#sidebar a').forEach(a => a.addEventListener('click', closeMenu));
  document.querySelector('.print-button')?.addEventListener('click', () => window.print());

  document.querySelectorAll('pre').forEach(pre => {
    const button = document.createElement('button');
    button.className = 'copy-button'; button.textContent = 'Copy'; button.setAttribute('aria-label','Copy code');
    button.addEventListener('click', async () => {
      const code = pre.querySelector('code');
      try {
        await navigator.clipboard.writeText(code.textContent);
        button.textContent = 'Copied';
        document.querySelector('#copy-status').textContent = 'Code copied to clipboard.';
      } catch {
        const selection = window.getSelection();
        const range = document.createRange(); range.selectNodeContents(code);
        selection.removeAllRanges(); selection.addRange(range);
        button.textContent = 'Selected';
        document.querySelector('#copy-status').textContent = 'Code selected. Use your keyboard to copy.';
      }
      setTimeout(() => { button.textContent = 'Copy'; }, 1800);
    });
    pre.append(button);
  });

  const search = document.querySelector('#article-search');
  if (search) {
    let category = 'All';
    const cards = [...document.querySelectorAll('#article-grid .article-card')];
    const records = window.FIELDNOTES_SEARCH || [];
    function update() {
      const query = search.value.toLocaleLowerCase().trim();
      let shown = 0;
      cards.forEach((card, i) => {
        const entry = records[i];
        const haystack = entry ? `${entry.title} ${entry.summary} ${entry.category} ${entry.text}` : card.textContent;
        const visible = (category === 'All' || card.dataset.category === category) && haystack.toLocaleLowerCase().includes(query);
        card.hidden = !visible; if (visible) shown++;
      });
      document.querySelector('#result-count').textContent = `${shown} ${shown === 1 ? 'note' : 'notes'}${query ? ' matching your search' : ''}`;
      document.querySelector('#empty-state').hidden = shown !== 0;
      const params = new URLSearchParams();
      if (query) params.set('q', search.value); if (category !== 'All') params.set('topic', category);
      try { history.replaceState(null, '', `${location.pathname}${params.size ? '?' + params : ''}`); } catch { /* Local file previews may disallow history. */ }
    }
    const initial = new URLSearchParams(location.search);
    search.value = initial.get('q') || '';
    const filters = [...document.querySelectorAll('.filter')];
    if (filters.some(b => b.dataset.filter === initial.get('topic'))) category = initial.get('topic');
    function selectFilter() { filters.forEach(b => { const active=b.dataset.filter===category; b.classList.toggle('is-active',active); b.setAttribute('aria-pressed',String(active)); }); }
    selectFilter();
    filters.forEach(button => button.addEventListener('click', () => { category=button.dataset.filter; selectFilter(); update(); }));
    search.addEventListener('input', update); update();
    document.addEventListener('keydown', event => {
      if (event.key === '/' && !event.ctrlKey && !event.metaKey && !['INPUT','TEXTAREA'].includes(document.activeElement.tagName)) { event.preventDefault(); search.focus(); }
    });
  }
})();
