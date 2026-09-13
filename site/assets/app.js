(() => {
  const items = [...document.querySelectorAll('.catalog-item')];
  const filterButtons = [...document.querySelectorAll('[data-filter]')];
  const search = document.querySelector('#catalog-search');
  const count = document.querySelector('#visible-count');
  const status = document.querySelector('#filter-status');
  const empty = document.querySelector('#empty-state');
  const reset = document.querySelector('#reset-filter');
  let activeFilter = 'all';

  const updateCatalog = () => {
    const query = search.value.trim().toLowerCase();
    let visible = 0;

    items.forEach((item) => {
      const matchesFilter = activeFilter === 'all' || item.dataset.category === activeFilter;
      const matchesQuery = !query || `${item.dataset.search} ${item.textContent}`.toLowerCase().includes(query);
      item.hidden = !(matchesFilter && matchesQuery);
      if (!item.hidden) visible += 1;
    });

    count.textContent = String(visible);
    empty.hidden = visible !== 0;
    const category = activeFilter === 'all' ? 'all work' : `${activeFilter} work`;
    status.textContent = query
      ? `Showing ${visible} ${visible === 1 ? 'route' : 'routes'} for “${search.value.trim()}” in ${category}.`
      : `Showing ${visible === items.length ? 'all ' : ''}${visible} ${visible === 1 ? 'route' : 'routes'}${activeFilter === 'all' ? '.' : ` in ${category}.`}`;
  };

  filterButtons.forEach((button) => {
    button.addEventListener('click', () => {
      activeFilter = button.dataset.filter;
      filterButtons.forEach((candidate) => candidate.setAttribute('aria-pressed', String(candidate === button)));
      updateCatalog();
    });
  });

  search.addEventListener('input', updateCatalog);
  reset.addEventListener('click', () => {
    activeFilter = 'all';
    search.value = '';
    filterButtons.forEach((button) => button.setAttribute('aria-pressed', String(button.dataset.filter === 'all')));
    updateCatalog();
    search.focus();
  });

  const form = document.querySelector('#contact-form');
  const submit = document.querySelector('#contact-submit');
  const formStatus = document.querySelector('#contact-status');

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    formStatus.textContent = '';
    formStatus.dataset.state = '';

    if (!form.reportValidity()) return;

    const data = new FormData(form);
    submit.disabled = true;
    submit.textContent = 'Sending…';

    try {
      const response = await fetch('/api/forms/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: data.get('name'),
          email: data.get('email'),
          interest: 'consulting',
          message: data.get('message'),
          website: data.get('website') || undefined,
        }),
      });

      if (!response.ok) throw new Error(`Request failed with status ${response.status}`);
      form.reset();
      formStatus.dataset.state = 'success';
      formStatus.textContent = 'Request received. The team will answer whether it is a fit.';
    } catch (error) {
      console.error('Contact form submission failed', error);
      formStatus.dataset.state = 'error';
      formStatus.textContent = 'Something went wrong. Email jeremy@intentsolutions.io directly.';
    } finally {
      submit.disabled = false;
      submit.textContent = 'Send to Intent Solutions';
    }
  });

  updateCatalog();
})();
