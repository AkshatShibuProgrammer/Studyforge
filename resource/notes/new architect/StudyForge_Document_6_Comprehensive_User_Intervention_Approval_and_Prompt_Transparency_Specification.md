# StudyForge — Document 6: Comprehensive User Intervention, Approval & Prompt Transparency Specification
## Every Point Where the User Can View, Edit, Approve, Reject, Regenerate, Override, Recover, or Export AI Work

> **Purpose:** This final document defines the human-control layer across the complete StudyForge pipeline. It ensures that AI assists the user but never silently takes irreversible product decisions.
>
> **Relationship to other documents:**
> - Document 1: which AI operations exist.
> - Document 2: how those operations depend on each other.
> - Document 3: exact prompt templates.
> - Document 4: runtime execution/retry/safety rules.
> - Document 5: product-document amendments/gaps.
>
> **Implementation instruction:** Canonical prompt text remains unchanged. This document controls UI actions, approval state, prompt visibility, user overrides, and resulting state transitions.

---

# 1. Human-Control Principles

| Principle | Mandatory product behavior |
|---|---|
| AI suggests; user decides | AI can propose scope, bundles, parts, blueprints, images, CA, edits and validation actions. The user can approve, edit, ignore, defer, or cancel. |
| No hidden prompt | Every AI request must expose the final task prompt used; system instruction is available through a read-only toggle. |
| No destructive silent regeneration | A change that can overwrite user text, blueprint work, images or approval must warn the user and identify scope. |
| Minimum friction where safe | Non-destructive defaults may run automatically: routed analysis, blueprint generation, image generation after approved plan, CA on Auto-Generate, etc. |
| Approval is meaningful | A part is not silently approved. Per-part validation offers user choices; Approve All is sequential, not invisible bulk approval. |
| User edits are first-class data | Manual edits are saved, protected outside intended AI scope, and reflected in stale/validation status. |
| Recovery stays available | Every failed AI call retains prompt, error context, retry/edit/skip/cancel actions. |
| Transparency without overload | Default prompt view shows final task prompt; system instructions remain available on demand. |

---

# 2. Global User-Control Matrix

| Stage | User can view/copy prompt | User can edit final prompt | User can change AI scope/settings | User can approve/ignore/cancel | User can regenerate | User-visible result/state |
|---|---:|---:|---:|---:|---:|---|
| Screen 1 upload/paste | Not applicable until AI used | N/A | Input method, settings | Continue/cancel | N/A | Canonical source preview |
| Screen 1 Method 2 scope | Yes | Yes for run | Topic, subtopics, depth, internet, CA | Approve proposed list/cancel | Re-run scope | Approved subtopic list |
| Screen 1 Method 2 draft | Yes | Yes for run | Approved list/depth/current options | Edit generated source/continue | Re-draft | Method 3 editable source |
| Screen 2 fallback | Yes | Yes for retry | Extraction method A/B/C | Retry/skip/cancel | Retry cleanup/restructure | Reader quality/diagnostic state |
| Screen 3 analysis | Yes | Yes for re-run | Bundles/features, manual subject if needed | Continue with selection | Reanalyse / force-enable | Counts, evidence, tiered bundles |
| Screen 4 split | Yes | Yes for re-run | Parts, ranges, title, merge/add/remove, part bundles | Accept/edit | Re-split | Confirmed part plan |
| Screen 5 blueprint | Yes per card | Yes for re-run | Per-part bundle chips/open detail | Approve/open detail | Retry failed part | Card status/progress |
| Screen 6 blueprint detail | Yes | Chat request is editable | Targeted blueprint section, styles, CA query | Undo/cancel targeted change | Regenerate target section | Updated/highlighted plan |
| Screen 7 generation | Yes per operation | Yes for re-run | Generate one/all, bundles if permitted | Retain/remove/continue | Regenerate part/image/CA | Draft notes/assets |
| Screen 7 images | Yes | Yes | Style, user direction, preview setting | Accept/remove | Same/different/edit prompt regen | Image asset at anchor |
| Screen 7 CA | Yes | Yes query | Fetch/refresh/omit/merge choice | Include or omit | Re-fetch | WEB_SOURCED result block |
| Screen 7 refinement | Yes | User request editable | Scope; selected patches | Apply all/selective/discard/expand | Re-run refinement | Diff preview + updated draft |
| Screen 7 validation | Yes | Yes for retry | Select suggestions | Apply/ignore/cancel | Revalidate | Validation summary/status |
| Screen 7 final validation | Yes | Yes for retry | Select final additions | Skip/apply/review each | Revalidate | Document readiness/gaps |
| Screen 8 export | No AI prompt | N/A | Format/include options | Confirm export | N/A | Copy/PDF document |

