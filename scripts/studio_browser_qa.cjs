const {chromium}=require('playwright');
const fs=require('fs');
const path=require('path');
(async()=>{
  const root=path.resolve(__dirname,'..');
  const url='file://'+path.join(root,'index.html');
  const out=path.join(root,'audit');
  fs.mkdirSync(out,{recursive:true});
  const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
  const matrix=[
    {name:'phone-360',width:360,height:740},
    {name:'iphone-393',width:393,height:852},
    {name:'iphone-402',width:402,height:874},
    {name:'tablet-768',width:768,height:1024},
    {name:'desktop-1440',width:1440,height:900}
  ];
  const report={edition:'MANIFESTO Studio Edition II',testedAt:new Date().toISOString(),matrix:[],interactions:{}};
  let failed=false;
  for(const item of matrix){
    const context=await browser.newContext({viewport:{width:item.width,height:item.height},deviceScaleFactor:1,isMobile:item.width<=500,hasTouch:item.width<=500,reducedMotion:'reduce'});
    const page=await context.newPage();
    const errors=[];
    const external=[];
    page.on('pageerror',e=>errors.push(e.message));
    page.on('request',request=>{if(/^https?:/.test(request.url()))external.push(request.url())});
    const t=Date.now();
    await page.goto(url,{waitUntil:'load',timeout:60000});
    await page.waitForTimeout(300);
    const pre=await page.evaluate(async()=>{
      const images=[...document.images];
      images.forEach(img=>{img.loading='eager'});
      await Promise.all(images.map(img=>img.decode().catch(()=>null)));
      const nav=[...document.querySelectorAll('[id^=chapter-]')].filter(x=>['chapter-one','chapter-two','chapter-three','chapter-four','chapter-five'].includes(x.id)).map(x=>x.id);
      const hero=document.querySelector('.manifesto-opening-portrait img');
      const heroRect=hero?.getBoundingClientRect();
      const figures=[...document.querySelectorAll('.story-figure')];
      return {
        order:nav.join(','),
        documentWidth:document.documentElement.scrollWidth,
        viewportWidth:innerWidth,
        brokenImages:images.filter(x=>x.hasAttribute('src')&&Boolean(x.getAttribute('src'))&&(!x.complete||!x.naturalWidth)).map(x=>x.alt),
        images:images.length,
        artButtons:document.querySelectorAll('.figure-zoom').length,
        figures:figures.length,
        hero:{loaded:!!hero?.naturalWidth,width:Math.round(heroRect?.width||0),height:Math.round(heroRect?.height||0),top:Math.round(heroRect?.top||0)},
        footerOutsideFinale:!document.querySelector('.final-reveal footer'),
        oneFinale:document.querySelectorAll('#final-reveal').length===1,
        outdatedText:document.body.innerText.includes('THE FINAL CHAPTER IS BEING WRITTEN'),
        dialogExists:!!document.querySelector('#studio-lightbox'),
        chapterFiveBodyFont:getComputedStyle(document.querySelector('.c5-story>p')).fontFamily,
        gridColumns:getComputedStyle(document.querySelector('.cover-copy')).gridTemplateColumns
      };
    });
    const record={viewport:item.name,loadMs:Date.now()-t,...pre,errors,externalRequests:external};
    if(record.documentWidth>record.viewportWidth+2||record.brokenImages.length||errors.length||external.length||record.order!=='chapter-one,chapter-two,chapter-three,chapter-four,chapter-five'||!record.hero.loaded||!record.footerOutsideFinale||!record.oneFinale||record.outdatedText||record.artButtons<10)failed=true;
    if(['iphone-393','desktop-1440','phone-360'].includes(item.name)){
      await page.screenshot({path:path.join(out,'studio-'+item.name+'.jpg'),type:'jpeg',quality:72,fullPage:false});
    }
    report.matrix.push(record);
    console.log('VIEWPORT',item.name,JSON.stringify({loadMs:record.loadMs,chapterOrder:record.order,allImages:record.images,broken:record.brokenImages.length,docWidth:record.documentWidth,viewportWidth:record.viewportWidth,hero:record.hero,artButtons:record.artButtons,errors:record.errors,external:record.externalRequests.length}));
    if(item.name==='iphone-393'){
      const lightbox=page.locator('#studio-lightbox');
      await page.locator('.figure-zoom').first().click();
      const open=await lightbox.evaluate(e=>e.open);
      await page.locator('#studio-lightbox-zoom').click();
      const zoomed=await lightbox.evaluate(e=>e.classList.contains('studio-zoomed'));
      await page.locator('#studio-lightbox-close').click();
      const closed=await lightbox.evaluate(e=>!e.open);
      await page.locator('#skip-choice').click();
      await page.locator('#signal-skip').click();
      await page.locator('#bell-skip').click();
      await page.locator('#archive-skip').click();
      const afterFour=await page.evaluate(()=>({
        route:document.getElementById('route-reveal')?.classList.contains('show'),
        signal:document.getElementById('ch2-reveal')?.classList.contains('show'),
        bell:document.getElementById('bell-reveal')?.classList.contains('show'),
        archive:document.getElementById('chapter-four-reveal')?.classList.contains('show')
      }));
      await page.locator('[data-final-choice="keep"]').click();
      const gate=await page.locator('#final-reveal').evaluate(e=>!e.classList.contains('show'));
      await page.locator('[data-final-choice="return"]').click();
      const end=await page.locator('#final-reveal').evaluate(e=>e.classList.contains('show'));
      await page.locator('#final-reveal').scrollIntoViewIfNeeded();
      await page.screenshot({path:path.join(out,'studio-finale-393.jpg'),type:'jpeg',quality:72,fullPage:false});
      for(const c of ['chapter-two','chapter-three','chapter-four']){
        await page.locator('#'+c).scrollIntoViewIfNeeded();
        await page.screenshot({path:path.join(out,'studio-'+c+'-393.jpg'),type:'jpeg',quality:70,fullPage:false});
      }
      await page.reload({waitUntil:'load'});
      await page.waitForTimeout(180);
      const persisted=await page.locator('#final-reveal').evaluate(e=>e.classList.contains('show'));
      const footerVisible=await page.locator('.footer').evaluate(e=>!!e.getClientRects().length);
      report.interactions={lightbox:{open,zoomed,closed},puzzles:afterFour,finalChoiceGate:gate,finaleUnlocked:end,persisted,footerVisible};
      if(errors.length)failed=true;
      if(!open||!zoomed||!closed||Object.values(afterFour).some(x=>!x)||!gate||!end||!persisted||!footerVisible){failed=true;console.error('INTERACTION FAILED',JSON.stringify(report.interactions))}
      console.log('INTERACTIONS',JSON.stringify(report.interactions));
    }
    await context.close();
  }
  fs.writeFileSync(path.join(out,'studio-browser-qa.json'),JSON.stringify(report,null,2));
  await browser.close();
  if(failed)process.exit(1);
})().catch(e=>{console.error('BROWSER QA EXCEPTION',e);process.exit(1)});
