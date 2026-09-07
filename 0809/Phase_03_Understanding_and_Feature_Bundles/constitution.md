# Constitution: Phase 03 — Understanding & Feature Bundles

## 1. Principles
### Rule 1: Stable Entity Identification
Every extracted entity MUST have a prefixed stable identifier (`T-`, `D-`, `F-`, `PYQ-`, `CMP-`, `EX-`, `TL-`, `TB-`, `DG-`, `LOC-`, `PER-`, `LAW-`, `PR-`, `KF-`) and retain source page references.

### Rule 2: Downstream Stale-State Invalidation
Any manual modification to subject signals, topics, or definitions MUST automatically invalidate downstream parts, blueprints, and generated notes, setting `status: 'stale'`.
