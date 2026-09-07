# StudyForge — Document 5: Missing Features & Agreed Amendments Register
## Product-Document Update Register: User Demands, Developer-Discovered Gaps, and Decisions Agreed During Prompt Architecture Planning

> **Scope rule:** This register includes only: (1) user requirements stated in the discussions, (2) defects/gaps surfaced through actual developer work, and (3) items discussed and agreed for the StudyForge flow. It excludes speculative “nice-to-have” product ideas that were not accepted.

---

# 1. How to Use This Register

| Column | Meaning |
|---|---|
| Source | Where requirement came from: User, Developer-discovered, or Agreed design decision. |
| Priority | Blocking = flow cannot work correctly; Major = core capability/quality; Implementation = required technical support. |
| Product-document action | What must be added or clarified in original product document. |
| Related docs | Detailed design reference among Documents 1–4. |

---

# 2. Quick Comparison Table

| # | Missing/unclear in original plan | Final agreed requirement | Source | Priority | Stage |
|---:|---|---|---|---|---|
| 1 | Fixed/basic feature detection | Dynamic routed bundle detection based on actual source signals, with force-enable | User + agreed | Major | 3 |
| 2 | Static sub-topic field | Add/remove multiple user sub-topics and AI expansion/approval flow | User + dev gap | Major | 1 |
| 3 | AI Draft Text absent/unclear | Topic → related subtopics → user approval → full editable source draft → Method 3 | User + dev gap | Major | 1 |
| 4 | Save/resume vague | Resume must repopulate visible UI fields and state, not only internal data | Developer-discovered | Major | Cross-stage |
| 5 | Forward/back navigation unclear | `navigate()` advances/updates stage; `navTo()` only returns to completed stage | Developer-discovered | Blocking | Cross-stage |
| 6 | Screen 4 edit not specified | Real part-edit modal with title/range/count/description/bundles and save | Developer-discovered | Major | 4 |
| 7 | Prompt architecture not user-visible | Every actual executed prompt visible/copyable; task prompt editable per run; system toggle | User + dev gap | Major | All AI stages |
| 8 | Subject-only rules | Content-driven cross-domain logic; strategies are guidance only | User + agreed | Major | 3–7 |
| 9 | Location handling too simple | Context-driven location facts/maps/neighbours only when relevant to exact topic | User + agreed | 3, 7 |
| 10 | Personality handling too simple | PSC-relevant role/contribution/facts; CA through grounding only when needed | User + agreed | 3, 7 |
| 11 | Formula handling too simple | Formula operations: variable deep dive, relationships, derivation/examples/mistakes when relevant | User + agreed | 3, 7 |
| 12 | Image plan only upfront | AI can discover image need during text, post-review, and validation via one insertion chain | User + agreed | Major | 5, 7 |
| 13 | Image style choice unclear | AI smart default; user override; mixed visual composite if clear, split if cluttered | User + agreed | Major | 5–7 |
| 14 | CA timing unclear | Plan editable queries in blueprint; execute grounded search in Stage 7 only | User + agreed | Major | 5, 7 |
| 15 | Traceability only partly specified | Four explicit origins including `WEB_SOURCED:url`; preserve source/date/fetch time | Agreed | Major | 1, 7, 8 |
| 16 | Per-part bundle inheritance unclear | Global selection inherited only into evidence-relevant parts; per-part override | User + agreed | Major | 4–6 |
| 17 | Blueprint chat vague | Surgical patch, scope detection, diff/undo; section-only regenerate | User + agreed | Major | 6 |
| 18 | Screen 7 generation lacks precise data scope | Sliced source + scoped analysis + all definitions/formulas + blueprint/bundles | Agreed | Major | 7 |
| 19 | Add/remove parts only earlier | Screen 7 can remove part and add AI-created part via quick blueprint | User + dev gap | Major | 7 |
| 20 | Approval UI incomplete | Separate review controls plus Approve All; final part approval embeds text/images/CA together | User + dev gap | Major | 7 |
| 21 | Validation description incomplete | One per-part combined validation on approval; final cross-document validation after all approvals | User + agreed | Major | 7 |
| 22 | No safe output/anchor rules | Structured safe blocks, sanitized render, known anchors; prompt/quote safety | Developer-discovered | Blocking | 7, cross-stage |
| 23 | Retry generic | Exact prompt recovery, context simplification, rate/network/safety/schema classification | User + agreed | Major | All AI stages |
| 24 | Large source handling partial | Semantic chunking + structured merge/dedupe, not arbitrary samples | User + agreed | Major | 2–4 |
| 25 | Prompt settings/caching unspecified | Canonical settings, grounding, cache, telemetry, cancellation, persistence | Agreed | Implementation | Cross-stage |
| 26 | Export flow may imply further AI | Export is pure formatted approved state; copy formatted content/images and PDF | User | Major | 8 |

---

# 3. Detailed Amendment Register

## A. Screen 1 — Input and AI Draft

### A1. Dynamic sub-topic management

