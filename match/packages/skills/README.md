# skills (espanso mirror)

Mirror of your opencode skills (`~/.config/opencode/skills`) as **static espanso
triggers**. Each skill's name becomes a trigger whose replacement is the **full
skill body** (everything after the `SKILL.md` frontmatter) — so typing `:tdd`
expands the entire skill instantly (no shell round-trip).

`match/skills.yml` is auto-generated from the `SKILL.md` frontmatter and is
refreshed daily by `scripts/sync-daily.sh`.

## Triggers

| Trigger | Expands to |
|---------|-----------|
| `:skills` | List of every skill and a one-line summary |
| `:<skill-name>` | That skill's **full body**, e.g. `:tdd`, `:brainstorming` |

Nested skills use their bare name (`engineering/tdd` -> `:tdd`).

## Files

- `skills_lib.py` — parsing + md -> yml conversion functions and CLI
- `skills_updater.ipynb` — testing and manual regeneration (preferred)
- `match/skills.yml` — the generated mirror (do not edit by hand)

> Note: this lives under `match/packages/` only as the tooling home. The output
> is a plain match file (`match/skills.yml`) rather than an espanso package,
> because espanso packages must be named `package.yml` and can't be `skills.yml`.

## Regenerating

```bash
python3 skills_lib.py sync   # rewrite match/skills.yml
python3 skills_lib.py show   # print it to stdout
```

Run `skills_updater.ipynb` in VS Code to test and regenerate interactively.

## Environment

- `OPENCODE_SKILLS_DIR` — override the skills directory
  (default `~/.config/opencode/skills`)
