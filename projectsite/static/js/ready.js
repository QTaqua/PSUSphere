(function () {
  const menuButton = document.querySelector('[data-menu-toggle]');
  const sidebar = document.querySelector('#sidebar');

  if (menuButton && sidebar) {
    menuButton.addEventListener('click', function () {
      const isOpen = sidebar.classList.toggle('is-open');
      menuButton.setAttribute('aria-expanded', String(isOpen));
    });
  }

  const tabs = document.querySelectorAll('[data-auth-tab]');
  tabs.forEach(function (tab) {
    tab.addEventListener('click', function () {
      tabs.forEach(function (item) {
        const panel = document.getElementById(item.dataset.authTab);
        const active = item === tab;
        item.classList.toggle('is-active', active);
        item.setAttribute('aria-selected', String(active));
        if (panel) {
          panel.classList.toggle('is-active', active);
          panel.hidden = !active;
        }
      });
    });
  });
})();
