# StudyForge — Document 1: AI Usage Master Table

## Prompt-by-Prompt Operating Plan (Stages 1–8)

**Status:** Decision document based only on the agreed StudyForge discussions, skeleton, and supplied product plan.  
**Purpose:** Define every AI use case, the exact trigger, data it receives, how its prompt is assembled, what it returns, where the output is stored, and which next prompt uses it.

\---

## 1\. Governing Prompt Architecture

### 1.1 Core principle: store less; generate precise prompts from data

StudyForge must **not store a giant final prompt for every possible subject, topic, and part**. It stores only reusable prompt assets and builds the final prompt at runtime using the exact data for the current document/part.

|Asset type|Stored permanently in app code|Generated at runtime|Purpose|
|-|-|-|-|
|**System instruction**|Yes|No|Stable quality, safety, output-format, traceability, and education rules. Read-only to users.|
|**Prompt template**|Yes|No|Reusable task wording with placeholders such as `{{SOURCE\_SLICE}}`, `{{PART\_BLUEPRINT}}`, `{{TOPIC}}`.|
|**Prompt-generation rules**|Yes|No|Defines which template to choose, which data to inject, grounding setting, token limits, and response schema.|
|**Final execution prompt**|No|Yes|The completed system + task prompt after the current document data is injected. This is what is sent to AI and shown to users.|
|**Prompt output**|No|Yes|JSON/HTML/text returned by AI. Saved in session state and becomes input to later prompts.|

### 1.2 Storage and visibility decisions

|Item|Agreed implementation|
|-|-|
|Stored prompt location|`DEFAULT\_PROMPTS` and prompt-generation rules as JavaScript constants inside the unified HTML application.|
|Subject routing|`SUBJECT\_PROMPT\_MAP` selects relevant subject strategy where applicable. Subject strategy is guidance, not a rigid restriction; cross-domain topics such as GST must still cover economics, polity, history, etc.|
|End-user editing|Users **cannot edit base templates/system instructions**. They can view, copy, and edit the **final generated prompt** for a particular operation, then regenerate.|
|Prompt viewer|Every AI operation must provide a visible, copyable final prompt. Default view shows task/user prompt; **Show System Instructions** reveals system instructions.|
|Prompt regeneration|Normal regenerate = same prompt + “produce a different variation” + optional user creative direction. Edited regenerate = system prompt + edited final prompt + AI-generated/derived change context.|

### 1.3 Common data objects referenced below

|Data object|Created by|Used by|
|-|-|-|
|`inputProfile`|Screen 1|Method 2, reading, analysis, blueprint, export metadata|
|`sourceDocument`|Screen 1/2|Stage 3 analysis, Stage 4 splitting, Stage 7 text generation|
|`sourceSlices`|Stage 2 / chunker|Stage 3 chunk analysis and Stage 7 per-part generation|
|`subjectSignals`|AI-03A|AI-03B, AI-03C, feature UI, routing|
|`deepAnalysis`|AI-03B|splitting, blueprints, generation, validation|
|`bundleAnalysis`|AI-03C / AI-03D|Screen 3 selections, Stage 4 per-part routing, blueprint, generation|
|`partPlan\[]`|AI-04|Screen 4/5/6/7; contains page range, topics, applied bundles|
|`blueprint\[]`|AI-05|Screen 5/6/7; contains headings, text plan, image plan, CA plan, validation plan|
|`generatedPart\[]`|AI-07A and related calls|validation, approval, final formatted document|
|`imageAssets\[]`|AI-07B/AI-07C and visualisation flow|generated part, validation, export|
|`currentAffairsResults\[]`|AI-07D|generated part, validation, export|
|`approvalState`|user actions + validation|final validation and export|

\---

## 2\. Master AI Call Inventory

> \*\*Trigger definitions:\*\*  
> \*\*Always\*\* = automatically runs whenever the relevant flow is entered.  
> \*\*Conditional\*\* = runs only when data/state requires it.  
> \*\*User-triggered\*\* = runs only after explicit user action.  
> \*\*Chained\*\* = another AI/function call invokes it automatically after its prerequisite completes.

|ID|Stage / Screen|AI operation|Trigger|Primary final-prompt inputs|Output|Direct next consumer|
|-|-|-|-|-|-|-|
|AI-01A|1 — Method 2|Expand related sub-topics|Always when Method 2 is used|Topic, user sub-topics, desired depth, exam context, internet toggle|Suggested/optional sub-topic list with reasons|User approval → AI-01B|
|AI-01B|1 — Method 2|Draft full source material|Always after approved sub-topics|Topic, approved sub-topics, depth, current-affairs toggle, search toggle|Full editable study material|Method 3 paste area → Stage 3|
|AI-02A|2 — Reading|AI cleanup fallback|Conditional: technical extraction fails|Extracted text, extraction errors, source type|Cleaned text with retained page mapping|AI-02B only if cleanup inadequate; otherwise Stage 3|
|AI-02B|2 — Reading|AI restructuring fallback|Conditional: AI cleanup fails/is inadequate|Raw extraction, cleanup result/errors, page boundaries|Structured readable source sections|Stage 3|
|AI-03A|3 — Understanding|Subject and signal detection|Always|Source text/chunks, input profile, page map|Subject, sub-discipline, content signals, signal evidence|AI-03B and bundle router|
|AI-03B|3 — Understanding|Deep element extraction|Always after AI-03A|Subject signals, source text/chunks, page map|Topics, definitions, formulas, PYQs, comparisons, examples, timelines, tables, refs|AI-03C, AI-04, AI-07A|
|AI-03C|3 — Understanding|Smart bundle analysis|Always, but only for routed relevant bundles|Subject signals, deep extraction, relevant source sections, enabled global preferences|Detected bundles/features, evidence, confidence tier|Screen 3 UI; AI-04 / AI-05|
|AI-03D|3 — Understanding|On-demand force-enabled bundle analysis|User-triggered|User-selected bundle, source text/chunks, subject signals, deep extraction|Bundle-specific features and evidence|Updates Screen 3 selections; later AI-04/AI-05|
|AI-04|4 — Parts|Coherent part splitting + bundle assignment|Always upon entering/creating Screen 4|Deep analysis, bundle selections, page rules, raw text if small or topic summaries if large|Proposed parts, ranges, topics, rationale, per-part bundles|Screen 4 → AI-05|
|AI-05|5 — Blueprint cards|Per-part blueprint generation|Always after parts confirmed; one call per part with 1-second stagger|Specific part plan, relevant source slice, all definitions/formulas, applicable bundle data|Headings, text plan, image plan, CA plan, validation plan|Screen 5/6 → AI-07A/07D|
|AI-06A|6 — Blueprint detail|Surgical blueprint chat modification|User-triggered|User instruction, target blueprint section, current blueprint, part metadata|Targeted JSON patch + explanation|Updated blueprint; may alter AI-07 inputs|
|AI-06B|6 — Blueprint detail|Regenerate one blueprint section|User-triggered|Current blueprint, locked sections, requested section, user direction|Replacement of requested section only|Updated blueprint|
|AI-07A|7 — Generation|Per-part text/HTML generation|User-triggered per part; chained for Auto-Generate All|Part metadata, source slice, part analysis, **all definitions/formulas**, blueprint, bundles, selected CA data if ready|Structured HTML/content blocks, traceability tags, image-needed markers|Render part; may invoke AI-07B/07C|
|AI-07B|7 — Generation|Image prompt expansion|Chained whenever an approved image request exists|Image-plan item or image-needed marker, adjacent content, style choice, user direction|Detailed image-generation prompt and placement metadata|AI-07C|
|AI-07C|7 — Generation|Educational image generation|Chained after AI-07B|Expanded image prompt|Image asset|Insert image at defined HTML location; validation/export|
|AI-07D|7 — Generation|Current-affairs grounded research|User-triggered by Fetch CA; chained in Auto-Generate|CA query plan, part topic, time context, grounding enabled|Current facts, URLs, dates, source metadata|AI-07A or CA container insertion|
|AI-07E|7 — Generation|Post-text image gap review|Conditional after text generation / review|Generated part HTML, blueprint image plan, part metadata|Missing-image suggestions with exact insertion anchors|Shared image insertion chain → AI-07B/07C|
|AI-07F|7 — Generation|Highlight-to-visualize prompt design|User-triggered|Selected text, surrounding paragraph(s), part metadata, chosen/user-requested style|Expanded prompt + 3 recommended styles/reasons|User selects style → AI-07C|
|AI-07G|7 — Generation|Scope-aware refinement|User-triggered|User request, current generated HTML, selected text if any, part metadata, manual-edit markers|Proposed targeted patch + diff + detected scope|User applies → rendered HTML updates|
|AI-07H|7 — Approval|Per-part validation|Chained when user clicks Approve Part|Generated text, images + descriptions, source slice, blueprint, CA, traceability metadata|Summary, issues, suggestions, proposed modifications|User approve/ignore/cancel; modifications may invoke generation/image chain|
|AI-07I|7 — Approval|Final consolidated validation|Always after all remaining parts approved|Consolidated approved document, all part blueprints, coverage/bundle map, traceability data|Strengths, content-driven gaps, suggested parts/sections|User skip/apply/review; accepted additions → AI-07J|
|AI-07J|7 — Add part|Quick blueprint for added/suggested part|User-triggered (manual Add Part) or chained after final-validation suggestion accepted|New topic/subtopics, global bundles, CA setting, parent document context|New part plan + quick blueprint|User configures or generates → AI-07A|
|AI-07K|7 — Validation image gap|Image proposal during validation|Conditional when AI-07H finds visual gap|Validation issue, generated HTML, insertion location, relevant content|Image request/placement|Shared image insertion chain → AI-07B/07C|
|AI-08|8 — Export|None|None|Approved embedded content only|No AI output|Browser formatting, Copy formatted content, Save PDF|

\---

# 3\. Detailed Stage Tables

## Stage 1 — Input (Screen 1)

### AI-01A — Related Sub-topic Expansion

|Field|Detailed decision|
|-|-|
|**Purpose**|Turn a user-entered topic and initial sub-topics into a complete, exam/use-case appropriate scope before source material is drafted.|
|**Trigger**|**Always** when the user chooses Method 2 and clicks **AI Draft Text for This Topic**.|
|**Prompt is created by**|Prompt Builder using `subtopicExpansionTemplate` + `inputProfile` + optional grounding flag.|
|**Stored prompt assets used**|Universal educational system instruction; sub-topic expansion template; prompt-generation rule for selected depth and internet mode.|
|**Runtime data injected**|`topic`; user-entered `subtopics\[]`; exam/context (if selected); depth = **medium by default** or comprehensive; user language/format preference if present; internet/current-affairs toggles.|
|**Grounding/search**|**OFF** normally. **ON** only when user enabled internet search/current information for Method 2. Search instruction appears in this prompt and AI-01B.|
|**Final prompt must ask AI to**|Preserve every user sub-topic as guaranteed; identify essential related sub-topics; separate essential vs optional additions; include current/developing sub-topics only when internet/current mode is enabled; provide concise reasons.|
|**Output schema**|`{guaranteed\_topics:\[], suggested\_essential:\[], suggested\_optional:\[], current\_topics:\[], reasons:{topic: reason}, scope\_notes:\[]}`|
|**User interaction**|User sees suggested list, can check/uncheck each, add up to the allowed number of their own sub-topics, then clicks **Approve \& Generate**.|
|**Saved state**|`inputProfile.approvedSubtopics`; `promptHistory.AI-01A`; `aiOutputs.subtopicExpansion`.|
|**What happens next**|The approved list is injected into AI-01B. No content generation occurs until user approves the scope.|
|**Failure handling**|Show editable final prompt with Retry As-Is / Retry Simplified / Retry with Edited Prompt / Skip / Cancel. If skipped, user may write sub-topics manually and continue.|

### AI-01B — Full Study-Material Draft Generation

|Field|Detailed decision|
|-|-|
|**Purpose**|Create editable, full study-material-style source content, which then enters the normal pipeline as pasted text.|
|**Trigger**|**Always**, after user approves the expanded sub-topic list.|
|**Prompt is created by**|Prompt Builder using `draftSourceMaterialTemplate` and data approved after AI-01A.|
|**Runtime data injected**|Topic; approved/guaranteed sub-topics; depth (medium default or comprehensive); intended exam/context; current-affairs toggle; internet-search toggle; any user guidance.|
|**Grounding/search**|ON only if user enabled internet search/current mode. If ON, prompt requires web-derived facts to retain URL/date metadata for later `WEB\_SOURCED` tagging.|
|**Final prompt must ask AI to**|Produce complete, source-like study material; use headings and logical flow; cover all approved sub-topics; add relevant related explanations; include current facts only when enabled; avoid pretending web facts are source-backed; preserve citations/URLs where grounding supplies them.|
|**Output format**|Editable structured text/HTML-safe text plus metadata: `{content, headings, web\_sources\[], current\_fact\_markers\[]}`. It is not yet final Screen 7 formatted notes.|
|**User interaction**|Result is inserted into **Method 3 paste area**. User may edit, remove, or extend it before Continue.|
|**Saved state**|`sourceDocument.text`; origin = `ai\_draft`; source metadata and web source references; final prompt in prompt history.|
|**What happens next**|Stage 2 is skipped for AI-drafted text. It goes directly to AI-03A when user continues.|

