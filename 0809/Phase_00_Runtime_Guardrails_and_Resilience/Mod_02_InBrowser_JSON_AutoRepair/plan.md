# Implementation Plan: Module 02 — In-Browser JSON Auto-Repair

## 1. Algorithm Design

```
Raw LLM String
      │
      ▼
[1. Strip Code Fences & Whitespace]
      │
      ▼
[2. Attempt Native JSON.parse()] ───> SUCCESS ───> Return { isRepaired: false, data }
      │
      └──> FAILS (SyntaxError)
             │
             ▼
[3. Run Token State Machine Scanner]
      • Track string state (inQuote: true/false)
      • Push '{' or '[' onto stack
      • Pop when '}' or ']' encountered
             │
             ▼
[4. Apply String Repair Rules]
      • If inQuote is true: append '"'
      • Strip dangling commas (e.g. ", }", ", ]", or trailing ",")
      • Strip incomplete keys (e.g. ', "key":' or ', "key"')
             │
             ▼
[5. Unwind Structural Stack]
      • For each item in stack, append matching '}' or ']'
             │
             ▼
[6. Parse Repaired String] ─────────> SUCCESS ───> Return { isRepaired: true, data }
      │
      └──> FAILS ───────────────────> Return Fallback Default Object
```
