# StudyForge Implementation & Validation Guidelines

## 1. Architectural Guardrails
- **No External Dependencies**: Never add `npm install` packages, CDN scripts that require build steps, or backend Python/Node servers.
- **State Integrity**: `window.app.state` must remain serializable. Functions, circular references, and DOM nodes must never be saved in state.
- **CSS Architecture**: Use the established design system tokens in `sindhuskeleton.html`. Preserve all 22 pedagogical container classes.

## 2. API Call Standards
- Endpoint: `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=""`
- Image Endpoint: `https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict?key=""`
- Error Handling: Always wrap with `StudyForge.API.callWithRetry()` using exponential backoff (2 attempts, 2000ms/4000ms).

## 3. UI/UX Consistency
- Screen Transition: Smooth fade between screens `#screen-1` to `#screen-10`.
- Dark Mode / High Contrast: Adhere to WCAG 2.1 AA standards for typography and contrast ratios.
