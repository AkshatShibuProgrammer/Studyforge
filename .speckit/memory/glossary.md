# StudyForge Domain Glossary & Terminology Reference

| Term | Definition in StudyForge Canvas Platform |
| :--- | :--- |
| **AppState** | The single source of truth JavaScript object (`window.app.state`) containing document metadata, scope subtopics, extracted text, raw chunks, understanding nodes, blueprints, generated notes, and PYQ analysis. |
| **Canvas Sandbox** | The iframe browser execution environment in Google Gemini Canvas where `apiKey = ""` triggers automatic ambient token interception by Google's reverse proxy. |
| **Ambient Auth** | Native zero-config authorization in Gemini Canvas. REST calls to `generativelanguage.googleapis.com` succeed with empty `key=` query parameters via runtime headers. |
| **Guardrails & Repair** | `StudyForge.Guardrails.safeParseJSON` - deterministic streaming bracket/quote repair balancing truncated JSON from 8192-token streaming responses. |
| **ImageDB** | `StudyForge.ImageDB` - dedicated client-side IndexedDB store (`StudyForge_V3_DB`) isolating large Base64 generated diagrams from localStorage to prevent browser quota crashes. |
| **Dual-Pass Dynamic CA** | Generation architecture: Pass 1 executes real-time search swarm; Pass 2 employs a dedicated Validator subagent to fact-check, verify recency, and append citations. |
| **Multi-Exam PYQ Intelligence** | Retrieval and alignment engine matching notes to authentic past-year questions from MPPSC, UPSC, and State PSCs with model answers, mark weights, and trap analysis. |
| **Self-Explanatory Visuals** | Imagen 4.0 2D vector conceptual schematics generated alongside a 3-column breakdown: (1) Component Legend, (2) Mechanism / Process Flow, (3) Exam Takeaway. |
| **Pedagogical Containers** | 22 curated CSS callout blocks (`formula-box`, `concept-trap`, `mnemonic`, `case-law`, `comparative-matrix`, etc.) designed for visual study engagement. |
| **Deterministic Export** | Clean HTML, Markdown, and print-ready PDF generator compiling generated notes, diagrams, and PYQ cards without external dependencies. |
| **Thinking Tier** | Adaptive reasoning budget in Gemini 3.7 Flash (`1024` tokens for indexing, `4096` for blueprints, `8192` for notes generation). |
