# Speckit Workflow Manifest: Two-Layer Validation Subagent

## Metadata
- **Phase ID**: `Phase_09`
- **Directory**: `Phase_09_Two_Layer_Validation_Subagent`
- **Total Modules**: 3
- **Governing Constitution**: [constitution.md](file:///f:/Code%20by%20Akshat/testgemini/studyforge/Phase_09_Two_Layer_Validation_Subagent/constitution.md)

## Speckit Lifecycle Commands
- `/speckit-constitution`: Inherits master platform rules and phase-specific invariants.
- `/speckit-specify`: [specify.md](file:///f:/Code%20by%20Akshat/testgemini/studyforge/Phase_09_Two_Layer_Validation_Subagent/specify.md) & [spec.md](file:///f:/Code%20by%20Akshat/testgemini/studyforge/Phase_09_Two_Layer_Validation_Subagent/spec.md)
- `/speckit-clarify`: Gap register items verified against Document 5 and code audit.
- `/speckit-plan`: [plan.md](file:///f:/Code%20by%20Akshat/testgemini/studyforge/Phase_09_Two_Layer_Validation_Subagent/plan.md)
- `/speckit-tasks`: [tasks.md](file:///f:/Code%20by%20Akshat/testgemini/studyforge/Phase_09_Two_Layer_Validation_Subagent/tasks.md)
- `/speckit-implement`: Integration into `studyforgeImplementation/Mainapp19Jul/actual app/sindhuskeleton.html`.

## Submodules
- **[Mod_01_Fact_Checking_and_Audit_Agent](Mod_01_Fact_Checking_and_Audit_Agent/speckit.md)**: Pass 2 validator cross-referencing generated assertions against source material and search grounding.
- **[Mod_02_Pedagogical_Container_Auditor](Mod_02_Pedagogical_Container_Auditor/speckit.md)**: Ensures all required containers, LaTeX formulas, and visual explainers are fully rendered.
- **[Mod_03_Auto_Correction_and_Patch_Applier](Mod_03_Auto_Correction_and_Patch_Applier/speckit.md)**: Applies non-destructive surgical patches to generated notes without restarting generation.

## Verification Gate
1. Zero runtime syntax errors in browser context.
2. Compliance with zero-API-key Canvas ambient auth.
3. State persistence strictly isolated from localStorage overflow.
