# Implementation Plan: Phase 08 — Multi-Exam PYQ Intelligence Layer

## Steps
1. Read user's target exam selection from `app.state.inputProfile.options.exam`.
2. Formulate domain prompt querying past 5-10 year question patterns for the active topic.
3. Call `StudyForge.API.generateText` -> Parse and extract PYQs with solutions.
4. Render dedicated `#c-exam-pyq` container at the conclusion of each generated part.
