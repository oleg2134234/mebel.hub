"use strict";

const crypto = require("crypto");

function safeEqual(a, b) {
  const bufA = Buffer.from(a);
  const bufB = Buffer.from(b);
  if (bufA.length !== bufB.length) return false;
  return crypto.timingSafeEqual(bufA, bufB);
}

/** HTTP Basic Auth gate for the admin panel. Disabled (503) until credentials are set. */
function adminAuth(req, res, next) {
  const user = process.env.ADMIN_USER;
  const pass = process.env.ADMIN_PASS;
  if (!user || !pass) {
    return res
      .status(503)
      .send("Admin panel is not configured. Set ADMIN_USER and ADMIN_PASS in .env.");
  }

  const header = req.headers.authorization || "";
  const [scheme, encoded] = header.split(" ");
  if (scheme !== "Basic" || !encoded) {
    res.set("WWW-Authenticate", 'Basic realm="Sytnie Ugodya Admin"');
    return res.status(401).send("Authentication required.");
  }

  const [reqUser, reqPass] = Buffer.from(encoded, "base64").toString("utf8").split(":");
  if (!reqUser || !reqPass || !safeEqual(reqUser, user) || !safeEqual(reqPass, pass)) {
    res.set("WWW-Authenticate", 'Basic realm="Sytnie Ugodya Admin"');
    return res.status(401).send("Invalid credentials.");
  }

  next();
}

module.exports = adminAuth;
