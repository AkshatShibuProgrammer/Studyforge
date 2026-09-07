# Contracts: Phase 07 — Notes Synthesis, CA & Visuals

```typescript
interface HTMLBlock {
    anchor: string;
    heading_id: string;
    container_type: string; // One of 22 container types
    title: string;
    safe_content: string;   // Rich Markdown formatting
    traceability: "SOURCE_BACKED" | "RESEARCH_REQUIRED" | "OPTIONAL_ENRICHMENT" | "WEB_SOURCED";
    source_refs: string[];
    web_source_refs?: Array<{ claim: string; url: string; publisher: string; date: string }>;
}

interface VisualExplainerCard {
    image_id: string;
    url: string;
    title: string;
    style: string;
    component_map: Array<{ component_num: number; label: string; description: string }>;
    process_walkthrough: string;
    exam_takeaway: string;
}

interface GeneratedPartRecord {
    part_id: string;
    html_blocks: HTMLBlock[];
    visual_cards: VisualExplainerCard[];
    current_affairs_callout: {
        summary: string;
        verified_facts: Array<{ fact: string; url: string; publisher: string; date: string }>;
    };
    generation_summary: string;
}
```
