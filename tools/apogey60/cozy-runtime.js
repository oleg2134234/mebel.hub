/* CARDS[id] = [kind(s|a|b), ref, color, style, action, config] — задаётся патчем (python cozy_build.py patch ID…) */
window.cozyPrompt = (id) => {
  const a = window.CARDS[id], kind = { s: "sofa", a: "armchair", b: "bed" }[a[0]], bed = kind === "bed";
  return window.CTPL[bed ? "bed" : "sofa"]
    .replaceAll("@KIND@", kind === "armchair" ? "armchair" : "sofa").replaceAll("@ROOM_WORD@", kind === "armchair" ? "reading corner" : "living room")
    .replaceAll("@COLOR@", a[2]).replaceAll("@STYLE@", a[3]).replaceAll("@ACTION@", a[4]).replaceAll("@CONFIG@", a[5]);
};
window.cozyRun = async (id) => {
  const dt = new DataTransfer();
  const r = await fetch("https://admin.apogey-mebel.ru/uploads/" + window.CARDS[id][1]); const b = await r.blob(); const bm = await createImageBitmap(b);
  const s = Math.min(1, 1600 / Math.max(bm.width, bm.height));
  const cv = document.createElement("canvas"); cv.width = Math.round(bm.width * s); cv.height = Math.round(bm.height * s);
  const cx = cv.getContext("2d"); cx.fillStyle = "#ffffff"; cx.fillRect(0, 0, cv.width, cv.height); cx.drawImage(bm, 0, 0, cv.width, cv.height);
  const jb = await new Promise(r => cv.toBlob(r, "image/jpeg", 0.9)); dt.items.add(new File([jb], "ref0.jpg", { type: "image/jpeg" }));
  const inp = document.querySelector("input[type=file]"); inp.files = dt.files; inp.dispatchEvent(new Event("change", { bubbles: true }));
  await new Promise(r => setTimeout(r, 5000));
  const p = window.cozyPrompt(id); const ta = document.querySelector("textarea.textarea-input");
  Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, "value").set.call(ta, p); ta.dispatchEvent(new Event("input", { bubbles: true }));
  await new Promise(r => setTimeout(r, 800));
  let btn = document.querySelector("button.send-actions__send"), sent = !!(btn && !btn.disabled && !p.includes("@"));
  if (sent) btn.click();
  else { for (let k = 0; k < 8 && !sent; k++) { await new Promise(r => setTimeout(r, 3000)); btn = document.querySelector("button.send-actions__send"); if (btn && !btn.disabled && !p.includes("@")) { btn.click(); sent = "retry"; } } }
  return { id, sent, promptLen: p.length };
};
window.cozyResult = () => {
  const g = [...document.querySelectorAll("img")].map(i => i.currentSrc || i.src).filter(s => s.includes("/generated/"));
  return g.length ? g[g.length - 1].replace("_500.jpg", ".jpg") : null;
};
