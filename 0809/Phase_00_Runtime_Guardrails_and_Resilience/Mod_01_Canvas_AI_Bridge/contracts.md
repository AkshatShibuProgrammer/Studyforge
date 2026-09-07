# Contracts: Module 01 — Canvas AI Bridge

## 1. REST Payload Interfaces

```typescript
interface GeminiContentPart {
    text: string;
}

interface GeminiContent {
    parts: GeminiContentPart[];
    role?: string;
}

interface GeminiGenerationConfig {
    temperature?: number;
    maxOutputTokens?: number;
    responseMimeType?: string;
}

interface GeminiRequestBody {
    contents: GeminiContent[];
    generationConfig?: GeminiGenerationConfig;
    tools?: Array<{ googleSearch: {} }>;
}

interface GeminiCandidate {
    content: {
        parts: GeminiContentPart[];
    };
    finishReason?: string;
}

interface GeminiResponseBody {
    candidates?: GeminiCandidate[];
    error?: {
        code: number;
        message: string;
        status: string;
    };
}
```

---

## 2. Imagen 4.0 Prediction Interfaces

```typescript
interface ImagenPredictRequestBody {
    instances: Array<{ prompt: string }>;
    parameters: {
        sampleCount: number;
        aspectRatio: "16:9" | "1:1" | "4:3";
    };
}

interface ImagenPredictionResult {
    bytesBase64Encoded?: string;
    mimeType?: string;
}

interface ImagenPredictResponseBody {
    predictions?: ImagenPredictionResult[];
    error?: {
        code: number;
        message: string;
    };
}
```
