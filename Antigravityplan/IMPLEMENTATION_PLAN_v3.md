# StudyForge Implementation Plan v3: Gap Analysis & Architectural Realignment

## Background
Following the initial implementations, a deep audit was conducted against `StudyForge_Document_5_Missing_Features_and_Agreed_Amendments_Register.md` and the `Single HTML File Architecture.txt` mandate.

**CRITICAL FINDING:** The previous iteration of `studyforge_main.html` violated the strict Single HTML File Architecture by utilizing React JSX and Babel via CDNs. The architecture mandate explicitly states: *"Do NOT use any framework that requires a build step (React JSX, Vue SFC, etc.)"* and mandates a **Vanilla JavaScript Namespace (Object Literal) Pattern** (`API`, `State`, `Screen1_Input`, etc.).

This v3 plan outlines the roadmap to strictly realign the codebase to Vanilla JS while simultaneously resolving all missing feature gaps.

---

> [!WARNING]
> **User Review Required: Architectural Rewrite**
> The most significant step in this plan is removing React/Babel and rewriting the UI rendering logic into Vanilla JavaScript string literals and DOM manipulation. This guarantees 100% portability without relying on in-browser compilers. Please confirm this strict adherence is desired before execution begins.

---

## Identified Gaps (What is Missing/Partial)

### 1. Architectural Violations (The React Problem)
- **Gap 1: React Dependency:** The codebase uses JSX and Babel. It must be refactored to use Vanilla JS with `document.getElementById` and `innerHTML`.
- **Gap 2: Missing Namespaces:** The logic is coupled in React components. It must be explicitly separated into `API`, `State`, `Session`, `Prompts`, `UI`, and individual `Screen1` through `Screen8` namespace objects.

### 2. Phase 1: Input & Method 2 (AI Draft)
- **Gap 3: Dynamic Sub-topics:** The UI currently has fixed inputs for sub-topics. It requires a dynamic list (up to 10) with Add/Remove controls.
- **Gap 4: AI Draft Workflow:** Missing the intermediate "User Approval Panel" where users can review/edit expanded topics before the final draft is generated (AI-01A to AI-01B).
- **Gap 5: Internet & CA Toggles:** Missing explicit toggles for `Search internet for this topic` and `Include Current Affairs for this topic`.

### 3. Phase 2: Reading & Extraction
- **Gap 6: Semantic Chunking:** Missing semantic chunking for large PDFs. Needs structured merge and deduplication instead of arbitrary substring slicing.
- **Gap 7: Manual Cascade Override:** Missing UI controls for the user to manually force "Technical Extraction", "AI Cleanup", or "AI Restructure".

### 4. Phase 3: Analysis Engine
- **Gap 8: Three-Tier Bundle UI:** Needs the "Green (auto-on), Yellow (suggested), Grey (force-enable)" visual tiering with evidence tooltips on hover.
- **Gap 9: Detailed Summary Counts:** Missing the dedicated counts row: `📚 topics • definitions • formulas • PYQs • diagrams • comparisons • examples • timelines • tables`.

### 5. Phase 4: Parts & Coherence
- **Gap 10: Advanced Part Editing:** Missing fields for topic/formula counts, applied bundle chips, and page-guide deviation warnings in the part editor.
- **Gap 11: Part Operations:** Missing "Merge Parts" action and downstream stale-flag updates.

### 6. Phase 5 & 6: Blueprints (Screen 5 & 6)
- **Gap 12: Surgical AI Chat (Screen 6):** Missing surgical AI chat, visible diff highlights, lightweight Undo, and section-only regeneration logic.

### 7. Phase 7: Generation, Visuals, and CA
- **Gap 13: Specialized Rendering Containers:** Must implement Vanilla JS HTML templates for Geography, Bio, Formula, Data, Institution, Analogy, Process, Experiment, and Medical Info boxes.
- **Gap 14: Two-Layer Validation:** Missing the **Final Cross-Document Validation** (`AI-07I`) that runs after all parts are approved.
- **Gap 15: Add/Remove Parts Dynamically:** Missing Quick Blueprint flows in Screen 7.

### 8. Phase 8: Export
- **Gap 16: Export Screen:** Must implement compiling approved text, safe images, CA blocks, and citations into a clean view with "Copy" and "Save PDF" options (no AI execution).

---

## Proposed Implementation Roadmap (v3)

### Step 1: Architectural Foundation (Vanilla JS Rewrite)
- Strip all React/Babel code from `studyforge_main.html`.
- Establish the Vanilla JS Namespace skeleton (`API`, `State`, `Session`, `Prompts`, `UI`).
- Implement the baseline 8 screen namespaces (`Screen1_Input` through `Screen8_Export`) with basic HTML string rendering.
- Wire up `localStorage` JSON persistence as mandated.

### Step 2: Input & Extraction Precision (Screens 1 & 2)
- Build the dynamic sub-topic UI in Vanilla JS.
- Implement the AI Draft User Approval Panel.
- Write the semantic chunking logic for PDF extraction.

### Step 3: Analysis & Parts (Screens 3 & 4)
- Implement the 3-tier bundle UI with DOM event listeners for hover tooltips.
- Add detailed summary counts parsing.
- Build the manual part-merging logic and metadata editors.

### Step 4: Blueprints & Generation (Screens 5, 6 & 7)
- Build the interactive Blueprint Overlay (Screen 6) with Vanilla JS diff rendering.
- Implement the 10 specific HTML/CSS specialized rendering containers.
- Wire up the Final Cross-Document Validation (`AI-07I`).

### Step 5: Export Compilation (Screen 8)
- Build the final export compilation screen merging all approved HTML.

---
## Verification Plan

### Manual Verification
- **Architecture Validation:** Ensure no `<script type="text/babel">` or React CDN links exist in the file.
- **Zero-Dependency Check:** Verify the file opens immediately with `file://` protocol and no build tools.
- **Feature Check:** Walk through the 8 stages to ensure the new Vanilla JS implementation matches or exceeds the capabilities of the former React prototype.
