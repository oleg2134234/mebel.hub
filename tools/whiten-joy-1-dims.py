# Фон -> белый: нейтральные светлые пиксели (фон, тень на полу) линейно растягиваются 229 -> 255,
# ткань дивана (хроматичные пиксели) и тёмные пиксели не трогаются; металл механизма защищён.
import numpy as np
from PIL import Image, ImageDraw
im=Image.open('assets/joy-1-dku-o/slide3_dims.jpg').convert('RGB')
BG=(229,229,229); d=ImageDraw.Draw(im)
OLD=[((75.5,523.3),(341.7,604)),((369.3,606.3),(1118,515.3)),((777,1003.5),(1111.3,1073.3)),((397,1470),(1116,1308))]
for A,B in OLD:
    d.line([A,B],fill=BG,width=16)
    for P in (A,B): d.ellipse([P[0]-15,P[1]-15,P[0]+15,P[1]+15],fill=BG)
for box in [(140,538,254,602),(697,538,810,602),(886,999,1000,1063),(565,1379,675,1443)]:
    d.rounded_rectangle(box,radius=30,fill=BG)
a=np.asarray(im).astype(float)
lum=a.mean(2); ch=a.max(2)-a.min(2)
neutral=(ch<=12)&(lum>=150)
prot=np.zeros(neutral.shape,bool); prot[1240:1345,286:362]=True   # металл механизма
from scipy import ndimage as nd
body=nd.binary_fill_holes(nd.binary_closing(ch>12,np.ones((15,15))))
# светлые блики ткани на верхних кромках: над ними (ниже по кадру в пределах 40px) есть тело дивана
below=np.zeros_like(body)
for k in range(1,41): below[:-k]|=body[k:]
edge=nd.binary_dilation(body,np.ones((9,9)))&below&(lum<=222)
sel=neutral&~prot&~body&~edge
out=a.copy()
out[sel]=np.clip(a[sel]*255/229,0,255)
out[sel & (out.min(2)>=247)]=255
chg=np.abs(out-a).max(2)>0
print('fabric px changed:', int((chg & (ch>12)).sum()), ' bg white share:', round(float((out.min(2)==255).mean()),3))
Image.fromarray(out.round().astype(np.uint8)).save('white.png')
