"""Сюжеты слайдов «Уют»: у каждой карточки свой сюжет, свои люди (мужчины, женщины, дети; иногда двое) и своё животное (кошки, кролики, попугаи, морские свинки, собаки).
Требования пользователя 02.10.2026: плед не использовать; сюжет «питомец на пледе» не повторять; можно двух людей, в том числе детей."""

# {w} — человек/люди, {p} — питомец, {pp} — поза питомца (зависит от вида и места: диван/кровать/кресло)
ACT = {
 # --- один человек, диван ---
 "tea": "{w} is sipping tea from a large mug held in both hands, looking dreamily at the window, while {p} {pp}.",
 "laptop": "{w} is working on a laptop resting on the knees with a mug nearby, while {p} {pp}.",
 "game": "{w} is playing a video game with a controller in both hands, laughing, while {p} {pp}.",
 "movie": "{w} is watching a movie on a TV out of frame with a remote in one hand and a bowl of popcorn on the lap, while {p} {pp}.",
 "music": "{w} is listening to music with large headphones and eyes closed, while {p} {pp}.",
 "puzzle": "{w} is doing a jigsaw puzzle on a lap tray, while {p} {pp}.",
 "knit": "{w} is knitting a scarf with a basket of yarn beside them, while {p} watches the yarn with great interest.",
 "phone": "{w} is relaxing with a smartphone in hand, smiling at the screen, while {p} {pp}.",
 "tablet": "{w} is watching something on a tablet propped on the knees, while {p} {pp}.",
 "snack": "{w} is enjoying a small plate of snacks and a cup of cocoa, while {p} {pp}.",
 "homework": "{w} is doing homework with an open notebook on the lap, while {p} {pp}.",
 "guitar": "{w} is softly playing an acoustic guitar, while {p} {pp}.",
 "selfie": "{w} is taking a cheerful selfie with {p} snuggled up next to them.",
 "nap": "{w} is dozing off with eyes closed and a cushion under the head, while {p} {pp}.",
 "cuddle": "{w} is cuddling and gently stroking {p}, who sits on the lap, while looking out of the window at the evening.",
 "stretch": "{w} is relaxing with arms behind the head, legs stretched out and eyes closed, while {p} {pp}.",
 "play": "{w} is laughing and dangling a small toy for {p}, who sits on the seat next to them eagerly watching it.",
 "crossword": "{w} is solving a crossword with a pencil, while {p} {pp}.",
 "reading": "{w} is reading a book, while {p} {pp}.",  # только для уже сделанных 274 и 296
 # --- кресла ---
 "arm_crossword": "{w} is solving a crossword with a pencil, glasses on, while {p} {pp_arm}.",
 "arm_draw": "{w} is sitting comfortably with a sketchbook and colored pencils, while {p} {pp_arm}.",
 "arm_story": "{w} is holding a picture book open and showing it to {p}, who sits on their lap.",
 # --- двое, диван ---
 "f_book": "{w} are sitting together sharing a picture book, while {p} {pp}.",
 "f_game": "{w} are playing a video game together with controllers, laughing, while {p} {pp}.",
 "f_movie": "{w} are watching a movie together with a bowl of popcorn between them, while {p} {pp}.",
 "f_draw": "{w} are drawing together in sketchbooks with colored pencils, while {p} {pp}.",
 "f_cuddle": "{w} are cuddling up close and laughing, while {p} {pp}.",
 "f_tea": "{w} are chatting over cups of tea and cocoa, while {p} {pp}.",
 "f_board": "{w} are playing a card game on a small tray between them, while {p} {pp}.",
 # --- кровати, один человек ---
 "bed_tablet": "{w} is propped up on the pillows watching a series on a tablet, while {p} {pp}.",
 "bed_laptop": "{w} is sitting up with a laptop on the knees, working late, while {p} {pp}.",
 "bed_sleepy": "{w} is lying on the side under the duvet, sleepy, hugging a pillow, while {p} {pp}.",
 "bed_diary": "{w} is sitting cross-legged writing in a diary with a pen, while {p} {pp}.",
 "bed_play": "{w} is sitting cross-legged and laughing, playing with {p} using a small toy.",
 "bed_music": "{w} is lying on the back with headphones on and eyes closed, while {p} {pp}.",
 "bed_phone": "{w} is sitting up with a smartphone, smiling at the screen, while {p} {pp}.",
 "bed_tea": "{w} is sitting up with a mug in both hands, looking sleepily at the window, while {p} {pp}.",
 "bed_draw": "{w} is sitting cross-legged drawing in a sketchbook, while {p} {pp}.",
 "bed_stretch": "{w} is stretching with arms up and yawning, while {p} {pp}.",
 "bed_book": "{w} is sitting up in bed reading a book with glasses on, while {p} {pp}.",
 "bed_knit": "{w} is sitting up in bed knitting, with a ball of yarn nearby, while {p} watches the yarn with great interest.",
 "bed_story": "{w} is sitting on the bed with a teddy bear and a picture book, while {p} {pp}.",
 # --- кровати, двое ---
 "fb_story": "{w} are sitting up in bed — one reads a bedtime story aloud from a picture book to the other, while {p} {pp}.",
 "fb_giggle": "{w} are sitting cross-legged on the bed whispering and giggling, while {p} {pp}.",
 "fb_tablet": "{w} are propped up on the pillows watching cartoons on a tablet together, while {p} {pp}.",
}

