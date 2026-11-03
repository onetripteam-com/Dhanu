# MANIFESTO — The Missing Minute

**An original birthday graphic novel for Dhanu.** A cinematic, mobile-first story about a lost minute, an impossible voyage, and the legendary timepiece called Manifesto.

### Read it

The main illustrated graphic novel is in **[index.html](index.html)**, with the finale in **[chapter-five.html](chapter-five.html)**. On the public GitHub Pages website, open:

**https://onetripteam-com.github.io/Dhanu/**

**New Chapter V finale (standalone): https://onetripteam-com.github.io/Dhanu/chapter-five.html**

Both HTML pages are self-contained: illustrations, styles, scripts and challenges are embedded. No login, tracking, external fonts or internet requests are needed to read a downloaded copy.

### Story chapters / new standalone finale

- Chapter I — Eleven Fifty-Nine
- Chapter II — The Ship of Forgotten Tomorrows
- Chapter III — The Thousandth Morning
- Chapter IV — The City Behind the Wall
- Chapter V — The Hour You Choose ([read the new finale](chapter-five.html))

The existing illustrated graphic novel remains unchanged in `index.html`. A new standalone Chapter V interpretation has been added with an optional interactive decision and birthday reveal. Because the original HTML is about 3.3 MB and could not be fully retrieved through the connector, **this release has not been integrated or continuity-checked against every scene in `index.html`**. Use the direct Chapter V link above. Progress for this page is stored locally in the reader's browser.

### Edit and publish

Update `index.html` and/or `chapter-five.html` on the `main` branch to publish the next version. GitHub Pages should be set to **Deploy from branch → main → / (root)**. Deployment status is visible under **Actions** and **Settings → Pages**.

The artwork includes original anime-inspired character studies. Dhanu's name is fixed in the story—there is no personalization field. The supporting characters are fictional illustrations rather than photographs.

### Implementation notes

- Two self-contained static HTML pages; no build commands
- Accessible button controls and optional skip paths
- Mobile reading layout and responsive desktop view
- Reduced-motion-aware animations
- Existing Chapter I–III progress keys preserved across updates

See `STORY_BIBLE.md` for editorial continuity and future-chapter notes (contains spoilers).
