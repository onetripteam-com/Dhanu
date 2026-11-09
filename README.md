# MANIFESTO: REWIND — The Missing Minute

**A completely reimagined, playable anime-inspired birthday adventure starring Dhanu.**

**Live:** https://onetripteam-com.github.io/Dhanu/

The live entry point is one self-contained **index.html**: all original illustrated assets, CSS, and gameplay JavaScript are embedded. No external fonts, tracking, APIs, accounts, or mandatory sound. The full experience runs offline once the HTML file is saved.

## The new story

The world freezes at **11:59 PM**, one minute before Dhanu's birthday. A copper-ringed storm petrel called Nix delivers a warning from Dhanu's future. An army of Minute Hunters is closing in. The Collector, a clockwork enforcer who believes every promised moment must stay locked forever, stands between Dhanu and midnight.

The five episodes:

1. **The Birthday Heist / Catch Me If Time Can** — a banter-filled opening, a rooftop pursuit, and a five-round lane-dodging reaction game.
2. **The Ship That Fights Back** — storm-ships made from abandoned futures, Sanjay on the radio, a five-turn tactical fight against the Iron Mariner, and a mysterious Dhanu echo. **BEGIN**.
3. **The Thousandth Bell** — the Bellkeeper's failed attempts, a colossal Clock Ogre, and an interactive machine repair that actually changes the battle. **RETURN**.
4. **The Impossible Break-In** — Siri inside the archive, Clockguard pursuit, a three-clue vault code, and evidence that future Dhanu reserved the missing minute. **WITNESS**.
5. **The Last Sixty Seconds** — seven-stage fight against the Collector, a quieter confrontation with future Dhanu, and the freely given final gear **CHOOSE**. Midnight finally arrives, with the birthday surprise and a Nix post-credits gag.

The reboot introduces more action, genuine game controls, character-specific jokes, improved pacing, a prominent hero-first opening on phones, and a more visually dramatic finale.

## Controls and progress

- Touch the on-screen buttons, or use **1 / 2 / 3** for rooftop lanes and for **Strike / Guard / Dash** in an active fight.
- Combat enemies telegraph their moves. Wrong choices cost hearts; Nix helps the player recover, so nobody is permanently stuck.
- The bell mechanism has two parts to repair before striking.
- The Vesper vault uses a code derived from three illustrated clues.
- The final dialogue choice unlocks the birthday ending after defeating or skipping the Collector.
- Every game has **Story Mode · Skip** for readers who prefer the narrative.
- Progress stays in **localStorage on that browser**. **Reset Missions & Replay** clears only the new MANIFESTO: REWIND progress after confirmation.
- The top **EPISODES** menu allows free navigation; puzzles are never an involuntary trap.

## Edit the project

The editable source lives in:
- `reboot/story.html` — plot, character dialogue, the five episode layouts, and illustration placements.
- `reboot/style.css` — visual direction, animation, desktop and mobile layouts.
- `reboot/game.js` — real game mechanics, progression, saves, replay and keyboard controls.
- `reboot/build.py` — produces a **single** `index.html`, embedding original artwork from the archived edition.
- `reboot/qa.cjs` — extended Chromium/WebKit browser and gameplay checks.
- `reboot/quick-qa.cjs` — the faster verified launch checks.

The prior working Studio Edition II is preserved in `archive/studio-edition-ii.html`. The separate `chapter-five.html` is an older alternate finale and is not part of the canonical new story.

**Do not run the old Studio Edition II transforms over the reboot** or edit the generated index alone if changes should survive the next build.

## QA and known limitations

- Extended automated Chromium and WebKit tests passed on 360, 393, 402, and 1440px viewports, including the interaction flow, wrong move penalties, all boss fights, the ending, local saves and reset. WebKit was tested at 393 and 1440px.
- A subsequent hero-first mobile-cover revision passed the verified Chrome smoke test. The artwork appears within the first phone screen rather than below the fold.
- All 18 reused original embedded illustrations load; there is no external network request or page-wide horizontal overflow in the tested builds.
- This remains an **original-asset reboot**. The battles include animated CSS enemies and effects; new fully illustrated fight keyframes and frame-by-frame animation can be a later art pass.
- Physical iPhone Safari has not been personally tested; browser-engine simulation is useful but not identical.

For story spoilers and consistency rules see `STORY_BIBLE.md`.
