"use strict";

const express = require("express");
const db = require("./db");
const { sendEmail, EMAIL_RE } = require("./leads");

const router = express.Router();

router.get("/leads", (req, res) => {
  const { status, channel } = req.query;
  res.json({ leads: db.listLeads({ status, channel }) });
});

router.patch("/leads/:id", (req, res) => {
  const { status } = req.body || {};
  if (!db.VALID_STATUSES.includes(status)) {
    return res.status(400).json({ error: `status must be one of: ${db.VALID_STATUSES.join(", ")}` });
  }
  const lead = db.updateLeadStatus(req.params.id, status);
  if (!lead) return res.status(404).json({ error: "lead_not_found" });
  res.json({ lead });
});

// Manual broadcast to selected leads. Only leads whose stored contact is an
// email address can be reached automatically — phone/WhatsApp/Telegram
// contacts have no configured automated channel here, so they're reported as
// skipped for manual follow-up instead of silently dropped.
router.post("/broadcast", async (req, res) => {
  const { leadIds, subject, message } = req.body || {};
  if (!Array.isArray(leadIds) || leadIds.length === 0) {
    return res.status(400).json({ error: "leadIds must be a non-empty array" });
  }
  if (!subject || !message) {
    return res.status(400).json({ error: "subject and message are required" });
  }

  const leads = db.getLeadsByIds(leadIds);
  const results = [];

  for (const lead of leads) {
    if (!EMAIL_RE.test(lead.contact)) {
      results.push({ id: lead.id, contact: lead.contact, status: "skipped_not_email" });
      continue;
    }
    try {
      const sent = await sendEmail({ to: lead.contact, subject, text: message });
      results.push({
        id: lead.id,
        contact: lead.contact,
        status: sent ? "sent" : "skipped_smtp_not_configured",
      });
    } catch (err) {
      console.error("Broadcast send failed for", lead.contact, err);
      results.push({ id: lead.id, contact: lead.contact, status: "failed" });
    }
  }

  res.json({ results });
});

module.exports = router;
