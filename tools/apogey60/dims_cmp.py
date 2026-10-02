"""python dims_cmp.py <localId> <url результата> [tag]  -> work/dims-<id>/syntx-<tag>.jpg + cmp-<tag>.jpg (референсы слева, результат справа)"""
import sys, os, json, urllib.request
from PIL import Image
lid, url = sys.argv[1], sys.argv[2]; tag = sys.argv[3] if len(sys.argv) > 3 else "v1"
W = os.path.abspath(f"../../work/dims-{lid}"); os.makedirs(W, exist_ok=True)
res = f"{W}/syntx-{tag}.jpg"
req = urllib.request.Request(url.replace("_500.jpg", ".jpg"), headers={"User-Agent": "Mozilla/5.0"})
open(res, "wb").write(urllib.request.urlopen(req).read())
im = Image.open(res).convert("RGB"); print("result", im.size)
pk = json.load(open("dims-picks.json", encoding="utf-8"))[lid]
def ref(n):
    if lid == "270": return Image.open(f"../../work/dims-270/ref{n+0}.png").convert("RGBA")
    return Image.open(f"../../work/dims-sheets/{lid}/{n}.jpg").convert("RGBA")
refs = []
for n in (pk["folded"], pk["unfolded"]):
    r = ref(n if lid != "270" else (2 if n == 2 else 3)); bg = Image.new("RGBA", r.size, "white"); bg.alpha_composite(r); refs.append(bg.convert("RGB"))
RW = 700
refs = [r.resize((RW, int(r.height * RW / r.width))) for r in refs]
H = sum(r.height for r in refs) + 10
out = im.resize((int(im.width * H / im.height), H))
S = Image.new("RGB", (RW + 10 + out.width, H), "white"); y = 0
for r in refs: S.paste(r, (0, y)); y += r.height + 10
S.paste(out, (RW + 10, 0)); S.save(f"{W}/cmp-{tag}.jpg", quality=86); print("cmp", S.size, f"{W}/cmp-{tag}.jpg")
