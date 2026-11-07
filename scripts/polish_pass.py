#!/usr/bin/env python3
"""Final compositional polish for the canonical MANIFESTO illustrated page."""
from pathlib import Path
p=Path(__file__).resolve().parent.parent/'index.html'
s=p.read_text(encoding='utf-8')
assert len(s)>3000000
assert 'id="chapter-five"' in s and 'id="manifesto-final-launch"' not in s
marker='<style id="manifesto-polish-pass">'
if marker in s:
  print('Visual polish already applied')
  raise SystemExit(0)
css='''<style id="manifesto-polish-pass">
/* Keep one definitive hero shot, not two overlapping Dhanu illustrations. */
.cover .cover-hero{display:none!important}
.cover .manifesto-opening-portrait{isolation:isolate;transform:none!important}
.cover .manifesto-opening-portrait img{object-position:center center;max-height:none}
.cover .manifesto-opening-portrait figcaption{position:relative}
@media(min-width:901px){
 .cover .manifesto-opening-portrait{margin-top:44px;margin-bottom:30px;box-shadow:0 20px 65px #0007}
}
@media(max-width:640px){
 .cover .manifesto-opening-portrait{margin-top:24px}
}
</style>'''
assert s.count('</head>')==1
s=s.replace('</head>',css+'\n</head>',1)
p.write_text(s,encoding='utf-8')
print('Visual compositional polish applied, bytes:',p.stat().st_size)
