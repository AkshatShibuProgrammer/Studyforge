# Contracts: Phase 08 — Multi-Exam PYQ Intelligence Layer

```typescript
interface PYQItem {
    id: string;
    exam: string;       // e.g. "MPPSC Mains"
    year: string;       // e.g. "2022"
    paper: string;      // e.g. "GS Paper 2"
    marks: number;      // e.g. 5
    question_text: string;
    model_solution: {
        intro: string;
        core_points: string[];
        diagram_hint?: string;
        conclusion: string;
    };
    examiner_trap: string;
}

interface ExamIntelligenceCard {
    topic: string;
    exam_target: string;
    frequency_rating: "high" | "medium" | "low";
    historical_frequency_summary: string;
    pyqs: PYQItem[];
}
```
