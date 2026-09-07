# Contracts: Phase 05 — Pedagogical Blueprint Strategy

```typescript
interface BlueprintRecord {
    part_id: string;
    headings: Array<{ heading_id: string; title: string; level: number; purpose: string }>;
    text_plan: Array<{
        container_id: string;
        heading_id: string;
        container_type: string;
        teaching_goal: string;
        source_refs: string[];
        analysis_refs: string[];
        bundle_features: string[];
    }>;
    image_plan: Array<{
        image_id: string;
        title: string;
        placement_after: string;
        learning_goal: string;
        content_to_show: string[];
        style_recommended: string;
        style_reasoning: string;
        mixed_style_allowed: boolean;
    }>;
    ca_plan: {
        historical_window: { from: string; to: string; queries: Array<{ query: string; purpose: string }> };
        recent_window: { from: string; to: string; queries: Array<{ query: string; purpose: string }> };
    };
    validation_plan: Array<{ check_id: string; what_to_check: string; reason: string }>;
    applied_bundles: string[];
}
```
