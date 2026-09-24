from pathlib import Path
import json,re,subprocess
git=r'C:/Users/user/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/git/cmd/git.exe'
head=subprocess.check_output([git,'show','HEAD:index.html']).decode('utf-8')
current=Path('index.html').read_text(encoding='utf-8')
candidate=head
for name in ['PRODUCTS','IMAGES','GALLERIES']:
    pattern=r'(const '+name+r' = )(.*?)(;\s*\n)'
    old=json.loads(re.search(pattern,head)[2])
    new=json.loads(re.search(pattern,current)[2])
    if name=='PRODUCTS':
        print(name,'changed ids:',[p['id'] for p in new if p not in old])
        assert not any(p['id']==232 for p in old)
        old.append(next(p for p in new if p['id']==232))
    else:
        print(name,'changed ids:',[k for k in new if new[k]!=old.get(k)])
        old['232']=new['232']
    candidate=re.sub(pattern,lambda m:m[1]+json.dumps(old,ensure_ascii=False)+m[3],candidate,count=1)
Path('work/sandra-2/publish-index.html').write_text(candidate,encoding='utf-8',newline='\n')
gallery=json.loads(re.search(r'const GALLERIES = (.*?);\s*\n',candidate)[1])['232']
for s in gallery['slides']:
    p=Path(s['src'])
    assert p.is_file() and p.stat().st_size<5_000_000
print('Publish candidate ready; 10 gallery entries checked.')
