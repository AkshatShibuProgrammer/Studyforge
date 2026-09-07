# Implementation Plan: Phase 01 — Ingestion, Scope & Multi-Method Input

## 1. Sequence Flow
1. User chooses Method 1, 2, or 3.
2. If Method 1: Client libraries extract text -> Populate `app.state.sourceDocument` -> Navigate to Screen 2.
3. If Method 2: AI-01A expands scope -> Render approval panel -> User approves -> AI-01B drafts text -> Write to `#paste-area` -> User edits -> Navigate directly to Screen 3.
4. If Method 3: User pastes text -> Update character count -> Navigate to Screen 3.

## 2. Failure Recovery
- If PDF extraction fails: Display clear file error; offer fallback to paste or AI Draft.
- If AI-01A returns invalid JSON: In-browser auto-repair rescues partial topics.
