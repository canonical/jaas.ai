window.app.modal = function() {
  const modal = document.querySelector('.p-modal');
  const modalTrigger = document.querySelector('[data-js=modalTrigger]');

  window.onload = function() {
    modal.classList.remove('u-hide');
  };

  modalTrigger.onclick = function() {
    modal.classList.remove('p-modal--hidden');
  };

  const closeModal = document.querySelector('[data-js=modalClose]');
  closeModal.onclick = function() {
    modal.classList.add('p-modal--hidden');
  };
};
