window.addEventListener('DOMContentLoaded', () => {
  const tabs = document.querySelectorAll('[role="tab"]');

  // Add a click event handler to each tab
  tabs.forEach(tab => {
    tab.addEventListener('click', changeTabs);
  });
});

function changeTabs(e) {
  const target = e.target.closest('[role="tab"]');
  const tabs = document.querySelectorAll('[role="tab"]');
  const panels = document.querySelectorAll('[role="tabpanel"]');

  // Remove all current selected tabs
  tabs.forEach(tab => {
    tab.setAttribute('aria-selected', false);
  });

  // Set this tab as selected
  target.setAttribute('aria-selected', true);

  // Hide all tab panels
  panels.forEach(panel => panel.setAttribute('hidden', true));

  // Show the selected panel
  document.querySelector(`#${target.getAttribute('aria-controls')}`).removeAttribute('hidden');
}
