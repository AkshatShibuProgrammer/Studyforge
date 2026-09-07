# Speckit Workflow Manifest: Runtime Guardrails & Resilience

## Metadata
- **Phase ID**: `Phase_00`
- **Directory**: `Phase_00_Runtime_Guardrails_and_Resilience`
- **Total Modules**: 3
- **Governing Constitution**: [constitution.md](file:///f:/Code%20by%20Akshat/testgemini/studyforge/Phase_00_Runtime_Guardrails_and_Resilience/constitution.md)

## Speckit Lifecycle Commands
- `/speckit-constitution`: Inherits master platform rules and phase-specific invariants.
- `/speckit-specify`: [specify.md](file:///f:/Code%20by%20Akshat/testgemini/studyforge/Phase_00_Runtime_Guardrails_and_Resilience/specify.md) & [spec.md](file:///f:/Code%20by%20Akshat/testgemini/studyforge/Phase_00_Runtime_Guardrails_and_Resilience/spec.md)
- `/speckit-clarify`: Gap register items verified against Document 5 and code audit.
- `/speckit-plan`: [plan.md](file:///f:/Code%20by%20Akshat/testgemini/studyforge/Phase_00_Runtime_Guardrails_and_Resilience/plan.md)
- `/speckit-tasks`: [tasks.md](file:///f:/Code%20by%20Akshat/testgemini/studyforge/Phase_00_Runtime_Guardrails_and_Resilience/tasks.md)
- `/speckit-implement`: Integration into `studyforgeImplementation/Mainapp19Jul/actual app/sindhuskeleton.html`.

## Submodules
- **[Mod_01_Canvas_AI_Bridge](Mod_01_Canvas_AI_Bridge/speckit.md)**: Zero-config Gemini 2.5 Flash & Imagen 4.0 fetch client with ambient authorization and exponential retry backoff.
- **[Mod_02_InBrowser_JSON_AutoRepair](Mod_02_InBrowser_JSON_AutoRepair/speckit.md)**: Deterministic bracket stack repair and quote closure for truncated 8192-token streaming responses.
- **[Mod_03_IndexedDB_Persistence_Isolation](Mod_03_IndexedDB_Persistence_Isolation/speckit.md)**: Client-side IndexedDB store (StudyForge_V3_DB) isolating Base64 visuals from 5MB localStorage quota.

## Verification Gate
1. Zero runtime syntax errors in browser context.
2. Compliance with zero-API-key Canvas ambient auth.
3. State persistence strictly isolated from localStorage overflow.
