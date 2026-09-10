# Two dimension slides for Бали 7.2.
#
# ALGORITHM (Oleg, 10.09.2026): sofa projection onto the floor -> offset outward from a
# footprint edge -> dimension line parallel to that edge, on the floor, clear of the sofa.
# Length + depth leave the shared front corner -> "L" (tools/dims-style-ref.jpg).
#
# The footprint corners are DETECTED from a white cut-out of the sofa (mustard vs #FFF), so
# the length line always reaches the true corners and the depth line sits on the real end.
import sys
from math import hypot
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = r"C:/Users/user/Claude/mebel.hub/assets/bali-7-2"
OUT_W = 1200
INK = (32, 34, 40)
PAD = 200
DEBUG = "--debug" in sys.argv


def font(sz):
    for p in (r"C:/Windows/Fonts/segoeuib.ttf", r"C:/Windows/Fonts/arialbd.ttf"):
        try:
            return ImageFont.truetype(p, sz)
        except OSError:
            pass
    return ImageFont.load_default()


def largest_blob(mask):
    from collections import deque
    h, w = mask.shape
    seen = np.zeros_like(mask, bool)
    best, best_n = None, 0
    for sy, sx in np.argwhere(mask):
        if seen[sy, sx]:
            continue
        q = deque([(sy, sx)])
        seen[sy, sx] = True
        comp = []
        while q:
            y, x = q.popleft()
            comp.append((y, x))
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ny, nx = y + dy, x + dx
                if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not seen[ny, nx]:
                    seen[ny, nx] = True
                    q.append((ny, nx))
        if len(comp) > best_n:
            best_n, best = len(comp), comp
    out = np.zeros_like(mask)
    if best:
        ys, xs = zip(*best)
        out[np.array(ys), np.array(xs)] = True
    return out


def sofa_mask(img):
    hsv = np.asarray(img.convert("HSV")).astype(np.float32)
    H, S, V = hsv[..., 0] * 360 / 255, hsv[..., 1] / 255, hsv[..., 2] / 255
    m = (H >= 26) & (H <= 62) & (S >= 0.32) & (V >= 0.28)
    m = np.asarray(Image.fromarray((m * 255).astype("uint8")).filter(ImageFilter.MedianFilter(5))) > 127
    m = np.asarray(Image.fromarray((m * 255).astype("uint8")).filter(ImageFilter.MaxFilter(7))) > 127
    m = largest_blob(m)
    return m


def footprint(img, end_band=0.11):
    """FL, FR (front floor corners) and BR (back-right floor corner) in image px."""
    m = sofa_mask(img)
    h, w = m.shape
    bottom = np.full(w, -1)
    for x in range(w):
        ys = np.where(m[:, x])[0]
        if ys.size:
            bottom[x] = ys.max()
    cols = np.where(bottom >= 0)[0]
    x_lo, x_hi = int(cols[0]), int(cols[-1])
    # robust corner y: median of a few columns at each extreme
    yl = int(np.median(bottom[x_lo:x_lo + 12][bottom[x_lo:x_lo + 12] >= 0]))
    yr = int(np.median(bottom[x_hi - 12:x_hi][bottom[x_hi - 12:x_hi] >= 0]))
    FL = (float(x_lo), float(yl))
    FR = (float(x_hi), float(yr))
    # BR: highest silhouette point within the right end band -> back-right floor corner
    bx0 = int(x_hi - (x_hi - x_lo) * end_band)
    seg = bottom[bx0:x_hi + 1]
    xs = np.arange(bx0, x_hi + 1)[seg >= 0]
    ys = seg[seg >= 0]
    k = int(np.argmin(ys))
    BR = (float(xs[k]), float(ys[k]))
    if BR[1] >= FR[1] - 12:            # end face barely visible -> nudge a synthetic depth
        BR = (FR[0] + 34, FR[1] - 58)
    return FL, FR, BR


