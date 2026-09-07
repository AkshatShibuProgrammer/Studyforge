# Contracts: Phase 10 — Export & Monolithic Packaging

```typescript
interface ExportOptions {
    includeCover: boolean;
    includeTOC: boolean;
    includeImages: boolean;
    includeCurrentAffairs: boolean;
    format: "html" | "md" | "pdf" | "copy";
}

interface ExportPackage {
    title: string;
    generatedDate: string;
    parts: Array<{
        num: number;
        title: string;
        markdown_body: string;
        html_body: string;
        images: Array<{ url: string; title: string; takeaway: string }>;
        current_affairs: Array<{ fact: string; url: string }>;
    }>;
}
```
