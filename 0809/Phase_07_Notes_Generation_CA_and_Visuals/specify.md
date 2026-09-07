# Functional Specification: Notes Generation, Dynamic Current Affairs & Visuals

## 1. Scope & Objective
Core generation engine executing Pass 1 notes generation, search-grounded Current Affairs swarm, and self-explanatory visual synthesis.

## 2. Requirements & Acceptance Criteria
- **Architecture**: Must run 100% client-side inside `sindhuskeleton.html`.
- **Interface Contract**: Exposes clean functions on `window.app` or `window.StudyForge`.
- **Resilience**: Comprehensive try-catch wrapping with user-facing toasts on failure.

## 3. Submodule Specifications
### [Mod_01_High_Fidelity_Notes_Generator](Mod_01_High_Fidelity_Notes_Generator/specify.md)
Generates rich markdown notes formatted with all 22 pedagogical containers and LaTeX equations.

### [Mod_02_Dynamic_Search_Grounding_Swarm](Mod_02_Dynamic_Search_Grounding_Swarm/specify.md)
Pass 1 live Google search swarm retrieving latest policies, judgments, and statistical indicators.

### [Mod_03_Imagen_Schematic_Synthesis](Mod_03_Imagen_Schematic_Synthesis/specify.md)
Calls Imagen 4.0 to generate 2D conceptual diagrams stored directly into ImageDB.

### [Mod_04_Self_Explanatory_Visual_Explainer](Mod_04_Self_Explanatory_Visual_Explainer/specify.md)
Generates 3-column HTML explainer (Component Legend, Mechanism Flow, Exam Takeaway).

### [Mod_05_Pedagogical_Container_Renderer](Mod_05_Pedagogical_Container_Renderer/specify.md)
Parses markdown into interactive, styled HTML components in Screen 8.

