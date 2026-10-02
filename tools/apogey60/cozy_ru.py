"""Русские подписи к слайдам «Уют»: «Тёплый вечер на диване: мужчина с белой кошкой. Визуализация.»"""
WHO = {
 "A young woman": "девушка", "A man in his thirties": "мужчина", "A girl about 8 years old": "девочка", "A woman in her forties": "женщина",
 "An elderly man with glasses": "пожилой мужчина", "A boy about 9 years old": "мальчик", "A teenage girl": "девочка-подросток",
 "A man in his forties": "мужчина", "An elderly woman with grey hair": "пожилая женщина", "A teenage boy": "подросток",
 "A woman in her thirties": "женщина", "A bearded man in his thirties": "мужчина с бородой", "A child about 7 years old": "ребёнок",
 "A couple, a man and a woman in their thirties": "пара", "A couple, a man and a woman in their forties": "пара",
 "Two sisters about 8 and 12 years old": "две сестры", "Two sisters about 9 and 12 years old": "две сестры",
 "A father and his son about 8 years old": "отец с сыном", "A father and his son about 7 years old": "отец с сыном",
 "A father and his daughter about 9 years old": "папа с дочкой", "A mother and her son about 6 years old": "мама с сыном",
 "A mother and her daughter about 7 years old": "мама с дочкой", "A mother and her daughter about 6 years old": "мама с дочкой",
 "A grandmother and her granddaughter about 7 years old": "бабушка с внучкой", "A grandmother and her granddaughter about 8 years old": "бабушка с внучкой",
 "Two brothers about 7 and 10 years old": "два брата", "Two brothers about 8 and 10 years old": "два брата", "Two boys about 8 and 10 years old": "двое мальчишек",
}
PET = {  # творительный падеж
 "a ginger cat": "рыжим котом", "a white rabbit": "белым кроликом", "a grey lop-eared rabbit": "серым вислоухим кроликом", "a black cat": "чёрным котом",
 "a cream labrador puppy": "щенком лабрадора", "a guinea pig": "морской свинкой", "a blue budgerigar": "голубым волнистым попугайчиком",
 "a calico cat": "пёстрой кошкой", "a grey British shorthair cat": "британской кошкой", "a Siamese cat": "сиамской кошкой", "a pug": "мопсом",
 "a ginger kitten": "рыжим котёнком", "a Maine Coon cat": "кошкой мейн-кун", "a black-and-white cat": "чёрно-белой кошкой", "a beagle": "биглем",
 "a border collie": "бордер-колли", "a tabby kitten": "полосатым котёнком", "a small poodle": "маленьким пуделем", "a cockatiel": "попугаем корелла",
 "a fluffy white kitten": "пушистым белым котёнком", "a corgi": "корги", "a grey tabby cat": "серым полосатым котом", "a dachshund": "таксой",
 "a fluffy white cat": "пушистой белой кошкой", "a French bulldog": "французским бульдогом", "a beagle puppy": "щенком бигля",
}
PLACE = {"sofa": "на диване", "armchair": "в кресле", "bed": "на кровати"}


def desc(c):
    w, p = WHO[c["who"]], PET[c["pet"]]
    joiner = " и " if " с " in w else " с "
    return f"Тёплый вечер {PLACE[c['kind']]}: {w}{joiner}{p}. Визуализация."
