/* =========================================================================
   site.js — tiny progressive-enhancement helpers for "Bottling the Sun"
   Why this file exists:
     The site is static HTML; this adds only what plain HTML can't do on its
     own — a mobile nav toggle, marking the current page's nav link, and
     stamping the current year in the footer. No frameworks, no dependencies,
     no network calls. If JS is disabled the site still reads fine.
   How to use:
     <script src="js/site.js" defer></script>  (adjust path in subfolders)
     Nav markup:
        <button class="nav-toggle" aria-label="Menu" aria-expanded="false">☰</button>
        <nav class="nav-links" id="nav">... links ...</nav>
   Last updated: 2026-07-23 (Pacific)
   ========================================================================= */
(function () {
  "use strict";

  // --- mobile nav toggle ---
  var toggle = document.querySelector(".nav-toggle");
  var links = document.getElementById("nav");
  if (toggle && links) {
    toggle.addEventListener("click", function () {
      var open = links.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    // close the menu after tapping a link (mobile)
    links.addEventListener("click", function (e) {
      if (e.target.tagName === "A") {
        links.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  // --- mark the active nav link based on the current file name ---
  var here = location.pathname.split("/").pop() || "index.html";
  var navA = document.querySelectorAll(".nav-links a");
  for (var i = 0; i < navA.length; i++) {
    var target = navA[i].getAttribute("href");
    if (target === here || (here === "" && target === "index.html")) {
      navA[i].classList.add("active");
    }
  }

  // --- stamp current year in any element with [data-year] ---
  var y = String(new Date().getFullYear());
  var slots = document.querySelectorAll("[data-year]");
  for (var j = 0; j < slots.length; j++) { slots[j].textContent = y; }
})();
