#!/usr/bin/env python3
"""MANIFESTO: REWIND — compile a new interactive novel to one self-contained index.html.

First run archives prior Studio Edition II as an untouched HTML.
Subsequent runs use archive as original asset source, never an external CDN.
"""
from pathlib import Path
from html.parser import HTMLParser
from html import escape
import re,sys,hashlib,json,shutil
ROOT=Path(__file__).resolve().parent.parent
INDEX=ROOT/"index.html"
ARCHIVE=ROOT/"archive"/"studio-edition-ii.html"
SRC=ARCHIVE if ARCHIVE.exists() else INDEX
assert SRC.exists(), "Missing source artwork"
text=SRC.read_text("utf8")
assert len(text)>3000000, "Source is not complete; refusing to erase old work"
class Images(HTMLParser):
 def __init__(self):super().__init__();self.items=[]
 def handle_starttag(self,tag,attrs):
  if tag=="img":
   a=dict(attrs);src=a.get("src","")
   if src.startswith("data:image/"):
    self.items.append((a.get("alt",""),src))
parser=Images();parser.feed(text)
lookups={
 "COVER":"Chapter 1 key art: Dhanu receives",
 "HERO":"Dhanu, the heroic traveller of Manifesto, wearing a navy",
 "RUN":"Dhanu in a new anime action angle: running toward",
 "SEA":"Chapter 2 readout: the Sea of Almosts",
 "RADIO":"Sanjay’s radio guidance helps Dhanu",
 "ECHO":"Dhanu confronts a future version of himself aboard",
 "MOUNTAIN":"Chapter 3 readout: Dhanu studies",
 "STUDY":"Dhanu in a new anime action angle: examining",
 "VESPER":"Vesper, a monumental walled city",
 "ALLEY":"A deserted city alley narrowing",
 "ARCHIVE":"Ancient archive room with giant brass",
 "SIRI":"Siri follows the records",
 "LEDGER":"Inside Vesper’s archive, the records reveal",
 "GEARS":"A huge brass watch mechanism is illuminated",
 "REACH":"Dhanu in a new anime action angle: reaching",
 "DUEL":"Dhanu confronts his older self beside the Manifesto",
 "DAWN":"Dhanu releases the minute and time begins",
 "CREW":"Dhanu, Sanjay, and Siri look toward sunrise",
}
assets={}
for key,prefix in lookups.items():
 matches=[(a,src) for a,src in parser.items if a.startswith(prefix)]
 assert matches, f"Missing artwork for {key}: {prefix}"
 assets[key]=matches[0][1]
 print("asset",key,"bytes",len(assets[key]),"alt",matches[0][0][:75])
html=(ROOT/"reboot"/"story.html").read_text("utf8")
css=(ROOT/"reboot"/"style.css").read_text("utf8")
js=(ROOT/"reboot"/"game.js").read_text("utf8")
for key,val in assets.items():
 token="@@IMG_"+key+"@@"
 assert token in html, "No placement for "+key
 html=html.replace(token,escape(val,quote=True))
assert not re.search(r"@@IMG_[A-Z]+@@",html)
assert "__STYLE__" in html and "__SCRIPT__" in html
html=html.replace("__STYLE__",css).replace("__SCRIPT__",js)
assert html.count("<html")==1 and html.count("</html>")==1
assert len(html)>2000000
assert len(re.findall(r"data:image/[^;,]+;base64,",html))>=15
assert "Manifesto: Rewind" in html
assert "font-face" not in html and 'https://' not in html, "Unexpected external dependency"
# Never overwrite the old built edition until fully compiled.
ROOT.joinpath("reboot").mkdir(exist_ok=True)
tmp=ROOT/"reboot"/".build.html"
tmp.write_text(html,encoding="utf8")
if not ARCHIVE.exists():
 ARCHIVE.parent.mkdir(exist_ok=True)
 shutil.copy2(INDEX,ARCHIVE)
tmp.replace(INDEX)
meta={"title":"MANIFESTO: REWIND","artwork_keys":list(assets),"embedded_image_occurrences":len(re.findall("data:image/",html)),"html_bytes":INDEX.stat().st_size}
(ROOT/"reboot"/"build-report.json").write_text(json.dumps(meta,indent=2)+"\n","utf8")
print("SUCCESS:",meta)
