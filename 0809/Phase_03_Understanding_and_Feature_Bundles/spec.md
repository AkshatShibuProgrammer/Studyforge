# Specification: Phase 03 — Understanding & Feature Bundles

## 1. Requirements
- **FR-301**: AI-03A detects primary subject, sub-discipline, purpose, and 12 signal strengths (strong/weak/not_detected).
- **FR-302**: AI-03B deep core extraction across chunks, merging duplicates while preserving page numbers.
- **FR-303**: Deterministic bundle routing: only signals detected as strong or weak trigger bundle fragments in AI-03C.
- **FR-304**: 3-Tier Visual UI: Green (Auto-on), Yellow (Suggested), Grey (Not detected) with evidence tooltips.
- **FR-305**: Manual Analysis Correction Editor modal permitting full editing of signals, topics, and definitions JSON.

## 2. Gap Traceability
- Eliminates GAP-10 (Hardcoded subject headings).
- Eliminates GAP-11 (Granular extraction lacking stable IDs).
- Eliminates GAP-12 (Feature bundles lacking 3-tier visual hierarchy).
- Eliminates GAP-13 (Manual analysis editor not invalidating downstream state).
