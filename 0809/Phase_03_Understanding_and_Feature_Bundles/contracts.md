# Contracts: Phase 03 — Understanding & Feature Bundles

```typescript
interface AnalysisState {
    status: "idle" | "running" | "success" | "failed";
    sourceVersion: number;
    subjectSignals: {
        primary_subject: string;
        sub_discipline: string;
        purpose: string;
        secondary_domains: string[];
        signals: Record<string, { strength: "strong" | "weak" | "not_detected"; evidence: string[]; page_refs: number[] }>;
    } | null;
    deepAnalysis: {
        topics: Array<{ id: string; title: string; parent_id?: string; page_refs: number[] }>;
        definitions: Array<{ id: string; term: string; definition: string; page_refs: number[] }>;
        formulas: Array<{ id: string; expression: string; variables: Record<string, string>; page_refs: number[] }>;
        pyqs: Array<{ id: string; year: string; exam: string; question: string }>;
        comparisons: Array<{ id: string; entity_a: string; entity_b: string; basis: string[] }>;
        timelines: Array<{ id: string; event: string; date: string; significance: string }>;
        tables: Array<{ id: string; title: string; headers: string[]; rows: string[][] }>;
    };
    bundleAnalysis: {
        bundles: Array<{
            bundle_id: string;
            state: "auto_on" | "suggested" | "not_detected";
            evidence: string[];
            features: Array<{ feature_id: string; state: string; reason: string }>;
        }>;
    };
    userBundleOverrides: Record<string, any>;
}
```
