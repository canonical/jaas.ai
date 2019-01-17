window.Jujucharms.stickyHeader = () => {
  // copied from the old detail-view
  const header = document.querySelector('.entity-header');
  let enabled = window.Jujucharms._stickyHeaderEnabled;

  function setSticky() {
    header.classList.add('entity-header--sticky');
    enabled = true;
  }

  function unsetSticky() {
    header.classList.remove('entity-header--sticky');
    enabled = false;
  }

  function onScroll() {
    if (window.scrollY > triggerSticky && !enabled) {
      setSticky();
    } else if (window.scrollY < triggerSticky && enabled) {
      unsetSticky();
    }
  }

  if (header) {
    var headerHeight = header.offsetHeight,
      headerYPos = header.getBoundingClientRect().y,
      triggerOffset = 60,
      triggerSticky = headerYPos + headerHeight - triggerOffset;

    if (window.scrollY > triggerSticky && !enabled) {
      setSticky();
    }
    document.addEventListener('scroll', onScroll);
    document.addEventListener('click', e => {
      if (!e.target.classList.contains('deep-link')) {
        return;
      }
      e.preventDefault();
      window.Jujucharms._scrollToHeader(e.target.attributes.href.value);
    });
  }
};

/**
  Scroll to the sticky header when present.
  On mobile/tablet(<1030px) size for example sticky header is not present.
  @param {String} location the element to scroll to
**/
window.Jujucharms._scrollToHeader = location => {
  // Setting hash twice to force the browser to jump
  // in particular when this is the same as the current hash.
  if (location !== '') {
    window.location.hash = 'something-which-does-not-exist';
    window.location.hash = location;
    var width = window.innerWidth;
    var scrolledY = window.scrollY;
    if (width > 1030 && scrolledY > 0) {
      window.scroll(0, scrolledY - 115);
    }

    // Repeat, because on page load we need to check the sticky header
    // after the initial jump (it's not active the first time)
    if (window.Jujucharms._stickyHeaderEnabled) {
      window.scroll(0, window.scrollY - 55);
    }
  }
};
