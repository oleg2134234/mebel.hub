"""Выбор кадров и цифр для слайдов «Размеры» (диваны/кресла). Запуск: python dims_picks.py -> dims-picks.json"""
import json, sys
sys.stdout.reconfigure(encoding="utf-8")
man = {o["localId"]: o for o in json.load(open("dims-manifest.json", encoding="utf-8"))}
# localId: (номер медиа сложенного, номер медиа разложенного) — по контактным листам work/dims-sheets
PICK = {270:(2,3), 271:(2,3), 272:(5,7), 273:(5,6), 274:(5,6), 276:(5,6), 277:(5,6), 278:(5,6), 279:(5,6), 280:(5,6),
        282:(5,6), 283:(5,6), 284:(6,7), 296:(5,6), 297:(5,7), 298:(5,6), 309:(5,6), 313:(5,6), 314:(5,6), 315:(5,6),
        316:(5,6), 317:(5,6), 318:(5,6), 319:(5,6), 320:(5,6), 321:(5,6), 322:(5,6), 323:(5,6), 324:(2,3), 325:(4,5), 326:(4,5)}
SWAP = {284}   # спальное место выкатывается в глубину: меньшее число — вдоль переднего края
OVERRIDE = {297: {"F": 270}}   # решение пользователя 02.10.2026: спальное место Остин ДКУ — 270 вдоль переднего края
GAP = {275:"нет кадра разложенного вида", 281:"нет кадра разложенного вида и спального места в API", 285:"нет кадра разложенного вида"}
out = {}
for lid, (f, u) in PICK.items():
    o = man[lid]; L = o["folded_mm"]["length"] // 10; D = o["folded_mm"]["depth_or_widths"][0] // 10
    s = o["sleep"]; a, b = s["length_mm"] // 10, s["width_mm"] // 10
    cand = [v for v in (a, b) if v <= L]
    F = max(cand) if cand else min(a, b); S = b if F == a else a        # F — вдоль переднего края, S — в глубину
    if lid in SWAP: F, S = S, F
    if lid in OVERRIDE: F = OVERRIDE[lid].get("F", F); S = OVERRIDE[lid].get("S", S)
    flag = []
    if S > 230: flag.append(f"глубина разложенного {S} см неправдоподобна — проверить исходные данные")
    if o["category"] == "Диваны" and "ДКУ" in o["title"].upper() or "Мартин" in o["title"] or "МАРТИН" in o["title"]: flag.append("угловой: соответствие F/S проверить глазами")
    out[lid] = {"title": o["title"], "folded": f, "unfolded": u, "L": L, "D": D, "F": F, "S": S,
                "urls": [o["media"][f-1]["url"], o["media"][u-1]["url"]], "flags": flag}
for lid, why in GAP.items(): out[lid] = {"title": man[lid]["title"], "gap": why}
json.dump(out, open("dims-picks.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for lid, v in sorted(out.items()):
    print(lid, v["title"][:30].ljust(30), ("ПРОБЕЛ: " + v["gap"]) if "gap" in v else f'сложен {v["L"]}x{v["D"]}  спал.: перед {v["F"]} / бок {v["S"]}  кадры {v["folded"]}/{v["unfolded"]}  {"; ".join(v["flags"])}')
