(function () {
  "use strict";

  var scriptEl = document.currentScript;
  var cfg = (scriptEl && scriptEl.dataset) || {};
  var API_URL = cfg.apiUrl || "/api/chat";
  var ACCENT = cfg.accent || "#8a4a2a";
  var TITLE = cfg.title || "Сытные угодья";
  var SUBTITLE = cfg.subtitle || "Онлайн-консультант";
  var GREETING =
    cfg.greeting ||
    "Здравствуйте! Я виртуальный консультант «Сытных угодий». Расскажу о наших мясных консервах и готовых блюдах, помогу подобрать ассортимент — для себя или для бизнеса. Чем могу помочь?";
  var STORAGE_KEY = "syu_chat_history_v1";
  var MAX_STORED_MESSAGES = 40;

  var css =
    ".syu-launcher{position:fixed;right:20px;bottom:20px;width:60px;height:60px;border-radius:50%;" +
    "background:" + ACCENT + ";color:#fff;border:none;box-shadow:0 6px 20px rgba(0,0,0,.25);cursor:pointer;" +
    "z-index:999999;display:flex;align-items:center;justify-content:center;transition:transform .15s ease;}" +
    ".syu-launcher:hover{transform:scale(1.06);}" +
    ".syu-launcher svg{width:28px;height:28px;fill:#fff;}" +
    ".syu-panel{position:fixed;right:20px;bottom:92px;width:360px;max-width:calc(100vw - 24px);" +
    "height:520px;max-height:calc(100vh - 120px);background:#fff;border-radius:16px;overflow:hidden;" +
    "box-shadow:0 12px 40px rgba(0,0,0,.3);display:none;flex-direction:column;z-index:999999;" +
    "font-family:-apple-system,'Segoe UI',Roboto,Arial,sans-serif;}" +
    ".syu-panel.syu-open{display:flex;}" +
    ".syu-header{background:" + ACCENT + ";color:#fff;padding:14px 16px;display:flex;align-items:center;gap:10px;}" +
    ".syu-header-text{flex:1;}" +
    ".syu-header-title{font-weight:600;font-size:15px;line-height:1.2;}" +
    ".syu-header-sub{font-size:12px;opacity:.85;}" +
    ".syu-close{background:transparent;border:none;color:#fff;font-size:20px;cursor:pointer;line-height:1;padding:4px;}" +
    ".syu-messages{flex:1;overflow-y:auto;padding:14px;background:#faf6f0;display:flex;flex-direction:column;gap:10px;}" +
    ".syu-msg{max-width:82%;padding:9px 12px;border-radius:14px;font-size:13.5px;line-height:1.45;white-space:pre-wrap;word-wrap:break-word;}" +
    ".syu-msg.bot{align-self:flex-start;background:#fff;border:1px solid #eee0cf;color:#2b2418;border-bottom-left-radius:4px;}" +
    ".syu-msg.user{align-self:flex-end;background:" + ACCENT + ";color:#fff;border-bottom-right-radius:4px;}" +
    ".syu-msg.error{align-self:flex-start;background:#fdeceb;border:1px solid #f3c6c2;color:#7a2a20;}" +
    ".syu-typing{align-self:flex-start;display:flex;gap:4px;padding:10px 12px;}" +
    ".syu-typing span{width:6px;height:6px;border-radius:50%;background:#b9ac95;animation:syu-blink 1.2s infinite ease-in-out;}" +
    ".syu-typing span:nth-child(2){animation-delay:.2s;}" +
    ".syu-typing span:nth-child(3){animation-delay:.4s;}" +
    "@keyframes syu-blink{0%,80%,100%{opacity:.3;}40%{opacity:1;}}" +
    ".syu-inputbar{display:flex;gap:8px;padding:10px;border-top:1px solid #eee0cf;background:#fff;}" +
    ".syu-input{flex:1;border:1px solid #ddd0ba;border-radius:20px;padding:9px 14px;font-size:13.5px;outline:none;resize:none;font-family:inherit;max-height:80px;}" +
    ".syu-input:focus{border-color:" + ACCENT + ";}" +
    ".syu-send{background:" + ACCENT + ";border:none;color:#fff;width:36px;height:36px;border-radius:50%;cursor:pointer;flex-shrink:0;display:flex;align-items:center;justify-content:center;}" +
    ".syu-send:disabled{opacity:.5;cursor:not-allowed;}" +
    ".syu-send svg{width:16px;height:16px;fill:#fff;}" +
    "@media (max-width:480px){.syu-panel{right:8px;bottom:80px;width:calc(100vw - 16px);height:calc(100vh - 100px);}}";

  var styleTag = document.createElement("style");
  styleTag.textContent = css;
  document.head.appendChild(styleTag);

  var launcher = document.createElement("button");
  launcher.className = "syu-launcher";
  launcher.setAttribute("aria-label", "Открыть чат с консультантом");
  launcher.innerHTML =
    '<svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.03 2 11c0 2.39 1.06 4.55 2.8 6.14L4 22l5.15-1.55C10.05 20.8 11 21 12 21c5.52 0 10-4.03 10-9s-4.48-10-10-10z"/></svg>';

  var panel = document.createElement("div");
  panel.className = "syu-panel";
  panel.innerHTML =
    '<div class="syu-header">' +
    '<div class="syu-header-text">' +
    '<div class="syu-header-title">' + escapeHtml(TITLE) + '</div>' +
    '<div class="syu-header-sub">' + escapeHtml(SUBTITLE) + '</div>' +
    '</div>' +
    '<button class="syu-close" aria-label="Закрыть">×</button>' +
    '</div>' +
    '<div class="syu-messages" id="syu-messages"></div>' +
    '<div class="syu-inputbar">' +
    '<textarea class="syu-input" id="syu-input" rows="1" placeholder="Напишите сообщение…"></textarea>' +
    '<button class="syu-send" id="syu-send" aria-label="Отправить">' +
    '<svg viewBox="0 0 24 24"><path d="M2 21l21-9L2 3v7l15 2-15 2z"/></svg>' +
    "</button>" +
    "</div>";

  document.body.appendChild(launcher);
  document.body.appendChild(panel);

  var messagesEl = panel.querySelector("#syu-messages");
  var inputEl = panel.querySelector("#syu-input");
  var sendBtn = panel.querySelector("#syu-send");
  var closeBtn = panel.querySelector(".syu-close");

  var history = loadHistory();
  var isSending = false;

  function escapeHtml(str) {
    return String(str == null ? "" : str).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function loadHistory() {
    try {
      var raw = sessionStorage.getItem(STORAGE_KEY);
      if (!raw) return [];
      var parsed = JSON.parse(raw);
      return Array.isArray(parsed) ? parsed : [];
    } catch (e) {
      return [];
    }
  }

  function saveHistory() {
    try {
      sessionStorage.setItem(
        STORAGE_KEY,
        JSON.stringify(history.slice(-MAX_STORED_MESSAGES))
      );
    } catch (e) {
      /* storage unavailable — conversation just won't persist across reloads */
    }
  }

  function renderMessage(role, text) {
    var div = document.createElement("div");
    div.className = "syu-msg " + (role === "user" ? "user" : role === "error" ? "error" : "bot");
    div.textContent = text;
    messagesEl.appendChild(div);
    messagesEl.scrollTop = messagesEl.scrollHeight;
    return div;
  }

  function renderTyping() {
    var div = document.createElement("div");
    div.className = "syu-typing";
    div.id = "syu-typing-indicator";
    div.innerHTML = "<span></span><span></span><span></span>";
    messagesEl.appendChild(div);
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  function removeTyping() {
    var el = document.getElementById("syu-typing-indicator");
    if (el) el.remove();
  }

  function openPanel() {
    panel.classList.add("syu-open");
    if (messagesEl.children.length === 0) {
      if (history.length > 0) {
        history.forEach(function (m) {
          renderMessage(m.role === "user" ? "user" : "bot", m.content);
        });
      } else {
        renderMessage("bot", GREETING);
      }
    }
    inputEl.focus();
  }

  function togglePanel() {
    if (panel.classList.contains("syu-open")) {
      panel.classList.remove("syu-open");
    } else {
      openPanel();
    }
  }

  launcher.addEventListener("click", togglePanel);
  closeBtn.addEventListener("click", function () {
    panel.classList.remove("syu-open");
  });

  inputEl.addEventListener("input", function () {
    inputEl.style.height = "auto";
    inputEl.style.height = Math.min(inputEl.scrollHeight, 80) + "px";
  });

  inputEl.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  });

  sendBtn.addEventListener("click", send);

  function send() {
    var text = inputEl.value.trim();
    if (!text || isSending) return;

    renderMessage("user", text);
    inputEl.value = "";
    inputEl.style.height = "auto";
    history.push({ role: "user", content: text });
    saveHistory();

    isSending = true;
    sendBtn.disabled = true;
    renderTyping();

    fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: text,
        history: history.slice(0, -1), // backend appends the current message itself
      }),
    })
      .then(function (resp) {
        if (!resp.ok) throw new Error("HTTP " + resp.status);
        return resp.json();
      })
      .then(function (data) {
        removeTyping();
        var reply = data && data.reply ? data.reply : "Извините, не получилось ответить. Попробуйте ещё раз.";
        renderMessage("bot", reply);
        history.push({ role: "assistant", content: reply });
        saveHistory();
      })
      .catch(function () {
        removeTyping();
        renderMessage(
          "error",
          "Не получилось отправить сообщение. Попробуйте ещё раз или свяжитесь с нами напрямую."
        );
      })
      .finally(function () {
        isSending = false;
        sendBtn.disabled = false;
      });
  }
})();
