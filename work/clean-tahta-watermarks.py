from PIL import Image, ImageDraw, ImageFont, ImageOps
from pathlib import Path
p=Path('assets/tahta-nice')
items=['real_general','real_side','real_unfolded','real_storage']
for name in items:
    im=Image.open(p/f'{name}.jpg').convert('RGB')
    w,h=im.size
    cut=max(30, round(h*0.12))
    clean=im.crop((0,0,w,h-cut)).resize((w,h),Image.Resampling.LANCZOS)
    clean.save(p/f'{name}-v2.jpg',quality=94,subsampling=0)

def font(size,bold=False):
    roots=[Path('C:/Windows/Fonts')]
    fn='arialbd.ttf' if bold else 'arial.ttf'
    return ImageFont.truetype(str(roots[0]/fn),size)

def panel(src, labels):
    W,H=1200,760
    canvas=Image.new('RGB',(W,H),'white')
    im=Image.open(p/src).convert('RGB')
    im.thumbnail((980,610),Image.Resampling.LANCZOS)
    x=(W-im.width)//2; y=45+(610-im.height)//2
    canvas.paste(im,(x,y))
    d=ImageDraw.Draw(canvas)
    # horizontal dimension
    yy=700; x1=150; x2=1050
    d.line((x1,yy,x2,yy),fill='#20262b',width=4)
    d.polygon([(x1,yy),(x1+20,yy-10),(x1+20,yy+10)],fill='#20262b')
    d.polygon([(x2,yy),(x2-20,yy-10),(x2-20,yy+10)],fill='#20262b')
    txt=labels[0]; f=font(34,True); box=d.textbbox((0,0),txt,font=f); tw=box[2]
    d.rounded_rectangle(((W-tw)//2-18,yy-25,(W+tw)//2+18,yy+25),radius=18,fill='#20262b')
    d.text(((W-tw)//2,yy-20),txt,font=f,fill='white')
    # vertical dimension
    xx=1125; y1=85; y2=650
    d.line((xx,y1,xx,y2),fill='#20262b',width=4)
    d.polygon([(xx,y1),(xx-10,y1+20),(xx+10,y1+20)],fill='#20262b')
    d.polygon([(xx,y2),(xx-10,y2-20),(xx+10,y2-20)],fill='#20262b')
    txt=labels[1]; box=d.textbbox((0,0),txt,font=f); tw=box[2]
    d.rounded_rectangle((xx-tw//2-18,(y1+y2)//2-26,xx+tw//2+18,(y1+y2)//2+26),radius=18,fill='#20262b')
    d.text((xx-tw//2,(y1+y2)//2-20),txt,font=f,fill='white')
    return canvas
upper=panel('real_general-v2.jpg',('1600','760'))
lower=panel('real_unfolded-v2.jpg',('760','2000'))
out=Image.new('RGB',(1200,1540),'white'); out.paste(upper,(0,0)); out.paste(lower,(0,780))
out.save(p/'slide_dims-v2.jpg',quality=94,subsampling=0)

