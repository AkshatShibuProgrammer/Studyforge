# StudyForge Architectural Analysis Summary

Based on a comprehensive review of the `architect guideline.txt`, the PDF Scratch Plan, the AI Lead/Sub-Lead implementation notes, and the existing skeleton HTML codes, here is the synthesized analysis to guide our implementation.

## 1. Project Goal & Constraints
- **Format**: A complete, monolithic Single-Page Application (SPA) contained entirely within one `.html` file.
- **Tech Stack**: React 18 (via Babel standalone), Tailwind CSS (via CDN), and Vanilla JS for utilities. No build step (Node.js/Webpack) is used.
- **AI Integration**: The app relies exclusively on the "Gemini Canvas Environment Hack" using the pre-built `geminiGenerateText`, `geminiSearchText`, and `geminiImageCreation` functions with a blank API key (`const apiKey = "";`).

## 2. The 8-Stage Pipeline
The core data flow of StudyForge transforms raw material into structured, visual study notes across 8 distinct screens:
1. **Input (Screen 1)**: Accepts a PDF/TXT file upload, manual text paste, or a typed Topic (which triggers AI auto-drafting). Includes optional settings (Exam Type, Target Audience, Language).
2. **Reading (Screen 2)**: Extracts text from files (or uses typed text). Handles PDF parsing if a PDF was uploaded.
3. **Understanding (Screen 3)**: An AI analysis phase. The model breaks the material into an overarching summary, detects key entities, and decides if it needs current affairs grounding.
4. **Parts (Screen 4)**: The material is logically divided into "Parts" (chapters/sections). Users can manually add, edit, or remove parts.
5. **Blueprints (Screen 5)**: AI generates a teaching strategy (blueprint) for each individual part.
6. **Blueprint Detail (Screen 6)**: The user can review, edit, or regenerate specific blueprints.
7. **Generation (Screen 7)**: The heavy lifting. AI generates the final detailed notes and triggers `imagen-4.0` for visual assets based on the blueprint.
8. **Export (Screen 8)**: The final document is presented as rich Markdown and can be downloaded.

## 3. Critical State Management & UI Architecture
- **Auto-Save**: A debounced auto-save function writes the massive React state object to `localStorage` every second. 
- **Lead AI Insight (Crucial)**: Base64 strings from Image generation are massive and will crash `localStorage` quota (typically 5MB). Images must be stripped from the auto-save payload before persisting.
- **Global Navigation**: A sticky `TopBar` indicates progress across the 8 stages (using circles/checkmarks). Users can navigate backward freely, but forward navigation is locked until a stage is complete.
- **Componentization**: Despite being a single file, the code must be strictly organized into logical sections: Constants -> Prompt Builders -> UI Components -> Screen Components -> Overlays -> Main App.

## 4. UI/UX Design System
- **Colors**: Blue-600 (`primary`), Gray-50/200 (`surface/border`), Green-500 (`success`), Amber-500 (`warning`).
- **Typography**: `Inter` font.
- **Micro-interactions**: Hover states on cards, pulse animations for loading spinners, and drag-and-drop feedback zones.
- **Skeletons**: The provided skeletons (`akshatpckskeleton.html`, etc.) show the desired clean, glassmorphic/modern Tailwind layouts that we must emulate when building the final views.

## Next Steps for Implementation
With this deep analysis consolidated, we have a clear blueprint of the exact state object, the 8-stage render loop, and the exact AI functions required. We are now fully prepared to begin coding the master HTML file.
