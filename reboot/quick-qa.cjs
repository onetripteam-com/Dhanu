const {chromium}=require('playwright');
const {spawn}=require('child_process');
const fs=require('fs');
const assert=require('assert').strict;
(async()=>{
 const server=spawn('python3',['-m','http.server','8764','--bind','127.0.0.1'],{stdio:'ignore'});
 await new Promise(r=>setTimeout(r,650));
 const url='http://127.0.0.1:8764/index.html';
 const browser=await chromium.launch({headless:true,executablePath:process.env.CHROME_PATH||undefined,args:['--no-sandbox']});
 const report={results:[],games:{}};
 try{
  for(const [width,height] of [[360,740],[393,852],[1440,900]]){
   const context=await browser.newContext({viewport:{width,height},isMobile:width<600,hasTouch:width<600,reducedMotion:'reduce'});
   const page=await context.newPage();
   const errors=[];
   page.on('pageerror',e=>errors.push(e.message));
   await page.goto(url,{waitUntil:'load'});
   const x=await page.evaluate(async()=>{
    const imgList=[...document.images]; imgList.forEach(i=>i.loading='eager'); await Promise.all(imgList.map(i=>i.decode().catch(()=>null)));
    return {width:document.documentElement.scrollWidth,viewport:innerWidth,images:[...document.images].filter(i=>!i.naturalWidth).length,chapters:[...document.querySelectorAll('.episode[id]')].map(x=>x.id),portrait:document.querySelector('.cover-illustration img').naturalWidth,portraitTop:Math.round(document.querySelector('.cover-illustration').getBoundingClientRect().top),posterStamp:getComputedStyle(document.querySelector('.cover-illustration'),'::after').display,buttons:document.querySelectorAll('[data-move]').length};
   });
   assert(x.images===0,'image load');
   assert(x.width<=x.viewport+2,'horizontal overflow '+width);
   assert(x.chapters.join(',')==='act1,act2,act3,act4,act5','chapter order');
   assert(x.portrait>0&&x.buttons===6,'portrait and combat controls');
   if(width<600){assert(x.portraitTop<640,'hero artwork must be visible in mobile first screen; top='+x.portraitTop);assert(x.posterStamp==='none','mobile poster stamp should not obscure artwork caption')}
   if(width===393){
    await page.screenshot({path:'reboot/quick-mobile.jpg',type:'jpeg',quality:70});
    const click=async s=>page.locator(s).click({timeout:15000});
    await click('#chase-start');
    for(const n of [2,0,1,2,0]){await click('[data-lane="'+n+'"]');await page.waitForTimeout(640)}
    assert(await page.locator('#reward-chase').isVisible(),'chase');
    await click('[data-combat="sea"] .battle-start');
    for(const m of ['guard','strike','dash','guard','strike']){await click('[data-combat="sea"] [data-move="'+m+'"]');await page.waitForTimeout(650)}
    assert(await page.locator('#reward-sea').isVisible(),'sea');
    await click('[data-mech="brace"]');await click('[data-mech="weight"]');await click('#bell-hit');
    assert(await page.locator('#reward-bell').isVisible(),'bell');
    for(const n of [4,1,3])await click('[data-digit="'+n+'"]');
    await click('#vault-enter');assert(await page.locator('#reward-vault').isVisible(),'vault');
    await click('[data-combat="collector"] .battle-start');
    for(const m of ['guard','dash','strike','guard','dash','strike','strike']){await click('[data-combat="collector"] [data-move="'+m+'"]');await page.waitForTimeout(650)}
    assert(await page.locator('#reward-collector').isVisible(),'final fight');
    await click('[data-last="demand"]');assert(!(await page.locator('#birthday-ending').isVisible()),'dialogue gating');
    await click('[data-last="choose"]');assert(await page.locator('#birthday-ending').isVisible(),'ending');
    await page.reload({waitUntil:'load'});assert(await page.locator('#birthday-ending').isVisible(),'saved progress');
    report.games={chase:true,sea:true,bell:true,vault:true,collector:true,choiceGate:true,endingPersisted:true};
    await page.locator('#birthday-ending').scrollIntoViewIfNeeded();
    await page.screenshot({path:'reboot/quick-ending.jpg',type:'jpeg',quality:70});
   }
   assert(!errors.length,'page errors '+errors.join(','));
   report.results.push({viewport:width,...x,errors});
   console.log('REWIND QA',width,JSON.stringify(x));
   await context.close();
  }
  fs.writeFileSync('reboot/quick-qa.json',JSON.stringify(report,null,2));
  console.log('REWIND / SMOKE QA PASS');
 }finally{await browser.close();server.kill()}
})().catch(e=>{console.error('REWIND / SMOKE QA FAIL',e.stack||e);process.exit(1)});
