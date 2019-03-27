window.app.modal = function(modalId) {
  const modal = document.querySelector(`#${modalId}`);
  const modalTrigger = document.querySelector(`[data-js=${modalId}Trigger]`);

  modalTrigger.onclick = function() {
    modal.classList.remove('p-modal--hidden');
  };

  const closeModal = document.querySelector(`#${modalId} [data-js=modalClose]`);
  closeModal.onclick = function() {
    modal.classList.add('p-modal--hidden');
  };

  modal.onclick = function(e) {
    modal.classList.add('p-modal--hidden');
  };

  document.querySelector(`.p-modal__dialog`).onclick = function(e) {
    e.stopPropagation();
  };
};
