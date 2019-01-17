window.Jujucharms.slideout = () => {
  const slideoutToggles = document.querySelectorAll('.slideout .slideout__toggle');
  const slideoutAnchors = document.querySelectorAll('.slideout a');

  slideoutAnchors.forEach(ele =>
    ele.addEventListener('click', e => e.stopImmediatePropagation())
  );

  slideoutToggles.forEach(ele =>
    ele.addEventListener('click', e => {
      e.preventDefault();
      const ancestor = e.target.closest('.slideout');
      if (ancestor.classList.contains('open')) {
        ancestor.classList.remove('open');
      } else {
        ancestor.classList.add('open');
      }
    })
  );
};
