# Implementation Plan: Phase 09 — Two-Layer Validation Subagent

## Steps
1. User clicks Approve Part -> Trigger AI-07H.
2. Render `#sf-validation` modal with actionable suggestion cards.
3. If user clicks Apply on `update_image`, invoke AI-07K adapter -> Call `createImage()`.
4. Run Validator Subagent Pass 2 -> Check for dated statistics -> Update citations.
5. User confirms -> Mark `approvedParts[part_id] = true`.
6. When all parts approved -> Trigger AI-07I Final Document Validation modal.
