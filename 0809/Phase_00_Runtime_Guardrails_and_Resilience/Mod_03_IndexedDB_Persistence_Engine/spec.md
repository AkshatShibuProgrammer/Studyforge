# Specification: Module 03 — IndexedDB Persistence Engine

## 1. Functional Requirements

### FR-03.1: Database Lifecycle Management
* Database Name: `StudyForge_V3_DB`
* Version: `1`
* Stores:
  * `image_assets`: Key path `image_id`, indexed on `part_id`.
  * `document_cache`: Key path `doc_id`, indexed on `created_at`.

### FR-03.2: Visual Asset Persistence (`ImageDB`)
* `saveImage(record)`:
  * Accepts `{ image_id, part_id, title, data_url, style, expanded_prompt }`.
  * Saves to `image_assets`.
  * Strips `data_url` before recording the metadata entry in `app.state.imageMetadata`.
* `getImage(imageId)`: Resolves with full asset including `data_url`.
* `getImagesByPart(partId)`: Uses index `part_id` to retrieve all visual assets for a given part.
* `deleteImage(imageId)`: Removes record from store.

### FR-03.3: State Sanitizer Interceptor
* Patches `app.save()` to filter out all Base64 strings from `app.state` before serializing to `localStorage`.
* Restricts `localStorage` key to `studyforge_v21_skeleton_state`.
* Validates schema version `3.0` during `app.init()` hydration.
