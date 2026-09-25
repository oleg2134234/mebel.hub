# -*- coding: utf-8 -*-
"""Слайд «Размеры» для матрасов Apogey (черновик шаблона, 24.09.2026).
Источник — 3D-изображение матраса с официальной листовки (slide_razrez.jpg, белый фон).
1) вырезаем только матрас (без иконок и текста листовки);
2) убираем номера-маркеры слоёв (бордовые кружки) инпейнтингом — пиксели матраса вне маркеров не меняются;
3) высота — вертикальная линия параллельно ближнему вертикальному ребру торца, с одинаковым отступом у обоих концов;
4) внизу плашка «Размеры Ш×Д см».
Запуск: python3 tools/render-mattress-dims.py <slug> — параметры в CFG."""
import sys, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
FONT='/home/claude/work/inter-bold-all.ttf'  # Inter Bold (латиница+кириллица) из assets/fonts
INK=(32,36,43); LW=4; DOT=8
CFG={
 'real-soft-matras': dict(crop=(168,38,812,390), edge=((183,215),(186,260)), h='17', size='80–180 × 200 см'),
}
slug=sys.argv[1]; c=CFG[slug]
src=cv2.imread(f'assets/{slug}/slide_razrez.jpg')
# маркеры: насыщенный бордовый
hsv=cv2.cvtColor(src,cv2.COLOR_BGR2HSV)
b,g,r=[src[...,i].astype(int) for i in range(3)]
mk=((r>90)&(r<200)&(g<70)&(b<110)&(r-g>60)).astype(np.uint8)
x0,y0,x1,y1=c['crop']; roi=np.zeros_like(mk); roi[y0:y1,x0:x1]=1; mk*=roi
n,lab,st,_=cv2.connectedComponentsWithStats(mk)
mask=np.zeros_like(mk)
for i in range(1,n):
    x,y,w,h,a=st[i]
    if a>150 and 0.7<w/h<1.4: cv2.circle(mask,(x+w//2,y+h//2),max(w,h)//2+3,1,-1)
mask=cv2.dilate(mask,np.ones((5,5),np.uint8))
fixed=cv2.inpaint(src,mask*255,7,cv2.INPAINT_TELEA)
# всё, что не связано с самим матрасом (текст/иконки листовки), — в белый
x0,y0,x1,y1=c['crop']
sub=fixed[y0:y1,x0:x1]
nw=(sub.min(axis=2)<246).astype(np.uint8)
nwc=cv2.morphologyEx(nw,cv2.MORPH_CLOSE,np.ones((3,3),np.uint8))
n2,lab2,st2,_=cv2.connectedComponentsWithStats(nwc)
big=1+int(np.argmax(st2[1:,4]))
keep=cv2.dilate((lab2==big).astype(np.uint8),np.ones((3,3),np.uint8)).astype(bool)
sub[~keep]=255
im=Image.fromarray(cv2.cvtColor(fixed,cv2.COLOR_BGR2RGB)).crop(c['crop'])
S=2.05
im=im.resize((round(im.width*S),round(im.height*S)),Image.LANCZOS)
W,H=1600,1000
cv=Image.new('RGB',(W,H),'white'); ox=(W-im.width)//2+70; oy=60
cv.paste(im,(ox,oy)); d=ImageDraw.Draw(cv)
f=ImageFont.truetype(FONT,44)
def T(p): return (ox+(p[0]-x0)*S, oy+(p[1]-y0)*S)
A,B=T(c['edge'][0]),T(c['edge'][1]); off=38
P1=(A[0]-off,A[1]); P2=(B[0]-off,B[1])
d.line([P1,P2],fill=INK,width=LW)
for P in (P1,P2): d.ellipse([P[0]-DOT,P[1]-DOT,P[0]+DOT,P[1]+DOT],fill=INK)
def pill(cx,cy,t,font,pad=30,h=66):
    l,tp,r,bm=d.textbbox((0,0),t,font=font); tw,th=r-l,bm-tp; w=max(h+10,tw+2*pad)
    d.rounded_rectangle([cx-w/2,cy-h/2,cx+w/2,cy+h/2],radius=h/2,fill=INK)
    d.text((cx-tw/2-l,cy-th/2-tp),t,font=font,fill='white')
    return w
mid=((P1[0]+P2[0])/2,(P1[1]+P2[1])/2)
l,tp,r,bm=d.textbbox((0,0),c['h'],font=f); pw=max(76,r-l+60)
pill(mid[0]-pw/2-18,mid[1],c['h'],f)
pill(W/2,H-110,'Размеры '+c['size'],ImageFont.truetype(FONT,46),pad=40,h=84)
out=f'assets/{slug}/slide_dims.jpg'; cv.save(out,quality=90,optimize=True); print(out, int(mask.sum()),'px inpainted')
