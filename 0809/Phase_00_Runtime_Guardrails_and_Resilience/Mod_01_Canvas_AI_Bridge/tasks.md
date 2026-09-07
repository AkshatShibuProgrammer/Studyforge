# Tasks: Module 01 — Canvas AI Bridge

## 1. Implementation Tasks
- [ ] Task 01.1: Construct `StudyForge.API` namespace object in JavaScript.
- [ ] Task 01.2: Implement `generateText(prompt, options)` supporting temperature, token limits, and `responseMimeType`.
- [ ] Task 01.3: Implement `searchText(query, options)` wrapping Google Search Grounding.
- [ ] Task 01.4: Implement `generateImage(prompt, aspectRatio)` interacting with Imagen 4.0.
- [ ] Task 01.5: Implement retry loop with exponential sleep (`delays = [2000, 4000]`).
- [ ] Task 01.6: Add execution telemetry writer recording to `app.state.promptHistory`.

## 2. Verification Criteria
* Calling `generateText` in Gemini Canvas returns valid text without throwing 401/403.
* Calling `searchText` with `"current repo rate India"` returns text grounded with web citations.
* Calling `generateImage` returns a valid PNG data URL.
