#!/usr/bin/env python3
"""Draft a Codex skill folder from a Claude Code skill file or directory."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path


SCRIPT_EXTS = {".py", ".sh", ".bash", ".zsh", ".ps1", ".js", ".mjs", ".cjs", ".ts"}
DOC_EXTS = {".md", ".markdown", ".txt", ".rst"}
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv"}


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return (value or "imported-skill")[:63].strip("-") or "imported-skill"


def read_text(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "cp932"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(errors="replace")


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, flags=re.S)
    if not match:
        return {}, text

    raw = match.group(1)
    body = text[match.end() :]
    data: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" not in line or line.lstrip().startswith("#"):
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip("\"'")
    return data, body


def json_metadata(path: Path) -> dict[str, str]:
    try:
        data = json.loads(read_text(path))
    except Exception:
        return {}
    if not isinstance(data, dict):
        return {}
    result = {}
    for key in ("name", "title", "description", "summary"):
        value = data.get(key)
        if isinstance(value, str):
            result[key] = value
    return result


def primary_files(source: Path) -> list[Path]:
    if source.is_file():
        return [source]

    seen: set[Path] = set()
    files: list[Path] = []
    preferred = [
        "SKILL.md",
        "skill.md",
        "README.md",
        "readme.md",
        "instructions.md",
        "prompt.md",
        "system.md",
    ]
    for name in preferred:
        candidate = source / name
        if candidate.exists() and candidate.is_file() and candidate.resolve() not in seen:
            files.append(candidate)
            seen.add(candidate.resolve())

    if files:
        return files

    docs = [
        path
        for path in source.rglob("*")
        if path.is_file()
        and path.suffix.lower() in DOC_EXTS
        and not any(part in SKIP_DIRS for part in path.parts)
    ]
    return sorted(docs)[:5]


def first_heading(text: str) -> str | None:
    match = re.search(r"^#\s+(.+?)\s*$", text, flags=re.M)
    return match.group(1).strip() if match else None


def first_paragraph(text: str) -> str | None:
    for block in re.split(r"\n\s*\n", text.strip()):
        block = block.strip()
        if not block or block.startswith("#") or block.startswith("```"):
            continue
        clean = re.sub(r"\s+", " ", block)
        return clean[:320]
    return None


def yaml_quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def build_skill_md(name: str, title: str, description: str, bodies: list[tuple[str, str]]) -> str:
    sections = []
    for label, body in bodies:
        _, clean = parse_frontmatter(body)
        clean = clean.strip()
        if not clean:
            continue
        sections.append(f"## Source: {label}\n\n{clean}")

    body_text = "\n\n".join(sections) if sections else "## Workflow\n\nFollow the source skill instructions provided by the user."
    return (
        "---\n"
        f"name: {name}\n"
        f"description: {description}\n"
        "---\n\n"
        f"# {title}\n\n"
        "## Codex Usage\n\n"
        "Use this skill when the user's request matches the trigger description above. "
        "Follow the migrated source instructions, adapting Claude-specific wording to the local Codex workspace.\n\n"
        f"{body_text}\n"
    )


def copy_resources(source: Path, target: Path, primary: set[Path]) -> None:
    if not source.is_dir():
        return

    for path in source.rglob("*"):
        if not path.is_file() or path in primary:
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue

        rel = path.relative_to(source)
        suffix = path.suffix.lower()
        if suffix in SCRIPT_EXTS:
            dest = target / "scripts" / rel
        elif suffix in DOC_EXTS:
            dest = target / "references" / rel
        else:
            dest = target / "assets" / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)


def write_openai_yaml(target: Path, title: str, name: str, description: str) -> None:
    short = description
    if len(short) < 25:
        short = f"{title} skill for Codex migration"
    if len(short) > 64:
        short = short[:61].rstrip() + "..."

    agents_dir = target / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    (agents_dir / "openai.yaml").write_text(
        "interface:\n"
        f"  display_name: {yaml_quote(title)}\n"
        f"  short_description: {yaml_quote(short)}\n"
        f"  default_prompt: {yaml_quote(f'Use ${name} to handle this migrated skill workflow.')}\n",
        encoding="utf-8",
    )


def default_codex_dir() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        return Path(codex_home) / "skills"
    return Path.home() / ".codex" / "skills"


def main() -> int:
    parser = argparse.ArgumentParser(description="Draft a Codex skill from a Claude Code skill export.")
    parser.add_argument("source", type=Path, help="Source skill file or directory")
    parser.add_argument("--out", type=Path, default=default_codex_dir(), help="Destination skills directory")
    parser.add_argument("--name", help="Codex skill name; defaults to source metadata or path")
    parser.add_argument("--overwrite", action="store_true", help="Replace an existing generated skill folder")
    args = parser.parse_args()

    source = args.source.expanduser().resolve()
    if not source.exists():
        print(f"Source not found: {source}", file=sys.stderr)
        return 2

    docs = primary_files(source)
    if not docs:
        print("No readable prompt or markdown source files found.", file=sys.stderr)
        return 2

    metadata: dict[str, str] = {}
    if source.is_dir():
        for meta_name in ("skill.json", "manifest.json", "config.json"):
            meta_path = source / meta_name
            if meta_path.exists():
                metadata.update(json_metadata(meta_path))

    bodies: list[tuple[str, str]] = []
    for doc in docs:
        text = read_text(doc)
        frontmatter, _ = parse_frontmatter(text)
        metadata = {**frontmatter, **metadata}
        label = doc.name if source.is_file() else str(doc.relative_to(source))
        bodies.append((label, text))

    combined = "\n\n".join(text for _, text in bodies)
    title = (
        metadata.get("title")
        or metadata.get("name")
        or first_heading(combined)
        or source.stem
        or "Imported Skill"
    )
    name = slugify(args.name or metadata.get("name") or title)
    description = (
        metadata.get("description")
        or metadata.get("summary")
        or first_paragraph(combined)
        or f"Migrated Codex skill for {title}."
    )
    description = re.sub(r"\s+", " ", description).strip()

    target = args.out.expanduser().resolve() / name
    if target.exists():
        if not args.overwrite:
            print(f"Target already exists: {target}. Use --overwrite to replace it.", file=sys.stderr)
            return 2
        shutil.rmtree(target)

    target.mkdir(parents=True)
    (target / "SKILL.md").write_text(build_skill_md(name, title, description, bodies), encoding="utf-8")
    copy_resources(source, target, set(docs))
    write_openai_yaml(target, title, name, description)

    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
