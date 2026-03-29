# Zone: Game Engine (`engine/`)

```contract
requires:
  - .claude/CLAUDE.md
  - .claude/brain/QUALITY.md

inputs:
  task: request touching combat logic, dice, heroes, structures, or simulation

produces:
  file_map: relevant engine files
  conventions: engine-local rules
  hard_skills: applicable hard skills

pre-gate:
  - zone identified as engine/
  - task scope clear

post-gate:
  - relevant files can be named
  - RNG injection pattern understood
  - validation approach known
```

You are working in the core game engine — no Flask dependency. All logic here must be independently testable.

## File map

```text
engine/
  models.py       — Dataclasses: Hero, Structure, Army, RoundResult, BattleResult
  dice.py         — Dice rolling; all functions accept optional rng parameter
  heroes.py       — Hero tier definitions (Captain d8, General d10, Admiral d12); roll_with_hero()
  structures.py   — Structure definitions; damage_absorbed(), extra_defender_dice()
  combat.py       — resolve_single_round(), resolve_battle()
  probabilities.py — Taflin exact probability matrices; Markov chain DP solver (fractions.Fraction)
  simulation.py   — Monte Carlo runner: SimulationConfig, run_simulation()
```

## Conventions

- All dice functions accept an optional `rng` parameter (default: `random` module).
- Never use global random state — always inject `random.Random(seed)` in tests.
- Hero die **replaces** one of the attacker's 3 dice; it is not an extra die.
- Structures use damage-absorption (absorb N losses/round), not dice manipulation.
- Orbital Battery is the one exception: grants +1 defender die.
- Base Risk probabilities must hold when no upgrades are active — validate against `probabilities.py`.
- Attacker role: heroes only. Defender role: structures only. Never mix.

## Hard skills

- `.claude/skills/hard/combat-balance.md` — tuning hero/structure values for balance targets
