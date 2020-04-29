const searchPanel = () => {
  /**
    Sets up the search handler.
  */
  const input = document.querySelector('[data-js="form-text"]');
  const header = document.querySelector('[data-js="navigation"]');
  const searchClose = document.querySelector('[data-js="search-close"]');
  const searchReset = document.querySelector('[data-js="search-reset"]');

  input.addEventListener('focus', () => {
    header.classList.add('search-active');
  });

  if (searchClose !== null) {
    searchClose.addEventListener('click', (e) => {
      e.preventDefault();
      header.classList.remove('search-active');
    });
  }

  if (searchReset !== null) {
    searchReset.addEventListener('click', (e) => {
      e.preventDefault();
      input.value = '';
    });
  }

  // Close search panel if anywhere outside header and search panel area is clicked.
  const html = document.querySelector('html');
  html.addEventListener('click', (event) => {
    if (!header.contains(event.target)) {
      header.classList.remove('search-active');
    }
  });
};

export default searchPanel;
