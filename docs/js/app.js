(function () {
  var root = document.documentElement;
  var btn = document.getElementById("lang");
  var titles = { en: "Coffee Guy – Menu", sv: "Coffee Guy – Meny" };
  function sync() {
    document.title = titles[root.lang];
    btn.textContent = root.lang === "sv" ? "English" : "Svenska";
  }
  btn.hidden = false;
  btn.addEventListener("click", function () {
    root.lang = root.lang === "sv" ? "en" : "sv";
    sync();
  });
  sync();
})();

// Set FEEDBACK_PUBLIC to false to hide the feedback form from visitors (add ?feedback to the address to preview it).
// FEEDBACK_URL is the private form endpoint that receives the messages (JSON POST, e.g. a Formspree form URL).
// If FEEDBACK_URL changes host, update connect-src in the Content-Security-Policy meta tag in index.html.
(function () {
  var FEEDBACK_PUBLIC = true;
  var FEEDBACK_URL = "https://formspree.io/f/mnppjjwe";
  if (!FEEDBACK_PUBLIC && !new URLSearchParams(location.search).has("feedback")) return;
  document.getElementById("feedback").hidden = false;
  var form = document.getElementById("fb");
  var send = document.getElementById("fb-send");
  var status = document.getElementById("fb-status");
  var text = {
    en: { empty: "Please choose a rating or write a message.", preview: "Preview only: feedback is not connected yet.", sending: "Sending…", error: "Something went wrong. Please try again.", thanks: "Thank you for your feedback!" },
    sv: { empty: "Välj ett betyg eller skriv ett meddelande.", preview: "Endast förhandsvisning: feedback är inte kopplad ännu.", sending: "Skickar…", error: "Något gick fel. Försök igen.", thanks: "Tack för din feedback!" }
  };
  function say(key) { status.textContent = text[document.documentElement.lang][key]; }
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var data = new FormData(form);
    if (data.get("_gotcha")) return;
    var rating = data.get("rating");
    var message = (data.get("message") || "").trim();
    if (!rating && !message) return say("empty");
    if (!FEEDBACK_URL) return say("preview");
    send.disabled = true;
    say("sending");
    fetch(FEEDBACK_URL, {
      method: "POST",
      headers: { "Accept": "application/json", "Content-Type": "application/json" },
      body: JSON.stringify({ rating: rating, message: message, name: (data.get("name") || "").trim() })
    }).then(function (r) {
      if (!r.ok) throw new Error(r.status);
      form.reset();
      say("thanks");
    }).catch(function () {
      send.disabled = false;
      say("error");
    });
  });
})();