---

# 3. Prompt Visibility Specification

## 3.1 Prompt viewer standard component

Every AI operation uses the same prompt viewer component.

```text
┌──────────────────────────────────────────────────────────┐
│ 🔍 View AI Prompt                                         │
├──────────────────────────────────────────────────────────┤
│ Operation: AI-07A — Generate Part 2                      │
│ Status: Executed successfully / Failed / Cached           │
│ Model: configured model   Grounding: OFF                  │
│                                                            │
│ FINAL TASK PROMPT                                         │
│ [read-only / editable textarea for regeneration]          │
│                                                            │
│ [📋 Copy Prompt] [✏️ Edit for Regeneration]               │
│                                                            │
│ ▶ Show System Instructions                                │
│   [read-only system instruction]                           │
│                                                            │
│ Input references: Part P-02, pages 6–10, Blueprint v3    │
│ Prompt version: 1.0  Execution: EX-...                    │
└──────────────────────────────────────────────────────────┘
```

## 3.2 Prompt-viewer rules

| Requirement | Rule |
|---|---|
| Displayed prompt | It must be the saved final executed prompt, including runtime variable values and regeneration suffix. |
| Task prompt default | Display first, because it is understandable/editable by user. |
| System prompt | Read-only toggle; never hidden from users who want transparency. |
| Copy | Copies exact displayed prompt as text, not HTML markup. |
| Edit | Opens a per-execution draft; it never changes `DEFAULT_PROMPTS`. |
| Cached output | Viewer says Cached and links to original execution history. |
| Failed output | Viewer displays exact failed prompt and safe error reason. |
| Prompt safety | Prompt content goes in textarea/text node only; quotes/HTML-like text cannot break UI. |

## 3.3 Required prompt-viewer locations

| Location | Button/section | Operations visible |
|---|---|---|
| Screen 1 Method 2 | View Scope Prompt / View Draft Prompt | AI-01A, AI-01B |
| Screen 2 | View Extraction Prompt | AI-02A, AI-02B |
| Screen 3 | Analysis Prompts accordion | AI-03A, AI-03B, AI-03C, AI-03D |
| Screen 4 | View Splitting Prompt | AI-04 and guardrail factors |
| Screen 5 | View Blueprint Prompt per card | AI-05 target part |
| Screen 6 | Prompt/patch history | AI-06A, AI-06B |
| Screen 7 part | View Notes Prompt | AI-07A and CTX enrichment subcalls if separate |
| Screen 7 image | Show Prompt | AI-07B, AI-07C execution instruction |
| Screen 7 CA | View CA Prompt / Query | AI-07D |
| Screen 7 visualise/refine | View Visualize Prompt / View Refinement Prompt | AI-07F, AI-07G |
| Screen 7 validation | View Validation Prompt | AI-07H, AI-07I, AI-07K |
| Screen 7 Add Part | View Quick Blueprint Prompt | AI-07J |

---

# 4. Screen 1 Intervention Specification

## 4.1 Method 2 control flow

```text
User enters topic + 0–10 user subtopics + depth + optional internet/CA settings
  ↓
[AI Draft Text for This Topic]
  ↓
AI-01A result panel
  ↓
User checks/unchecks suggested topics; can add own topic
  ↓
[Approve & Generate] → AI-01B
  ↓
Draft inserts into Method 3 textarea
  ↓
User edits source, then Continue
```

## 4.2 Scope-approval panel requirements

| Item | Required behavior |
|---|---|
| User topics | Always marked mandatory/checked; cannot be silently omitted. |
| Essential suggestions | Checked by default; user can uncheck. |
| Optional suggestions | Unchecked by default unless user selects. |
| Current topics | Display source/date when grounded; user chooses inclusion. |
| Add custom | Adds an editable user item to final approved list. |
| Cancel | No draft is generated; original topic fields remain. |
| View prompt | Shows exact AI-01A request. |
| Re-run | Uses current topic/settings, not stale initial values. |

## 4.3 Draft review requirements

