"""Замена числа в плашке: берём готовую плашку с нужным числом из этого же изображения и ставим на место старой.
python dims_fixnum.py <in.jpg> <out.jpg> <src_cx,src_cy> <dst_cx,dst_cy>   (центры плашек, px полного размера)"""
import sys, numpy as np
from PIL import Image
inp, outp = sys.argv[1], sys.argv[2]
sc = tuple(int(v) for v in sys.argv[3].split(",")); dc = tuple(int(v) for v in sys.argv[4].split(","))
im = Image.open(inp).convert("RGB"); a = np.asarray(im).astype(int); H, W = a.shape[:2]
def dark(x, y):  # тёмно-графитовый цвет плашки/линий (не коричневая обивка/дерево)
    p = a[y, x]; return p.max() < 90 and p[2] >= p[0] - 6
def bbox(cx, cy):
    ys = [y for y in range(cy - 70, cy + 71) if any(dark(x, y) for x in range(cx - 10, cx + 11))]
    top, bot = min(ys), max(ys); h = bot - top + 1
    d = int(0.15 * h); yy = top + d
    l = cx
    while not dark(l, yy) and l > cx - 40: l -= 1      # от центра к ближайшему тёмному пикселю верхней строки плашки
    x0 = l; r = l
    while dark(l - 1, yy): l -= 1
    while dark(r + 1, yy): r += 1
    R = h / 2; pad = int(round(R - (R * R - (R - d) ** 2) ** 0.5))  # поправка на скругление
    return l - pad, top, r + pad, bot
sb = bbox(*sc); db = bbox(*dc)
print("src bbox", sb, "dst bbox", db)
sw, sh = sb[2] - sb[0] + 1, sb[3] - sb[1] + 1; dw, dh = db[2] - db[0] + 1, db[3] - db[1] + 1
# 1) закрасить ТОЛЬКО контур старой плашки фоном (линия вне плашки остаётся целой)
from PIL import ImageFilter
out = im.copy(); arr = np.asarray(out).copy()
bg = np.median(arr[db[1] - 22:db[1] - 8, db[0]:db[2] + 1].reshape(-1, 3), axis=0).astype(np.uint8)
dmask = np.zeros((H, W), np.uint8)
for y in range(db[1], db[3] + 1):
    row = [x for x in range(db[0], db[2] + 1) if dark(x, y) or a[y, x].min() > 235 and db[0] + 4 < x < db[2] - 4]
    drow = [x for x in range(db[0], db[2] + 1) if dark(x, y)]
    if drow: dmask[y, min(drow):max(drow) + 1] = 255
dm = Image.fromarray(dmask).filter(ImageFilter.MaxFilter(5))
arr_img = Image.fromarray(arr); arr_img.paste(Image.new("RGB", (W, H), tuple(int(v) for v in bg)), (0, 0), dm)
out = arr_img
# 2) плашка-образец: прямоугольник с закруглением по маске «тёмное + белые цифры внутри»
tpl = im.crop((sb[0], sb[1], sb[2] + 1, sb[3] + 1)).convert("RGB")
ta = np.asarray(tpl).astype(int)
mask = np.zeros((sh, sw), np.uint8)
for y in range(sh):
    row = [x for x in range(sw) if ta[y, x].max() < 90 and ta[y, x][2] >= ta[y, x][0] - 6]
    if row: mask[y, min(row):max(row) + 1] = 255   # заполняем внутренность (цифры) между краями
tpl2 = tpl.resize((dw, dh), Image.LANCZOS); mk = Image.fromarray(mask).resize((dw, dh), Image.LANCZOS)
out.paste(tpl2, (db[0], db[1]), mk)
out.save(outp, quality=95); print("saved", outp)
