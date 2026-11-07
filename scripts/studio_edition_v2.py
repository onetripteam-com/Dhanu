#!/usr/bin/env python3
"""MANIFESTO / Director's Cut II: phases 1–4, one self-contained HTML.

Edit the existing definitive illustrated edition, not the archived alternate finale.
Preserve every data URI, original figure, scene, puzzle and local progress key.
Runs exactly once; fails closed on unexpectedly changed source.
"""
from pathlib import Path
import re

root=Path(__file__).resolve().parent.parent
path=root/"index.html"
s=path.read_text(encoding="utf8")
MARK="MANIFESTO-STUDIO-EDITION-2"
if MARK in s:
    print("Studio Edition II already present; nothing to change")
    raise SystemExit(0)
assert len(s)>3200000, "Original art appears missing"
for key in ["chapter-one","chapter-two","chapter-three","chapter-four","chapter-five","final-choice","final-reveal","archive-trial","signal-game","bell-trial"]:
    assert s.count('id="'+key+'"')==1, key
assert s.count('id="manifesto-finale-frame"')==0

def once(old,new,label):
    global s
    n=s.count(old)
    if n!=1:
        raise RuntimeError("%s: expected one exact anchor, found %d"%(label,n))
    s=s.replace(old,new,1)

# PHASE 1 — fix the final reveal HTML boundary so the footer is not swallowed.
once('<a class="back-top" href="#top">↑ BACK TO THE BEGINNING</a>\n</main>',
     '<a class="back-top" href="#top">↑ BACK TO THE BEGINNING</a>\n</div><!-- /final-reveal: closes the celebratory scene -->\n</main>',
     "close the finale reveal")

# Existing Chapter IV correctly leads into V. Make the end-card a real editorial beat
# instead of repeating the same "next chapter" language three times.
once('<div class="next-tag"><span>FINAL ARC · CHAPTER 05</span><strong>THE HOUR YOU CHOOSE</strong></div><a class="manifesto-final-cta"',
     '<div class="next-tag"><span>ONE LAST GEAR</span><strong>It cannot be taken. It must be given.</strong></div><a class="manifesto-final-cta"',
     "chapter IV transition")

# PHASE 3 — resolve the ship's echo, the letter's misleading warning,
# Vesper's impossible recording and the future-self motive without retcons.
once('“I am one possible Dhanu who never left this ship. Manifesto kept the choice. The sea kept me.”',
     '“I am a possible Dhanu — the part that never dared to leave this ship. Manifesto gave me a shape. The sea kept me here. The person who made the bargain is waiting somewhere else.”',
     "ship echo clarification")
once("It wasn't magic, he realised. It was evidence.",
     "Vesper had kept the call like a receipt. Whether it was magic or machinery didn't matter: Siri had heard the wrong voice, and now Dhanu had proof.",
     "Siri's receipt")
once("The man waiting beside the mechanism wore Dhanu’s face, only older, weathered, and tired in a way that came not from battle but from hesitation. He admitted what the record had only implied: when he once stood at the edge of his own next life, he had hidden a minute inside Manifesto so he would not have to step forward before he was ready.",
     "The man waiting beneath the mechanism wore Dhanu’s face, only older. It was the same tired gaze he'd seen aboard the ship — except that man had been an echo. This one was real enough to be frightened. He had written the letter, reserved the missing minute and sent his younger self through every place he once lacked the courage to leave.",
     "finale echo connection")
once("That was the cost of the Sea of Almosts. The minute stayed safe, but the life around it grew smaller. Legends had chased Manifesto for years — sailors, swordsmen, scouts, city-watchers — but the watch was never meant to <em>give</em> a future. It only asked one question: <strong>when your next arc arrives, will you live it, or will you hide from it?</strong>",
     "“You said someone stole my birthday,” Dhanu said. “You knew it was a promise.”<br/><br/>“I knew you wouldn't come looking for a gift,” the older Dhanu replied. “Not one from me.” He looked at the stopped clock. “I thought if I could keep one perfect minute safe, I wouldn't have to risk the next one.”<br/><br/>“And the man on the ferry?”<br/><br/>“A life I almost chose. Vesper keeps echoes of the decisions we never make. He gave you BEGIN because he couldn't begin again himself.”<br/><br/>Dhanu looked at the fourth gear on the stranger's wrist. “Then stop deciding for me.”",
     "climactic dialogue")
