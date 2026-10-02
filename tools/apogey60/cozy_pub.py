"""Публикация принятых слайдов «Уют» пачкой.
python cozy_pub.py <PUB-worktree> <папка-с-результатами> <id> [<id> ...]   (результат — <папка>/<id>.jpg, 1792×2400 из Syntx)
Кладёт assets/<slug>/slide_cozy.jpg (1400 px, q86) и вставляет слайд «Уют» ВТОРЫМ в GALLERIES[id] (после «В интерьере»; «Размеры» сдвигаются на 3-е место).
Строковая вставка без пересериализации index.html. Коммит и пуш — отдельно."""
import sys, os, json
from PIL import Image
sys.stdout.reconfigure(encoding="utf-8")
PUB, GEN, ids = sys.argv[1], sys.argv[2], [int(a) for a in sys.argv[3:]]
HERE = os.path.dirname(os.path.abspath(__file__))
cards = {int(k): v for k, v in json.load(open(HERE + "/cozy-cards.json", encoding="utf-8")).items()}

from cozy_ru import desc as _desc

def desc(c, i): return _desc(c)

html_path = PUB + "/index.html"; h = open(html_path, encoding="utf-8", newline="").read()
dec = json.JSONDecoder(); done = []
for i in ids:
    c = cards[i]; slug = c["slug"]; dst = f"assets/{slug}/slide_cozy.jpg"
    start = h.index(f'"{i}":{{"title":'); first = h.index('{"src"', start)
    _, end = dec.raw_decode(h, first)  # конец первого слайда («В интерьере»)
    seg = h[start:h.index("]}", end)]
    if '"name":"Уют"' in seg: print("уже есть слайд у", i); continue
    os.makedirs(f"{PUB}/assets/{slug}", exist_ok=True)
    im = Image.open(f"{GEN}/{i}.jpg").convert("RGB"); im = im.resize((1400, round(im.height * 1400 / im.width)), Image.LANCZOS)
    im.save(f"{PUB}/{dst}", quality=86, optimize=True)
    d = desc(c, i); new = "," + json.dumps({"src": dst, "name": "Уют", "desc": d}, ensure_ascii=False, separators=(",", ":"))
    h = h[:end] + new + h[end:]
    done.append((i, slug, d, os.path.getsize(f"{PUB}/{dst}") // 1024))
open(html_path, "w", encoding="utf-8", newline="").write(h)
for i, slug, d, kb in done: print(i, slug, kb, "КБ |", d)
