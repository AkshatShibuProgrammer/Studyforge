# StudyForge — Document 4: Comprehensive Prompt Generation Rules & Runtime Implementation Specification
## Canonical Runtime Rules for Building, Executing, Validating, Retrying, Caching, Rendering, and Auditing Prompts

> # IMPLEMENTATION INSTRUCTION — READ FIRST
>
> Use the canonical prompts in **Document 3 exactly as written**. This document does not authorize wording changes to any system prompt, task prompt, output schema, traceability label, or prompt rule.
>
> The developer must only:
>
> 1. choose the correct prompt ID;
> 2. build its permitted runtime context;
> 3. replace its declared variables;
> 4. apply the required model settings;
> 5. validate the AI response;
> 6. save the exact executed final prompt and result;
> 7. safely update state and the UI.
>
> If a provider requires different API field names, map the fields. Do **not** rewrite canonical prompt content.

---

# 1. Purpose and Scope

This document turns the canonical prompt library into executable app behavior. It specifies:

- prompt registry structure;
- runtime prompt assembly;
- context selection and token budgeting;
- subject and bundle routing;
- model settings and grounding guardrails;
- response/schema validation;
- state updates and stale-data rules;
- image, current-affairs, and validation orchestration;
- retry and error recovery;
- cache rules;
- prompt history and prompt visibility;
- concurrency/rate-limit control;
- safe rendering rules;
- developer test requirements.

This is the implementation companion to:

- **Document 1:** AI Usage Master Table
- **Document 2:** Prompt Dependency Map
- **Document 3:** Canonical Stored Prompt Library

---

# 2. Canonical Runtime Principles

| # | Rule | Required behavior |
|---:|---|---|
| 1 | Canonical text is immutable | `DEFAULT_PROMPTS` is read-only at runtime. Only final prompt copies may be edited per user run. |
| 2 | Current state wins | Prompt builders use current user-edited source, part, blueprint, and bundle state—not stale initial AI output. |
| 3 | Minimum necessary context | Include only data needed for the operation. Never attach full document content to every part call. |
| 4 | Stable IDs are mandatory | IDs from analysis/parts/blueprints/anchors are carried forward; no silent renaming. |
| 5 | Grounding is explicit | Only approved prompts may enable grounding. No prompt may silently search web. |
| 6 | Raw AI output is untrusted | Parse, validate, sanitize, and map outputs to state before rendering. |
| 7 | User control is preserved | User can view/copy final prompts; edits apply to that one run only. |
| 8 | Failure is isolated | Retry the failed bundle/part/image/query only; do not reset successful work. |
| 9 | Traceability is preserved | Source-backed, research-required, enrichment, and web-sourced material remain distinguishable. |
| 10 | AI does not export | Screen 8 uses approved state only; no hidden prompt or validation call occurs during export. |

---

# 3. Required Prompt Registry Structure

```javascript
const DEFAULT_PROMPTS = Object.freeze({
  SYS_01: `...canonical text from Document 3...`,
  SYS_02: `...`,
  SYS_03: `...`,
  SYS_04: `...`,
  SYS_05: `...`,

  AI_01A: `...`,
  AI_01B: `...`,
  AI_02A: `...`,
  AI_02B: `...`,
  AI_03A: `...`,
  AI_03B: `...`,
  AI_03C: `...`,
  AI_03D: `...`,
  AI_04: `...`,
  AI_05: `...`,
  AI_06A: `...`,
  AI_06B: `...`,
  AI_07A: `...`,
  AI_07B: `...`,
  AI_07C: `...`,
  AI_07D: `...`,
  AI_07E: `...`,
  AI_07F: `...`,
  AI_07G: `...`,
  AI_07H: `...`,
  AI_07I: `...`,
  AI_07J: `...`,
  AI_07K: `...`,

  BND_GEO: `...`,
  BND_PER: `...`,
  BND_FORM: `...`,
  BND_DATA: `...`,
  BND_LAW: `...`,
  BND_TIME: `...`,
  BND_STORY: `...`,
  BND_ADM: `...`,
  BND_PROC: `...`,
  BND_CS: `...`,
  BND_MED: `...`,
  BND_CA: `...`,

  CTX_LOC: `...`,
  CTX_PER: `...`,
  CTX_FORM: `...`,

  REG_01: `...`,
  REG_02: `...`,
  REG_03: `...`
});
```

## 3.1 Prompt configuration registry

Prompt text and operational rules must be separate. The following object is the source of runtime execution rules.

```javascript
const PROMPT_CONFIG = Object.freeze({
  AI_01A: {
    systemKeys: ['SYS_01'],
    templateKey: 'AI_01A',
    allowedGrounding: 'method2InternetOnly',
    temperature: 0.3,
    maxOutputTokens: 2000,
    responseType: 'json',
    schemaKey: 'subtopicExpansion',
    retryClass: 'standard',
    contextPolicy: 'method2Scope'
  },
  AI_07A: {
    systemKeys: ['SYS_01'],
    templateKey: 'AI_07A',
    allowedGrounding: 'never',
    temperature: 0.4,
    maxOutputTokens: 15000,
    responseType: 'json',
    schemaKey: 'generatedPart',
    retryClass: 'largePart',
    contextPolicy: 'partGeneration'
  },
  AI_07D: {
    systemKeys: ['SYS_04'],
    templateKey: 'AI_07D',
    allowedGrounding: 'required',
    temperature: 0.1,
    maxOutputTokens: 5000,
    responseType: 'json',
    schemaKey: 'currentAffairs',
    retryClass: 'groundedSearch',
    contextPolicy: 'currentAffairs'
  }
  // All remaining Prompt IDs must use the exact settings in Document 3.
});
```

## 3.2 Mandatory configuration fields

