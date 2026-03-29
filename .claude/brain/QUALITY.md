# Quality Standards

Universal engineering standards for this repository.

## Scope discipline

- Make only requested changes plus required supporting updates.
- Do not add unrelated features or broad refactors.

## Read before write

- Never edit a file before reading it.
- Match existing naming and structure patterns.

## Security

Do not introduce:

- Unsafe rendering of untrusted content
- Unsanitized input flows to shell/file/database operations
- Hardcoded secrets

## Contract stability

- Keep API/data/UI contracts stable unless intentionally changed.
- Document intentional contract changes in the same PR.

## Validation

Run relevant checks after changes:

```bash
# Tests
python -m pytest tests/ -v

# Smoke check (starts server, verify manually)
python app.py
```

No linter is configured. If checks cannot be run, state what was not verified.

## Engine-specific rules

- All dice functions must accept an optional `rng` parameter.
- Never use global random state in tests — always pass `random.Random(seed)`.
- Base Risk probabilities must hold when no upgrades are active.
- Validate balance changes against exact Taflin matrices via `probabilities.py`.
