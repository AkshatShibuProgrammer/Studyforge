# Implementation Plan: Phase 04 — Pedagogical Part Splitting & Structure

## Steps
1. Calculate page guardrail range from source document metrics.
2. Formulate AI-04 prompt payload with deep analysis summary and active bundles.
3. Call `StudyForge.API.generateText` -> Parse via JSON Auto-Repair.
4. Validate that all topic IDs are assigned.
5. Populate `app.state.parts` -> Render Screen 4 cards.
6. Wire Reorder, Merge, Add, Remove event handlers with automated downstream invalidation.
