# Tasks: Module 02 — In-Browser JSON Auto-Repair

## 1. Implementation Tasks
- [ ] Task 02.1: Implement `cleanRawString()` extracting content between outer brackets.
- [ ] Task 02.2: Implement `scanTokensAndBalance()` tracking quote state and brace stack.
- [ ] Task 02.3: Implement `trimDanglingSyntax()` removing orphaned commas and trailing keys.
- [ ] Task 02.4: Implement `StudyForge.Guardrails.safeParseJSON()`.
- [ ] Task 02.5: Create schema default injection for `headings`, `html_blocks`, `topics`, `pyqs`.

## 2. Verification Criteria
* Successfully parses Test Scenarios T-01, T-02, T-03, and T-04 without throwing.
* Returns fallback object without crashing if string is completely unrecoverable gibberish.
