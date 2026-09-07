# Phase 01: Ingestion, Scope & Multi-Method Input

## Executive Summary
Phase 01 establishes the universal input intake layer for StudyForge. It supports:
1. Method 1: Local document uploads (PDF via PDF.js, DOCX via Mammoth.js, TXT, Markdown, HTML, CSV) and clipboard/file image OCR.
2. Method 2: Concept-driven AI subtopic expansion (AI-01A) and textbook-grade source drafting (AI-01B).
3. Method 3: Direct semantic text pasting with live character tracking.

## Module Breakdown
- `Mod_01_Multi_Format_Upload_and_OCR`: Client-side parsing of binary documents and images.
- `Mod_02_Dynamic_Scope_Expansion_AI01A`: Dynamic subtopics list (up to 10) and structured proposal panel.
- `Mod_03_Source_Drafting_AI01B`: Comprehensive source drafting flowing to textarea and skipping Screen 2.
