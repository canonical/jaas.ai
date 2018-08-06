window.Jujucharms.cookieNotification = templateSelector => {
  if (!Cookies.get('_cookies_accepted')) {
    const templateElement = document.querySelector(templateSelector);
    if (!templateElement) {
      return;
    }
    document.querySelector('body').insertAdjacentHTML('beforeend', templateElement.innerText);
    document
      .querySelector('.cookie-policy .link-cta')
      .addEventListener('click', e => {
        e.preventDefault();
        Cookies.set(
          '_cookies_accepted', 'true', {expires: new Date('January 12, 2050')});
        document.querySelector('.cookie-policy').remove();
      });
  }
};