| Item | Requirement |
|---|---|
| Source | User requirement and developer-discovered missing UI behavior. |
| Product-document amendment | Method 2 must support multiple sub-topic fields (up to configured limit), add/remove controls, and user-created sub-topics. |
| AI flow | AI-01A sees user entries as mandatory; returns essential/optional additions; user checks/unchecks/adds before draft creation. |
| Acceptance criteria | User’s original topics remain included; AI cannot silently add scope; approved list is saved/restored. |
| Related docs | 1, 2, 3, 4 |

### A2. AI Draft Text multi-step flow

| Item | Requirement |
|---|---|
| Source | Explicit user decision. |
| Product-document amendment | Add: Topic → AI related-subtopic expansion → user approval → full source-like draft → Method 3 editable paste field. |
| Depth | Medium default; comprehensive optional. |
| Internet/current | Optional user flag; when on, scope and draft may use grounded web information with source metadata. |
| Downstream rule | User-edited Method 3 content becomes canonical source; Stage 2 reading is skipped for this path. |
| Acceptance criteria | Draft does not bypass user editing; final Stage 3 analysis uses edited text, not stale original draft. |

### A3. Source origin and canonical-source rule

| Item | Requirement |
|---|---|
| Product-document amendment | Define canonical source for upload, paste, and AI Draft paths. |
| Rule | Latest user-visible source after edits is what later analysis treats as source-backed. |
| Importance | Prevents source references and validation from referring to a version user has already changed. |

---

## B. Screen 2 — Reading and Large Sources

### B1. Extraction cascade

| Item | Requirement |
|---|---|
| Source | User decision. |
| Product-document amendment | Technical extraction is default. If it fails, automatically try AI cleanup; if inadequate, AI restructuring. User can select A/B/C manually. |
| AI constraints | Cleanup/restructure preserve source; no external enrichment; unresolved content is marked, never invented. |
| Acceptance criteria | OCR/encoding failure does not silently produce invented source content. |

### B2. Semantic chunking and structured merge

| Item | Requirement |
|---|---|
| Source | Agreed large-context solution. |
| Product-document amendment | When source exceeds safe context, split by chapters → headings → pages → paragraph groups, retain continuity metadata, analyze chunks, then merge/dedupe structured output. |
| Preserve | Topics, definitions, formulas, PYQs, timelines, tables, page references and uncertainty. |
| Do not use | Arbitrary truncation or first/middle/last sampling as substitute for complete semantic analysis. |

---

## C. Screen 3 — Dynamic Detection and Feature Bundles

### C1. Three-prompt hybrid, smart routing

| Item | Requirement |
|---|---|
| Product-document amendment | Define AI-03A signals, AI-03B deep extraction, AI-03C routed bundle analysis, AI-03D user force-enable. |
| Reason | Accuracy/cost balance: do not run all bundle prompts against every source. |
| UI | Green auto-on, yellow suggested, grey force-enable; evidence tooltips rather than numeric confidence. |
| Acceptance criteria | Bundle UI is connected from detection → state → part assignment → blueprint → generation/export, not cosmetic. |

### C2. New/expanded bundle categories

Add the following dynamic categories to original product documentation:

- Geography/locations/maps;
- personalities/contributions;
- formula operations/mathematics;
- charts/data/comparisons;
- legal/constitutional/case law;
- timelines/historical evolution;
- storytelling/analogy;
- institutions/administration;
- processes/creation;
- computer science/code/algorithms;
- medical/science;
- current-affairs relevance.

### C3. Context-driven locations

| Context | Allowed factual focus |
|---|---|
| History/civilisation | archaeological, historical, trade/cultural relevance |
| Economics | GSDP, industries, resources, relevant comparisons/policy |
| Geography | physical/political/economic geography needed by topic |
| Geopolitics | neighbours, borders, capitals, seas/passages, strategic relation when relevant |
| Current affairs | grounded current facts only |
| Passing mention | minimal directly relevant context; no generic fact dump |

### C4. Formula and personality enrichment

| Entity | Product-document amendment |
|---|---|
| Formula | Detect in Stage 3; deep operations only in Stage 7 for applied bundles. Include variables, relationships, derivation, examples, edge cases, mistakes only where relevant. |
| Personality | Detect name/role/context in Stage 3; create PSC/exam-relevant facts in Stage 7. Current news goes via CA grounding, never assumed fresh. |

---

## D. Screen 4 — Parts

### D1. Coherence-first split and editable modal

| Item | Requirement |
|---|---|
| Product-document amendment | Page-count range is guardrail; conceptual coherence wins. Warn if proposal lies outside range. |
| User edit modal | Must edit title, page start/end, topic/formula counts, description, and applied bundles; Save changes must update state/re-render. |
| Per-part bundles | Inherit global selected feature only where evidence supports it; user can override on Screen 5/6. |

### D2. Routing/navigation correction

