# Specification: Phase 11 — In-Canvas Diagnostics, E2E Testing & Benchmarks

## 1. Functional Requirements
- **FR-1101**: Collapsible Live Diagnostic Drawer rendering:
  - Active Model & Endpoint (`gemini-3-flash-preview`, `imagen-4.0-generate-001`).
  - Roundtrip Latency (ms) and Token Usage Estimator.
  - JSON Auto-Repair Audit (before/after string diffs and repaired token count).
  - Storage Quota Telemetry (`localStorage` usage in KB vs IndexedDB `ImageDB` in MB).
- **FR-1102**: Automated E2E Test Suite executing 5 core verification flows:
  - Test Flow 1: Upload Document -> Extraction -> Deep Analysis -> Parts -> Blueprint -> Notes -> Export.
  - Test Flow 2: Method 2 Topic -> AI-01A Subtopic Expansion -> AI-01B Draft -> Generation -> Export.
  - Test Flow 3: Truncated JSON & Network 429 backoff recovery test.
  - Test Flow 4: Image generation and IndexedDB storage persistence across reloads.
  - Test Flow 5: Screen 8 Export compile verification (asserts zero network calls).
- **FR-1103**: Multi-Domain Benchmark Suite verifying 4 standardized syllabus benchmarks:
  - Benchmark A: Indian Polity (Basic Structure Doctrine, 106th Amendment, Article 21 interpretation).
  - Benchmark B: Macroeconomics (Monetary Policy Transmission, Repo rate trends 2020-2025, GDP calculation).
  - Benchmark C: Modern Indian History (Non-Cooperation Movement, regional uprisings, socio-religious reform).
  - Benchmark D: Science & Technology (CRISPR-Cas9 gene editing, Gaganyaan mission, semiconductor policy).

## 2. Gap Traceability
- Fully eliminates any residual verification gap or regression risk across the 10 prior phases.
