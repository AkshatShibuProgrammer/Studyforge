# Contracts: Phase 11 — In-Canvas Diagnostics, E2E Testing & Benchmarks

```typescript
interface DiagnosticLogEntry {
    logId: string;
    timestamp: string;
    operationId: string;
    durationMs: number;
    tokensEstimated: number;
    temperature: number;
    wasRepaired: boolean;
    repairDetails?: {
        unclosedQuotes: number;
        bracketsAppended: string;
    };
    storageDeltaKB: number;
    status: "success" | "retry" | "failed";
}

interface TestRunResult {
    testName: string;
    passed: boolean;
    durationMs: number;
    assertions: Array<{ name: string; expected: any; actual: any; passed: boolean }>;
    error?: string;
}

interface BenchmarkScorecard {
    domain: "Polity" | "Economy" | "History" | "Science";
    overallScore: number; // 0 to 100
    subscores: {
        conceptualRigor: number;     // max 30
        pyqExamRelevance: number;    // max 25
        caRecency: number;           // max 20
        visualExplanations: number;  // max 15
        traceabilityAndTraps: number;// max 10
    };
    passThresholdMet: boolean;
    recommendations: string[];
}
```