| Issue | Required amendment |
|---|---|
| Dev-discovered blocker | Define forward and backward navigation APIs/semantics. |
| Rule | `navigate(next)` advances and updates completion/max screen. `navTo(existing)` is only for backwards/completed navigation. |
| Acceptance criteria | Screen 4, 5, 7 forward actions cannot be blocked by a max-screen guard. |

---

## E. Screens 5–6 — Blueprint

### E1. Parallel per-part blueprints

| Item | Requirement |
|---|---|
| Product-document amendment | One coherent blueprint prompt per part, launched staggered parallel (~1s) with isolated retry. |
| Output | headings, text plan, image plan, CA query plan, validation plan in one object. |
| Inputs | target source slice, scoped analysis, all definitions/formulas, part bundles and subject strategy. |

### E2. AI smart image defaults with override

| Item | Requirement |
|---|---|
| Rule | AI chooses image count/style based on learning objective; user can override. |
| Visual philosophy | Understanding over beauty; one composite may combine graph/table/flowchart when clear; split only when cluttered. |
| Blueprint image fields | title, anchor, learning goal, content, recommended style/reason, prompt seed/layout intent. |

### E3. CA plan vs execution

| Item | Requirement |
|---|---|
| Blueprint | Generates editable query strings only. |
| Generation | Executes only in Stage 7 via grounded search when user fetches or auto-generate applies. |
| Reason | Results stay fresh and no searches are wasted on removed/edited parts. |

### E4. Blueprint surgical editing and undo

| Item | Requirement |
|---|---|
| Product-document amendment | AI chat detects smallest affected scope and returns patch/diff; unrelated blueprint data remains unchanged. |
| User protection | Lightweight Undo Last Change. Section-only regeneration available. |
| Whole scope | “whole/entire/everything” requires warning because manual edits/other work may be affected. |

---

## F. Screen 7 — Generation, Images, CA, Refinement and Part Operations

### F1. Sliced source writing

| Item | Requirement |
|---|---|
| Product-document amendment | Per-part generation uses only target source slice + scoped analysis + active blueprint/bundles, while retaining all document definitions/formulas for cross-part reference. |
| Output | Structured safe blocks with source refs, tags, stable anchors and image-needed objects. |
| Safety | Renderer creates safe HTML; raw model HTML is never inserted directly. |

### F2. Unified dynamic image insertion chain

| Item | Requirement |
|---|---|
| Trigger moments | Blueprint, AI text generation, post-text image review, validation suggestion, user highlight. |
| Required chain | validate anchor → reserve slot → detailed image prompt → preview if setting on → image asset → attach to slot. |
| Placement | AI supplies stable location anchor; app validates anchor. |
| Regeneration | Same prompt + different-variation instruction, or edited prompt with change context. |

### F3. Grounded Current Affairs

| Item | Requirement |
|---|---|
| Product-document amendment | CA uses built-in Gemini grounding/search, with user-editable query and result URL/date/publisher/fetch time. |
| Fallback | If grounding unavailable, show explicit unavailable/training-data disclaimer; do not fabricate fresh sources. |
| Tag | `WEB_SOURCED:url`, visually distinct from source-backed content. |

### F4. Smart refinement and highlight-to-visualize

| Feature | Requirement |
|---|---|
| Refinement | AI infers scope, produces diff, preserves unrelated manual edits. UI: Apply All / Apply Selective / Discard / Expand Scope. |
| Highlight visual | Capture selected text + surrounding paragraph(s) + part metadata; return detailed prompt plus 3 style recommendations/reasons. Duplicate images are allowed. |

### F5. Dynamic add/remove parts on Screen 7

| Item | Requirement |
|---|---|
| Remove | Per-part remove button with confirmation; update part numbering, coverage and final validation. |
| Add | Topic + optional subtopics + CA choice → quick blueprint. Offer Generate Immediately or Configure Blueprint First. |
| CA decision | Use global CA setting; if off but topic includes recent/current/year cues, suggest CA rather than forcing it. |

### F6. Granular review and final approval

| Item | Requirement |
|---|---|
| Developer-discovered UI gap | Add separate review controls for text/images where required and master Approve All status/progress. |
| Final rule | On final Approve Part, text + included images + CA approve/embed together. |
| Approval count | Show complete approved-part progress. |

### F7. Two-layer AI validation

| Layer | Requirement |
|---|---|
| Per part | Single combined call on Approve Part: summary, checks, gaps, suggestions, possible image additions. User chooses Cancel / Apply / Ignore and Approve. |
| Approve All | Same popup sequentially for every part; never silently approves all. |
| Final | Runs after all non-removed parts approved; checks actual cross-domain content needs, suggests add/enrich actions. |
| Follow-up | User-approved new part uses quick blueprint → generation → validation → final validation again. |

---

## G. Export, Security, Reliability and Prompt Operations

### G1. Export

- No AI at export.
- Compile approved text, safe embedded images, CA blocks, traceability/citations.
- Required user options: copy formatted content/images and save/print PDF.
- If PDF fails, provide HTML fallback where implementation supports it.

### G2. Prompt visibility