- Generated draft enters the same Method 3 editor used for pasted text.
- Character count updates.
- User can edit, remove, add or replace anything before continuing.
- The saved canonical source is the editor’s current value at Continue.
- If user selects Method 2, Screen 2 reading is skipped after source editing.

---

# 5. Screen 2 Intervention Specification

## 5.1 Extraction method controls

| UI control | Behavior |
|---|---|
| `Extraction Method: Auto` | Technical extraction then AI cleanup/restructure only when required. |
| `Technical Only` | No AI fallback; report quality issues to user. |
| `AI Cleanup` | Invoke AI-02A directly on extract. |
| `AI Restructure` | Invoke AI-02B directly where user chooses. |
| View diagnostic/prompt | Shows quality reason, selected method, actual prompt if AI used. |
| Retry/skip/cancel | Uses universal recovery modal; skip preserves best usable text with warning. |

## 5.2 User decision boundaries

- User may choose source method, but app must not enrich/alter factual content during extraction.
- Unresolved spans remain visibly marked in state for later transparency.
- User can manually replace/paste corrected source if all recovery attempts fail.

---

# 6. Screen 3 Intervention Specification

## 6.1 Analysis results layout

```text
Subject / Sub-discipline / Purpose
📚 19 topics • 20 definitions • 12 formulas • 4 PYQs • ...

Auto-enabled (green)        Suggested (yellow)       Show more (grey)
☑ Formula Derivation        ☐ Sensitivity Analysis   ☐ Medical Information
☑ Comparison Tables         ☐ Storytelling            ☐ Legal/Case Law
...

[View Analysis Prompts] [Reanalyse] [Fix Manually] [Continue]
```

## 6.2 User controls

| Control | State effect |
|---|---|
| Toggle auto-on feature off | Creates user override; later stages must honor it. |
| Toggle suggested on | Creates user selection; eligible parts inherit it. |
| Show More / force-enable | Opens/uses AI-03D only for chosen bundle. |
| Reanalyse | Marks old analysis stale and runs fresh pipeline; user confirms if existing downstream work would be affected. |
| Fix Manually | Allows manual subject/bundle setting when detection failed; does not fabricate signals. |
| Continue | Allowed without approving every suggestion; final selected state is saved. |

## 6.3 Evidence interaction

- Green/yellow/grey icon hover shows evidence such as page refs and count.
- No visible percentage values.
- Basic extraction counts remain separate from bundle-specific evidence/counts.

---

# 7. Screen 4 Intervention Specification

## 7.1 Part card controls

| Control | Behavior |
|---|---|
| View Splitting Prompt | Shows page guardrail, coherence rules, input refs and final AI-04 prompt. |
| Edit Settings | Opens actual modal, never a toast. |
| Add Part | Creates stable ID, inherits eligible bundles, marks new part for blueprint. |
| Merge | User selects parts; app combines scope/analysis and re-blueprints merged result. |
| Remove | Confirms removal and updates downstream progress/counts. |
| Bundle chips | User can see current applied bundles; change routes through stale blueprint logic. |
| Continue to Blueprint | Uses forward navigation and updates completed stage. |

## 7.2 Edit Settings modal

Required fields: title, page start/end, topic count, formula count, description, applied bundles; Save Changes and Cancel. Save updates state, re-renders card, and marks precisely affected downstream data stale.

---

# 8. Screens 5–6 Intervention Specification

## 8.1 Blueprint card grid

| User action | Result |
|---|---|
| Open card | Opens Screen 6 overlay/detail, never breaks overall navigation. |
| View AI prompt | Opens exact AI-05 prompt for that part. |
| Retry failed card | Retries that part only. |
| See progress | Queued/generating/ready/failed/retrying per part. |
| See bundles | Per-part chips show inherited/overridden bundle state. |

## 8.2 Blueprint detail edit controls

| Action | Required result |
|---|---|
| AI chat “Add more formulas” | AI-06A changes only relevant Text Plan formula items. |
| AI chat “Change comic to flowchart” | Changes only target image item. |
| Undo last change | Restores exact changed fields from payload. |
| Regenerate Image Plan Only | Uses AI-06B; locks other plan sections. |
| Edit CA query | Changes only query; no live search yet. |
| Change bundle chip | Updates blueprint target sections; warns if downstream output stale. |
| Full-scope instruction | Warning that full regeneration can lose manual edits; user confirms. |

