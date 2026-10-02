
window.TPL = "Create one vertical 3:4 furniture-catalog dimensions slide with exactly two stacked panels on a clean warm-white studio background.\n\nPRODUCT IDENTITY — ABSOLUTE PRIORITY\nImage 1 is the authoritative reference for the sofa in its folded state. Use that exact sofa without redesigning, improving, simplifying, widening, narrowing, stretching, or replacing any part. Preserve exactly its construction, overall proportions, width-to-depth ratio, armrest shape and thickness, light wood trim, upholstery color and texture, seam positions, panel count, backrest shape, seat divisions, front rail, feet, and every visible structural detail.\nImage 2 is the authoritative reference for the same sofa in its unfolded state. Preserve the real transformation and every structural detail from Image 2. Do not invent a different mechanism or sleeping platform.\n\nLAYOUT AND CAMERA\nTop panel: the exact folded sofa from Image 1, fully visible, at its original natural front three-quarter angle.\nBottom panel: the exact same sofa unfolded as in Image 2, fully visible. Rotate/reframe the unfolded sofa only as needed so its camera position, viewing direction, perspective, scale, and front three-quarter angle match the top panel exactly. It must look like the same fixed camera photographed the sofa before and after unfolding. Do not alter the sofa itself while matching the angle.\nKeep generous empty floor space below and beside each sofa for dimension annotations. Do not crop any part.\n\nDIMENSION ANNOTATIONS\nUse thin dark-charcoal lines, one small solid circle at each end, and a dark rounded capsule centered on each line with bold white numerals. Numerals only, in centimeters. No extension or leader lines.\nTop panel: length line labelled “@L1@” on the floor below the sofa, precisely parallel to the visible front bottom edge in image perspective; depth line labelled “@D1@” on the floor beside the sofa, precisely parallel to the visible side bottom edge receding from the camera. The lines form a clean perspective-aligned corner.\nBottom panel: line labelled “@F@” along the FRONT edge of the unfolded sleeping platform (the edge nearest the camera), precisely parallel to the front bottom edge of the sofa; line labelled “@S@” along the SIDE edge of the platform receding away from the camera, precisely parallel to the visible side bottom edge. The two lines form the same perspective-aligned corner as the real platform edges.\n\nGEOMETRY CHECK — MANDATORY\nEvery dimension line must follow the sofa’s actual projected floor geometry. Never align a line to the image frame unless the corresponding sofa edge is also parallel to the frame. No arbitrary horizontal or diagonal lines. No line, endpoint circle, or number capsule may cross, touch, overlap, or float over the sofa, feet, upholstery, wooden trim, sleeping surface, or contact shadow. Keep all annotations outside the silhouette on the floor with a small even gap.\n\nDo not add a title, product name, height dimension, explanatory text, arrows, logos, watermark, decor, people, pets, or other furniture. The only visible text is exactly “@L1@”, “@D1@”, “@F@”, “@S@”.\nFinal self-check: both panels show the identical sofa model; folded and unfolded views use the same camera angle; construction and proportions are unchanged; all four dimension lines are parallel to their corresponding real edges in perspective; annotations do not overlap the product.\n";
window.dimsRun = async (urls, nums) => {
  const dt = new DataTransfer();
  for (const u of urls) {
    const r = await fetch("https://admin.apogey-mebel.ru" + u); const b = await r.blob(); const bm = await createImageBitmap(b);
    const s = Math.min(1, 1600 / Math.max(bm.width, bm.height));
    const cv = document.createElement("canvas"); cv.width = Math.round(bm.width * s); cv.height = Math.round(bm.height * s);
    const cx = cv.getContext("2d"); cx.fillStyle = "#ffffff"; cx.fillRect(0, 0, cv.width, cv.height); cx.drawImage(bm, 0, 0, cv.width, cv.height);
    const jb = await new Promise(r => cv.toBlob(r, "image/jpeg", 0.9));
    dt.items.add(new File([jb], "ref" + dt.items.length + ".jpg", { type: "image/jpeg" }));
  }
  const inp = document.querySelector("input[type=file]"); inp.files = dt.files; inp.dispatchEvent(new Event("change", { bubbles: true }));
  await new Promise(r => setTimeout(r, 5000));
  const p = window.TPL.replaceAll("@L1@", nums[0]).replaceAll("@D1@", nums[1]).replaceAll("@F@", nums[2]).replaceAll("@S@", nums[3]);
  const ta = document.querySelector("textarea.textarea-input");
  Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, "value").set.call(ta, p);
  ta.dispatchEvent(new Event("input", { bubbles: true }));
  await new Promise(r => setTimeout(r, 800));
  const att = document.querySelectorAll(".uploaded-files img, .uploaded-files__item").length;
  const btn = document.querySelector("button.send-actions__send");
  const ok = btn && !btn.disabled && !(p.includes("@"));
  if (ok) btn.click();
  return { sent: !!ok, att, promptLen: p.length, cost: (document.body.innerText.match(/\n(\d)\s*\n?\s*$/m) || [])[1] || null };
};
window.dimsResult = () => {
  const g = [...document.querySelectorAll("img")].map(i => i.currentSrc || i.src).filter(s => s.includes("/generated/"));
  return g.length ? g[g.length - 1].replace("_500.jpg", ".jpg") : null;
};