# id: (кто, сюжет, питомец) — все 57; 274, 296, 301 уже сделаны (оставляем как есть, сюжет «чтение» в записи для истории)
SC = {
 270: ("A young woman", "tea", "a ginger cat"),
 271: ("An elderly man with glasses", "arm_crossword", "a white rabbit"),
 272: ("A couple, a man and a woman in their thirties", "f_movie", "a grey lop-eared rabbit"),
 273: ("A bearded man in his thirties", "game", "a black cat"),
 274: ("A woman in her thirties", "reading", "a cream labrador puppy"),
 275: ("A teenage girl", "arm_draw", "a guinea pig"),
 276: ("A teenage boy", "music", "a blue budgerigar"),
 277: ("Two sisters about 8 and 12 years old", "f_draw", "a calico cat"),
 278: ("An elderly woman with grey hair", "knit", "a grey British shorthair cat"),
 279: ("A woman in her thirties", "phone", "a Siamese cat"),
 280: ("A father and his son about 8 years old", "f_game", "a pug"),
 281: ("A girl about 8 years old", "arm_story", "a ginger kitten"),
 282: ("A teenage girl", "selfie", "a Maine Coon cat"),
 283: ("A grandmother and her granddaughter about 7 years old", "f_book", "a grey lop-eared rabbit"),
 284: ("A woman in her forties", "snack", "a black-and-white cat"),
 285: ("Two brothers about 7 and 10 years old", "f_board", "a tabby kitten"),
 296: ("A man in his thirties", "reading", "a fluffy white cat"),
 297: ("A mother and her son about 6 years old", "f_cuddle", "a small poodle"),
 298: ("An elderly man with glasses", "guitar", "a cockatiel"),
 309: ("A mother and her daughter about 7 years old", "f_book", "a fluffy white kitten"),
 313: ("A young woman", "music", "a ginger cat"),
 314: ("A man in his thirties", "snack", "a corgi"),
 315: ("A woman in her forties", "nap", "a grey tabby cat"),
 316: ("A father and his daughter about 9 years old", "f_board", "a beagle puppy"),
 317: ("A teenage boy", "laptop", "a black cat"),
 318: ("A bearded man in his thirties", "guitar", "a Siamese cat"),
 319: ("An elderly woman with grey hair", "tablet", "a white rabbit"),
 320: ("A man in his forties", "stretch", "a Maine Coon cat"),
 321: ("A couple, a man and a woman in their forties", "f_tea", "a calico cat"),
 322: ("A young woman", "cuddle", "a grey lop-eared rabbit"),
 323: ("A teenage girl", "phone", "a ginger cat"),
 324: ("Two boys about 8 and 10 years old", "f_movie", "a dachshund"),
 325: ("A girl about 8 years old", "homework", "a guinea pig"),
 326: ("A woman in her forties", "tea", "a grey British shorthair cat"),
 286: ("A woman in her forties", "bed_diary", "a fluffy white cat"),
 287: ("A man in his thirties", "bed_laptop", "a black cat"),
 288: ("Two sisters about 9 and 12 years old", "fb_giggle", "a grey lop-eared rabbit"),
 289: ("An elderly man with glasses", "bed_book", "a grey tabby cat"),
 290: ("A teenage girl", "bed_music", "a ginger cat"),
 291: ("A bearded man in his thirties", "bed_phone", "a pug"),
 292: ("A father and his son about 7 years old", "fb_story", "a tabby kitten"),
 293: ("A woman in her thirties", "bed_tea", "a Siamese cat"),
 294: ("A man in his forties", "bed_stretch", "a Maine Coon cat"),
 301: ("A girl about 8 years old", "bed_book", "a grey tabby cat"),
 302: ("A grandmother and her granddaughter about 8 years old", "fb_story", "a grey British shorthair cat"),
 303: ("A teenage boy", "bed_draw", "a black-and-white cat"),
 304: ("A mother and her daughter about 6 years old", "fb_story", "a French bulldog"),
 305: ("A young woman", "bed_diary", "a calico cat"),
 306: ("A couple, a man and a woman in their thirties", "fb_tablet", "a white rabbit"),
 307: ("A boy about 9 years old", "bed_play", "a fluffy white kitten"),
 308: ("A child about 7 years old", "bed_story", "a ginger kitten"),
 310: ("A woman in her thirties", "bed_laptop", "a grey tabby cat"),
 311: ("A man in his forties", "bed_sleepy", "a ginger cat"),
 312: ("A teenage girl", "bed_phone", "a guinea pig"),
 327: ("A young woman", "bed_tea", "a black cat"),
 328: ("An elderly woman with grey hair", "bed_book", "a calico cat"),
 329: ("Two brothers about 8 and 10 years old", "fb_tablet", "a beagle"),
}


def pet_kind(p):
    p = p.lower()
    if any(k in p for k in ("budgerigar", "cockatiel", "parrot")): return "bird"
    if "rabbit" in p: return "rabbit"
    if "guinea pig" in p: return "gp"
    if any(k in p for k in ("pug", "poodle", "dachshund", "corgi", "beagle", "bulldog", "labrador", "retriever", "terrier", "collie", "spitz", "husky")): return "dog"
    return "cat"


# поза питомца: диван / кровать / кресло
PP = {
 "cat": ("sleeps curled up beside them", "sleeps curled up at the foot of the bed", "sleeps curled up on their lap"),
 "dog": ("lies stretched out beside them", "lies at the foot of the bed", "rests its head on their lap"),
 "rabbit": ("sits calmly beside them, nose twitching", "sits calmly at the foot of the bed", "sits calmly on their lap"),
 "gp": ("sits on their lap", "sits on the pillow beside them", "sits on their lap"),
 "bird": ("perches on their shoulder", "perches on the bedside table", "perches on the armrest"),
}