once("The older Dhanu placed his hand over Manifesto. Its gears trembled at 11:59. Three paths opened in the turning brass. The minute was his to live. But the final gear was still in the other Dhanu’s hand. How will he answer the watch?",
     "The last gear was still fastened to the older Dhanu's wrist. Dhanu remembered the archivist's warning: it couldn't be taken. There would be no battle here — only a conversation difficult enough to change both their lives.",
     "meaningful final choice setup")
once('What should Dhanu do<br/><em>with the missing minute?</em>',
     'How does Dhanu reach<br/><em>the man he could become?</em>',
     "final choice question")
once('<button data-final-choice="keep" type="button"><small>OPTION 01</small><strong>Keep the minute</strong><span>Store it for another day, just in case the future becomes too heavy.</span></button>',
     '<button data-final-choice="keep" type="button" aria-pressed="false"><small>REACH FOR CONTROL</small><strong>Demand the gear</strong><span>Take what is yours before he changes his mind.</span></button>',
     "wrong choice 1")
once('<button data-final-choice="break" type="button"><small>OPTION 02</small><strong>Destroy Manifesto</strong><span>Smash the mechanism and hope the fear disappears with it.</span></button>',
     '<button data-final-choice="break" type="button" aria-pressed="false"><small>LOOK FOR CERTAINTY</small><strong>Make another bargain</strong><span>Ask him to promise that nothing will ever go wrong.</span></button>',
     "wrong choice 2")
once('<button data-final-choice="return" type="button"><small>OPTION 03</small><strong>Return the minute</strong><span>Release it back into time and step into the unwritten life ahead.</span></button>',
     '<button data-final-choice="return" type="button" aria-pressed="false"><small>LEAVE THE DOOR OPEN</small><strong>Offer him a choice</strong><span>Tell him that neither of them needs a perfect tomorrow.</span></button>',
     "true choice")
once('Read the confrontation, then decide how Dhanu should answer the watch.',
     'There is no way to force a gift. Choose what Dhanu says next.',
     "final choice instructions")

once('<div class="closing-note"><strong>Manifesto’s last secret.</strong> The watch had never stolen tomorrow. It had guarded one minute for a man who feared choosing what came next. Dhanu held out his hand. The older Dhanu, afraid and uncertain, gave him the last gear freely. No villain fell. No future was erased. With BEGIN, RETURN, WITNESS and CHOOSE joined at last, Dhanu returned the promised minute to the world. He could not know every road ahead — but he could take the first step.</div>',
     '<div class="closing-note"><strong>Manifesto’s last secret.</strong> Dhanu did not reach for the wrist. He held out an empty hand. For a long moment, the other Dhanu stared at it. Then he unclasped the last gear himself.<br/><br/>“I cannot promise you an easy life,” he said.<br/><br/>“Good,” Dhanu answered. “I would rather have my own.”<br/><br/>No villain fell, and no future was erased. With BEGIN, RETURN, WITNESS and CHOOSE together, the watch finally moved. Midnight arrived. The first minute of Dhanu’s birthday belonged to him again.</div>',
     "emotional resolution")
once('<div class="credit-plate"><em>For Dhanu — from your people.</em> Happy Birthday, bro. May the days ahead bring good adventures, the discipline to build what matters, and people worth coming home to. And as graduation draws closer, may your next chapter be one you’re excited to write.</div>',
     '<div class="credit-plate"><em>For Dhanu — from your people.</em> Happy Birthday, bro. Here’s to every difficult morning you show up for, every ridiculous adventure we still haven’t planned, and the friends who’ll be waiting when you come back with the story. The next chapter is yours. Make it a good one.</div>',
     "final birthday message")
once("feedback.textContent='Correct. Dhanu returns the minute to time, and the city begins to move again.'",
     "feedback.textContent='He listens. The older Dhanu gives the fourth gear freely. The minute can finally return.'",
     "success feedback")
once("keep:'That is the mistake the older Dhanu already made. Keeping the minute protects fear, not life.',",
     "keep:'He closes his fist. “You cannot take a choice from me,” he says. Nix looks toward the open hand Dhanu could offer instead.',",
     "wrong branch feedback 1")
once("break:'The watch is not the real prison. Destroying the mechanism avoids the choice instead of answering it.'",
     "break:'“Another guarantee?” the older Dhanu asks. “That is what trapped me here.” Try reaching him without another promise.',",
     "wrong branch feedback 2")
# Keep the same data-final-choice values and localStorage keys so old progress survives.

