(function () {
  "use strict";

  var scriptEl = document.currentScript;
  var cfg = (scriptEl && scriptEl.dataset) || {};
  var BOT_USERNAME = cfg.bot; // required, e.g. "sytnie_ugodya_bot" (no @, no t.me/)
  var ACCENT = cfg.accent || "#8a4a2a";
  var LABEL = cfg.label || "Спросить в Telegram";

  if (!BOT_USERNAME) {
    console.error(
      "telegram-button.js: data-bot is required, e.g. " +
        '<script src="telegram-button.js" data-bot="your_bot_username" async></script>'
    );
    return;
  }

  var css =
    ".syu-tg-btn{position:fixed;right:20px;bottom:20px;z-index:999999;display:flex;" +
    "align-items:center;gap:10px;background:" + ACCENT + ";color:#fff;text-decoration:none;" +
    "font-family:-apple-system,'Segoe UI',Roboto,Arial,sans-serif;font-size:14.5px;font-weight:600;" +
    "padding:12px 18px 12px 14px;border-radius:999px;box-shadow:0 6px 20px rgba(0,0,0,.25);" +
    "transition:transform .15s ease;}" +
    ".syu-tg-btn:hover{transform:scale(1.04);}" +
    ".syu-tg-btn svg{width:24px;height:24px;flex-shrink:0;}" +
    "@media (max-width:480px){.syu-tg-btn{right:12px;bottom:12px;padding:11px 16px 11px 12px;font-size:13.5px;}}";

  var styleTag = document.createElement("style");
  styleTag.textContent = css;
  document.head.appendChild(styleTag);

  var link = document.createElement("a");
  link.className = "syu-tg-btn";
  link.href = "https://t.me/" + encodeURIComponent(BOT_USERNAME);
  link.target = "_blank";
  link.rel = "noopener noreferrer";
  link.setAttribute("aria-label", LABEL);
  link.innerHTML =
    '<svg viewBox="0 0 240 240" fill="none"><circle cx="120" cy="120" r="120" fill="#fff" fill-opacity="0"/>' +
    '<path fill="#fff" d="M177 62l-25 129c-2 8-7 10-14 6l-38-28-18 17c-2 2-4 4-8 4l3-40 73-66c3-3-1-4-5-2l-90 57-39-12c-8-3-9-8 2-12l153-59c7-2 13 2 6 12z"/></svg>' +
    "<span>" + LABEL + "</span>";

  document.body.appendChild(link);
})();
