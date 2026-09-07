# Constitution: Phase 10 — Export & Monolithic Packaging

## 1. Principles
### Rule 1: Zero AI Execution During Export
Under NO circumstances may Screen 8 trigger an API call to Gemini or any external service. Export compilation MUST be 100% deterministic, immediate, and local.

### Rule 2: Strict Exclusion of Internal Planning Data
The exported document MUST NOT contain internal blueprint prompts, validation check logs, draft parts, or developer debug tokens. Only approved notes, explainer diagrams, and current affairs callouts are exported.

### Rule 3: Single-File Canvas Artifact Guarantee
The final assembled file (`sindhuskeleton.html`) MUST remain a single standalone HTML file opening cleanly in Gemini Canvas with zero external build requirements.
