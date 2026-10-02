"""Слайды «Уют» для 57 карточек Apogey: данные по карточкам + сборка cozy-lib.js (шаблоны + код для консоли Syntx).
Требования пользователя (02.10.2026): интерьер и сюжет на каждом слайде свои; на слайдах мужчины, женщины и дети, кошки и собаки;
стиль интерьера отличается, но сочетается с мебелью; диван/кровать целиком в кадре, без обрезания; уже сделанные слайды остаются.
python cozy_build.py           -> cozy-cards.json + cozy-lib.js
python cozy_build.py patch ID… -> JS-патч window.CARDS для перечисленных карточек (вставлять в консоль Syntx после cozy-lib.js)"""
import json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(HERE + "/../..")
sj = open(HERE + "/setup.js", encoding="utf-8").read(); AP, _ = json.JSONDecoder().raw_decode(sj, sj.find("window.AP=") + 10)
sofa = json.load(open(HERE + "/dims-picks.json", encoding="utf-8"))
h = open(ROOT + "/index.html", encoding="utf-8").read(); G, _ = json.JSONDecoder().raw_decode(h, h.index("const GALLERIES = ") + 18)

COLOR = {
 270: "medium warm grey fabric with cream-ivory side panels", 271: "mustard-yellow fabric with dark brown wooden side panels",
 272: "slate blue-grey fabric with cream-ivory side panels", 273: "dark chocolate-brown crushed velvet",
 274: "cornflower blue velvet with dark wooden armrest tops", 275: "khaki olive-beige fabric with dark wooden armrest tops",
 276: "light warm grey fabric", 277: "sage mint-green velvet with dark wooden armrest tops", 278: "sand-beige taupe fabric with dark wooden armrest tops",
 279: "rich royal blue velvet", 280: "slate steel-grey fabric", 281: "soft aqua mint-turquoise fabric",
 282: "cream-ecru fabric", 283: "medium grey fabric", 284: "medium grey fabric", 285: "medium grey fabric",
 286: "blush powder-beige fabric", 287: "dark graphite-grey velvet", 288: "taupe mocha-grey fabric", 289: "steel blue-grey fabric",
 290: "raspberry burgundy-rose fabric", 291: "olive khaki-green fabric", 292: "mustard-yellow fabric", 293: "dusty mauve-pink fabric",
 294: "deep burgundy wine-red fabric", 296: "camel sand-beige fabric with dark wooden armrest tops", 297: "rust terracotta-red velvet", 298: "grey-blue velvet",
 301: "dusty pink velvet", 302: "deep navy-blue fabric", 303: "cream-milk fabric", 304: "latte tan-beige fabric", 305: "sage green fabric",
 306: "chocolate-brown fabric", 307: "slate blue-grey velvet", 308: "aqua turquoise-blue velvet",
 309: "sage green velvet", 310: "cobalt royal-blue velvet", 311: "greige taupe fabric", 312: "graphite-grey velvet",
 313: "light sky-blue upholstery on the seats and backrest with a grey base", 314: "soft lilac-pink upholstery on the seats and backrest with a grey base",
 315: "greige sage-grey fabric", 316: "dusty rose-mocha fabric", 317: "olive sage-green fabric", 318: "petrol blue-teal grey fabric", 319: "mustard-yellow fabric", 320: "mottled marble-grey velvet",
 321: "denim blue-grey fabric", 322: "cream-ecru fabric", 323: "dusty mauve-pink velvet", 324: "dark slate blue-grey fabric",
 325: "raspberry red fabric", 326: "emerald green fabric", 327: "dark taupe-grey velvet", 328: "light blue-grey velvet", 329: "mid grey velvet",
}
ARM = {271, 275, 281}
CORNER = {277, 279, 280, 283, 284, 285, 297, 309, 313, 314, 315, 317, 320, 322}
STRAIGHT = "This is a straight sofa with exactly the same number of seats and backrest sections as in Image 1: do not turn it into a corner sofa and do not add modules."
CORNERS = "This is a corner / modular sofa: do not mirror, flip, extend or rearrange its modules; the ottoman / chaise keeps the same side, shape and size as in Image 1."
ARMCH = "This is a single armchair: do not turn it into a sofa."