Add product-document requirement: every AI operation has final prompt view/copy; user prompt editable for that next run; system instructions visible via read-only toggle. Viewer displays saved executed prompt, not reconstructed sample.

### G3. Safe rendering and quote escaping

| Gap | Required implementation amendment |
|---|---|
| User-edited prompts with quotes break HTML | Store/render prompt as textarea/text data, never inline attribute/unsafe HTML. |
| AI HTML/XSS risk | Validate JSON, whitelist container types, sanitize text/allowed markup, validate anchors. |
| Unsafe URLs | Permit only safe protocols and source metadata before web rendering. |

### G4. Runtime reliability requirements

- Retry: temporary failures 2s then 4s; context simplification; rate-limit wait; network reconnect; safety requires user action; schema repair once.
- Cache/context: semantic chunking, source/version-aware cache keys, entity+context cache for deferred enrichment, 24-hour CA freshness.
- Persistence: schema-versioned state saved after valid transitions; resume repopulates fields and visible UI.
- Cancellation: cancel queued/running/retry wait jobs without affecting successful siblings.
- Diagnostics: prompt/model/grounding/cache/token/latency/retry/error log in developer panel.

---

# 4. Documentation Insert Checklist

Add or revise the following sections in original StudyForge product document:

- [ ] Screen 1 Method 2 multi-step AI Draft and dynamic sub-topics.
- [ ] Canonical source and Stage 2 extraction cascade.
- [ ] Semantic chunking / structured merge.
- [ ] Stage 3 hybrid/routed bundle system with three tiers and force-enable.
- [ ] Full dynamic bundle catalog and deferred contextual enrichment.
- [ ] Page guide/coherence split plus real Screen 4 edit modal.
- [ ] Correct forward/back navigation behavior.
- [ ] Per-part bundle inheritance and override.
- [ ] One coherent five-section blueprint per part; parallel execution; surgical Screen 6 edits.
- [ ] Deferred grounded CA execution and four traceability labels.
- [ ] Sliced notes generation, safe structured rendering and stable anchors.
- [ ] Unified image discovery/insertion chain and user style/prompt controls.
- [ ] Screen 7 add/remove parts, refinement and highlight visual features.
- [ ] Granular review plus two-layer validation/approval loop.
- [ ] Prompt visibility/copy/edit requirements for all AI actions.
- [ ] Retry/caching/persistence/cancellation/diagnostics rules.
- [ ] Export is no-AI approved-state formatting only.

## End of Document 5

---

# Appendix A — Full Requirement-by-Requirement Product-Document Amendment Specification

This appendix expands every register item into wording/behavior that can be inserted into the main product document. It is intentionally detailed so no requirement is reduced to a short label.

## A.1 Prompt architecture and transparency

### Requirement
The product document must state that StudyForge stores reusable system instructions, templates, bundle fragments, subject strategy fragments and prompt-generation rules—not prewritten final prompts for every subject. The application builds a fresh final prompt from current source/part/blueprint data every time an AI operation runs.

### Required behavior

1. The stored canonical template remains read-only to end users.
2. The application stores the exact **final executed** system and task prompt, with injected values, before every model request.
3. Every prompt viewer must show the final task prompt, allow copy, and offer a read-only “Show System Instructions” toggle.
4. For regeneration, user may edit the final current-run prompt. This creates a new prompt execution; it must not mutate the stored template.
5. A developer cannot show a generic/sample prompt while sending a different hidden prompt. Prompt history is the source of truth.
6. Prompt history must identify operation ID, template version, input references, grounding/model settings, response reference, retry status and errors.

### Screens affected
Screen 1 (AI Draft), Screen 2 (AI fallback), Screen 3 (analysis), Screen 4 (split), Screen 5/6 (blueprint), Screen 7 (notes/images/CA/refinement/validation/add part).

---

## A.2 Dynamic feature detection is not a fixed toggle list

### Requirement
Screen 3 must analyze actual content, identify signals, route only relevant bundles, show evidence, and preserve user ability to force-enable skipped bundles. It must not behave as a fixed generic list of 12 feature switches.

### Required hybrid chain

1. **Subject/signal detection:** determines primary subject, sub-discipline, content purpose, cross-domain aspects and evidence signals.
2. **Deep extraction:** builds reusable IDs for topics, definitions, formulas, key facts, PYQs, comparisons, examples, timelines, tables, diagrams, locations, people, legal references and processes.
3. **Smart bundle detection:** deterministic routing selects only relevant bundle fragments; AI returns evidence and feature tier.
4. **Force-enable:** user can request a skipped bundle; only that selected bundle is scanned.

### UI decision

| Tier | Visual | Default | Meaning |
|---|---|---|---|
| Strong | Green | On | Direct strong source evidence; safe automatic default |
| Medium | Yellow | Off but visible | Possible/useful; user chooses |
| Not detected | Grey / Show More | Off | Not supported now, but user may force-enable |

Do not show arbitrary percentages. Hover should show the actual reason/evidence.

