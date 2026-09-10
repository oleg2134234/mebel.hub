# -*- coding: utf-8 -*-
"""Джой 7 ДКУ-О (id 226) — размерные выноски на белых панелях.

Раскладка по образцу Олега (нарисован от руки 10.09.2026, "не трогай линии и их расположение"):
  сложенный вид  — длина 377 прямой линией ПОД диваном во всю ширину, от края до края;
                   глубина 180 короткой диагональю у кушетки сверху-справа, параллельно торцу.
  разложенный    — ширина спального 174 прямой линией ПОД платформой во всю ширину;
                   глубина 198 короткой диагональю у левого торца снизу-слева, параллельно грани.
Линии строятся детерминированно, у каждого конца — тонкая выносная линия до реального угла габарита.

Источники: assets/joy-7-dku-o/dims_white_{folded,unfolded}.jpg
          (панели из старого slide3_dims.jpg, серый фон убран до белого через Nano Banana).
Числа: PRODUCTS[226].dims 3770x1800x855 -> сложенный 377 x 180 (высота 86 -> подпись);
       desc "Спальное место 1740x1980" -> 174 (ширина) x 198 (глубина).
"""
import math
from PIL import Image, ImageDraw, ImageFont

DEST = r"C:\Users\user\Claude\mebel.hub\assets\joy-7-dku-o"
INK = (58, 42, 38)
LW = 6            # основная размерная линия
EW = 3           # выносная линия
DOT = 15         # кружок на конце линии
EXT = False      # выносные линии к углам габарита (Олег 10.09.2026: не нужны, стиль как у др. слайдов)
FONT_PATH = r"C:\Windows\Fonts\arialbd.ttf"


def unit(A, B):
    dx, dy = B[0]-A[0], B[1]-A[1]
    L = math.hypot(dx, dy)
    return (dx/L, dy/L), L


def pick_norm(u, want):
    n1 = (u[1], -u[0]); n2 = (-u[1], u[0])
    s = lambda n: {'+x': n[0], '-x': -n[0], '+y': n[1], '-y': -n[1]}[want]
    return n1 if s(n1) >= s(n2) else n2


def pill(draw, c, text, font):
    l, t, r, b = draw.textbbox((0, 0), text, font=font)
    tw, th = r-l, b-t
    px, py = 36, 22
    x0, y0 = c[0]-tw/2-px, c[1]-th/2-py
    x1, y1 = c[0]+tw/2+px, c[1]+th/2+py
    draw.rounded_rectangle([x0, y0, x1, y1], radius=(y1-y0)/2, fill=INK)
    draw.text((c[0]-tw/2-l, c[1]-th/2-t), text, font=font, fill="white")


def dim(draw, A, B, d, want, label, font, pill_t=0.5, ext_gap=14):
    """Размерная линия параллельно грани A-B, отступ d наружу по нормали want.
    Выносные линии идут от реальных углов A,B к концам размерной линии."""
    (u), L = unit(A, B)
    n = pick_norm(u, want)
    P1 = (A[0]+n[0]*d, A[1]+n[1]*d)
    P2 = (B[0]+n[0]*d, B[1]+n[1]*d)
    if EXT:
        for C, P in ((A, P1), (B, P2)):
            (uc), Lc = unit(C, P)
            draw.line([(C[0]+uc[0]*ext_gap, C[1]+uc[1]*ext_gap),
                       (P[0]+uc[0]*8, P[1]+uc[1]*8)], fill=INK, width=EW)
    draw.line([P1, P2], fill=INK, width=LW)
    for P in (P1, P2):
        draw.ellipse([P[0]-DOT, P[1]-DOT, P[0]+DOT, P[1]+DOT], fill=INK)
    pill(draw, (P1[0]+(P2[0]-P1[0])*pill_t, P1[1]+(P2[1]-P1[1])*pill_t), label, font)


def dim_explicit(draw, P1, P2, anchors, label, font, pill_t=0.5, ext_gap=14):
    """Размерная линия по явным концам P1,P2 (anchors — для опциональных выносных линий)."""
    if EXT:
        for C, P in zip(anchors, (P1, P2)):
            (uc), Lc = unit(C, P)
            draw.line([(C[0]+uc[0]*ext_gap, C[1]+uc[1]*ext_gap),
                       (P[0]-uc[0]*8, P[1]-uc[1]*8)], fill=INK, width=EW)
    draw.line([P1, P2], fill=INK, width=LW)
    for P in (P1, P2):
        draw.ellipse([P[0]-DOT, P[1]-DOT, P[0]+DOT, P[1]+DOT], fill=INK)
    pill(draw, (P1[0]+(P2[0]-P1[0])*pill_t, P1[1]+(P2[1]-P1[1])*pill_t), label, font)


_DRAFTS = {}


def load(tag):
    im = Image.open(f"{DEST}\\dims_white_{tag}.jpg").convert("RGB")
    return im, ImageDraw.Draw(im), ImageFont.truetype(FONT_PATH, 58)


def save_draft(im, tag):
    _DRAFTS[tag] = im; print("draft", tag, im.size)


# ================= FOLDED (по образцу Олега) =================
# длина 377 — прямой линией ПОД диваном во всю ширину, от края до края (выносные линии к углам);
# глубина 180 — короткой диагональю по перспективе у кушетки сверху-справа, параллельно её торцу.
im, d, font = load("folded")
dim(d, (150, 968), (2445, 1035), 175, '+y', "377", font, pill_t=0.55)
dim_explicit(d, (2560, 795), (2668, 652), anchors=((2440, 1035), (2548, 892)),
             label="180", font=font, pill_t=0.5)
save_draft(im, "folded")

# ================= UNFOLDED (по образцу Олега) =================
# ширина спального 174 — прямой линией ПОД платформой во всю ширину (без изменений);
# глубина 198 — короткая диагональ снизу-слева в белом поле, наклон "\" как на референсе Олега.
im, d, font = load("unfolded")
dim(d, (420, 995), (2380, 978), 165, '+y', "174", font, pill_t=0.52)
dim_explicit(d, (95, 720), (310, 1015), anchors=((95, 720), (310, 1015)),
             label="198", font=font, pill_t=0.62)
save_draft(im, "unfolded")


# ================= финальные слайды =================
def finalize(tag, box):
    im = _DRAFTS[tag].convert("RGB").crop(box)
    w = 1500; h = round(im.height*w/im.width)
    im = im.resize((w, h), Image.LANCZOS)
    canvas = Image.new("RGB", (w, h), "white"); canvas.paste(im, (0, 0))
    out = f"{DEST}\\slide_dims_{tag}.jpg"
    canvas.save(out, "JPEG", quality=90, optimize=True)
    print("FINAL", out, canvas.size)


finalize("folded",   (30, 300, 2748, 1380))
finalize("unfolded", (30, 180, 2560, 1330))