---

# 9. Screen 7 Intervention Specification

## 9.1 Generation controls

| Control | Requirement |
|---|---|
| Generate Part | Generates selected valid non-stale part only. |
| Auto-Generate Part/All | Runs controlled part queue; triggers CA only when applicable/selected. |
| View notes prompt | Shows exact AI-07A plus any separately executed CTX calls. |
| Remove Part | Confirmation; updates part IDs/order/progress/final validation. |
| Add New Part | Topic/subtopic/CA modal; Generate Immediately or Configure Blueprint First. |
| Reopen approved part | Unlock to Edit returns part to draft/review and marks validation stale. |

## 9.2 Image controls

```text
[Generated Image]
[Show Prompt] [Regenerate] [Edit Prompt & Regen] [Different Style] [Remove]
```

- Default behavior: generated after prompt expansion without user pre-approval.
- Global Screen 1 setting can require image-prompt preview.
- `Regenerate` appends canonical different-variation instruction.
- User direction field supports “more comprehensive”, “artistic”, “simpler”, etc.
- Remove does not remove text; it marks validation stale if relevant.

## 9.3 CA controls

| Action | Requirement |
|---|---|
| View/edit query | User can edit blueprint-generated query before search. |
| Fetch CA | Runs grounded AI-07D. |
| Refresh CA | Re-runs query and replaces stale web facts only after validation/confirmation route. |
| Merge/omit result | User can include a result in part CA block or leave it out. |
| Verify source | URL/date/publisher is visible and clickable. |
| Grounding unavailable | User sees disclaimer and can skip/retry; no fake live fact. |

## 9.4 Highlight-to-visualize

1. User selects text.
2. Clicks Visualize This.
3. App collects selection + surrounding paragraph(s) + part metadata.
4. AI-07F returns one detailed prompt and exactly 3 styles/reasons.
5. User selects a style, edits prompt if wanted, then generates.
6. Similar existing images do not block action.

## 9.5 Refinement controls

```text
User message → AI scope/diff
[Apply All] [Apply Selective] [Discard] [Expand Scope to Whole Part]
```

- Local request modifies only identified anchors.
- Whole-part request requires warning and confirmation.
- Prompt/history and manual edits remain auditable.
- Current data request routes to CA rather than silently grounding refinement.

---

# 10. Approval and Validation Intervention Specification

## 10.1 Review controls and final approval

| UI state | Meaning |
|---|---|
| Pending | No complete draft yet |
| Generating | AI job active |
| Awaiting review | Text/images/CA generated; user reviews |
| Text reviewed | User checked text review control |
| Images reviewed | User checked image review control |
| Approve Part available | Required review controls complete; user can start validation/approval |
| Validating | AI-07H active |
| Approved | Text + included images + CA embedded as approved version |
| Unlocked/Edit | Approved content changed; return to review and validation state |

## 10.2 Per-part validation popup

```text
Part N Validation
- Summary: text covered, images, source scope, enrichments, web facts
- Checks: formula/fact/coverage/image/traceability status
- Issues and suggestions, each target/priority/actionable

[Cancel] [Approve Modifications] [Ignore & Approve As-Is]
```

- Cancel leaves draft unapproved.
- Approve Modifications applies only accepted targeted changes and then approves.
- Ignore approves as-is with suggestions discarded.
- Validation may propose text/container/image/CA actions, each routed correctly.

## 10.3 Approve All

```text
Approve All
 → Validate Part 1 of N → user decision
 → Validate Part 2 of N → user decision
 → ...
 → all remaining approved → final validation
```

- It never silently approves all parts.
- Cancellation stops remaining queue; previous approved parts remain approved.
- Progress is explicit.

## 10.4 Final validation popup

```text
Final Document Validation
Covered well: ...
Potential gaps: ...
Suggestions: Add Part / Enrich Part / Add Container / Add Visual

[Skip All] [Apply Selected Suggestions] [Review Each]
```

Accepted additions re-enter quick blueprint/generation/per-part validation and final validation repeats. Skip proceeds to export with current approved document.

---

# 11. Failure-Recovery Intervention Specification

