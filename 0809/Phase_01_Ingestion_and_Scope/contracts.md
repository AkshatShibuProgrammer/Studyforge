# Contracts: Phase 01 — Ingestion, Scope & Multi-Method Input

## 1. Input State Schema
```typescript
interface InputProfileState {
    topic: string;
    focus: string;
    userSubtopics: string[];
    scopeProposal: {
        guaranteed_topics: Array<{ title: string; reason: string }>;
        suggested_essential: Array<{ title: string; reason: string }>;
        suggested_optional: Array<{ title: string; reason: string }>;
        current_topics: Array<{ title: string; reason: string; web_source_url?: string; source_date?: string }>;
        scope_notes: string[];
    } | null;
    approvedSubtopics: string[];
    customSubtopics: string[];
    options: {
        depth: "basic" | "medium" | "comprehensive";
        searchInternet: boolean;
        includeCA: boolean;
        previewImagePrompts: boolean;
        exam: string;
        objective: string;
        stateFocus: string;
    };
}
```

## 2. Source Document Schema
```typescript
interface SourceDocumentState {
    origin: "upload" | "ai_draft" | "pasted_text" | "image_ocr";
    type: string;
    text: string;
    rawText: string;
    fileName?: string;
    fileSize?: string;
    version: number;
}
```
