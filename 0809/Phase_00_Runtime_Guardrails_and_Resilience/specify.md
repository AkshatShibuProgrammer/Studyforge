# Functional Specification: Runtime Guardrails & Resilience

## 1. Scope & Objective
Establishes zero-config Gemini Canvas API bridge, in-browser streaming JSON auto-repair, and IndexedDB image isolation.

## 2. Requirements & Acceptance Criteria
- **Architecture**: Must run 100% client-side inside `sindhuskeleton.html`.
- **Interface Contract**: Exposes clean functions on `window.app` or `window.StudyForge`.
- **Resilience**: Comprehensive try-catch wrapping with user-facing toasts on failure.

## 3. Submodule Specifications
### [Mod_01_Canvas_AI_Bridge](Mod_01_Canvas_AI_Bridge/specify.md)
Zero-config Gemini 2.5 Flash & Imagen 4.0 fetch client with ambient authorization and exponential retry backoff.

### [Mod_02_InBrowser_JSON_AutoRepair](Mod_02_InBrowser_JSON_AutoRepair/specify.md)
Deterministic bracket stack repair and quote closure for truncated 8192-token streaming responses.

### [Mod_03_IndexedDB_Persistence_Isolation](Mod_03_IndexedDB_Persistence_Isolation/specify.md)
Client-side IndexedDB store (StudyForge_V3_DB) isolating Base64 visuals from 5MB localStorage quota.

