# Architectural Decision Records (ADR) — StudyForge Platform

## ADR-001: Pure Client-Side Single-File Monolithic Runtime
- **Context**: StudyForge runs inside Google Gemini Canvas, which only accepts HTML/CSS/JavaScript and cannot host Node.js, Python, LangChain, or databases.
- **Decision**: All application logic, state management, parsing, rendering, and validation must exist entirely within `sindhuskeleton.html` in vanilla JavaScript.
- **Status**: Accepted & Enforced.

---

## ADR-002: Ambient Authorization (Zero API Key Input)
- **Context**: Requiring users to enter Gemini API keys creates friction and violates Canvas UX guidelines. Canvas intercepts empty keys and adds platform credentials.
- **Decision**: Default `apiKey = ""`. Calls to `https://generativelanguage.googleapis.com` use empty key parameter.
- **Status**: Accepted & Implemented in `StudyForge.API`.

---

## ADR-003: In-Browser Truncated JSON Auto-Repair
- **Context**: LLM calls with `maxOutputTokens: 8192` can be abruptly truncated mid-stream, resulting in broken JSON that crashes standard `JSON.parse`.
- **Decision**: Implement `StudyForge.Guardrails.safeParseJSON` with quote closure, bracket stack balancing (`}`, `]`), and dangling key trimming.
- **Status**: Accepted & Implemented in Phase 00.

---

## ADR-004: IndexedDB Storage Isolation for Generated Visuals
- **Context**: Storing Base64 images directly in `localStorage` quickly exceeds the browser's 5MB limit, causing fatal `QuotaExceededError`.
- **Decision**: Store all image payloads in IndexedDB (`StudyForge_V3_DB`). Cleanse image fields before serializing `app.state` to `localStorage`.
- **Status**: Accepted & Implemented in Phase 00.

---

## ADR-005: Dual-Pass Dynamic Current Affairs Pipeline
- **Context**: Static notes lack recent events, policy updates, and statutory amendments required for civil services exams.
- **Decision**: Pass 1 generates notes with search grounding. Pass 2 deploys a dedicated Validator subagent to cross-reference and verify fact accuracy.
- **Status**: Accepted & Planned in Phases 07 & 09.

---

## ADR-006: Multi-Exam PYQ Intelligence Layer
- **Context**: Aspirants preparing for MPPSC, UPSC, and other state PSCs need direct question-to-concept mapping with authentic model answers.
- **Decision**: Implement a dedicated PYQ extraction and analysis engine classifying questions by exam board, tier (Prelims/Mains), marks, and traps.
- **Status**: Accepted & Planned in Phase 08.

---

## ADR-007: Self-Explanatory Visual Schematics
- **Context**: Raw AI images often contain hallucinated text or lack educational context.
- **Decision**: Pair every Imagen schematic with an HTML 3-column explainer: Component Legend, Mechanism Breakdown, and Exam Takeaway.
- **Status**: Accepted & Planned in Phase 07.
