# Galactic Conquest — Agent Instructions

## Modes

You operate in distinct modes:

### MODE A — EXPLAIN (default)

Goal: minimize total tokens to understanding.

- Answer directly and concisely.
- Use analogies only when they genuinely clarify complex concepts.
- Spend tokens only to prevent likely follow-up questions.
- Avoid verbose or tutorial-style explanations.
- Avoid filler or meta-offers (e.g., "just say the word", "if you want me to…"). Only suggest next steps when asked.

### MODE B — PLAN

Goal: define a clear, approved approach before implementation.

- Use for non-trivial work only (multi-file, architectural, or unclear requirements).
- Present approach options if multiple valid paths exist.
- Get user approval before implementing.
- Skip for simple/obvious changes.

### MODE C — DEVELOP (when writing code)

Goal: correctness and coverage, not minimal tokens.

- Write clear, complete, production-ready code.
- Include necessary structure for testing and maintainability.
- Do NOT sacrifice correctness, edge cases, or testability to save tokens.
- Add comments only for: security-critical code, non-obvious algorithms, or "why" decisions that aren't clear from the code itself.
- After code changes, briefly state what changed and why that approach was chosen (1-2 sentences).
- Don't narrate every tool call or explain obvious actions.

### MODE D — TEST

Goal: verify correctness and surface failures early.

- Run automated tests if they exist.
- Backend: pytest (unit + integration as needed).
- Frontend: manual verification documented in response (automated tests later if needed).
- If tests fail, return to DEVELOP.

### MODE E — DOCUMENT

Goal: capture reusable patterns and architectural decisions.

- Create/update pattern docs when:
  - New reusable pattern emerges (e.g., "two-level zoom interaction")
  - Existing pattern changes significantly
  - Architectural decision is made that should guide future work
- Don't document one-off implementations or obvious/standard practices.

### Rules

- If no mode is specified, assume EXPLAIN.
- Never mix modes in the same response unless explicitly told.
- When switching modes, state the mode in one short line.
- Mode switching is automatic: if you're writing/editing code, you're in DEVELOP mode.

### Formatting

- EXPLAIN → Direct answers. Use analogies sparingly when they add real value.
- PLAN → Short, ordered plan with approval prompt.
- DEVELOP → Code first, brief context after.
- TEST → Test command(s) + results; if not run, state why.
- DOCUMENT → Doc changes first, brief context after.

---

## Zone Dispatch

Before working in any area, load the zone soft skill first.

| Working in... | Read | Purpose |
| - | - | - |
| `engine/` | `.claude/skills/soft/engine.md` | Game engine logic, combat model, RNG patterns |
| `app.py`, `templates/`, `static/` | `.claude/skills/soft/frontend.md` | Flask app, UI, API endpoints |
| `tests/` | `.claude/skills/soft/testing.md` | Test patterns, pytest conventions |
| `docs/` | N/A | Pattern docs — update per MODE E rules |

See `.claude/skills/hard/combat-balance.md` for balance tuning procedures.

---

## Project: Galactic Conquest

**Type:** Python project (3.13+)
**Framework:** Vercel serverless (Python 3.12 runtime) + static HTML frontend
**Purpose:** Risk-style sci-fi strategy game — battle system prototype with web UI for simulation and balance testing

### Tech Stack

- **Language:** Python 3.13 (local), Python 3.12 (Vercel runtime)
- **Web:** Vercel serverless functions (`api/*.py`), vanilla JS frontend, static HTML/CSS
- **Testing:** pytest
- **Dependencies:** See `requirements.txt`

### Project Structure

```text
engine/           # Core game engine (no web framework dependency)
  models.py       # Dataclasses: Hero, Structure, Army, RoundResult, BattleResult
  dice.py         # Dice rolling with RNG injection for deterministic testing
  heroes.py       # Hero tier definitions, roll_with_hero()
  structures.py   # Defensive structure definitions, damage_absorbed(), extra_defender_dice()
  combat.py       # resolve_single_round(), resolve_battle()
  probabilities.py # Taflin exact probability matrices, Markov chain solver
  simulation.py   # Monte Carlo simulation runner (SimulationConfig, run_simulation)
_shared.py        # Shared helpers: _parse_army, _parse_tuning, send_json, read_json_body, spec builders
api/              # Vercel serverless functions (each file = one endpoint)
  config.py       # GET  /api/config   — hero tiers, structures, slider specs
  battle.py       # POST /api/battle   — full battle resolution
  round.py        # POST /api/round    — single round resolution
  simulate.py     # POST /api/simulate — Monte Carlo simulation
  exact.py        # POST /api/exact    — Taflin exact probabilities
index.html        # Static single-page UI; fetches /api/config on load to build the UI
style.css         # Dark theme styling
vercel.json       # Vercel config (Python 3.12 runtime for api/*.py)
tests/            # pytest test suite
  test_dice.py
  test_combat.py
  test_heroes.py
  test_structures.py
  test_probabilities.py
docs/
  combat-design.md # Full combat design brief
```

