# Contracts: Module 02 — In-Browser JSON Auto-Repair

## 1. Type Interfaces

```typescript
namespace StudyForge.Guardrails {
    interface AutoRepairLog {
        wasTruncated: boolean;
        unclosedQuotesFixed: number;
        danglingCommasRemoved: number;
        bracketsAppended: string;
        repairedStringLength: number;
    }

    interface SafeParseResult<T> {
        success: boolean;
        data: T;
        isRepaired: boolean;
        log: AutoRepairLog;
        error?: string;
    }

    function safeParseJSON<T = any>(
        rawText: string, 
        fallbackDefault?: T
    ): SafeParseResult<T>;
}
```

---

## 2. Test Input/Output Scenarios

| Test ID | Input Raw Text | Expected Repaired Output |
|---|---|---|
| **T-01** | `{"items": ["apple", "ban` | `{"items": ["apple", "ban"]}` |
| **T-02** | `{"part": {"title": "Macro", "topics": [{"id": "T1"` | `{"part": {"title": "Macro", "topics": [{"id": "T1"}]}}` |
| **T-03** | ````json\n{"summary": "ok", "list": [1, 2, 3,]}\n```` | `{"summary": "ok", "list": [1, 2, 3]}` |
| **T-04** | `{"title": "Note", "content": "Text", "missing": ` | `{"title": "Note", "content": "Text"}` |
