import fs from "node:fs";
import {execSync} from "node:child_process";
const PUB="C:/Temp/claude/pub";
const M=[
 {id:295,web:173,slug:"nova-1-matras",title:"Нова 1 Матрас",dims:"2000×800–1800×230–240",src:"C:/Temp/claude/work/src/173/1.jpg",
  desc:"Пружинный матрас «Нова 1» на независимом пружинном блоке НПБ (высота 140 мм, 256 шт/м²). Трикотажный чехол, простёганный на полисинтексе 300 и ППУ 10 мм, слой ППУ 20 мм и термотекстиль. Нагрузка 120 кг, высота 23–24 см, жёсткость средне-мягкая. Ширина 80–180 см, длина 200 см.",
  cap:"Нагрузка 120 кг, высота 23–24 см, независимый пружинный блок. Официальная схема."},
 {id:299,web:116,slug:"real-medium-layt-matras",title:"Реал Медиум Лайт Матрас",dims:"2000×800–1800×200–210",src:"C:/Temp/claude/work/src/116/1.jpeg",
  desc:"Беспружинный матрас «Реал Медиум Лайт»: жаккард с эффектом состава хлопка на полисинтексе 150 г/м², массажный слой рифлёного высокоэластичного ППУ 30 мм и блок высокоэластичного ППУ повышенной жёсткости 140 мм. Нагрузка 120 кг, высота 20–21 см, жёсткость средняя. Ширина 80–180 см, длина 200 см.",
  cap:"Нагрузка 120 кг, массажный слой ППУ, высота 20–21 см. Официальная схема."},
 {id:300,web:115,slug:"real-soft-layt-matras",title:"Реал Софт Лайт Матрас",dims:"2000×800–1800×150–160",src:"C:/Temp/claude/work/src/115/1.jpeg",
  desc:"Беспружинный матрас «Реал Софт Лайт»: жаккард с эффектом состава хлопка на полисинтексе 150 г/м² и блок высокоэластичного ППУ повышенной жёсткости 140 мм. Нагрузка 90 кг, высота 15–16 см, жёсткость средняя. Ширина 80–180 см, длина 200 см.",
  cap:"Нагрузка 90 кг, высота 15–16 см, ППУ повышенной жёсткости. Официальная схема."}];
let h=fs.readFileSync(`${PUB}/index.html`,"utf8");
function edit(name,fn){const re=new RegExp(`^(  const ${name} = )(.*)(;)$`,"m");const m=h.match(re);const v=JSON.parse(m[2]);fn(v);h=h.replace(re,(_,a,__,z)=>a+JSON.stringify(v)+z);}
for(const c of M){
  const dir=`${PUB}/assets/${c.slug}`;fs.mkdirSync(dir,{recursive:true});
  const out=`${dir}/slide1_scheme.jpg`;
  execSync(`python -c "from PIL import Image;im=Image.open(r'${c.src}').convert('RGB');im.thumbnail((1600,1600));im.save(r'${out}',quality=88)"`);
  const rel=`assets/${c.slug}/slide1_scheme.jpg`;
  edit("PRODUCTS",v=>{if(v.some(p=>p.id==c.id||p.title==c.title))throw new Error("dup "+c.title);v.push({id:c.id,title:c.title,category:"mattress",dims:c.dims,desc:c.desc,colorIdx:5});});
  edit("IMAGES",v=>{v[String(c.id)]=rel;});
  edit("GALLERIES",v=>{v[String(c.id)]={title:c.title,slides:[{src:rel,name:"Схема матраса",desc:c.cap}]};});
}
fs.writeFileSync(`${PUB}/index.html`,h);console.log("ok");
