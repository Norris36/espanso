# skills (espanso package)

Bridges your opencode skills (`~/.config/opencode/skills`) into espanso.
Auto-generated `package.yml` — do not edit by hand.

## Triggers

| Trigger  | Effect |
|----------|--------|
| `:skills` | Lists every opencode skill with a one-line summary |
| `:skill`  | Form prompt: type a skill name → expands to its description + SKILL.md path |

Skill lookup accepts full ids (`engineering/tdd`), bare names (`tdd`),
and `:skill-<id>` forms.

## Regenerating

Skills change over time — regenerate `package.yml` after adding/removing any:

```bash
python3 skills_lib.py regen
```

or run `skills_updater.ipynb` in VS Code (preferred for testing).

## Files

- `skills_lib.py` — parsing, lookup, and YAML generation functions + CLI
- `package.yml` — generated espanso package (matches above)
- `skills_updater.ipynb` — notebook for testing and regeneration

## Environment

- `OPENCODE_SKILLS_DIR` — override the skills directory
  (default `~/.config/opencode/skills`)
