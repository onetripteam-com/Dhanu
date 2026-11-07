#!/usr/bin/env python3
"""Rebuild MANIFESTO as one ordered, illustrated five-chapter HTML story.

Idempotent source transformation: preserves the original chapters, puzzles, illustration
data URIs and progress keys. Use with GitHub Actions; no paid external services.
"""
from pathlib import Path
import re, html, hashlib

ROOT = Path(__file__).resolve().parent.parent
PATH = ROOT / "index.html"
s = PATH.read_text(encoding="utf-8")
assert len(s) > 3000000, "Refusing to modify incomplete story"
assert "MANIFESTO" in s and "The Missing Minute" in s

# Legacy self-contained iframe inserted in a prior iteration duplicates the native
# illustrated ending. The original Chapter V is the canonical ending.
a = "<!-- MANIFESTO-CHAPTER-FIVE-INLINE:START -->"
b = "<!-- MANIFESTO-CHAPTER-FIVE-INLINE:END -->"
if a in s:
    assert b in s
    s = s[:s.index(a)] + s[s.index(b) + len(b):]

# Move the original illustrated V block (divider, figures, choice, resolution) as
# an intact chunk from the accidental I->V->II order to the natural I->II->III->IV->V order.
v = re.search(r'<section\b[^>]*\bid=["\']chapter-five["\'][^>]*>', s, re.I)
ii = re.search(r'<section\b[^>]*\bid=["\']chapter-two["\'][^>]*>', s, re.I)
assert v and ii and v.start() < ii.start(), "Unexpected chapter structure; no destructive rewrite"
chapter_v = s[v.start():ii.start()]
assert 'id="ch5-story"' in chapter_v and 'id="final-choice"' in chapter_v
print('MOVE DEBUG: articles',chapter_v.count('<article'),chapter_v.count('</article>'),'tail',repr(chapter_v[-950:]))
assert chapter_v.count('<article') == chapter_v.count('</article>')
s = s[:v.start()] + s[ii.start():]
main_end = s.index("</main>")
assert s.index('id="chapter-four"') < main_end
s = s[:main_end] + '\n<!-- THE DEFINITIVE ILLUSTRATED FINALE -->\n' + chapter_v + '\n' + s[main_end:]

# Replace the "work in progress" end-card with a real handoff to the final chapter.
s = s.replace(
    '<span class="ending-wait">THE FINAL CHAPTER IS BEING WRITTEN</span>',
    '<a class="manifesto-final-cta" href="#chapter-five" aria-label="Continue to Chapter Five, The Hour You Choose">ENTER THE FINAL CHAPTER →</a>'
)
s = s.replace("Chapters 01–03 of 05", "Complete five-chapter illustrated edition")

# The plot's most important reveal should belong after Chapter IV; the chosen
# native illustrated ending is the only one left. Make the final decision personal.
s = s.replace(
    'Which one would Dhanu take?',
    'The minute was his to live. But the final gear was still in the other Dhanu’s hand. What would he ask for?'
)
s = s.replace(
    'The watch had never stolen tomorrow. It had guarded one minute for a man who feared choosing what came next. Dhanu returned it to the world.',
    'The watch had never stolen tomorrow. It had guarded one minute for a man who feared choosing what came next. Dhanu held out his hand. The older Dhanu, afraid and uncertain, gave him the last gear freely. No villain fell. No future was erased. With BEGIN, RETURN, WITNESS and CHOOSE joined at last, Dhanu returned the promised minute to the world.'
)

# Make our protagonist immediately visible in a deliberate cinematic image.
# Reuse the strongest already-embedded opening illustration, preserving offline access.
asset = None
for m in re.finditer(r'<img\b[^>]*>', s, re.I|re.S):
    tag = m.group(0)
    src = re.search(r'\bsrc=["\'](data:image/webp;base64,[A-Za-z0-9+/=]+)["\']', tag, re.I)
    if src and hashlib.sha1(src.group(1).encode()).hexdigest().startswith("53fd1d4f4377"):
        asset = src.group(1)
        break
