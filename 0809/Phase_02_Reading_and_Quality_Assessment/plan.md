# Implementation Plan: Phase 02 — Reading & Quality Assessment

## Steps
1. Ingest uploaded file -> Execute technical extraction.
2. Run heuristic quality check.
3. If degraded, chunk text (24,000 char windows) -> Call AI-02A -> Re-assess.
4. If still degraded, chunk text -> Call AI-02B -> Re-assess.
5. Populate `#extraction-preview` -> User clicks Confirm Extraction -> Navigate to Screen 3.
