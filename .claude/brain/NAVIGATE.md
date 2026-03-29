# Navigation State Machine

Context loading is a state machine with blocking gates.

```text
ENTRY -> ZONE_LOADED -> SKILL_IDENTIFIED -> READY -> EXECUTING -> DONE
```

## ENTRY

- Load `.claude/CLAUDE.md`.
- Identify impacted zone(s).

## ZONE_LOADED

- Load zone soft skill(s) from dispatch.
- Satisfy each soft-skill contract.

## SKILL_IDENTIFIED

- Load applicable hard skill(s) if present.
- Confirm procedure, preconditions, and postconditions.

## READY

- Read every file that will be modified.
- Confirm no unresolved structure surprises.

Never skip READY.

## EXECUTING

- Apply active mode from `.claude/AGENTS.md`.
- Implement and validate against postconditions.

## DONE

- Deliver result.
- If reusable gaps were found, update skills/contracts.

## Cross-zone sequence

When work spans multiple zones, default to:

1. `engine/` model/data changes
2. `app.py` API changes
3. `templates/` + `static/` UI integration
4. `tests/` verification
