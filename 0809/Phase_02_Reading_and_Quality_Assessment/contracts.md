# Contracts: Phase 02 — Reading & Quality Assessment

```typescript
interface QualityReport {
    characterCount: number;
    printableRatio: number;
    replacementCharacterCount: number;
    emptyPageCount: number;
    status: "usable" | "partially_usable" | "unusable";
    reasons: string[];
}

interface PageMapEntry {
    page: number;
    text: string;
}

interface ReadingState {
    status: "pending" | "running" | "success" | "failed";
    selectedMethod: "auto" | "technical" | "ai_cleanup" | "ai_restructure";
    originalExtract: string;
    currentText: string;
    pageMap: PageMapEntry[];
    sections: Array<{ sectionId: string; title: string; text: string; pageRange: number[] }>;
    unresolvedSegments: Array<{ page_ref: string; raw_text: string; reason: string }>;
    quality: QualityReport | null;
    tierUsed: "technical" | "ai_cleanup" | "ai_restructure";
}
```
