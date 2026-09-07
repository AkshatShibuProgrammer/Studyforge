# StudyForge — UI Alignment Gate
## UI Must Match Approved Architecture Before Prompt Integration or Functional Code Changes

> **Lead instruction:** First align the existing skeleton UI to the approved StudyForge documents. Do not add/replace Gemini prompt calls, fake AI results, placeholder AI behavior, or downstream functionality until the relevant UI phase is aligned and approved.

---

# 1. Build Order Rule

For every stage, use this sequence:

```text
1. Align static UI with approved documents
2. Verify all required controls, states, modals, labels and empty/loading areas exist
3. Freeze the visual structure for that stage
4. Add canonical prompt wiring
5. Add real Gemini calls and state updates
6. Test the real route
```

Never use a static/dummy example as a replacement for missing real functionality. If a UI area is not implemented yet, show an honest empty or planned state.

---

# 2. Global UI Alignment Rules

| Rule | Required behavior |
|---|---|
| Skeleton look and feel | Preserve existing visual design, Tailwind layout, cards, sidebar, progress areas, overlay style and container styling. |
| No hardcoded study subject | Do not show National Income/Economics/MP/Amartya Sen/GDP sample content as live user results. Use neutral empty/loading states before real data arrives. |
| Loading UI | Every future AI operation needs a visible target loading/status area before prompts are wired. |
| Prompt UI | Every future AI operation needs a View Prompt location, but until code exists it must say `No executed prompt yet`, not display fake prompt text. |
| Button honesty | A button may exist only if it has a defined future action. Before its phase implementation, show disabled state/`Available in next phase` rather than fake toast success. |
| Empty states | Use clear empty-state language: `No analysis yet`, `Generate blueprint first`, `No approved parts yet`. |
| UI state source | UI must eventually render from state; do not hardcode sample counts/parts/cards/content. |

---

# 3. Screen 1 UI Alignment Checklist

## Required static UI before Stage 1 prompt wiring

- [ ] Method 1 Upload card.
- [ ] Method 2 Topic card.
- [ ] Method 3 Paste Text card.
- [ ] Dynamic sub-topic rows with Add and Remove controls.
- [ ] Main topic and optional focus field.
- [ ] Depth selector: Medium / Comprehensive.
- [ ] Separate Internet Search checkbox.
- [ ] Separate Include Current Affairs checkbox.
- [ ] Preview Image Prompts checkbox.
- [ ] Target Exam, Objective and State Focus inputs.
- [ ] AI Draft button with correct safe label, no corrupted `??` characters.
- [ ] Scope panel area, hidden until real AI-01A result exists.
- [ ] Scope panel supports mandatory/essential/optional/custom sections.
- [ ] Method 3 source textarea and character counter.
- [ ] Image upload/paste-image area/preview placeholder if image input is part of approved Phase 2 scope.
- [ ] Continue button.
- [ ] Stage 1 prompt viewer location.
- [ ] Stage 1 loading/progress area.
- [ ] Stage 1 error/recovery modal location.

## Must remove/replace visually

```text
?? AI Draft
fake Auto-Write generated text
sample success toasts claiming AI work completed
```

---

# 4. Screen 2 UI Alignment Checklist

- [ ] Reading title and real progress list structure.
- [ ] Status labels for file accepted, technical extraction, image/OCR check, quality check, source ready.
- [ ] Progress bar.
- [ ] Extraction method selector: Auto / Technical / AI Cleanup / AI Restructure.
- [ ] Quality status card: usable / partially usable / unusable.
- [ ] Reason list area.
- [ ] Editable recovered text preview.
- [ ] Unresolved/uncertain source segment area.
- [ ] AI Cleanup button.
- [ ] AI Restructure button.
- [ ] Confirm & Use button.
- [ ] Re-upload/Paste Text fallback action.
- [ ] View executed prompt location for AI-02A/AI-02B.
- [ ] No static fake “extracted X pages” data before real extraction.

---

# 5. Screen 3 UI Alignment Checklist

- [ ] Neutral subject/purpose loading state before analysis.
- [ ] Subject and purpose result header.
- [ ] Separate actual analysis counts row.
- [ ] Full-details expandable area with empty tables before analysis.
- [ ] Three-tier bundle sections:
  - green auto-enabled;
  - yellow suggested;
  - grey/show-more force-enable.
