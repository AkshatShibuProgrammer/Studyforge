# Specification: Module 02 — In-Browser JSON Auto-Repair

## 1. Functional Requirements

### FR-02.1: Markdown Code Fence Stripper
* Input: Raw string potentially containing ```` ```json ```` or ```` ``` ```` code fences or conversational prefixes (e.g., `"Here is the output: {"`).
* Operation: Finds the index of the first `{` or `[` and extracts to the last `}` or `]` (or end of string).
* Strips all leading/trailing non-JSON wrapper noise.

### FR-02.2: Unterminated String Closure
* Scans the string sequentially while tracking escaping state (`\`).
* If end-of-string is reached while inside an open double quote `"`, appends a closing `"` character.

### FR-02.3: Structural Stack & Bracket Balancing
* Maintains a LIFO stack tracking whether an open context is an object `{` or an array `[`.
* Trailing incomplete keys (e.g. `, "title": ` or `, "summary": "incomplete text...`) are sanitized.
* If a dangling comma `,` precedes the cut-off, it is removed.
* For each unmatched brace or bracket remaining on the stack, the matching closer `}` or `]` is appended in reverse order.

### FR-02.4: Schema Defaulting
* If the repaired object is missing mandatory arrays (`topics`, `definitions`, `formulas`, `headings`, `html_blocks`, `pyqs`), the validator injects `[]`.
* If title or content string properties are missing, injects empty strings `""`.