# стиль интерьера — подобран под цвет и характер мебели, все разные
STYLE = {
 # диваны и кресла
 270: "Scandinavian (light oak floor, white walls, linen floor lamp, birch branches in a vase)",
 271: "mid-century modern (walnut sideboard, tapered-leg side table, tulip lamp, teak floor)",
 272: "classic-modern (wall moldings, herringbone parquet, brass table lamp, velvet curtains)",
 273: "dark and moody (charcoal walls, picture rail with framed art, candles, brass lamp)",
 274: "coastal (whitewashed wood walls, pale blue accents, jute rug, rope table lamp, seashells)",
 275: "Scandinavian forest (pale pine paneling, green plants, wool throw, window view of pine trees)",
 276: "japandi (low wooden coffee table, paper lantern lamp, ceramic vase with dry branches)",
 277: "pastel modern (soft pink and sage color-blocked walls, arched mirror, ceramic table lamp)",
 278: "warm Tuscan (stone wall, wooden beams, terracotta pots, candles)",
 279: "Parisian apartment (tall windows, ornate cornice, herringbone floor, gilded mirror, brass sconces)",
 280: "urban penthouse (floor-to-ceiling windows with evening city lights, sleek arc lamp)",
 281: "retro seventies (orange and brown accents, rattan, sunburst mirror, shag rug)",
 282: "Italian modern (fluted wood wall panels, marble coffee table, sculptural floor lamp)",
 283: "contemporary gallery (white walls with large abstract canvases, track lighting, polished concrete floor)",
 284: "neoclassic (soft grey wall panels, crystal-drop lamp, cream curtains, parquet)",
 285: "modern minimal (microcement wall, built-in shelves with a few objects, slim black floor lamp)",
 296: "warm-modern earthy (beige plaster walls, travertine side table, arched brass floor lamp)",
 297: "Moroccan-inspired (patterned tiles, lantern lamps, kilim rug, brass tray table)",
 298: "English country (chintz curtains, wood paneling, brass reading lamp, patterned rug)",
 309: "country house (wide plank floor, whitewashed beams, window to the garden at dusk, wildflowers)",
 313: "Scandi-boho (white walls, macrame wall hanging, pampas grass, sheepskin throw)",
 314: "bookish eclectic (floor-to-ceiling bookshelves, rolling ladder, reading lamp, Persian rug)",
 315: "Japanese minimal (low shoji-style screen, bonsai, paper floor lamp, natural fiber rug)",
 316: "boho-cottage (rattan accents, woven basket with blankets, many plants)",
 317: "cozy cabin (wood-paneled walls, stone fireplace with a gentle fire, plaid blanket, warm lamp)",
 318: "Mediterranean (white lime-washed walls, terracotta tiles, arched niche, olive tree in a pot)",
 319: "art-deco (deep green walls, brass accents, fluted glass lamp, geometric rug)",
 320: "industrial-chic (concrete wall, steel-framed window, Edison bulb pendant, leather pouf)",
 321: "modern farmhouse (shiplap wall, wooden ceiling beams, wrought-iron lamp, woven rug)",
 322: "airy attic (sloped wood-beam ceiling, skylight with dusk sky, string lights)",
 323: "vintage library (dark wood shelves, green banker lamp, leather-bound books)",
 324: "loft (soft brick wall, black metal floor lamp, wooden floor, large leafy plant)",
 325: "hygge winter evening (many candles, wool blankets, snowy window, warm string lights)",
 326: "modern bohemian (terracotta color-blocked wall, cane furniture, hanging plants)",
 # кровати (спальни)
 286: "warm-modern earthy (beige plaster walls, travertine bedside table, arched mirror)",
 287: "dark and moody (deep navy walls, framed prints, candles, brass lamp)",
 288: "Italian modern (fluted panels, marble nightstand, sculptural lamp)",
 289: "coastal (whitewashed boards, pale blue accents, jute rug, rope lamp)",
 290: "classic-modern (wall moldings, herringbone parquet, brass sconces, velvet curtains)",
 291: "cozy cabin (wood-paneled walls, plaid throw, warm lantern, wool rug)",
 292: "mid-century modern (walnut nightstand with tapered legs, sunburst mirror, teak floor)",
 293: "romantic (sheer curtains, fairy lights, pampas grass, soft rug)",
 294: "art-deco (deep green wall, brass lamp, geometric rug)",
 301: "Scandinavian (light oak floor, white walls, linen curtains, paper table lamp)",
 302: "loft (soft brick wall, black metal lamp, wooden floor)",
 303: "japandi (low wooden bedside table, paper lantern, vase with dry branches)",
 304: "boho (rattan pendant lamp, macrame, many plants, woven basket)",
 305: "garden cottage (window with a garden at dusk, wildflowers, wicker nightstand)",
 306: "modern farmhouse (shiplap walls, wooden ceiling beams, iron lamp, woven rug)",
 307: "industrial (concrete wall, steel-framed window, bulb pendant)",
 308: "soft pastel Scandinavian children's room (toys on a shelf, a small rug)",
 310: "modern minimal (microcement wall, slim shelf, simple sculptural lamp)",
 311: "attic bedroom (sloped beamed ceiling, skylight with dusk sky, string lights)",
 312: "library bedroom (bookshelf wall, reading lamp, a plant)",
 327: "retro seventies (orange and brown accents, rattan, sunburst mirror)",
 328: "pastel (blush and sage walls, arched mirror, ceramic lamp)",
 329: "French country (toile curtains, painted nightstand, brass candlesticks)",
}