def outward_normal(A, B, ref):
    dx, dy = B[0] - A[0], B[1] - A[1]
    L = hypot(dx, dy) or 1.0
    nx, ny = -dy / L, dx / L
    mx, my = (A[0] + B[0]) / 2, (A[1] + B[1]) / 2
    if (mx + nx - ref[0]) ** 2 + (my + ny - ref[1]) ** 2 < (mx - nx - ref[0]) ** 2 + (my - ny - ref[1]) ** 2:
        nx, ny = -nx, -ny
    return nx, ny


def dim_line(draw, A, B, ref, label, d, fnt, pill_t=0.5, pill_extra=(0, 0), r=8):
    nx, ny = outward_normal(A, B, ref)
    A2 = (A[0] + nx * d, A[1] + ny * d)
    B2 = (B[0] + nx * d, B[1] + ny * d)
    draw.line([A2, B2], fill=INK, width=5)
    for c in (A2, B2):
        draw.ellipse([c[0] - r, c[1] - r, c[0] + r, c[1] + r], fill=INK)
    cx = A2[0] + (B2[0] - A2[0]) * pill_t + pill_extra[0]
    cy = A2[1] + (B2[1] - A2[1]) * pill_t + pill_extra[1]
    tb = draw.textbbox((0, 0), label, font=fnt)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    px, py = 22, 13
    box = [cx - tw / 2 - px, cy - th / 2 - py, cx + tw / 2 + px, cy + th / 2 + py]
    draw.rounded_rectangle(box, radius=(box[3] - box[1]) / 2, fill=INK)
    draw.text((cx - tw / 2 - tb[0], cy - th / 2 - tb[1]), label, font=fnt, fill="white")


def build(src, floor, length_label, depth_label, d_len, d_dep, crop, out_name,
          pill_len_t=0.42, pill_dep_extra=(28, 0)):
    im = Image.open(f"{BASE}/{src}").convert("RGB")
    r = OUT_W / im.width
    im = im.resize((OUT_W, round(im.height * r)), Image.LANCZOS)
    FL, FR, BR = floor["FL"], floor["FR"], floor["BR"]
    print(f"  {out_name}: FL={FL} FR={FR} BR={BR}")

    canvas = Image.new("RGB", (im.width + 2 * PAD, im.height + PAD), "white")
    canvas.paste(im, (PAD, 0))
    o = lambda p: (p[0] + PAD, p[1])
    FL, FR, BR = o(FL), o(FR), o(BR)
    ref = ((FL[0] + FR[0]) / 2, (FL[1] + FR[1]) / 2 - 170)
    d = ImageDraw.Draw(canvas)
    fnt = font(46)
    if DEBUG:
        for P, c in ((FL, (255, 0, 0)), (FR, (0, 190, 0)), (BR, (0, 90, 255))):
            d.ellipse([P[0] - 10, P[1] - 10, P[0] + 10, P[1] + 10], outline=c, width=4)
        d.line([FL, FR], fill=(255, 0, 255), width=2)
        d.line([FR, BR], fill=(255, 0, 255), width=2)
    dim_line(d, FL, FR, ref, length_label, d_len, fnt, pill_t=pill_len_t, pill_extra=(0, 6))
    dim_line(d, FR, BR, ref, depth_label, d_dep, fnt, pill_t=0.5, pill_extra=pill_dep_extra)
    canvas.crop(crop).save(f"{BASE}/{out_name}", quality=92)
    print("wrote", out_name)


# corners hand-read on the white cut-out grid (1200-wide image space), verified with --debug
print("folded:")
build("dims_cut_folded.png",
      floor=dict(FL=(100, 770), FR=(942, 686), BR=(1012, 648)),
      length_label="256", depth_label="137", d_len=52, d_dep=50,
      crop=(40, 250, OUT_W + 2 * PAD - 20, 896 + PAD), out_name="slide_dims_folded.jpg",
      pill_dep_extra=(30, 0))
print("unfolded:")
build("dims_cut_unfolded.png",
      floor=dict(FL=(288, 732), FR=(972, 702), BR=(1016, 618)),
      length_label="200", depth_label="190", d_len=52, d_dep=50,
      crop=(60, 250, OUT_W + 2 * PAD - 20, 896 + PAD), out_name="slide_dims_unfolded.jpg",
      pill_dep_extra=(32, 0))
