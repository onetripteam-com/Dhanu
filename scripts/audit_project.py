#!/usr/bin/env python3
"""Generate a structured review of the complete self-contained MANIFESTO HTML."""
from pathlib import Path
from html.parser import HTMLParser
from collections import Counter
import re, json, base64, io, hashlib
root=Path(__file__).resolve().parent.parent
raw=(root/'index.html').read_text(encoding='utf-8')
out=root/'audit'
out.mkdir(exist_ok=True)
class Collector(HTMLParser):
 def __init__(self):
  super().__init__(convert_charrefs=True);self.elements=[];self.tags=[];self.text=[];self.current=[];self.stack=[]
 def handle_starttag(self,tag,attrs):
  d=dict(attrs);self.tags.append(tag)
  if tag in ('img','picture','source','iframe','video','audio','button','section','nav','h1','h2','h3','h4','figure','figcaption','a'):
   self.elements.append(dict(tag=tag,attrs={k:(v[:120]+'...' if v and len(v)>150 else v) for k,v in d.items()},offset=self.getpos()))
  self.stack.append(tag)
 def handle_endtag(self,tag):
  if tag in self.stack:self.stack=self.stack[:len(self.stack)-1-self.stack[::-1].index(tag)]
 def handle_data(self,data):
  s=re.sub(r'\s+',' ',data).strip()
  if s and not any(t in self.stack for t in ['style','script']):self.text.append(s)
p=Collector();p.feed(raw)
images=[]
patterns=[
 ('img-src',r'<img\b[^>]*?src\s*=\s*["\'](data:image/[^"\']+)["\']'),
 ('css-url',r'url\(\s*["\']?(data:image/[^)"\']+)'),
 ('js-base64',r'(data:image/(?:png|jpeg|webp|svg\+xml);base64,[a-zA-Z0-9+/=]{500,})')
]
used=set()
for typ,pat in patterns:
 for m in re.finditer(pat,raw,re.I):
  val=m.group(1);key=hashlib.sha1(val.encode()).hexdigest()
  if key in used:continue
  used.add(key)
  head,_,payload=val.partition(',')
  mime=head.split(';')[0].replace('data:','')
  item=dict(id=len(images)+1,kind=typ,sha=key[:12],mime=mime,encoded_length=len(payload),offset=m.start())
  if ';base64' in head:
   try:
    bs=base64.b64decode(payload,validate=True)
    item['bytes']=len(bs)
    item['signature']=bs[:12].hex()
    (out / ('image-%03d.%s' % (len(images)+1, 'jpg' if mime=='image/jpeg' else 'png' if mime=='image/png' else 'webp' if mime=='image/webp' else 'svg'))).write_bytes(bs)
   except Exception as ex:item['decode_error']=str(ex)
  images.append(item)
# A second pass finds arbitrary JS or HTML embedded image sources that weren't captured above
for m in re.finditer(r'data:image/(png|jpeg|webp);base64,([A-Za-z0-9+/=]{1000,})',raw):
 val=m.group(0);key=hashlib.sha1(val.encode()).hexdigest()
 if key in used:continue
 used.add(key); bs=base64.b64decode(m.group(2));ext='jpg' if m.group(1)=='jpeg' else m.group(1)
 (out/f'image-{len(images)+1:03d}.{ext}').write_bytes(bs)
 images.append(dict(id=len(images)+1,kind='general-embedded',sha=key[:12],mime=m.group(1),bytes=len(bs),offset=m.start()))
# Extract readable text and context around scene markers, but don't dump artwork.
visible='\n'.join(p.text)
(out/'visible-text.txt').write_text(visible,encoding='utf-8')
headings=[e for e in p.elements if e['tag'] in ('h1','h2','h3','h4','section','figure','figcaption')]
buttons=[e for e in p.elements if e['tag'] in ('button','a')]
data=dict(chars=len(raw),lines=raw.count('\n')+1,tags=Counter(p.tags),images=images,headings=headings[:500],buttons=buttons[:400],text_chars=len(visible),
 dialogue_like=[s for s in p.text if any(q in s for q in ['“','”','"'])][:250],
 headings_text=[s for s in p.text if re.search(r'Chapter|CHAPTER|Dhanu|Nix|Siri|Sanjay|Manifesto|MANIFESTO',s)][:220],
 id_duplicates={k:v for k,v in Counter(re.findall(r'\bid=["\']([^"\']+)["\']',raw)).items() if v>1},
 scripts= len(re.findall(r'<script\b',raw,re.I)), styles=len(re.findall(r'<style\b',raw,re.I)),
 refs=re.findall(r'href=["\']([^"\']{1,120})["\']',raw)[:140])
