# Phase 00: Runtime Guardrails, Resilience & Canvas Bridge

## 1. Executive Summary
Phase 00 establishes the rock-solid foundation for the StudyForge application inside the Google Gemini Canvas runtime environment. It eliminates the single greatest point of platform fragility: silent fetch failures, token boundary JSON truncation crashes (`invalid_model_json`), and `localStorage` quota crashes from Base64 images.

---

## 2. Deliverables & Module Breakdown

| Module | Purpose | Status |
|---|---|---|
| **`Mod_01_Canvas_AI_Bridge`** | Ambient auth handling, unified Gemini 3 Flash REST client, Google Search Grounding wrapper, and Imagen 4.0 predict interface. | Specified |
| **`Mod_02_InBrowser_JSON_AutoRepair`** | Streaming quote/bracket auto-repair engine, schema validation, and 2-attempt backoff retry logic. | Specified |
| **`Mod_03_IndexedDB_Persistence_Engine`** | Decoupled `ImageDB` for Base64 visual assets and `localStorage` state schema v3.0 synchronization. | Specified |

---

## 3. Spec-Kit Inventory
- 📜 **`constitution.md`**: Architectural constraints, zero-backend rules, and token policies.
- 📐 **`spec.md`**: Functional requirements (FR-001 through FR-008), user stories, and gap resolutions.
- 📋 **`contracts.md`**: REST API contracts, JavaScript interfaces, error schemas, and IndexedDB stores.
- 🏗️ **`plan.md`**: Implementation roadmap, state machine design, and sequence flows.
- 📌 **`tasks.md`**: Task breakdown, unit tests, and validation acceptance criteria.
