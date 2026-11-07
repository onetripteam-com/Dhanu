# MANIFESTO — The Missing Minute

**An original five-chapter, illustrated, interactive birthday graphic novel starring Dhanu.**

## Read the finished website

**https://onetripteam-com.github.io/Dhanu/**

All five chapters, the original artwork, puzzles and birthday finale are in **one self-contained `index.html`**. No login, analytics, third-party fonts, or external image requests are needed. The page can be downloaded and read offline in a modern browser.

The story, in order:
1. **Eleven Fifty-Nine** — the frozen city, Nix and the letter.
2. **The Ship of Forgotten Tomorrows** — the Sea of Almosts; BEGIN.
3. **The Thousandth Morning** — the Bellkeeper and learning to adjust; RETURN.
4. **The City Behind the Wall** — Vesper, Siri's evidence, the beneficiary; WITNESS.
5. **The Hour You Choose** — the confrontation, freely given CHOOSE gear and Dhanu's birthday.

The one-page **illustrated Chapter V** is the definitive ending. The separate `chapter-five.html` is an archived alternate interpretation and must not be merged back into `index.html`.

## Studio Edition II — all four enhancement phases

**Phase 1 — structure.** Five correct chapters, one unique finale, clear Chapter IV → V hand-off, restored HTML closing tags, chapter index and Continue Reading links.

**Phase 2 — art direction.** Reworked desktop two-column cover and mobile portrait composition, consistent navy/copper/ivory typography and image treatments, responsive panels, a live animated four-gear finale, and an accessible zoom/fit image viewer for original illustrated spreads. Original embedded artwork remains intact. This release refines the existing art rather than claiming new character drawings were produced.

**Phase 3 — dialogue and continuity.** Clarified that the future self aboard the ship is an echo of the person waiting in Vesper, why the letter called the reserved minute "stolen", and how Siri's call was retained. Replaced the generic right/wrong destruction choice with a dialogue choice that fulfils the fourth gear's condition: it must be **given**. The final birthday message is shorter and more personal.

**Phase 4 — functionality and QA.** Improved responsive navigation and focus indicators, reduced-motion styling, local-only progress, the optional "Reset my story choices" control, improved scroll and image sizing, repaired an on-reload bell-progress JavaScript error, and automated browser checks for five screen sizes and the complete puzzle/finale flow.

## Controls

- Use **I–V** in the sticky top bar to navigate chapters.
- Use **View artwork +** on illustrated spreads; toggle **Zoom in / Fit to screen** and **Close**.
- Choose puzzle answers or use each puzzle's **skip** option. Neither path prevents the ending.
- Select **Offer him a choice** for the final handover; the other actions explain why they do not resolve it.
- **Resume Reading** appears on revisits after reaching a later chapter.
- **Start again at Chapter I** returns to the beginning without deleting choices.
- **Reset my story choices** asks for confirmation before deleting only MANIFESTO progress stored in this browser.

No sound is needed and there is no audio autoplay.

## Project workflow

- Edit `index.html` on a branch or in GitHub to change the canonical experience.
- The scripts in `scripts/` represent the source-to-source, one-time release transformations and QA tooling. Do not rerun the old `directors_cut.py` or old `merge_chapters.py` over the current HTML; that would undo editorial decisions.
- Production Studio Edition II was committed by the `.github/workflows/studio-edition.yml` workflow. The returning-reader hotfix is in `scripts/studio_hotfix.py`.
- Browser QA runs via `.github/workflows/studio-browser-qa.yml`. The factual output is `audit/studio-browser-qa.json`, with screenshots stored in `audit/studio-*.jpg`.
- Original panel and artwork inventories are in `audit/panels.md` and the two `audit/contact-sheet-*.jpg` files.
- `STORY_BIBLE.md` contains narrative spoilers and character rules.

## Testing scope and limits

Automated **Chromium** checks run at 360×740, 393×852, 402×874, 768×1024 and 1440×900. They examine chapter order, broken images, no horizontal overflow, zero external requests, artwork zoom, all earlier puzzles, the gated finale, and saved ending on reload.

These browser checks do **not** prove the design is perfect on every device; check real iPhone Safari and desktop browsers before sharing as a gift. The 39 original embedded image assets remain as supplied; manual illustration review may still suggest replacing individual drawings in a future art-focused edition.
