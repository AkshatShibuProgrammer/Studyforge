# Implementation Plan: Phase 10 — Export & Monolithic Packaging

## Steps
1. User configures checkboxes on Screen 8 -> Click Export.
2. Read options -> Iterate approved parts in `app.state.parts`.
3. Synthesize clean Markdown string with proper `# Heading` hierarchy.
4. If format is 'copy': Write to `navigator.clipboard`.
5. If format is 'md': Create `Blob(['text/markdown'])` -> Trigger download.
6. If format is 'html': Wrap in print-ready CSS template -> Trigger download.
7. If format is 'pdf': Open print-ready window -> Trigger `window.print()`.
