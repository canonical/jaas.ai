/*
  Allow users to open a modal overlay
*/
const modal = () => {
  /**
    Activate modals
    @method modal.instantiateModals
    @static
  * */
  const instantiateModals = (modals) => {
    modals.forEach((modalEl) => {
      const modalId = modalEl.getAttribute('id');
      const modalTrigger = document.querySelector(`[data-js=${modalId}Trigger]`);
      const closeModal = modalEl.querySelector(`#${modalId} [data-js=modalClose]`);
      const modalDialog = modalEl.querySelector(`.p-modal__dialog`);

      modalTrigger.addEventListener('click', () => {
        modalEl.classList.remove('p-modal--hidden');
      });

      closeModal.addEventListener('click', () => {
        modalEl.classList.add('p-modal--hidden');
      });

      modalEl.addEventListener('click', () => {
        modalEl.classList.add('p-modal--hidden');
      });

      modalDialog.addEventListener('click', (e) => {
        e.stopPropagation();
      });
    });
  };

  // Check to ensure modal elements exist on the page
  const modals = document.querySelectorAll('.p-modal');
  // If so, instantiate.
  if (modals.length) {
    instantiateModals(modals);
  }
};

export default modal;
