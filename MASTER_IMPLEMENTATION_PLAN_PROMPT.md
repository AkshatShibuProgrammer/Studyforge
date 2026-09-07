# MASTER PROMPT: STUDYFORGE ARCHITECTURAL REBUILD

## ROLE
You are a Lead Full-Stack Architect. Your job is to take an "imperfect" single-file prototype and rebuild it into the "Complete Product" specified in the 8-screen documentation.

## CONTEXT
Folder: `F:\Code by Akshat\testgemini\studyforge\resource\notes\new architect`
You must read the following:
1. The original "Complete Product Document" (8 Screens).
2. Document 5 (56 Gaps/Amendments Register).
3. Document 6 (Master AI Usage Table - 20 Calls).
4. The provided code images (Architecture Foundation).

## EXISTING ARCHITECTURE RULES (DO NOT CHANGE)
- **Single HTML File:** Maintain everything in one file.
- **AI Functions:** Use the existing `API.streamContent`, `API.generateContent`, and `API.generateImage` patterns.
- **Persistence:** Use the existing `appState` with `localStorage` and `ImageDB` (IndexedDB) for assets.
- **Prompt Logic:** Keep the `PromptRegistry` and `DEFAULT_PROMPTS` object. Do not hide the prompts; they must be editable.

## REBUILD INSTRUCTIONS
1. **Expand Screens:** The current code has 4 steps. You MUST expand this to 8 distinct logical screens as per the product document.
2. **Fix Routing:** Replace the current step logic with the `navigate(n)` (forward/state-save) vs `navTo(n)` (backward/jump) logic.
3. **Prompt Injection:** Use the prompts from the "Canonical Stored Prompt Library" verbatim.
4. **Validation:** Implement the two-layer validation workflow (Per-part summary popup + Final consolidated gap analysis).
5. **Container System:** Implement the 22+ styled containers in CSS and create a JS renderer that maps AI output to these classes.

## OUTPUT
Generate the full, corrected source code for `studyforge.html`. Ensure every one of the 56 gaps from Document 5 is addressed in the code comments and logic.
