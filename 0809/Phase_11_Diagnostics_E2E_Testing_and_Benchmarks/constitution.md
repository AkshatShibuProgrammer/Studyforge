# Constitution: Phase 11 — In-Canvas Diagnostics, E2E Testing & Benchmarks

## 1. Principles
### Rule 1: Non-Intrusive Production Diagnostics
The live diagnostic drawer MUST remain completely non-intrusive. In standard user mode, it is collapsed into a small floating telemetry badge or triggered via `Ctrl + ~` / `Cmd + ~`. It must never obstruct study notes or alter the primary canvas layout.

### Rule 2: Zero-Dependency Client-Side Testing
The test harness MUST be capable of running entirely in the browser using native JavaScript assertions without requiring Jest, Playwright, or external test runners, while exposing an external hook for automated Playwright execution when run in CI/headless environments.

### Rule 3: Objective Exam Grading Rubric
The benchmark suite MUST score generated notes against objective 100-point rubrics (30 pts Conceptual Rigor, 25 pts Exam/PYQ Relevance, 20 pts Current Affairs Recency, 15 pts Visual Self-Explanation, 10 pts Traceability & Traps). Notes scoring under 90 points trigger regression alerts.
