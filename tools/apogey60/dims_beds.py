"""Данные для слайдов «Размеры» кроватей (23 шт.): кадр #2 (студийный 3/4), длина/ширина(макс. вариант)/высота из dims карточки.
Запуск: python dims_beds.py -> dims-picks-beds.json"""
import json, re, sys
sys.stdout.reconfigure(encoding="utf-8")
cards = {c["localId"]: c for c in json.load(open("cards.json", encoding="utf-8"))}
man = {o["localId"]: o for o in json.load(open("dims-manifest.json", encoding="utf-8"))}
def cm(v):
    x = v / 10; return str(int(x)) if x == int(x) else str(x).replace(".", ",")
PICK = {304: 3, 305: 1, 306: 3, 307: 1}   # номер кадра (1-based), если студийный 3/4 не #2
out = {}
for lid, o in man.items():
    if o["category"] != "Кровати": continue
    L, W, H = cards[lid]["dims"].split("×")
    widths = [int(t) for t in re.findall(r"\d+", W)]
    out[lid] = {"title": o["title"], "L": cm(int(L)), "W": cm(max(widths)), "Wvariants": [cm(w) for w in widths], "H": cm(int(H)),
                "url": o["media"][PICK.get(lid, 2) - 1]["url"], "frame": PICK.get(lid, 2), "media_n": len(o["media"])}
json.dump(out, open("dims-picks-beds.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for lid, v in sorted(out.items()): print(lid, v["title"][:18].ljust(18), f'Д{v["L"]} Ш{v["W"]} {v["Wvariants"]} В{v["H"]}', v["url"].split("/")[-1][:30])
