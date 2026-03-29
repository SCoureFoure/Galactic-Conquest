# Hard Skill: Combat Balance Tuning

```contract
requires:
  - .claude/skills/soft/engine.md

inputs:
  target: hero tier values, structure absorption values, or Orbital Battery behavior
  balance_goal: desired win-rate range for attacker vs defender

produces:
  changes: updated values in heroes.py, structures.py, or combat.py
  verification: Monte Carlo win rates + exact probability cross-check

pre-gate:
  - target files read (heroes.py, structures.py, combat.py, probabilities.py)
  - current win-rate baseline known (see CLAUDE.md balance status)
  - balance goal is stated (e.g., "Admiral at 10v10 should be ~70%")

post-gate:
  - tests pass (python -m pytest tests/ -v)
  - Monte Carlo results match stated goal within acceptable tolerance
  - base Risk probabilities still hold with no upgrades active
```

## Design constraints

- Base Risk probabilities are **locked** — verify via `probabilities.py` after any combat.py change.
- Structures blunt damage, they do not prevent it — absorption values must not reach "0% attacker win".
- End-game ceiling: fully upgraded attacker vs fully upgraded defender should approach 50/50.
- Hero die replaces one d6, never adds a die.

## Procedure

1. Read `heroes.py`, `structures.py`, `combat.py` to understand current values.
2. Run a baseline simulation: `SimulationConfig(attacker_units=10, defender_units=10, ...)`.
3. Adjust the target value (die size, absorption amount).
4. Re-run simulation to check win rate.
5. Verify base case: `SimulationConfig(attacker_units=10, defender_units=10)` (no hero, no structure) should match Taflin ~41.5% attacker win at 10v10.
6. Run `python -m pytest tests/ -v` — all must pass.
7. Update balance status in `CLAUDE.md` if numbers changed materially.

## Current balance targets

| Matchup | Target attacker win | Notes |
| - | - | - |
| 10v10 no upgrades | ~41.5% | Taflin baseline — do not change |
| 10v10 Captain (d8) | ~65-75% | Moderate upgrade |
| 10v10 General (d10) | ~80-88% | Strong but counterplayable |
| 10v10 Admiral (d12) | ~70-80% | Needs to come down — currently ~92% |
| 10v10 Orbital Battery | ~20-35% | Strong defender edge, not unbeatable |
| 10v10 Admiral vs Orbital Battery | ~45-55% | End-game equilibrium target |
