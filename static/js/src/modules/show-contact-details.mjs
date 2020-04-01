const showContactDetails = () => {
  const button = document.querySelector('[data-js="show-btn"]');
  if (button) {
    button.addEventListener('click', (e) => {
      e.preventDefault();
      button.classList.add('u-hide');
      document.querySelector('[data-js="contact-info"]').classList.remove('u-hide');
    });
  }
};

export default showContactDetails;