| Field | Purpose |
|---|---|
| `systemKeys` | Stable canonical system prompt(s) appended in stated order. |
| `templateKey` | Canonical operation prompt ID. |
| `allowedGrounding` | `never`, `required`, or approved conditional mode only. |
| `temperature` | Must match Document 3 settings matrix. |
| `maxOutputTokens` | Target output budget. |
| `responseType` | `json` or `image`. |
| `schemaKey` | JSON validator selected before state update. |
| `retryClass` | Determines retry timing/context reduction. |
| `contextPolicy` | Determines exact state objects allowed into runtime prompt. |
| `promptVersion` | Canonical template/rule version stored with prompt history. |

---

# 4. Runtime Prompt Assembly

## 4.1 Canonical assembly sequence

```text
1. User/system triggers operation ID.
2. Validate prerequisite state.
3. Select PROMPT_CONFIG[operation ID].
4. Resolve allowed grounding from config and current UI flags.
5. Gather minimum context through contextPolicy.
6. Serialize data safely and deterministically.
7. Insert only declared variables into canonical template.
8. Append any canonical regeneration suffix if applicable.
9. Create immutable execution record with exact final prompt.
10. Display prompt in UI as available/copyable.
11. Call provider with required model settings.
12. Validate response before updating state.
```

## 4.2 Reference pseudocode

```javascript
async function executePrompt(operationId, runtimeInput = {}) {
  const config = PROMPT_CONFIG[operationId];
  assert(config, `Unknown operation: ${operationId}`);

  assertPrerequisites(operationId, state, runtimeInput);

  const context = selectContext(config.contextPolicy, state, runtimeInput);
  const groundingEnabled = resolveGrounding(config.allowedGrounding, state, runtimeInput);
  const variables = normalizeVariables(operationId, context, runtimeInput);

  const systemInstruction = config.systemKeys
    .map(key => DEFAULT_PROMPTS[key])
    .join('\n\n');

  let finalTaskPrompt = fillCanonicalTemplate(
    DEFAULT_PROMPTS[config.templateKey],
    variables
  );

  finalTaskPrompt = applyCanonicalRegenerationAddendum(
    operationId,
    finalTaskPrompt,
    runtimeInput
  );

  const execution = createPromptExecutionRecord({
    operationId,
    config,
    systemInstruction,
    finalTaskPrompt,
    variables,
    groundingEnabled,
    inputRefs: context.inputRefs
  });

  savePromptExecution(execution);
  renderPromptAvailability(execution);

  try {
    const rawResponse = await callModel({
      systemInstruction,
      prompt: finalTaskPrompt,
      temperature: config.temperature,
      maxOutputTokens: resolveOutputBudget(config, context),
      groundingEnabled,
      responseType: config.responseType
    });

    const validatedOutput = validateAndNormalizeOutput(
      config.schemaKey,
      rawResponse,
      operationId
    );

    commitOperationOutput(operationId, validatedOutput, execution, runtimeInput);
    markExecutionSuccess(execution.executionId, validatedOutput);
    return validatedOutput;
  } catch (error) {
    return handleOperationFailure(operationId, error, execution, runtimeInput);
  }
}
```

## 4.3 Variable insertion rules

| Rule | Required implementation |
|---|---|
| Replace all declared variables | Before calling model, scan final task prompt for unresolved `{{...}}`. If any remain, block request and report developer error. |
| Escape runtime values safely | Values are prompt text, not HTML. JSON is serialized with stable indentation. |
| Preserve empty values honestly | Insert stated fallback such as `[]`, `{}`, `None provided`, not invented text. |
| No template mutation | `fillCanonicalTemplate()` returns a new string; it never changes `DEFAULT_PROMPTS`. |
| No hidden extra instructions | Only canonical system/template/addendum text may be sent. Any provider formatting wrapper must be logged separately. |
| Record final prompt | Save final system prompt and final task prompt before request. |

---

# 5. Context Policies and Token Budgeting

## 5.1 Context-policy registry

| Policy | Used by | Required context | Explicitly excluded unless required |
|---|---|---|---|
| `method2Scope` | AI-01A | Topic, user sub-topics, depth, exam/state context, internet flag | Full source, later analysis |
| `method2Draft` | AI-01B | Topic, approved sub-topics, depth, CA/internet flags, exam/state context | Stage 3/4 output |
| `sourceCleanup` | AI-02A | Raw extract, diagnostics, file type, page map | Web, subject strategy |
| `sourceRestructure` | AI-02B | Raw/clean extract, diagnostics, file type, page map | Web, later analysis |
| `sourceAnalysis` | AI-03A/B | Whole safe source or one semantic chunk, page map, chunk continuity | Blueprints/generated notes |
| `bundleRouting` | AI-03C/D | Signals, deep analysis, routed fragments, relevant excerpts | Full unrelated bundle catalog |
| `partSplit` | AI-04 | Deep analysis, bundle selection, guardrail, source/summaries | Generated output/images/CA |
| `partBlueprint` | AI-05 | One part plan, source slice, part analysis, all definitions/formulas, bundles | Other parts’ raw sources/outputs |
| `blueprintEdit` | AI-06A/B | Current target blueprint, part plan, relevant analysis, chat instruction | Unrelated blueprints |
| `partGeneration` | AI-07A | One part plan, source slice, scoped analysis, all definitions/formulas, blueprint, bundles, fetched CA | Full raw document, unrelated part notes |
| `imagePlanning` | AI-07B/F/K | One image request, local surrounding text, part metadata, style/direction | Full document unless selected content needs it |
| `currentAffairs` | AI-07D | One query, part/topic context, current date, user state focus | Full source document |
| `contentRefinement` | AI-07G | Current part blocks, user request, selected text, blueprint, manual-edit metadata | Other parts |
| `partValidation` | AI-07H | Current part, assets, CA, source slice, blueprint, traceability | Full document |
| `finalValidation` | AI-07I | Approved document, blueprint summaries, coverage map, traceability | Raw unapproved drafts |
| `quickBlueprint` | AI-07J | New topic/subtopics, parent summary, global bundles, CA setting | Full original source unless user supplies it |

## 5.2 Token budget rule

Before every call, estimate input tokens and reserve output capacity.