# Four gears: use true live HTML, not inaccessible lettering baked into a picture.
once('<div class="final-reveal" id="final-reveal">\n',
     '<div class="final-reveal" id="final-reveal">\n'
     '<div class="gear-ceremony" role="img" aria-label="All four mechanisms of Manifesto are united: Begin, Return, Witness and Choose">'
     '<div class="gear-heart"><span class="gear-hand"></span><b>12:00</b></div>'
     '<div class="gear-runes"><span>BEGIN</span><span>RETURN</span><span>WITNESS</span><span>CHOOSE</span></div>'
     '<p>One minute. A lifetime of choices.</p></div>\n',
     "four gear ceremony")

# PHASE 2 — hero art direction, readable panels and focused cinematic typography.
# PHASE 4 — mobile/focus/reduced-motion/better controls, without external requests.
css=r"""
<style id="manifesto-studio-edition-v2">
/* MANIFESTO-STUDIO-EDITION-2 — intentionally restrained visual system */
:root{--studio-ivory:#f3e7d4;--studio-gold:#ecc18c;--studio-navy:#081824;--studio-line:rgba(237,194,138,.35)}
html{scroll-padding-top:80px}
body{background:radial-gradient(ellipse at 50% 3%,#27455a33,transparent 42%),#081520}
.nav-links a{display:inline-grid;place-items:center;min-height:40px;min-width:38px;padding:9px 8px;border-radius:3px;transition:background .18s,border .18s}
.nav-links a[aria-current="location"]{color:#122333;background:var(--studio-gold);border-color:var(--studio-gold)}
.nav-links a:focus-visible{outline:3px solid #ffdc9d;outline-offset:3px}
.nav-right{min-width:0}
.cover{min-height:680px;max-height:none;align-items:center;background:radial-gradient(circle at 78% 25%,#37455591,#0c1926 70%)}
.cover-copy{display:grid;grid-template-columns:minmax(0,.95fr) minmax(0,1.05fr);column-gap:clamp(24px,4vw,75px);row-gap:22px;align-items:center;width:100%;max-width:none;padding:clamp(30px,5.4vw,78px)}
.cover .kicker{grid-column:1;grid-row:1;margin:0;font-size:10px}
.cover h1{grid-column:1;grid-row:2;font-size:clamp(58px,6.7vw,104px);margin:4px 0 0;letter-spacing:-.07em}
.cover .manifesto-opening-portrait{grid-column:2;grid-row:1/span 7;align-self:center;justify-self:stretch;max-width:none;width:100%;margin:0;border:1px solid #b59b79a8;box-shadow:0 30px 90px #0009}
.cover .manifesto-opening-portrait img{display:block;width:100%;height:auto;aspect-ratio:16/11;object-fit:contain;object-position:center center;background:#0a121c}
.cover .manifesto-opening-portrait figcaption{padding:16px 18px;letter-spacing:.01em}
.cover .cover-copy>p{grid-column:1;grid-row:3;font-size:clamp(16px,1.5vw,20px);margin:0;max-width:510px}
.cover .start-btn{grid-column:1;grid-row:4;justify-self:start;min-height:52px}
.cover #resume-reading{grid-column:1;grid-row:5;justify-self:start;margin:0}
.cover .cover-edition{grid-column:1;grid-row:6;margin:0}
.cover .cover-foot{grid-column:1;grid-row:7;padding:0;font-size:10px;line-height:1.7}
.cover:before{background:linear-gradient(90deg,#06132177,transparent 80%);z-index:-1}
.cover>img:first-child{opacity:.2;filter:blur(2px)}
.cover .manifesto-opening-portrait figcaption span{display:block;margin-bottom:5px}
.chapter-intro,.chapter-divider{position:relative}
.chapter-intro:before,.chapter-divider:before{content:"";display:block;width:44px;height:1px;background:var(--studio-gold);margin:0 auto 20px}
.chapter-intro h2,.chapter-divider h2{overflow-wrap:normal}
.story-figure{border-radius:12px;border:1px solid var(--studio-line);box-shadow:0 24px 72px #020c1780}
.story-figure img{height:auto;object-fit:contain;object-position:center;max-width:100%}
.story-figure figcaption{padding:19px 24px 22px;background:#101f2c;color:#e3dfd5;font:clamp(14px,1.3vw,17px)/1.65 Georgia,serif}
.story-figure strong{font:800 10px/1.6 Arial,sans-serif;letter-spacing:.15em;color:var(--studio-gold)}
.story-figure, .manga-shot{scroll-margin-top:82px}
.manga-shot{transform:none;border-width:4px;border-color:#d6c7b4;box-shadow:8px 11px 0 #020c17}
.manga-shot figcaption{pointer-events:none}
.c5-story{max-width:760px;padding:0 22px;margin:34px auto 54px}
.c5-story>p{font:clamp(20px,2.4vw,27px)/1.62 Georgia,serif;letter-spacing:-.015em;color:#e6dfd3;margin:0 0 32px}
.c5-story>p:first-child::first-letter{font-size:1.2em;color:var(--studio-gold)}
.choice-trial{border-radius:12px;padding:clamp(22px,4vw,40px);box-shadow:0 20px 65px #0008}
.choice-trial h3{font-family:Georgia,serif;font-weight:400}
.final-choices button{border-radius:8px;min-height:154px;line-height:1.55}
.final-choices button:focus-visible,.final-choices button[aria-pressed="true"]{border-color:var(--studio-gold);background:#294354;outline:3px solid #f7d5a5;outline-offset:2px}
.final-choices strong{font-family:Georgia,serif;font-weight:400;font-size:clamp(21px,2.3vw,27px)}
.closing-note{font:clamp(18px,2vw,23px)/1.8 Georgia,serif;padding:22px 26px;border-radius:6px}
.credit-plate{font:clamp(18px,2.2vw,24px)/1.65 Georgia,serif}
.gear-ceremony{text-align:center;position:relative;isolation:isolate;max-width:760px;margin:75px auto 60px;padding:36px 18px 26px;border-top:1px solid #d3aa725c;border-bottom:1px solid #d3aa725c;background:radial-gradient(circle at 50% 45%,#cba15f29,transparent 68%)}
.gear-heart{position:relative;width:clamp(160px,27vw,230px);aspect-ratio:1;border:10px double #d9af71;border-radius:50%;margin:0 auto 32px;box-shadow:0 0 0 10px #192e3b,0 0 60px #e3ae576b,inset 0 0 40px #04111c;background:repeating-conic-gradient(#34495a 0 2deg,#142638 2deg 30deg);display:grid;place-items:center}
.gear-heart:before{content:"";position:absolute;inset:12%;border:1px dashed #cfaa73;border-radius:50%;animation:studio-turn 18s linear infinite}
.gear-heart:after{content:"";position:absolute;inset:0;border-radius:50%;box-shadow:inset 0 0 25px #e9b96c42}
.gear-heart b{position:relative;z-index:2;color:#ffe3b4;font:400 clamp(34px,6vw,51px)/1 Georgia,serif;letter-spacing:.05em;text-shadow:0 2px 12px #000}
.gear-runes{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;max-width:650px;margin:auto}
.gear-runes span{padding:12px 5px;border:1px solid #dfb77995;color:#f8d8ad;font:800 clamp(9px,1.6vw,12px)/1.5 Arial,sans-serif;letter-spacing:.1em}
.gear-ceremony p{margin:28px 0 0;color:#f1e4cd;font:italic clamp(20px,2.6vw,30px)/1.4 Georgia,serif}
@keyframes studio-turn{to{transform:rotate(360deg)}}
.figure-zoom{position:absolute;top:12px;right:12px;z-index:7;display:inline-flex;align-items:center;gap:6px;padding:10px 13px;min-height:42px;border:1px solid #e5c596;border-radius:5px;background:#071724ea;color:#f5dfbe;font:800 11px/1.3 Arial,sans-serif;letter-spacing:.07em;cursor:pointer}
.figure-zoom:hover,.figure-zoom:focus-visible{background:#314658}
.story-figure{position:relative}
.story-figure .figure-zoom{top:13px;right:13px}
.manga-shot .figure-zoom{top:13px;right:13px}
#studio-lightbox{border:1px solid #ae946d;background:#071521;color:#eee3d1;width:min(98vw,1200px);max-width:98vw;max-height:96dvh;padding:0;border-radius:9px;box-shadow:0 25px 100px #000d}
#studio-lightbox::backdrop{background:#000d;backdrop-filter:blur(7px)}
#studio-lightbox header{display:flex;align-items:center;justify-content:space-between;gap:12px;position:sticky;top:0;z-index:2;background:#091824;padding:12px 15px;border-bottom:1px solid #786f60}
#studio-lightbox header strong{font:800 11px Arial,sans-serif;letter-spacing:.1em}
#studio-lightbox button{border:1px solid #b89c79;border-radius:3px;background:#243b4c;color:#f9e8d1;min-height:40px;padding:9px 13px;cursor:pointer}
#studio-lightbox .studio-art-canvas{overflow:auto;max-height:calc(96dvh - 75px);text-align:center;padding:10px}
#studio-lightbox img{display:block;width:auto;max-width:100%;height:auto;max-height:calc(96dvh - 120px);margin:auto;object-fit:contain}
#studio-lightbox.studio-zoomed img{max-width:none;max-height:none;width:max(100%,1050px)}
#studio-lightbox p{font:14px/1.6 Georgia,serif;color:#ded7c9;margin:12px auto}
.studio-footer-controls{display:flex;justify-content:center;gap:15px;flex-wrap:wrap;margin-top:18px}
.studio-footer-controls button{background:transparent;color:#e9c391;border:1px solid #73624e;padding:10px 15px;min-height:44px;border-radius:3px;cursor:pointer}
.studio-footer-controls button:hover{background:#273e4d}
.sanjay-transmission{max-width:100%!important}
@media(min-width:1280px){.story-figure.wide{max-width:min(1060px,92vw)}}
@media(max-width:850px){
 .cover{min-height:auto;max-height:none}
 .cover-copy{display:block;padding:clamp(28px,5vw,52px);max-width:none}
 .cover h1{font-size:clamp(60px,10vw,100px);margin:26px 0}
 .cover .manifesto-opening-portrait{margin:28px auto;width:100%;max-width:730px}
 .cover .cover-copy>p{margin:24px 0;font-size:clamp(16px,2vw,20px)}
 .cover .start-btn{margin-top:4px}
 .cover .cover-edition{margin-top:17px}
 .cover .cover-foot{margin-top:12px}
}
@media(max-width:500px){
 .nav{padding:8px 10px;gap:8px}
 .nav-right{gap:4px}
 .logo{font-size:12px;letter-spacing:.07em;white-space:nowrap}
 .logo i{width:7px;height:7px;margin-right:6px}
 .nav-links{gap:3px}
 .nav-links a{min-width:36px;min-height:42px;font-size:10px;padding:9px 5px}
 .cover-copy{padding:27px 19px 38px}
 .cover h1{font-size:clamp(54px,13vw,74px)}
 .cover .manifesto-opening-portrait{width:100%;margin:22px 0}
 .cover .manifesto-opening-portrait img{aspect-ratio:16/10;object-fit:contain}
 .cover .manifesto-opening-portrait figcaption{font-size:12px;padding:13px}
 .cover p{max-width:100%}
 .story-figure{max-width:calc(100vw - 24px);margin:34px auto 48px}
 .story-figure figcaption{font-size:15px;line-height:1.65;padding:14px}
 .manga-shot{margin:65px auto}
 .c5-story{padding:0 16px}
 .c5-story>p{font-size:20px;line-height:1.65}
 .choice-trial{padding:19px}
 .final-choices{grid-template-columns:1fr}
 .final-choices button{min-height:100px}
 .gear-runes{grid-template-columns:repeat(2,minmax(0,1fr))}
 .sanjay-transmission{right:auto!important;max-width:96%!important}
 .figure-zoom{font-size:10px;padding:9px 10px}
}
@media(prefers-reduced-motion:reduce){
 .gear-heart:before{animation:none}
 .story-figure,.manga-shot,.choice-trial,.final-choices button{animation:none!important;transition:none!important}
}
</style>
"""
once("</head>",css+"\n</head>","art direction stylesheet")