(out/'report.json').write_text(json.dumps(data,indent=2,ensure_ascii=False,default=list),encoding='utf-8')
lines=['# MANIFESTO — source inventory','',f'HTML characters: {len(raw):,}; lines: {raw.count(chr(10))+1:,}; text fragments: {len(p.text):,}',f'Unique embedded images: {len(images)}; scripts: {data["scripts"]}; styles: {data["styles"]}','',
'## Image inventory','', '| # | type | bytes | position |','|---|---|---:|---:|']
lines +=[f'| {i["id"]} | {i["mime"]} | {i.get("bytes","?")} | {i["offset"]} |' for i in images]
lines+=['','## Section and figure tags','']
lines +=['- '+json.dumps(e,ensure_ascii=False)[:260] for e in headings[:150]]
lines+=['','## Controls and anchors','']
lines +=['- '+json.dumps(e,ensure_ascii=False)[:220] for e in buttons[:130]]
lines+=['','## Key text lines','']
lines += ['- '+x[:300] for x in data['headings_text'][:180]]
lines+=['','## Dialogue excerpts','']
lines+=['- '+x[:400] for x in data['dialogue_like'][:120]]
lines+=['','## Duplicate IDs','',str(data['id_duplicates'])]
(out/'inventory.md').write_text('\n'.join(lines),encoding='utf-8')

# Extract image alt text, panel captions and immediate textual framing.
class PanelParser(HTMLParser):
 def __init__(self):
  super().__init__(convert_charrefs=True)
  self.current=None;self.panels=[];self.depth=0;self.capture_caption=False
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if tag=='figure':
   if self.current is None:
    self.current=dict(number=len(self.panels)+1,figure_class=d.get('class',''),images=[],caption='')
    self.depth=1
   else:self.depth+=1
  elif self.current is not None:
   if tag=='img':
    src=d.get('src','')
    match=re.search(r'data:image/[^,]+,([A-Za-z0-9+/=]+)',src)
    sha=hashlib.sha1(src.encode()).hexdigest()[:12] if src else ''
    self.current['images'].append(dict(alt=d.get('alt',''),class_name=d.get('class',''),style=d.get('style',''),sha=sha))
   if tag=='figcaption':self.capture_caption=True
 def handle_endtag(self,tag):
  if tag=='figcaption':self.capture_caption=False
  if tag=='figure' and self.current is not None:
   self.depth-=1
   if self.depth==0:self.panels.append(self.current);self.current=None
 def handle_data(self,content):
  if self.current is not None and self.capture_caption:self.current['caption']+=re.sub(r'\\s+',' ',content).strip()+' '
panel=PanelParser();panel.feed(raw)
panel_md=['# Visual scene and caption inventory','',f'Figures: {len(panel.panels)}','']
for item in panel.panels:
 panel_md += [f'## Panel {item["number"]} / {item["figure_class"]}',f'Caption: {item["caption"][:700]}']
 for im in item['images']:panel_md.append('Image '+json.dumps(im,ensure_ascii=False))
 panel_md.append('')
(out/'panels.md').write_text('\\n'.join(panel_md),encoding='utf-8')

print('Images:',len(images),'inventory chars:',len('\n'.join(lines)),'raw visible text:',len(visible))
try:
 from PIL import Image, ImageDraw
 files=list(out.glob('image-*.jpg'))+list(out.glob('image-*.png'))+list(out.glob('image-*.webp'))+list(out.glob('image-*.svg'))
 tiles=[]
 for f in sorted(files):
  try:
   \n   if f.suffix=='.svg':\n    import cairosvg\n    im=Image.open(io.BytesIO(cairosvg.svg2png(url=str(f),output_width=480))).convert('RGBA')\n    backdrop=Image.new('RGBA',im.size,(235,227,206,255));backdrop.alpha_composite(im);im=backdrop.convert('RGB')\n   else: im=Image.open(f).convert('RGB')\n   im.thumbnail((310,190))
   tiles.append((f,im.copy()))
  except Exception as ex:print('image failed',f,ex)
 for page in range(0,len(tiles),24):
  subset=tiles[page:page+24]
  sheet=Image.new('RGB',(1000,((len(subset)+2)//3)*240),(19,26,39))
  d=ImageDraw.Draw(sheet)
  for j,(f,im) in enumerate(subset):
   x=(j%3)*330+10;y=(j//3)*240+8
   sheet.paste(im,(x+(310-im.width)//2,y))
   d.text((x+5,y+196),f.name,fill='white')
  sheet.save(out/f'contact-sheet-{page//24+1:02d}.jpg',quality=75,optimize=True)
  print('Contact sheet',page//24+1)
except ImportError:
 print('Pillow not installed; text inventory saved.')