```text
safeInputBudget = modelContextLimit - requiredOutputBudget - systemPromptBudget - safetyMargin
```

Recommended safety margin: **20% of model context** or a minimum configured safety threshold.

## 5.3 Context reduction order

When context does not fit, reduce only according to this order:

| Priority | Preserve / reduce | Rule |
|---:|---|---|
| 1 | Preserve canonical system/template text and output schema | Never remove. |
| 2 | Preserve current target source slice and stable IDs | Never remove for source-backed task. |
| 3 | Preserve current part blueprint and user-edited instruction | Never remove. |
| 4 | Preserve all definitions/formulas for AI-05/AI-07A | Compact registry; preserve unless impossible. |
| 5 | Reduce duplicated narrative context | Remove repeated summaries/evidence first. |
| 6 | Reduce non-target examples/PYQs/timelines | Keep only items assigned to current part. |
| 7 | Reduce optional style catalog/secondary rationale | Keep selected style only. |
| 8 | Use semantic topic summaries instead of raw non-target source text | Only for supporting context. |

## 5.4 Large-document semantic chunking

| Step | Requirement |
|---:|---|
| Detect | If source exceeds ~80% of usable model context. |
| Split | Chapter heading → section heading → page boundary → paragraph group. |
| Context | Every chunk carries chunk ID, boundary metadata, prior summary, next preview. |
| Analyze | AI-03A and AI-03B process each chunk. |
| Merge | Merge/dedupe topics, definitions, formulas, PYQs, tables, timelines with source refs. |
| Warn | Warn only if a single section requires paragraph-level splitting. |

---

# 6. Grounding and Web-Source Enforcement

## 6.1 Single source of truth

```javascript
function resolveGrounding(mode, state, runtimeInput) {
  if (mode === 'never') return false;
  if (mode === 'required') return true;
  if (mode === 'method2InternetOnly') {
    return Boolean(state.inputProfile.internetSearchEnabled);
  }
  throw new Error(`Unsupported grounding mode: ${mode}`);
}
```

## 6.2 Grounding policy

| Situation | Required behavior |
|---|---|
| User uploads/pastes source | Do not ground analysis, extraction, splitting, blueprinting, normal writing, or validation. |
| Method 2 with internet flag OFF | AI-01A/AI-01B grounding OFF. |
| Method 2 with internet flag ON | AI-01A/AI-01B grounding ON; web outputs must retain URL/date metadata. |
| Current Affairs fetch | AI-07D grounding ON. |
| Grounding unavailable | AI-07D returns `grounding_status: unavailable` and disclaimer; it does not invent fresh results. |
| User asks for current facts during refinement | AI-07G returns CA action required; it does not silently use model memory as current data. |

## 6.3 Web-source acceptance rule

A block can become `WEB_SOURCED` only if all are true:

- It originated from AI-07D or explicitly grounded Method 2 output.
- It has a non-empty, valid `https://` or `http://` URL.
- It has source/publisher name where available.
- It includes fact date or explicit `date unavailable` value.
- It retains fetch timestamp.

If any condition fails, it must not display as verified web-sourced content.

---

# 7. Response Parsing, Schema Validation, and Repair

## 7.1 Mandatory pipeline

```text
Raw model response
      ↓
Extract response payload
      ↓
Parse JSON or image metadata
      ↓
Validate required schema fields
      ↓
Validate enums, IDs, anchors, URLs, traceability
      ↓
Normalize safe values
      ↓
Commit state
      ↓
Render UI
```

## 7.2 JSON response rules

| Rule | Required behavior |
|---|---|
| JSON only prompts | Reject commentary before/after JSON unless provider wrapper is known and safely stripped. |
| Parse failure | Do not update state. Enter response-format retry route. |
| Missing required field | Do not guess. Request repair/retry with same canonical prompt plus provider error context. |
| Unknown enum | Reject/normalize only if safe mapping is explicitly configured. |
| Duplicate stable IDs | Reject result or remap only through explicit ID-collision resolver; log collision. |
| Invalid anchor | Reject affected item and request correction; never insert into arbitrary DOM selector. |
| Invalid web URL | Remove web verification status; request correction or treat as unverified. |

## 7.3 Schema validator examples

```javascript
const OUTPUT_SCHEMAS = {
  subtopicExpansion: {
    required: ['guaranteed_topics', 'suggested_essential', 'suggested_optional', 'current_topics', 'scope_notes']
  },
  deepAnalysis: {
    required: ['topics', 'definitions', 'formulas', 'pyqs', 'comparisons', 'examples', 'timelines', 'tables', 'key_facts']
  },
  generatedPart: {
    required: ['part_id', 'html_blocks', 'image_needed', 'citations', 'generation_summary']
  },
  currentAffairs: {
    required: ['query', 'grounding_status', 'fetched_at', 'results', 'disclaimer']
  }
};
```

## 7.4 Response-format repair

If the model returns near-valid but malformed JSON:

1. Do not silently manually parse it into state.
2. Use one controlled repair attempt with the original response and this exact non-canonical **provider-format wrapper**:

```text
Your previous response did not match the required JSON contract. Return the same intended content as valid JSON only. Do not add commentary, markdown fences, or new facts. Preserve all existing stable IDs and required fields.
```

3. The original canonical task prompt and output schema remain unchanged.
4. If repair fails, show standard retry modal.

---

# 8. State Commit Rules and Stale-Data Management

## 8.1 Commit only after validation

```javascript
function commitOperationOutput(operationId, output, execution, runtimeInput) {
  validateOutputForState(operationId, output);
  assertOutputMatchesCurrentPrerequisites(operationId, runtimeInput);
  applyStateMutation(operationId, output);
  persistState();
  renderAffectedUI(operationId);
}
```

## 8.2 Stale-state rules