---

## A.3 Geography, location and map behavior

### Requirement
When a location appears, StudyForge does not automatically show generic facts. It determines why the location matters to the exact part and fetches/generates only useful context.

### Required context matrix

| Part context | Relevant location output | Must avoid |
|---|---|---|
| Indus Valley/history | sites, artefacts, historical routes, cultural/archaeological relevance | unrelated current CM/GDP/schemes |
| Economics | GSDP, industries, resources, policy/data/comparison relevance | unrelated historical trivia |
| Geography | rivers, relief, climate, resources, political/economic geography | generic biography/personality content |
| Geopolitics | borders, neighbours, capitals, sea/strait/passage, strategic relation where relevant | map facts with no learning purpose |
| Current Affairs | grounded current facts with URL/date | unverified “latest” claims |
| Passing mention | minimal direct context only | fact dumping |

### Timing
Screen 3 records name, context, frequency/page refs. Stage 7 performs `CTX-LOC` only if part relevance and selected bundle justify it. Current facts are routed to AI-07D grounding.

---

## A.4 Personalities and formulas

### Personalities

- Screen 3 detects person, role, source context and relevance.
- Stage 7 creates concise exam/PSC-oriented context: contribution, theory/work, award/publication/institution where relevant, related people and quick revision value.
- Personal/private details are excluded unless exam-relevant.
- Recent news is never generated from memory; it is requested through grounded CA research only.

### Formulas

- Screen 3 extracts exact formula, variables, nearby purpose and page refs.
- Stage 7 Formula Operations can provide variable inclusion/exclusion, derivation/relationships, illustrative substitution, edge cases, common mistakes, related formulas and visual need only if selected/relevant.
- Real figures/current data/exam PYQs cannot be invented. Any real current fact must be web-sourced; teaching examples must be marked enrichment.

---

## A.5 Parts and blueprint requirements

### Part splitting

The documentation must explicitly say that page ranges give an expected range, but conceptual coherence is more important. Formula/explanation, PYQ/topic, example/concept and tightly related sections stay together. A proposal outside range is allowed with a warning and user confirmation.

### Real part editing

The “Edit Settings” action must open an actual modal, not a disappearing toast. The modal supports title, page range, topic/formula count, description and applied bundle chips. Saving updates state and makes downstream blueprint/output stale only where needed.

### Blueprint output

A part blueprint is a single coherent plan containing:

1. ordered headings and teaching purpose;
2. text/container plan with source and analysis references;
3. image plan with learning goal, anchor, recommended style/reason and layout intent;
4. editable CA query plan, not live results;
5. content-driven validation plan.

Blueprint calls run once per part with staggered parallel execution; a failure in one part must not destroy successful blueprints.

---

## A.6 Image philosophy and dynamic image creation

### Core requirement
Images are for understanding difficult material, not decoration. A visual should make the learner understand a process, formula, comparison, story, map, trend, cycle or algorithm more clearly.

### Styles and composite rule

- AI recommends style based on content: formula → breakdown/pictograph; comparison → matrix; process → flowchart; narrative → comic; trend → graph/data insight; place relation → labelled map.
- A single visual can combine graph, table and flowchart sections where that produces one clear teaching artifact.
- If one visual would be cluttered, AI returns multiple focused requests and explains split reason.
- User can override style, edit prompt, choose different variation, or request preview-before-generation globally.

### Unified insertion chain

Images may originate in blueprint, notes generation, post-text review, validation or highlight-to-visualize. All paths must use exactly one chain: validate known anchor → reserve slot → build detailed prompt → optional preview → generate asset → insert asset → save metadata.

---

## A.7 Current affairs and web-source requirements

1. Blueprint stage generates editable search strings only.
2. Stage 7 executes fresh search using Gemini grounding when user fetches CA or auto-generation makes it applicable.
3. Each accepted grounded result needs claim, relevance, URL, publisher/source if available, fact date and fetch timestamp.
4. CA uses `WEB_SOURCED:url`, never `SOURCE_BACKED`.
5. If grounding is unavailable, show clear status/disclaimer; do not make a false fresh-data claim.
6. Current affairs is time-sensitive: cache for a short period and offer refresh.

---

## A.8 Screen 7 additions and approval logic

### Dynamic parts

Screen 7 must permit removal of generated part and addition of a new topic. Add Part offers:

- Topic and optional subtopics;
- CA choice;
- Generate Immediately (quick blueprint then generation);
- Configure Blueprint First (Screen 6-style editing);
- automatic CA suggestion for time-sensitive topic markers when global CA is off.

### Refinement

Natural language refinement detects scope and returns visible before/after diff. User chooses Apply All, Apply Selective, Discard, or Expand Scope. Whole-part requests require warning about manual edits.

### Per-part approval

Review controls can separately indicate text/image review, but final approval embeds all included text, image and CA assets together. Master Approve All is sequential validation, never silent bulk approval.

---

## A.9 Validation requirement detail

### Per-part validation

