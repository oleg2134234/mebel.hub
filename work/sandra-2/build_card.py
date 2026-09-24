from pathlib import Path
import json, re, shutil
from PIL import Image, ImageDraw, ImageFont

root = Path(r'C:/Users/user/Claude/mebel.hub')
assets = root / 'assets/sandra-2-dk'
scratch = root / 'work/sandra-2'
font = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 36)
ink = '#292d30'

def line(draw, a, b, text, center=None):
    draw.line([a,b], fill=ink, width=3)
    for x,y in (a,b): draw.ellipse((x-5,y-5,x+5,y+5), fill=ink)
    x,y = center or ((a[0]+b[0])/2,(a[1]+b[1])/2)
    box=draw.textbbox((0,0),text,font=font)
    w=box[2]-box[0]+34
    draw.rounded_rectangle((x-w/2,y-29,x+w/2,y+29),radius=25,fill=ink)
    draw.text((x,y-2),text,font=font,fill='white',anchor='mm')

# Two independent panels, with the same photos used in the gallery.
top=Image.new('RGB',(1200,720),'#f3f3f1')
top.paste(Image.open(assets/'real_general.png').convert('RGB').resize((740,530)),(230,60))
d=ImageDraw.Draw(top)
line(d,(320,475),(870,660),'2460')
line(d,(1000,570),(1080,290),'1065')
top.save(scratch/'dims_folded.png')

bottom=Image.new('RGB',(1200,850),'#f3f3f1')
im=Image.open(assets/'slide_unfolded_supplier.png').convert('RGB')
im.thumbnail((840,652))
bottom.paste(im,(180,70))
d=ImageDraw.Draw(bottom)
line(d,(190,615),(860,825),'2140')
line(d,(990,685),(1110,350),'1500')
bottom.save(scratch/'dims_unfolded.png')
combined=Image.new('RGB',(1200,1590),'#f3f3f1')
combined.paste(top,(0,0)); combined.paste(bottom,(0,740))
combined.save(assets/'slide_dims.jpg',quality=92)

# Delivery media: JPEG as required by the project. Keep originals in scratch.
for p in list(assets.glob('*.png')):
    out=p.with_suffix('.jpg')
    im=Image.open(p).convert('RGB')
    im.thumbnail((1600,1600))
    im.save(out,quality=92)
    shutil.move(str(p),str(scratch/p.name))

page=root/'index.html'
html=page.read_text(encoding='utf-8')
shutil.copy2(page,scratch/'index.before-sandra.html')
def data(name):
    return json.loads(re.search(r'const '+name+r' = (.*?);\s*\n',html).group(1))
products,images,galleries=(data(n) for n in ['PRODUCTS','IMAGES','GALLERIES'])
assert not any('Сандра' in p['title'] for p in products),'Sandra already exists; inspect instead of duplicating'
pid=max(p['id'] for p in products)+1
products.append({'id':pid,'title':'Сандра 2 ДК','category':'sofa','dims':'2460×1065×945','desc':'Прямой диван фабрики «Апогей». Механизм «Тик-так», спальное место 2140×1500 мм. Основание — латы и высокоэластичный ППУ. Три приспинные подушки, цельное сиденье и мягкие подлокотники с кантом. Высота опор — 140 мм.','colorIdx':4})
base='assets/sandra-2-dk/'
def slide(file,name,desc,typ=None):
    s={'src':base+file,'name':name,'desc':desc}
    if typ:s['type']=typ
    return s
slides=[
 slide('slide_interior.jpg','В интерьере','Интерьерная визуализация прямой «Сандры 2» по кадрам исходного видео. Серая обивка, три приспинные подушки и тонкие подлокотники.'),
 slide('slide_cozy.jpg','Уют','Визуализация уютного вечера: отдых с книгой и питомцем. Форма и отделка дивана сохранены по референсу.'),
 slide('slide_dims.jpg','Размеры','Размеры в миллиметрах. Сверху: корпус 2460×1065, высота 945. Снизу: спальное место 2140×1500. Верх — кадр видео, низ — изображение разложенного дивана из карточки поставщика.'),
 slide('video_unfold.mp4','Видео: раскладка «Тик-так»','Реальная демонстрация механизма прямого дивана из исходного ролика. Короткий фрагмент без звука.','video'),
 slide('real_general.jpg','Общий вид','Реальный кадр прямого дивана, 00:12 исходного видео. Качество ограничено разрешением записи 376×640.'),
 slide('real_arm.jpg','Подлокотник и спинка','Реальный крупный план: мягкий подлокотник с кантом и задняя планка, 00:05 исходного видео.'),
 slide('real_fabric.jpg','Обивка и сиденье','Реальный крупный план серой обивки и канта. В видео заявлены латы и высокоэластичный ППУ; это описание наполнения, не технический разрез.'),
 slide('slide_unfolded_supplier.jpg','В разложенном виде','Дополнительное изображение прямой «Сандры 2» из карточки поставщика «АРТ Мебель». Спальное место 2140×1500 мм.'),
 slide('real_bed.jpg','Спальное место','Реальный кадр разложенного прямого дивана из видео, 00:32. Исходный титр подтверждает размер 1500×2140 мм.'),
 slide('slide_practical.jpg','Практичность','Высота опор — 140 мм. Визуализация по реальному крупному плану опор из ролика; пространство под диваном доступно для уборки.')
]
images[str(pid)]=base+'slide_interior.jpg'
galleries[str(pid)]={'title':'Сандра 2 ДК','slides':slides}
for name,value in [('PRODUCTS',products),('IMAGES',images),('GALLERIES',galleries)]:
    html=re.sub(r'(const '+name+r' = ).*?(;\s*\n)',lambda m:m[1]+json.dumps(value,ensure_ascii=False)+m[2],html,count=1)
page.write_text(html,encoding='utf-8')
(scratch/'card.json').write_text(json.dumps({'id':pid,'slides':slides},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'id':pid,'slides':len(slides),'media_bytes':sum(p.stat().st_size for p in assets.iterdir())}))
