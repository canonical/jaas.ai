window.Jujucharms.entityDetailsSetup = () => {
  document.addEventListener('click', e => {
    if (!e.target.classList.contains('section__title')) {
      return;
    }
    const ancestor = e.target.closest('.section');
    if (ancestor.classList.contains('is-closed')) {
      ancestor.classList.remove('is-closed');
    } else {
      ancestor.classList.add('is-closed');
    }
  });

  document.addEventListener('click', e => {
    if (!e.target.classList.contains('files__list--item-folder')) {
      return;
    }
    if (e.target.classList.contains('is-closed')) {
      e.target.classList.remove('is-closed');
    } else {
      e.target.classList.add('is-closed');
    }
  });

  document.addEventListener('click', e => {
    const target = e.target;
    const cl = target.classList;
    if (!cl.contains('btn__see--more') && !cl.contains('btn__see--less')) {
      return;
    }
    e.preventDefault();
    if (cl.contains('btn__see--more')) {
      const ancestor = target.closest('.list--concealed');
      ancestor.classList.remove('list--concealed');
      ancestor.classList.add('list--revealed');
    } else {
      const ancestor = target.closest('.list--revealed');
      ancestor.classList.remove('list--revealed');
      ancestor.classList.add('list--concealed');
    }
  });
};