| Change | Mark stale | Required UI behavior |
|---|---|---|
| Canonical source changes | Signals, deep analysis, bundles, parts, blueprints, generated output | Warn that complete downstream re-analysis is needed. |
| Global bundle selection changes | Per-part bundle assignments and blueprints not yet generated | Show affected parts; preserve deep analysis. |
| Part range/topic changes | That part’s blueprint and generated output | Show stale indicator; require re-blueprint before generate. |
| Part bundle changes | Affected blueprint section(s) and future output | Offer targeted blueprint update. |
| Blueprint text plan changes | Generated text and dependent image markers | Mark that part draft stale. |
| Blueprint image plan changes | Planned/generated image assets for that item | Mark only image item stale. |
| Generated text refined | Part approval and validation output | Return part to review/draft state. |
| Image replaced | Image validation status | Mark part validation stale. |
| CA refreshed | CA container/validation summary | Mark part validation stale. |
| Part removed | Consolidated coverage/final validation | Exclude from approval count/export. |
| New part added | Final validation | New part must be generated and approved. |

## 8.3 User override precedence

```text
User-edited source > parser/AI source output
User-approved subtopic list > AI-01A suggestions
User-selected bundle setting > AI-03C default state
User per-part bundle override > global inherited bundle
User selected image style > AI style recommendation
User edited final prompt for current run > non-edited final prompt
User manual text edit > later automatic patch unless user explicitly accepts overwrite
```

---

# 9. Deferred Context Enrichment Orchestration

Document 3 added `CTX-LOC`, `CTX-PER`, and `CTX-FORM`. This section defines exactly how to run them.

## 9.1 Execution decision

| Condition | Call required? |
|---|---:|
| Location merely appears once as a passing mention | No |
| Location is central/supporting and Geography bundle applies | CTX-LOC conditional |
| Person is central/supporting and Personality bundle applies | CTX-PER conditional |
| Formula is included in part and Formula Operations features apply | CTX-FORM conditional |
| Current fact needed by location/person context | Do not ground CTX prompt; generate/query through AI-07D |

## 9.2 Two valid implementation modes

| Mode | How it works | Required record |
|---|---|---|
| Separate subcalls | Execute CTX-LOC/PER/FORM before AI-07A; inject results into `{{PART_ANALYSIS_JSON}}` or named enrichment context | Each subcall has own prompt history and retry state. |
| Embedded sub-instructions | Insert exact canonical CTX prompt text as a sub-instruction inside final AI-07A task prompt; one model call creates notes and context | The final AI-07A prompt history must include embedded full CTX text and input data. |

**Preferred implementation:** Separate subcalls when the target is central/complex or reusable across parts. This improves caching, retry isolation, and auditability.

## 9.3 Cache keys

| Context prompt | Cache key | Cache invalidation |
|---|---|---|
| CTX-LOC | `location:{normalizedName}:{contextHash}:{sourceVersion}` | Source/context/part objective changes |
| CTX-PER | `person:{normalizedName}:{examContext}:{topicHash}:{sourceVersion}` | Source/exam/topic context changes |
| CTX-FORM | `formula:{formulaId}:{featuresHash}:{sourceVersion}` | Formula record/features/source changes |

---

# 10. Image Orchestration Rules

## 10.1 Unified image request object

Every path must normalize into this structure before AI-07B:

```javascript
{
  requestId: 'IR-001',
  source: 'blueprint|writer|post_review|validation|highlight',
  description: '',
  learningGoal: '',
  placementAnchor: '',
  styleHint: '',
  relatedPartId: '',
  userDirection: ''
}
```

## 10.2 Image generation sequence

```text
Create/receive image request
      ↓
Validate request + safe anchor
      ↓
Reserve image slot in state
      ↓
AI-07B detailed prompt expansion
      ↓
◇ preview-image-prompts setting enabled?
   ├── yes → user edits/approves final prompt
   └── no  → continue automatically
      ↓
AI-07C image provider request
      ↓
Validate returned asset/metadata
      ↓
Attach asset to reserved slot
      ↓
Mark image status generated / failed / needs_review
```

## 10.3 Image regeneration

| User action | Required final prompt behavior |
|---|---|
| Regenerate with no edit | Original final image prompt + canonical `REG-01`. |
| Edit prompt and regenerate | System prompt + user-edited task prompt + canonical `REG-02`. |
| Different style | Update style selection, rebuild AI-07B, then AI-07C. |
| Remove image | Remove asset/slot; mark validation stale if part was validated. |

---

# 11. Current-Affairs Orchestration Rules

## 11.1 CA execution sequence

```text
Blueprint CA query exists
       ↓
User Fetch CA OR Auto-Generate calls CA
       ↓
Validate editable query is non-empty
       ↓
AI-07D grounding ON
       ↓
Validate URL/date/publisher/status
       ↓
Store result with fetchedAt timestamp
       ↓
Render WEB_SOURCED CA block
       ↓
If user integrates into notes, revalidate affected part
```

## 11.2 Freshness rule

| Situation | Required behavior |
|---|---|
| CA query planned in Screen 5/6 | Do not execute yet. |
| User generates part later | Execute only if user chose auto-generate and CA is applicable. |
| CA results are older than configured freshness window | Display Refresh CA action. |
| Grounding unavailable | Show disclaimer; do not fake fresh result. |
| User edits CA query | Save user query and execute only that query on next fetch. |

---

# 12. Concurrency, Progress, and Rate Limits

## 12.1 Job queue types

| Queue | Operations | Concurrency rule |
|---|---|---|
| Analysis queue | AI-03A/B chunks; AI-03C bundle analysis | Chunk jobs may run limited parallel; preserve merge dependencies. |
| Blueprint queue | AI-05 parts | Start in staggered parallel sequence, ~1 second between launches. |
| Generation queue | AI-07A parts | User-triggered per part; Auto-Generate uses controlled parallelism based on provider rate limits. |
| Image queue | AI-07B/C | Separate asset queue; image failure cannot block notes. |
| CA queue | AI-07D | Limit concurrent grounded calls; preserve query→result association. |
| Validation queue | AI-07H sequential for Approve All | Must wait for user decision after each part popup. |

## 12.2 Required status model

