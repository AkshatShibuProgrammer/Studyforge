# Specification: Module 01 — Canvas AI Bridge

## 1. Functional Requirements

### FR-01.1: Text Generation Invocation
* Signature: `StudyForge.API.generateText(promptText, options)`
* Endpoint: `https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key=`
* Header: `Content-Type: application/json`
* Method: `POST`
* Body Format:
  ```json
  {
    "contents": [{ "parts": [{ "text": "<PROMPT>" }] }],
    "generationConfig": {
      "temperature": 0.2,
      "maxOutputTokens": 8192,
      "responseMimeType": "application/json"
    }
  }
  ```

### FR-01.2: Grounded Web Search Invocation
* Signature: `StudyForge.API.searchText(searchQuery, options)`
* Endpoint: `https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key=`
* Body Format:
  ```json
  {
    "contents": [{ "parts": [{ "text": "<SEARCH_PROMPT>" }] }],
    "tools": [{ "googleSearch": {} }]
  }
  ```

### FR-01.3: Imagen 4.0 Educational Diagram Invocation
* Signature: `StudyForge.API.generateImage(imagePrompt, aspectRatio)`
* Endpoint: `https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict?key=`
* Body Format:
  ```json
  {
    "instances": [{ "prompt": "<IMAGE_PROMPT>" }],
    "parameters": {
      "sampleCount": 1,
      "aspectRatio": "16:9"
    }
  }
  ```
* Return: `data:image/png;base64,<BASE64_BYTES>`

### FR-01.4: Telemetry & Execution Audit
* Every AI call MUST record an entry into `app.state.promptHistory` capturing:
  * `executionId`: Unique ID (e.g. `EXEC-1725752400-abcd`)
  * `operationId`: Canonical ID (`AI-01A`, `AI-03A`, `AI-07A`, etc.)
  * `timestamp`: ISO string
  * `durationMs`: Total roundtrip time in milliseconds
  * `status`: `'running'` | `'success'` | `'repaired'` | `'failed'`