# Add convenient but quiet replay control; never reset user's progress without a click.
footer_target='Made for Dhanu · Made to be read, not rushed.</footer>'
footer_replacement=('Made for Dhanu · Made to be read, not rushed.'
    '<div class="studio-footer-controls"><button type="button" id="studio-restart">Start again at Chapter I</button>'
    '<button type="button" id="studio-reset">Reset my story choices</button></div></footer>')
once(footer_target,footer_replacement,"footer reading controls")

# Native dialog is in the same HTML; loaded only when a reader asks to zoom an illustration.
dialog='''<dialog id="studio-lightbox" aria-label="Illustration viewer">
<header><strong>MANIFESTO · ILLUSTRATION VIEWER</strong><div>
<button type="button" id="studio-lightbox-zoom">Zoom in</button>
<button type="button" id="studio-lightbox-close">Close ×</button></div></header>
<div class="studio-art-canvas"><img id="studio-lightbox-image" alt=""/>
<p id="studio-lightbox-caption"></p></div>
</dialog>
'''
once("</body>",dialog+"\n</body>","single lightbox")

# Observe the reading marker without forcing scroll. Offer read-only art zoom on demand.
js=r"""
<script id="manifesto-studio-edition-v2-script">
(()=>{
'use strict';
const sections=['chapter-one','chapter-two','chapter-three','chapter-four','chapter-five'];
const links=[...document.querySelectorAll('.nav-links a')];
const nodes=sections.map(id=>document.getElementById(id));
function setActive(id){
  links.forEach(a=>{
    if(a.getAttribute('href')==='#'+id)a.setAttribute('aria-current','location');
    else a.removeAttribute('aria-current');
  });
}
if('IntersectionObserver' in window){
  const visible=new Map();
  const observer=new IntersectionObserver(entries=>{
    for(const e of entries){
      if(e.isIntersecting)visible.set(e.target.id,e.boundingClientRect.top);
      else visible.delete(e.target.id);
    }
    if(visible.size){
      const chosen=[...visible].sort((a,b)=>Math.abs(a[1])-Math.abs(b[1]))[0];
      setActive(chosen[0]);
    }
  },{rootMargin:'-70px 0px -70% 0px',threshold:0});
  nodes.filter(Boolean).forEach(el=>observer.observe(el));
}
function storageClear(){
  try{
    const keys=[];
    for(let i=0;i<localStorage.length;i++){
      const k=localStorage.key(i);
      if(/^manifesto-v[2345]-/.test(k))keys.push(k);
    }
    keys.forEach(k=>localStorage.removeItem(k));
  }catch(e){}
}
const restart=document.getElementById('studio-restart');
const reset=document.getElementById('studio-reset');
if(restart)restart.addEventListener('click',()=>{location.hash='#chapter-one';document.getElementById('chapter-one').scrollIntoView()});
if(reset)reset.addEventListener('click',()=>{
  if(!window.confirm('Reset MANIFESTO puzzle choices and reading progress on this device?'))return;
  storageClear();
  location.href=location.pathname+location.search+'#chapter-one';
  location.reload();
});
const dialog=document.getElementById('studio-lightbox');
const close=document.getElementById('studio-lightbox-close');
const zoom=document.getElementById('studio-lightbox-zoom');
const photo=document.getElementById('studio-lightbox-image');
const note=document.getElementById('studio-lightbox-caption');
let opener=null;
function dismiss(){
  if(dialog.open)dialog.close();
  if(opener&&opener.isConnected)opener.focus({preventScroll:true});
}
function openArtwork(button,img,caption){
  opener=button;
  photo.src=img.currentSrc||img.src;
  photo.alt=img.alt||'MANIFESTO illustration';
  note.textContent=caption?.innerText||img.alt||'';
  dialog.classList.remove('studio-zoomed');
  zoom.textContent='Zoom in';
  if(typeof dialog.showModal==='function')dialog.showModal();
  else{dialog.setAttribute('open','');dialog.style.display='block'}
  close.focus();
}
document.querySelectorAll('figure.story-figure,figure.manga-shot').forEach(figure=>{
 const img=figure.querySelector('img');
 if(!img)return;
 const b=document.createElement('button');
 b.type='button';b.className='figure-zoom';
 b.textContent='View artwork +';
 b.setAttribute('aria-label','Enlarge illustration: '+(img.alt||'MANIFESTO scene').slice(0,100));
 b.addEventListener('click',()=>openArtwork(b,img,figure.querySelector('figcaption')));
 figure.appendChild(b);
});
close.addEventListener('click',dismiss);
zoom.addEventListener('click',()=>{
 const on=dialog.classList.toggle('studio-zoomed');
 zoom.textContent=on?'Fit to screen':'Zoom in';
});
dialog.addEventListener('click',e=>{if(e.target===dialog)dismiss()});
dialog.addEventListener('close',()=>{if(opener&&opener.isConnected)opener.focus({preventScroll:true})});
})();
</script>
"""
once("</body>",js+"\n</body>","reader interactions")

# Structural safety — protect every original embedded asset and legacy puzzle.
anchors=[s.index('id="chapter-'+n+'"') for n in ('one','two','three','four','five')]
assert anchors==sorted(anchors)
assert s.count('id="final-reveal"')==1
assert s.count('id="studio-lightbox"')==1
assert s.count('id="studio-restart"')==1
assert s.count("data-final-choice=")==3
assert s.count('id="manifesto-finale-frame"')==0
assert len(re.findall(r'data:image/[^;,]+;base64,',s))>=35
assert len(s)>3200000
path.write_text(s,encoding="utf8")
print("Studio Edition II built:",len(s),"characters; chapter offsets:",anchors)
