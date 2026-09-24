from pathlib import Path
import json,re,subprocess
git=r'C:/Users/user/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/git/cmd/git.exe'
remote=subprocess.check_output([git,'show','c15e92591c5035b700651f40af19b5fe344c9adb:index.html']).decode('utf-8')
ours=subprocess.check_output([git,'show','4bbf997:index.html']).decode('utf-8')
result=remote
def parse(text,name): return json.loads(re.search(r'const '+name+r' = (.*?);\s*\n',text)[1])
for name in ('PRODUCTS','IMAGES','GALLERIES'):
    dst,src=parse(result,name),parse(ours,name)
    if name=='PRODUCTS':
        item=next(p for p in src if p['id']==233)
        dst=[p for p in dst if p['id']!=233]+[item]
    else: dst['233']=src['233']
    result=re.sub(r'(const '+name+r' = ).*?(;\s*\n)',lambda m:m[1]+json.dumps(dst,ensure_ascii=False)+m[2],result,count=1)
Path('index.html').write_text(result,encoding='utf-8')
print('Remote index preserved; Tahta Nice id 233 applied.')
