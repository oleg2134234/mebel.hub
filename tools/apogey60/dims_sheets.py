"""Контактные листы превью (формат small, 500px) для выбора сложенного/разложенного кадров.
Запуск: python dims_sheets.py  -> ../../work/dims-sheets/<localId>/<n>.jpg и sheet_XX.jpg (по 4 карточки)."""
import json, os, sys, urllib.request
from PIL import Image, ImageDraw
sys.stdout.reconfigure(encoding="utf-8")
OUT = os.path.abspath("../../work/dims-sheets-beds" if len(sys.argv) > 1 and sys.argv[1] == "beds" else "../../work/dims-sheets"); os.makedirs(OUT, exist_ok=True)
api = {x["id"]: x["attributes"] for x in json.load(open("all.json", encoding="utf-8"))}
BEDS = len(sys.argv) > 1 and sys.argv[1] == "beds"
man = [o for o in json.load(open("dims-manifest.json", encoding="utf-8"))
       if ((o["category"] == "Кровати") if BEDS else (o["category"] in ("Диваны", "Кресла") and o["localId"] not in (270, 272)))]
for o in man:
    d = f'{OUT}/{o["localId"]}'; os.makedirs(d, exist_ok=True)
    for i, m in enumerate(api[o["webId"]]["media"]["data"], 1):
        f = d + f"/{i}.jpg"
        if os.path.exists(f): continue
        at = m["attributes"]; u = (at.get("formats") or {}).get("small", {}).get("url") or at["url"]
        urllib.request.urlretrieve("https://admin.apogey-mebel.ru" + u, f)
TW = 230
for s in range(0, len(man), 4):
    grp = man[s:s + 4]; rows = []
    for o in grp:
        ims = []
        for i in range(1, len(o["media"]) + 1):
            im = Image.open(f'{OUT}/{o["localId"]}/{i}.jpg').convert("RGB"); im = im.resize((TW, int(im.height * TW / im.width)))
            c = Image.new("RGB", (TW, 150 + 14), "white"); c.paste(im.crop((0, max(0, (im.height - 150) // 2), TW, max(0, (im.height - 150) // 2) + 150)), (0, 14))
            ImageDraw.Draw(c).text((3, 1), f"#{i}", fill="red"); ims.append(c)
        rows.append((o, ims))
    W = max(len(ims) for _, ims in rows) * (TW + 4); H = sum(164 + 16 for _ in rows)
    sheet = Image.new("RGB", (W, H), "white"); y = 0
    for o, ims in rows:
        ImageDraw.Draw(sheet).text((3, y + 1), f'{o["localId"]} {o["title"]}  складн.{o["folded_mm"]["length"]//10}x{o["folded_mm"]["depth_or_widths"][0]//10}', fill="blue")
        for k, c in enumerate(ims): sheet.paste(c, (k * (TW + 4), y + 16))
        y += 180
    sheet.save(f"{OUT}/sheet_{s//4+1:02d}.jpg", quality=80); print("sheet", s // 4 + 1, [o["localId"] for o in grp])
