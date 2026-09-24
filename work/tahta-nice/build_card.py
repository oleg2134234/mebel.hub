from pathlib import Path
import json
import re
import shutil

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(r"C:/Users/user/Claude/mebel.hub")
SOURCE = Path(r"C:/Users/user/Downloads/Диваны/Тахта Найс")
ASSETS = ROOT / "assets/tahta-nice"
WORK = ROOT / "work/tahta-nice"

ASSETS.mkdir(parents=True, exist_ok=True)
WORK.mkdir(parents=True, exist_ok=True)

FILES = {
    "f5ab4c1a-a4e2-4abf-a53f-3c69b95cf2cc.jfif": "real_general.jpg",
    "c79ff170-cfce-4872-a966-7816add36007.jfif": "real_side.jpg",
    "686f23b4-ecc9-4afe-94d7-68281647dca6.jfif": "real_unfolded.jpg",
    "9b2a09e9-c454-4caa-b046-75ff1089eb98.jfif": "real_storage.jpg",
    "45675467856.png": "supplier_card.jpg",
}

for original, output in FILES.items():
    image = Image.open(SOURCE / original).convert("RGB")
    image.thumbnail((1800, 1800), Image.Resampling.LANCZOS)
    image.save(ASSETS / output, quality=92, optimize=True)


def cover(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    return ImageOps.fit(image.convert("RGB"), size, Image.Resampling.LANCZOS)


canvas = Image.new("RGB", (1200, 1500), "#f4f2ee")
draw = ImageDraw.Draw(canvas)
title_font = ImageFont.truetype(r"C:/Windows/Fonts/arialbd.ttf", 44)
label_font = ImageFont.truetype(r"C:/Windows/Fonts/arialbd.ttf", 38)
small_font = ImageFont.truetype(r"C:/Windows/Fonts/arial.ttf", 27)
ink = "#263238"
accent = "#2f7f86"

draw.text((70, 55), "ТАХТА НАЙС", font=title_font, fill=ink)
draw.text((70, 112), "компактная тахта-кровать", font=small_font, fill="#687478")

folded = cover(Image.open(ASSETS / "real_general.jpg"), (1060, 570))
canvas.paste(folded, (70, 175))
draw.rounded_rectangle((70, 675, 500, 730), radius=26, fill=ink)
draw.text((285, 702), "1600 × 760 мм", font=label_font, fill="white", anchor="mm")

unfolded = cover(Image.open(ASSETS / "real_unfolded.jpg"), (1060, 570))
canvas.paste(unfolded, (70, 825))
draw.rounded_rectangle((70, 1325, 520, 1380), radius=26, fill=accent)
draw.text((295, 1352), "760 × 2000 мм", font=label_font, fill="white", anchor="mm")
draw.text((70, 1415), "Габариты / спальное место", font=small_font, fill="#687478")
canvas.save(ASSETS / "slide_dims.jpg", quality=94, optimize=True)

page = ROOT / "index.html"
html = page.read_text(encoding="utf-8")


def data(name: str):
    match = re.search(r"const " + name + r" = (.*?);\s*\n", html)
    if not match:
        raise RuntimeError(f"Не найден блок {name}")
    return json.loads(match.group(1))


products, images, galleries = (data(name) for name in ("PRODUCTS", "IMAGES", "GALLERIES"))
if any(product["title"] == "Тахта Найс" for product in products):
    raise RuntimeError("Карточка «Тахта Найс» уже существует")

product_id = max(product["id"] for product in products) + 1
products.append({
    "id": product_id,
    "title": "Тахта Найс",
    "category": "sofa",
    "dims": "1600×760",
    "desc": "Компактная тахта-кровать фабрики «Апогей» в бирюзовой велюровой обивке. Габариты 1600×760 мм, спальное место 760×2000 мм. Мягкий съёмный подголовник, простроченное сиденье, высокие опоры и вместительный бельевой короб в основании.",
    "colorIdx": 12,
})

base = "assets/tahta-nice/"
slides = [
    {"src": base + "real_general.jpg", "name": "Общий вид", "desc": "Реальное фото компактной тахты «Найс» в бирюзовом велюре."},
    {"src": base + "slide_dims.jpg", "name": "Размеры", "desc": "Габариты: 1600×760 мм. Спальное место: 760×2000 мм."},
    {"src": base + "real_side.jpg", "name": "Вид сбоку", "desc": "Реальное фото товара, боковой ракурс и высокие опоры."},
    {"src": base + "real_unfolded.jpg", "name": "Спальное место", "desc": "Тахта в разложенном виде, спальное место 760×2000 мм."},
    {"src": base + "real_storage.jpg", "name": "Практичность", "desc": "Вместительный бельевой короб в основании тахты."},
    {"src": base + "supplier_card.jpg", "name": "Карточка поставщика", "desc": "Исходная карточка поставщика с подтверждёнными размерами модели."},
]
images[str(product_id)] = base + "real_general.jpg"
galleries[str(product_id)] = {"title": "Тахта Найс", "slides": slides}

shutil.copy2(page, WORK / "index.before-tahta-nice.html")
for name, value in (("PRODUCTS", products), ("IMAGES", images), ("GALLERIES", galleries)):
    html = re.sub(
        r"(const " + name + r" = ).*?(;\s*\n)",
        lambda match: match.group(1) + json.dumps(value, ensure_ascii=False) + match.group(2),
        html,
        count=1,
    )

page.write_text(html, encoding="utf-8")
(WORK / "card.json").write_text(
    json.dumps({"id": product_id, "title": "Тахта Найс", "slides": slides}, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
print(json.dumps({"id": product_id, "slides": len(slides), "assets": sorted(FILES.values()) + ["slide_dims.jpg"]}, ensure_ascii=False))
