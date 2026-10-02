"""python dims_cmp_bed.py <localId> <url> [tag] -> work/dims-<id>/syntx-<tag>.jpg + cmp-<tag>.jpg (референс слева, результат справа)"""
import sys, os, json, urllib.request
from PIL import Image
lid, url = sys.argv[1], sys.argv[2]; tag = sys.argv[3] if len(sys.argv) > 3 else "v1"
W = os.path.abspath(f"../../work/dims-{lid}"); os.makedirs(W, exist_ok=True)
res = f"{W}/syntx-{tag}.jpg"
req = urllib.request.Request(url.replace("_500.jpg", ".jpg"), headers={"User-Agent": "Mozilla/5.0"})
open(res, "wb").write(urllib.request.urlopen(req).read())
im = Image.open(res).convert("RGB"); print("result", im.size)
fr = json.load(open("dims-picks-beds.json", encoding="utf-8"))[lid]["frame"]
r = Image.open(f"../../work/dims-sheets-beds/{lid}/{fr}.jpg").convert("RGBA"); bg = Image.new("RGBA", r.size, "white"); bg.alpha_composite(r); r = bg.convert("RGB")
RW = 760; r = r.resize((RW, int(r.height * RW / r.width))); out = im.resize((900, int(im.height * 900 / im.width)))
S = Image.new("RGB", (RW + 10 + out.width, out.height), "white"); S.paste(r, (0, 0)); S.paste(out, (RW + 10, 0)); S.save(f"{W}/cmp-{tag}.jpg", quality=86); print("cmp", S.size)
