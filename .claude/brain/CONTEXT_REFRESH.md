# Context Refresh Policy

## Trigger

- On every merge to main.
- Before a balance-testing session after significant engine changes.

## Checks

1. Verify all `.claude` file references resolve.
2. Verify documented commands match actual project structure (`python -m pytest tests/ -v`, `python app.py`).
3. Verify zone soft-skill file maps match actual paths in `engine/`, `templates/`, `static/`, `tests/`.
4. Verify every soft/hard skill has a contract block.
5. Verify balance status numbers in `CLAUDE.md` still reflect current simulation results.

## Metadata

- Add `Last reviewed: YYYY-MM-DD` to each instruction-bearing file when updated.
