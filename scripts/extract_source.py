#!/usr/bin/env python3
"""Export image-free source slices and DOM inventory for human editorial and browser review."""
from pathlib import Path
from html.parser import HTMLParser
import json, re
root=Path(__file__).resolve().parent.parent
out=root/'audit'
out.mkdir(exist_ok=True)
s=(root/'index.html').read_text('utf8')
# Replace huge inline base64/image sources with labels; retain the entire document structure.
def imgref(m):
    v=m.group(0)
    mime=m.group(1)
    return '[EMBEDDED '+mime+' '+str(len(v))+' chars]'
clean=re.sub(r'data:image/(svg\+xml|webp|png|jpeg);base64,[a-zA-Z0-9+/=]+',imgref,s)
(out/'source-no-images.html.txt').write_text(clean,'utf8')
print('Sanitized source',len(clean),'characters',len(clean.splitlines()),'lines')
# Concise useful fragment locations, no embedded data.
anchors=['<head','</head>','class="cover"','id="chapter-one"','id="chapter-two"','id="chapter-three"','id="chapter-four"','id="chapter-five"','id="final-choice"','id="archive-trial"','id="signal-game"','id="bell-trial"','id="resume-reading"','<script','</main>','</body>']
parts=[]
for target in anchors:
    for m in list(re.finditer(re.escape(target),clean))[:12]:
        parts.append(dict(anchor=target,offset=m.start(),excerpt=clean[max(0,m.start()-700):m.start()+2600]))
(out/'source-sections.json').write_text(json.dumps(parts,ensure_ascii=False,indent=2),'utf8')
