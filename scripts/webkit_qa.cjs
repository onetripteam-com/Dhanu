const {webkit}=require('playwright');
const {spawn}=require('child_process');
const fs=require('fs');
const path=require('path');
(async()=>{
 const root=path.resolve(__dirname,'..');
 const port=8123;
 const server=spawn('python3',['-m','http.server',String(port),'--bind','127.0.0.1'],{cwd:root,stdio:'ignore'});
 const wait=ms=>new Promise(resolve=>setTimeout(resolve,ms));
 await wait(800);
 const browser=await webkit.launch({headless:true});
 const tests=[];
 const errors=[];
 let failed=false;
 try {
  for(const vp of [{name:'webkit-phone-393',width:393,height:852},{name:'webkit-desktop',width:1440,height:900}]){
   const ctx=await browser.newContext({viewport:{width:vp.width,height:vp.height},deviceScaleFactor:1,hasTouch:vp.width<500,isMobile:vp.width<500,reducedMotion:'reduce'});
   const page=await ctx.newPage();
   page.on('pageerror',e=>errors.push(vp.name+': '+e.message));
   const external=[];
   page.on('request',r=>{if(r.url().startsWith('http')&&!r.url().startsWith('http://127.0.0.1:'+port+'/'))external.push(r.url())});
   await page.goto('http://127.0.0.1:'+port+'/index.html',{waitUntil:'load',timeout:60000});
   await page.waitForTimeout(200);
   const basic=await page.evaluate(()=>{
    const seq=['one','two','three','four','five'].map(x=>document.getElementById('chapter-'+x));
    const hero=document.querySelector('.manifesto-opening-portrait img');
    return {order:seq.every(Boolean)&&seq.every((x,i)=>!i||seq[i-1].compareDocumentPosition(x)&Node.DOCUMENT_POSITION_FOLLOWING),
      width:document.documentElement.scrollWidth,viewport:innerWidth,heroLoaded:hero.complete&&hero.naturalWidth>0,
      galleryButtons:document.querySelectorAll('.figure-zoom').length,footerOutside:!document.querySelector('.final-reveal footer')};
   });
   await page.locator('.figure-zoom').first().click();
   const modalOpen=await page.locator('#studio-lightbox').evaluate(x=>x.open);
   await page.locator('#studio-lightbox-close').click();
   const modalClosed=await page.locator('#studio-lightbox').evaluate(x=>!x.open);
   await page.locator('[data-final-choice="return"]').click();
   const unlocked=await page.locator('#final-reveal').evaluate(x=>x.classList.contains('show'));
   await page.reload({waitUntil:'load'});
   const persisted=await page.locator('#final-reveal').evaluate(x=>x.classList.contains('show'));
   let reset=false;
   page.once('dialog',async d=>{await d.accept()});
   await page.locator('#studio-reset').click();
   await page.waitForLoadState('load');
   await page.waitForTimeout(180);
   const resetState=await page.evaluate(()=>{
     const seen=Object.keys(localStorage).filter(k=>/^manifesto-v[2345]-/.test(k));
     const revealed=document.getElementById('final-reveal').classList.contains('show');
     const unexpected=seen.filter(k=>k!=='manifesto-v4-lastchapter');
     return {revealed,seen,unexpected,lastChapter:localStorage.getItem('manifesto-v4-lastchapter')};
   });
   // Chapter-I reading position can be saved immediately after a reset;
   // puzzle/ending progress must all be cleared.
   reset=!resetState.revealed&&resetState.unexpected.length===0&&(resetState.lastChapter===null||resetState.lastChapter==='chapter-one');
   const info={viewport:vp.name,...basic,modalOpen,modalClosed,unlocked,persisted,reset,resetState,external};
   tests.push(info);
   console.log('WEBKIT',JSON.stringify(info));
   if(!basic.order||basic.width>basic.viewport+2||!basic.heroLoaded||basic.galleryButtons<10||!basic.footerOutside||!modalOpen||!modalClosed||!unlocked||!persisted||!reset||external.length)failed=true;
   if(vp.width<500)await page.screenshot({path:path.join(root,'audit','webkit-mobile-final.jpg'),type:'jpeg',quality:70,fullPage:false});
   await ctx.close();
  }
 }finally{await browser.close();server.kill()}
 if(errors.length)failed=true;
 const report={engine:'WebKit browser engine on Ubuntu, not physical iOS Safari',tests,errors};
 fs.mkdirSync(path.join(root,'audit'),{recursive:true});
 fs.writeFileSync(path.join(root,'audit','webkit-browser-qa.json'),JSON.stringify(report,null,2));
 if(failed)process.exit(1);
})().catch(e=>{console.error('WEBKIT ERROR',e);process.exit(1)});
