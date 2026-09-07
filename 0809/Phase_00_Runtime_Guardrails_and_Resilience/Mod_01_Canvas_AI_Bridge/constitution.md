# Constitution: Module 01 — Canvas AI Bridge

## 1. Principles

### Rule 1: Ambient Key Exclusivity
The module MUST set `const apiKey = "";`. No interactive prompts, prompt popups, or fallback prompts requesting an API key may be introduced.

### Rule 2: Token Budget Allocation
All calls using reasoning or complex prompt structures MUST specify `"maxOutputTokens": 8192` in `generationConfig` to ensure adequate budget for structured responses.

### Rule 3: Native Search Tooling
When web search is requested, the payload MUST specify `tools: [{ googleSearch: {} }]`. The module MUST NOT attempt third-party scraping or unauthorized HTTP requests.
