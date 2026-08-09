"use strict";

require("dotenv").config();
const path = require("path");
const express = require("express");
const cors = require("cors");
const Anthropic = require("@anthropic-ai/sdk");
const { SYSTEM_PROMPT, SUBMIT_LEAD_TOOL } = require("./knowledge");
const { notifyLead } = require("./leads");
const db = require("./db");
const adminAuth = require("./adminAuth");
const adminRoutes = require("./adminRoutes");

const PORT = process.env.PORT || 3001;
const MODEL = process.env.CLAUDE_MODEL || "claude-opus-5";
const MAX_HISTORY_MESSAGES = 24; // caps token spend on long conversations
const MAX_MESSAGE_LENGTH = 4000;

const allowedOrigins = (process.env.ALLOWED_ORIGINS || "")
  .split(",")
  .map((o) => o.trim())
  .filter(Boolean);

const client = new Anthropic(); // reads ANTHROPIC_API_KEY from env

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

    const messages = [
      ...sanitizeHistory(req.body?.history),
      { role: "user", content: userMessage },
    ];

    // First turn: Claude may answer directly, or ask to call submit_lead.
    let response = await client.messages.create({
      model: MODEL,
      max_tokens: 1024,
      system: SYSTEM_PROMPT,
      output_config: { effort: "medium" },
      tools: [SUBMIT_LEAD_TOOL],
      messages,
    });

    let leadCaptured = null;

    // Handle at most one round of tool use per request — the bot only ever
    // calls one tool (submit_lead) at most once per turn.
    if (response.stop_reason === "tool_use") {
      const toolUseBlock = response.content.find((b) => b.type === "tool_use");

      if (toolUseBlock && toolUseBlock.name === "submit_lead") {
        leadCaptured = db.addLead(toolUseBlock.input);
        await notifyLead(leadCaptured);

        messages.push({ role: "assistant", content: response.content });
        messages.push({
          role: "user",
          content: [
            {
              type: "tool_result",
              tool_use_id: toolUseBlock.id,
              content: "Заявка сохранена и передана менеджеру.",
            },
          ],
        });

        // Second turn: let Claude produce the user-facing confirmation text.
        response = await client.messages.create({
          model: MODEL,
          max_tokens: 512,
          system: SYSTEM_PROMPT,
          output_config: { effort: "low" },
          tools: [SUBMIT_LEAD_TOOL],
          messages,
        });
      }
    }

    const replyText = response.content
      .filter((b) => b.type === "text")
      .map((b) => b.text)
      .join("\n")
      .trim();

    res.json({
      reply: replyText || "Извините, не получилось сформировать ответ. Попробуйте ещё раз.",
      leadCaptured: Boolean(leadCaptured),
    });
  } catch (err) {
    console.error("chat error:", err);
    res.status(502).json({ error: "chat_failed" });
  }
});

app.listen(PORT, () => {
  console.log(`Sales chatbot backend listening on :${PORT} (model: ${MODEL})`);
});
