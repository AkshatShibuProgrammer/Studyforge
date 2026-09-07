# Speckit Workflow Manifest: Multi-Exam PYQ Intelligence Layer

## Metadata
- **Phase ID**: `Phase_08`
- **Directory**: `Phase_08_Multi_Exam_PYQ_Intelligence_Layer`
- **Total Modules**: 3
- **Governing Constitution**: [constitution.md](file:///f:/Code%20by%20Akshat/testgemini/studyforge/Phase_08_Multi_Exam_PYQ_Intelligence_Layer/constitution.md)

## Speckit Lifecycle Commands
- `/speckit-constitution`: Inherits master platform rules and phase-specific invariants.
- `/speckit-specify`: [specify.md](file:///f:/Code%20by%20Akshat/testgemini/studyforge/Phase_08_Multi_Exam_PYQ_Intelligence_Layer/specify.md) & [spec.md](file:///f:/Code%20by%20Akshat/testgemini/studyforge/Phase_08_Multi_Exam_PYQ_Intelligence_Layer/spec.md)
- `/speckit-clarify`: Gap register items verified against Document 5 and code audit.
- `/speckit-plan`: [plan.md](file:///f:/Code%20by%20Akshat/testgemini/studyforge/Phase_08_Multi_Exam_PYQ_Intelligence_Layer/plan.md)
- `/speckit-tasks`: [tasks.md](file:///f:/Code%20by%20Akshat/testgemini/studyforge/Phase_08_Multi_Exam_PYQ_Intelligence_Layer/tasks.md)
- `/speckit-implement`: Integration into `studyforgeImplementation/Mainapp19Jul/actual app/sindhuskeleton.html`.

## Submodules
- **[Mod_01_Exam_Board_Question_Extractor](Mod_01_Exam_Board_Question_Extractor/speckit.md)**: Retrieves authentic past-year questions filtered by target exam board and tier (Prelims/Mains).
- **[Mod_02_Model_Answer_and_Trap_Analyzer](Mod_02_Model_Answer_and_Trap_Analyzer/speckit.md)**: Synthesizes standard model answers and highlights common examiner deception traps.
- **[Mod_03_Interactive_PYQ_Card_Renderer](Mod_03_Interactive_PYQ_Card_Renderer/speckit.md)**: Renders interactive flip cards, self-assessment scoring, and difficulty tags in the study view.

## Verification Gate
1. Zero runtime syntax errors in browser context.
2. Compliance with zero-API-key Canvas ambient auth.
3. State persistence strictly isolated from localStorage overflow.
