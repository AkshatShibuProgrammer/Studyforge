# Specification: Phase 02 — Reading & Quality Assessment

## 1. Requirements
- **FR-201**: Page-by-page extraction maintaining `pageMap: Array<{page: number, text: string}>`.
- **FR-202**: Quality heuristic calculating printable ratio, replacement chars (``, `□`), and empty page percentage.
- **FR-203**: Automatic tier escalation: if `quality !== 'usable'`, automatically trigger `AI-02A` (Cleanup), followed by `AI-02B` (Restructure) if still degraded.
- **FR-204**: Editable source preview panel allowing user to inspect and confirm final extracted text.

## 2. Gap Traceability
- Eliminates GAP-08 (Incomplete extraction quality heuristics).
- Eliminates GAP-09 (Simplified recovery prompts; restores full canonical AI-02A/B).
