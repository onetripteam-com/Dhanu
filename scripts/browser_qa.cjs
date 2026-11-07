const {chromium}=require('playwright');
const fs=require('fs');
const path=require('path');
(async()=>{
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 const url='file://'+path.resolve(__dirname,'../index.html');
 const cases=[
  {name:'mobile-393',width:393,height:852,isMobile:true,deviceScaleFactor:1},
  {name:'mobile-360',width:360,height:740,isMobile:true,deviceScaleFactor:1},
  {name:'desktop-1440',width:1440,height:900,isMobile:false,deviceScaleFactor:1}
 ];
 const result={testedAt:new Date().toISOString(),cases:[]};
 fs.mkdirSync(path.resolve(__dirname,'../audit'),{recursive:true});
 for(const v of cases){
   const ctx=await browser.newContext({viewport:{width:v.width,height:v.height},isMobile:v.isMobile,deviceScaleFactor:1,hasTouch:v.isMobile,reducedMotion:'reduce'});
   const page=await ctx.newPage();
   const errors=[];
   page.on('pageerror',e=>errors.push(e.message));
   await page.goto(url,{waitUntil:'load',timeout:60000});
   await page.waitForTimeout(600);
   const data=await page.evaluate(()=>{
     const ids=['chapter-one','chapter-two','chapter-three','chapter-four','chapter-five'];
     const nodeList=ids.map(x=>document.getElementById(x));
     const picture=document.querySelector('.manifesto-opening-portrait img');
     const rect=picture?.getBoundingClientRect();
     const allImgs=[...document.querySelectorAll('img')];
     const failed=allImgs.filter(i=>!i.complete||i.naturalWidth===0).map(x=>x.alt.slice(0,80));
     const huge=[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.right>innerWidth+8&&getComputedStyle(e).position!=='fixed'}).slice(0,6).map(e=>({tag:e.tagName,cls:String(e.className).slice(0,60),right:Math.round(e.getBoundingClientRect().right)}));
     return {chapterOrder:nodeList.every(Boolean)&&nodeList.every((x,i)=>!i||nodeList[i-1].compareDocumentPosition(x)&Node.DOCUMENT_POSITION_FOLLOWING),
       chapterOffsets:nodeList.map(x=>x?.offsetTop),documentWidth:document.documentElement.scrollWidth,viewportWidth:innerWidth,
       hero:{visible:!!rect&&rect.width>180&&rect.height>100,rect:rect&&{width:Math.round(rect.width),height:Math.round(rect.height),top:Math.round(rect.top)},loaded:!!picture?.naturalWidth},
       images:allImgs.length,failedImages:failed,
       finaleCount:document.querySelectorAll('#chapter-five').length,
       removedIframe:!document.querySelector('#manifesto-finale-frame'),
       outdatedCopy:document.body.innerText.includes('THE FINAL CHAPTER IS BEING WRITTEN'),
       overflowElements:huge};
   });
   await page.screenshot({path:path.resolve(__dirname,'../audit/preview-'+v.name+'.jpg'),type:'jpeg',quality:68,fullPage:false});
   result.cases.push({viewport:v.name,...data,errors});
   console.log('QA',v.name,JSON.stringify({order:data.chapterOrder,scroll:data.documentWidth,viewport:data.viewportWidth,hero:data.hero,failedImages:data.failedImages.length,errors,overflow:data.overflowElements}));
   await ctx.close();
 }
 fs.writeFileSync(path.resolve(__dirname,'../audit/browser-qa.json'),JSON.stringify(result,null,2));
 await browser.close();
 if(result.cases.some(r=>!r.chapterOrder||!r.hero.visible||!r.hero.loaded||r.finaleCount!==1||!r.removedIframe||r.outdatedCopy||r.failedImages.length))process.exit(1);
})().catch(e=>{console.error(e);process.exit(1)});
