const {chromium,webkit}=require('playwright');
const {spawn}=require('child_process');
const fs=require('fs');
const path=require('path');
const assert=require('assert').strict;

(async()=>{
 const root=path.resolve(__dirname,'..');
 const reportDir=path.join(root,'reboot','qa-results');
 fs.mkdirSync(reportDir,{recursive:true});
 const server=spawn('python3',['-m','http.server','8729','--bind','127.0.0.1'],{cwd:root,stdio:'ignore'});
 const url='http://127.0.0.1:8729/index.html';
 const wait=ms=>new Promise(r=>setTimeout(r,ms));
 await wait(900);
 const report={version:'MANIFESTO REWIND',tests:[],functional:{},errors:[]};
 async function run(engine,opts){
  const browser=await engine.launch({headless:true,args:engine===chromium?['--no-sandbox']:[]});
  const context=await browser.newContext({viewport:{width:opts.w,height:opts.h},isMobile:opts.w<600,hasTouch:opts.w<600,deviceScaleFactor:1,reducedMotion:'reduce'});
  const page=await context.newPage();
  const errors=[],external=[];
  page.on('pageerror',e=>errors.push(e.message));
  page.on('request',r=>{if(/^https?:/.test(r.url())&&!r.url().startsWith('http://127.0.0.1:8729/'))external.push(r.url())});
  await page.goto(url,{waitUntil:'load',timeout:60000});
  await page.waitForTimeout(250);
  const basics=await page.evaluate(async()=>{
   const images=[...document.images];
   images.forEach(img=>img.loading='eager');
   await Promise.all(images.map(img=>img.decode().catch(()=>null)));
   const sections=['act1','act2','act3','act4','act5'].map(x=>document.getElementById(x));
   const picture=document.querySelector('.cover-illustration img');
   const r=picture.getBoundingClientRect();
   return {
    order:sections.every(Boolean)&&sections.every((x,i)=>!i||sections[i-1].compareDocumentPosition(x)&Node.DOCUMENT_POSITION_FOLLOWING),
    hasFiveChallenges:!!document.querySelector('#chase-game')&&document.querySelectorAll('[data-combat]').length===2&&!!document.querySelector('#bell-game')&&!!document.querySelector('#vault-game'),
    images:images.length,
    brokenImages:images.filter(img=>!img.complete||!img.naturalWidth).map(img=>img.alt),
    width:document.documentElement.scrollWidth,viewportWidth:innerWidth,
    hero:{loaded:picture.complete&&picture.naturalWidth>0,width:Math.round(r.width),height:Math.round(r.height)},
    title:document.title,
    links:[...document.querySelectorAll('.chapter-nav a')].length,
    choices:document.querySelectorAll('[data-last]').length,
    hash:window.location.hash
   };
  });
  assert(basics.order,'chapter order');
  assert(basics.hasFiveChallenges,'challenges exist');
  assert(basics.brokenImages.length===0,'broken artwork: '+JSON.stringify(basics.brokenImages));
  assert(basics.hero.loaded && basics.hero.width>200,'hero artwork loads');
  assert(basics.width<=basics.viewportWidth+2,'overflow '+opts.w+' '+basics.width);
  assert(basics.choices===3,'final choices');
  assert(external.length===0,'no external requests');
  await page.screenshot({path:path.join(reportDir,opts.name+'.jpg'),type:'jpeg',quality:70,fullPage:false});
  report.tests.push({name:opts.name,...basics,external,errors});
  console.log('VISUAL',opts.name,JSON.stringify({...basics,brokenImages:basics.brokenImages.length,errors}));
  if(opts.play){
    const fire=async(selector)=>{await page.locator(selector).click({timeout:15000})};
    await fire('#chase-start');
    const routes=[2,0,1,2,0];
    for(let i=0;i<routes.length;i++){
      await fire('[data-lane="'+routes[i]+'"]');
      await page.waitForTimeout(660);
    }
    assert(await page.locator('#reward-chase').isVisible(),'chase reward');
    assert(await page.locator('#continue-story').isVisible(),'continue appears after first mission');
    assert(await page.locator('#continue-story').getAttribute('href')==='#act2','continue points to next mission');

    await fire('[data-combat="sea"] .battle-start');
    await fire('[data-combat="sea"] [data-move="strike"]'); // deliberate wrong move
    await page.waitForTimeout(520);
    assert(await page.locator('[data-combat="sea"] .hero-health').innerText()==='♥ ♥','wrong move costs a heart');
    for(const move of ['guard','strike','dash','guard','strike']){
      await fire('[data-combat="sea"] [data-move="'+move+'"]');
      await page.waitForTimeout(720);
    }
    assert(await page.locator('#reward-sea').isVisible(),'sea reward');

    await fire('#bell-hit'); // deliberate incorrect order
    assert((await page.locator('#bell-feedback').innerText()).includes('BEFORE hitting'),'bell explains mechanics');
    await fire('[data-mech="brace"]');
    await fire('[data-mech="weight"]');
    await fire('#bell-hit');
    assert(await page.locator('#reward-bell').isVisible(),'bell reward');

    for(const digit of ['4','1','3'])await fire('[data-digit="'+digit+'"]');
    await fire('#vault-enter');
    assert(await page.locator('#reward-vault').isVisible(),'vault reward');

    await fire('[data-combat="collector"] .battle-start');
    for(const move of ['guard','dash','strike','guard','dash','strike','strike']){
      await fire('[data-combat="collector"] [data-move="'+move+'"]');
      await page.waitForTimeout(720);
    }
    assert(await page.locator('#reward-collector').isVisible(),'collector reward');
    assert(await page.locator('#last-choice').isVisible(),'choice becomes available');
    await fire('[data-last="demand"]');
    assert(!(await page.locator('#birthday-ending').isVisible()),'demand does not skip ethical choice');
    await fire('[data-last="choose"]');
    assert(await page.locator('#birthday-ending').isVisible(),'birthday ending');
    await page.screenshot({path:path.join(reportDir,'finale.jpg'),type:'jpeg',quality:70,fullPage:false});
    const completed=await page.evaluate(()=>Object.keys(localStorage).filter(k=>k.startsWith('manifesto-rewind:v1:')).sort());
    for(const id of ['chase','sea','bell','vault','collector','ending'])assert(completed.includes('manifesto-rewind:v1:'+id),'missing completion '+id);
    assert(await page.locator('#story-clock').innerText()==='12:00','the clock must move after the finale');
    await fire('#keepsake-letter summary');
    assert(await page.locator('#gift-note-content').isVisible(),'signed keepsake opens');
    assert((await page.locator('#gift-note-content').innerText()).includes('later than I wanted'),'belated gift note');
    const downloadWait=page.waitForEvent('download');
    await fire('#keep-letter');
    const noteDownload=await downloadWait;
    assert(noteDownload.suggestedFilename()==='A-Note-For-Dhanu.txt','downloadable personal note');
    assert(await page.locator('#continue-story').getAttribute('href')==='#birthday-ending','resume should revisit completed ending');
    await page.reload({waitUntil:'load'});
    assert(await page.locator('#birthday-ending').isVisible(),'finale persists');
    assert(await page.locator('#reward-collector').isVisible(),'collector persists');
    page.once('dialog',d=>d.accept());
    await fire('#replay-game');
    await page.waitForLoadState('load');
    await page.waitForTimeout(220);
    const reset=await page.evaluate(()=>({progress:Object.keys(localStorage).filter(k=>k.startsWith('manifesto-rewind:v1:')),ending:!document.querySelector('#birthday-ending').hidden}));
    assert(reset.progress.length===0&&!reset.ending,'replay resets all but no old progress');
    report.functional={chase:true,sea:true,wrongMoveHealth:true,bell:true,bellEarlyStrike:true,vault:true,collector:true,finalChoiceGate:true,endingSaved:true,reset:true};
    console.log('FUNCTIONAL',JSON.stringify(report.functional));
  }
  if(errors.length)throw Error(opts.name+' browser JS errors: '+errors.join('; '));
  await context.close();await browser.close();
 }
 try{
  await run(chromium,{name:'chromium-360',w:360,h:740});
  await run(chromium,{name:'chromium-393',w:393,h:852,play:true});
  await run(chromium,{name:'chromium-402',w:402,h:874});
  await run(chromium,{name:'chromium-1440',w:1440,h:900});
  await run(webkit,{name:'webkit-393',w:393,h:852});
  await run(webkit,{name:'webkit-1440',w:1440,h:900});
  fs.writeFileSync(path.join(reportDir,'results.json'),JSON.stringify(report,null,2));
  console.log('ALL TESTS PASSED');
 }catch(e){
  report.errors.push(String(e.stack||e));
  fs.writeFileSync(path.join(reportDir,'results.json'),JSON.stringify(report,null,2));
  console.error('TEST FAILED',e.stack||e);
  process.exitCode=1;
 }finally{server.kill()}
})().catch(e=>{console.error(e);process.exit(1)});
