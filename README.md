# MANIFESTO — The Missing Minute

An original, illustrated five-chapter birthday adventure for Dhanu. **Director's Cut**: the story is now one continuous HTML page, in the correct chronological order, with no duplicate finale.

## Read the story

**https://onetripteam-com.github.io/Dhanu/**

The main `index.html` contains all five chapters, all illustrations, puzzles, styles and scripts. It supports offline reading when downloaded. The experience doesn't require login, external fonts, tracking or cloud infrastructure.

1. Chapter I — Eleven Fifty-Nine
2. Chapter II — The Ship of Forgotten Tomorrows
3. Chapter III — The Thousandth Morning
4. Chapter IV — The City Behind the Wall
5. Chapter V — The Hour You Choose

The illustrated Chapter V in the main page is the **definitive ending**. `chapter-five.html` is retained as an archival, alternative standalone interpretation, not linked from the main reading path. Do not republish it over the definitive ending.

## What's changed in the Director's Cut

- Restored the I → II → III → IV → V order, including the original misplaced Chapter I closing wrappers
- Removed the duplicate iframe finale; navigation now reaches the native illustrated Chapter V
- Introduced Dhanu immediately with face-visible, cinematic existing artwork
- Fixed Chapter IV's outdated "being written" message and the incorrect three-chapter footer
- Refined the final gear handover to fulfill Chapter IV's promise: the gear must be **given**
- Kept original artwork, existing choices, local progress keys and the original single-file offline format

## How to edit

Edit `index.html` directly on `main`, or create a branch before making extensive changes. Do **not** rerun `scripts/directors_cut.py` against an already revised Director's Cut: it is a one-time transformation of the older, misordered edition. Its published GitHub Actions build is recorded in commit `449e9ac`. The old iframe merger is archived to prevent undoing this work.

GitHub Pages: Deploy from branch → `main` → `/ (root)`. The public URL is the same.

Visual inventories and full story text are in `audit/`; `STORY_BIBLE.md` documents continuity and spoilers.

## QA

The GitHub Actions Director's Cut workflow validated chapter order, unique finale, embedded image data and structural invariants. Browser/device visual tests are separate; the project should be tested on iPhone Safari and desktop before gifting.
