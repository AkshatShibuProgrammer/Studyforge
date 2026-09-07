# Contracts: Phase 00 — Runtime Guardrails, Resilience & Canvas Bridge

## 1. JavaScript API Interfaces & Signatures

```typescript
namespace StudyForge.API {
    interface RequestOptions {
        temperature?: number;          // Range: 0.1 (strict extraction) to 0.7 (creative)
        maxOutputTokens?: number;      // Default: 8192
        retries?: number;              // Default: 2
        backoffDelays?: number[];      // Default: [2000, 4000]
        grounding?: boolean;           // Enables Google Search tool
        responseMimeType?: string;     // Default: "application/json"
    }

    interface GenerationResult<T> {
        success: boolean;
        data: T | null;
        repaired: boolean;
        executionId: string;
        error?: string;
        attempts: number;
        durationMs: number;
    }

    function generateText<T = any>(
        prompt: string, 
        options?: RequestOptions
    ): Promise<GenerationResult<T>>;

    function searchText(
        searchQuery: string, 
        options?: RequestOptions
    ): Promise<string>;

    function generateImage(
        imagePrompt: string, 
        aspectRatio?: "16:9" | "1:1" | "4:3"
    ): Promise<string>; // Returns base64 Data URL
}
```

---

## 2. In-Browser JSON Repair Engine Signature

```typescript
namespace StudyForge.Guardrails {
    interface RepairResult<T> {
        parsed: T;
        isRepaired: boolean;
        repairLog: string[];
    }

    function safeParseJSON<T = any>(
        rawText: string, 
        fallbackDefault?: T
    ): RepairResult<T>;

    function balanceBrackets(brokenJson: string): string;
    function closeUnterminatedStrings(brokenJson: string): string;
    function stripTrailingCommas(brokenJson: string): string;
}
```

---

## 3. IndexedDB Storage Schema (`StudyForge_V3_DB`)

```typescript
// Database Name: "StudyForge_V3_DB"
// Version: 1

interface ImageStoreRecord {
    image_id: string;               // Primary Key (e.g., "IMG-P01-01")
    part_id: string;                // Foreign Key to Part
    title: string;                  // User-facing title
    data_url: string;               // Base64 PNG data URL (1-2 MB)
    style_recommended: string;      // From 35 visual styles
    expanded_prompt: string;        // Final executed prompt
    created_at: string;             // ISO timestamp
    byte_size: number;              // Calculated binary size
}

namespace StudyForge.ImageDB {
    function init(): Promise<IDBDatabase>;
    function saveImage(record: ImageStoreRecord): Promise<boolean>;
    function getImage(imageId: string): Promise<ImageStoreRecord | null>;
    function getImagesByPart(partId: string): Promise<ImageStoreRecord[]>;
    function deleteImage(imageId: string): Promise<boolean>;
    function clearAll(): Promise<boolean>;
}
```

---

## 4. LocalStorage State Snapshot Schema (`studyforge_v21_skeleton_state`)

```json
{
  "version": "3.0",
  "currentScreen": 1,
  "maxScreen": 1,
  "mainTopic": "National Income Accounting",
  "focusArea": "Macroeconomics",
  "inputProfile": {
    "userSubtopics": ["GDP", "GNP", "NDP", "NNP"],
    "options": {
      "depth": "medium",
      "searchInternet": true,
      "includeCA": true,
      "exam": "UPSC Civil Services / MPPSC",
      "language": "English"
    }
  },
  "sourceDocument": {
    "origin": "upload",
    "type": "pdf",
    "version": 1
  },
  "imageMetadata": [
    {
      "image_id": "IMG-P01-01",
      "part_id": "P-01",
      "title": "Circular Flow of Income Diagram",
      "style": "Flowchart",
      "hasBinaryInIndexedDB": true
    }
  ],
  "promptHistory": []
}
```
*(Notice: Raw Base64 data is strictly excluded from localStorage).*