| Error type | Automatic behavior | User options |
|---|---|---|
| Context/token | Prepare simplified context, preserve source/blueprint/IDs | Retry As-Is, Retry Simplified, Edit & Retry, Skip, Cancel |
| Rate limit | Wait ~30 seconds | Wait/retry, skip, cancel |
| Network | Wait/retry after reconnect if possible | Retry, skip, cancel |
| Safety | No automatic retry | Edit prompt, skip, cancel |
| JSON/schema | One format repair | Retry/edit/simplify/skip/cancel |
| Image failure | Preserve text and failed slot | Retry, different style, edit prompt, remove |
| CA failure | Preserve query/no false fact | Refresh/retry, omit, cancel |

### Failure modal requirements

- Exact failed final prompt is visible/editable.
- Safe human-readable error reason is shown.
- Successful sibling operations remain untouched.
- Skip affects only current bundle/part/image/query; never deletes completed work.
- User cancellation disables auto retry and retains valid pre-call state.

---

# 12. Resume, Persistence and Navigation Intervention Specification

## 12.1 Save/resume UI restoration

On resume, user-visible controls must match saved state:

- previous filename label where file bytes cannot be restored;
- selected method;
- topic and all dynamically created sub-topic fields;
- pasted/AI-drafted text;
- depth, exam, objective, state, CA/internet/image preview settings;
- selected bundles, part state, blueprints, generated content, approvals and current stage.

State restored internally but not reflected in UI is a failure of Save and Resume.

## 12.2 Navigation

| Action | Required function behavior |
|---|---|
| Forward valid action | `navigate(target)` updates max/completed state and renders target. |
| Back/sidebar | `navTo(target)` permits completed screen only and does not falsely advance state. |
| Screen 6 | Overlay/detail view, not independent forward stage. |
| Refresh/resume | Returns to saved stage only after UI is hydrated. |

---

# 13. Final User-Control Acceptance Checklist

- [ ] User can change/approve Method 2 scope before content draft.
- [ ] User edits draft/pasted source before it becomes canonical.
- [ ] User can select extraction strategy and recover failed extraction.
- [ ] User sees analysis counts/evidence and controls bundle selections.
- [ ] User edits parts in a real modal and controls part structure/bundles.
- [ ] User can inspect every actual final prompt and system instruction.
- [ ] User can modify blueprints surgically and undo last patch.
- [ ] User controls image prompt/style/regeneration and optional preview.
- [ ] User controls CA query/fetch/refresh/include behavior.
- [ ] User can refine notes through diff, not silent overwrite.
- [ ] User can add/remove parts during generation.
- [ ] User has meaningful per-part validation choices.
- [ ] Approve All validates sequentially with user decisions.
- [ ] User controls final-validation suggestions before new content is created.
- [ ] User can recover from every AI failure with prompt visibility.
- [ ] Resume restores visible fields and navigation works forward/backward.
- [ ] Export contains approved state only and uses no AI.

---

# 14. Document Validation Report

## 14.1 Validation method

This document was checked against the operation inventory (Document 1), dependency map (Document 2), canonical prompt library (Document 3), runtime rules (Document 4), and missing-feature register (Document 5).

## 14.2 Cross-document validation results

| Check | Result |
|---|---|
| All main AI operations AI-01A through AI-07K have a user/control or automatic-operation explanation | Pass |
| Deferred CTX-LOC, CTX-PER, CTX-FORM handling included | Pass |
| Every agreed prompt visibility point has a UI location | Pass |
| Method 2 approval/edit flow included | Pass |
| Three-tier Screen 3 controls and counts included | Pass |
| Screen 4 part-edit modal and navigation correction included | Pass |
| Blueprint chat/undo/section regeneration included | Pass |
| Image/CA/refinement/add-remove/validation Screen 7 controls included | Pass |
| Sequential Approve All and final validation loop included | Pass |
| Failure/retry, resume and export behavior included | Pass |

## 14.3 Independent-model validation limitation

This workspace does not provide a second independently callable AI model for a genuine external model review. Therefore I cannot honestly claim that a “different AI” has executed or approved this document. The validation above is a structured cross-document consistency check. When you provide access to another model/provider, send it this document together with Documents 1–5 and request a contradiction/coverage audit using the checklist in Section 13.

## End of Document 6

---

## Addendum — AI-07E Post-Text Image Gap Review Control

When conditional `AI-07E` runs after text generation, its missing-image suggestions must be shown to the user with description, learning reason, priority, recommended style and exact target anchor. The user can **Accept**, **Ignore**, or **Edit the request**. It must not silently create extra images. An accepted request enters the normal `AI-07B → AI-07C` chain; ignored suggestions do not affect approval.

