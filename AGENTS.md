# AGENTS.md

espanso configuration for this machine. espanso auto-loads every `match/**/*.yml`; there is no build step.

## Verify changes
- Config errors: `espanso log | tail -20`
- Triggers loaded: `espanso match list` (grep for `:name`)
- Daemon: `espanso status`, `espanso restart`

## Layout
- `match/*.yml` - top-level trigger files (`base.yml`, `skills.yml`, ...)
- `match/packages/<name>/package.yml` - installed packages; the file MUST be named `package.yml`
- `match/scripts/*.py` - helper scripts (Python 3, anaconda)

## Skills mirror (do not hand-edit)
`match/skills.yml` is GENERATED from `~/.config/opencode/skills` by `match/packages/skills/skills_lib.py`.
Regenerate with `python3 match/packages/skills/skills_lib.py sync`. Details in `match/packages/skills/README.md`.

## Automation
- `scripts/sync-daily.sh` runs daily (crontab, 09:30): regenerates the mirror, commits local changes, merges `origin/master`, pushes `HEAD:master`.
- `master` is auto-pushed; `dev` is the working branch.

## Guardrails
A pre-commit hook (`.githooks/`, wired via `git config core.hooksPath .githooks`) rejects non-UTF-8 files, invalid YAML under `match/`, and a stale mirror. On a fresh clone re-run that `git config`; `scripts/sync-daily.sh` re-applies it.

## Conventions
- Python functions: one-line summary, `~~~`, bulleted operations, `~~~`, `returns type: ...`.