When Approve Part is clicked, send current notes, image descriptions, CA, source slice, blueprint, tags and applied bundles in **one** validation call. Return summary, factual/source checks, coverage/image/traceability issues, actionable suggestions and suggested images with anchors.

### Final validation

After all non-removed parts are approved, evaluate whole approved document. It must be content-driven rather than a subject-only checklist. For cross-domain topic, check relevant formulas, law, timeline, maps, comparisons, persons, processes, data and CA where supported. User may skip, review each, or apply selected suggestions. Accepted new parts re-enter quick-blueprint → generation → validation → final-validation loop.

---

## A.10 Reliability, safety, persistence and navigation

### Navigation

Forward navigation updates completion state. Back navigation accesses completed screens only. No valid forward action can be blocked merely because max-screen was not updated.

### Recovery

- temporary error: retries 2s/4s;
- context limit: preserve core input and offer simplified retry;
- rate limit: wait/retry;
- network: reconnect/retry;
- safety: user edit/skip/cancel;
- invalid JSON/schema: one controlled repair then full recovery modal.

### Persistence

Save validated state after each transition and restore visible field values on resume. Persist source, analysis, bundles, parts, blueprints, outputs, approvals and prompt metadata with schema versioning.

### Safe rendering

Text/prompt values are rendered as text/textarea data. AI output is parsed and schema-checked before rendering. Anchor/container/URL validation is mandatory. This prevents the discovered quote and HTML escaping failures.

---

# Appendix B — Developer-Discovered Defect Closure Checklist

| Defect/gap observed | Required proof of closure |
|---|---|
| Screens 4/5/7 forward navigation locked | Manual walkthrough reaches next valid screen using forward navigation functions. |
| Edit Settings was toast only | Modal supports fields, saves state, re-renders part. |
| Prompts hidden/fake | Viewer shows exact saved final execution record for each operation. |
| Granular approval absent | Review controls/master progress work; final Approval rules correctly embed assets. |
| Validation button had no workflow | Loading → AI result popup → apply/ignore/cancel modifies state as designed. |
| Cannot add/remove parts in generation | Remove confirmation/state update; Add Part quick blueprint flow works. |
| Screen 3 counts missing | Counts derive from deepAnalysis and display separately from bundle evidence. |
| AI Draft feature dropped | Method 2 creates and inserts editable draft into Method 3. |
| New Screen 4 part lost bundle state | Added part receives eligible inherited bundles and displays them in Screen 5/6. |
| Prompt quotes break page | Prompt stored/rendered safely; test quotes/HTML-like strings without breakage. |

## End of expanded Document 5 appendix

---

# Amendment 2 — Full Gap Matrix Reconciled Against the Additional Supplied Document

The additional supplied gap-analysis document contains substantially more concrete UI, priority, timing, prompt, and developer-verification detail than the earlier register. The following full matrix is added so none of those decisions are reduced to a brief summary.

## A. Complete original-doc versus actual-requirement matrix

