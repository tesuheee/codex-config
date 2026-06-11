#!/usr/bin/env python3
"""Compare Claude Code skill folders with installed Codex skill folders."""

from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path


SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv"}


@dataclass(frozen=True)
class SkillInfo:
    name: str
    key: str
    path: Path
    description: str


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "unnamed-skill"


def read_text(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "cp932"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(errors="replace")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, flags=re.S)
    if not match:
        return {}

    data: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line or line.lstrip().startswith("#"):
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip("\"'")
    return data


def should_skip(path: Path, root: Path) -> bool:
    try:
        rel = path.relative_to(root)
    except ValueError:
        rel = path
    return any(part in SKIP_DIRS or part.startswith(".") for part in rel.parts)


def find_skill_files(root: Path) -> list[Path]:
    if root.is_file():
        return [root] if root.name.lower() == "skill.md" or root.suffix.lower() in {".md", ".txt"} else []

    own = root / "SKILL.md"
    if own.exists():
        return [own]

    files = []
    for path in root.rglob("SKILL.md"):
        if path.is_file() and not should_skip(path, root):
            files.append(path)
    return sorted(files)


def load_skills(root: Path) -> dict[str, SkillInfo]:
    root = root.expanduser().resolve()
    skills: dict[str, SkillInfo] = {}
    for skill_file in find_skill_files(root):
        text = read_text(skill_file)
        frontmatter = parse_frontmatter(text)
        folder_name = skill_file.parent.name if skill_file.name.lower() == "skill.md" else skill_file.stem
        name = frontmatter.get("name") or folder_name
        key = slugify(name)
        description = re.sub(r"\s+", " ", frontmatter.get("description", "")).strip()
        skills[key] = SkillInfo(name=name, key=key, path=skill_file.parent, description=description)
    return skills


def default_codex_dir() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        return Path(codex_home) / "skills"
    return Path.home() / ".codex" / "skills"


def default_claude_dir() -> Path:
    return Path.home() / ".claude" / "skills"


def status_for(claude: SkillInfo | None, codex: SkillInfo | None) -> str:
    if claude and not codex:
        return "claude-only"
    if codex and not claude:
        return "codex-only"
    if claude and codex and claude.description != codex.description:
        return "both-description-diff"
    return "both"


def markdown_table(rows: list[dict[str, str]]) -> str:
    headers = ["status", "skill", "claude_path", "codex_path", "note"]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        values = [row.get(header, "").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def compare(claude_dir: Path, codex_dir: Path) -> list[dict[str, str]]:
    claude = load_skills(claude_dir)
    codex = load_skills(codex_dir)
    rows = []
    for key in sorted(set(claude) | set(codex)):
        claude_skill = claude.get(key)
        codex_skill = codex.get(key)
        status = status_for(claude_skill, codex_skill)
        note = ""
        if status == "both-description-diff":
            note = "Descriptions differ; review before update."
        elif status == "claude-only":
            note = "Candidate to import."
        elif status == "codex-only":
            note = "Keep unless user asks to remove or ignore."
        name = (claude_skill or codex_skill).name
        rows.append(
            {
                "status": status,
                "skill": name,
                "claude_path": str(claude_skill.path) if claude_skill else "",
                "codex_path": str(codex_skill.path) if codex_skill else "",
                "note": note,
            }
        )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare Claude Code skills with Codex skills.")
    parser.add_argument("--claude", type=Path, default=default_claude_dir(), help="Claude Code skill folder or folder containing skills")
    parser.add_argument("--codex", type=Path, default=default_codex_dir(), help="Codex skills folder")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of a Markdown table")
    args = parser.parse_args()

    if not args.claude.exists():
        parser.error(f"Claude path not found: {args.claude}")
    if not args.codex.exists():
        parser.error(f"Codex skills path not found: {args.codex}")

    rows = compare(args.claude, args.codex)
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        print(markdown_table(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
