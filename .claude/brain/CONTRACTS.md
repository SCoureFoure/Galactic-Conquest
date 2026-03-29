# Contract System

Contracts are blocking interfaces for skill files.

## Contract block format

```contract
requires:
  - .claude/CLAUDE.md

inputs:
  task: scoped user request
  zone: impacted code area

produces:
  file_map: relevant files and responsibilities
  conventions: rules to apply
  checks: validation commands and smoke tests

pre-gate:
  - Required context is loaded
  - Task scope is clear

post-gate:
  - Relevant files are identified
  - Applicable conventions are known
  - Validation plan is known
```

## Enforcement rules

- Failed pre-gate: stop and load missing context.
- Failed post-gate: re-read or clarify before execution.
- Do not satisfy gates by guessing.

## Contract inheritance

`requires` creates a typed dependency chain:

```text
CLAUDE.md -> soft skill -> hard skill -> execution
```

## Update rule

Update contracts only when real failure modes show missing or weak gates.