### Stage 1 non-AI behavior that affects prompt flow

|Path|Behavior|AI consequence|
|-|-|-|
|File upload|User uploads PDF/TXT/DOCX/HTML/MD/JPG/PNG etc.|Stage 2 technical extraction runs first; AI only appears if extraction needs fallback.|
|Pasted text|Taken as-is.|No cleanup prompt automatically; it goes to AI-03A after user continues.|
|AI-drafted text|User edits in paste area.|Stage 2 skipped; AI-03A uses final edited text, not only original AI-01B output.|

\---

## Stage 2 — Reading / Source Preparation (Screen 2)

### AI-02A — AI Cleanup Fallback

|Field|Detailed decision|
|-|-|
|**Purpose**|Repair text where technical extraction produced garbling, broken sentences, encoding issues, or unusable layout.|
|**Trigger**|**Conditional.** Technical extraction is always attempted first. This call triggers automatically only if quality checks fail. User can also manually choose extraction method B.|
|**Prompt is created by**|`extractionCleanupTemplate` + extraction diagnostics + raw extracted text.|
|**Runtime data injected**|Source type; raw extraction; page/paragraph boundaries; detected errors; preservation requirements; file origin.|
|**Grounding/search**|OFF.|
|**Final prompt must ask AI to**|Correct encoding/spacing/broken lines; retain factual wording; retain page mapping wherever possible; not add missing knowledge; report uncertain sections instead of inventing text.|
|**Output schema**|`{clean\_text, page\_map, unresolved\_segments\[], quality\_status, cleanup\_log\[]}`|
|**Saved state**|Updated `sourceDocument`; cleanup diagnostics; final prompt/output history.|
|**What happens next**|If quality is acceptable → AI-03A. If not → AI-02B.|

### AI-02B — AI Source Restructuring Fallback

|Field|Detailed decision|
|-|-|
|**Purpose**|Make a severely damaged, scanned, or poorly extracted source readable and structurally usable when cleanup alone is insufficient.|
|**Trigger**|**Conditional.** Triggered after AI-02A remains inadequate or user explicitly selects method C.|
|**Prompt is created by**|`sourceRestructureTemplate` + raw extraction/cleanup output + page boundaries.|
|**Runtime data injected**|Raw/cleaned text; extraction issues; page map; document type; instruction to preserve uncertain/illegible areas.|
|**Grounding/search**|OFF.|
|**Final prompt must ask AI to**|Reconstruct headings/sections/lists where supported by the source; preserve page association; mark uncertain reconstructions; do not enrich with outside facts.|
|**Output schema**|`{structured\_text, sections:\[{id,title,page\_range,text}], unresolved\_segments\[], reconstruction\_notes\[]}`|
|**What happens next**|`sourceDocument` becomes the source for AI-03A.|

### Large-source/chunking rule (applies before AI-03A / AI-03B)

|Rule|Implementation|
|-|-|
|Trigger threshold|If source tokens exceed \~80% of the selected model context limit.|
|Semantic split priority|Chapter heading → section heading → page boundary → paragraph group.|
|Per-chunk continuity inputs|`chunk\_id`, section boundaries, previous chunk summary, next chunk preview.|
|Merge behavior|Union topics; deduplicate definitions/formulas by content; concatenate/deduplicate PYQs; preserve page refs.|
|User notice|Warn only when a very large section had to be split at paragraph level: “analysis may have reduced granularity.”|

\---

## Stage 3 — Understanding and Feature Detection (Screen 3)

### AI-03A — Subject and Signal Detection

|Field|Detailed decision|
|-|-|
|**Purpose**|Determine what the content is about and detect broad signals that route only relevant deep/bundle analysis.|
|**Trigger**|**Always** whenever any final source reaches Screen 3. Per chunk if semantic chunking is active, then merged.|
|**Prompt is created by**|`subjectSignalTemplate` + source text/chunks + page map.|
|**Runtime data injected**|Source text or semantic chunks; source origin; user exam/context if provided; page refs.|
|**Grounding/search**|OFF. It must analyze the submitted source, not web knowledge.|
|**Final prompt must ask AI to**|Return primary subject, sub-discipline, and evidence-based signals: formulas, dates, code, locations, persons, legal references, diagrams, charts/data, institutions/administration, processes/creation, medical/scientific content, etc. It must provide evidence references, not unsupported confidence percentages for UI.|
|**Output schema**|`{primary\_subject, sub\_discipline, secondary\_domains\[], signals:{signal:{strength,evidence\[],page\_refs\[]}}, routing\_hints\[]}`|
|**UI treatment**|Strength becomes visual confidence only: 🟢 strong/auto-on, 🟡 weak/suggested, ⚪ not detected/force-enable. Do **not** show percentages. Hover reveals detected evidence.|
|**What creates next prompts**|Rule-based router maps `signals` to relevant bundle prompts for AI-03C. The subject/sub-discipline and page map are injected into AI-03B.|

### AI-03B — Deep Core Extraction

|Field|Detailed decision|
|-|-|
|**Purpose**|Extract the reusable, structured knowledge layer that drives splitting, blueprints, source-backed writing, and cross-part references.|
|**Trigger**|**Always** immediately after AI-03A. Per chunk if needed, followed by structured merge.|
|**Prompt is created by**|`deepExtractionTemplate` + subject/sub-discipline from AI-03A + source text/chunks.|
|**Runtime data injected**|`subjectSignals`; source content; page references; chunk continuity info; output ID rules.|
|**Grounding/search**|OFF.|
|**Final prompt must ask AI to extract**|Topics with page refs; definitions with stable IDs; formulas and variable definitions with stable IDs; PYQs with year/type; comparisons; examples; timelines; tables; diagrams/visual candidates. It should record source references and avoid external enrichment.|
|**Output schema**|`{topics\[], definitions:\[D-\*], formulas:\[F-\*], pyqs\[], comparisons\[], examples\[], timelines\[], tables\[], diagrams\[], source\_coverage\[]}`|
|**Saved state**|`deepAnalysis`; each item keeps source page/chunk reference.|
|**What creates next prompts**|AI-03C receives the signals plus relevant deep-analysis elements. AI-04 uses all merged deep analysis. AI-07A receives part-relevant elements plus all definitions/formulas.|

### AI-03C — Smart Routed Bundle Analysis

