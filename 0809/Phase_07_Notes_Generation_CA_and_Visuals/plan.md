# Implementation Plan: Phase 07 — Notes Synthesis, CA & Visuals

## Steps
1. Fetch CA swarm in parallel using `geminiSearchText` for blueprint queries.
2. Build AI-07A payload: Source slice + Deep analysis + Active bundles + Subject Strategy (`STRAT-*`) + Fetched CA.
3. Call `StudyForge.API.generateText` -> Parse via JSON Auto-Repair.
4. Loop through `image_needed` requests -> Expand prompt via AI-07B -> Generate image via Imagen 4.0 -> Generate paired component map & exam takeaway -> Store in IndexedDB.
5. Render Screen 7 card using 22 pedagogical container renderers.
