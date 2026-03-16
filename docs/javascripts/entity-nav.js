// Entity Navigation Dropdowns — shared across all 6 documentation sites (ADR-024)
document.addEventListener("DOMContentLoaded", function () {
  var dropdowns = document.querySelectorAll(".entity-dropdown");
  if (!dropdowns.length) return;

  dropdowns.forEach(function (dropdown) {
    var toggle = dropdown.querySelector(".entity-dropdown-toggle");

    toggle.addEventListener("click", function (e) {
      e.stopPropagation();
      var isOpen = dropdown.hasAttribute("data-open");

      // Close all dropdowns first
      dropdowns.forEach(function (d) {
        d.removeAttribute("data-open");
        d.querySelector(".entity-dropdown-toggle").setAttribute("aria-expanded", "false");
      });

      // Toggle the clicked one
      if (!isOpen) {
        dropdown.setAttribute("data-open", "");
        toggle.setAttribute("aria-expanded", "true");
      }
    });
  });

  // Close on click outside
  document.addEventListener("click", function () {
    dropdowns.forEach(function (d) {
      d.removeAttribute("data-open");
      d.querySelector(".entity-dropdown-toggle").setAttribute("aria-expanded", "false");
    });
  });

  // Close on Escape
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      dropdowns.forEach(function (d) {
        d.removeAttribute("data-open");
        d.querySelector(".entity-dropdown-toggle").setAttribute("aria-expanded", "false");
      });
    }
  });
});
