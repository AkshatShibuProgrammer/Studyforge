# Implementation Plan: Module 01 — Canvas AI Bridge

## 1. Implementation Flow

```
User Action / Pipeline Step
       │
       ▼
StudyForge.API.generateText(prompt, options)
       │
       ├──> Inject ambient URL & generationConfig
       │
       ├──> Try fetch()
       │      │
       │      ├──> Success (HTTP 200) ──> Return raw text to JSON Auto-Repair
       │      │
       │      └──> Failure (429 / 503 / Network Drop)
       │             │
       │             ├──> Attempt < 2?
       │             │      │
       │             │      └──> Yes: Sleep (2s or 4s) ──> Retry
       │             │
       │             └──> No: Throw structured NetworkError
```

---

## 2. Coding Steps
1. Write the base request builder function constructing URLs with empty keys.
2. Implement sleep utility `delay(ms)`.
3. Build the resilient fetch executor checking response status and logging retry warnings.
4. Extract candidates safely (`result?.candidates?.[0]?.content?.parts?.[0]?.text`).
5. Wire Imagen base64 formatter to prefix `data:image/png;base64,`.
