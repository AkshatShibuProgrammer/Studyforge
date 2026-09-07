# StudyForge — Build Handoff Package

This package is for a new AI/developer who will integrate real Gemini AI into the existing StudyForge UI skeleton.

## Local resources to inspect first

| Resource | Required purpose |
|---|---|
| `F:\Code by Akshat\testgemini\studyforge\studyforgeImplementation\skeleton` | Existing UI skeleton. It defines the current look, feel, screen layout, IDs, CSS, navigation, placeholders, state, and any existing helper functions. Do not rebuild working UI unnecessarily. |
| `F:\Code by Akshat\testgemini\studyforge\resource\way to use gemini text and gemini image` | Existing Gemini text/image integration examples. Extract exact function names, signatures, model usage, grounding options, error handling, and image return format. |
| `F:\Code by Akshat\testgemini\studyforge\resource\notes\new architect` | Read every document in this folder, including Documents 1–7, original plan/skeleton notes, mandatory architecture analysis, and all existing supporting files. |

## Files in this handoff package

1. `StudyForge_New_AI_Build_Master_Prompt.md` — paste into the new AI.
2. `StudyForge_Stage_by_Stage_Integration_Plan.md` — definitive implementation sequence.
3. `StudyForge_Detailed_Implementation_TODO.md` — task-level checklist and acceptance criteria.
4. `StudyForge_Build_Handoff_README.md` — this file.

## Non-negotiable rules

- Inspect actual code before proposing function names or changing UI.
- Keep the app as one HTML file unless the existing product constraint is formally changed.
- Preserve the skeleton look and feel; integrate logic into its existing UI.
- Use canonical prompt text from Document 3 exactly as written.
- Use existing Gemini functions from the integration examples/current skeleton; do not invent a new provider architecture.
- Do not add speculative features.
- Do not claim a feature is done unless tested end-to-end in the actual skeleton.
- Use the 4-part delivery format after every phase: binary status, function map, test walkthrough, honest declaration.
