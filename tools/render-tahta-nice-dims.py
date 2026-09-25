"""Render the approved one-photo Tahta Nice dimensions exception as one JPG."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "tahta-nice"
SOURCE = ASSETS / "dims_folded_white-v1.png"
OUTPUT = ASSETS / "slide_dims-v3.jpg"
INK = "#282d2f"


canvas = Image.new("RGB", (1200, 900), "white")
sofa = Image.open(SOURCE).convert("RGB").resize((960, 720), Image.Resampling.LANCZOS)
canvas.paste(sofa, (120, 4))
draw = ImageDraw.Draw(canvas)
font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 38)


def dimension(a, b, label, center):
    draw.line((a, b), fill=INK, width=4)
    for x, y in (a, b):
        draw.ellipse((x - 7, y - 7, x + 7, y + 7), fill=INK)
    box = draw.textbbox((0, 0), label, font=font)
    width = box[2] - box[0] + 42
    x, y = center
    draw.rounded_rectangle((x - width / 2, y - 32, x + width / 2, y + 32), radius=32, fill=INK)
    draw.text((x, y + 1), label, font=font, fill="white", anchor="mm")


# Lines follow the visible front and side floor-projection edges.
dimension((115, 680), (1025, 764), "160", (570, 722))
dimension((997, 218), (1129, 618), "76", (1063, 418))
canvas.save(OUTPUT, quality=94, subsampling=0)

for path in (ROOT / "index.html", ROOT / "work" / "tahta-nice" / "card.json"):
    text = path.read_text(encoding="utf-8")
    text = text.replace("assets/tahta-nice/slide_dims-v3.svg", "assets/tahta-nice/slide_dims-v3.jpg")
    path.write_text(text, encoding="utf-8")

old_svg = ASSETS / "slide_dims-v3.svg"
if old_svg.exists():
    old_svg.unlink()

print(OUTPUT)