assert asset, "Expected original illustrated Dhanu/Nix opening art not found"
cover = re.search(r'<section\b[^>]*class=["\'][^"\']*\bcover\b[^"\']*["\'][^>]*>',s)
assert cover
cover_end = s.index("</section>", cover.end())
part = s[cover.end():cover_end]
portrait_marker = "MANIFESTO-OPENING-PORTRAIT"
assert portrait_marker not in part
h1end = part.find("</h1>")
assert h1end != -1
insert = """
<figure class="manifesto-opening-portrait" aria-label="Meet Dhanu, the hero of this story">
<img alt="Dhanu in his navy coat and red sash, face clearly visible, reaches toward Nix above a rainlit clockwork city." decoding="async" fetchpriority="high" src="ASSET"/>
<figcaption><span>THIS IS DHANU</span> One birthday. One impossible minute. His story starts here.</figcaption>
</figure>
""".replace("ASSET",html.escape(asset,quote=True))
part = part[:h1end+5] + insert + part[h1end+5:]
s = s[:cover.end()] + part + s[cover_end:]

# Purposeful rhythm and reliable framing rather than an indiscriminate animation pass.
css = """
<style id="manifesto-directors-cut-styles">
/* MANIFESTO-OPENING-PORTRAIT */
.manifesto-opening-portrait{position:relative;z-index:2;display:block;width:min(90vw,900px);max-width:100%;margin:clamp(22px,5vw,58px) auto 28px;padding:0;isolation:isolate;overflow:hidden;border:1px solid rgba(239,200,137,.36);border-radius:clamp(12px,2vw,22px);background:#0b1723;box-shadow:0 30px 80px rgba(0,0,0,.42)}
.manifesto-opening-portrait img{display:block;width:100%;height:auto;aspect-ratio:16/9;object-fit:contain;object-position:center center}
.manifesto-opening-portrait figcaption{position:relative;z-index:2;padding:12px 18px 15px;text-align:left;background:#091321;color:#e3e8e6;font:500 clamp(12px,1.6vw,15px)/1.55 system-ui,sans-serif;letter-spacing:.01em}
.manifesto-opening-portrait figcaption span{color:#e5bd7e;font-weight:800;letter-spacing:.13em;margin-right:10px}
.manifesto-final-cta{display:inline-flex;align-items:center;justify-content:center;min-height:52px;margin:22px 0 5px;padding:12px 22px;border:1px solid #e5bd7e;border-radius:4px;background:#e5bd7e;color:#132133!important;text-decoration:none!important;font:800 12px/1.5 system-ui,sans-serif;letter-spacing:.12em}
.manifesto-final-cta:hover{filter:brightness(1.09)}
.manifesto-final-cta:focus-visible{outline:3px solid #fff;outline-offset:4px}
.story-figure img,.manga-shot img,.c4-illustration img{max-width:100%}
#chapter-five{scroll-margin-top:74px}
@media(max-width:640px){
 .manifesto-opening-portrait{width:calc(100vw - 28px);margin:26px auto 24px;border-radius:12px}
 .manifesto-opening-portrait img{aspect-ratio:16/10;object-fit:contain}
 .manifesto-opening-portrait figcaption{padding:12px;font-size:12px}
 .manifesto-opening-portrait figcaption span{display:block;margin-bottom:4px}
 .manifesto-final-cta{width:100%;letter-spacing:.075em}
}
@media(prefers-reduced-motion:reduce){.manifesto-opening-portrait,.manifesto-opening-portrait *{animation:none!important;transition:none!important}}
</style>
"""
assert "</head>" in s
s = s.replace("</head>", css + "\n</head>",1)

# Refrain from changing the existing choice puzzle JS/progress keys.
ids = [s.index('id="chapter-'+name+'"') for name in ("one","two","three","four","five")]
assert ids == sorted(ids)
assert s.count('id="chapter-five"') == 1
assert s.count('id="final-choice"') == 1
assert s.count('id="manifesto-final-launch"') == 0
assert "THE FINAL CHAPTER IS BEING WRITTEN" not in s
assert s.count("MANIFESTO-OPENING-PORTRAIT") >= 1
assert s.count('<article') == 5
assert s.count('</article>') == 5
assert len(s) > 3000000
PATH.write_text(s, encoding="utf-8")
print("DIRECTOR CUT VERIFIED; chapter offsets=", ids,"HTML bytes=",PATH.stat().st_size)