| # | Area | Required product-document addition / clarification | Source | Priority |
|---:|---|---|---|---|
| 1 | Method 2 scope | Two steps: AI expands related topics; user approves/edits; only then content is drafted. | Lead | Blocking |
| 2 | Method 2 internet | Internet toggle applies to **both** expansion and content-draft prompts. | Lead | Major |
| 3 | Method 2 depth | Medium default (~8k words) and comprehensive option (~15k words) as user setting. | Lead | Major |
| 4 | Method 2 CA | Separate CA inclusion toggle at Method 2, distinct from internet toggle. | Lead | Minor |
| 5 | AI Draft control | Visible AI Draft Text button triggers expand → approve → generate → Method 3 flow. | Lead/dev | Blocking |
| 6 | Sub-topic inputs | Dynamic separate fields, up to 10, with add/remove and count. | Developer | Major |
| 7 | Reading cascade | A technical extraction → B AI cleanup → C AI restructure; user can force A/B/C. | Lead | Blocking |
| 8 | AI draft reading | AI Draft path skips Screen 2 and goes directly to Screen 3 after Method 3 edit. | Lead | Minor |
| 9 | Analysis architecture | Hybrid: AI-03A signals → AI-03B deep extraction → AI-03C routed bundle analysis. | Lead | Blocking |
| 10 | Feature tiers | Green auto-on, yellow suggested, grey force-enable/show-more—not binary toggles. | Lead | Major |
| 11 | Confidence UI | Visual icons and evidence hover; no numeric percentages. | Lead | Minor |
| 12 | Location facts | Context-driven facts, not fixed generic location facts. | Lead | Blocking |
| 13 | Neighbour logic | Countries/states can include relevant neighbours, capitals, seas/passages and strategic significance. | Lead | Major |
| 14 | Location timing | Stage 3 detects name/context/pages; Stage 7 fetches deep contextual facts and caches entity+context. | Lead | Major |
| 15 | International handling | Same contextual logic for domestic/international; no forced India angle. | Lead | Major |
| 16 | Formula depth | Stage 3 formula detection; Stage 7 derivation, variables, substitutions, relationships, edge cases, applications/mistakes. | Lead | Blocking |
| 17 | People depth | PSC/UPSC-focused contribution/facts/current relevance, not generic bio. | Lead | Major |
| 18 | Split table | Page table is a guardrail; coherence has priority; outside-range warning and user final choice. | Lead | Major |
| 19 | Split input | Deep analysis primary; full source only if safe; otherwise topic summaries. | Lead | Major |
| 20 | Part bundles | Global feature inheritance only where relevant; per-part chips/override. | Lead | Major |
| 21 | Blueprints | One blueprint call per part in staggered parallel, isolated retry/progress. | Lead | Major |
| 22 | Blueprint object | One coherent call returns headings, text plan, image plan, CA plan and validation plan; one-section regenerate exists. | Lead | Blocking |
| 23 | Style defaults | AI recommends style from content and explains reason; user dropdown override. | Lead | Major |
| 24 | CA timing | Blueprint plans queries; Stage 7 executes fresh fetch; auto-generate may execute. | Lead | Major |
| 25 | Blueprint chat | Targeted patch only, changed-section highlight, lightweight undo, full-scope warning. | Lead | Major |
| 26 | Generation input | Target source slice + scoped analysis + all definitions/formulas + blueprint + part bundles. | Lead | Blocking |
| 27 | Generated output | Properly formatted safe structured content rendered as styled containers; final approval embeds text/images/CA. | Lead | Blocking |
| 28 | Image prompt flow | Image brief → detailed prompt → immediate generate by default; view/edit/regenerate; global preview option. | Lead | Major |
| 29 | CA mechanism | Gemini grounding/search; fallback status/disclaimer if unavailable; no external API key. | Lead | Blocking |
| 30 | Validation layers | One combined per-part validation plus final consolidated validation. | Lead | Blocking |
| 31 | Validation scope | Cross-domain/content-driven validation, not subject-locked. | Lead | Major |
| 32 | Approve All | Sequential popup for every part, visible `Part X of Y`, preserves previous approvals if stopped. | Lead | Major |
| 33 | Refinement | Smart scope detection and visible diff; Apply All/Selective/Discard/Expand Scope. | Lead | Major |
| 34 | Visualize context | Selected text + parent/surrounding paragraphs + part/bundles/subject; exactly three style recommendations. | Lead | Major |
| 35 | Duplicate visuals | Do not block potentially similar visual requests. | Lead | Minor |
| 36 | Screen 7 parts | Remove Part confirmation and Add New Part quick-blueprint/configure-first path. | Lead/dev | Major |
| 37 | Export | No AI at export; approved formatted content/images/CA → copy/PDF. | Lead | Minor |
| 38 | Error popup | Show error details and editable executed prompt with As-Is/Simplified/Edited/Skip/Cancel. | Lead | Blocking |
| 39 | Large documents | Semantic chunking at natural boundaries with continuity and structured merge. | Lead | Major |
| 40 | Prompt views | Final task prompt default; read-only system prompt toggle; copy and per-run edit. | Lead | Major |
| 41 | Dynamic images | During writing, post-review and validation image discovery use one common insertion chain. | Lead | Blocking |
| 42 | Mixed visuals | Combine graph/table/flow/process in one clear composite; split only if clarity requires. | Lead | Major |
| 43 | Image philosophy | Teach/clarify first; infographic/comic/formula/metric/fact visual preference; labels/legends/annotations. | Lead | Major |
| 44 | Regeneration | Same prompt + different-variation instruction + optional comprehensive/artistic/simpler direction. | Lead | Minor |
| 45 | Edited regen | Original + edited prompt + change/diff context sent with unchanged canonical system rules. | Lead | Minor |
| 46 | Cross-part formula | Structured formula record is passed across parts; writer chooses full/reference presentation. | Lead | Major |
| 47 | Analysis slicing | All definitions/formulas global; PYQs/examples/timelines/etc. strict scoped unless referenced. | Lead | Major |
| 48 | Grounding scope | ON only for explicit Method 2 internet mode and AI-07D CA; OFF source work. | Lead | Blocking |
| 49 | Web tag | Purple `WEB_SOURCED:url`, clickable citation, distinct from source/inference/enrichment. | Lead | Major |
| 50 | Prompt storage | Inline `DEFAULT_PROMPTS`, strategies/rules/placeholder builder, `SUBJECT_PROMPT_MAP`; only final runs editable. | Lead | Blocking |
| 51 | Resume UI | Saved values must repopulate visible Screen 1 fields/settings/sub-topic inputs/paste field. | Developer | Blocking |
| 52 | Navigation | Forward `navigate()` updates stage; backward `navTo()` only opens completed screen. | Developer | Blocking |
| 53 | Part modal | Real Screen 4 edit modal: title, range, counts, description, bundle chips, Save/Cancel. | Developer | Major |
| 54 | Prompt buttons | Concrete View Prompt affordance at analysis, split, blueprint, notes, images, CA and validation. | Lead/dev | Blocking |
| 55 | Approval checks | Per-part Approve Text and Approve Images review controls, master button/progress; final approval embeds all assets. | Developer | Major |
| 56 | Validation UI | Loading, overall status, formula/fact/image/coverage results, per-suggestion apply/ignore, close. | Developer | Major |
| 57 | Screen 7 remove | Remove button confirms, reindexes, updates sidebar/progress/final validation. | Developer | Major |
| 58 | Screen 7 add | Add New Part inputs, CA toggle/auto decision, inherited bundles, generation action. | Developer | Major |
| 59 | Summary counts | Separate Screen 3 row: topics, definitions, formulas, PYQs, diagrams, comparisons, examples, timelines, tables. | Developer | Minor |
| 60 | Containers | Add location, bio, data, formula ops, institution, CA, analogy, process, experiment and medical containers. | Developer | Major |
| 61 | Escaping | Prompt/user content safe text rendering; generated blocks sanitized/allowlisted; quote test mandatory. | Developer | Blocking |
| 62 | Bundle sync | New/edited part preserves `applied_bundles` and chips across Screen 4→5→6→7. | Developer | Major |
| 63 | Trigger taxonomy | Explicit Always/User-triggered/Conditional classification for all calls and subcalls. | Lead | Major |

