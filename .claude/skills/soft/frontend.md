# Zone: Flask App & UI (`app.py`, `templates/`, `static/`)

```contract
requires:
  - .claude/CLAUDE.md
  - .claude/brain/QUALITY.md

inputs:
  task: request touching API endpoints, HTML templates, or CSS styling

produces:
  file_map: relevant frontend files
  conventions: frontend-local rules
  hard_skills: applicable hard skills

pre-gate:
  - zone identified as app/templates/static
  - task scope clear

post-gate:
  - relevant files can be named
  - API contract understood
  - no unsafe rendering introduced
```

You are working in the Flask web layer — simulation controls, battle log display, and API endpoints.

## File map

```text
app.py              — Flask app; API endpoints consumed by the frontend
templates/
  index.html        — Single-page UI: battle controls, log panel, simulation panel
static/
  style.css         — Dark theme; vanilla CSS, no framework
```

## Conventions

- Vanilla JS only — no framework, no build step.
- Jinja2 for server-side rendering; JS fetches JSON from Flask endpoints for dynamic updates.
- All user input reaching Flask endpoints must be validated before use.
- Dark theme is established in `style.css` — match it for new UI elements.
- API responses follow existing JSON shape — do not break the frontend contract without updating both sides.
- `app.py` is the only file allowed to import Flask; engine code stays framework-free.

## Hard skills

- None defined yet. Add as recurring patterns emerge.
