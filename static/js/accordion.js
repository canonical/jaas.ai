/**
  Accordion to show config of bundles in bundles template
* */
window.app.accordion = (accordionList) => {
  /**
    Attaches event listeners for the accordion open and close click events.
    @param {String} accordionContainerSelector The selector of the accordion container.
  */
  function setupAccordionListener(accordionContainerSelector) {
    /**
      Toggles the necessary values on the accordion panels and handles to show or
      hide depending on the supplied values.
      @param {HTMLElement} element The tab that acts as the handles for the
        accordion panes.
      @param {Boolean} show Whether to show or hide the accordion panel.
    */
    const toggle = (element, show) => {
      element.setAttribute('aria-expanded', show);
      ariaControls = document.querySelector(element.getAttribute('aria-controls'));

      if (ariaControls) {
        ariaControls.setAttribute('aria-hidden', !show);
      }
    };
    // Set up an event listener on the container so that panels can be added
    // and removed and events do not need to be managed separately.
    document.querySelector(accordionContainerSelector).addEventListener('click', (e) => {
      const {target} = e;
      panelAlreadyOpen = e.target.getAttribute('aria-expanded');
      if (panelAlreadyOpen === 'false') {
        toggle(target, true);
      } else {
        toggle(target, false);
      }
    });
  }

  setupAccordionListener(accordionList);
};
