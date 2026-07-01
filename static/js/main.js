/* ==========================================================
   FitFusion AI - main.js
   --------------------------------------------------------
   Purpose:
     Global, page-agnostic frontend behavior only.
     - Mobile navbar toggle (UI state only)
     - A single init entry point for future global scripts
       (e.g. theme toggle, once it's built)

   IMPORTANT:
     No business logic, no API calls, and no form handling
     belong in this file. Those will live in validation.js,
     dashboard.js, and api.js in later phases.
   ========================================================== */

document.addEventListener('DOMContentLoaded', function () {
  initNavbarToggle();
  initApp();
});

/**
 * initNavbarToggle
 * ----------------------------------------------------------
 * Wires up the hamburger button so it shows/hides the nav
 * links list on small screens. Purely a UI state toggle --
 * adds/removes a class and updates the aria-expanded
 * attribute for accessibility. No navigation logic here.
 */
function initNavbarToggle() {
  const toggleButton = document.getElementById('navbarToggle');
  const navLinks = document.getElementById('navbarLinks');

  if (!toggleButton || !navLinks) {
    return; // Elements not present on this page -- nothing to do.
  }

  toggleButton.addEventListener('click', function () {
    const isOpen = navLinks.classList.toggle('is-open');
    toggleButton.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
  });
}

/**
 * initApp
 * ----------------------------------------------------------
 * Placeholder entry point for future global initialization
 * (e.g. dark/light theme toggle, reading saved preferences).
 * Intentionally left minimal for this phase.
 */
function initApp() {
  // Future: read saved theme preference and apply data-theme
  // attribute on <html>. Not implemented yet -- structure
  // only, as per this phase's requirements.
}