---

# Amendment 1 — Reconciliation with Additional User-Control Matrix

The supplied additional control matrix adds concrete UI requirements. The following additions are mandatory and supplement, rather than replace, the main Document 6 sections.

## A. Blueprint approval controls (Screen 5/6)

| Control | Required behavior |
|---|---|
| Per-card blueprint approval | Each Screen 5 card offers **Approve This Blueprint** after review. |
| Master blueprint approval | `Approve All Blueprints` marks/reviews all currently ready blueprint cards; it must show part progress. |
| Unlock/edit blueprint | An approved blueprint can be reopened; changing it marks dependent generated output stale. |
| Screen 6 approve | `Approve this Part's Blueprint`, `Save Changes`, and `Back to Blueprint Cards` are explicit actions. |
| Detail layout | Screen 6 remains overlay: main area for headings/text/image/CA/validation plan, sticky side AI chat, bundle chips and section regeneration controls. |

## B. Stage 2 editable extraction preview

When AI cleanup/restructuring is used, Screen 2 includes an editable extracted-text preview before continuing. User corrections become canonical source. The extraction prompt template itself remains immutable; user edits the recovered text, not the stored template.

## C. Screen 3 concrete controls

Add the following visible actions:

- `Looks good → Continue` — Continue remains active; no forced feature approval gate.
- `See full details` — opens definitions/formulas/PYQ/table extraction detail tables with IDs/page refs.
- `Re-analyze` — reruns analysis after warning about existing downstream work.
- `Fix manually` — lets user set subject and bundles if AI analysis failed or is unsuitable.

## D. Screen 4 additional interaction

| UI item | Requirement |
|---|---|
| Drag-to-reorder parts | Reorder only affects presentation/order; scope and stable part IDs remain tracked. |
| Count override | User may override suggested part count by add/merge/remove, with range warning preserved. |
| Continue | `Continue to Blueprint` uses forward `navigate(5)`, never backward-only `navTo()`. |

## E. Screen 7 CA merge controls

Each returned CA result must provide:

- `Merge into notes` — adds result to default relevant CA container;
- `Merge at specific spot` — user selects a valid known content anchor;
- `Omit` — result remains unmerged and does not enter approval/export;
- timestamp and `Refresh CA` control.

Any merge or refresh marks the part validation state stale.

## F. Screen 7 validation suggestion controls

In addition to the overall validation choices, every individual suggestion must offer `Accept & Apply` and `Ignore` where action can be independently performed. The popup shows overall status (`Good`, `Needs Review`, `Poor`) and per-check results for formula, source facts, coverage, images and traceability when relevant.

## G. Screen 8 include controls and preview

Screen 8 must support a preview plus export options that may include/exclude, where relevant:

- traceability/source tags;
- current-affairs blocks;
- PYQ sections;
- images;
- blueprint/plan metadata only if the product explicitly permits it.

The product’s default final export is approved notes with embedded assets. Blueprint metadata must never be included accidentally. Export remains AI-free.

## H. Important reconciliation of terminology

The supplied matrix sometimes uses “edit prompt” to mean edit generated source/text. The final rule is:

- **Stored base/system prompt:** never end-user editable.
- **Final task prompt for a single regeneration:** editable through prompt viewer.
- **Generated source/text/blueprint/content:** editable through its screen-specific UI.

These are distinct controls and must not be implemented as one unsafe raw HTML editor.

## I. Open-item status correction

The supplied document lists model settings, schemas, caching and concrete prompt documents as open. In the final StudyForge document set those are already covered by:

- **Document 3:** exact canonical prompt texts, schemas and subject/bundle fragments;
- **Document 4:** model configuration, top-p/temperature, token budgets, caching, retry, cancellation, persistence, diagnostics and safety;
- **Document 5:** container and product-document amendment requirements.

Potential future product decisions not yet locked include exact CSS visual design/print styling and final user-facing microcopy. They are not missing AI architecture decisions.

## Amendment validation

This amendment adds every concrete control from the supplied matrix that was not explicit in Document 6: blueprint approval/master controls, editable recovery preview, Screen 3 detail/manual controls, drag reorder, CA merge-at-anchor, per-suggestion validation actions, and Screen 8 include/preview controls.

## End of Amendment 1
