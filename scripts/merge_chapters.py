#!/usr/bin/env python3
"""Embed the complete standalone Chapter V in the existing MANIFESTO index.html.
No external assets, HTTP calls, or separate HTML files are needed to read all chapters.
The existing 3.3 MB illustrated novel is preserved byte-for-byte except for insertion
of one isolated reader and its launcher immediately before </body>.
"""
from pathlib import Path
from html import escape
import re
import sys

root = Path(__file__).resolve().parent.parent
index_path = root / "index.html"
finale_path = root / "chapter-five.html"
index = index_path.read_text(encoding="utf-8")
finale = finale_path.read_text(encoding="utf-8")
if len(index) < 1000000:
    raise SystemExit("Refusing merge: original illustrated novel unexpectedly short")
if len(finale) < 10000 or "The Hour" not in finale or "final-reveal" not in finale:
    raise SystemExit("Refusing merge: Chapter V source appears incomplete")
if not re.search(r"</body\s*>", index, re.I):
    raise SystemExit("Refusing merge: no original closing body tag")

# Keep the self-contained finale usable inside a same-origin sandboxed reader.
# Its own scripts/localStorage remain intact; navigation to the earlier chapters closes it.
finale = re.sub(
    r'<a\s+([^>]*?)href=["\']\./index\.html["\']([^>]*)>',
    r'<a \1href="#back-to-manifesto" data-return-manifesto\2>',
    finale,
    flags=re.I,
)
finale = re.sub(
    r"</body\s*>",
    """<script>
document.querySelectorAll('[data-return-manifesto]').forEach(function(link){
  link.addEventListener('click',function(e){
    e.preventDefault();parent.postMessage({manifestoFinale:'close'},'*');
  });
});
<\/script>
</body>""".replace("<\\/script>", "</script>"),
    finale, count=1, flags=re.I
)

start_marker = "<!-- MANIFESTO-CHAPTER-FIVE-INLINE:START -->"
end_marker = "<!-- MANIFESTO-CHAPTER-FIVE-INLINE:END -->"
if start_marker in index:
    if end_marker not in index:
        raise SystemExit("Broken existing merge markers")
    index = index[:index.index(start_marker)] + index[index.index(end_marker) + len(end_marker):]

# srcdoc is the whole Chapter V HTML: its CSS and JavaScript are isolated.
srcdoc = escape(finale, quote=True)
injection = r"""
<!-- MANIFESTO-CHAPTER-FIVE-INLINE:START -->
<style id="manifesto-finale-shell-style">
#manifesto-final-launch{position:fixed;z-index:2147483000;right:max(14px,env(safe-area-inset-right));bottom:max(16px,env(safe-area-inset-bottom));padding:13px 17px;min-height:48px;max-width:min(80vw,330px);border-radius:999px;border:1px solid #d6b87f;background:#14283b;color:#f7dfac;box-shadow:0 7px 28px #0009;font:700 12px/1.3 system-ui,sans-serif;letter-spacing:.055em;cursor:pointer}
#manifesto-final-launch:focus-visible,#manifesto-final-close:focus-visible{outline:3px solid #eec782;outline-offset:3px}
#manifesto-finale-shell[hidden],#manifesto-final-launch[hidden]{display:none!important}
#manifesto-finale-shell{position:fixed;inset:0;z-index:2147483600;background:#091322;display:flex;flex-direction:column}
#manifesto-finale-bar{flex:none;display:flex;justify-content:space-between;align-items:center;gap:15px;min-height:56px;padding:calc(7px + env(safe-area-inset-top)) max(16px,env(safe-area-inset-right)) 7px max(16px,env(safe-area-inset-left));background:#08111b;color:#eac78e;font:600 11px/1.5 system-ui,sans-serif;letter-spacing:.07em}
#manifesto-final-close{color:#14283b;background:#eac78e;border:0;border-radius:4px;min-height:40px;padding:8px 13px;font:700 12px system-ui,sans-serif;cursor:pointer}
#manifesto-finale-frame{width:100%;flex:1;min-height:0;border:0;background:#091322}
body.manifesto-finale-open{overflow:hidden!important}
@media(max-width:420px){#manifesto-finale-bar{font-size:10px}#manifesto-final-launch{font-size:11px}}
</style>
<button id="manifesto-final-launch" type="button" aria-haspopup="dialog" aria-controls="manifesto-finale-shell">Chapter V · The Finale ✦</button>
<section id="manifesto-finale-shell" role="dialog" aria-modal="true" aria-label="Chapter V — The Hour You Choose" hidden>
<div id="manifesto-finale-bar"><span>MANIFESTO / CHAPTER V</span><button type="button" id="manifesto-final-close" aria-label="Return to chapters one through four">← Back to story</button></div>
<iframe id="manifesto-finale-frame" title="Chapter V — The Hour You Choose" loading="lazy" srcdoc="__SRCDOC__"></iframe>
</section>
<script id="manifesto-finale-shell-script">
(function(){
  'use strict';
  var launch=document.getElementById('manifesto-final-launch');
  var shell=document.getElementById('manifesto-finale-shell');
  var close=document.getElementById('manifesto-final-close');
  var frame=document.getElementById('manifesto-finale-frame');
  var prev=null;
  function openFinale(){
    prev=document.activeElement;
    shell.hidden=false;launch.hidden=true;
    document.body.classList.add('manifesto-finale-open');
    close.focus();
    try{history.replaceState(null,'',location.pathname+location.search+'#chapter-five')}catch(e){}
  }
  function closeFinale(){
    shell.hidden=true;launch.hidden=false;
    document.body.classList.remove('manifesto-finale-open');
    try{history.replaceState(null,'',location.pathname+location.search)}catch(e){}
    (prev&&prev.isConnected?prev:launch).focus();
  }
  launch.addEventListener('click',openFinale);
  close.addEventListener('click',closeFinale);
  document.addEventListener('keydown',function(e){
    if(shell.hidden)return;
    if(e.key==='Escape'){e.preventDefault();closeFinale()}
    if(e.key==='Tab'&&document.activeElement===close){e.preventDefault();frame.focus()}
  });
  window.addEventListener('message',function(e){
    if(e.source===frame.contentWindow&&e.data&&e.data.manifestoFinale==='close')closeFinale();
  });
  if(location.hash==='#chapter-five')openFinale();
})();
</script>
<!-- MANIFESTO-CHAPTER-FIVE-INLINE:END -->
""".replace("__SRCDOC__",srcdoc)
index = re.sub(r"(?=</body\s*>)",lambda _:injection,index,count=1,flags=re.I)
index_path.write_text(index,encoding="utf-8")
print("Merged inline finale. HTML bytes:",index_path.stat().st_size)
assert index.count(start_marker)==1 and index.count(end_marker)==1
assert index.count('id="manifesto-finale-frame"')==1
assert "Happy Birthday, Dhanu." in index
