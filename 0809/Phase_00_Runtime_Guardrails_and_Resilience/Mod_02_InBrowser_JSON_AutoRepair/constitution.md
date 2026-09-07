# Constitution: Module 02 — In-Browser JSON Auto-Repair

## 1. Principles

### Rule 1: No Uncaught Syntax Exceptions
Direct invocation of `JSON.parse()` without guardrail wrapper protection is STRICTLY PROHIBITED throughout the entire codebase. All AI responses MUST pass through `StudyForge.Guardrails.safeParseJSON()`.

### Rule 2: Non-Destructive Incomplete Data Rescue
When repairing truncated payloads, the parser MUST preserve all complete sibling keys and array elements that were generated prior to the cut-off point. It must never discard the entire object merely because the final key was truncated.

### Rule 3: Diagnostic Transparency
Whenever a repair is performed, the resulting object MUST be tagged with `_repaired: true` and an entry appended to the telemetry log indicating the characters appended or pruned.
