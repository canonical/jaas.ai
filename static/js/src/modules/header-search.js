const handleSearch = () => {
  document.querySelector('[data-js="search-form"]').addEventListener('submit', e => {
    e.preventDefault();
    const text = document.querySelector('[data-js="search-form-text"]').value;
    const re = new RegExp(' ', 'g');
    const url = '/q/' + text.replace(re, '/');
    window.location.pathname = url;
  });
};

export default handleSearch;
