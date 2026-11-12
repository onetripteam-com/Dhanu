(()=>{
'use strict';
const KEY='manifesto-rewind:v1:';
const reduced=window.matchMedia('(prefers-reduced-motion: reduce)');
const $=s=>document.querySelector(s);
const $$=s=>[...document.querySelectorAll(s)];
const has=id=>{try{return localStorage.getItem(KEY+id)==='done'}catch(e){return false}};
const save=id=>{try{localStorage.setItem(KEY+id,'done')}catch(e){}};
const moveTo=id=>document.getElementById(id)?.scrollIntoView({behavior:reduced.matches?'auto':'smooth',block:'start'});
const reveal=id=>{const el=document.getElementById(id);if(el)el.hidden=false};
const toast=$('#toast');
let toastTimer;
function notify(text){
 if(!toast)return;
 toast.textContent=text;toast.hidden=false;
 clearTimeout(toastTimer);
 toastTimer=setTimeout(()=>{toast.hidden=true},2700);
}
function finish(id,{jump=true}={}){
 if(!has(id))save(id);
 renderExperienceProgress();
 const rid='reward-'+id;
 reveal(rid);
 if(id==='collector')reveal('last-choice');
 if(jump)setTimeout(()=>moveTo(rid),440);
 notify('MISSION CLEARED / STORY CONTINUES');
}

// --- Chapter menu, reading progress, and scroll position ---
const toggle=$('#nav-toggle'),nav=$('#chapternav');
toggle?.addEventListener('click',()=>{
 const open=toggle.getAttribute('aria-expanded')!=='true';
 toggle.setAttribute('aria-expanded',String(open));
 nav.classList.toggle('open',open);
});
$$('.chapter-nav a').forEach(link=>link.addEventListener('click',()=>{
 nav.classList.remove('open');toggle?.setAttribute('aria-expanded','false');
}));
const titles={prologue:'PROLOGUE',act1:'ROOFTOP CHASE',act2:'SEA DUEL',act3:'THOUSANDTH BELL',act4:'VESPER HEIST',act5:'FINAL BOSS'};
let lastRemembered=null;
function activeSection(){
 const y=window.scrollY+140;
 let active='prologue';
 for(const id of Object.keys(titles)){
   const node=document.getElementById(id);
   if(node&&node.offsetTop<=y)active=id;
 }
 $$('#chapternav a').forEach(a=>{
   if(a.dataset.actNav===active)a.setAttribute('aria-current','location');
   else a.removeAttribute('aria-current');
 });
 $('#current-act').textContent=titles[active];
 if(window.scrollY>220 && active!==lastRemembered){
   lastRemembered=active;
   try{localStorage.setItem(KEY+'last-act',active)}catch(e){}
 }
 const max=document.documentElement.scrollHeight-window.innerHeight;
 $('#read-fill').style.width=(max>0?Math.round(Math.min(1,window.scrollY/max)*100):0)+'%';
}
let scrollWait=false;
window.addEventListener('scroll',()=>{
 if(scrollWait)return;
 scrollWait=true;
 requestAnimationFrame(()=>{scrollWait=false;activeSection()});
},{passive:true});
window.addEventListener('resize',activeSection);
window.addEventListener('hashchange',activeSection);
activeSection();

// --- Gift journey: recover progress without interrupting the canonical story ---
const missionSteps=[
 {key:'chase',target:'act1',label:'01 / ROOFTOP RUN'},
 {key:'sea',target:'act2',label:'02 / SEA DUEL'},
 {key:'bell',target:'act3',label:'03 / THE BELL'},
 {key:'vault',target:'act4',label:'04 / VESPER VAULT'},
 {key:'collector',target:'act5',label:'05 / FINAL DUEL'}
];
function savedBookmark(){
 try{
  const id=localStorage.getItem(KEY+'last-act');
  return ['act1','act2','act3','act4','act5'].includes(id)?id:null;
 }catch(e){return null}
}
function renderExperienceProgress(){
 const cleared=missionSteps.filter(step=>has(step.key)).length;
 const next=missionSteps.find(step=>!has(step.key));
 const progress=$('#missions-completed'),bar=$('#mission-meter-fill');
 if(progress)progress.textContent=cleared+' / 5 CHALLENGES CLEARED'+(has('ending')?' · MIDNIGHT RESTORED':'');
 if(bar)bar.style.width=(cleared/5*100)+'%';
 $('.mission-grid a').forEach((card,index)=>{
  const step=missionSteps[index];
  if(!step)return;
  const done=has(step.key);
  card.classList.toggle('cleared',done);
  const state=card.querySelector('.mission-state')||document.createElement('strong');
  state.className='mission-state';
  state.textContent=done?'✓ CLEARED':step===next?'◷ NEXT MISSION':'◇ AVAILABLE';
  if(!state.isConnected)card.appendChild(state);
 });
 const clock=$('#story-clock');
 if(clock)clock.textContent=has('ending')?'12:00':'11:59';
 const resume=$('#continue-story'),copy=$('#cover-progress');
 if(!resume)return;
 if(has('ending')){
  resume.hidden=false;resume.href='#birthday-ending';resume.textContent='REVISIT THE ENDING ↗';
  if(copy)copy.textContent='The clock is moving again. Your story is always here.';
  return;
 }
 const bookmark=savedBookmark();
 if(cleared||bookmark){
  const nextIndex=next?missionSteps.indexOf(next):4;
  const lastIndex=bookmark?missionSteps.findIndex(step=>step.target===bookmark):-1;
  const target=has('collector')?'last-choice':missionSteps[Math.max(nextIndex,lastIndex,0)].target;
  resume.hidden=false;resume.href='#'+target;
  resume.textContent=has('collector')?'CONTINUE TO THE FINAL CHOICE ↗':'CONTINUE YOUR ADVENTURE ↗';
  if(copy)copy.textContent=cleared+' of 5 challenges cleared · Your place is saved on this device.';
 }else{
  resume.hidden=true;
  if(copy)copy.textContent='Your story begins whenever you’re ready.';
 }
}
renderExperienceProgress();

// Keep the signed message as an offline keepsake; no account, API or tracking.
$('#keep-letter')?.addEventListener('click',()=>{
 const note=$('#gift-note-content');
 if(!note)return;
 const content="MANIFESTO: REWIND — A NOTE FOR DHANU\n\n"+note.innerText.replace(/SAVE THIS NOTE ↓/g,'').trim()+"\n";
 const file=new Blob([content],{type:'text/plain;charset=utf-8'});
 const href=URL.createObjectURL(file);
 const link=document.createElement('a');
 link.href=href;link.download='A-Note-For-Dhanu.txt';
 document.body.appendChild(link);link.click();link.remove();
 setTimeout(()=>URL.revokeObjectURL(href),1000);
 notify('YOUR NOTE IS READY TO KEEP');
});

// --- Rooftop chase: FIVE real reaction rounds with limited time, safe lane telegraph ---
const chaseBoard=$('#chase-game');
const laneButtons=$$('#chase-lanes [data-lane]');
const chaseStart=$('#chase-start'),chaseSkip=$('#chase-skip');
const chaseFeedback=$('#chase-feedback');
const safeSequence=[2,0,1,2,0];
const mishaps=[
 'Chain across your shoulder! Nix: "Try moving AWAY from the shiny metal!"',
 'A guard cuts you off. Dhanu: "I saw that coming." Nix: "Then why are we here?"',
 'You lose a heart. Nix: "Personal space, please. From the sword."'
];
let chase={running:false,step:0,hp:3,timer:null,deadline:0,locked:false};
function chaseStop(){
 if(chase.timer!==null){clearInterval(chase.timer);chase.timer=null}
}
function chaseUpdateHearts(){
 $('#chase-hearts').textContent='♥ '.repeat(chase.hp).trim()+'  ·  '+(3-chase.hp)+' HIT'+(3-chase.hp===1?'':'S');
}
function chaseDisable(){laneButtons.forEach(b=>b.disabled=true)}
function chaseSetup(){
 chase.locked=false;
 $('#chase-level').textContent='ROOFTOP '+(chase.step+1)+' / 5';
 const safe=safeSequence[chase.step];
 const names=['LEFT','CENTRE','RIGHT'];
 laneButtons.forEach((b,i)=>{
  b.disabled=false;
  b.classList.toggle('safe',i===safe);
  b.classList.toggle('danger',i!==safe);
  b.classList.remove('selected');
  b.querySelector('small').textContent=i===safe?'GAP OPEN':'CHAIN BLOCKED';
  b.setAttribute('aria-label',names[i]+(i===safe?' lane open':' lane blocked'));
 });
 chaseFeedback.textContent='MOVE! The green lane is safe. 3.5 seconds before the next chain.';
 chase.deadline=performance.now()+3500;
 $('#chase-timer').style.width='100%';
 chaseStop();
 chase.timer=setInterval(()=>{
   if(!chase.running||document.hidden){chase.deadline=performance.now()+3500;return}
   const remain=Math.max(0,chase.deadline-performance.now());
   $('#chase-timer').style.width=(remain/3500*100).toFixed(1)+'%';
   if(remain<=0){chaseHit('The hunters caught you standing still. Nix: "We were going for the MOVING part."')}
 },40);
}
function chaseHit(message){
 if(chase.locked||!chase.running)return;
 chaseStop();chase.locked=true;chase.hp--;
 chaseFeedback.textContent=message;
 if(chase.hp<=0){
  chase.hp=3;
  chaseFeedback.textContent+=' Nix grabs your collar. Three more hearts. No game-over screen on your birthday.';
 }
 chaseUpdateHearts();
 chaseDisable();
 setTimeout(()=>{if(chase.running)chaseSetup()},750);
}
function chaseChoose(n){
 if(!chase.running||chase.locked)return;
 if(n!==safeSequence[chase.step]){
   laneButtons[n]?.classList.add('selected');
   chaseHit(mishaps[(chase.step+n)%mishaps.length]);return;
 }
 chaseStop();chase.locked=true;
 laneButtons[n]?.classList.add('selected');chaseDisable();
 chase.step++;
 chaseFeedback.textContent=['First roof cleared!','Two jumps down. Nix is screaming, professionally.','The hunters are losing ground!','The harbour is in sight.','LAST JUMP! Dhanu lands on the ghost ship.'][chase.step-1];
 if(chase.step>=5){
   chase.running=false;chaseStart.hidden=true;chaseSkip.hidden=true;
   $('#chase-timer').style.width='100%';
   finish('chase');return;
 }
 setTimeout(()=>{if(chase.running)chaseSetup()},570);
}
chaseStart.addEventListener('click',()=>{
 chaseStop();chase={running:true,step:0,hp:3,timer:null,deadline:0,locked:false};
 chaseStart.hidden=true;chaseUpdateHearts();chaseSetup();
});
chaseSkip.addEventListener('click',()=>{
 chaseStop();chase.running=false;chaseDisable();chaseStart.hidden=true;chaseSkip.hidden=true;
 chaseFeedback.textContent='Nix shows Dhanu a shortcut through the guard patrols. Story mode engaged.';
 finish('chase');
});
laneButtons.forEach(b=>b.addEventListener('click',()=>chaseChoose(Number(b.dataset.lane))));
if(has('chase')){
 chaseStart.hidden=true;chaseSkip.hidden=true;chaseDisable();
 chaseFeedback.textContent='Rooftop chase cleared. The harbour is yours.';
 finish('chase',{jump:false});
}

// --- Tactical fights: visible tells, true move choices, health and phase changes ---
const bouts={
 sea:{
  name:'IRON MARINER', reward:'sea', rounds:[
   {move:'guard',tell:'HEAVY OVERHEAD SLASH: the iron sword rises above its head. GUARD the blow.',success:'CLANG! Dhanu catches the strike on his blade. Nix: "That was genuinely cool."'},
   {move:'strike',tell:'OPEN CORE: a crack of gold appears across its chest. STRIKE now.',success:'DIRECT HIT! Its armor splits. Dhanu: "There we go."'},
   {move:'dash',tell:'DECK BREAK: the planks below you glow red and split. DASH away.',success:'Dhanu leaps clear as the ship folds beneath his feet.'},
   {move:'guard',tell:'BRUTAL CHARGE: both iron fists come forward. GUARD!',success:'The charge rebounds. Nix: "Lovely. The ship lost the argument."'},
   {move:'strike',tell:'FINAL OPENING: the Mariner stumbles, its core wide open. STRIKE.',success:'FINISHER! Dhanu breaks the iron core. The sea answers with a thunderclap.'}
  ]
 },
 collector:{
  name:'THE COLLECTOR',reward:'collector',rounds:[
   {move:'guard',tell:'THE HAMMER FALLS: both hands lift the bronze hourglass. GUARD.',success:'Dhanu braces. The entire stairwell cracks under the impact.'},
   {move:'dash',tell:'TIME RIFT: the floor glows like a shattered clock. DASH out of its path.',success:'A whole second breaks where Dhanu stood. He is already gone.'},
   {move:'strike',tell:'EXPOSED HEART: the Collector opens his clockwork chest. STRIKE.',success:'The first armour plate flies across the tower.'},
   {move:'guard',tell:'PHASE TWO — THE COLLECTOR ROARS. A wave of golden blades descends. GUARD.',success:'BEGIN and RETURN flash. Dhanu blocks a storm of frozen seconds.'},
   {move:'dash',tell:'SECOND HAND SWEEP: a giant metal needle sweeps the floor. DASH!',success:'Dhanu vaults the needle and lands behind the Collector.'},
   {move:'strike',tell:'A CRACK RUNS THROUGH ITS ARMOUR. STRIKE the broken plate.',success:'WITNESS ignites. The watch exposes the Collector’s final weakness.'},
   {move:'strike',tell:'FINAL OPENING: all three gears align. STRIKE NOW!',success:'LAST HIT! The Collector shatters. The clock still waits for one choice.'}
  ]
 }
};
let activeCombat=null;
function bindCombat(el){
 const id=el.dataset.combat;
 const config=bouts[id];
 const start=el.querySelector('.battle-start');
 const skip=el.querySelector('.battle-skip');
 const actions=[...el.querySelectorAll('[data-move]')];
 const stage=el.querySelector('.battle-stage');
 const tell=el.querySelector('.boss-tell');
 const feedback=el.querySelector('.battle-feedback');
 const hero=el.querySelector('.hero-health');
 const boss=el.querySelector('.boss-health');
 let step=0,hp=3,running=false,locked=false;
 function refresh(){
   hero.textContent='♥ '.repeat(hp).trim();
   boss.textContent=step+' / '+config.rounds.length;
   if(step<config.rounds.length)tell.textContent=config.rounds[step].tell;
 }
 function battleDone(){
  running=false;locked=true;activeCombat=null;
  actions.forEach(b=>b.disabled=true);
  start.hidden=true;skip.hidden=true;
  tell.textContent='BOSS DEFEATED / THE FIGHT IS OVER';
  feedback.textContent=id==='sea'?'The Iron Mariner falls. One gear glows in the wreckage.':'The Collector is defeated. But the clock is still stopped.';
  finish(config.reward);
 }
 function action(move){
  if(!running||locked)return;
  const round=config.rounds[step];
  if(move===round.move){
    locked=true;step++;refresh();
    stage.classList.remove('hurt');stage.classList.remove('hit');void stage.offsetWidth;stage.classList.add('hit');
    feedback.textContent=round.success;
    if(step>=config.rounds.length){setTimeout(battleDone,420);return}
    setTimeout(()=>{
     locked=false;
     if(id==='collector'&&step===3)stage.classList.add('enraged');
     refresh();
    },580);
  }else{
    locked=true;hp--;
    stage.classList.remove('hit');stage.classList.remove('hurt');void stage.offsetWidth;stage.classList.add('hurt');
    const hints={strike:'Attacking now leaves Dhanu open.',guard:'A guard cannot stop that hazard.',dash:'Dashing now gives the boss a clean hit.'};
    feedback.textContent=(hints[move]||'Wrong read.')+' Nix: "He literally telegraphed the move!"';
    if(hp<=0){
       hp=3;
       feedback.textContent+=' Nix pulls Dhanu free. Hearts restored. Try the same tell again.';
    }
    hero.textContent='♥ '.repeat(hp).trim();
    setTimeout(()=>{locked=false},500);
  }
 }
 actions.forEach(b=>b.addEventListener('click',()=>action(b.dataset.move)));
 start.addEventListener('click',()=>{
   running=true;locked=false;step=0;hp=3;activeCombat={id,action};
   start.hidden=true;actions.forEach(b=>b.disabled=false);
   refresh();feedback.textContent='Watch the tell. Read it. Move with purpose.';
 });
 skip.addEventListener('click',()=>{
   running=false;locked=true;activeCombat=null;
   actions.forEach(b=>b.disabled=true);start.hidden=true;skip.hidden=true;
   step=config.rounds.length;refresh();
   feedback.textContent='Story mode: Dhanu wins with a last-second assist from his crew.';
   finish(config.reward);
 });
 actions.forEach(b=>b.disabled=true);
 if(has(config.reward)){
    step=config.rounds.length;
    actions.forEach(b=>b.disabled=true);start.hidden=true;skip.hidden=true;
    tell.textContent='BOSS DEFEATED';
    hero.textContent='♥ ♥ ♥';boss.textContent=step+' / '+config.rounds.length;
    feedback.textContent='Already defeated. The story continues.';
    finish(config.reward,{jump:false});
 }
}
$$('[data-combat]').forEach(bindCombat);

// --- Third challenge: genuinely interactive mechanism, not an arbitrary tap count ---
const mechButtons=$$('[data-mech]');
const machine=$('.machine-stage');
const mechState={brace:false,weight:false,completed:has('bell')};
function finishBell({jump=true}={}){
 mechState.completed=true;
 machine.classList.add('fixed');
 $('#machine-status').textContent='THE THOUSANDTH BELL RINGS!';
 $('#bell-feedback').textContent='The brace is released. The balance is aligned. One clean strike breaks the loop.';
 $('#bell-skip').hidden=true;
 mechButtons.forEach(b=>b.disabled=true);
 $('#bell-hit').disabled=true;
 finish('bell',{jump});
}
mechButtons.forEach(b=>b.addEventListener('click',()=>{
 if(mechState.completed)return;
 const key=b.dataset.mech;
 mechState[key]=!mechState[key];
 b.setAttribute('aria-pressed',String(mechState[key]));
 const details=key==='brace'?'Iron brace '+(mechState[key]?'released.':'fastened again.'):'Counterweight '+(mechState[key]?'aligned.':'misaligned again.');
 $('#bell-feedback').textContent=details+' '+(mechState.brace&&mechState.weight?'NOW STRIKE!':'Check the other part.');
 $('#machine-status').textContent=mechState.brace&&mechState.weight?'THE BELL CAN MOVE!':'MECHANISM ADJUSTED · NOT READY';
}));
$('#bell-hit').addEventListener('click',()=>{
 if(mechState.completed)return;
 if(mechState.brace&&mechState.weight){finishBell();return}
 machine.classList.remove('fixed');void machine.offsetWidth;machine.classList.add('rattled');
 $('#bell-feedback').textContent='KRRANG! The ogre grows stronger. Nix: "Perhaps we fix the machine BEFORE hitting it?"';
});
$('#bell-skip').addEventListener('click',()=>finishBell());
if(mechState.completed)finishBell({jump:false});

// --- Vault heist: code must be deciphered from three on-screen clues ---
const vaultInput=[];
let vaultAlert=0;
const vault=$('.vault-screen');
const digitField=$('#vault-digits');
function vaultRender(){digitField.textContent=Array.from({length:3},(_,i)=>vaultInput[i]||'—').join('  ')}
function finishVault({jump=true}={}){
 $$('[data-digit]').forEach(b=>b.disabled=true);
 $('#vault-enter').disabled=true;$('#vault-clear').disabled=true;$('#vault-skip').hidden=true;
 $('#vault-feedback').textContent='LOCK OPEN. Dhanu: "Did you see that?" Siri: "I wrote the clues. Yes."';
 $('#vault-alert').textContent='ACCESS GRANTED / THE OFFICE IS OPEN';
 vault.classList.remove('warning');
 digitField.textContent='4  1  3';
 finish('vault',{jump});
}
$$('[data-digit]').forEach(b=>b.addEventListener('click',()=>{
 if(has('vault'))return;
 if(vaultInput.length>=3)return;
 vaultInput.push(b.dataset.digit);
 vaultRender();
}));
$('#vault-clear').addEventListener('click',()=>{
 vaultInput.length=0;vaultRender();
 $('#vault-feedback').textContent='Code cleared. Three clues, three digits.';
});
$('#vault-enter').addEventListener('click',()=>{
 if(has('vault'))return;
 if(vaultInput.length!==3){$('#vault-feedback').textContent='Siri: "Three digits, Dhanu. THREE."';return}
 if(vaultInput.join('')==='413'){finishVault();return}
 vaultAlert++;vault.classList.remove('warning');void vault.offsetWidth;vault.classList.add('warning');
 $('#vault-alert').textContent='ALERT LEVEL: '+(vaultAlert===1?'SUSPICIOUS':vaultAlert===2?'HIGH':'VERY HIGH');
 $('#vault-feedback').textContent=vaultAlert<3?'The lock buzzes. A Clockguard turns toward the vault. Try again.':'Siri: "It is the number of gears, then minutes, then the shelf. Please stop guessing."';
 vaultInput.length=0;vaultRender();
 setTimeout(()=>vault.classList.remove('warning'),550);
});
$('#vault-skip').addEventListener('click',()=>finishVault());
vaultRender();
if(has('vault'))finishVault({jump:false});

// --- Final choice; the fourth gear is offered, never seized ---
const lastFeedback=$('#last-feedback');
function confetti(){
 if(reduced.matches)return;
 const container=$('#birthday-ending');
 if(container.dataset.celebrated)return;
 container.dataset.celebrated='true';
 const flakes=document.createElement('div');
 flakes.setAttribute('aria-hidden','true');flakes.className='confetti-layer';
 flakes.style.cssText='position:absolute;inset:0;z-index:3;overflow:hidden;pointer-events:none';
 const colors=['#edc08b','#f3e8d6','#a2c7bc','#c16d58'];
 for(let i=0;i<60;i++){
  const el=document.createElement('i');
  const x=(i*37+19)%100;
  const delay=(i*13%25)/10;
  const duration=3+(i*17%30)/10;
  el.style.cssText='position:absolute;top:-25px;left:'+x+'%;width:'+(5+i%4)+'px;height:'+(8+i%6)+'px;background:'+colors[i%4]+';opacity:.9;animation:fall '+duration+'s '+delay+'s linear forwards;transform:rotate('+(i*17)+'deg)';
  flakes.appendChild(el);
 }
 const style=document.createElement('style');
 style.textContent='@keyframes fall{to{transform:translate('+ (8) +'vw,110vh) rotate(720deg);opacity:.05}}';
 container.append(style,flakes);
 setTimeout(()=>flakes.remove(),7800);
}
function endStory({jump=true}={}){
 save('ending');
 reveal('birthday-ending');
 renderExperienceProgress();
 $('#last-skip').hidden=true;
 $$('[data-last]').forEach(b=>b.disabled=true);
 lastFeedback.textContent='He takes off the last gear. Not because Dhanu demanded it, but because he finally understands.';
 if(jump){
   confetti();
   setTimeout(()=>moveTo('birthday-ending'),300);
 }
}
$$('[data-last]').forEach(btn=>btn.addEventListener('click',()=>{
 if(has('ending'))return;
 $$('[data-last]').forEach(b=>b.removeAttribute('aria-pressed'));
 btn.setAttribute('aria-pressed','true');
 const choice=btn.dataset.last;
 if(choice==='choose'){endStory();return}
 if(choice==='demand'){
  lastFeedback.textContent='Future Dhanu closes his hand. "Taking a choice is not the same as making one." Nix stays quiet. Try speaking to him, not winning.';
 }else{
  lastFeedback.textContent='Future Dhanu shakes his head. "I begged for guarantees. They were my prison." Dhanu needs a braver answer than another promise.';
 }
}));
$('#last-skip').addEventListener('click',()=>endStory());
if(has('collector'))reveal('last-choice');
else $('#last-choice').hidden=true;
if(has('ending'))endStory({jump:false});

// Complete a second time without deleting progress can replay earlier mini-games only via reset
function reset(){
 if(!window.confirm('Reset your MANIFESTO: REWIND mission progress on this device? All five challenges and the finale will be playable again.'))return;
 try{
   for(const k of Object.keys(localStorage))if(k.startsWith(KEY))localStorage.removeItem(k);
 }catch(e){}
 window.location.href=window.location.pathname+window.location.search+'#prologue';
 window.location.reload();
}
$('#replay-game')?.addEventListener('click',reset);

// Keyboard access beyond native button activation: 1/2/3 react to the active fight or chase.
document.addEventListener('keydown',e=>{
 const tag=document.activeElement?.tagName;
 if(['INPUT','TEXTAREA','SELECT'].includes(tag)||e.altKey||e.ctrlKey||e.metaKey)return;
 if(e.key==='Escape'&&nav.classList.contains('open')){nav.classList.remove('open');toggle?.setAttribute('aria-expanded','false')}
 if(!['1','2','3'].includes(e.key))return;
 if(chase.running&&!chase.locked){
    chaseChoose(Number(e.key)-1);return;
 }
 if(activeCombat){
   const actions=['strike','guard','dash'];
   activeCombat.action(actions[Number(e.key)-1]);
 }
});

})();
