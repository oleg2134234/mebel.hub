#!/bin/bash
# usage: getgen.sh localId webId url500
cd /c/Temp/claude/work
u="${3/_500.jpg/.jpg}"
curl -s -o gen/$1_raw.jpg "$u"
python - "$1" "$2" <<'PY'
import sys
from PIL import Image
lid,wid=sys.argv[1:3]
im=Image.open(f'gen/{lid}_raw.jpg').convert('RGB');im.save(f'gen/{lid}.jpg',quality=86,optimize=True)
ref=Image.open(f'refs/{wid}_2.jpg') if __import__('os').path.exists(f'refs/{wid}_2.jpg') else Image.open(f'refs/{wid}_1.jpg')
h=700
a=ref.resize((int(ref.width*h/ref.height),h));b=im.resize((int(im.width*h/im.height),h))
S=Image.new('RGB',(a.width+b.width+10,h),'white');S.paste(a,(0,0));S.paste(b,(a.width+10,0));S.save(f'gen/{lid}_cmp.jpg',quality=80)
print(im.size)
PY
