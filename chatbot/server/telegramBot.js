"use strict";

const { runChatTurn } = require("./chatEngine");

const MAX_HISTORY_MESSAGES = 24;
const MAX_MESSAGE_LENGTH = 4000;
const POLL_TIMEOUT_SEC = 25;
const RETRY_DELAY_MS = 3000;

const GREETING =
  "Здравствуйте! Я виртуальный консультант «Сытных угодий». Расскажу о наших мясных " +
  "консервах и готовых блюдах, помогу подобрать ассортимент — для себя или для бизнеса. " +
  "Чем могу помочь?";

// In-memory per-chat conversation history. Resets on process restart — fine
// for a test/demo bot; move to a persistent store if that matters later.
const conversations = new Map();

function getHistory(chatId) {
  return conversations.get(chatId) || [];
}

function pushHistory(chatId, role, content) {
  const history = getHistory(chatId);
  history.push({ role, content });
  conversations.set(chatId, history.slice(-MAX_HISTORY_MESSAGES));
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function callTelegram(token, method, body) {
  const resp = await fetch(`https://api.telegram.org/bot${token}/${method}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!resp.ok) {
    console.error(`telegramBot: ${method} failed`, resp.status, await resp.text());
    return null;
  }
  return resp.json();
}

async function sendMessage(token, chatId, text) {
  await callTelegram(token, "sendMessage", { chat_id: chatId, text });
}

async function handleMessage(token, message) {
  const chatId = message.chat.id;
  const text = String(message.text || "").slice(0, MAX_MESSAGE_LENGTH).trim();
  if (!text) return;

  if (text === "/start") {
    conversations.delete(chatId);
    await sendMessage(token, chatId, GREETING);
    return;
  }

  try {
    const history = getHistory(chatId);
    const { reply } = await runChatTurn(text, history);
    pushHistory(chatId, "user", text);
    pushHistory(chatId, "assistant", reply);
    await sendMessage(token, chatId, reply);
  } catch (err) {
    console.error("telegramBot: chat turn failed for chat", chatId, err);
    await sendMessage(token, chatId, "Извините, произошла ошибка. Попробуйте ещё раз чуть позже.");
  }
}

async function pollLoop(token) {
  let offset = 0;
  console.log("telegramBot: customer chat long-polling started");
  for (;;) {
    let data;
    try {
      const resp = await fetch(
        `https://api.telegram.org/bot${token}/getUpdates?timeout=${POLL_TIMEOUT_SEC}&offset=${offset}`
      );
      if (!resp.ok) {
        console.error("telegramBot: getUpdates failed", resp.status);
        await sleep(RETRY_DELAY_MS);
        continue;
      }
      data = await resp.json();
    } catch (err) {
      console.error("telegramBot: poll error", err);
      await sleep(RETRY_DELAY_MS);
      continue;
    }

    for (const update of data.result || []) {
      offset = update.update_id + 1;
      if (update.message) {
        // Fire-and-forget so one slow reply doesn't stall polling for others.
        handleMessage(token, update.message).catch((err) =>
          console.error("telegramBot: unhandled error", err)
        );
      }
    }
  }
}

/**
 * Starts the customer-facing Telegram bot (long polling) if enabled. Uses
 * the same TELEGRAM_BOT_TOKEN as the manager lead notifications in leads.js
 * — one bot serves both roles. Opt-in via TELEGRAM_CUSTOMER_BOT=true so an
 * existing notifications-only setup doesn't suddenly start answering
 * strangers on Telegram.
 */
function startTelegramBot() {
  const token = process.env.TELEGRAM_BOT_TOKEN;
  const enabled = process.env.TELEGRAM_CUSTOMER_BOT === "true";
  if (!enabled) return;
  if (!token) {
    console.warn("telegramBot: TELEGRAM_CUSTOMER_BOT=true but TELEGRAM_BOT_TOKEN is not set — skipping");
    return;
  }
  pollLoop(token).catch((err) => console.error("telegramBot: poll loop crashed", err));
}

module.exports = { startTelegramBot };
