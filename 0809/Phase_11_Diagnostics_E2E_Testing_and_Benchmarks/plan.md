# Implementation Plan: Phase 11 — In-Canvas Diagnostics, E2E Testing & Benchmarks

## Steps
1. Build `#sf-diagnostic-drawer` in HTML with tabbed views (Logs, Storage, Telemetry, Test Suite).
2. Wire telemetry event emitter into `StudyForge.API` and `StudyForge.Guardrails`.
3. Build lightweight client-side assertion runner `StudyForge.TestRunner`.
4. Implement synthetic mock data generators for automated E2E testing.
5. Create benchmark evaluation evaluator running test notes through rubric grading prompts.
6. Provide one-click "Run All Self-Tests" button in diagnostic panel.
