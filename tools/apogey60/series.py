import re,sys,json
sys.stdout.reconfigure(encoding='utf-8')
p='C:/Temp/claude/pub/index.html'
h=open(p,encoding='utf-8').read()
i=h.index('const PRODUCT_SERIES');j=h.index('\n  ];',i)
blk=h[i:j]
EX={p['id'] for p in json.loads(re.search(r'^  const PRODUCTS = (.*);$',h,re.M).group(1))}
def series_span(sid):
    k=blk.index(f'id: "{sid}"'); s=blk.rfind('{',0,k); e=blk.index('\n    }',k)+6
    return s,e
def edit(sid,add=None,names=None,desc=None,summary=None):
    global blk
    add=[a for a in (add or []) if a in EX]
    names={k:v for k,v in (names or {}).items() if k in EX}
    s,e=series_span(sid); t=blk[s:e]
    if add:
        m=re.search(r'memberIds: \[([^\]]*)\]',t); ids=[int(x) for x in m.group(1).split(',')]
        for a in add:
            if a not in ids: ids.append(a)
        t=t.replace(m.group(0),'memberIds: ['+', '.join(map(str,ids))+']')
    if desc:
        t=re.sub(r'description: "[^"]*"','description: "'+desc+'"',t)
    if summary:
        t=re.sub(r'summary: \[[^\]]*\]','summary: '+json.dumps(summary,ensure_ascii=False),t)
    if names:
        if 'displayNames' in t:
            m=re.search(r'displayNames: \{(.*?)\n      \}',t,re.S)
            body=m.group(1).rstrip()
            add_lines=''.join(f',\n        {k}: {json.dumps(v,ensure_ascii=False)}' for k,v in names.items())
            t=t.replace(m.group(0),'displayNames: {'+body+add_lines+'\n      }')
        else:
            body=',\n'.join(f'        {k}: {json.dumps(v,ensure_ascii=False)}' for k,v in names.items())
            t=t.rstrip().rstrip('}').rstrip()
            if not t.endswith(','): t+=','
            t+='\n      displayNames: {\n'+body+'\n      }\n    }'
    blk=blk[:s]+t+blk[e:]
def new(sid,title,cat,ids,desc,names=None):
    global blk
    if f'id: "{sid}"' in blk:
        return edit(sid,ids,names)
    ids=[i for i in ids if i in EX]
    names={k:v for k,v in (names or {}).items() if k in EX} or None
    if len(ids)<2: return
    obj='\n    ,{\n      id: "%s",\n      title: "%s",\n      category: "%s",\n      memberIds: [%s],\n      description: "%s"'%(sid,title,cat,', '.join(map(str,ids)),desc)
    if names:
        obj+=',\n      displayNames: {\n'+',\n'.join(f'        {k}: {json.dumps(v,ensure_ascii=False)}' for k,v in names.items())+'\n      }'
    obj+='\n    }'
    blk=blk+obj
G="Диваны одной линейки: сравните размеры, конфигурации и спальное место."
edit('bali-sofas',[274,276,277,278,279],{274:"Бали 4 · прямой",276:"Бали 4 · без боковин",277:"Бали 4 · с оттоманкой",278:"Бали 4.1 · удлинённый",279:"Бали 7.2 · угловой"})
edit('lorton-sofas',[282],{282:"Лортон 2 · прямой"})
edit('martin-sofas',[284,285],{284:"Мартин 2 · угловой",285:"Мартин 3 · угловой"},desc="Модульные диваны с взаимозаменяемым углом. Сравните угловые и П-образные конфигурации для разных размеров гостиной.")
edit('bruno-sofas',[280],{280:"Бруно · П-образный"})
edit('lotos-sofas',[283],{283:"Лотос 1 · угловой"},desc="Угловые диваны одной линейки. Сравните размеры и конфигурации.")
edit('adel-sofas',[270,272,273],{270:"Адель 2 · МДК",272:"Адель 2 · 1500 ДК",273:"Адель 4 · 1500 ДК"},desc="Компактные и полноразмерные прямые диваны. Сравните исполнения по ширине и спальному месту.")
edit('finka-sofas',[321,322,323,324,325,326],{321:"Финка · хромированные боковины",322:"Финка · угловой, хромированные боковины",323:"Финка 18 · прямой",324:"Финка 3 · хромированные боковины",325:"Финка 5 · прямой",326:"Финка 5 · НПБ"})
edit('mono-beds',[286,287],{286:"Моно 3",287:"Моно 4"},desc="Кровати с лаконичным мягким изголовьем. Выберите исполнение для спального места шириной 140, 160 или 180 см.",summary=["Спальное место 140–180 × 200 см","4 исполнения"])
new('ostin-sofas','Остин','sofa',[5,296,297,298],G)
new('sofia-sofas','София','sofa',[206,313,314],G)
new('soft-sofas','Софт','sofa',[268,315,316,317,318,319,320],G)
new('sandra-sofas','Сандра','sofa',[232,309],G)
B="Кровати одной линейки: сравните изголовья, цвета и размеры спального места."
new('montana-beds','Монтана','bed',[288,289,290,291],B)
new('nevada-beds','Невада','bed',[213,292,293,294],B)
new('rica-beds','Рица','bed',[212,301,302,303,304,305,306,307,308],B,{301:"Рица 1 · 90 × 200",303:"Рица 2 · 90 × 200",305:"Рица 3 · 90 × 200",307:"Рица 4 · 90 × 200",308:"Рица детская"})
new('soty-beds','Соты','bed',[210,310,311,312],B)
new('eklips-beds','Эклипс','bed',[327,328,214,329],B)
edit('nova',[295])
edit('real',[300,299],desc="Беспружинные матрасы шириной 80–180 см. Сравните высоту, допустимую нагрузку и наполнение вариантов.",summary=['Ширина 80–180 см','Высота 15–24 см','Нагрузка 90–140 кг'])
h=h[:i]+blk+h[j:]
open(p,'w',encoding='utf-8').write(h)
print('ok')