### Architecture & Design Decisions

**Role separation:**
- **Attackers** get heroes/commanders (die upgrades: d8/d10/d12 replacing one d6)
- **Defenders** get planetary structures (damage absorption, extra dice)
- Defender never gets a hero. Attacker never gets structures.

**Combat model:**
- Standard Risk dice: attacker up to 3d6, defender up to 2d6, compare sorted pairs, defender wins ties
- Hero die replaces ONE of the attacker's 3 dice (not an extra die)
- Structures use a damage-absorption model: absorb N defender losses per round (not dice manipulation)
- Orbital Battery grants +1 defender die

**Design philosophy:**
- Base Risk probabilities must be preserved when no upgrades are active
- Structures should "blunt the damage, not disallow it" — defenders take punches, not dodge them
- End-game fully upgraded attacker vs fully upgraded defender should approach 50/50
- System must be easily tweakable for balance iteration

**RNG injection pattern:**
- All dice functions accept an optional `rng` parameter (default: `random` module)
- Pass `random.Random(seed)` for deterministic tests
- Never use global random state in tests

**Probability validation:**
- Engine validated against Daniel Taflin (2001) exact Risk probability matrices
- `probabilities.py` implements Markov chain DP solver using `fractions.Fraction` for exact arithmetic
- Monte Carlo simulations cross-checked against exact solutions

### Running

```bash
# Run tests
python -m pytest tests/ -v

# Local dev: Vercel CLI (recommended)
vercel dev
# Opens at http://localhost:3000

# Or serve static files manually (API endpoints won't work)
python -m http.server 8000

# Quick balance simulation (Python REPL)
from engine.simulation import SimulationConfig, run_simulation
from engine.models import Hero
cfg = SimulationConfig(attacker_units=10, defender_units=10, attacker_hero=Hero("admiral", 12))
result = run_simulation(cfg)
```

### Current Balance Status

**Attacker tuning:**
- Captain (d8): ~72% win rate at 10v10 — moderate upgrade
- General (d10): ~86% win rate at 10v10 — strong upgrade
- Admiral (d12): ~92% win rate at 10v10 — dominant, needs counterplay

**Defender tuning:**
- Shield Generator (absorb 1/round): too strong — 0% attacker win at 10v10
- Fortress (absorb 1/round): too strong — 0% attacker win at 10v10
- Orbital Battery (+1 die): ~11% attacker win at 10v10 — strong but beatable

**Active work:** Tuning absorption values and making the engine more data-driven with UI sliders for balance iteration

---

## Development Workflow

| Step | Purpose | Mode |
| - | - | - |
| Intake | Receive request, identify scope (trivial vs non-trivial). | EXPLAIN |
| Discovery | Check `docs/patterns/` for relevant patterns; note gaps. | EXPLAIN |
| Plan | Required for multi-file/architectural/unclear work; present options and get approval. | PLAN |
| Develop | Implement changes following existing patterns. | DEVELOP |
| Test | Run automated tests; if failures, return to Develop. | TEST |
| Iterate | Develop → Test until satisfactory. | DEVELOP / TEST |
| Document | Update pattern docs when needed (see MODE E rules). | DOCUMENT |

Update CLAUDE.md only when workflow or mode rules need to change.

---

## Pattern Documentation Structure

Location: `docs/patterns/{domain}-{pattern}.md`

Template:

```markdown
# {Domain}: {Pattern Name}

## Context
When and why to use this pattern

## Implementation
Code approach with key technical decisions explained

## Trade-offs
What this approach optimizes for and what it sacrifices

## Examples
References to actual implementations (file:line)

## Updated
YYYY-MM-DD: Brief changelog of what changed
```

Deprecated patterns:
- Prefix filename with `DEPRECATED-`
- Add migration path in doc
- Keep for reference, don't delete
