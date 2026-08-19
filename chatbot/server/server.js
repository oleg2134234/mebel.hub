"use strict";

require("dotenv").config();
const path = require("path");
const express = require("express");
const cors = require("cors");
const { runChatTurn } = require("./chatEngine");
const { startTelegramBot } = require("./telegramBot");
const adminAuth = require("./adminAuth");
const adminRoutes = require("./adminRoutes");

const PORT = process.env.PORT || 3001;
const MAX_HISTORY_MESSAGES = 24; // caps token spend on long conversations
const MAX_MESSAGE_LENGTH = 4000;

const allowedOrigins = (process.env.ALLOWED_ORIGINS || "")
  .split(",")
  .map((o) => o.trim())
  .filter(Boolean);

const app = express();
app.use(express.json({ limit: "200kb" }));
app.use(
  cors({
    origin: allowedOrigins.length > 0 ? allowedOrigins : true,
    methods: ["POST", "GET", "OPTIONS"],
  })
);

app.get("/api/health", (_req, res) => {
  res.json({ ok: true });
});

// Serves the embeddable scripts from their single source of truth
// (chatbot/widget/) so sites can point a <script> tag straight at this
// backend instead of hosting a second copy of the files.
app.get("/widget.js", (_req, res) => {
  res.type("application/javascript");
  res.sendFile(path.join(__dirname, "..", "widget", "widget.js"));
});
app.get("/telegram-button.js", (_req, res) => {
  res.type("application/javascript");
  res.sendFile(path.join(__dirname, "..", "widget", "telegram-button.js"));
});

// Admin panel — lead list, status updates, manual broadcast. Gated by HTTP
// Basic Auth (ADMIN_USER/ADMIN_PASS); returns 503 until those are set.
app.use("/api/admin", adminAuth, adminRoutes);
app.use("/admin", adminAuth, express.static(path.join(__dirname, "public/admin")));

function sanitizeHistory(rawHistory) {
  if (!Array.isArray(rawHistory)) return [];
  return rawHistory
    .filter(
      (m) =>
        m &&
        (m.role === "user" || m.role === "assistant") &&
        typeof m.content === "string" &&
        m.content.trim().length > 0
    )
    .slice(-MAX_HISTORY_MESSAGES)
    .map((m) => ({
      role: m.role,
      content: m.content.slice(0, MAX_MESSAGE_LENGTH),
    }));
}

app.post("/api/chat", async (req, res) => {
  try {
    const userMessage = String(req.body?.message ?? "").slice(0, MAX_MESSAGE_LENGTH).trim();
    if (!userMessage) {
      return res.status(400).json({ error: "message is required" });
    }

    const history = sanitizeHistory(req.body?.history);
    const { reply, leadCaptured } = await runChatTurn(userMessage, history);
    res.json({ reply, leadCaptured });
  } catch (err) {
    console.error("chat error:", err);
    res.status(502).json({ error: "chat_failed" });
  }
});

app.listen(PORT, () => {
  console.log(`Sales chatbot backend listening on :${PORT}`);
  startTelegramBot();
});
