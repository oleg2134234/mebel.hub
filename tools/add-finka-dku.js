const fs = require('fs');
const path = require('path');
const root = path.resolve(__dirname, '..');
const dir = path.join(root, 'assets', 'finka-dku');
const ink = '#282d2f';

function dataUri(file) {
  return `data:image/jpeg;base64,${fs.readFileSync(path.join(dir, file)).toString('base64')}`;
}
function dim(label, a, b, offset) {
  const dx=b[0]-a[0], dy=b[1]-a[1], len=Math.hypot(dx,dy);
  const p=[a[0]-dy/len*offset,a[1]+dx/len*offset];
  const q=[b[0]-dy/len*offset,b[1]+dx/len*offset];
  const mx=(p[0]+q[0])/2, my=(p[1]+q[1])/2;
  return `<g fill="${ink}"><path d="M${p} L${q}" fill="none" stroke="${ink}" stroke-width="2"/><circle cx="${p[0]}" cy="${p[1]}" r="3"/><circle cx="${q[0]}" cy="${q[1]}" r="3"/><rect x="${mx-32}" y="${my-16}" width="64" height="32" rx="16"/><text x="${mx}" y="${my+1}" dominant-baseline="middle" text-anchor="middle" font-family="Arial,sans-serif" font-size="21" font-weight="700" fill="white">${label}</text></g>`;
}
function panel(file, lines) {
  return `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="700" viewBox="-45 0 750 437.5"><rect x="-45" width="750" height="437.5" fill="white"/><image href="${dataUri(file)}" x="0" y="0" width="668" height="374" preserveAspectRatio="xMidYMid meet"/>${lines.map(x=>dim(...x)).join('')}</svg>`;
}
const folded=panel('source-4.jpg', [
  ['290',[72,316],[626,260],55],
  ['180',[72,316],[20,245],-55],
]);
const opened=panel('source-5.jpg', [
  ['290',[65,280],[624,245],65],
  ['138',[65,280],[15,203],-55],
]);
fs.writeFileSync(path.join(dir,'dims-panel-folded.svg'),folded);
fs.writeFileSync(path.join(dir,'dims-panel-unfolded.svg'),opened);
fs.writeFileSync(path.join(dir,'slide_dims-v1.svg'),`<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1400" viewBox="0 0 1200 1400"><rect width="1200" height="1400" fill="white"/><g>${folded}</g><g transform="translate(0 700)">${opened}</g></svg>`);

const benefits=`<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="900" viewBox="0 0 1200 900"><rect width="1200" height="900" fill="#f6f2ea"/><image href="${dataUri('source-4.jpg')}" x="80" y="100" width="540" height="348"/><text x="80" y="70" font-family="Arial,sans-serif" font-size="42" font-weight="700" fill="${ink}">Преимущества и особенности</text><g font-family="Arial,sans-serif" fill="${ink}"><text x="690" y="170" font-size="32" font-weight="700">Книжка</text><text x="690" y="210" font-size="24">3 положения спинки</text><text x="690" y="300" font-size="32" font-weight="700">Два бельевых ящика</text><text x="690" y="340" font-size="24">под сиденьем и оттоманкой</text><text x="690" y="430" font-size="32" font-weight="700">Ортопедическое основание</text><text x="690" y="470" font-size="24">металлокаркас, ППУ и синтепон</text><text x="80" y="610" font-size="32" font-weight="700">Без подлокотников</text><text x="80" y="650" font-size="24">свободный доступ к посадочному месту</text><text x="80" y="745" font-size="32" font-weight="700">Хромированные опоры</text><text x="80" y="785" font-size="24">с силиконовой вставкой</text></g></svg>`;
fs.writeFileSync(path.join(dir,'slide_benefits-v1.svg'),benefits);

let html=fs.readFileSync(path.join(root,'index.html'),'utf8');
html=html.replace(/const PRODUCTS\s*=\s*(\[.*?\]);/,(_,json)=>{
  const products=JSON.parse(json);
  if (!products.some(p=>p.id===236)) products.push({id:236,title:'Финка ДКУ',category:'sofa',dims:'2900×1800×1000',desc:'Угловой диван-кровать без подлокотников. Механизм «Книжка», три положения спинки. Металлокаркас, ППУ, синтепон и ортопедическое основание; два бельевых ящика. Спальное место 2900×1380 мм.',colorIdx:4});
  return 'const PRODUCTS = '+JSON.stringify(products)+';';
});
html=html.replace(/const IMAGES\s*=\s*(\{.*?\});/,(_,json)=>{
  const images=JSON.parse(json); images[236]='assets/finka-dku/source-9.jpg';
  return 'const IMAGES = '+JSON.stringify(images)+';';
});
html=html.replace(/const GALLERIES\s*=\s*(\{.*?\});/,(_,json)=>{
  const g=JSON.parse(json);
  g[236]={title:'Финка ДКУ',slides:[
    {src:'assets/finka-dku/source-9.jpg',name:'В интерьере',desc:'Официальное изображение поставщика: угловой диван «Финка ДКУ» в зелёной обивке.'},
    {src:'assets/finka-dku/slide_cozy-v1.png',name:'Уютный вечер',desc:'Тёплый семейный вечер: чтение, чай и домашний питомец. Визуализация создана по официальному интерьерному изображению зелёной модели.'},
    {src:'assets/finka-dku/slide_dims-v1.svg',name:'Размеры',desc:'Размеры в сантиметрах. Сверху: габариты 290×180. Снизу: спальное место 290×138. Высота дивана — 100 см.'},
    {src:'assets/finka-dku/source-4.jpg',name:'Общий вид',desc:'Официальное изображение поставщика. Общий вид углового дивана без подлокотников.'},
    {src:'assets/finka-dku/source-1.jpg',name:'Вид спереди',desc:'Официальное изображение поставщика. Вид спереди.'},
    {src:'assets/finka-dku/source-2.jpg',name:'Вид сбоку',desc:'Официальное изображение поставщика. Боковой профиль в сложенном виде.'},
    {src:'assets/finka-dku/source-3.jpg',name:'Вид сзади',desc:'Официальное изображение поставщика. Задняя стенка показана в основной ткани; стандартную комплектацию необходимо уточнять.'},
    {src:'assets/finka-dku/source-5.jpg',name:'В разложенном виде',desc:'Официальное изображение поставщика. Спальное место 2900×1380 мм.'},
    {src:'assets/finka-dku/source-6.jpg',name:'Раскладка',desc:'Официальное изображение поставщика. Промежуточное положение механизма «Книжка».'},
    {src:'assets/finka-dku/source-7.jpg',name:'Бельевые ящики',desc:'Официальное изображение поставщика. Два бельевых ящика: под сиденьем и оттоманкой.'},
    {src:'assets/finka-dku/slide_benefits-v1.svg',name:'Преимущества и особенности',desc:'Механизм «Книжка», три положения спинки, два бельевых ящика, ортопедическое основание и отсутствие подлокотников.'}
  ]};
  return 'const GALLERIES = '+JSON.stringify(g)+';';
});
fs.writeFileSync(path.join(root,'index.html'),html);
console.log('Added 236 Финка ДКУ with 11 slides.');
