/* =========================================================================
   analytics.js — Google Analytics 4 (gtag.js) loader for "Bottling the Sun"

   Why this file exists:
     Centralizes web analytics in ONE place so the Measurement ID lives in a
     single spot instead of being pasted into every page's <head>. Every page
     includes this one script; set your ID once, below.

   HOW TO TURN IT ON:
     1. In Google Analytics (the sanya.shopper@gmail.com account):
        Admin → Data streams → your web stream → copy the Measurement ID.
        It looks like  G-XXXXXXXXXX.
     2. Paste it into GA_MEASUREMENT_ID below, replacing the placeholder.
     3. Commit & push. GitHub Pages redeploys; data appears in GA Realtime
        within a minute or two.

   Privacy notes (this is the only third-party call on the whole site):
     - While the ID is left as the placeholder, this script does NOTHING and
       makes no external request — the site stays fully self-contained.
     - It counts ALL visitors, including the site owner ("Do Not Track" is not
       honored, by choice). See the note by the config line to change that.
     - GA4 does not log full IP addresses; IP anonymization is the default.

   Last updated: 2026-07-23 (Pacific)
   ========================================================================= */
(function () {
  "use strict";

  /* ---- set your GA4 Measurement ID here (looks like G-XXXXXXXXXX) ---- */
  var GA_MEASUREMENT_ID = "G-10E9K3M38P";

  // Not configured yet → stay off, make no external request.
  if (!GA_MEASUREMENT_ID || GA_MEASUREMENT_ID === "G-XXXXXXXXXX") { return; }

  // Note: "Do Not Track" is intentionally NOT honored — every visitor is
  // counted, including the site owner. To go back to skipping DNT visitors,
  // re-add a guard here that returns early when navigator.doNotTrack === "1".

  // Load the official gtag.js library.
  var s = document.createElement("script");
  s.async = true;
  s.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(GA_MEASUREMENT_ID);
  document.head.appendChild(s);

  // Standard GA4 bootstrap.
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = gtag;
  gtag("js", new Date());
  gtag("config", GA_MEASUREMENT_ID);
})();
