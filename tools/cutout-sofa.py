"""Deterministic mustard-sofa cutout onto solid white, with a short synthetic shadow.
Nano Banana refuses to remove busy warehouse backgrounds; this masks by the velour
colour instead. Usage: python tools/cutout-sofa.py <in> <out> [--pad-bottom N]
"""
import sys
import numpy as np
from PIL import Image, ImageFilter


def largest_blob(mask):
    """Keep only the largest 4-connected component of a bool mask (no scipy)."""
    h, w = mask.shape
    seen = np.zeros_like(mask, dtype=bool)
    best = None
    best_n = 0
    idx = np.argwhere(mask)
    from collections import deque
    for sy, sx in idx:
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
            best_n = len(comp)
            best = comp
    out = np.zeros_like(mask)
    if best:
        ys, xs = zip(*best)
        out[np.array(ys), np.array(xs)] = True
    return out


def fill_enclosed_holes(mask):
    """Fill only background regions with no path to the image border (true interior holes)."""
    h, w = mask.shape
    from collections import deque
    outside = np.zeros_like(mask, dtype=bool)
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if not mask[y, x] and not outside[y, x]:
                outside[y, x] = True
                q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if not mask[y, x] and not outside[y, x]:
                outside[y, x] = True
                q.append((y, x))
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and not mask[ny, nx] and not outside[ny, nx]:
                outside[ny, nx] = True
                q.append((ny, nx))
    return mask | (~outside)


def main():
    src, dst = sys.argv[1], sys.argv[2]
    pad_bottom = 0
    if "--pad-bottom" in sys.argv:
        pad_bottom = int(sys.argv[sys.argv.index("--pad-bottom") + 1])

    im = Image.open(src).convert("RGB")
    W, H = im.size
    # work at reduced res for the mask
    mw = 760
    mh = round(H * mw / W)
    small = im.resize((mw, mh), Image.LANCZOS)
    hsv = np.asarray(small.convert("HSV")).astype(np.float32)
    Hh = hsv[..., 0] * 360.0 / 255.0
    Ss = hsv[..., 1] / 255.0
    Vv = hsv[..., 2] / 255.0
    a = np.asarray(small).astype(np.int16)

    # mustard velour: yellow-orange hue, clearly saturated, not dark.
    # warehouse wood / cardboard / beige walls / brown sofa are all LOW saturation.
    mustard = (Hh >= 30) & (Hh <= 58) & (Ss >= 0.42) & (Vv >= 0.32)
    dark = (a.max(axis=2) <= 82)  # black feet / plinth

    m = np.asarray(Image.fromarray((mustard * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(5))) > 127
    m = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(9))) > 127  # close gaps
    m = largest_blob(m)
    # add dark feet only where they touch the sofa blob
    near = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(15))) > 127
    m = m | (dark & near)
    m = largest_blob(m)
    m = fill_enclosed_holes(m)          # only holes fully surrounded by the blob
    # close ragged edges, then erode inwards so leftover background fringe is trimmed off
    m = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(7))) > 127
    m = fill_enclosed_holes(m)
    m = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(11))) > 127
    m = largest_blob(m)

    alpha_small = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2.2))
    alpha = alpha_small.resize((W, H), Image.LANCZOS)

    # synthetic shadow: mask shifted down a touch, squashed, blurred, faint
    sh = alpha.resize((W, H)).filter(ImageFilter.GaussianBlur(W * 0.012))
    sh_arr = np.asarray(sh).astype(np.float32) / 255.0
    sh_arr = np.roll(sh_arr, int(H * 0.012), axis=0) * 0.28  # short, faint

    canvas = np.ones((H, W, 3), dtype=np.float32)
    canvas *= (1.0 - sh_arr[..., None])          # lay shadow on white
    fg = np.asarray(im).astype(np.float32) / 255.0
    al = np.asarray(alpha).astype(np.float32) / 255.0
    out = fg * al[..., None] + canvas * (1.0 - al[..., None])
    out = (np.clip(out, 0, 1) * 255).astype(np.uint8)

    res = Image.fromarray(out)
    if pad_bottom:
        pad = Image.new("RGB", (W, H + pad_bottom), (255, 255, 255))
        pad.paste(res, (0, 0))
        res = pad
    res.save(dst, quality=94)
    print("wrote", dst, res.size)


if __name__ == "__main__":
    main()
