window.Jujucharms.lightbox = function() {
  var lightboxes = document.querySelectorAll('.lightbox');

  /**
    Add interactions for lightboxes.

    @param {HTMLElement} lightbox The lightbox element.
  */
  function addLightboxInteraction(lightbox) {
    var id = lightbox.id;
    var controlledBy = document.querySelector('[aria-controls="' + id + '"]');

    controlledBy.addEventListener(
      'click',
      function(e) {
        e.preventDefault();
        lightbox.classList.remove('hidden');
      }.bind(this)
    );

    lightbox.querySelector('.lightbox__close').addEventListener('click', function(e) {
      e.preventDefault();
      lightbox.classList.add('hidden');
    });
  }

  for (var i = 0, ii = lightboxes.length; i < ii; i += 1) {
    addLightboxInteraction(lightboxes[i]);
  }
};
