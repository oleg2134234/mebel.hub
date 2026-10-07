"use strict";

const CHANNEL_LABELS = { retail: "розница", wholesale: "опт" };
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function formatLead(lead) {
  const lines = [
    "Новая заявка с сайта sytnie-ugodya.ru",
    `Имя: ${lead.name || "—"}`,
    `Контакт: ${lead.contact || "—"}`,
    `Тип клиента: ${CHANNEL_LABELS[lead.channel] || lead.channel || "—"}`,
    `Потребность: ${lead.need || "—"}`,
  ];
  if (lead.volume) lines.push(`Объём/периодичность: ${lead.volume}`);
  return lines.join("\n");
}

async function sendTelegram(text) {
  const token = process.env.TELEGRAM_BOT_TOKEN;
  const chatId = process.env.TELEGRAM_CHAT_ID;
  if (!token || !chatId) return false;

  const url = `https://api.telegram.org/bot${token}/sendMessage`;
  const resp = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ chat_id: chatId, text }),
  });
  if (!resp.ok) {
    console.error("Telegram notify failed:", resp.status, await resp.text());
    return false;
  }
  return true;
}

let cachedTransporter = null;
function getTransporter() {
  if (cachedTransporter) return cachedTransporter;
  const host = process.env.SMTP_HOST;
  if (!host) return null;

  const nodemailer = require("nodemailer");
  cachedTransporter = nodemailer.createTransport({
    host,
    port: Number(process.env.SMTP_PORT || 587),
    secure: process.env.SMTP_SECURE === "true",
    auth: process.env.SMTP_USER
      ? { user: process.env.SMTP_USER, pass: process.env.SMTP_PASS }
      : undefined,
  });
  return cachedTransporter;
}

/** Sends an email to an arbitrary recipient. Returns false if SMTP isn't configured. */
async function sendEmail({ to, subject, text }) {
  const transporter = getTransporter();
  if (!transporter) return false;
  await transporter.sendMail({
    from: process.env.SMTP_FROM || process.env.SMTP_USER,
    to,
    subject,
    text,
  });
  return true;
}

/**
 * Notifies the business (not the customer) that a new lead came in, via every
 * configured channel: Telegram (TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID) and/or
 * email (SMTP_* + LEADS_EMAIL_TO). Silently no-ops per channel if unconfigured.
 */
async function notifyLead(lead) {
  const text = formatLead(lead);
  const leadsEmailTo = process.env.LEADS_EMAIL_TO;

  const results = await Promise.allSettled([
    sendTelegram(text),
    leadsEmailTo
      ? sendEmail({ to: leadsEmailTo, subject: "Новая заявка — Сытные угодья", text })
      : Promise.resolve(false),
  ]);

  results.forEach((r) => {
    if (r.status === "rejected") console.error("Lead notification error:", r.reason);
  });
}

module.exports = { notifyLead, sendEmail, EMAIL_RE };
