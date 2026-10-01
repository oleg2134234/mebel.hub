import fs from "node:fs";
const [,, localId, imgPath] = process.argv;
const PUB="C:/Temp/claude/pub";
const cards=JSON.parse(fs.readFileSync("C:/Temp/claude/work/cards.json","utf8"));
const c=cards.find(x=>x.localId==localId); if(!c) throw new Error("no card");
const dir=`${PUB}/assets/${c.slug}`; fs.mkdirSync(dir,{recursive:true});
const rel=`assets/${c.slug}/slide1_interior.jpg`;
fs.copyFileSync(imgPath,`${PUB}/${rel}`);
let h=fs.readFileSync(`${PUB}/index.html`,"utf8");
function edit(name,fn){const re=new RegExp(`^(  const ${name} = )(.*)(;)$`,"m");const m=h.match(re);if(!m)throw new Error(name);
  const v=JSON.parse(m[2]);fn(v);h=h.replace(re,(_,a,__,z)=>a+JSON.stringify(v)+z);}
edit("PRODUCTS",v=>{if(v.some(p=>p.id==c.localId||p.title==c.title))throw new Error("dup "+c.title);v.push({id:c.localId,title:c.title,category:c.category,dims:c.dims,desc:c.desc,colorIdx:c.colorIdx});});
edit("IMAGES",v=>{v[String(c.localId)]=rel;});
edit("GALLERIES",v=>{v[String(c.localId)]={title:c.title,slides:[{src:rel,name:"В интерьере",desc:c.caption}]};});
fs.writeFileSync(`${PUB}/index.html`,h);
console.log("added",c.title,rel);
