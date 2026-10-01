import fs from "node:fs";
const cards=JSON.parse(fs.readFileSync("C:/Temp/claude/work/cards.json","utf8"));
let h=fs.readFileSync("C:/Temp/claude/pub/index.html","utf8");
const re=/^(  const PRODUCTS = )(.*)(;)$/m;const m=h.match(re);const P=JSON.parse(m[2]);let n=0;
for(const p of P){const c=cards.find(x=>x.localId==p.id);if(c){p.desc=c.desc;p.dims=c.dims;n++;}}
h=h.replace(re,(_,a,__,z)=>a+JSON.stringify(P)+z);fs.writeFileSync("C:/Temp/claude/pub/index.html",h);console.log("updated",n);
