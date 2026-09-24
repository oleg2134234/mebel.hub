# -*- coding: utf-8 -*-
"""Джой 1 ДКУ-О (id 220) — слайд «Размеры» v2.
Исходник: assets/joy-1-dku-o/slide3_dims.jpg (одобренная геометрия линий 02.09.2026).
Фон 229-серый -> #FFFFFF детерминированно по маске (пиксели дивана не меняются).
Линии — строго в прежних координатах, меняются только числа:
  сложенный 278 x 180 (PRODUCTS[220].dims 2780x1800x855),
  разложенный 170 x 200 (desc: спальное место 1700x2000)."""
from PIL import Image, ImageDraw, ImageFont
INK=(61,63,39); LW=4; DOT=8
im=Image.open('white.png').convert('RGB'); d=ImageDraw.Draw(im)
font=ImageFont.truetype('inter-bold.ttf',36)
def dim(A,B,label,t):
    d.line([A,B],fill=INK,width=LW)
    for P in (A,B): d.ellipse([P[0]-DOT,P[1]-DOT,P[0]+DOT,P[1]+DOT],fill=INK)
    c=(A[0]+(B[0]-A[0])*t, A[1]+(B[1]-A[1])*t)
    l,tp,r,b=d.textbbox((0,0),label,font=font); tw,th=r-l,b-tp
    w,h=max(104,tw+44),54
    d.rounded_rectangle([c[0]-w/2,c[1]-h/2,c[0]+w/2,c[1]+h/2],radius=h/2,fill=INK)
    d.text((c[0]-tw/2-l,c[1]-th/2-tp),label,font=font,fill='white')
dim((75.5,523.3),(341.7,604.0),'180',0.45)
dim((369.3,606.3),(1118.0,515.3),'278',0.513)
dim((777.0,1003.5),(1111.3,1073.3),'200',0.5)
dim((397.0,1470.0),(1116.0,1308.0),'170',0.31)
im.save('slide3_dims-v2.jpg',quality=90,optimize=True)
print(im.size)
