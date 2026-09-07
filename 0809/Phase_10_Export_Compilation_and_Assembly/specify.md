# Functional Specification: Deterministic Export & Assembly

## 1. Scope & Objective
Client-side export compiler generating standalone interactive HTML, clean GitHub-flavored Markdown, and printable paginated PDF.

## 2. Requirements & Acceptance Criteria
- **Architecture**: Must run 100% client-side inside `sindhuskeleton.html`.
- **Interface Contract**: Exposes clean functions on `window.app` or `window.StudyForge`.
- **Resilience**: Comprehensive try-catch wrapping with user-facing toasts on failure.

## 3. Submodule Specifications
### [Mod_01_Self_Contained_HTML_Compiler](Mod_01_Self_Contained_HTML_Compiler/specify.md)
Packages complete notes, embedded Base64 diagrams from ImageDB, and CSS into a single portable HTML document.

### [Mod_02_Markdown_and_Docx_Packager](Mod_02_Markdown_and_Docx_Packager/specify.md)
Generates clean, sanitized Markdown bundles with structured image references.

### [Mod_03_Print_Optimized_CSS_and_PDF_Engine](Mod_03_Print_Optimized_CSS_and_PDF_Engine/specify.md)
Applies `@media print` rules, page-break hygiene, and custom headers/footers for PDF generation.

