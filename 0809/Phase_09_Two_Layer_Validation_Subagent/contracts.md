# Contracts: Phase 09 — Two-Layer Validation Subagent

```typescript
interface ValidationSuggestion {
    suggestion_id: string;
    action: "add_container" | "update_text" | "update_image" | "fetch_ca";
    target: string;
    details: string;
    rationale: string;
    priority: "high" | "medium" | "low";
}

interface ValidationReport {
    overall_status: "good" | "needs_review" | "poor";
    summary: {
        text_covered: string[];
        images_created: string[];
        sources_used: string[];
        web_sources_used: string[];
    };
    issues: Array<{ issue_id: string; detail: string; priority: "high" | "medium" | "low" }>;
    suggestions: ValidationSuggestion[];
}

interface FinalValidationReport {
    readiness_status: "ready" | "needs_review";
    covered_well: string[];
    potential_gaps: Array<{ gap_id: string; detail: string; why_it_matters: string }>;
    suggestions: Array<{
        suggestion_id: string;
        type: "add_part" | "enrich_part" | "add_container";
        target: string;
        title: string;
        details: string;
    }>;
}
```
