# Specification: Phase 04 — Pedagogical Part Splitting & Structure

## 1. Requirements
- **FR-401**: AI-04 execution receiving deep analysis JSON, active bundles, and page count.
- **FR-402**: Schema validation enforcing `part_id`, `title`, `page_range`, `topic_ids`, `analysis_refs`, `applied_bundles`, and `rationale`.
- **FR-403**: Interactive part card grid displaying applied bundle badges and entity statistics.
- **FR-404**: Reorder controls (Move Up / Move Down) updating `part.num` and re-indexing.
- **FR-405**: Merge Parts modal combining analysis refs, topic IDs, and bundle lists.
- **FR-406**: Edit Settings modal for custom title and page range modifications.

## 2. Gap Traceability
- Eliminates GAP-14 (Part splitting ignoring density and page guardrails).
- Eliminates GAP-15 (Part merge operation stubbed or dropping bundle definitions).
