# Zone: Serverless API & UI (`api/`, `index.html`, `style.css`)

```contract
requires:
  - .claude/CLAUDE.md
  - .claude/brain/QUALITY.md

inputs:
  task: request touching API endpoints, static HTML, or CSS styling

produces:
  file_map: relevant frontend files
  conventions: frontend-local rules
  hard_skills: applicable hard skills

pre-gate:
  - zone identified as api/, index.html, or style.css
  - task scope clear

post-gate:
  - relevant files can be named
  - API contract understood
  - no unsafe rendering introduced
```

You are working in the serverless web layer — Vercel Python functions for the API and a static HTML/JS frontend.

## File map

```text
_shared.py        — Shared helpers at project root: _parse_army, _parse_tuning, send_json,
                    read_json_body, slider/mode spec builders, structures_config()
api/
  config.py       — GET  /api/config   — returns hero tiers, structures, slider specs
  battle.py       — POST /api/battle   — full battle resolution
  round.py        — POST /api/round    — single round resolution
  simulate.py     — POST /api/simulate — Monte Carlo simulation
  exact.py        — POST /api/exact    — Taflin exact probabilities
index.html        — Static single-page UI; fetches /api/config on load to build all dynamic UI
style.css         — Dark theme; vanilla CSS, no framework
vercel.json       — Vercel config: explicit builds (includeFiles for engine/ + _shared.py)
                    and explicit routes mapping /api/<name> → api/<name>.py
```

## Conventions

- Vanilla JS only — no framework, no build step.
- UI is fully static HTML; `initFromConfig()` fetches `/api/config` on load and builds hero dropdown, structure checkboxes, sliders, and mode select dynamically via DOM APIs (not innerHTML with user data).
- Each `api/*.py` file is one Vercel serverless function using `BaseHTTPRequestHandler`. Shared logic lives in `_shared.py` at the project root.
- All user input reaching API endpoints is validated in `_shared.py` before passing to the engine.
- Dark theme is established in `style.css` — match it for new UI elements.
- API responses follow existing JSON shape — do not break the frontend contract without updating both sides.
- Engine code stays framework-free; web-layer concerns stay in `api/` and `_shared.py`.
- Adding a new endpoint requires: (1) new file in `api/`, (2) new route in `vercel.json` `routes` array, (3) new `builds` entry in `vercel.json` with `includeFiles`.

## Hard skills

- None defined yet. Add as recurring patterns emerge.
