"use strict";

// Minimal file-backed lead store — good enough for a single-instance deployment.
// If lead volume grows enough to need concurrent writers or querying, swap this
// module for a real database; the rest of the app only depends on this file's
// exported functions.

const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const DATA_DIR = path.join(__dirname, "data");
const LEADS_FILE = path.join(DATA_DIR, "leads.json");

const VALID_STATUSES = ["new", "in_progress", "closed"];

function ensureStore() {
  if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });
  if (!fs.existsSync(LEADS_FILE)) fs.writeFileSync(LEADS_FILE, "[]", "utf8");
}

function readAll() {
  ensureStore();
  try {
    return JSON.parse(fs.readFileSync(LEADS_FILE, "utf8"));
  } catch (err) {
    console.error("Failed to read leads store, starting empty:", err);
    return [];
  }
}

function writeAll(leads) {
  fs.writeFileSync(LEADS_FILE, JSON.stringify(leads, null, 2), "utf8");
}

function addLead(input) {
  const leads = readAll();
  const lead = {
    id: crypto.randomUUID(),
    name: String(input.name || "").slice(0, 200),
    contact: String(input.contact || "").slice(0, 200),
    channel: input.channel === "wholesale" ? "wholesale" : "retail",
    need: String(input.need || "").slice(0, 1000),
    volume: String(input.volume || "").slice(0, 300),
    status: "new",
    createdAt: new Date().toISOString(),
  };
  leads.unshift(lead);
  writeAll(leads);
  return lead;
}

function listLeads({ status, channel } = {}) {
  return readAll()
    .filter((l) => !status || l.status === status)
    .filter((l) => !channel || l.channel === channel);
}

function getLeadsByIds(ids) {
  const set = new Set(ids);
  return readAll().filter((l) => set.has(l.id));
}

function updateLeadStatus(id, status) {
  if (!VALID_STATUSES.includes(status)) return null;
  const leads = readAll();
  const lead = leads.find((l) => l.id === id);
  if (!lead) return null;
  lead.status = status;
  writeAll(leads);
  return lead;
}

module.exports = { addLead, listLeads, getLeadsByIds, updateLeadStatus, VALID_STATUSES };
