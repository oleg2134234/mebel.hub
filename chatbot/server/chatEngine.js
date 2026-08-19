"use strict";

const Anthropic = require("@anthropic-ai/sdk");
const { SYSTEM_PROMPT, SUBMIT_LEAD_TOOL } = require("./knowledge");
const { notifyLead } = require("./leads");
const db = require("./db");

const MODEL = process.env.CLAUDE_MODEL || "claude-opus-5";

const client = new Anthropic(); // reads ANTHROPIC_API_KEY from env

/**
 * Runs one chat turn against Claude, handling at most one submit_lead tool
 * call in the same round trip. Shared by the website widget's HTTP endpoint
 * and the Telegram bot, so both channels answer with identical behavior.
 *
 * @param {string} userMessage
 * @param {{role: "user"|"assistant", content: string}[]} history
 */
async function runChatTurn(userMessage, history) {
  const messages = [...history, { role: "user", content: userMessage }];

  let response = await client.messages.create({
    model: MODEL,
    max_tokens: 1024,
    system: SYSTEM_PROMPT,
    output_config: { effort: "medium" },
    tools: [SUBMIT_LEAD_TOOL],
    messages,
  });

  let leadCaptured = null;

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

  return {
    reply: replyText || "Извините, не получилось сформировать ответ. Попробуйте ещё раз.",
    leadCaptured: Boolean(leadCaptured),
  };
}

module.exports = { runChatTurn };
