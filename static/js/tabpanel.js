let timer;

window.addEventListener('DOMContentLoaded', () => {
  const tabs = document.querySelectorAll('[role="tab"]');

  // Add a click event handler to each tab
  tabs.forEach(tab => {
    tab.addEventListener('click', function(e) {
      const target = e.target.closest('[role="tab"]');
      changeTabs(target);
    });
  });

  // Select the inital active tab
  const initalActiveTab = document.querySelector('.p-hero-tab__item[aria-selected="true"]');
  if (initalActiveTab) {
    playTab(initalActiveTab);
  }
});

function changeTabs(target) {
  const tabs = document.querySelectorAll('[role="tab"]');
  const panels = document.querySelectorAll('[role="tabpanel"]');
  clearInterval(timer);

  // Remove all current selected tabs
  tabs.forEach(tab => {
    draw(0, tab.querySelector('.before'));
    tab.setAttribute('aria-selected', false);
  });

  // Set this tab as selected
  target.setAttribute('aria-selected', true);

  // Hide all tab panels
  panels.forEach(panel => panel.classList.remove('u-animate--reveal'));

  // Show the selected panel
  document
    .querySelector(`#${target.getAttribute('aria-controls')}`)
    .classList.add('u-animate--reveal');

  playTab(target);
}

function playTab(tab) {
  let start = Date.now();
  let duration = 10000;
  let tabIndicator = tab.querySelector('.before');
  if (tabIndicator) {
    timer = setInterval(function() {
      let timePassed = Date.now() - start;
      if (timePassed >= duration) {
        clearInterval(timer);
        triggerNextTab(tab);
        return;
      }
      draw(timePassed / (duration / 100), tabIndicator);
    }, 20);
  }
}

function draw(timePassed, tab) {
  tab.style.width = timePassed + '%';
}

function triggerNextTab(tab) {
  let nextTab = tab.nextElementSibling;
  if (!nextTab) {
    nextTab = document.querySelectorAll('.p-hero-tab__item')[0];
  }
  changeTabs(nextTab);
}
