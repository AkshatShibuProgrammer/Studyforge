# Tasks: Module 03 — IndexedDB Persistence Engine

## 1. Implementation Tasks
- [ ] Task 03.1: Implement `init()` for `StudyForge_V3_DB` with version checking.
- [ ] Task 03.2: Implement `saveImage()` wrapping IndexedDB transaction in a Promise.
- [ ] Task 03.3: Implement `getImage()` and `getImagesByPart()`.
- [ ] Task 03.4: Implement `deleteImage()` and `clearAll()`.
- [ ] Task 03.5: Sanitize `app.save()` to prevent Base64 strings from leaking into `localStorage`.
- [ ] Task 03.6: Verify hydration of saved images upon browser page reload.

## 2. Verification Criteria
* Successfully writes and reads a 2 MB binary string to IndexedDB.
* Calling `localStorage.getItem('studyforge_v21_skeleton_state')` shows zero `data:image/png` substrings.
