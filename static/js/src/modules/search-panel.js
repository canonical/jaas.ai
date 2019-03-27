const searchPanel = () => {
  /**
    Sets up the search handler.
  */
  const form = document.querySelector('[data-js="search-form"]'),
    input = document.querySelector('[data-js="form-text"]'),
    header = document.querySelector('[data-js="navigation"]'),
    searchClose = document.querySelector('[data-js="search-close"]');

  input.addEventListener('focus', e => {
    header.classList.add('search-active');
  });

  if (searchClose !== null) {
    searchClose.addEventListener('click', e => {
      e.preventDefault();
      header.classList.remove('search-active');
      input.value = '';
    });
  }

  window.addEventListener('keydown', e => {
    if (e.keyCode === 27) {
      input.blur();
    }
  });

  form.addEventListener('submit', e => {
    e.preventDefault();
    const text = document.querySelector('input[name="text"]').value;
    const re = new RegExp(' ', 'g');
    const url = '/q/' + text.replace(re, '/');
    window.location.pathname = url;
  });

  // Close search panel is anywhere outside header and search panel area is clicked
  const html = document.querySelector('html');
  html.addEventListener('click', event => {
    if (!header.contains(event.target)) {
      header.classList.remove('search-active');
    }
  });
};

export default searchPanel;
