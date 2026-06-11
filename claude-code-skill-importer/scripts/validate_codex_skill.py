#!/usr/bin/env python3
"""Locate skill-creator's quick_validate.py and validate a Codex skill."""

from __future__ import annotations

import os
import runpy
import sys
from pathlib import Path


def candidate_paths() -> list[Path]:
    paths: list[Path] = []
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    paths.append(codex_home / "skills" / ".system" / "skill-creator" / "scripts" / "quick_validate.py")
    paths.append(codex_home / "skills" / "skill-creator" / "scripts" / "quick_validate.py")
    paths.append(Path.home() / ".codex" / "skills" / ".system" / "skill-creator" / "scripts" / "quick_validate.py")
    return paths


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_codex_skill.py <path-to-skill>", file=sys.stderr)
        return 2

    for path in candidate_paths():
        if path.exists():
            sys.argv = [str(path), sys.argv[1]]
            runpy.run_path(str(path), run_name="__main__")
            return 0

    print("quick_validate.py was not found under CODEX_HOME or ~/.codex.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
