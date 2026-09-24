const { chromium } = require('C:/Users/user/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
 const browser=await chromium.launch({headless:true,channel:'msedge'});
 const page=await browser.newPage({viewport:{width:1440,height:1100}});
 const errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:8792');
 await page.evaluate(()=>window.openGallery(232));
 await page.locator('#galleryOverlay').waitFor({state:'visible'});
 await page.locator('#galTrack img').evaluateAll(async imgs=>Promise.all(imgs.map(im=>im.decode())));
 const media=await page.locator('#galTrack').evaluate(async el=>{
   const v=el.querySelector('video');
   if(v.readyState===0)await new Promise((ok,fail)=>{v.addEventListener('loadedmetadata',ok,{once:true});v.addEventListener('error',fail,{once:true});});
   return {images:[...el.querySelectorAll('img')].map(i=>({src:i.getAttribute('src'),width:i.naturalWidth})),videoDuration:v.duration};
 });
 await page.screenshot({path:'work/sandra-2/desktop.png'});
 await page.setViewportSize({width:390,height:844});
 await page.screenshot({path:'work/sandra-2/mobile.png'});
 console.log(JSON.stringify({errors,media,slideCount:await page.locator('#galTotal').textContent()}));
 await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
