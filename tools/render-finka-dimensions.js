// SVG composition keeps the original gallery photographs embedded without re-encoding.
const fs = require('fs');
const path = require('path');
const root = path.resolve(__dirname, '..');
const ink = '#282d2f';
function dimension(label, a, b, offset) {
  const dx=b[0]-a[0], dy=b[1]-a[1], len=Math.hypot(dx,dy);
  const p=[a[0]-dy/len*offset,a[1]+dx/len*offset];
  const q=[b[0]-dy/len*offset,b[1]+dx/len*offset];
  const mx=(p[0]+q[0])/2, my=(p[1]+q[1])/2;
  return `<g fill="${ink}"><path d="M${p} L${q}" fill="none" stroke="${ink}" stroke-width="2"/><circle cx="${p[0]}" cy="${p[1]}" r="3"/><circle cx="${q[0]}" cy="${q[1]}" r="3"/><rect x="${mx-32}" y="${my-16}" width="64" height="32" rx="16"/><text x="${mx}" y="${my+1}" dominant-baseline="middle" text-anchor="middle" font-family="Arial,sans-serif" font-size="21" font-weight="700" fill="white">${label}</text></g>`;
}
const specs=[
  {id:233,dir:'finka-5-dk-npb',fold:'real4_angle.jpg',open:'real5_unfold.jpg',dims:'195×105',bed:'195×142',height:'100',
   lines:[[['195',[200,346],[583,289],35],['105',[200,346],[140,286],-45]], [['195',[145,305],[558,243],35],['142',[145,305],[70,172],-42]]]},
  {id:235,dir:'finka-4-1-dk',fold:'real3_angle.jpg',open:'real6_unfold.jpg',dims:'225×110',bed:'195×143',height:'94',
   lines:[[['225',[150,306],[580,248],45],['110',[150,306],[98,224],-42]], [['195',[150,280],[618,224],47],['143',[150,280],[88,147],-85]]]},
  {id:234,dir:'finka-4-1-dku',fold:'real4_angle.jpg',open:'real7_unfold.jpg',dims:'310×163',bed:'280×140',height:'94',
   lines:[[['310',[92,286],[618,232],90],['163',[160,335],[64,224],-46]], [['280',[120,163],[625,144],-55],['140',[142,315],[70,173],-100]]]},
];
for(const spec of specs){
  const panels=[spec.fold,spec.open].map((file,i)=>{
    const jpg=fs.readFileSync(path.join(root,'assets',spec.dir,file)).toString('base64');
    return `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="700" viewBox="-45 0 750 437.5"><rect x="-55" y="-35" width="780" height="520" fill="white"/><image href="data:image/jpeg;base64,${jpg}" x="0" y="0" width="668" height="375" preserveAspectRatio="xMidYMid meet"/>${spec.lines[i].map(l=>dimension(...l)).join('')}</svg>`;
  });
  panels.forEach((svg,i)=>fs.writeFileSync(path.join(root,'assets',spec.dir,`dims-panel-${i+1}.svg`),svg));
  const composed=`<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1400" viewBox="0 0 1200 1400"><rect width="1200" height="1400" fill="white"/>${panels.map((p,i)=>`<g transform="translate(0 ${i*700})">${p}</g>`).join('')}</svg>`;
  fs.writeFileSync(path.join(root,'assets',spec.dir,'slide_dims-v3.svg'),composed);
}
let html=fs.readFileSync(path.join(root,'index.html'),'utf8');
html=html.replace(/const GALLERIES\s*=\s*(\{.*?\});/,(_,json)=>{
  const g=JSON.parse(json);
  g[5].slides=g[5].slides.filter(s=>s.src!=='assets/ostin-3-dk/slide_angle2.jpg');
  for(const s of specs){
    g[s.id].slides=g[s.id].slides.filter(x=>x.name!=='Размеры');
    const pos=g[s.id].slides.findIndex(x=>!['В интерьере','Уют','Уютный вечер'].includes(x.name));
    g[s.id].slides.splice(pos,0,{src:`assets/${s.dir}/slide_dims-v3.svg`,name:'Размеры',desc:`Размеры в сантиметрах. Сверху: габариты ${s.dims}. Снизу: спальное место ${s.bed}. Высота дивана — ${s.height} см.`});
  }
  return 'const GALLERIES = '+JSON.stringify(g)+';';
});
fs.writeFileSync(path.join(root,'index.html'),html);
console.log('Created three dimension slides; removed Ostin angle2 gallery entry.');
