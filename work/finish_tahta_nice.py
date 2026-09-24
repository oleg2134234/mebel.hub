from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, re

root=Path(__file__).resolve().parents[1]
assets=root/'assets/tahta-nice'
font=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',38)
ink='#292d30'

def measure(draw,a,b,label,center=None):
    draw.line((a,b),fill=ink,width=3)
    for x,y in (a,b): draw.ellipse((x-6,y-6,x+6,y+6),fill=ink)
    x,y=center or ((a[0]+b[0])/2,(a[1]+b[1])/2)
    box=draw.textbbox((0,0),label,font=font); w=box[2]-box[0]+40
    draw.rounded_rectangle((x-w/2,y-31,x+w/2,y+31),radius=28,fill=ink)
    draw.text((x,y-2),label,font=font,fill='white',anchor='mm')

# Fixed two-panel dimensions slide made from the very same gallery photos.
canvas=Image.new('RGB',(1200,1600),'#f3f3f1')
top=Image.open(assets/'real_general.jpg').convert('RGB'); top.thumbnail((900,675))
canvas.paste(top,((1200-top.width)//2,35))
d=ImageDraw.Draw(canvas)
measure(d,(180,690),(1020,690),'1600')
measure(d,(1060,610),(1060,185),'760')
bottom=Image.open(assets/'real_unfolded.jpg').convert('RGB'); bottom.thumbnail((700,700))
bx=(1200-bottom.width)//2; by=820
canvas.paste(bottom,(bx,by))
measure(d,(bx+bottom.width+70,by+20),(bx+bottom.width+70,by+bottom.height-20),'2000')
measure(d,(bx+10,1545),(bx+bottom.width-10,1545),'760')
canvas.save(assets/'slide_dims.jpg',quality=92)

html_path=root/'index.html'; html=html_path.read_text(encoding='utf-8')
def obj(name): return json.loads(re.search(r'const '+name+r' = (.*?);\s*\n',html)[1])
products,images,galleries=(obj(n) for n in ('PRODUCTS','IMAGES','GALLERIES'))
p=next(x for x in products if x['id']==233)
p.update(title='Тахта Найс',category='sofa',dims='1600×760',desc='Компактная тахта-кровать фабрики «Апогей» в бирюзовой велюровой обивке. Габариты 1600×760 мм, спальное место 760×2000 мм. Съёмный подголовник, простроченное сиденье, высокие опоры и бельевой короб в основании.',colorIdx=12)
base='assets/tahta-nice/'
galleries['233']={'title':'Тахта Найс','slides':[
 {'src':base+'slide_interior.jpg','name':'В интерьере','desc':'Интерьерная визуализация по реальному фото: компактная бирюзовая тахта без подлокотников со съёмным подголовником.'},
 {'src':base+'slide_cozy.jpg','name':'Уют','desc':'Визуализация уютного вечера: тахта «Найс» с человеком и питомцем. Форма, цвет и отделка сохранены по референсу.'},
 {'src':base+'slide_dims.jpg','name':'Размеры','desc':'Размеры в миллиметрах. Сверху: габариты 1600×760. Снизу: спальное место 2000×760.'},
 {'src':base+'real_general.jpg','name':'Общий вид','desc':'Реальное фото компактной тахты «Найс» в бирюзовом велюре.'},
 {'src':base+'real_side.jpg','name':'Вид сбоку','desc':'Реальное фото товара: боковой ракурс, съёмный подголовник и высокие опоры.'},
 {'src':base+'real_unfolded.jpg','name':'В разложенном виде','desc':'Реальное фото спального места размером 2000×760 мм.'},
 {'src':base+'real_storage.jpg','name':'Бельевой ящик','desc':'Реальное фото вместительного бельевого ящика в основании тахты.'}
]}
images['233']=base+'slide_interior.jpg'
for name,value in (('PRODUCTS',products),('IMAGES',images),('GALLERIES',galleries)):
    html=re.sub(r'(const '+name+r' = ).*?(;\s*\n)',lambda m:m[1]+json.dumps(value,ensure_ascii=False)+m[2],html,count=1)
html_path.write_text(html,encoding='utf-8')
print('Tахта Найс: 7 slides, required order applied.')
