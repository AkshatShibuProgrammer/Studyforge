# Implementation Plan: Phase 03 — Understanding & Feature Bundles

## Steps
1. Chunk canonical source into 24,000 char blocks.
2. Execute AI-03A across chunks -> Merge signal vectors.
3. Execute AI-03B across chunks -> Deduplicate entities by term/formula/id.
4. Route active signals -> Assemble prompt fragments -> Execute AI-03C.
5. Render Screen 3 dashboard: Subject badge, Summary count chips, 3-tier bundle cards, and Details tables.