## B. Exact UI additions that must be inserted into product documentation

### Screen 1 controls

- Dynamic sub-topic list with `+ Add Sub-topic`, `Remove`, `x of 10` counter.
- `Depth: Medium / Comprehensive` selector.
- `Search internet for this topic` toggle.
- `Include Current Affairs for this topic` toggle.
- `AI Draft Text for This Topic` button with actual staged progress: **Expanding topics** → user approval panel → **Generating content**.

### Screen 3 controls

- Separate counts row: `📚 topics • definitions • formulas • PYQs • diagrams • comparisons • examples • timelines • tables`.
- Three-tier bundles with evidence tooltip.
- Show More/force-enable action.
- Reanalyse/fix manually action where analysis is unavailable.
- View Analysis Prompts viewer for actual AI-03A/03B/03C/03D runs.

### Screen 4 controls

- View Splitting Prompt and factors.
- Page-guide deviation warning.
- Actual Edit Settings modal, not toast.
- Bundle chips and per-part assignment state.
- Add/merge/remove actions update state and downstream stale flags.

### Screen 5/6 controls

- Per-card actual final blueprint prompt viewer.
- Per-card queued/generating/ready/failed progress.
- Per-part bundle chips.
- Full-screen? No: Screen 6 remains overlay/detail view.
- Surgical AI chat, change highlight and Undo Last Change.
- Section-only regeneration buttons, especially Image Plan.

### Screen 7 controls

- Generate Part / Auto-Generate Part / Auto-Generate All.
- View generated note prompt, every image prompt, CA prompt/query and validation prompt.
- Image controls: Show Prompt, Regenerate, Edit Prompt & Regen, Different Style, Preview setting behavior.
- Fetch CA and Refresh CA with URL/date display.
- Highlight + Visualize This popup with three style choices.
- Refinement chat with diff controls.
- Add New Part and Remove Part actions.
- Approve Text / Approve Images review checks; Approve Part; master Approve All progress.
- Per-part validation popup and final validation popup.

## C. Exact additional container specification

| Container | Minimum required content | Used by |
|---|---|---|
| Geography/Location Box | location title, context facts, map/reference where relevant | CTX-LOC / geography bundle |
| Personality Bio Card | name, role, contributions, relevant facts/CA link | CTX-PER |
| Data Insight Box | highlighted metric, data context, source/tag | chart/data bundle |
| Formula Operations Box | formula, variables, operations/derivation/mistakes | CTX-FORM |
| Institution/Admin Box | body, role, function/structure/reform | administration bundle |
| Current Affairs Box | date, fact, relevance, clickable WEB source | AI-07D |
| Analogy Box | “Think of it like…” clarification, enrichment tag | storytelling |
| Process/Creation Box | inputs, numbered steps, output/flow | process bundle |
| Experiment Box | hypothesis, method, observation, result | science |
| Medical Info Box | relevant symptom/diagnosis/treatment/process relationship | medical |

Every container requires CSS, a safe renderer template, allowed container enum, export handling, and prompt/blueprint selection rule.

## D. Priority reconciliation

The supplied document labels 18 items blocking, 29 major and 7 minor, while its detailed table uses both “missing”, “underspecified”, “developer bug” and “architecture” labels. The implementation must use **blocking vs major vs minor** only for delivery sequencing; no listed item is to be discarded as optional without explicit lead decision.

## E. Amendment validation

This amendment was compared against the preceding Document 5 text. It adds the previously under-detailed Method 2 controls, explicit Screen 3 counts, detailed containers, concrete Screen 7 UI controls, exact 63-item matrix, priority reconciliation, and all stated developer defect closures.

## End of Amendment 2
