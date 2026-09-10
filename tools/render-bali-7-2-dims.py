# Two dimension slides for Бали 7.2, built on REAL photos (real floor, real perspective).
#
# ALGORITHM (Oleg, 10.09.2026 — use this for every "Размеры" slide):
#   1. Take the sofa's projection onto the floor — the quad of its four ground corners
#      FL (front-left), FR (front-right), BR (back-right), BL (back-left).
#   2. For each measured side, offset OUTWARD from that floor-projection edge by a fixed
#      distance, large enough to clear the sofa and its ground shadow.
#   3. Draw the dimension line on that offset, strictly PARALLEL to the floor-projection edge,
#      both ends the same perpendicular distance out. Circle at each end, dark pill + white cm.
#   Length and depth lines share the front corner -> they read as an "L" (see tools/dims-style-ref.jpg).
from PIL import Image, ImageDraw, ImageFont
from math import hypot

BASE = r"C:/Users/user/Claude/mebel.hub/assets/bali-7-2"
OUT_W = 1200
INK = (38, 40, 46)
PAD = 170  # white margin added around the photo so offset lines/pills never clip


def font(sz):
    for p in (r"C:/Windows/Fonts/segoeuib.ttf", r"C:/Windows/Fonts/arialbd.ttf"):
        try:
            return ImageFont.truetype(p, sz)
        except OSError:
            pass
    return ImageFont.load_default()


def outward_normal(A, B, ref):
    """Unit normal to A->B pointing AWAY from ref point (the sofa body centre)."""
    dx, dy = B[0] - A[0], B[1] - A[1]
    L = hypot(dx, dy) or 1.0
    nx, ny = -dy / L, dx / L
    mx, my = (A[0] + B[0]) / 2, (A[1] + B[1]) / 2
    if (mx + nx - ref[0]) ** 2 + (my + ny - ref[1]) ** 2 < (mx - nx - ref[0]) ** 2 + (my - ny - ref[1]) ** 2:
        nx, ny = -nx, -ny
    return nx, ny


def dim_line(draw, A, B, ref, label, d, fnt, pill_along=0.5, pill_extra=(0, 0), r=8):
    """A,B = the two floor-projection corners of the measured side. Offset outward by d."""
    nx, ny = outward_normal(A, B, ref)
    A2 = (A[0] + nx * d, A[1] + ny * d)
    B2 = (B[0] + nx * d, B[1] + ny * d)
    draw.line([A2, B2], fill=INK, width=5)
    for c in (A2, B2):
        draw.ellipse([c[0] - r, c[1] - r, c[0] + r, c[1] + r], fill=INK)
    cx = A2[0] + (B2[0] - A2[0]) * pill_along + pill_extra[0]
    cy = A2[1] + (B2[1] - A2[1]) * pill_along + pill_extra[1]
    tb = draw.textbbox((0, 0), label, font=fnt)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    px, py = 22, 13
    box = [cx - tw / 2 - px, cy - th / 2 - py, cx + tw / 2 + px, cy + th / 2 + py]
    draw.rounded_rectangle(box, radius=(box[3] - box[1]) / 2, fill=INK)
    draw.text((cx - tw / 2 - tb[0], cy - th / 2 - tb[1]), label, font=fnt, fill="white")


def build(src, floor, sides, crop, out_name):
    im = Image.open(f"{BASE}/{src}").convert("RGB")
    r = OUT_W / im.width
    im = im.resize((OUT_W, round(im.height * r)), Image.LANCZOS)
    canvas = Image.new("RGB", (im.width + 2 * PAD, im.height + PAD), "white")
    canvas.paste(im, (PAD, 0))
    off = lambda p: (p[0] + PAD, p[1])
    FL, FR, BR, BL = (off(floor[k]) for k in ("FL", "FR", "BR", "BL"))
    ref = ((FL[0] + FR[0] + BR[0] + BL[0]) / 4, (FL[1] + FR[1] + BR[1] + BL[1]) / 4 - 120)
    d = ImageDraw.Draw(canvas)
    fnt = font(46)
    for s in sides:
        A, B = {"FL": FL, "FR": FR, "BR": BR, "BL": BL}[s["a"]], {"FL": FL, "FR": FR, "BR": BR, "BL": BL}[s["b"]]
        dim_line(d, A, B, ref, s["label"], s["d"], fnt,
                 s.get("pill_along", 0.5), s.get("pill_extra", (0, 0)))
    if crop:
        x0, y0, x1, y1 = crop
        canvas = canvas.crop((x0 + PAD if x0 == 0 else x0, y0, x1 + PAD if x1 == OUT_W else x1, y1)) \
            if False else canvas.crop(crop)
    canvas.save(f"{BASE}/{out_name}", quality=92)
    print("wrote", out_name, canvas.size)


# ---------------- FOLDED (folded34_src.jpg — real photo rotated to 3/4) : габариты корпуса ----------------
# 3/4 from front-left: front edge FL->FR = длина 256, right end FR->BR = глубина 137, L at FR.
build(
    "folded34_src.jpg",
    floor=dict(FL=(110, 720), FR=(900, 645), BR=(985, 600), BL=(95, 690)),
    sides=[
        dict(a="FL", b="FR", label="256", d=84, pill_along=0.42, pill_extra=(0, 8)),
        dict(a="FR", b="BR", label="137", d=74, pill_along=0.5, pill_extra=(24, 2)),
    ],
    crop=(60, 300, 1200 + 2 * PAD - 10, 896 + PAD),
    out_name="slide_dims_folded.jpg",
)

# ---------------- UNFOLDED (slide_unfolded.jpg, real photo, person removed) : спальное место ----------------
# clear 3/4 from front-left: front edge FL->FR = длина, left edge FL->BL = глубина, share FL (L-shape).
build(
    "slide_unfolded.jpg",
    floor=dict(FL=(291, 694), FR=(974, 678), BR=(1006, 590), BL=(223, 447)),
    sides=[
        dict(a="FL", b="FR", label="200", d=84, pill_along=0.46, pill_extra=(0, 8)),
        dict(a="FL", b="BL", label="190", d=74, pill_along=0.52, pill_extra=(-28, 0)),
    ],
    crop=(120, 300, 1200 + 2 * PAD - 10, 896 + PAD),
    out_name="slide_dims_unfolded.jpg",
)
