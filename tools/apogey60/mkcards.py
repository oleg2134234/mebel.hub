import json,re,sys,os
from PIL import Image
import numpy as np
sys.stdout.reconfigure(encoding='utf-8')
all_=json.load(open('all.json',encoding='utf-8'))
by={x['id']:x['attributes'] for x in all_}
rows=[l.split('|') for l in open('rows.txt',encoding='utf-8').read().strip().split('\n')]
# n|cat|sheetname|webid(primary)|dims|sleepnote
tr=dict(zip("абвгдеёжзийклмнопрстуфхцчшщъыьэюя",["a","b","v","g","d","e","e","zh","z","i","y","k","l","m","n","o","p","r","s","t","u","f","h","c","ch","sh","sch","","y","","e","yu","ya"]))
def slug(t): return re.sub(r'[^a-z0-9]+','-',''.join(tr.get(c,c) for c in t.lower())).strip('-')
ABBR={'МДК','ДК','ДКУ','ДКУ-О','ДКУ-П','ДКУ-ОО','НПБ','ДКУ О'}
def title(s):
    out=[]
    for w in re.split(r'\s+',s.strip()):
        if w.upper() in ABBR: out.append(w.upper().replace(' ','-'))
        elif w=='о': out.append('О')
        elif w.isdigit() or re.match(r'^[\d.\-]+$',w): out.append(w)
        elif w=='-': out.append('-')
        elif w.lower() in ('без','с','на'): out.append(w.lower())
        else: out.append(w[:1].upper()+w[1:].lower())
    t=' '.join(out).replace('Рица Детская','Рица детская')
    t=t.replace('Дку О','ДКУ-О').replace('ДКУ О','ДКУ-О').replace('Клик - Кляк','Клик-Кляк')
    for w in ('Оттоманкой','Боковин','Боковинами','Хромированными'):
        t=t.replace(' '+w,' '+w.lower())
    return t
SW=[("Графит","#4a4a4a"),("Бежевый","#d9c7a8"),("Терракота","#b5603f"),("Синий","#4a5d8a"),("Зелёный","#5c6b45"),("Молочный","#efe8d8"),("Фуксия","#a2578f"),("Пудровый","#8a6f80"),("Мятный","#a9bab8"),("Коньяк","#633925"),("Горчичный","#a5702b"),("Серый","#7c7c7c"),("Изумрудный","#48646a"),("Марсала","#6b4448"),("Сиреневый","#a196b0"),("Мокко","#886957")]
def hexrgb(h): return np.array([int(h[i:i+2],16) for i in (1,3,5)])
def color_idx(wid):
    d=f'src/{wid}'
    fs=sorted(f for f in os.listdir(d) if f[0].isdigit())
    f=[x for x in fs if x.startswith('2.')] or fs
    im=Image.open(f'{d}/{f[0]}').convert('RGBA');im.thumbnail((400,400))
    a=np.array(im).reshape(-1,4)
    px=a[(a[:,3]>250)][:,:3].astype(int)
    px=px[(px.min(1)<225)] if len(px) else px
    if len(px)==0: return 11
    m=np.median(px,axis=0)
    return int(np.argmin([np.linalg.norm(m-hexrgb(c)) for _,c in SW]))
CAT={'Диваны':'sofa','Кресла':'armchair','Кровати':'bed','Матрасы':'mattress'}
cards=[];nid=270
for r in rows:
    n,cat,name,wid,dims,sleep=r
    wid=int(wid);a=by[wid]
    t=title(name)
    adv=[x['name'].strip() for x in (a.get('advantages') or [])]
    advtxt=[]
    for x in adv:
        s=x.lower().replace('х','x') if False else x
        s=s[:1]+s[1:].lower()
        s=re.sub(r'(\d)\s*[хx]\s*(\d)',lambda m:m.group(1)+'×'+m.group(2),s)
        s=re.sub(r'^(Спальное место [\d/]+×\d+)$',lambda m:m.group(1)+' мм',s)
        for ab in ('ппу','нпб','мдф','лдсп','мдк','пвх'): s=re.sub('(?<![а-яa-z])'+ab+'(?![а-яa-z])',ab.upper(),s,flags=re.I)
        advtxt.append(s)
    desc=(a.get('description') or '').strip().replace('\n\n',' ').replace('\n',' ')
    desc=desc.replace(' Доступен к заказу в разных вариантах обивки.','').replace(' Доступен к заказу в разных цветах обивочной ткани.','')
    extra='. '.join(advtxt)
    full=desc+(' '+extra+'.' if extra else '')
    if sleep: full+=' '+sleep
    def advfmt(x):
        x=x.strip().lower()
        x=re.sub(r'(\d)\s*[хx]\s*(\d)',lambda m:m.group(1)+'×'+m.group(2),x)
        x=re.sub(r'^механизм\s+(.*)$',lambda m:'механизм «'+m.group(1).replace('"','').replace('«','').replace('»','').strip()+'»',x)
        for ab in ('нпб','ппу','мдф','лдсп','мдк'): x=re.sub(r'(?<![а-я])'+ab+r'(?![а-я])',ab.upper(),x)
        return x
    advl=[advfmt(x) for x in adv]
    cat0=CAT[cat]
    if cat0=='sofa': hook='Украшает гостиную и раскладывается в спальное место.'
    elif cat0=='armchair': hook='Днём компактное кресло, ночью — спальное место.' if 'кровать' in t.lower() else 'Компактное кресло, подчёркивает стиль комнаты.'
    elif cat0=='bed': hook='Задаёт характер спальни и дарит уют.'
    else: hook='Комфортный сон каждую ночь.'
    cap=((', '.join(advl[:2])+'. ' if advl else '')+hook+' Визуализация.')
    cap=cap[0].upper()+cap[1:]
    cards.append(dict(caption=cap,n=int(n),localId=nid,webId=wid,title=t,category=CAT[cat],dims=dims,desc=re.sub(r'\s+',' ',full).strip(),slug=slug(t),colorIdx=(5 if CAT[cat]=='mattress' else color_idx(wid))))
    nid+=1
json.dump(cards,open('cards.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
for c in cards: print(c['localId'],c['title'],c['category'],c['dims'],SW[c['colorIdx']][0],'|',c['slug'])
