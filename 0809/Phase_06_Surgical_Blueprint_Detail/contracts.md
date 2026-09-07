# Contracts: Phase 06 — Surgical Blueprint Detail

```typescript
interface PatchOperation {
    op: "replace" | "add" | "remove";
    path: string; // e.g. "/image_plan/0" or "/headings"
    value: any;
    reason: string;
}

interface AIChatResponse {
    detected_scope: {
        sections: string[];
        target_ids: string[];
        scope_reason: string;
    };
    patch_operations: PatchOperation[];
    updated_sections: string[];
    undo_payload: any[];
    requires_full_regeneration: boolean;
    warning?: string;
}

interface SectionRegenResponse {
    target_section: string;
    replacement_content: any;
    preserved_ids: string[];
    new_ids: string[];
    compatibility_notes: string[];
}
```
