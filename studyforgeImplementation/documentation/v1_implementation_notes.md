# StudyForge V1 Implementation Notes

## Overview
This document outlines the implementation details for **StudyForge V1**. In this version, we have established the foundational architecture of the monolithic application and fully implemented **Stage 1 (Input Material)** with AI integration. Stages 2-8 exist as dummy skeletons to be built out in future versions.

## Foundational Architecture
1. **Single File Structure:** Everything is contained within `studyforge_v1.html`.
2. **Tech Stack:**
   - React 18 & ReactDOM (loaded via CDN)
   - Babel (for in-browser JSX compilation)
   - Tailwind CSS (for modern UI styling)
   - PDF.js (for client-side PDF text extraction)
3. **State Management (`IndexedDB`):**
   - Implemented a custom `IndexedDB` wrapper (`const DB = {...}`) to avoid `localStorage` quota limits (which typically crash at 5MB when storing base64 images).
   - The app auto-saves the user's `appState` every time an input is changed.
4. **AI Core:**
   - The three core AI functions (`geminiGenerateText`, `geminiSearchText`, `geminiImageCreation`) are injected at the top of the script block. They use the empty `apiKey` string hack to utilize the Gemini Canvas runtime environment authentication.

## Stage 1 Implementation
The `Screen1Input` React component is fully functional. It is clearly demarcated in the codebase with `STAGE 1 START` and `STAGE 1 END` comments.

It features three input methods:
- **Method A (Upload File):** Users can drag-and-drop or select PDF, TXT, MD, or HTML files. The `FileReader` API handles plain text, while `pdfjsLib` extracts text from PDFs locally in the browser.
- **Method B (Type Topic & Generate):** 
  - **AI Integration Active:** Users can input a Main Topic, Sub-topics, and a Specific Focus.
  - Clicking the "Auto-Draft Material" button triggers the `geminiGenerateText` function. 
  - The AI drafts a comprehensive ~600-word study guide based on the topic.
- **Method C (Paste Text):** A master textarea that serves as the final source of truth. It is automatically populated by Method A or Method B, allowing the user to review or manually edit the text before proceeding.

**Settings & Progression:**
- Optional settings (Exam Type, State Focus) are saved to the global state.
- The "Continue" button validates that there is text present before advancing the user to Stage 2.

## Dummy Stages (2-8)
Stages 2 through 8 are currently implemented using a single `DummyScreen` placeholder component. The TopBar navigation allows jumping back to Stage 1, but progress is gated by `maxReachedScreen`.
