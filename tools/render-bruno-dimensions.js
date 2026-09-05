const fs=require('fs');
const path=require('path');
const root=path.resolve(__dirname,'..');
const dir=path.join(root,'assets/bruno-bd-l');
// Values confirmed by the user on 2026-09-05. 217 follows the pull-out direction.
function line(label,a,b,d){
  const dx=b[0]-a[0],dy=b[1]-a[1],l=Math.hypot(dx,dy);
  const p=[a[0]-dy/l*d,a[1]+dx/l*d],q=[b[0]-dy/l*d,b[1]+dx/l*d];
  const x=(p[0]+q[0])/2,y=(p[1]+q[1])/2;
  return `<g fill="#282d2f"><path d="M${p} L${q}" stroke="#282d2f" stroke-width="5" fill="none"/><circle cx="${p[0]}" cy="${p[1]}" r="7"/><circle cx="${q[0]}" cy="${q[1]}" r="7"/><rect x="${x-65}" y="${y-33}" width="130" height="66" rx="33"/><text x="${x}" y="${y+3}" fill="white" text-anchor="middle" dominant-baseline="middle" font-family="Arial,sans-serif" font-size="43" font-weight="700">${label}</text></g>`;
}
const specs=[['dims-folded-white-v1.png',[['308',[230,1010],[1265,602],70],['110',[230,1010],[65,655],-80]]],['dims-unfolded-white-v1.png',[['170',[465,780],[1410,770],275],['217',[1410,770],[1090,365],160]]]];
const panels=specs.map(([file,lines],i)=>{
  const data=fs.readFileSync(path.join(dir,file)).toString('base64');
  const svg=`<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="800" viewBox="-100 130 1725 1150"><rect x="-100" y="130" width="1725" height="1150" fill="white"/><image width="1448" height="1086" href="data:image/png;base64,${data}"/>${lines.map(x=>line(...x)).join('')}</svg>`;
  fs.writeFileSync(path.join(dir,`dims-panel-${i+1}-v2.svg`),svg); return svg;
});
fs.writeFileSync(path.join(dir,'slide_dims-v2.svg'),`<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1600"><rect width="1200" height="1600" fill="white"/>${panels.map((s,i)=>`<g transform="translate(0 ${i*800})">${s}</g>`).join('')}</svg>`);
let html=fs.readFileSync(path.join(root,'index.html'),'utf8');
html=html.replace(/const GALLERIES\s*=\s*(\{.*?\});/,(_,json)=>{
 const g=JSON.parse(json),s=g[231].slides.find(x=>x.name==='Размеры');
 s.src='assets/bruno-bd-l/slide_dims-v2.svg';
 s.desc='Размеры в сантиметрах. Сверху: корпус 308×110. Снизу: спальное место 217 вдоль раскладки × 170 поперёк.';
 return 'const GALLERIES = '+JSON.stringify(g)+';';
});
fs.writeFileSync(path.join(root,'index.html'),html);
