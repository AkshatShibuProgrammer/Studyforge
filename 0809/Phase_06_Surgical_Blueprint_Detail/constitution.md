# Constitution: Phase 06 — Surgical Blueprint Detail

## 1. Principles
### Rule 1: Scoped Atomic Patching
Assistant chat MUST NOT regenerate the entire blueprint. It MUST emit atomic JSON patch operations (`replace`, `add`, `remove`) targeted at stable section paths (`/image_plan`, `/text_plan`, `/headings`, `/ca_plan`).

### Rule 2: Mandatory Undo Payload
Every executed patch MUST snapshot the pre-change state into `app.state.blueprintUndo[part_id]` to guarantee instant, single-click restoration.
