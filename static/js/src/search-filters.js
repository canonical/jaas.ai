/**
  Update the filter query strings.
  @param {String} type the type of filter to change.
  @param {String} value the new filter value.
*/
function searchChangeFilter(type, value) {
  const url = window.location.href.split('?')[0];
  const queries = {};
  window.location.search
    .substr(1)
    .split('&')
    .forEach((ele) => {
      const parts = ele.split('=');
      if (parts[0]) {
        // eslint-disable-next-line prefer-destructuring
        queries[parts[0]] = parts[1];
      }
    });
  // No need to change the url if the filter value is already selected.
  if (value !== queries[type]) {
    queries[type] = value;
    const queryString = Object.keys(queries)
      .map((key) => `${key}=${queries[key]}`)
      .join('&');
    window.location = `${url}?${queryString}`;
  }
}
document
  .querySelector('.js-sort-select')
  .addEventListener('change', (e) => searchChangeFilter('sort', e.target.value));

function toggleMenu(element, show) {
  element.setAttribute('aria-expanded', show);
  element.classList.toggle('p-contextual-menu__toggle--active', show);
  const control = document.querySelector(element.getAttribute('aria-controls'));
  if (control) {
    control.setAttribute('aria-hidden', !show);
  }
}

function setupContextualMenuListeners(contextualMenuToggleSelector) {
  const toggles = document.querySelectorAll(contextualMenuToggleSelector);
  toggles.forEach((toggle) => {
    toggle.addEventListener('mousedown', (e) => {
      e.preventDefault();
      const {target} = e;
      target.blur();
      document.querySelector('.p-contextual-menu__dropdown').focus();
      const menuAlreadyOpen = target.getAttribute('aria-expanded') === 'true';
      toggleMenu(target, !menuAlreadyOpen);
    });
  });
  document.addEventListener('click', (e) => {
    toggles.forEach((toggle) => {
      const contextualMenu = document.querySelector(toggle.getAttribute('aria-controls'));
      const clickOutside = !(toggle.contains(e.target) || contextualMenu.contains(e.target));
      if (clickOutside) {
        toggleMenu(toggle, false);
      }
    });
  });
  const oldKeyDown = document.onkeydown;
  document.onkeydown = (e) => {
    e = e || window.event;
    if (e.keyCode === 27) {
      toggles.forEach((toggle) => {
        toggleMenu(toggle, false);
      });
    }
    // If another script provides a document.onkeydown then call it here so it still works.
    if (oldKeyDown) {
      oldKeyDown(e);
    }
  };
}

setupContextualMenuListeners('.p-contextual-menu__toggle');
