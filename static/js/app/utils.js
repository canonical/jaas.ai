window.Jujucharms.utils = {
  /**
   * Generates a storefront url given an entity (bundle or charm) ID.
   * @param {String} entityId The ID to turn into a url.
   * @return The url.
   */
  generateEntityUrlFromId: function(entityId) {
    var entity = '',
      owner = '',
      series = '',
      revision = '';
    var idParts = entityId.replace(/^cs:/, '').split('/');
    entity = idParts.pop();
    var entityParts = entity.split('-');
    if (/^\d+$/.test(entityParts[entityParts.length - 1])) {
      entity = entityParts.splice(0, entityParts.length - 1).join('-');
      revision = entityParts[0] + '/';
    }
    entity = entity + '/';
    if (/^~/.test(idParts[0])) {
      owner = idParts.shift().replace(/^~/, 'u/') + '/';
    }
    if (idParts[0]) {
      series = idParts[0] + '/';
    }
    return '/' + owner + entity + series + revision;
  },
  /**
    Sets up the search handler.
  */
  setupSearch: function() {
    const form = document.querySelector('.search-form'),
      input = document.querySelector('.search-form .form-text'),
      header = document.querySelector('header.banner'),
      searchClose = document.querySelector('.search-close');

    input.addEventListener('focus', e => {
      header.classList.add('search-active');
    });

    input.addEventListener('blur', e => {
      header.classList.remove('search-active');
    });

    if (searchClose !== null) {
      searchClose.addEventListener('click', e => {
        e.preventDefault();
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
  }
};
