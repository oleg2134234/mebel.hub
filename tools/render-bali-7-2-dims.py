# Builds TWO separate dimension slides for Бали 7.2:
#   assets/bali-7-2/slide_dims_folded.jpg    — folded sofa + габариты корпуса (длина, глубина)
#   assets/bali-7-2/slide_dims_unfolded.jpg  — unfolded sofa + спальное место (длина, ширина)
# Callouts are computed geometrically: each line is parallel to the measured floor edge A->B,
# pushed outward by a constant perpendicular offset (never crossing the sofa), circles at the
# ends, a dark pill with a white number (cm, no units). Height is NOT on the slides.
from PIL import Image, ImageDraw, ImageFont
from math import hypot
import numpy as np

BASE = r"C:/Users/user/Claude/mebel.hub/assets/bali-7-2"
OUT_W = 1200
GRAPHITE = (44, 46, 52)

def load_font(sz):
    for p in (r"C:/Windows/Fonts/segoeuib.ttf", r"C:/Windows/Fonts/arialbd.ttf"):
        try:
            return ImageFont.truetype(p, sz)
        except OSError:
            pass
    return ImageFont.load_default()

def purify(im):
    a = np.asarray(im.convert("RGB")).astype(np.int16)
    mx = a.max(axis=2); mn = a.min(axis=2)
    bg = (mn > 234) & ((mx - mn) < 16)
    a[bg] = [255, 255, 255]
    return Image.fromarray(a.astype(np.uint8))

def edge_callout(draw, A, B, label, font, d, side, pill_shift=(0, 0), r=8):
    """Line parallel to A->B, offset by d along the outward unit normal (side = +1/-1).
    Circles at both ends; a centered dark pill with white `label`."""
    dx, dy = B[0] - A[0], B[1] - A[1]
    L = hypot(dx, dy) or 1.0
    nx, ny = -dy / L * side, dx / L * side
    A2 = (A[0] + nx * d, A[1] + ny * d)
    B2 = (B[0] + nx * d, B[1] + ny * d)
    draw.line([A2, B2], fill=GRAPHITE, width=3)
    for c in (A2, B2):
        draw.ellipse([c[0] - r, c[1] - r, c[0] + r, c[1] + r], fill=GRAPHITE)
    cx = (A2[0] + B2[0]) / 2 + pill_shift[0]
    cy = (A2[1] + B2[1]) / 2 + pill_shift[1]
    tb = draw.textbbox((0, 0), label, font=font)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    padx, pady = 20, 12
    box = [cx - tw / 2 - padx, cy - th / 2 - pady, cx + tw / 2 + padx, cy + th / 2 + pady]
    draw.rounded_rectangle(box, radius=(box[3] - box[1]) / 2, fill=GRAPHITE)
    draw.text((cx - tw / 2 - tb[0], cy - th / 2 - tb[1]), label, font=font, fill=(255, 255, 255))

PAD_BOTTOM = 150  # white room so bottom pills never clip

def build(src, edges, crop, out_name):
    im = purify(Image.open(f"{BASE}/{src}")).convert("RGB")
    r = OUT_W / im.width
    im = im.resize((OUT_W, round(im.height * r)), Image.LANCZOS)
    canvas = Image.new("RGB", (OUT_W, im.height + PAD_BOTTOM), (255, 255, 255))
    canvas.paste(im, (0, 0))
    im = canvas
    d = ImageDraw.Draw(im)
    font = load_font(46)
    for e in edges:
        edge_callout(d, e["A"], e["B"], e["label"], font, e["d"], e["side"], e.get("shift", (0, 0)))
    if crop:
        im = im.crop(crop)
    im.save(f"{BASE}/{out_name}", quality=92)
    print("wrote", out_name, im.size)

OFFSET = 56  # one shared perpendicular offset for every line, per the 10.09.2026 rule

# ---------- FOLDED: габариты корпуса ----------  (panel: shadow-free cut, 1200x896)
build(
    "dims_src_folded.png",
    edges=[
        # длина 256 — параллельно передней нижней грани, от левого угла проекции до правого
        dict(A=(140, 665), B=(1000, 703), label="256", d=OFFSET, side=1, shift=(0, 4)),
        # глубина 137 — параллельно правой нижней грани (торцу), вынесена вправо-вниз
        dict(A=(1000, 700), B=(1085, 655), label="137", d=OFFSET, side=1, shift=(20, 0)),
    ],
    crop=(0, 270, 1200, 852),
    out_name="slide_dims_folded.jpg",
)

# ---------- UNFOLDED: спальное место ----------  (panel: clean white v4, 1200x896)
build(
    "dims_src_unfolded.png",
    edges=[
        # длина спального 200 — параллельно передней нижней грани
        dict(A=(135, 645), B=(1000, 745), label="200", d=OFFSET, side=1, shift=(0, 4)),
        # ширина спального 190 — параллельно правой нижней грани (торцу)
        dict(A=(1000, 745), B=(1090, 690), label="190", d=OFFSET, side=1, shift=(20, 0)),
    ],
    crop=(0, 300, 1200, 884),
    out_name="slide_dims_unfolded.jpg",
)