- [ ] Evidence tooltip/description area.
- [ ] Re-analyze button.
- [ ] Fix Manually action.
- [ ] Looks Good → Continue action.
- [ ] Analysis prompt accordion for AI-03A/B/C/D.
- [ ] No static National Income definitions/formulas/PYQs/counts.

---

# 6. Screen 4 UI Alignment Checklist

- [ ] Neutral empty state before real parts exist.
- [ ] Dynamic title: `How I’ll split your material (N parts)`.
- [ ] View Splitting Prompt button.
- [ ] Guardrail/range warning location.
- [ ] Dynamic part-card container.
- [ ] Each part card shows title, source range, counts, description, applied bundle chips.
- [ ] Real Edit Settings modal fields:
  - title;
  - page/section range;
  - topic/formula counts;
  - description;
  - applied bundle chips;
  - Save / Cancel.
- [ ] Add Part, Merge Parts, Remove Part and Reorder controls.
- [ ] Back / Continue to Blueprint.
- [ ] No hardcoded National Income part cards or static six-part title.

---

# 7. Screen 5 UI Alignment Checklist

- [ ] Blueprint Overview header.
- [ ] Overall status/progress area.
- [ ] Blueprint card grid empty state.
- [ ] Per-card job status: queued/generating/ready/failed.
- [ ] Per-card View Blueprint Prompt button.
- [ ] Per-card applied bundle chips.
- [ ] Per-card headings/text/image/CA/validation summary placeholders.
- [ ] Per-card Open Detail / Retry / Approve controls.
- [ ] Approve All Blueprints control.
- [ ] Start Generation button disabled until real valid blueprint state exists.
- [ ] No hardcoded blueprint text-plan/image-plan/CA sample content.

---

# 8. Screen 6 Blueprint Detail Overlay Alignment Checklist

- [ ] Remains overlay; not independent navigation screen.
- [ ] Back to Blueprint Cards action.
- [ ] Dynamic part title.
- [ ] Bundle chip editor area.
- [ ] Section 1 headings panel.
- [ ] Section 2 text-plan panel.
- [ ] Section 3 image-plan panel.
- [ ] Section 4 CA plan panel with two windows:
  - 2020–2023 important background CA;
  - 2024–today recent/current CA.
- [ ] Section 5 validation plan panel.
- [ ] Real prompt viewer/edit area per relevant operation.
- [ ] AI chat history starts empty or clearly labeled example-only; no fake live messages.
- [ ] Chat input/send button.
- [ ] Undo Last Change control.
- [ ] Regenerate Image Plan Only control.
- [ ] Approve this Blueprint / Save Changes controls.
- [ ] No static National Income/GDP/MP sample blueprint content.

---

# 9. Generation Workspace UI Alignment Checklist

- [ ] Sticky generation toolbar.
- [ ] Generate All control.
- [ ] Overall progress.
- [ ] Global validation control, disabled until valid conditions exist.
- [ ] Quick Jump side navigation.
- [ ] Dynamic part-card stack with honest empty state.
- [ ] Per-part state labels:
  - queued;
  - building context;
  - generating text;
  - generating images;
  - fetching CA;
  - ready for review;
  - failed;
  - approved.
- [ ] Per-part actual prompt viewer location.
- [ ] Per-part text/image review controls.
- [ ] Per-part Generate / Retry / Remove / Unlock controls.
- [ ] Add New Part UI.
- [ ] Image slot/loading/error/approved UI.
- [ ] CA query/result/merge/refresh UI.
- [ ] Highlight-to-visualize UI.
- [ ] Refinement/diff UI.
- [ ] Per-part validation popup area.
- [ ] No static GDP notes, Shyam story, MP data, current affairs, image placeholders, or fake generated content.

---

# 10. Export UI Alignment Checklist

- [ ] Export settings and preview panel.
- [ ] Format choices only if supported by implementation plan.
- [ ] Include/exclude controls for approved assets only.
- [ ] Honest empty state when no approved content exists.
- [ ] Preview must be dynamic approved content placeholder, not static National Income content.
- [ ] Copy/Download actions disabled until real approved document exists.
- [ ] No AI call UI at export.

---

# 11. UI Alignment Sign-Off

Before prompt integration begins for a stage:

```text
☐ Layout matches approved documents
☐ All required controls/modals/empty/loading states exist
☐ No hardcoded subject/sample result appears as real output
☐ Buttons are disabled or clearly marked if later-stage behavior is not implemented
☐ UI state can be populated entirely from future state objects
☐ No visual change breaks existing skeleton style
```

## End of UI Alignment Gate