```javascript
const JobStatus = {
  QUEUED: 'queued',
  RUNNING: 'running',
  RETRY_WAIT: 'retry_wait',
  SUCCEEDED: 'succeeded',
  FAILED: 'failed',
  SKIPPED: 'skipped',
  CANCELED: 'canceled',
  STALE: 'stale'
};
```

## 12.3 Progress rules

- Show operation-specific progress; never show fake completion.
- A blueprint card shows queued/generating/ready/failed individually.
- Auto-Generate All shows each part and its text/image/CA sub-status.
- Approve All shows `Validating Part X of Y` and waits for user choice per part.
- If one operation fails, display it without overwriting successful sibling results.

---

# 13. Retry and Error-Recovery Rules

## 13.1 Retry schedule

| Failure class | Automatic behavior | User options after retries |
|---|---|---|
| Temporary/provider error | Up to 2 retries with backoff, e.g. 2s then 4s | Retry As-Is / Edit / Skip / Cancel |
| Rate limit | Wait approximately 30s then retry once according to limits | Retry later / Skip / Cancel |
| Network | Retry on network restoration where possible | Retry / Skip / Cancel |
| Context/token length | Do not keep retrying same oversized input | Highlight Retry Simplified |
| JSON/schema error | One controlled response-format repair | Retry As-Is / Simplified / Edit / Skip / Cancel |
| Image asset error | Retry image only | Regenerate / edit prompt / different style / remove |

## 13.2 Failure modal requirements

```text
Failed operation: {{OPERATION_NAME}}
Reason: {{SAFE_ERROR_MESSAGE}}

Final executed prompt:
{{FINAL_PROMPT_EDITABLE_TEXTAREA}}

[Retry As-Is]
[Retry with Simplified Prompt]
[Retry with Edited Prompt]
[Skip This Item]
[Cancel]
```

- Context-limit errors visually prioritize Simplified Prompt.
- `Skip This Item` skips only bundle/part/image/query that failed.
- Never silently discard the final prompt, raw error, or partial successful outputs.

---

# 14. Prompt History, Auditability, and UI Transparency

## 14.1 Required prompt execution record

```javascript
{
  executionId: 'EX-...',
  operationId: 'AI-07A',
  promptVersion: '1.0',
  templateKey: 'AI_07A',
  systemKeys: ['SYS_01'],
  createdAt: 'ISO-8601',
  inputRefs: ['part:P-02', 'source:pages:6-10', 'blueprint:P-02:v3'],
  groundingEnabled: false,
  temperature: 0.4,
  maxOutputTokens: 15000,
  finalSystemInstruction: '...',
  finalTaskPrompt: '...',
  userEdited: false,
  retryOf: null,
  status: 'queued|running|success|failed|skipped',
  responseRef: 'generatedParts:P-02:v1',
  error: null
}
```

## 14.2 Prompt viewer rules

| Requirement | Behavior |
|---|---|
| Default display | Show final task prompt. |
| System toggle | User can expand Show System Instructions. |
| Copy | Copies current exact visible final prompt. |
| Edit | Editing creates a run-specific draft; does not mutate canonical template. |
| History | Current item retains prior execution records for review within session. |
| Match execution | Viewer must render saved executed record, not re-build a potentially different prompt on view. |

---

# 15. Safe Rendering and Anchor Rules

## 15.1 No direct model HTML injection

AI-07A safe content blocks are rendered only through application templates.

```javascript
function renderBlock(block) {
  assertAllowedContainerType(block.container_type);
  assertValidTraceability(block.traceability);
  const sanitizedText = sanitizeTextOrAllowlistedMarkup(block.safe_content);
  return renderApprovedContainer(block.container_type, sanitizedText, block);
}
```

## 15.2 Anchor requirements

| Rule | Required behavior |
|---|---|
| Stable anchors | Created by app from stable `partId`, `containerId`, or `headingId`. |
| AI references | AI may reference only anchors supplied in prompt or a newly specified controlled anchor pattern. |
| Validation | Before insertion, `documentState.hasAnchor(anchor)` must return true. |
| Missing anchor | Do not guess DOM location. Return image/request to correction/retry UI. |
| User manual edits | Anchor is retained outside editable text so later operations can find target safely. |

## 15.3 Quote/HTML prompt safety

- Prompt text must always be inserted into a textarea/text node, never raw `innerHTML`.
- Model output must not be interpolated inside inline event-handler attributes.
- User text containing quotes, `<script>`, or markup-like characters must remain text data.
- This addresses the previously discovered custom-image prompt escaping issue.

---

# 16. Operation Prerequisite Matrix

| Operation | Required prerequisites | Block condition |
|---|---|---|
| AI-01A | Topic exists | Empty topic |
| AI-01B | User-approved subtopic scope exists | Scope not approved |
| AI-02A | Failed technical extraction/raw text exists | No extraction content |
| AI-02B | AI-02A inadequate or user chose method C | No source/diagnostics |
| AI-03A | Canonical source exists | Empty source |
| AI-03B | AI-03A subject signals exist | Signals missing |
| AI-03C | Signals + deep analysis + routed bundles exist | Router not complete |
| AI-03D | User selected bundle exists | No requested bundle |
| AI-04 | Deep analysis + final global bundles available | Analysis incomplete |
| AI-05 | Confirmed part plan for target part | Part stale/unconfirmed |
| AI-06A/B | Current blueprint exists | No blueprint |
| AI-07A | Valid non-stale part + blueprint + source slice | Stale/missing plan |
| AI-07B | Valid normalized image request + anchor | Invalid/missing anchor |
| AI-07C | Valid expanded image prompt | Prompt missing |
| AI-07D | Valid CA query and part context | Empty query |
| AI-07E | Generated part exists | No generated part |
| AI-07F | Selected text + context/anchor exists | No selection |
| AI-07G | Generated part exists | No generated content |
| AI-07H | Generated part exists | No generated part |
| AI-07I | All non-removed parts approved | Any remaining required part unapproved |
| AI-07J | New topic or accepted suggestion exists | Empty topic/suggestion |
| AI-07K | Accepted validation image request exists | User has not accepted suggestion |

