# Specification: Phase 09 — Two-Layer Validation Subagent

## 1. Requirements
- **FR-901**: AI-07H evaluates part notes against blueprint, source slice, and active bundles.
- **FR-902**: Suggestion actions:
  - `update_text`: Injects replacement text into target anchor.
  - `add_container`: Appends missing clarification or formula container.
  - `fetch_ca`: Executes targeted research query.
  - `update_image`: Calls AI-07K to adapt suggestion into concrete Imagen visual.
- **FR-903**: Validator Subagent Pass 2: Automated inspection for dated statements (e.g. referencing 2019 without mentioning 2024 amendments).
- **FR-904**: AI-07I final validation: Cross-part continuity check and dynamic Part addition proposal (`applyFinalSuggestion`).

## 2. Gap Traceability
- Eliminates GAP-23 (Missing second-pass CA verification).
- Eliminates GAP-27 (Validation popups offering generic text without one-click fixes).
- Eliminates GAP-28 (Validation visual suggestions not translating to concrete image calls).
