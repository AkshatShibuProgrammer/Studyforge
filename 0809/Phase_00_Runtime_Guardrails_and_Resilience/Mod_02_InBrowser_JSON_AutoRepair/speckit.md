# Speckit Workflow Manifest: Mod_02_InBrowser_JSON_AutoRepair

## Metadata
- **Module ID**: `Mod_02_InBrowser_JSON_AutoRepair`
- **Parent Phase**: `[Runtime Guardrails & Resilience](../speckit.md)`
- **Governing Constitution**: [constitution.md](constitution.md)

## Speckit Commands
- `/speckit-constitution`: Local module boundaries and invariants.
- `/speckit-specify`: [specify.md](specify.md) & [spec.md](spec.md)
- `/speckit-clarify`: Edge case resolutions and error boundary definitions.
- `/speckit-plan`: [plan.md](plan.md)
- `/speckit-tasks`: [tasks.md](tasks.md)
- `/speckit-implement`: Live code integration in `sindhuskeleton.html`.

## Module Responsibilities
Deterministic bracket stack repair and quote closure for truncated 8192-token streaming responses.

## Quality Gate Checklist
- [x] Typed contract definitions verified in [contracts.md](contracts.md)
- [x] Zero external npm/CDN runtime dependencies
- [x] Deterministic error recovery