---

# 17. Implementation Test Plan

## 17.1 Prompt builder tests

- [ ] Every operation resolves correct canonical system prompt(s).
- [ ] Every declared placeholder is replaced; unresolved placeholder blocks execution.
- [ ] Prompt builder does not mutate `DEFAULT_PROMPTS`.
- [ ] Grounding flag is false for disallowed calls even if generic app state requests web.
- [ ] AI-07D grounding flag is true.
- [ ] Final prompt record is saved before model call.
- [ ] User edited final prompt changes one run only.

## 17.2 Context tests

- [ ] AI-07A gets only target part source slice, not whole source document.
- [ ] AI-07A gets all definitions/formulas registry.
- [ ] AI-07A gets only relevant PYQs/examples/timelines/tables.
- [ ] AI-05 gets target part plan and source slice.
- [ ] AI-03C gets only routed bundle fragments.
- [ ] Force-enable invokes selected fragment only.
- [ ] Large source activates chunking and structured merge.

## 17.3 Output safety tests

- [ ] Malformed JSON never changes state.
- [ ] Unknown container type is rejected.
- [ ] Invalid anchor cannot insert an image.
- [ ] User prompt containing quotes or HTML does not break UI.
- [ ] `WEB_SOURCED` result without URL is rejected as verified web content.
- [ ] Raw model script/event attributes do not render.

## 17.4 Flow tests

- [ ] AI Draft: expand → user approve → draft → edit → Stage 3 source uses edited content.
- [ ] Stage 3 routing → force-enable → part assignment → blueprint → generation chain works.
- [ ] Formula from later part is available in earlier part generation via global formula registry.
- [ ] Blueprint image request and validation image request use same insertion chain.
- [ ] CA stays deferred until fetch/auto-generate action.
- [ ] Per-part approval invokes one combined validation call.
- [ ] Approve All pauses for each user validation decision.
- [ ] Final validation suggestion adds part through quick blueprint flow.
- [ ] Export triggers no AI request.

---

# 18. Runtime Validation Summary

This implementation specification was checked against Documents 1–3.

| Check | Status |
|---|---|
| Prompt use remains canonical and immutable | Pass |
| All runtime operations have assembly/configuration behavior | Pass |
| Token/context strategy matches semantic chunking decision | Pass |
| Grounding policy matches agreed restricted usage | Pass |
| Added deferred location/person/formula prompts have execution rules | Pass |
| Image/CA/validation flow matches dependency map | Pass |
| Retry rules preserve canonical prompt wording | Pass |
| Prompt transparency and audit requirements are explicit | Pass |
| Safe HTML/anchor rules address known rendering risks | Pass |
| Stage 8 correctly uses no AI | Pass |

---

## End of Document 4

**Next planned document:** Document 5 — Missing Features & Agreed Amendments Register: original-plan comparison, user-demands/developer-discovered gaps, decisions, priority, implementation impact, and documentation insertions.

---

# Amendment 1 — Additions After Comparison with Supplied Runtime-Rules Draft

## A. Review outcome

The supplied runtime-rules draft was compared with this implementation specification. The following useful operational controls are adopted in this amendment:

- explicit model profile and provider fallback rules;
- `topP` configuration;
- safety-block classification;
- operation-specific cache keys and TTLs;
- session persistence and user cancellation rules;
- cost/usage telemetry and a developer diagnostics panel;
- performance target table;
- more exact fallback/degradation behaviors.

The following supplied items are intentionally not adopted unchanged because they conflict with the agreed architecture or can damage source integrity:

| Supplied item | Reason | Canonical rule retained |
|---|---|---|
| Subject-detection fallback marks all signals medium/detected | This would falsely enable irrelevant bundles and cause hallucination. | On failure, allow manual subject/bundle selection; mark AI detection unavailable. |
| Deep-extraction fallback silently performs a smaller extraction | Downstream stages would treat incomplete analysis as complete. | Mark analysis incomplete, show affected features unavailable, and require user retry/manual route. |
| Part-writer returns raw HTML directly | Quote/escaping/XSS issue was already found; unsafe. | Return structured safe blocks; application renderer builds HTML. |
| Normal writing always adds newest metrics/India comparisons/state facts | Grounding is off in normal writing, and relevance varies. | Fresh facts only via AI-07D; state/international comparison only when relevant. |
| First/middle/last sample instead of semantic chunks for large source | Loses large sections and breaks completeness. | Semantic chunking and structured merge remain mandatory. |
| Reject “SQL-injection-like” user text | An academic source may legitimately contain SQL/code. | Treat input as text and render safely; do not reject educational content based on word patterns. |

---

## B. Model Profile and Provider Fallback

```javascript
const MODEL_PROFILE = Object.freeze({
  primaryTextModel: 'gemini-3-flash-preview',
  primaryImageModel: 'gemini-native-image',
  fallbackTextModel: 'configured_previous_stable_text_model',
  fallbackImageModel: 'configured_previous_stable_image_model',
  defaultTopP: 0.9,
  maxParallelCalls: 5,
  maxCallsPerMinute: 60,
  maxTokensPerMinute: 100000
});
```

### B.1 Model selection rules

| Operation class | Primary model | Fallback behavior |
|---|---|---|
| Text analysis, extraction, split, blueprint, writing, validation | `gemini-3-flash-preview` or the current approved fast text model | After configured retries fail due to provider/model availability—not prompt/data error—retry through approved stable text model and record model switch. |
| Image generation | `gemini-native-image` | Use approved stable image model only if image provider is unavailable; preserve exact final image prompt. |
| Grounded CA | Approved Gemini text model with grounding enabled | If grounding feature is unavailable, return `grounding_status=unavailable` / disclaimer. Do not silently use a different search API or fabricate fresh web sources. |

### B.2 Model switch audit rule

Any model fallback must create this execution-history field:

```json
{
  "model_requested": "gemini-3-flash-preview",
  "model_used": "configured_previous_stable_text_model",
  "model_switch_reason": "primary provider unavailable after retry policy"
}
```

No model switch is allowed for a content/safety/schema error unless user explicitly retries after editing the prompt.

---

## C. Top-P Configuration Amendment

Add `topP` to every `PROMPT_CONFIG` entry. Use the following canonical values.

| Operation | Top-P |
|---|---:|
| AI-01A | 0.9 |
| AI-01B | 0.9 |
| AI-02A | 0.8 |
| AI-02B | 0.8 |
| AI-03A | 0.7 |
| AI-03B | 0.8 |
| AI-03C | 0.9 |
| AI-03D | 0.9 |
| AI-04 | 0.8 |
| AI-05 | 0.9 |
| AI-06A | 0.9 |
| AI-06B | 0.9 |
| AI-07A | 0.9 |
| AI-07B | 0.9 |
| AI-07D | 0.7 |
| AI-07E | 0.8 |
| AI-07F | 0.9 |
| AI-07G | 0.9 |
| AI-07H | 0.7 |
| AI-07I | 0.8 |
| AI-07J | 0.9 |
| AI-07K | 0.8 |

Provider request fields must record `temperature`, `topP`, maximum output tokens, grounding state, and actual model used.

---

## D. Universal Error Classification Amendment

```javascript
function classifyError(error) {
  const message = String(error?.message || error).toLowerCase();
  if (/(context|token|length|limit)/.test(message)) return 'context_limit';
  if (/(rate limit|quota|resource exhausted)/.test(message)) return 'rate_limit';
  if (/(network|timeout|connection|offline)/.test(message)) return 'network';
  if (/(safety|blocked|policy)/.test(message)) return 'safety_block';
  if (/(json|parse|schema|structured output)/.test(message)) return 'format_error';
  return 'unknown';
}
```

| Error class | Automatic action | User-facing action |
|---|---|---|
| `context_limit` | Do not repeat oversized request endlessly; prepare simplified context path | Highlight Retry with Simplified Prompt |
| `rate_limit` | Wait ~30 seconds then retry within retry allowance | Show waiting/progress status |
| `network` | Pause until connection returns where feasible, then retry | Show reconnect state; allow cancel |
| `safety_block` | No automatic retry and no provider-model switch | Show clear safe error; user must edit prompt, skip, or cancel |
| `format_error` | One controlled JSON-format repair attempt | If repair fails, standard retry modal |
| `unknown` | Standard 2-second then 4-second retries | Standard recovery modal |

---

## E. Cache Specification Amendment

> Cache keys must include prompt version and relevant source/context version. A cache hit must restore the saved output **and** prompt history record; it must not pretend a new model call happened.

| Output | Cache key | TTL | Invalidate when |
|---|---|---:|---|
| AI-01A sub-topic expansion | `promptVersion + topic + userSubtopicsHash + exam + state + depth + internetFlag` | 7 days | Any input field changes |
| AI-01B draft material | `promptVersion + topic + approvedTopicsHash + depth + exam + state + CAFlag + internetFlag` | 24 hours | Any input changes; current/web mode age requires fresh run |
| AI-02A cleanup | `fileHash + extractionHash + promptVersion` | Session | Source/file is changed or reprocessed |
| AI-02B restructure | `fileHash + cleanedTextHash + promptVersion` | Session | Source/file is changed or reprocessed |
| AI-03A signals | `canonicalSourceHash + promptVersion` | 30 days | Canonical source changes |
| AI-03B deep analysis | `canonicalSourceHash + subjectSignalsHash + promptVersion` | 30 days | Canonical source or detection context changes |
| AI-03C bundle analysis | `canonicalSourceHash + routedBundleHash + promptVersion` | 30 days | Source or routing/bundle definition changes |
| AI-03D force-enable | `canonicalSourceHash + requestedBundleId + promptVersion` | 30 days | Source changes |
| AI-04 split | `deepAnalysisHash + globalBundleHash + sourceScopeHash + promptVersion` | 7 days | Part plan manually changed or upstream analysis changes |
| AI-05 blueprint | `partHash + partAnalysisHash + bundleHash + promptVersion` | 7 days | Part/source/bundle/blueprint changes |
| AI-06A/B edit output | No persistent response cache | N/A | Each instruction is unique; retain undo/history only |
| AI-07A generated part | `partHash + blueprintHash + sourceSliceHash + bundleHash + promptVersion` | Session or persisted session state | Any part/blueprint/source/bundle/user edit change |
| AI-07B image prompt | `imageRequestHash + styleHash + localContextHash + promptVersion` | Session | User changes prompt/style/direction |
| AI-07C image asset | `expandedImagePromptHash + imageModel` | Session | User explicitly regenerates or changes prompt |
| AI-07D CA | `normalizedQuery + currentDateDay + stateFocus + promptVersion` | 24 hours | TTL expiry or user refresh |
| CTX-LOC | `location + contextHash + sourceVersion` | 30 days | Context/source changes or manual refresh |
| CTX-PER | `person + examContext + topicHash + sourceVersion` | 30 days | Context/source changes or manual refresh |
| CTX-FORM | `formulaId + operationFeaturesHash + sourceVersion` | 30 days | Formula/features/source changes |
| AI-07H validation | `partContentHash + imageHash + CAHash + blueprintHash + promptVersion` | Session | Any part asset/content change |
| AI-07I final validation | `approvedDocumentHash + blueprintCoverageHash + promptVersion` | Session | Any approved part changes/adds/removes |
| AI-07J quick blueprint | `newTopic + subtopicsHash + globalBundleHash + promptVersion` | Session | User changes topic/settings |

### E.1 Cache storage policy

- Store lightweight structured outputs and metadata in localStorage only while quota permits.
- Large text, images, and verbose prompt history must use an indexed/local persistence strategy appropriate to implementation, or remain session-limited.
- If storage is full, preserve the current user-visible state first; show a non-blocking notice that older cached data cannot be retained.
- Never cache grounded CA beyond its TTL as “current.”

