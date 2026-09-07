# Implementation Plan: Phase 06 — Surgical Blueprint Detail

## Steps
1. Open Overlay `#overlay-blueprint` -> Populate 5 tabs.
2. User enters request in assistant chat -> Call AI-06A.
3. Verify patch paths against whitelist (`headings`, `text_plan`, `image_plan`, `ca_plan`, `validation_plan`).
4. Save snapshot in `blueprintUndo` -> Apply patch operations in memory.
5. Re-render affected sections and display scope explanation in chat.