|Field|Detailed decision|
|-|-|
|**Purpose**|Detect only the advanced study features that are truly relevant to this content, without sending every possible bundle for every document.|
|**Trigger**|**Always after AI-03A/03B**, but its scope is conditional: only bundles selected by deterministic signal→bundle routing run. MVP may combine the relevant bundles in one prompt; future version can split them into parallel focused bundle calls if quality requires.|
|**Prompt is created by**|Bundle router selects relevant instructions from `bundleTemplates`; Prompt Builder combines them with evidence and deep analysis.|
|**Runtime data injected**|Signals/evidence from AI-03A; core extraction from AI-03B; relevant source snippets/page refs; user global settings; bundle definitions.|
|**Grounding/search**|OFF.|
|**Final prompt must ask AI to**|Identify applicable bundle features with evidence and tier: auto-enabled (strong), suggested (medium), or not detected. It must not fabricate a feature only because it exists in the catalog.|
|**Output schema**|`{bundles:\[{bundle\_id, state:auto\_on|
|**User interaction**|Screen 3 displays auto-on features, visible suggested features, and hidden/expandable force-enable features. Continue remains available; no blocking approval gate.|
|**What happens next**|User’s final global bundle choices are merged with this output and feed AI-04 and AI-05.|

### AI-03D — Force-Enabled Bundle Analysis

|Field|Detailed decision|
|-|-|
|**Purpose**|Analyze an initially undetected bundle only when the user requests it.|
|**Trigger**|**User-triggered** when user enables a grey/hidden bundle or specific unavailable feature via **Show more options**.|
|**Prompt is created by**|`bundleTemplates\[chosenBundle]` + source/deep-analysis data.|
|**Runtime data injected**|Chosen bundle/feature; source text or relevant chunks; subject signals; deep analysis; user reason if entered.|
|**Grounding/search**|OFF.|
|**Output schema**|Same as selected bundle segment of AI-03C, with state/rationale.|
|**What happens next**|Updates global bundle selection and becomes available for per-part assignment by AI-04.|

### Deferred deep bundles: what Screen 3 detects vs what Screen 7 fetches

|Content found in Screen 3|Screen 3 stores|Stage 7 deep prompt behavior|
|-|-|-|
|Location|Names, page refs, frequency, local context/evidence|Fetch **context-specific** facts only for the generating part. History → historical/archaeological relevance; geopolitics → borders/security; economics → GSDP/industries; CA → current facts. Do not add generic unrelated trivia.|
|Country in relevant context|Name and source context|If needed, generate map-oriented learning content: neighbors, capitals, significant seas/passages, but only where relevant to the part/topic.|
|Person/personality|Name, role/context, page refs|Fetch PSC-relevant contribution/facts and relevant current affairs only during that part’s generation.|
|Formula|Formula, variables, source ref, brief purpose|During generation, produce derivation, variable deep dive, examples/substitution, relationships, applications, edge cases, common mistakes as allowed by the applied formula bundle.|

\---

## Stage 4 — Parts / Coherent Segmentation (Screen 4)

### AI-04 — Part Splitting and Per-Part Bundle Assignment

|Field|Detailed decision|
|-|-|
|**Purpose**|Convert the full analysis into logically teachable parts while preserving conceptual coherence and selecting only relevant bundles for each part.|
|**Trigger**|**Always** when Screen 4 is created/re-created after Stage 3 is ready.|
|**Prompt is created by**|`partSplittingTemplate` + page-count guardrails + deep analysis + selected global bundles.|
|**Runtime data injected**|Merged `deepAnalysis`; global bundle selections; total pages/length; source text if within safe token size, otherwise topic-level summaries; page-count range; source page map.|
|**Grounding/search**|OFF.|
|**Required splitting rules**|Use page count only as a guardrail; keep related topics together; never split formula from explanation; keep PYQs with the topic they test; avoid tiny 1–2 paragraph parts; may exceed recommended range only with explicit UI warning.|
|**Final prompt must ask AI to return**|Proposed part count; part title; page range/source sections; topics; reason; estimated density; applied bundle IDs; references to definitions/formulas/PYQs; warnings if outside guardrail.|
|**Output schema**|`{recommended\_range, proposed\_count, out\_of\_range\_warning, parts:\[{part\_id,title,page\_range,topics\[],analysis\_refs\[],applied\_bundles\[],rationale}]}`|
|**User interaction**|User can edit title/settings, add, remove, merge, or adjust parts. Global enabled bundles are inherited only into parts where content supports them. User may override per part.|
|**Prompt visibility**|Screen 4 must show the actual splitting prompt and factors used in a copyable viewer.|
|**What happens next**|Confirmed/edited `partPlan\[]` triggers AI-05 for every current part. If a part is manually added, it must retain/inherit bundle data rather than dropping it.|

\---

## Stage 5 — Blueprint Card Grid (Screen 5)

### AI-05 — Blueprint Generation per Part

|Field|Detailed decision|
|-|-|
|**Purpose**|Build one complete, coherent execution blueprint for every part before notes, images, or CA are generated.|
|**Trigger**|**Always** after parts are confirmed. One call per part, started in parallel with approximately a one-second gap to reduce rate-limit risk.|
|**Prompt is created by**|`universalBlueprintHeader` + selected subject strategy + `blueprintTemplate` + part-specific data.|
|**Runtime data injected**|Current part metadata; part source slice; part-specific deep analysis; **all document definitions and all document formulas**; applied bundles; global options; any user part edits.|
|**Grounding/search**|OFF. Blueprint creates CA query plans but does not execute live search.|
|**Final prompt must ask AI to create all five sections together**|1) headings; 2) text plan; 3) image plan; 4) CA plan/search queries; 5) validation plan. The plans must be mutually consistent.|
|**Image-plan rules**|AI selects count and recommended style based on teaching need; defaults prioritize understanding over appearance. It should try to combine related visual information into one clear composite/infographic; it may propose multiple images if a single visual would become cluttered. Each item includes `style\_recommended`, `style\_reasoning`, content, learning objective, and placement.|
|**CA-plan rules**|Return editable query strings only. Do not fetch results now because CA must be fresh when generation occurs.|
|**Output schema**|`{part\_id, headings\[], text\_plan\[], image\_plan\[], ca\_plan:{queries\[]}, validation\_plan\[], applied\_bundles\[], source\_scope}`|
|**Saved state**|`blueprint\[partId]`; final prompt stored under the part’s prompt history.|
|**User interaction**|Screen 5 card shows summary, bundle icons, and View AI Prompt. User can open Screen 6 to edit.|
|**What happens next**|Approved blueprint drives AI-07A text generation, AI-07B image expansion, AI-07D CA research, and AI-07H validation.|

\---

## Stage 6 — Blueprint Detail and AI Chat (Screen 6 overlay)

### AI-06A — Surgical Blueprint Chat Modification

|Field|Detailed decision|
|-|-|
|**Purpose**|Let user ask natural-language changes such as “add more formulas” or “make the Shyam comic a flowchart” without regenerating unrelated blueprint sections.|
|**Trigger**|**User-triggered** by a chat instruction in the Screen 6 overlay.|
|**Prompt is created by**|`blueprintPartRefinementPrompt` + current blueprint + targeted scope determined from user instruction.|
|**Runtime data injected**|User message; full current blueprint; part metadata; applied bundles; source/analysis references needed for the target; most recent modification info for undo.|
|**Grounding/search**|OFF.|
|**Scope rule**|AI identifies affected blueprint section(s). “Add more formulas” modifies Text Plan formula containers; “change comic to flowchart” modifies the relevant Image Plan item. Unrelated sections remain untouched.|
|**Output schema**|`{detected\_scope, patch\_operations\[], updated\_sections, explanation, undo\_payload}`|
|**User interaction**|Patch is applied directly and affected UI is subtly highlighted. A lightweight **Undo last change** is available. This is not a complete version-history feature.|
|**What happens next**|Updated blueprint becomes the only blueprint used by future generation calls.|

### AI-06B — Regenerate One Blueprint Section

|Field|Detailed decision|
|-|-|
|**Purpose**|Recreate only one planned section, such as Image Plan, while preserving locked/current sections.|
|**Trigger**|**User-triggered** via e.g. **Regenerate Image Plan Only**.|
|**Prompt is created by**|Section regeneration template + current blueprint.|
|**Runtime data injected**|Target section; current headings/text plan; relevant source and analysis; user direction; locked sections.|
|**Output schema**|`{target\_section, replacement\_content, compatibility\_notes}`|
|**What happens next**|Replaces only the requested blueprint section.|

\---

## Stage 7 — Write, Generate, Refine, Approve (Screen 7)

### AI-07A — Per-Part Notes / Structured HTML Generation

|Field|Detailed decision|
|-|-|
|**Purpose**|Generate comprehensive, source-aware, properly formatted study notes for one specific part.|
|**Trigger**|**User-triggered** by Generate Part, or automatically chained for each selected part when user chooses Auto-Generate Part/All.|
|**Prompt is created by**|`partWriterPrompt` + optional subject strategy + `buildPartGenerationContext()` rule.|
|**Runtime data injected**|Part title/range/topics; relevant source slice only; part-specific extraction (topics/PYQs/examples/etc.); **all definitions and all formulas for whole document**; part blueprint; applied bundles; optional completed CA output; location/personality/formula deep-request rules; user writing preference.|
|**Grounding/search**|OFF. Source-based generation must not silently mix web facts into SOURCE\_BACKED material.|
|**Traceability rules**|Mark every content block as `SOURCE\_BACKED` (with source page where possible), `RESEARCH\_REQUIRED` (AI inference/verification needed), or `OPTIONAL\_ENRICHMENT` (analogy/clarifying addition). `WEB\_SOURCED` is used only for live-grounded results arriving through AI-07D/Method 2 web mode.|
|**Deferred deep-fact behavior**|For relevant applied bundles, the generation context/request includes context-specific location facts, PSC-relevant personality facts, formula operations, etc. Cache by **entity + context**, e.g. `location\_facts\_MP\_indus\_valley`, not merely location name.|
|**Final prompt must request**|Structured, sanitizable HTML/content blocks with IDs/anchors, container types, traceability metadata, source refs, and zero or more `image\_needed` markers that specify description and insertion anchor.|
|**Output schema**|`{part\_id, html\_blocks\[], containers\[], citations\[], traceability\[], image\_needed:\[{description,after\_anchor,learning\_goal,style\_hint}], generation\_summary}`|
|**Rendering rule**|The app sanitizes returned content and renders through approved container templates; raw unsanitized AI HTML must never be injected directly.|
|**What happens next**|Rendered text is placed into the part. Any `image\_needed` item invokes the shared image insertion chain (AI-07B → AI-07C). CA results are inserted when available.|

### Shared Dynamic Image Insertion Chain

This function chain is used when an image is planned in the blueprint, requested by generated text, discovered after text review, or suggested in validation.

|Step|Function / AI responsibility|Input|Output|
|-|-|-|-|
|1|Trigger source|Blueprint / text generator / post-review / validation|`{description, content\_anchor, style\_hint, learning\_goal}`|
|2|`insertImageAtLocation()`|Requested anchor and content|Ensures target text/container exists and reserves a safe image slot in HTML state|
|3|AI-07B prompt builder|Image description, nearby content, part topic, selected/recommended style, user direction|Detailed image generation prompt + layout/placement metadata|
|4|AI-07C image generator|Detailed prompt|Image asset|
|5|Renderer|Image asset + reserved slot|Image is inserted after/at specified text anchor and saved to `imageAssets\[]`|

### AI-07B — Detailed Image Prompt Expansion

|Field|Detailed decision|
|-|-|
|**Purpose**|Convert a brief image plan/request into a precise educational image-generation prompt.|
|**Trigger**|**Chained** whenever a planned/dynamic/validation/visualize image request is accepted for generation.|
|**Prompt is created by**|`imagePromptBuilder` + teaching-first visual rules + selected input data.|
|**Runtime data injected**|Image description; related text; part subject/topic; image placement; recommended/chosen style; user direction; mixed-style requirement if applicable.|
|**Grounding/search**|OFF.|
|**Mandatory visual principles**|Understanding over beauty; explain difficult concepts visually; prefer infographics, comics for narratives, formula/metric visualisations, comparison matrices, flowcharts, timelines as appropriate; be creative but do not make visuals decorative only.|
|**Mixed-style rule**|AI tries to create one understandable composite when data/metrics/process/categories belong together. It may return more than one image request only when one visual would be too cluttered.|
|**Output schema**|`{expanded\_prompt, title, style\_recommended, style\_reasoning, layout\_plan, placement\_anchor, images\_needed, split\_reason?}`|
|**User interaction**|Default is generate immediately. User can Show Prompt, edit and regenerate, request Different Style, or enable Screen 1 global “Preview image prompts before generation” to approve prompt before creating image.|

### AI-07C — Image Generation

|Field|Detailed decision|
|-|-|
|**Purpose**|Generate the actual educational visual from AI-07B’s detailed prompt.|
|**Trigger**|**Chained** after AI-07B; user may also trigger after editing the final image prompt.|
|**Prompt input**|Expanded image prompt; image generation settings; no unrelated full document context.|
|**Output**|Image asset + stored final prompt + title/alt/description metadata.|
|**Regeneration rule**|Default retry/regenerate adds “create a clearly different variation” and optional user direction such as comprehensive, artistic, simpler, etc. Edited regeneration preserves system principles and includes an explanation/diff of user changes.|
|**What happens next**|Image is placed at the selected HTML anchor. It becomes included in part validation and export.|

### AI-07D — Grounded Current-Affairs Research

|Field|Detailed decision|
|-|-|
|**Purpose**|Fetch fresh, topic-specific current affairs only at the point they are needed.|
|**Trigger**|**User-triggered** by Fetch CA for a part; **chained** when user chooses Auto-Generate Part/All and CA is enabled/applies.|
|**Prompt is created by**|`currentAffairsPrompt` + editable query generated in the blueprint + part context.|
|**Runtime data injected**|CA query string; part topic; subtopics; time relevance; user/global CA selection; source/context boundaries.|
|**Grounding/search**|**ON.** Gemini native grounding/search is primary. If unavailable, use model knowledge with a visible freshness disclaimer.|
|**Final prompt must ask AI to return**|Current relevant facts, dates, why it matters to the topic/exam, source URLs, and no unsupported claims.|
|**Output schema**|`{query, results:\[{fact,date,context,url,publisher}], fetched\_at, grounding\_status, disclaimer?}`|
|**Tagging**|Inserted facts use `WEB\_SOURCED: url` (purple visual treatment) with clickable citation. Never label grounded content SOURCE\_BACKED.|
|**What happens next**|Results can be added to the generated part’s CA container or fed into a re-generation/update request if the text needs integration.|

### AI-07E — Post-Generation Image Gap Review

|Field|Detailed decision|
|-|-|
|**Purpose**|Discover visuals that would improve understanding but were not anticipated in the initial image plan.|
|**Trigger**|**Conditional** after text generation/review when enabled by the generation flow. This is one of the agreed three moments where image needs can be found.|
|**Runtime data injected**|Rendered part HTML; existing image plan; heading/anchor map; applied bundles.|
|**Grounding/search**|OFF.|
|**Output schema**|`{missing\_images:\[{description, insert\_at, style\_hint, reason, priority}]}`|
|**What happens next**|Each accepted suggestion uses shared image insertion chain AI-07B → AI-07C.|

### AI-07F — Highlight-to-Visualize Prompt Design

|Field|Detailed decision|
|-|-|
|**Purpose**|Turn a user-highlighted explanation into a suitable visual on demand.|
|**Trigger**|**User-triggered** when user highlights text and clicks **Visualize This**.|
|**Prompt is created by**|`highlightVisualizeTemplate` + selection context collector.|
|**Runtime data injected**|Selected text; parent/surrounding paragraph; if multi-paragraph, first paragraph before and last after; part metadata; applied bundles; subject; user direction.|
|**Grounding/search**|OFF.|
|**Final prompt must ask AI to return**|One detailed prompt plus three recommended styles from the 35-style catalog and a reason for each.|
|**Output schema**|`{expanded\_prompt, recommended\_styles:\[{style,reason}], placement\_anchor}`|
|**Duplicate rule**|Do **not** block or warn for potentially duplicate images; user may intentionally want a second perspective.|
|**What happens next**|User selects/edits style/prompt; AI-07C generates and inserts visual.|

### AI-07G — Scope-Aware Content Refinement

|Field|Detailed decision|
|-|-|
|**Purpose**|Apply natural-language refinements while protecting manual edits outside the relevant scope.|
|**Trigger**|**User-triggered** from part refinement chat.|
|**Prompt is created by**|`refinementPrompt` + scope detector + diff builder.|
|**Runtime data injected**|User request; part HTML/container map; selected content if any; blueprint; part metadata; manual-edit indicators.|
|**Grounding/search**|OFF.|
|**Scope rule**|AI infers target scope. “Formula explanation” targets formula containers. “Whole/entire/everything” triggers proposed full-part regeneration and a warning that manual edits may be lost.|
|**Output schema**|`{scope, proposed\_edits:\[{anchor,before,after}], diff\_summary, full\_regeneration\_required, warning?}`|
|**User interaction**|Show diff before applying: Apply All / Apply Selective / Discard / Expand Scope to Whole Part.|
|**What happens next**|Selected patches modify HTML state. If an accepted patch calls for image change, shared image insertion/replacement flow runs.|

### AI-07H — Per-Part Validation on Approval

|Field|Detailed decision|
|-|-|
|**Purpose**|Validate one complete part before it becomes approved: summarize its content/assets and identify actionable gaps.|
|**Trigger**|**Chained** automatically when user clicks **Approve Part**. Approval is not completed until user chooses a validation outcome.|
|**Number of AI calls**|**One combined call**, not three. It returns summary + issues + suggestions together.|
|**Prompt is created by**|`partValidationTemplate` + full current part context.|
|**Runtime data injected**|Generated HTML/text; images and descriptions; CA items; source slice; blueprint/validation plan; applied bundles; traceability tags and source refs.|
|**Grounding/search**|OFF. Validation compares output against source/blueprint and content requirements; it does not silently introduce live facts.|
|**Final prompt must ask AI to check**|Coverage against plan/source, factual/source consistency, formula correctness where applicable, image usefulness/labels, missing comparison/timeline/container needs, traceability, and relevant cross-domain coverage based on actual content—not rigid subject labels.|
|**Output schema**|`{summary:{text\_covered\[],images\_created\[],sources\_used\[],enrichments\_added\[]}, overall\_status, issues\[], suggestions:\[{action,target,details,priority}], suggested\_images\[]}`|
|**User interaction**|Popup offers Cancel, Approve Modifications, Ignore \& Approve As-Is. Approve All opens this popup sequentially for each part with progress; it does not approve silently.|
|**Modifications**|Accepted text/container changes use AI-07G/AI-07A as appropriate. Image suggestions use AI-07K → AI-07B → AI-07C.|
|**Approval rule**|Once final part approval happens, its text, images, and CA are approved together and embedded in final document state.|

### AI-07I — Final Consolidated Validation

|Field|Detailed decision|
|-|-|
|**Purpose**|Check the complete approved document for broader coverage gaps after all remaining parts are approved.|
|**Trigger**|**Always/chained** immediately after all non-removed parts reach approved status.|
|**Prompt is created by**|`consolidatedValidationTemplate` + coverage map built from all approved parts.|
|**Runtime data injected**|Consolidated approved HTML/text; all part summaries; blueprints; bundle coverage; traceability map; images/descriptions; CA items; original topic/context.|
|**Grounding/search**|OFF.|
|**Content-driven validation rule**|Do not use a rigid “Economics-only” or “Polity-only” checklist. Inspect actual topic needs. Example: GST should be checked for economic concepts, constitutional/legal aspects, historical evolution, comparisons, visuals, and CA where relevant.|
|**Output schema**|`{covered\_well\[], potential\_gaps\[], suggestions:\[{type:add\_part|
|**User interaction**|Skip All → export. Apply Selected → create additions. Review Each → choose suggestions one by one.|
|**What happens next**|Accepted add-part suggestions invoke AI-07J. Enrichment suggestions invoke AI-07G or AI-07A. After additions are approved, final validation runs again.|

### AI-07J — Quick Blueprint for a New Part

|Field|Detailed decision|
|-|-|
|**Purpose**|Add a topic during Screen 7 without re-running the full document pipeline.|
|**Trigger**|**User-triggered** by Add New Part, or **chained** after user accepts a final-validation add-part suggestion.|
|**Prompt is created by**|`quickBlueprintTemplate` + parent document context + global selections.|
|**Runtime data injected**|New topic; optional subtopics; surrounding document/subject context; global bundle selections; optional suggested bundles; global CA setting; time markers.|
|**Grounding/search**|OFF for planning. CA execution remains AI-07D later.|
|**CA rule**|CA automatically applies if global CA is ON. If OFF but title includes “2024,” “recent,” “current,” etc., prompt/UI suggests CA and user can choose.|
|**Output schema**|`{part\_plan, blueprint, applied\_bundles, ca\_recommended, rationale}`|
|**User interaction**|Generate Immediately → AI-07A. Configure Blueprint First → opens Screen 6-style editing before generation.|

### AI-07K — Validation-Originated Image Proposal

|Field|Detailed decision|
|-|-|
|**Purpose**|Convert a visual gap found by AI-07H into an actionable image request at a known location.|
|**Trigger**|**Conditional/chained** only if validation returns a suggested image and user accepts the modification.|
|**Runtime data injected**|Validation suggestion; target section/anchor; relevant surrounding HTML and text; part metadata.|
|**Output schema**|Standard image request object: `{description, content\_anchor, style\_hint, learning\_goal}`|
|**What happens next**|Uses the exact shared image chain: reserve location → AI-07B expands prompt → AI-07C generates → renderer inserts.|

\---

## Stage 8 — Export (Screen 8)

### AI-08 — No AI Call

|Field|Decision|
|-|-|
|**AI involvement**|None.|
|**Why**|Per-part and consolidated validation have already occurred. Export must be reliable, immediate, and token-free.|
|**Inputs**|Approved formatted HTML/text, approved images, approved current-affairs blocks, citations/tags, document metadata.|
|**Output options**|Copy formatted text and images; save/download as PDF using print-optimized HTML/browser print.|
|**Rule**|Export includes only approved/remaining parts and their embedded assets.|

\---

# 4\. Prompt-Generation Dependency Rules

## 4.1 How one AI output creates the next AI prompt

|From AI output|Prompt-builder action|Next AI call|
|-|-|-|
|AI-01A expanded sub-topic list|Wait for user’s checked/edited set; inject approved topics, not raw suggestions|AI-01B|
|AI-01B generated source material|Save user-edited final pasted text as canonical source|AI-03A|
|AI-02A/AI-02B prepared source|Preserve page/section map and use it as source context|AI-03A|
|AI-03A subject signals|Route relevant bundles; inject subject/sub-discipline into extraction|AI-03B, AI-03C|
|AI-03B deep analysis|Build reusable IDs and page mappings; prepare summaries for large source|AI-03C, AI-04, AI-05, AI-07A|
|AI-03C/AI-03D bundle choices|Merge AI state with user overrides; do not apply irrelevant bundles universally|AI-04, AI-05|
|AI-04 part plan|Slice source and analysis by part; include all definitions/formulas globally|AI-05|
|AI-05 blueprint|Create generation-ready text/image/CA/validation plans|AI-07A, AI-07B, AI-07D, AI-07H|
|AI-07A image-needed markers|Convert each marker into placement reservation and image prompt request|AI-07B → AI-07C|
|AI-07D grounded CA results|Add WEB\_SOURCED blocks or pass to content update|AI-07A/renderer|
|AI-07H accepted suggestions|Select targeted modification path instead of blindly regenerating|AI-07G, AI-07A, AI-07K|
|AI-07I accepted final gap|Create quick blueprint for additional part or target enrichment|AI-07J / AI-07G|

## 4.2 Data minimization rule

For every prompt builder, include **only the data needed to complete that operation**:

* Do not send all source pages to a per-part generation call.
* Send the specific part’s source slice and analysis.
* Send all definitions and formulas globally because they are compact and may be referenced across parts.
* Send other extraction types (PYQs, examples, timelines, comparisons) only when assigned/relevant to that part.
* For large documents, use semantic chunks and structured merged analysis rather than an indiscriminate summary that loses important content.

\---

# 5\. Grounding / Search Policy

|AI operation|Grounding|Reason|
|-|-:|-|
|AI-01A related-subtopic expansion|OFF by default; ON if Method 2 internet toggle is ON|User explicitly requests current/internet-aware scope.|
|AI-01B source draft|OFF by default; ON if Method 2 internet toggle is ON|User explicitly requests web/current facts.|
|AI-02A / AI-02B cleanup/restructure|OFF|Preserve user source; never enrich during extraction.|
|AI-03A / AI-03B / AI-03C / AI-03D|OFF|Analyze only supplied source.|
|AI-04 splitting|OFF|Planning from source analysis only.|
|AI-05 blueprint|OFF|Generates plans and queries; does not fetch CA.|
|AI-06A / AI-06B blueprint edit|OFF|Modify existing plan only.|
|AI-07A writing|OFF|Protect SOURCE\_BACKED traceability.|
|AI-07B / AI-07C image work|OFF|Visualize planned content; no live research needed.|
|AI-07D CA research|**ON**|Live/fresh facts are the purpose of the call.|
|AI-07E / AI-07F / AI-07G / AI-07H / AI-07I / AI-07J / AI-07K|OFF|Generation, evaluation, planning, and refinement work from known document context.|

\---

# 6\. Output and Traceability Requirements

|Content origin|Required tag|Meaning|Required metadata|
|-|-|-|-|
|Uploaded/pasted/AI-drafted canonical source|`SOURCE\_BACKED`|Directly supported by the source processed by the app|Page/section/chunk reference where available|
|AI inference needing verification|`RESEARCH\_REQUIRED`|Not directly stated in source; user should verify|Explanation/reason where possible|
|Clarifying analogy/teaching addition|`OPTIONAL\_ENRICHMENT`|Added to make understanding easier|Container/section source|
|Grounded live web fact|`WEB\_SOURCED: url`|Fresh web-derived information|URL, publisher if available, date, fetch time|

> \*\*Important:\*\* `WEB\_SOURCED` information must never be presented as `SOURCE\_BACKED`. Source-backed means the source currently being studied, not the web.

\---

# 7\. Universal AI Error and Retry Behavior

|Situation|Automated behavior|User-facing recovery|
|-|-|-|
|First temporary failure|Retry automatically according to universal retry policy|Loading/progress remains visible|
|Context/token/length error|Detect error words such as context, token, length, limit|Highlight **Retry with Simplified Prompt**; trimming removes optional/redundant context before source-critical context|
|Rate-limit error|Wait approximately 30 seconds before next retry|Display waiting state, then retry/update|
|Network error|Retry when connection returns where possible|Show failure popup if still unresolved|
|Failure after retries|Preserve prompt, inputs, and partial output state|Editable final prompt with: Retry As-Is / Retry Simplified / Retry with Edited Prompt / Skip This Part / Cancel|
|One parallel part/bundle fails|Do not restart successful siblings|Retry only the failed part/bundle call|

\---

# 8\. Implementation Checklist for This Document

The application is aligned with this document only when all items below are true:

* \[ ] Every AI call in the Master Inventory has a stored template/rule and a runtime prompt builder.
* \[ ] Every final execution prompt is saved in history and visible/copyable in the UI.
* \[ ] Stage 3 is routed: AI does not waste calls analyzing irrelevant bundles.
* \[ ] Definitions/formulas retain stable IDs and source refs across stages.
* \[ ] Part generation uses sliced source context, while making all definitions/formulas available.
* \[ ] Blueprint generation is one coherent prompt per part and runs in staggered parallel mode.
* \[ ] CA query planning and CA execution are separated; execution is grounded and deferred to Stage 7.
* \[ ] Dynamic images from writing, post-review, and validation all use the same placement → prompt → generation → insert chain.
* \[ ] Per-part validation is one combined call and final validation is content-driven, not rigidly subject-labeled.
* \[ ] Approved parts embed text, images, and CA together; Stage 8 uses no AI.
* \[ ] Failure UI displays the exact failed final prompt and all agreed recovery options.

\---

## End of Document 1

**Next planned document:** Document 2 — Prompt Dependency Map (visual/text flow showing every upstream output, decision gate, user intervention, and downstream prompt).

\---

# Appendix A — Complete Runtime Lifecycle, from Input to Export

This appendix expands the master table into the **actual runtime sequence**. It answers four questions at every point:

1. **What data exists now?**
2. **Who creates the next prompt?**
3. **What exact information is injected into that prompt?**
4. **Which output is saved, displayed, or used by the next call?**

## A.1 Path A — User uploads a file

|Sequence|System activity|AI used?|State created/updated|Next decision|
|-:|-|-|-|-|
|1|User uploads file(s) through Screen 1.|No|`inputProfile.method = upload`, file metadata, selected preferences|Continue to reading.|
|2|Technical reader detects type: PDF/DOCX/TXT/HTML/MD/image.|No|`sourceDocument.raw`, page count, file diagnostics|Attempt technical extraction first.|
|3|Parser/OCR extracts text, page map, images where possible.|No|`sourceDocument.text`, `pageMap`, extraction confidence|If usable → Screen 3. If poor → AI-02A.|
|4|AI cleanup fallback repairs extraction without adding outside knowledge.|Conditional|Clean source + unresolved spans|If usable → Screen 3. If poor → AI-02B.|
|5|AI restructuring fallback creates usable sections while retaining uncertainty.|Conditional|Structured source sections|Screen 3 begins.|
|6|If source is too long, semantic chunk planner splits content at natural boundaries.|No unless summaries are required by existing analysis chain|`sourceChunks\[]`, continuity context|AI-03A/AI-03B run per chunk.|
|7|Subject signals, deep extraction, and routed bundle analysis complete.|Yes|`subjectSignals`, `deepAnalysis`, `bundleAnalysis`|User adjusts features; Screen 4 splitting begins.|

## A.2 Path B — User pastes text

|Sequence|System activity|AI used?|State created/updated|Next decision|
|-:|-|-|-|-|
|1|User pastes text in Method 3.|No|`sourceDocument.text`; origin=`pasted`|Do not alter text automatically.|
|2|App performs only basic technical safety/encoding handling, not semantic cleanup.|No|Safe display form; original retained|Continue directly to Screen 3.|
|3|AI-03A begins source understanding.|Yes|Same Stage 3 objects as upload path|Standard pipeline continues.|

## A.3 Path C — User enters topic and uses AI Draft Text (Method 2)

|Sequence|System activity|AI used?|State created/updated|Next decision|
|-:|-|-|-|-|
|1|User enters main topic, initial sub-topics, medium/comprehensive depth, internet/current options.|No|Draft settings in `inputProfile`|User clicks AI Draft Text.|
|2|AI-01A expands related and essential sub-topics.|Yes|`aiOutputs.subtopicExpansion`|User sees, edits, approves checklist.|
|3|User's final approved sub-topics become canonical scope.|No|`inputProfile.approvedSubtopics`|Build content-draft prompt.|
|4|AI-01B creates full source-like study material.|Yes|Draft text + web-source metadata if applicable|Insert into Method 3.|
|5|User edits generated text in the same paste area used by Method 3.|No|Canonical source becomes user-edited version|User clicks Continue.|
|6|Reading stage is skipped because AI draft is already clean enough for the agreed flow.|No|Source is ready|Continue directly to Screen 3.|

## A.4 Canonical source rule

The application must distinguish between **AI output that helped form a source** and the **source ultimately accepted by the user**.

|Situation|Canonical source used by Stage 3 and later|
|-|-|
|File upload succeeds|Extracted/reconstructed file text with source page map|
|User pastes text|The user’s current pasted text|
|AI Draft Text is used|The content currently present in the Method 3 text area after user edits, not necessarily the original AI-01B response|
|User edits any source before Continue|The latest user-visible edited text|

This is essential because analysis, source-backed tags, and later validation must refer to the content the user actually approved as input.

\---

# Appendix B — Prompt Construction Contract

## B.1 Every final prompt has the same logical envelope

Every execution prompt is built as a controlled object, even if the model API ultimately receives strings.

```text
FINAL\_AI\_REQUEST = {
  operation\_id,
  system\_instruction: selected stable system instruction,
  task\_instruction: selected stored template with runtime data,
  context\_payload: minimum necessary current data,
  output\_contract: JSON/HTML schema and validation constraints,
  model\_settings: temperature, grounding flag, timeout/retry class,
  traceability\_policy,
  prompt\_version,
  created\_at
}
```

The viewer may show this in two layers:

1. **Task / final content prompt** — visible and editable for the current run.
2. **System Instructions** — visible through a toggle, copyable, but not editable by end users.

## B.2 Prompt builder algorithm

```javascript
function buildPrompt(operationId, runtimeContext) {
  const rule = PROMPT\_GENERATION\_RULES\[operationId];
  const system = DEFAULT\_PROMPTS\[rule.systemPromptKey];
  const template = DEFAULT\_PROMPTS\[rule.templateKey];

  const selectedStrategy = rule.subjectAware
    ? getSubjectStrategy(runtimeContext.subjectSignals, runtimeContext.topicDomains)
    : '';

  const minimizedContext = selectMinimumRequiredContext(
    rule.contextPolicy,
    runtimeContext
  );

  const filledTask = interpolate(template, {
    ...minimizedContext,
    subject\_strategy: selectedStrategy,
    output\_schema: rule.outputSchema,
    traceability\_rules: rule.traceabilityPolicy,
    user\_direction: runtimeContext.userDirection || 'None'
  });

  return {
    operationId,
    systemInstruction: system,
    userPrompt: filledTask,
    groundingEnabled: resolveGrounding(rule, runtimeContext),
    responseSchema: rule.outputSchema,
    retryClass: rule.retryClass,
    promptVersion: rule.version
  };
}
```

## B.3 Non-negotiable prompt builder rules

|Rule|Required implementation|
|-|-|
|Minimum necessary input|A prompt gets only the source/analysis context it needs. Do not pass the whole document by default.|
|Canonical data|The builder uses current state after user edits, not stale earlier outputs.|
|Structured IDs|Definitions, formulas, topics, parts, containers, image assets, and suggestions must use stable IDs.|
|User override precedence|Explicit user edits to final prompt, selected bundles, part settings, or style override AI defaults for that action.|
|No silent grounding|Grounding is on only for agreed operations. When used, output must carry web-source metadata.|
|No raw AI HTML injection|HTML-like output is transformed into validated structured blocks and rendered through safe templates.|
|Auditability|Save input context references, final prompt, model response, and any error/retry status in prompt history.|
|Versioning of templates|Each template/rule has `template\_id` and `version`; final prompt records both.|

## B.4 Context selection matrix

|Context item|AI-03 analysis|AI-04 split|AI-05 blueprint|AI-07A text|AI-07H part validate|AI-07I final validate|
|-|-:|-:|-:|-:|-:|-:|
|Entire raw source|Only when within context / otherwise chunks|Only when small|No|No|No|No|
|Current source slice|Per chunk|Optional supporting context|Yes, per part|Yes, per part|Yes, per part|No|
|Topic summaries|After chunk merge|Yes for large docs|Optional|No|No|No|
|Subject signals|Yes|Yes|Yes|Yes|Yes|Yes|
|Deep analysis|Produced|Yes|Yes, part relevant|Yes, part relevant|Yes|Aggregate coverage|
|All definitions|Produced|Optional|Yes|**Yes**|Relevant/full as needed|Coverage summary|
|All formulas|Produced|Optional|Yes|**Yes**|Relevant/full as needed|Coverage summary|
|Bundle selections|Result|Yes|Yes|Yes|Yes|Yes|
|Blueprint|No|No|Produced|Yes|Yes|Part summaries|
|Generated HTML|No|No|No|Produced|Yes|All approved parts|
|Images + descriptions|No|No|Planned only|Created later|Yes|Yes|
|CA web results|No|No|Query plan only|Optional integration|Yes|Yes|

\---

# Appendix C — Full Prompt Registry and Contract Table

The following is the implementation registry. It names each stored template, the prompt-builder rule, exact placeholder families, expected schema, quality constraints, and UI visibility requirement.

|ID|Template / rule key|Final prompt created from|Required placeholders / context|Required response contract|Visible where|
|-|-|-|-|-|-|
|AI-01A|`subtopicExpansionTemplate`|Universal education system + topic expansion task|`topic`, `user\_subtopics`, `depth`, `exam\_context`, `internet\_mode`, `current\_mode`|`guaranteed\_topics`, `essential`, `optional`, `current`, `reasons`|Screen 1 after suggestion appears|
|AI-01B|`draftSourceMaterialTemplate`|Universal education system + draft writer task|`topic`, `approved\_subtopics`, `depth`, `internet\_mode`, `current\_mode`, `exam\_context`|`content`, `heading\_map`, `web\_sources`, `fact\_markers`|Screen 1 / Method 3 draft result|
|AI-02A|`extractionCleanupTemplate`|Source-preservation system + cleanup task|`raw\_text`, `page\_map`, `diagnostics`, `source\_type`|`clean\_text`, `page\_map`, `unresolved\_segments`, `quality\_status`|Screen 2 extraction details|
|AI-02B|`sourceRestructureTemplate`|Source-preservation system + restructure task|`raw\_or\_cleaned\_text`, `page\_map`, `diagnostics`|`structured\_text`, `sections`, `unresolved\_segments`|Screen 2 extraction details|
|AI-03A|`subjectSignalTemplate`|Analysis system + detection task|`source\_text\_or\_chunk`, `page\_map`, `exam\_context`|subject, sub-discipline, domains, evidence-based signals|Screen 3 prompt accordion|
|AI-03B|`deepExtractionTemplate`|Analysis system + extraction task|`subject\_signals`, `source\_text\_or\_chunk`, `page\_map`, `chunk\_context`|topics, D-IDs, F-IDs, PYQs, examples, timelines, tables, comparisons|Screen 3 prompt accordion|
|AI-03C|`smartBundleTemplate` + selected bundle fragments|Bundle system + routed detection task|`signals`, `deep\_analysis`, `relevant\_source`, `routed\_bundle\_ids`|bundle/feature state, evidence, tier, reason|Screen 3 prompt accordion|
|AI-03D|`bundleTemplates\[bundleId]`|Bundle system + requested bundle task|`requested\_bundle`, `source`, `signals`, `analysis`|bundle-only detection response|Screen 3 on-demand viewer|
|AI-04|`partSplittingTemplate`|Planning system + splitting task|`deep\_analysis`, `page\_rules`, `source\_context\_or\_summaries`, `global\_bundles`|part array, range/reasoning, per-part bundles, warnings|Screen 4 above parts|
|AI-05|`blueprintTemplate` + subject strategy|Blueprint system + per-part plan task|`part\_plan`, `source\_slice`, `part\_analysis`, `all\_definitions`, `all\_formulas`, `bundles`|headings, text/image/CA/validation plans|Every Screen 5 card|
|AI-06A|`blueprintPartRefinementPrompt`|Blueprint edit system + scoped user request|`user\_message`, `blueprint`, `scope`, `part\_meta`|scope, JSON patch, update explanation, undo payload|Screen 6 chat history|
|AI-06B|`blueprintSectionRegenerationTemplate`|Blueprint system + section-only task|`target\_section`, `current\_blueprint`, `locked\_sections`, `user\_direction`|replacement target section|Screen 6 targeted action|
|AI-07A|`partWriterPrompt` + optional strategy|Writer system + part execution task|`part`, `source\_slice`, `part\_analysis`, `all\_definitions`, `all\_formulas`, `blueprint`, `bundles`, `CA`|safe blocks/HTML data, containers, tags, citations, image markers|Screen 7 above generated part|
|AI-07B|`imagePromptBuilder`|Educational image system + detailed visual task|`image\_description`, `nearby\_text`, `learning\_goal`, `style`, `placement`, `user\_direction`|detailed prompt, style/layout, location, split decision|Screen 7 per image|
|AI-07C|`imageGenerationRequest`|Image-model instruction generated by AI-07B|`expanded\_prompt`, image settings|image asset, metadata|Screen 7 per image|
|AI-07D|`currentAffairsPrompt`|Grounded research system + current query task|`query`, `part\_context`, time context, topic|facts/date/URL/source/fetch time|Screen 7 CA section|
|AI-07E|`imageGapReviewTemplate`|Teaching review system + visual gap task|`generated\_html`, `image\_plan`, `anchors`, `bundles`|missing image suggestions/anchors|Screen 7 review controls|
|AI-07F|`highlightVisualizeTemplate`|Visual planning system + selected text task|`selection`, `surrounding\_context`, `part\_meta`, `bundles`|one expanded prompt + 3 style choices/reasons|Visualize This popup|
|AI-07G|`refinementPrompt`|Refine system + scope/diff task|`user\_message`, current blocks, selection, manual edits, blueprint|detected scope + before/after patch/diff|Screen 7 refinement panel|
|AI-07H|`partValidationTemplate`|Validation system + part audit task|rendered part, images/descriptions, CA, source slice, blueprint, tags|summary, issues, suggestions, visual gaps|Approve Part validation popup|
|AI-07I|`consolidatedValidationTemplate`|Validation system + full-document audit|approved document, part summaries, coverage map, bundle map, traceability|strengths, gaps, suggestions, readiness|Final validation popup|
|AI-07J|`quickBlueprintTemplate`|Blueprint system + added part task|topic, subtopics, parent doc context, global bundles, CA choice|new part plan, blueprint, bundle/CA rationale|Add Part modal / Screen 6 style view|
|AI-07K|`validationImageRequestTemplate`|Image request adapter|validation recommendation, target anchor, local content|standard image request object|Validation popup then image controls|

\---

# Appendix D — Detailed Output Schemas

Schemas below are conceptual contracts. The implementation may use TypeScript-style objects or JSON, but fields and IDs must be preserved.

## D.1 Subject signal schema

```json
{
  "primary\_subject": "Economics",
  "sub\_discipline": "Macroeconomics",
  "secondary\_domains": \["Current Affairs", "Public Policy"],
  "signals": {
    "formula": {
      "strength": "strong",
      "evidence": \["GDP = C + I + G + NX"],
      "page\_refs": \[10]
    },
    "location": {
      "strength": "weak",
      "evidence": \["India", "Madhya Pradesh"],
      "page\_refs": \[7, 18]
    }
  },
  "routing\_hints": \["formula\_ops", "chart\_data", "current\_affairs"]
}
```

## D.2 Deep-analysis schema

```json
{
  "topics": \[
    {
      "id": "T-004",
      "title": "Methods of Measuring GDP",
      "page\_range": \[6, 10],
      "parent\_topic\_id": "T-001",
      "summary": "..."
    }
  ],
  "definitions": \[
    {
      "id": "D-002",
      "term": "Gross Domestic Product",
      "definition": "...",
      "page\_refs": \[4],
      "topic\_ids": \["T-001"]
    }
  ],
  "formulas": \[
    {
      "id": "F-001",
      "expression": "GDP = C + I + G + NX",
      "variables": \[{"symbol": "C", "meaning": "Consumption"}],
      "purpose": "Expenditure method of measuring GDP",
      "page\_refs": \[10],
      "topic\_ids": \["T-004"]
    }
  ],
  "pyqs": \[],
  "comparisons": \[],
  "examples": \[],
  "timelines": \[],
  "tables": \[],
  "diagrams": \[]
}
```

## D.3 Bundle analysis schema

```json
{
  "bundles": \[
    {
      "bundle\_id": "formula\_ops",
      "state": "auto\_on",
      "evidence": \["12 formulas detected across pages 6–15"],
      "features": \[
        {
          "feature\_id": "formula\_derivation",
          "state": "auto\_on",
          "reason": "Core formulas are directly explained in source"
        },
        {
          "feature\_id": "sensitivity\_analysis",
          "state": "suggested",
          "reason": "Variables permit relationship analysis"
        }
      ]
    }
  ]
}
```

## D.4 Part plan schema

```json
{
  "recommended\_range": {"min": 2, "max": 6},
  "proposed\_count": 5,
  "out\_of\_range\_warning": null,
  "parts": \[
    {
      "part\_id": "P-02",
      "title": "Types of GDP and Measurement Methods",
      "page\_range": \[6, 10],
      "topic\_ids": \["T-004"],
      "formula\_ids": \["F-001"],
      "definition\_ids": \["D-002", "D-003"],
      "applied\_bundles": \["formula\_ops", "storytelling", "comparison"],
      "rationale": "All three measurement methods must remain together."
    }
  ]
}
```

## D.5 Blueprint schema

```json
{
  "part\_id": "P-02",
  "headings": \[{"id": "H-1", "text": "Nominal and Real GDP"}],
  "text\_plan": \[
    {
      "container\_id": "C-01",
      "type": "concept\_box",
      "heading\_id": "H-1",
      "source\_refs": \["D-002", "F-001"],
      "purpose": "Clarify the base concept before formulas."
    }
  ],
  "image\_plan": \[
    {
      "image\_id": "IMG-02-01",
      "title": "Nominal vs Real GDP",
      "placement\_after": "C-01",
      "learning\_goal": "Show price change versus output change.",
      "style\_recommended": "Comparison Infographic",
      "style\_reasoning": "Learner must distinguish two similar concepts side-by-side."
    }
  ],
  "ca\_plan": {
    "queries": \["Latest India GDP growth and base-year update"]
  },
  "validation\_plan": \["Ensure each GDP method has formula, variables, and example."],
  "applied\_bundles": \["formula\_ops", "comparison"]
}
```

## D.6 Generated part schema

```json
{
  "part\_id": "P-02",
  "html\_blocks": \[
    {
      "anchor": "part-P-02-C-01",
      "container\_type": "concept\_box",
      "safe\_content": "...",
      "traceability": "SOURCE\_BACKED",
      "source\_refs": \["p. 6", "D-002"]
    }
  ],
  "image\_needed": \[
    {
      "request\_id": "IR-001",
      "description": "Visual comparison of nominal and real GDP...",
      "after\_anchor": "part-P-02-C-01",
      "style\_hint": "Comparison Infographic",
      "learning\_goal": "..."
    }
  ],
  "citations": \[],
  "generation\_summary": "..."
}
```

## D.7 Validation schema

```json
{
  "overall\_status": "needs\_review",
  "summary": {
    "text\_covered": \["..."],
    "images\_created": \[{"image\_id": "IMG-02-01", "shows": "..."}],
    "sources\_used": \["pages 6–10"],
    "enrichments\_added": \["Bread-maker analogy"]
  },
  "issues": \[
    {
      "issue\_id": "V-003",
      "type": "missing\_comparison",
      "target": "P-02",
      "detail": "A comparison table of the three GDP methods is missing.",
      "priority": "high"
    }
  ],
  "suggestions": \[
    {
      "suggestion\_id": "S-003",
      "action": "add\_container",
      "container\_type": "comparison\_table",
      "target\_anchor": "part-P-02-C-05",
      "details": "..."
    }
  ]
}
```

\---

# Appendix E — Complete User Intervention Matrix

This clarifies where the user controls AI and where the system should proceed automatically.

|Stage|User can view prompt|User can copy prompt|User can edit final prompt|User can approve/reject output|User can change scope/style|Automatic continuation|
|-|-:|-:|-:|-:|-:|-|
|Method 2 sub-topic expansion|Yes|Yes|Yes|Yes; select/edit topic list|Yes; depth/search settings|No; waits for topic approval|
|Method 2 content draft|Yes|Yes|Yes|Yes; edit inserted text|Yes; depth/current options|No; waits for Continue|
|Reading AI fallback|Yes|Yes|Yes for retry|Can retry/skip/cancel|Extraction method A/B/C|Yes only through fallback chain|
|Screen 3 analysis|Yes|Yes|Yes for rerun|Can keep/override selections|Bundles/features on/off|Analysis itself auto-runs|
|Screen 4 splitting|Yes|Yes|Yes for rerun|Can accept/edit/add/remove/merge|Per-part title/range/bundles|Runs on Stage 4 entry|
|Screen 5 blueprint|Yes, per part|Yes|Yes for rerun|Can approve/open detail|Bundle chips at part level|Runs in staggered parallel after parts confirmed|
|Screen 6 chat/refinement|Yes|Yes|User message itself is editable|Undo targeted change|Target section/bundles/styles|Only after user chat/action|
|Screen 7 text generation|Yes, per part|Yes|Yes for regeneration|Can retain/refine/remove part|Part generation scope|Generate only on user action/auto-generate action|
|Screen 7 image prompt|Yes|Yes|Yes|Preview setting can require approval|Style/dropdown/direction|Default auto-generate after image request|
|Screen 7 CA|Yes|Yes|Edit query before rerun|Can include/omit results|Fetch action / global CA|Auto only during Auto-Generate when applicable|
|Screen 7 validation|Yes|Yes|Editable for retry|Approve modifications / ignore / cancel|Select suggestions|Automatically runs after Approve Part click|
|Final validation|Yes|Yes|Editable for retry|Skip/apply/review suggestions|Select additions|Auto after all remaining parts approved|
|Export|Not applicable|Not applicable|Not applicable|Select export contents/options|Copy/PDF format|No AI|

\---

# Appendix F — Bundle-to-Prompt Routing Model

The bundle system is not a fixed list that is blindly executed for every subject. The rule is:

> \*\*Signals from actual content determine which advanced detection prompt fragments are included. User can force-enable any skipped bundle. Global selection then inherits into only relevant parts, subject to per-part override.\*\*

## F.1 Signal-to-bundle route examples

|Detected evidence|Routed bundle(s)|Deep analysis now|Deep generation later|
|-|-|-|-|
|Mathematical equations, variables, quantitative identities|Formula Operations, Mathematics|Formula IDs, variables, source refs|Derivation, operations, relationship facts, examples, mistakes|
|Place names, borders, regions, rivers, countries|Geography / Location / Maps|Location names/context/page refs|Context-specific facts; maps/neighbors/capitals/seas/passages only when useful|
|Named people, theorists, leaders, scientists|Personalities|Person name/role/context|PSC-relevant facts, contribution, related CA if applicable|
|Dates, events, periods, chronology|Timeline / Historical|Event/date sequence|Timeline container, cause-effect, relevant historical explanation|
|Laws, articles, cases, courts, constitutional references|Legal/Constitutional|Reference/case/article extraction|Case facts, plea/issue/verdict where relevant; legal context|
|Code, algorithms, data structures|Computer Science|Code/algorithm/complexity signals|Code blocks, I/O demos, complexity tables, edge cases|
|Tables, numbers, datasets, charts|Data / Chart operations|Table/chart references|Comparison, trend, data insight, appropriate visualisation|
|Abstract mechanism or production steps|Process / Creation|Process signals|Flowchart, decision tree, lifecycle/process explanation|
|Difficult abstract concept with narrative potential|Storytelling / Analogy|Candidate concepts/examples|Story box/comic/analogy when it improves understanding|
|Current/recent policy/news terms|Current Affairs|CA candidates / source cues|Editable grounded queries executed only at Stage 7|

## F.2 Context-aware location facts decision tree

```text
Location detected in part
  └─ Is location central to the part’s learning objective?
      ├─ No → use only basic directly relevant mention; do not create generic fact dump.
      └─ Yes → identify content context:
           ├─ History / civilisation → archaeological, historical, trade/cultural relevance
           ├─ Geography → physical, political, economic geography as relevant
           ├─ Geopolitics → borders, neighbours, strategic/political relationships
           ├─ Economics → GSDP/industries/resources/comparison/policy relevance
           ├─ Current Affairs → current event facts and grounded sources
           └─ Other → facts necessary for exact topic only
```

## F.3 Cache policy for deferred enrichment

|Entity type|Cache key|Why|
|-|-|-|
|Location|`location:{normalized\_name}:{context\_key}`|The same location requires different facts for Indus Valley history vs geopolitics.|
|Personality|`person:{normalized\_name}:{exam\_context}:{topic\_context}`|PSC-focused facts for a policy topic can differ from literature/medical context.|
|Formula|`formula:{formula\_id}:{operation\_set}`|Avoid repeated deep operations while allowing different treatment if a user enables new formula features.|
|CA query|`ca:{normalized\_query}:{time\_window}`|CA needs timestamp and refresh behavior; cannot be cached indefinitely.|

\---

# Appendix G — Image Intelligence Specification

## G.1 The image decision hierarchy

|Decision|Rule|
|-|-|
|Is an image needed?|Blueprint may plan it; text generation may request it; post-review may suggest it; validation may propose it.|
|Where should image go?|AI returns a stable container/paragraph anchor. The app reserves slot only after target text exists.|
|How many images?|Aim for one comprehensive understandable visual for related material. Split only if a composite becomes too dense/confusing.|
|Who picks style?|AI recommends according to learning objective; user can override.|
|What matters most?|Understanding difficult content, not aesthetic decoration.|
|Can styles mix?|Yes. A single composite may use metrics/graphs, a comparison table, and flow/process sections if that teaches better.|
|Are duplicates blocked?|No. The user may deliberately create a second visual perspective.|

## G.2 Recommended visual-style routing examples

|Learning need|Recommended style family|Reason|
|-|-|-|
|Formula with components|Pictograph, icon array, formula breakdown, labelled branches|Shows relationships and variables at a glance|
|Process / method / lifecycle|Flowchart, step-by-step, decision tree, process map|Preserves sequence and choices|
|Comparison|Comparison matrix, split screen, table + visual|Makes differences explicit|
|Timeline / evolution|Timeline strip, chronological cards|Shows order and change|
|Character-driven concept/example|Comic story / storyboard|Makes abstract process memorable|
|Dataset / trend|Chart plus data insight cards|Shows magnitude and pattern|
|Geography / international context|Context-aware map/labelled regional visual|Shows spatial relationships|
|Code/algorithm|Step trace, state visualization, complexity table|Makes execution/behavior visible|

## G.3 Image-prompt quality checklist

Each AI-07B final image prompt must include:

* The **exact learning objective**.
* The concept/facts that must be visually accurate.
* Labels, relationships, steps, values, or comparison dimensions to show.
* The intended layout, reading order, and style.
* Instruction to prioritize clarity, legible labels, and teaching value.
* Instruction to avoid irrelevant decoration and invented factual labels.
* If an image combines styles, explicit sections/panels and their roles.
* Placement anchor and title metadata for the application.

\---

# Appendix H — Approval and Validation State Machine

## H.1 Per-part approval state

```text
DRAFT
  → text generated
  → images/CA may be generated
  → user clicks Approve Part
  → VALIDATING
      ├─ Cancel → DRAFT
      ├─ Ignore \& Approve As-Is → APPROVED
      └─ Approve Modifications → APPLYING\_CHANGES → re-render → APPROVED
```

When a part reaches `APPROVED`, the approved version includes **text + images + current-affairs content together**, as agreed. If the UI exposes granular text/images checks for review, they are review controls; the final approved part embeds all included assets.

## H.2 Approve All state

```text
User selects Approve All Parts
  → validate first remaining unapproved part
  → show validation popup and wait for user's decision
  → preserve any completed approval
  → move to next remaining part
  → if user cancels, stop sequence; already approved parts stay approved
  → after all remaining parts approved, invoke final validation
```

## H.3 Final validation loop

```text
All remaining parts approved
  → AI-07I final validation
      ├─ Skip All → Export
      ├─ Review Each → user selects each action
      └─ Apply Selected → add/enrich targeted content
                            → validate newly changed/added part(s)
                            → final validation runs again
                            → Export when user skips/accepts final state
```

\---

# Appendix I — Screen-by-Screen Prompt Visibility Requirements

|Screen|Required viewer|Minimum displayed information|
|-|-|-|
|Screen 1|AI Draft scope/content prompt viewer|Current topic, approved sub-topics, depth, current/internet mode, final prompt, copy/edit/retry controls|
|Screen 2|Extraction fallback viewer|Raw extraction diagnosis, chosen method, final cleanup/restructure prompt, result status|
|Screen 3|Analysis accordion|Subject detection prompt, deep extraction prompt, routed bundle prompt(s), evidence and final response status|
|Screen 4|Split prompt viewer above part list|Final splitting prompt, page guardrail, source size strategy, factors leading to proposed count|
|Screen 5|Per-card blueprint prompt viewer|Exact part metadata, applied bundles, final blueprint prompt, copy action|
|Screen 6|Editable generation-related plan prompt sections|The text plan/image plan/CA plan prompts as applicable, plus AI chat request and patch outcome|
|Screen 7|Per generated part collapsible prompt panel|Actual text generation prompt; each image prompt; CA search prompt/query; validation prompt; refinement/visualize prompts when used|
|Screen 8|No AI viewer needed|Display traceability/citations as part of exported content if chosen|

\---

# Appendix J — Security and Safe Rendering Requirements Already Implied by the Agreed Flow

These are not new product features; they are implementation requirements necessary to make agreed features work safely, especially prompt editing and HTML output.

|Risk point|Required handling|
|-|-|
|User edits an image/text prompt with quotes or HTML-like content|Store prompt as data, never concatenate it into unsafe HTML attributes. Render textarea values safely.|
|AI returns HTML-like text|Convert to structured content blocks or sanitize against approved container allowlist before insertion.|
|Generated links from grounded CA|Validate URL protocol; render safe anchor attributes; preserve displayed source metadata.|
|Prompt viewer|Use text/textarea rendering, not raw HTML insertion, so a prompt cannot break the page.|
|User-provided pasted content|Display/parse safely; do not execute scripts or event handlers.|
|Image placement anchor|Resolve only known generated container IDs; never execute selectors supplied directly by arbitrary content without validation.|

\---

# Appendix K — State and Audit Record Requirements

## K.1 Minimum state objects

```javascript
const state = {
  inputProfile: {},
  sourceDocument: {
    origin: null, // upload | pasted | ai\_draft
    text: '',
    pageMap: \[],
    chunks: \[],
    diagnostics: {}
  },
  analysis: {
    subjectSignals: null,
    deepAnalysis: null,
    bundleAnalysis: null,
    userBundleOverrides: {}
  },
  parts: \[],
  blueprints: {},
  generatedParts: {},
  imageAssets: {},
  currentAffairs: {},
  approvals: {},
  promptHistory: {},
  retryHistory: {},
  cache: {
    entityContextFacts: {},
    caResults: {}
  }
};
```

## K.2 Prompt history record

```json
{
  "execution\_id": "EX-2026-00123",
  "operation\_id": "AI-07A",
  "template\_id": "partWriterPrompt",
  "template\_version": "1.0",
  "created\_at": "ISO-8601",
  "input\_refs": \["P-02", "blueprint:P-02", "source:pages-6-10"],
  "grounding\_enabled": false,
  "system\_instruction": "...",
  "final\_prompt": "...",
  "response\_status": "success",
  "output\_ref": "generatedParts:P-02:v1",
  "retry\_of": null,
  "user\_edited": false
}
```

## K.3 Why audit records matter

* The prompt visible to the user must match the prompt actually executed.
* An edited regeneration must be traceable to the exact edited prompt.
* When a developer claims a flow works, the prompt history proves the real chain from input to output.
* If a bundle or part receives wrong data, history shows whether routing, context assembly, or rendering failed.

\---

# Appendix L — Developer Build Order

This recommended order prevents a UI skeleton from pretending to have AI functionality.

|Build sequence|What must be completed|Evidence of completion|
|-:|-|-|
|1|Central state, prompt registry, prompt builder, prompt history/viewer|One test operation builds/stores/displays exact final prompt|
|2|Source preparation and canonical-source handling|Upload/paste/AI-draft paths all produce valid `sourceDocument`|
|3|AI-03A + AI-03B + structured merge|Analysis JSON with stable topic/definition/formula IDs and page refs|
|4|AI-03C/AI-03D plus Screen 3 three-tier UI|Toggle → state → prompt → updated bundle data chain works|
|5|AI-04 splitting and editable part state|Changes on Screen 4 persist and drive next screen|
|6|AI-05 blueprints in staggered parallel execution|Every part has a distinct saved blueprint/prompt and retry isolates failures|
|7|AI-06 surgical patch + undo|Only intended blueprint section changes after chat|
|8|AI-07A source-sliced writing and safe renderer|Generated part shows correct tags, source refs, containers, and prompt viewer|
|9|AI-07B/C shared image chain|Blueprint/text/validation image requests all enter same insert → prompt → generate → render path|
|10|AI-07D grounded CA and WEB\_SOURCED rendering|Query editable; result has URLs/date/fetch timestamp; no mis-tagging|
|11|AI-07G/H/I/J approval, refinement, additions|Per-part sequential validation and final validation loop work end-to-end|
|12|Export|Only approved embedded content copies/prints correctly with no AI call|

\---

# Appendix M — Final End-to-End Example: “National Income”

This example demonstrates the intended prompt chain rather than introducing a separate feature.

1. User chooses **Method 2**, enters `National Income`, sub-topics `GDP, GNP`, selects **Medium**, turns on internet/current option.
2. **AI-01A** receives topic/sub-topics/depth/search mode. It suggests NDP, NNP, Per Capita Income, GDP Deflator, India GDP rankings/current developments.
3. User unchecks one optional topic and approves the rest.
4. **AI-01B** receives the approved list and produces full source-like material. Grounding is enabled because user asked for internet/current facts. Result enters Method 3; user edits it.
5. User continues; Stage 2 is skipped. **AI-03A** detects Economics/Macroeconomics, formulas, data, comparisons, timeline/current cues, personality/location mentions if present.
6. **AI-03B** extracts stable items: `D-001 GDP`, `F-001 GDP = C+I+G+NX`, relevant PYQs, comparisons and tables.
7. Router invokes **AI-03C** for Formula Operations, Chart/Data, Comparison, Storytelling and Current Affairs-related planning signals—not unrelated medical or CS bundles.
8. Screen 3 shows auto-on/suggested/force-enable features. User accepts and force-enables an additional comparison feature.
9. **AI-04** uses deep analysis as primary context and page/topic summaries as necessary. It proposes coherent parts: foundations; methods; GNP/NDP; deflator; welfare/comparisons; PYQs/current data. Formula explanations remain with their methods.
10. **AI-05** runs per part with staggered parallel calls. For “GDP Measurement Methods,” it creates headings, formula/text plan, a comparison infographic plan, CA queries, and validation checks.
11. User changes one image plan via **AI-06A**: “Use flowchart instead of comic.” Only that image plan item changes; undo exists.
12. On Screen 7, **AI-07A** generates Part 2 using pages for that part, Part 2 analysis, all definitions/formulas, blueprint, and applied bundles. It returns source-tagged blocks and an image marker after the formula explanation.
13. The shared image chain calls **AI-07B**, which builds a teaching-first formula/flow visual prompt, then **AI-07C**, which generates and places the image.
14. User fetches current affairs. **AI-07D** uses the blueprint’s query with grounding, returns dated sources, and creates `WEB\_SOURCED` blocks.
15. User highlights a paragraph and clicks Visualize This. **AI-07F** receives highlighted text plus surrounding paragraphs and recommends three styles. User chooses one; image is generated.
16. User clicks Approve Part. **AI-07H** returns summary, image assessment, coverage gaps, and a suggestion for a comparison table. User accepts; system applies targeted change.
17. When all parts are approved, **AI-07I** checks full coverage across economic, historical, policy, comparison, and CA dimensions actually present in this topic. It may suggest a quick added part for current rankings.
18. User accepts added part; **AI-07J** builds quick blueprint. New part is generated, validated, approved; final validation re-runs.
19. Screen 8 compiles approved formatted text, images, CA and citations. **No AI call** runs during export.

\---

## Comprehensive Document End



\# DOCUMENT 1: AI USAGE MASTER TABLE



\*\*StudyForge — Complete AI Call Inventory Across All 8 Stages\*\*



Legend:

\- \*\*Trigger:\*\* ALWAYS / USER-TRIGGERED / CONDITIONAL

\- \*\*Grounding:\*\* ON (uses web search) / OFF (source only)

\- \*\*Editable:\*\* Whether user can view/edit the final prompt



\---



\## STAGE 1: INPUT (Screen 1)



| # | AI Call Name | Trigger | Input Data | Prompt Template (Stored) | Dynamic Injections | Output Format | Grounding | Feeds Into | User Editable? |

|---|---|---|---|---|---|---|---|---|---|

| 1.1 | \*\*Sub-Topic Expansion\*\* (Method 2 only) | ALWAYS (when Method 2 used) | User topic + user sub-topics + internet toggle + exam context + state | `subTopicExpansionPrompt` | {topic}, {user\_sub\_topics}, {exam}, {state}, {internet\_search\_flag} | JSON: `{expanded\_sub\_topics\[], reasoning\[], optional\_additions\[]}` | ON if internet toggle enabled, else OFF | Sub-topic approval panel → 1.2 | Yes (view + edit before regen) |

| 1.2 | \*\*Content Generation\*\* (Method 2 only) | ALWAYS (after user approves expanded list) | Final approved sub-topics + topic + depth setting + exam context + state + internet toggle | `contentDraftPrompt` | {topic}, {approved\_sub\_topics}, {depth: medium/comprehensive}, {exam}, {state}, {ca\_toggle}, {internet\_search\_flag} | Structured HTML/text formatted like study material | ON if internet toggle enabled, else OFF | Method 3 paste textarea | Yes |



\---



\## STAGE 2: READING (Screen 2)



| # | AI Call Name | Trigger | Input Data | Prompt Template (Stored) | Dynamic Injections | Output Format | Grounding | Feeds Into | User Editable? |

|---|---|---|---|---|---|---|---|---|---|

| 2.1 | \*\*Text Cleanup\*\* (auto-failover) | CONDITIONAL (only if technical extraction fails) | Raw extracted text (garbled) | `textCleanupPrompt` | {raw\_text}, {file\_type}, {error\_context} | Cleaned plain text | OFF | Stage 3 input | Yes (visible in settings) |

| 2.2 | \*\*Text Restructuring\*\* (auto-failover) | CONDITIONAL (only if 2.1 also insufficient) | Cleaned but unstructured text | `textRestructurePrompt` | {cleaned\_text}, {file\_type} | Structured text with sections | OFF | Stage 3 input | Yes |



\*\*Note:\*\* No AI for file upload (technical extraction), no AI for Method 2 text (already clean), no AI for pasted text (as-is).



\---



\## STAGE 3: UNDERSTANDING + FEATURE DETECTION (Screen 3)



| # | AI Call Name | Trigger | Input Data | Prompt Template (Stored) | Dynamic Injections | Output Format | Grounding | Feeds Into | User Editable? |

|---|---|---|---|---|---|---|---|---|---|

| 3.1 | \*\*Subject Detection\*\* (Prompt 1 of Hybrid) | ALWAYS | Full extracted/generated text | `subjectDetectionPrompt` | {full\_text\_or\_chunk} | JSON: `{primary\_subject, sub\_discipline, signals: {formulas, dates, code, locations, persons, legal\_refs, diagrams, charts, institutions, processes, medical\_terms}, confidence\_per\_signal}` | OFF | 3.2 + 3.3 (routing logic) | Yes |

| 3.2 | \*\*Deep Extraction\*\* (Prompt 2 of Hybrid) | ALWAYS | Full text + subject + sub-discipline from 3.1 | `deepExtractionPrompt` (subject-specific variants exist) | {full\_text}, {subject}, {sub\_discipline} | JSON: `{topics\[], definitions\[], formulas\[], pyqs\[], comparisons\[], examples\[], timelines\[], tables\[]}` | OFF | Screen 3 display, Stage 4 splitting, Stage 7 text generation | Yes |

| 3.3 | \*\*Smart Bundle Detection\*\* (Prompt 3 of Hybrid) | ALWAYS (only for signal-matched bundles) | Text snippets + signal context from 3.1 | Multiple bundle-specific templates fired as one combined prompt for relevant bundles | {relevant\_text}, {matched\_bundles\[]}, {subject} | JSON per bundle: `{detected, confidence, items\_found\_count, evidence, sub\_features\[]}` | OFF | Screen 3 three-tier toggle display | Yes |

| 3.4 | \*\*Force-Enable Bundle\*\* (on-demand) | USER-TRIGGERED (when user toggles hidden bundle) | Full text + specific bundle definition | `forceEnableBundlePrompt` (uses bundle-specific template) | {full\_text}, {bundle\_name}, {bundle\_criteria} | JSON: `{items\_found\[], evidence\[], sub\_features\[]}` | OFF | Screen 3 (bundle becomes visible) | Yes |



\*\*Bundle Templates Stored (fired conditionally within 3.3):\*\*

\- `geographyBundlePrompt`, `personalityBundlePrompt`, `formulaOpsBundlePrompt`, `chartDataBundlePrompt`, `legalCaseLawBundlePrompt`, `timelineHistoricalBundlePrompt`, `storytellingBundlePrompt`, `administrationBundlePrompt`, `processCreationBundlePrompt`, `codeCSBundlePrompt`, `medicalScienceBundlePrompt`, `currentAffairsLayerBundlePrompt`



\---



\## STAGE 4: PARTS (Screen 4)



| # | AI Call Name | Trigger | Input Data | Prompt Template (Stored) | Dynamic Injections | Output Format | Grounding | Feeds Into | User Editable? |

|---|---|---|---|---|---|---|---|---|---|

| 4.1 | \*\*Part Splitting\*\* | ALWAYS (when Screen 4 loads) | Stage 3 analysis JSON (primary) + full text if under token limit else per-topic summaries + page count table + splitting rules + global bundle selections | `partSplittingPrompt` | {analysis\_json}, {source\_text\_or\_summaries}, {page\_count\_guide}, {splitting\_rules}, {global\_bundles}, {total\_pages} | JSON: `parts\[{id, title, page\_range, topics\[], formulas\[], definitions\[], pyqs\[], applied\_bundles\[], description}]` | OFF | Screen 4 display, Stage 5 blueprint | Yes |



\---



\## STAGE 5: BLUEPRINT PLAN (Screen 5)



| # | AI Call Name | Trigger | Input Data | Prompt Template (Stored) | Dynamic Injections | Output Format | Grounding | Feeds Into | User Editable? |

|---|---|---|---|---|---|---|---|---|---|

| 5.1 | \*\*Blueprint Generation\*\* (per part, PARALLEL with 1s gap) | ALWAYS (when Screen 5 loads) | Part metadata from 4.1 + relevant source slice + relevant analysis (filtered to this part's topics) + applied bundles + subject-specific strategy | `blueprintPrompt` routed via `SUBJECT\_PROMPT\_MAP` (economicsBlueprintPrompt, polityBlueprintPrompt, historyBlueprintPrompt, geographyBlueprintPrompt, scienceTechBlueprintPrompt, environmentBlueprintPrompt, socialIssuesBlueprintPrompt, mpSpecificBlueprintPrompt, currentAffairsBlueprintPrompt) | {part\_metadata}, {source\_slice}, {part\_analysis}, {applied\_bundles}, {subject}, {universal\_blueprint\_header} | JSON: `{headings\[], text\_plan{}, image\_plan\[{title, style, description, prompt\_seed}], ca\_plan\[{query, purpose}], validation\_plan{}}` | OFF | Screen 5 card grid, Screen 6 detail view, Stage 7 generation | Yes |



\---



\## STAGE 6: BLUEPRINT DETAIL (Screen 6)



| # | AI Call Name | Trigger | Input Data | Prompt Template (Stored) | Dynamic Injections | Output Format | Grounding | Feeds Into | User Editable? |

|---|---|---|---|---|---|---|---|---|---|

| 6.1 | \*\*Blueprint Chat Modification\*\* (surgical) | USER-TRIGGERED (when user types in chat) | User message + current blueprint JSON + part metadata + previous chat history | `blueprintPartRefinementPrompt` | {user\_message}, {current\_blueprint}, {part\_metadata}, {chat\_history}, {applied\_bundles} | JSON: `{affected\_sections\[], changes{}, diff\_summary, undo\_snapshot{}}` | OFF | Screen 6 re-render (only affected sections) + undo stack | Yes (chat message is the prompt) |



\---



\## STAGE 7: GENERATION (Screen 7)



\### 7A. Text Generation



| # | AI Call Name | Trigger | Input Data | Prompt Template (Stored) | Dynamic Injections | Output Format | Grounding | Feeds Into | User Editable? |

|---|---|---|---|---|---|---|---|---|---|

| 7.1 | \*\*Text Generation\*\* (per part) | USER-TRIGGERED (Generate Part N) OR ALWAYS (Generate All) | Part metadata + sliced source (pages for that part) + part-specific analysis + ALL definitions + ALL formulas + blueprint text\_plan + applied bundles | `partWriterPrompt` (with subject variant `economicsPartWriterPrompt` etc.) | {part\_metadata}, {source\_slice}, {part\_analysis}, {all\_definitions}, {all\_formulas}, {text\_plan}, {applied\_bundles}, {tag\_instructions: SOURCE\_BACKED/RESEARCH\_REQUIRED/OPTIONAL\_ENRICHMENT/WEB\_SOURCED} | Formatted HTML with styled containers + traceability tags + IMAGE\_NEEDED markers | OFF | Screen 7 inline render → 7.2 (for each image marker) | Yes |



\### 7B. Image Generation (Function Chain)



| # | AI Call Name | Trigger | Input Data | Prompt Template (Stored) | Dynamic Injections | Output Format | Grounding | Feeds Into | User Editable? |

|---|---|---|---|---|---|---|---|---|---|

| 7.2 | \*\*Image Prompt Expansion\*\* | ALWAYS (chained after 7.1 image marker OR triggered mid-generation/validation) | Blueprint image description + surrounding text context + part subject + applied bundles + position info + creative guidelines | `imagePromptBuilder` | {image\_description}, {surrounding\_text}, {subject}, {applied\_bundles}, {position}, {creative\_guidelines: infographic/comic/formula-breakdown}, {mixed\_style\_support} | Detailed image prompt string + 3 recommended styles + reasoning | OFF | 7.3 | Yes (view + edit before regen) |

| 7.3 | \*\*Image Generation\*\* | ALWAYS (chained after 7.2) | Expanded prompt from 7.2 | Gemini native image generation API call (not text prompt template) | {expanded\_prompt} | Generated image (binary/base64) | N/A | Screen 7 inline display at specified position | Yes (regenerate with edited prompt or "different variation" instruction) |



\### 7C. Current Affairs



| # | AI Call Name | Trigger | Input Data | Prompt Template (Stored) | Dynamic Injections | Output Format | Grounding | Feeds Into | User Editable? |

|---|---|---|---|---|---|---|---|---|---|

| 7.4 | \*\*CA Search Execution\*\* | USER-TRIGGERED (Fetch CA button) OR ALWAYS (if Auto-Generate All clicked) | CA search queries from blueprint 5.1 + part topic + state focus setting | `currentAffairsPrompt` | {ca\_queries\[]}, {part\_topic}, {state\_focus}, {ca\_categories: national\_recent/national\_major/state\_recent/state\_major} | HTML CA boxes with WEB\_SOURCED tags + citation URLs | \*\*ON\*\* (Gemini grounding) | Screen 7 CA zone | Yes |



\### 7D. Bundle-Specific Deep Extraction (Runs During Text Generation)



| # | AI Call Name | Trigger | Input Data | Prompt Template (Stored) | Dynamic Injections | Output Format | Grounding | Feeds Into | User Editable? |

|---|---|---|---|---|---|---|---|---|---|

| 7.5 | \*\*Location Facts Extraction\*\* (context-driven) | CONDITIONAL (only if part contains locations) | Location name + content context (WHY location appears) + topic focus | `locationFactsPrompt` | {location\_name}, {content\_context}, {topic}, {relevance\_hint} | JSON: `{context\_specific\_facts\[], neighboring\_info?, map\_data?, ca\_relevance?}` (cached per location+context key) | OFF (unless CA relevance detected → ON) | Text generation output enrichment | Yes |

| 7.6 | \*\*Personality Facts Extraction\*\* (PSC-relevant) | CONDITIONAL (only if part contains persons) | Person name + PSC/exam context + current affairs relevance | `personalityFactsPrompt` | {person\_name}, {exam\_context}, {ca\_relevance\_flag} | JSON: `{psc\_relevant\_facts\[], contributions\[], recent\_news?}` (cached per person) | ON if CA relevance flag, else OFF | Text generation output enrichment | Yes |

| 7.7 | \*\*Formula Deep Operations\*\* | CONDITIONAL (only if part contains formulas) | Formula from analysis + variables + content context | `formulaOperationsPrompt` | {formula}, {variables}, {content\_context}, {applied\_bundles} | JSON: `{derivation\_steps\[], facts\[], operations\[], substitution\_examples\[], edge\_cases\[], common\_mistakes\[]}` | OFF | Text generation Formula Box container | Yes |



\### 7E. Highlight-to-Visualize



| # | AI Call Name | Trigger | Input Data | Prompt Template (Stored) | Dynamic Injections | Output Format | Grounding | Feeds Into | User Editable? |

|---|---|---|---|---|---|---|---|---|---|

| 7.8 | \*\*Visualize Selected Text\*\* (context-aware) | USER-TRIGGERED (highlight + Visualize This button) | Selected text + parent paragraph + part metadata (subject, bundles) | `visualizePromptBuilder` | {selected\_text}, {parent\_paragraph}, {part\_metadata}, {subject}, {applied\_bundles}, {35\_style\_catalog} | JSON: `{expanded\_prompt, recommended\_styles\[3], reasoning\_per\_style}` | OFF | Image generation popup → 7.2 → 7.3 | Yes |



\### 7F. Refinement Chat



| # | AI Call Name | Trigger | Input Data | Prompt Template (Stored) | Dynamic Injections | Output Format | Grounding | Feeds Into | User Editable? |

|---|---|---|---|---|---|---|---|---|---|

| 7.9 | \*\*Refinement Chat\*\* (smart scope) | USER-TRIGGERED (user types in refinement chat) | User message + current part text + surrounding context + part metadata + chat history | `refinementPrompt` | {user\_message}, {part\_text}, {surrounding\_context}, {part\_metadata}, {chat\_history} | JSON: `{affected\_sections\[], proposed\_edits\[], diff\_preview, scope\_detected}` | OFF | Screen 7 text update after user approves diff | Yes |



\### 7G. Add New Part



| # | AI Call Name | Trigger | Input Data | Prompt Template (Stored) | Dynamic Injections | Output Format | Grounding | Feeds Into | User Editable? |

|---|---|---|---|---|---|---|---|---|---|

| 7.10 | \*\*Quick Blueprint for New Part\*\* | USER-TRIGGERED (Add New Part → Generate Immediately) | User topic + sub-topics + global bundle selections + global CA toggle + auto-CA decision logic | `quickBlueprintPrompt` | {topic}, {sub\_topics}, {global\_bundles}, {ca\_decision: auto/on/off based on topic time markers} | JSON: same structure as 5.1 blueprint output | OFF | 7.1 (text generation for new part) | Yes |



\### 7H. Validation (Two Layers)



| # | AI Call Name | Trigger | Input Data | Prompt Template (Stored) | Dynamic Injections | Output Format | Grounding | Feeds Into | User Editable? |

|---|---|---|---|---|---|---|---|---|---|

| 7.11 | \*\*Per-Part Validation\*\* (single combined call) | ALWAYS (when user clicks Approve Part N) | Full part text + all part images with descriptions + part blueprint + source slice | `perPartValidationPrompt` | {part\_text}, {images\_with\_descriptions\[]}, {blueprint}, {source\_slice}, {part\_metadata} | JSON: `{summary: {text\_covered, images\_created, sources\_used, enrichments\_added}, issues\[], suggestions\[]}` | OFF | Validation popup (Approve Modifications / Ignore / Cancel) | Yes |

| 7.12 | \*\*Final Consolidated Validation\*\* (content-driven, cross-domain) | ALWAYS (auto after ALL parts approved) | ALL approved parts text + ALL images consolidated + subject + exam context + state focus | `finalConsolidatedValidationPrompt` | {consolidated\_document}, {consolidated\_images\_summary}, {subject}, {exam}, {state}, {cross\_domain\_check\_rules} | JSON: `{covered\_well\[], potential\_gaps\[], suggestions\_to\_add\[{type: new\_part/enrichment, detail}], priority\_per\_suggestion}` | OFF | Final validation popup → optionally triggers 7.10 for new parts | Yes |



\---



\## STAGE 8: EXPORT (Screen 8)



| # | AI Call Name | Trigger | Notes |

|---|---|---|---|

| — | \*\*NO AI\*\* | N/A | Pure formatting only. Compile approved text + embedded images + CA into HTML/PDF/Markdown/Clipboard. Copy formatted text + images option. Save as PDF via browser print. |



\---



\## SUMMARY STATISTICS



| Metric | Count |

|---|---|

| Total AI calls in system | 20 (numbered 1.1 through 7.12, excluding NO AI stages) |

| ALWAYS triggered | 11 |

| USER-TRIGGERED | 7 |

| CONDITIONAL | 5 (2.1, 2.2, 3.4, 7.5, 7.6, 7.7 — some overlap in conditional/always for bundle deep-dives) |

| Grounding ON | 2 always (7.4 CA) + 2 conditional (1.1, 1.2 if internet toggle) + 1 conditional (7.6 if CA relevance) |

| Grounding OFF | All others |

| Stages with NO AI | Stage 2 (technical extraction default), Stage 8 (export) |

| Parallel execution | 5.1 (blueprint per part with 1s gap), 3.3 (bundle detection combined) |

| Chained function calls | 7.1 → 7.2 → 7.3 (text → image prompt → image), 7.8 → 7.2 → 7.3 (visualize chain), 7.11 → 7.12 (validation chain) |



\---



\## PROMPT TEMPLATE INVENTORY (Stored in DEFAULT\_PROMPTS)



\*\*Universal Headers:\*\*

\- `UNIVERSAL\_HEADER` (Master Educational Content Engineer system prompt)

\- `universalBlueprintHeader`



\*\*Stage 1 (Method 2):\*\*

\- `subTopicExpansionPrompt`

\- `contentDraftPrompt`



\*\*Stage 2 (Failover):\*\*

\- `textCleanupPrompt`

\- `textRestructurePrompt`



\*\*Stage 3 (Analysis):\*\*

\- `subjectDetectionPrompt`

\- `deepExtractionPrompt` (+ subject variants)

\- 12 bundle-specific prompts (geography, personality, formulaOps, chartData, legal, timeline, storytelling, administration, process, code, medical, currentAffairsLayer)

\- `forceEnableBundlePrompt`



\*\*Stage 4:\*\*

\- `partSplittingPrompt`



\*\*Stage 5 (Blueprint — subject-routed via SUBJECT\_PROMPT\_MAP):\*\*

\- `economicsBlueprintPrompt`

\- `polityBlueprintPrompt`

\- `historyBlueprintPrompt`

\- `geographyBlueprintPrompt`

\- `scienceTechBlueprintPrompt`

\- `environmentBlueprintPrompt`

\- `socialIssuesBlueprintPrompt`

\- `mpSpecificBlueprintPrompt`

\- `currentAffairsBlueprintPrompt`



\*\*Stage 6:\*\*

\- `blueprintPartRefinementPrompt`



\*\*Stage 7 (Generation):\*\*

\- `partWriterPrompt` (+ subject variants like `economicsPartWriterPrompt`)

\- `imagePromptBuilder`

\- `currentAffairsPrompt`

\- `locationFactsPrompt`

\- `personalityFactsPrompt`

\- `formulaOperationsPrompt`

\- `visualizePromptBuilder`

\- `refinementPrompt`

\- `quickBlueprintPrompt`

\- `perPartValidationPrompt`

\- `finalConsolidatedValidationPrompt`



\*\*Total stored templates:\*\* \~40 (base + subject variants + bundle variants)



\---



\*\*Document 1 Complete.\*\*





