window.Jujucharms.onboardingNotification = (containerSelector, templateSelector) => {
  const templateElement = document.querySelector(templateSelector);
  const container = document.querySelector(containerSelector);
  if (templateElement) {
    const cookieName = templateElement.dataset.cookie;
    if (!Cookies.get(cookieName)) {
      container.insertAdjacentHTML('beforeend', templateElement.innerText);
    }
    document
      .querySelector('.onboarding-notification__close')
      .addEventListener('click', e => {
        e.preventDefault();
        Cookies.set(cookieName, 'true', {expires: new Date('January 12, 2050')});
        document.querySelector(containerSelector).remove();
      });
  }
};
