// Delegate error events to load default icons.
document.querySelectorAll('.search-results-table').forEach((table) => {
  table.addEventListener(
    'error',
    (evt) => {
      if (evt.target.classList.contains('search-results__icon')) {
        evt.target.src = 'https://assets.ubuntu.com/v1/d64591a6-default-charm.svg';
      }
    },
    true
  );
});
