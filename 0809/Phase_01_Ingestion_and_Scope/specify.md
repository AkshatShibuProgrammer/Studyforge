# Functional Specification: Ingestion & Scope Expansion

## 1. Scope & Objective
Multi-format document upload (PDF/DOCX/TXT/MD), OCR image paste handler, dynamic subtopic expansion (AI-01A), and comprehensive source drafting (AI-01B).

## 2. Requirements & Acceptance Criteria
- **Architecture**: Must run 100% client-side inside `sindhuskeleton.html`.
- **Interface Contract**: Exposes clean functions on `window.app` or `window.StudyForge`.
- **Resilience**: Comprehensive try-catch wrapping with user-facing toasts on failure.

## 3. Submodule Specifications
### [Mod_01_Multi_Format_Upload_and_OCR](Mod_01_Multi_Format_Upload_and_OCR/specify.md)
File input handlers for PDF, Word, text, and clipboard screenshot OCR.

### [Mod_02_Dynamic_Scope_Expansion_AI01A](Mod_02_Dynamic_Scope_Expansion_AI01A/specify.md)
AI-01A subtopic generator with guaranteed, essential, optional, and current categorization.

### [Mod_03_Source_Drafting_AI01B](Mod_03_Source_Drafting_AI01B/specify.md)
AI-01B full study text drafting with live character counting flowing directly into Screen 3.

