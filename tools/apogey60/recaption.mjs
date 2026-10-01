import fs from "node:fs";
const cards=JSON.parse(fs.readFileSync("C:/Temp/claude/work/cards.json","utf8"));
const ids=process.argv.slice(2).map(Number);
let h=fs.readFileSync("C:/Temp/claude/pub/index.html","utf8");
const re=/^(  const GALLERIES = )(.*)(;)$/m;const m=h.match(re);const G=JSON.parse(m[2]);
for(const id of ids){const c=cards.find(x=>x.localId==id);G[String(id)].slides[0].desc=c.caption;}
h=h.replace(re,(_,a,__,z)=>a+JSON.stringify(G)+z);fs.writeFileSync("C:/Temp/claude/pub/index.html",h);console.log("ok",ids.length);
