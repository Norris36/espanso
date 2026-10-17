"""opencode skills <-> espanso package bridge: parse SKILL.md files, look skills up, regenerate package.yml.
~~~
- parse frontmatter (name, description) from a SKILL.md file
- collect every skill under the opencode skills directory (including nested folders)
- format an all-skills listing or a single-skill lookup for espanso expansion
- regenerate match/packages/skills/package.yml from the live skills directory
- expose a tiny CLI (list / get / regen) used by espanso shell vars
~~~
returns type: dict | list | str | None -- per-function; see each docstring
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

DEFAULT_SKILLS_DIR = Path.home() / ".config" / "opencode" / "skills"
PACKAGE_DIR = Path(__file__).resolve().parent
DEFAULT_OUTPUT = PACKAGE_DIR / "package.yml"
PACKAGE_VERSION = "1.0.0"


def parse_frontmatter(skill_md: Path) -> Optional[Dict[str, str]]:
    """Read a SKILL.md file and extract its YAML frontmatter keys.
    ~~~
    - open the file and locate the leading --- fenced frontmatter block
    - split each line into key/value and strip surrounding quotes from values
    - stop at the closing --- fence
    ~~~
    returns type: dict | None -- {"name": ..., "description": ...} or None if no frontmatter
    """
    try:
        text = skill_md.read_text(encoding="utf-8")
    except OSError:
        return None
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    data: Dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        if key in ("name", "description"):
            data[key] = value
    return data or None


def collect_skills(skills_dir: Path = DEFAULT_SKILLS_DIR) -> List[Dict[str, str]]:
    """Walk the opencode skills directory and gather every SKILL.md's metadata.
    ~~~
    - glob recursively for SKILL.md under skills_dir
    - parse each file's frontmatter for name and description
    - derive a lookup id from the relative folder path (e.g. engineering/tdd)
    - skip files whose frontmatter cannot be parsed
    ~~~
    returns type: list -- [{"id": "brainstorming", "name": "brainstorming", "description": "...", "path": "..."}]
    """
    skills: List[Dict[str, str]] = []
    for md in sorted(skills_dir.rglob("SKILL.md")):
        meta = parse_frontmatter(md)
        if not meta or "name" not in meta:
            continue
        rel = md.parent.relative_to(skills_dir)
        skill_id = str(rel).replace(os.sep, "/")
        skills.append(
            {
                "id": skill_id,
                "name": meta["name"],
                "description": meta.get("description", ""),
                "path": str(md),
            }
        )
    return skills


def format_skill_list(skills: List[Dict[str, str]]) -> str:
    """Render the full skill catalogue as a compact text block for espanso.
    ~~~
    - sort skills by id
    - emit one line per skill: id — first sentence of the description
    - prepend a header with the skill count
    ~~~
    returns type: str -- multi-line plain-text listing
    """
    if not skills:
        return "No opencode skills found."
    header = f"opencode skills ({len(skills)}):"
    rows = []
    for s in sorted(skills, key=lambda x: x["id"]):
        desc = s["description"].split(". ")[0].rstrip(".")
        rows.append(f"  :skill-{s['id']}  {desc}")
    return "\n".join([header] + rows)


def lookup_skill(query: str, skills: List[Dict[str, str]]) -> str:
    """Find one skill by id or name and render its details for espanso.
    ~~~
    - normalise the query (strip, lower-case, drop a leading ':skill-' prefix)
    - exact-match against id, then bare name, then suffix of id
    - if nothing matches, return close candidates by substring
    - render the matched skill's description and SKILL.md path
    ~~~
    returns type: str -- skill detail block, or a 'not found' hint with candidates
    """
    q = (query or "").strip().lower().lstrip(":").removeprefix("skill-")
    if not q:
        return "Usage: type :skill then the skill name (see :skills for the list)."
    by_id = {s["id"].lower(): s for s in skills}
    by_name: Dict[str, Dict[str, str]] = {}
    for s in skills:
        by_name.setdefault(s["name"].lower(), s)
    match = (
        by_id.get(q)
        or by_name.get(q)
        or next((s for sid, s in by_id.items() if sid.endswith("/" + q)), None)
    )
    if match is None:
        candidates = [s["id"] for s in skills if q in s["id"].lower()][:5]
        if candidates:
            return f"No skill '{query}'. Did you mean: {', '.join(candidates)}?"
        return f"No skill '{query}' found. Type :skills for the full list."
    return f"{match['id']}\n{match['description']}\n\n{match['path']}"


def generate_package_yml(
    skills: List[Dict[str, str]],
    output_path: Path = DEFAULT_OUTPUT,
    version: str = PACKAGE_VERSION,
) -> Path:
    """Regenerate the espanso skills package.yml from the collected skill metadata.
    ~~~
    - build YAML text with name/parent/version header and a do-not-edit banner
    - emit the :skills match (shell var running 'list') with an absolute script path
    - emit the :skill match (form input + shell var running 'get')
    - embed the current skill ids as a comment block for quick reference
    - write the file to output_path
    ~~~
    returns type: Path -- the path that was written
    """
    script = str(PACKAGE_DIR / "skills_lib.py")
    ids = ", ".join(sorted(s["id"] for s in skills))
    yml = (
        "# AUTO-GENERATED by skills_lib.py -- do not edit by hand.\n"
        "# Regenerate with: python3 skills_lib.py regen  (or skills_updater.ipynb)\n"
        f"# Skills at generation time ({len(skills)}): {ids}\n"
        "name: skills\n"
        "parent: default\n"
        f"version: {version}\n"
        "matches:\n"
        "  - trigger: \":skills\"\n"
        "    replace: \"{{skills_out}}\"\n"
        "    vars:\n"
        "      - name: skills_out\n"
        "        type: shell\n"
        "        params:\n"
        f"          cmd: \"python3 '{script}' list\"\n"
        "  - trigger: \":skill\"\n"
        "    replace: \"{{skill_out}}\"\n"
        "    vars:\n"
        "      - name: input\n"
        "        type: form\n"
        "        params:\n"
        "          layout: |\n"
        "            [[name]]\n"
        "      - name: skill_out\n"
        "        type: shell\n"
        "        params:\n"
        f"          cmd: \"python3 '{script}' get '{{{{input.name}}}}'\"\n"
    )
    output_path.write_text(yml, encoding="utf-8")
    return output_path


def main(argv: List[str]) -> int:
    """CLI entry point used by espanso shell vars and manual regeneration.
    ~~~
    - dispatch on argv[1]: 'list' prints the catalogue, 'get <name>' prints one skill,
      'regen' rewrites package.yml
    - load skills from DEFAULT_SKILLS_DIR (override with OPENCODE_SKILLS_DIR)
    ~~~
    returns type: int -- process exit code (0 on success)
    """
    skills_dir = Path(os.environ.get("OPENCODE_SKILLS_DIR", str(DEFAULT_SKILLS_DIR)))
    command = argv[1] if len(argv) > 1 else "list"
    skills = collect_skills(skills_dir)
    if command == "list":
        print(format_skill_list(skills))
    elif command == "get":
        query = argv[2] if len(argv) > 2 else ""
        print(lookup_skill(query, skills))
    elif command == "regen":
        path = generate_package_yml(skills)
        print(f"Wrote {path} ({len(skills)} skills, version {PACKAGE_VERSION})")
    else:
        print(f"Unknown command '{command}'. Use: list | get <name> | regen")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
