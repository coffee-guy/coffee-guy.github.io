// ?lang=sv|en wins, otherwise the browser language.
(function () {
  var q = new URLSearchParams(location.search).get("lang");
  var l = (q || navigator.language || "en").slice(0, 2).toLowerCase();
  document.documentElement.lang = l === "sv" ? "sv" : "en";
})();
