# Master Gap & Defect Register: StudyForge 0809

## 1. Overview
This register documents every known defect, missing feature, and architectural inconsistency identified from **Document 5 (56 Missing Features / Agreed Amendments Register)**, the **Lead Questionnaire Decision Logs**, and our static code audit of `sindhuskeleton.html`. It maps each item to its precise resolving Phase and Module in the `0809` architecture.

---

## 2. Master Gap Resolution Matrix

| Gap ID | Description | Historical Origin | Resolving Phase & Module | Status |
|---|---|---|---|---|
| **GAP-01** | Truncated JSON syntax errors (`invalid_model_json`) on long prompts | Spec 021, Doc 4 | `Phase_00 / Mod_02_InBrowser_JSON_AutoRepair` | Specified |
| **GAP-02** | `localStorage` quota exceeded (~5MB) caused by raw Base64 image payloads | Doc 1, Audit | `Phase_00 / Mod_03_IndexedDB_Persistence_Engine` | Specified |
| **GAP-03** | Lack of automated fetch retry with backoff on network/rate glitches | Doc 4, §9 | `Phase_00 / Mod_01_Canvas_AI_Bridge` | Specified |
| **GAP-04** | Code duplication and monkey-patch fragility (12 appended `<script>` blocks) | Code Audit | `Phase_00 / Mod_01`, `Phase_10 / Mod_03` | Specified |
| **GAP-05** | Missing OCR / clipboard image paste support as an input source | Doc 5, #2F–2J | `Phase_01 / Mod_01_Multi_Format_Upload_and_OCR` | Specified |
| **GAP-06** | Dynamic subtopic inputs capped or not persisting on reload | Doc 5, #3 | `Phase_01 / Mod_02_Dynamic_Scope_Expansion_AI01A` | Specified |
| **GAP-07** | AI Draft does not bypass Screen 2 directly to Screen 3 | Doc 5, #7; Q2.2 | `Phase_01 / Mod_03_Source_Drafting_AI01B` | Specified |
| **GAP-08** | Incomplete extraction quality heuristics (missing replacement character count) | Doc 5, #9 | `Phase_02 / Mod_02_Quality_Heuristics_Diagnostics` | Specified |
| **GAP-09** | AI-02A and AI-02B prompt text simplified; missing unresolved-segments tracking | Doc 3, Doc 5 | `Phase_02 / Mod_03_AI_Cleanup_and_Restructure` | Specified |
| **GAP-10** | Subject and purpose headings hardcoded or static | Doc 5, #14 | `Phase_03 / Mod_01_Subject_and_Signal_Detection` | Specified |
| **GAP-11** | Granular entity extraction lacking stable IDs (`T-`, `D-`, `F-`, `PYQ-`) | Doc 3, Doc 5 | `Phase_03 / Mod_02_Deep_Core_Extraction_AI03B` | Specified |
| **GAP-12** | Feature bundles missing 3-tier visual hierarchy (Auto-on, Suggested, Not detected) | Doc 5, #18; Q3.2 | `Phase_03 / Mod_03_Smart_Bundle_Router` | Specified |
| **GAP-13** | "Fix manually" editor not persisting corrections or invalidating downstream work | Doc 5, #20 | `Phase_03 / Mod_04_Manual_Analysis_Correction` | Specified |
| **GAP-14** | Part splitting ignoring document density and strict page guardrails | Doc 5, #22; Q4.1 | `Phase_04 / Mod_01_AI_Part_Splitting_AI04` | Specified |
| **GAP-15** | Part merge operation stubbed or dropping applied bundle definitions | Doc 5, #24 | `Phase_04 / Mod_02_Part_Operations_Manager` | Specified |
| **GAP-16** | Blueprint generation lumped or missing 5-section schema | Doc 5, #27; Q5.2 | `Phase_05 / Mod_01_Five_Section_Blueprint_AI05` | Specified |
| **GAP-17** | Current Affairs search queries lumped into a single vague search string | Code Audit | `Phase_05 / Mod_01`, `Phase_07 / Mod_01` | Specified |
| **GAP-18** | Screen 6 Assistant chat faking responses; no real JSON patch operations | Doc 5, #31; Q5.5 | `Phase_06 / Mod_01_Surgical_AI_Chat_AI06A` | Specified |
| **GAP-19** | Missing isolated section-only regeneration (`AI-06B`) | Doc 3, Doc 5 | `Phase_06 / Mod_02_Targeted_Section_Regen` | Specified |
| **GAP-20** | **Critical**: Notes writer command `safe_content must be plain text only` stripping all rich formatting | Code Audit (L3653)| `Phase_07 / Mod_02_Master_Note_Writer_AI07A` | Specified |
| **GAP-21** | 22 Pedagogical Container CSS tokens defined but rendered as generic paragraphs | Code Audit (L3663)| `Phase_07 / Mod_04_Pedagogical_22_Container` | Specified |
| **GAP-22** | Decoupled Current Affairs dumped at the bottom instead of woven into notes | Code Audit | `Phase_07 / Mod_01_Dynamic_DualPass_CA_Engine` | Specified |
| **GAP-23** | Missing second-pass verification for dated claims and citation checks | User Request | `Phase_09 / Mod_02_Validator_Subagent_CA_Pass2` | Specified |
| **GAP-24** | Imagen visuals generating random art rather than educational schematics | Code Audit | `Phase_07 / Mod_03_Self_Explanatory_Visuals` | Specified |
| **GAP-25** | Visuals lack accompanying structured breakdown and component legends | User Request | `Phase_07 / Mod_03_Self_Explanatory_Visuals` | Specified |
| **GAP-26** | Absence of targeted competitive exam PYQ analysis (MPPSC, UPSC, State PSCs) | User Request | `Phase_08 / All Modules (PYQ Intelligence)` | Specified |
| **GAP-27** | Per-part validation popups offering generic text without one-click fixes | Doc 5, #44 | `Phase_09 / Mod_01_Per_Part_Actionable_Validator`| Specified |
| **GAP-28** | Accepted validation visual suggestions not translating to concrete image calls | Doc 5, #46; AI-07K| `Phase_09 / Mod_01_Per_Part_Actionable_Validator`| Specified |
| **GAP-29** | Export screen running AI calls or including unapproved/draft parts | Doc 5, #52; Q8.1 | `Phase_10 / Mod_01_Approved_Content_Compiler` | Specified |
| **GAP-30** | Export format missing clean Markdown file download | Doc 5, #54 | `Phase_10 / Mod_02_Multi_Format_Exporter` | Specified |

---

## 3. Verification & Elimination Protocol
Each Phase implementation MUST link its unit and integration verification directly to this register. A phase cannot be marked complete until all associated GAPs have verified tests demonstrating their full elimination in the Canvas environment.