from cozy_scenes import ACT, SC, PP, pet_kind
DETAIL = {}
for i in (286, 287): DETAIL[i] = "The headboard is a plain flat rectangular panel with a thin piped border — NO tufting, NO square quilting, NO buttons; the base is plain upholstery."
for i in (288, 289, 290, 291): DETAIL[i] = "The tall headboard has vertical and rectangular stitched panels in its upper part exactly as in Image 1; no other quilting."
for i in (292, 293, 294): DETAIL[i] = "The headboard has rectangular block panels arranged like bricks exactly as in Image 1; no other quilting."
for i in (301, 302, 303, 304, 305, 306, 307): DETAIL[i] = "The headboard has a pattern of thin diagonal geometric lines (triangular facets) exactly as in Image 1."
for i in (301, 303, 305, 307): DETAIL[i] += " This is a narrow single bed for one person."
DETAIL[308] = "This is a child's corner bed with a high L-shaped back and side panel with geometric diagonal lines, exactly as in Image 1."
for i in (310, 311, 312): DETAIL[i] = "The headboard has a hexagonal honeycomb panel pattern exactly as in Image 1."
for i in (327, 328, 329): DETAIL[i] = "The headboard has a chevron diagonal stitching pattern exactly as in Image 1."


def build():
    cards = {}
    for i in sorted(COLOR):
        kind = "bed" if AP[str(i)][0] == "b" else ("armchair" if i in ARM else "sofa")
        ref = sofa[str(i)]["urls"][0] if str(i) in sofa and "urls" in sofa[str(i)] else "/uploads/" + AP[str(i)][1]
        who, act, pet = SC[i]
        k = PP[pet_kind(pet)]; pp = k[1] if kind == "bed" else k[0]
        action = ACT[act].format(w=who + (" in cozy home clothes" if not who.startswith(("A couple", "Two", "A mother", "A father", "A grandmother")) else " in cozy home clothes"), p=pet, pp=pp, pp_arm=k[2])
        config = DETAIL.get(i, "") if kind == "bed" else (ARMCH if kind == "armchair" else (CORNERS if i in CORNER else STRAIGHT))
        cards[i] = dict(kind=kind, title=G[str(i)]["title"], slug=G[str(i)]["slides"][0]["src"].split("/")[1], ref=ref, color=COLOR[i],
                        style=STYLE[i], who=who, act=act, pet=pet, action=action, config=config)
    return cards

RUNTIME = open(HERE + "/cozy-runtime.js", encoding="utf-8").read() if os.path.exists(HERE + "/cozy-runtime.js") else ""
if __name__ == "__main__":
    cards = build()
    if len(sys.argv) > 1 and sys.argv[1] == "patch":
        ids = [int(a) for a in sys.argv[2:]]
        P = {i: [cards[i]["kind"][0], cards[i]["ref"].replace("/uploads/", ""), cards[i]["color"], cards[i]["style"], cards[i]["action"], cards[i]["config"]] for i in ids}
        print("Object.assign(window.CARDS=window.CARDS||{}," + json.dumps(P, ensure_ascii=False, separators=(",", ":")) + ");")
    else:
        json.dump(cards, open(HERE + "/cozy-cards.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        tpl = {k: open(HERE + "/cozy-prompt-%s.tpl.txt" % k, encoding="utf-8").read() for k in ("sofa", "bed")}
        js = "window.CTPL=" + json.dumps(tpl, ensure_ascii=False) + ";" + chr(10) + RUNTIME
        open(HERE + "/cozy-lib.js", "w", encoding="utf-8").write(js)
        print(len(cards), "cards;", sum(1 for c in cards.values() if c["kind"] == "bed"), "beds;", len(js), "bytes")
        print("styles unique:", len({c["style"] for c in cards.values()}), "| scenes unique (act,who,pet):", len({(c["act"], c["who"], c["pet"]) for c in cards.values()}))
