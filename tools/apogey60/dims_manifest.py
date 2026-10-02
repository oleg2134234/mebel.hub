"""Манифест для слайдов «Размеры» (Syntx): цифры и референсы для 60 карточек Apogey (ID 270-329).
Запуск: python dims_manifest.py  ->  dims-manifest.json + сводка в консоль. Ничего не скачивает."""
import json, re, sys
sys.stdout.reconfigure(encoding="utf-8")
api = {x["id"]: x["attributes"] for x in json.load(open("all.json", encoding="utf-8"))}
cards = {c["localId"]: c for c in json.load(open("cards.json", encoding="utf-8"))}
out = []
for line in open("rows.txt", encoding="utf-8"):
    p = line.rstrip("\n").split("|")
    if len(p) < 5 or not p[0].strip().isdigit():
        continue
    n, cat, title, web = int(p[0]), p[1], p[2], int(p[3])
    lid = 269 + n
    a = api[web]
    dm = a["dimensions"]
    num = lambda v: [int(t) for t in re.findall(r"\d+", str(v))]
    L, W = num(dm["length"])[0], num(dm["width"])   # у кроватей ширина — список вариантов
    sleep = None
    for adv in a.get("advantages") or []:
        m = re.search(r"СПАЛЬНОЕ МЕСТО\s+(\d+)\s*[хxХ×]\s*(\d+)", adv.get("name", ""), re.I)
        if m:
            s = sorted(map(int, m.groups()))   # (меньшая=ширина, большая=длина)
            sleep = {"length_mm": s[1], "width_mm": s[0], "src": adv["name"].strip()}
            break
    media = [{"id": m["id"], "name": m["attributes"]["name"], "url": m["attributes"]["url"],
              "w": m["attributes"]["width"], "h": m["attributes"]["height"], "ext": m["attributes"]["ext"]}
             for m in a["media"]["data"]]
    risks = []
    if cat == "Матрасы": risks.append("матрас: нет сложенного/разложенного вида — слайд скриптом, не Syntx")
    if sleep is None and cat != "Матрасы": risks.append("нет «СПАЛЬНОЕ МЕСТО» в преимуществах API — размер спального места подтвердить")
    if len(media) != 3: risks.append(f"media={len(media)} (ожидалось 3: интерьер, сложен., разложен.)")
    out.append({"localId": lid, "webId": web, "category": cat, "title": title,
                "slug": cards.get(lid, {}).get("slug"),
                "folded_mm": {"length": L, "depth_or_widths": W}, "sleep": sleep, "media": media, "risks": risks})
json.dump(out, open("dims-manifest.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
ok = [o for o in out if not o["risks"]]
print(f"всего {len(out)}; без рисков {len(ok)}; с замечаниями {len(out)-len(ok)}\n")
for o in out:
    s = o["sleep"]; sl = f'{s["length_mm"]//10}x{s["width_mm"]//10}' if s else "—"
    print(f'{o["localId"]} {o["category"][:4]} {o["title"][:34]:34} сл.{o["folded_mm"]["length"]//10}x{"/".join(str(w//10) for w in o["folded_mm"]["depth_or_widths"])} спал.{sl:8} media={len(o["media"])} {"; ".join(o["risks"])}')
