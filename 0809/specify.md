# Master System Specification — StudyForge AI Study Material Transformer

## 1. Vision & Purpose
StudyForge is an exam-grade AI Study Material Transformer designed to run natively inside **Google Gemini Canvas** as a single monolithic HTML/CSS/Vanilla JS application. It converts raw textbooks, PDFs, exam syllabi, and notes into structured, pedagogical study guides featuring dynamic current affairs, authentic past-year questions (MPPSC, UPSC, State PSCs), and self-explanatory visual schematics.

## 2. Platform Constraints & Inviolable Principles
- **Monolithic Single File**: All code must reside in `sindhuskeleton.html`. Zero external build scripts or node runtimes.
- **Ambient Canvas Auth**: Default `apiKey = ""`. Canvas automatically provides authorization tokens on runtime fetch requests.
- **Storage Quota Preservation**: LocalStorage limit is 5MB. Large Base64 visuals must be routed to client-side IndexedDB (`StudyForge_V3_DB`).
- **Resilient Parsing**: Streaming truncation from Gemini 2.5 Flash (`maxOutputTokens: 8192`) must be auto-repaired in-browser without crashing.
- **Rich Educational Typography**: Full support for 22 pedagogical CSS containers and KaTeX mathematical notation.

## 3. Core Functional Workflows
1. **Intake & Scope**: Upload PDF/DOCX/TXT or paste text/clipboard screenshots. Dynamically generate and refine subtopics with AI-01A/AI-01B.
2. **Quality Audit & Understanding**: Algorithmic assessment of source depth, gap detection, and ontology tree construction.
3. **Blueprint & Sizing**: Partition study material into token-budgeted chapters with explicit container assignments and visual prompts.
4. **Pass 1 Generation & Search Grounding**: Generate rich notes with embedded Google search grounding for real-time current affairs.
5. **Multi-Exam PYQ Analysis**: Match notes to real past-year questions from MPPSC, UPSC, and State PSCs with model answers.
6. **Pass 2 Validation**: Dedicated Validator subagent checks facts, verifies recency, and applies non-destructive patches.
7. **Assembly & Export**: Deterministic export to self-contained HTML, Markdown, or paginated print-ready PDF.
