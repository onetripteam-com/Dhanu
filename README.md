# MANIFESTO — The Missing Minute

**An original birthday graphic novel for Dhanu.** A cinematic, mobile-first story about a lost minute, an impossible voyage, and the legendary timepiece called Manifesto.

### Read it

**All five chapters are now readable inside [index.html](index.html)**. The finale is embedded directly in that one HTML file, without a separate network request. On the public GitHub Pages website, open:

**https://onetripteam-com.github.io/Dhanu/**

Chapter V is available via the **Chapter V · The Finale** control on the main page. The original [standalone Chapter V URL](chapter-five.html) remains available for compatibility.

The unified main HTML is self-contained: the original illustrations, styles, scripts and challenges are preserved, and Chapter V is embedded as an isolated inline reader. No login, tracking, external fonts, or internet requests are needed to read a downloaded copy.

### Story chapters — one HTML

- Chapter I — Eleven Fifty-Nine
- Chapter II — The Ship of Forgotten Tomorrows
- Chapter III — The Thousandth Morning
- Chapter IV — The City Behind the Wall
- Chapter V — The Hour You Choose ([read the new finale](chapter-five.html))

The existing illustrated graphic novel remains unchanged in `index.html`. A standalone Chapter V interpretation has been added with an optional recap, an interactive decision, scene navigation, and a birthday reveal that opens only after the reader continues past the decision. The post-credits scene opens with the reveal. Because the original HTML is about 3.3 MB and could not be fully retrieved through the connector, **this release has not been integrated or continuity-checked against every scene in `index.html`**. Use the direct Chapter V link above. Progress for this page is stored locally in the reader's browser.

### Edit and publish

Update the original Chapters I–IV in `index.html` and Chapter V in `chapter-five.html`. The GitHub Actions workflow `.github/workflows/merge-chapters.yml` reruns `scripts/merge_chapters.py` after updates to Chapter V or the merge tool, and publishes the combined `index.html`. If editing the main story, retain the marked inline Chapter V section. GitHub Pages should be set to **Deploy from branch → main → / (root)**. Deployment status is visible under **Actions** and **Settings → Pages**.

The artwork includes original anime-inspired character studies. Dhanu's name is fixed in the story—there is no personalization field. The supporting characters are fictional illustrations rather than photographs.

### Implementation notes

- One unified self-contained HTML reader on the home URL, plus a compatibility Chapter V source file
- Accessible button controls, a Chapter V recap, and a choice-gated finale
- Mobile reading layout and responsive desktop view
- Reduced-motion-aware animations
- Existing Chapter I–III progress keys preserved across updates

See `STORY_BIBLE.md` for editorial continuity and future-chapter notes (contains spoilers).
