# Contracts: Phase 04 — Pedagogical Part Splitting & Structure

```typescript
interface PartRecord {
    num: number;
    part_id: string;
    title: string;
    pages: string;
    topics: number;
    defs: number;
    desc: string;
    topic_ids: string[];
    analysis_refs: {
        definitions?: string[];
        formulas?: string[];
        pyqs?: string[];
        examples?: string[];
        timelines?: string[];
        tables?: string[];
    };
    applied_bundles: string[];
    status: "confirmed" | "draft" | "stale";
}

interface SplitOutputSchema {
    recommended_range: { min_parts: number; max_parts: number };
    proposed_count: number;
    out_of_range_warning: { required: boolean; message: string };
    parts: Array<{
        part_id: string;
        title: string;
        page_range: number[];
        topic_ids: string[];
        analysis_refs: Record<string, string[]>;
        applied_bundles: string[];
        rationale: string;
    }>;
}
```
