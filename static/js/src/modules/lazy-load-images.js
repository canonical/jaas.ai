import LazyLoad from 'vanilla-lazyload';

// Lazy loading images
const lazyLoadOptions = {
  elements_selector: '.lazy',
  to_webp: true
};

const createLazyLoadInstance = () => {
  return new LazyLoad(lazyLoadOptions);
};

export default () => {
  document.addEventListener('DOMContentLoaded', createLazyLoadInstance);
};
