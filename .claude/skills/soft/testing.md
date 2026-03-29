# Zone: Testing (`tests/`)

```contract
requires:
  - .claude/brain/QUALITY.md

inputs:
  change_scope: modified files and impacted zones

produces:
  verification_plan: checks to run
  evidence: pass/fail outcomes and blockers

pre-gate:
  - modified files are known
  - relevant test files are identified

post-gate:
  - relevant checks were run when available
  - unverified areas are explicitly called out
```

Use after any engine or API change.

## File map

```text
tests/
  test_dice.py         — Dice rolling, RNG injection
  test_combat.py       — round resolution, battle resolution
  test_heroes.py       — hero die replacement behavior
  test_structures.py   — damage absorption, Orbital Battery
  test_probabilities.py — Taflin matrix validation, Markov chain results
```

## Conventions

- Framework: pytest.
- All tests use `random.Random(seed)` — never rely on global random state.
- Probability tests use `fractions.Fraction` for exact comparisons.
- Monte Carlo tests cross-check against exact Taflin results — tolerance should be explicit and documented.
- Run: `python -m pytest tests/ -v`

## Verification strategy

- Run the full suite after any engine change.
- After balance tuning (hero/structure values), also run a Monte Carlo spot-check via `engine/simulation.py`.
- After Flask changes, manually verify the UI if automated endpoint tests don't exist.
- Record failures with the exact pytest output — do not paraphrase errors.