---

## F. User Cancellation and Session Persistence Amendment

### F.1 Cancellation rules

| User action | Required behavior |
|---|---|
| Cancel a queued job | Mark `canceled`; do not call model. |
| Cancel a running job | Abort provider request if provider supports it; otherwise ignore response if execution token no longer active. |
| Cancel during retry wait | Clear scheduled retry; mark canceled. |
| Cancel blueprint parallel job | Cancel only selected part; do not cancel sibling parts. |
| Cancel Approve All sequence | Preserve decisions already made; stop before next part. |
| Cancel image generation | Keep reserved slot as failed/canceled; do not remove surrounding text. |

Canceled jobs are never retried automatically. Do not commit partial model output unless it passed complete schema validation before cancellation.

### F.2 Session persistence rules

Persist immediately after each validated state transition:

- canonical source and source version;
- analysis objects;
- final global/per-part bundle selections;
- parts and blueprints;
- generated safe blocks and asset metadata;
- approvals and validation records;
- prompt execution history metadata;
- job statuses where resuming is meaningful.

Every persisted state must have `schemaVersion`. On version mismatch, migrate safely or show a clear “session version unsupported” state—never silently corrupt current work.

---

## G. Cost, Performance, Monitoring, and Diagnostics Amendment

### G.1 Session telemetry

Track locally for every request:

```json
{
  "timestamp": "",
  "execution_id": "",
  "operation_id": "",
  "model_used": "",
  "grounding_enabled": false,
  "cache": "hit|miss",
  "input_token_estimate": 0,
  "output_token_estimate": 0,
  "latency_ms": 0,
  "retry_count": 0,
  "status": "success|failed|skipped|canceled",
  "error_class": null
}
```

A session cost estimate may be shown only as an **optional user/developer setting**, clearly labelled estimated. It must not block study flow.

### G.2 Developer diagnostics panel

Provide an optional developer-only/session diagnostics view with:

- operation ID and timestamp;
- cache hit/miss;
- prompt size estimate and output size;
- actual model and grounding state;
- latency/retry count/error class;
- final prompt viewer link;
- input-reference list, not raw private data by default.

### G.3 Target performance benchmarks

| Operation | Target latency | Measurement condition |
|---|---:|---|
| AI-01A scope expansion | 5–10s | Normal topic request |
| AI-01B medium draft | 30–60s | Medium depth |
| AI-01B comprehensive draft | 60–120s | Comprehensive depth |
| AI-03A signal detection | 5–10s | Safe whole source/chunk |
| AI-03B deep extraction | 15–30s | Typical chunk/document |
| AI-03C routed bundles | 15–30s | Typical relevant bundle set |
| AI-04 split | 5–15s | Typical analysis |
| AI-05 one blueprint | 15–30s | One part |
| AI-05 six staggered parallel blueprints | 20–40s | Provider/rate-limit dependent |
| AI-06 targeted modification | 5–15s | One blueprint section |
| AI-07A part generation | 30–90s | Normal part size |
| AI-07B image prompt | 3–8s | One request |
| AI-07C image | 10–30s | Provider dependent |
| AI-07D CA grounded research | 15–30s | One part query batch |
| CTX enrichment | 5–15s | One entity/formula |
| AI-07H part validation | 10–20s | One part |
| AI-07I final validation | 15–40s | Approved document size dependent |

Targets are performance goals, not fake progress values. The app must record actual measured values.

---

## H. Fallback and Graceful-Degradation Matrix

| Operation class | If all retries fail | User can still do |
|---|---|---|
| AI-01A scope expansion | Display original user sub-topics only | Manually add/edit topics and continue to AI-01B |
| AI-01B draft generation | Keep source area editable and show prompt/error | Retry/edit prompt or paste source manually |
| AI-02A/AI-02B extraction | Preserve best available text and diagnostics | Paste corrected text manually or proceed with warning where usable |
| AI-03A detection | Mark detection unavailable; do not fabricate signals | User manually selects subject/bundles; then retry analysis |
| AI-03B extraction | Mark analysis incomplete | Retry; user may proceed only with clearly limited/manual planning flow |
| AI-03C bundle analysis | Leave bundles available for user force-enable | Continue with manual selections; show incomplete detection warning |
| AI-04 splitting | Generate deterministic page/topic-based provisional split | User edits/adds/merges manually before blueprint |
| AI-05 one blueprint | Mark only that part failed | Retry that part or create/edit blueprint manually |
| AI-06 edit/refinement | Preserve current blueprint/content unchanged | Rephrase or edit manually |
| AI-07A part writing | Do not fabricate partial completed part | Retry/edit prompt, skip part, or write/edit manually |
| AI-07B image prompt | Use original approved image request as an editable fallback prompt | User can edit then send to AI-07C |
| AI-07C image | Keep text; show failed image slot | Retry, different style, edit prompt, or remove |
| AI-07D CA | Show unavailable/disclaimer; preserve query | Refresh later, skip CA, or enter user-supplied info with correct tag |
| CTX location/person/formula | Use source-only/basic mention; do not invent enrichment | Retry/manual addition |
| AI-07H validation | Keep part unapproved by default | Retry, or user explicitly chooses approve-as-is with warning |
| AI-07I final validation | Allow user to export after explicit skip/warning | Retry later or export current approved document |

---

## I. Amendment Validation

This amendment was checked after insertion.

| Check | Result |
|---|---|
| Model profile and fallback controls added | Pass |
| Top-P added without changing canonical prompt text | Pass |
| Error safety handling added | Pass |
| Cache keys/TTL/invalidation rules added | Pass |
| Cancellation and persistence rules added | Pass |
| Diagnostics and real performance measurements added | Pass |
| Grounding and source-integrity restrictions retained | Pass |
| Unsafe raw-HTML and fake-detection fallbacks rejected | Pass |

## End of Amendment 1
