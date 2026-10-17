"""Pre-commit guardrails for the espanso config repo.
~~~
- reject staged text files that are not valid UTF-8 (catches UTF-16 files and BOMs)
- parse every staged match/**/*.yml as YAML (catches unescaped quotes and bad indentation)
- when the skills mirror source is staged, regenerate match/skills.yml and fail on drift
~~~
returns type: int -- process exit code (0 to allow the commit, 1 to block it)
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import List, Tuple


def repo_root() -> Path:
    """Resolve the repository root from git.
    ~~~
    - ask git for the top-level working directory
    - return it as a Path
    ~~~
    returns type: Path -- absolute path to the repository root
    """
    out = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True)
    return Path(out.strip())


def staged_files(root: Path) -> List[str]:
    """List staged file paths (added, copied, or modified) relative to the repo root.
    ~~~
    - run git diff --cached with a name-only diff filter
    - split the newline-separated output and drop blanks
    ~~~
    returns type: list -- staged paths as POSIX-style strings
    """
    out = subprocess.check_output(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
        text=True,
        cwd=str(root),
    )
    return [line for line in out.splitlines() if line]


def check_utf8(root: Path, files: List[str]) -> List[Tuple[str, str]]:
    """Flag staged files whose bytes are not UTF-8 (NUL bytes or a UTF-16 BOM).
    ~~~
    - read each staged file's raw bytes, skipping missing entries and directories
    - report files containing NUL bytes as binary/UTF-16
    - report files that fail a strict UTF-8 decode
    ~~~
    returns type: list -- [(path, reason)] for every offending file
    """
    problems: List[Tuple[str, str]] = []
    for rel in files:
        path = root / rel
        if not path.exists() or path.is_dir():
            continue
        data = path.read_bytes()
        if b"\x00" in data:
            problems.append((rel, "contains NUL bytes (binary or UTF-16?)"))
            continue
        try:
            data.decode("utf-8")
        except UnicodeDecodeError as exc:
            problems.append((rel, "not valid UTF-8 (%s)" % exc))
    return problems


def check_yaml(root: Path, files: List[str]) -> List[Tuple[str, str]]:
    """Parse every staged match yml file to confirm it is valid YAML.
    ~~~
    - import PyYAML lazily and skip the check with a warning if it is unavailable
    - restrict to staged files under match/ ending in .yml
    - report files that raise during yaml.safe_load
    ~~~
    returns type: list -- [(path, error)] for every file that fails to parse
    """
    try:
        import yaml
    except ImportError:
        print("pre-commit: PyYAML not available; skipping YAML validation", file=sys.stderr)
        return []
    problems: List[Tuple[str, str]] = []
    for rel in files:
        if not rel.endswith(".yml") or not (rel == "match" or rel.startswith("match/")):
            continue
        path = root / rel
        if not path.exists():
            continue
        try:
            yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001 - surface any parse failure
            problems.append((rel, str(exc)))
    return problems


def check_mirror_drift(root: Path, files: List[str]) -> List[Tuple[str, str]]:
    """Regenerate the skills mirror and report whether the staged copy was stale.
    ~~~
    - skip unless match/skills.yml or skills_lib.py is among the staged files
    - run skills_lib.py sync to rewrite match/skills.yml from the skill sources
    - report a diff between the regenerated file and the staged version
    ~~~
    returns type: list -- [(path, reason)] when the mirror drifts, else empty
    """
    watched = {"match/skills.yml", "match/packages/skills/skills_lib.py"}
    if not any(rel in watched for rel in files):
        return []
    lib = root / "match" / "packages" / "skills" / "skills_lib.py"
    if not lib.exists():
        return []
    subprocess.run([sys.executable, str(lib), "sync"], cwd=str(root), capture_output=True)
    diff = subprocess.run(
        ["git", "diff", "--name-only", "--", "match/skills.yml"],
        text=True,
        capture_output=True,
        cwd=str(root),
    )
    if diff.stdout.strip():
        return [("match/skills.yml", "stale - regenerated output differs; run skills_lib.py sync")]
    return []


def main() -> int:
    """Run all pre-commit checks and decide whether the commit may proceed.
    ~~~
    - gather the staged file list
    - run the UTF-8, YAML, and mirror-drift checks in order
    - print a grouped report and return 1 if any check failed
    ~~~
    returns type: int -- 0 when clean, 1 when any check reports a problem
    """
    root = repo_root()
    files = staged_files(root)
    utf8 = check_utf8(root, files)
    yaml_problems = check_yaml(root, files)
    drift = check_mirror_drift(root, files)

    if not (utf8 or yaml_problems or drift):
        return 0

    print("pre-commit FAILED:", file=sys.stderr)
    for label, problems in (
        ("non-UTF-8", utf8),
        ("invalid YAML", yaml_problems),
        ("mirror drift", drift),
    ):
        for rel, reason in problems:
            print("  [%s] %s: %s" % (label, rel, reason), file=sys.stderr)
    print("\nFix the above (or commit with --no-verify) and retry.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
