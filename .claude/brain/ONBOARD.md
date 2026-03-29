# Onboarding Workflow

Use this when work is non-trivial or crosses zones.

## Step 1: ENTRY

- Read `.claude/CLAUDE.md`.
- Identify zone(s) touched by the task.

## Step 2: ZONE_LOADED

- Read all relevant soft skills from `.claude/skills/soft/`.
- Satisfy each contract gate.

## Step 3: SKILL_IDENTIFIED

- Load hard skill(s) for recurring procedures from `.claude/skills/hard/`.
- Confirm execution and verification steps.

## Step 4: READY

- Read every file to be changed.
- Confirm local patterns and naming.

Proceed to execution only after READY gate is met.

## Zone breadcrumbs

Each major zone includes a `README.md` (or inline comment) with:

```md
<!-- agent-context: .claude/skills/soft/<zone>.md -->
```

This keeps file-system navigation and skill routing connected.
