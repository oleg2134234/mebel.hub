"""Публикация принятых слайдов «Размеры» пачкой.
python dims_pub.py <PUB-worktree> <id:tag> [<id:tag> ...]   (tag — суффикс файла work/dims-<id>/syntx-<tag>.jpg)
Добавляет assets/<slug>/slide_dims.jpg и слайд «Размеры» вторым в GALLERIES[id] (после «В интерьере»), коммитит. Пуш — отдельно."""
import sys, os, json, re, subprocess
from PIL import Image
sys.stdout.reconfigure(encoding="utf-8")
PUB = sys.argv[1]; items = [a.split(":") for a in sys.argv[2:]]
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.abspath(HERE + "/../../work")
cards = {c["localId"]: c for c in json.load(open(HERE + "/cards.json", encoding="utf-8"))}
man = {o["localId"]: o for o in json.load(open(HERE + "/dims-manifest.json", encoding="utf-8"))}
api = {x["id"]: x["attributes"] for x in json.load(open(HERE + "/all.json", encoding="utf-8"))}
pk = json.load(open(HERE + "/dims-picks.json", encoding="utf-8"))
beds = json.load(open(HERE + "/dims-picks-beds.json", encoding="utf-8"))
html_path = PUB + "/index.html"; h = open(html_path, encoding="utf-8", newline="").read()
done = []
for lid, tag in items:
    lid = int(lid); c = cards[lid]; slug = c["slug"]
    if str(lid) in beds:
        b = beds[str(lid)]; m = re.search(r"Спальное место ([\d/]+)[×x](\d+) мм", c["desc"])
        sl = ""
        if m: sl = " Спальное место " + "/".join(str(int(w) // 10) for w in m.group(1).split("/")) + "×" + str(int(m.group(2)) // 10) + " см."
        if len(b["Wvariants"]) > 1:
            desc = f'Габариты: длина {b["L"]} см, ширина {b["Wvariants"][0]}–{b["W"]} см (в зависимости от спального места), высота {b["H"]} см. На схеме — вариант шириной {b["W"]} см.{sl}'
        else:
            desc = f'Габариты: длина {b["L"]} см, ширина {b["W"]} см, высота {b["H"]} см.{sl}'
    else:
        p = pk[str(lid)]
        H = int(re.findall(r"\d+", str(api[man[lid]["webId"]]["dimensions"]["height"]))[0]) // 10
        a, b = sorted((p["F"], p["S"]), reverse=True)
        desc = f'Габариты в сложенном виде {p["L"]}×{p["D"]}×{H} см и спальное место в разложенном виде {a}×{b} см.'
    dst_rel = f"assets/{slug}/slide_dims.jpg"; os.makedirs(f"{PUB}/assets/{slug}", exist_ok=True)
    im = Image.open(f"{WORK}/dims-{lid}/syntx-{tag}.jpg").convert("RGB"); im = im.resize((1200, round(im.height * 1200 / im.width)), Image.LANCZOS)
    im.save(f"{PUB}/{dst_rel}", quality=86, optimize=True)
    start = h.index(f'"{lid}":{{"title":'); end = h.index('"}]}', start)
    seg = h[start:end]
    if '"name":"Размеры"' in seg: print("уже есть слайд у", lid); continue
    new = f'"}},{{"src":"{dst_rel}","name":"Размеры","desc":{json.dumps(desc, ensure_ascii=False)}'
    h = h[:end] + new + h[end + 1:]  # '"}]}' -> '"},{...slide..."}]}'
    done.append((lid, slug, desc))
open(html_path, "w", encoding="utf-8", newline="").write(h)
for lid, slug, desc in done: print(lid, slug, "|", desc)
