from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


KNOWN_VAULTS = [
    Path(r"C:\Users\nedie\Obsidian\■家関係"),
    Path("/Users/sugi/obsidian/■家関係"),
]


def find_vault(explicit: str | None) -> Path:
    candidates = [Path(explicit).expanduser()] if explicit else []
    candidates.extend(KNOWN_VAULTS)
    for candidate in candidates:
        if (candidate / "50_運用ツール" / "部屋別候補一覧HTML生成.py").exists():
            return candidate
    checked = ", ".join(str(path) for path in candidates)
    raise SystemExit(f"vault not found; checked: {checked}")


def run_step(vault: Path, args: list[str]) -> dict:
    command = [sys.executable, *args]
    env = os.environ.copy()
    env.setdefault("PYTHONUTF8", "1")
    completed = subprocess.run(
        command,
        cwd=str(vault),
        env=env,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.stderr:
        sys.stderr.write(completed.stderr)
    if completed.returncode != 0:
        if completed.stdout:
            sys.stdout.write(completed.stdout)
        raise SystemExit(completed.returncode)
    text = completed.stdout.strip()
    if text:
        sys.stdout.write(text + "\n")
    try:
        return json.loads(text.splitlines()[-1])
    except (IndexError, json.JSONDecodeError):
        return {"raw": text}


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Update the house-hunting room dashboards.")
    parser.add_argument("--vault", help="Override the house-hunting vault path.")
    parser.add_argument("--refresh", action="store_true", help="Refresh archive building pages.")
    parser.add_argument("--area-crawl", action="store_true", help="Allow homes.co.jp area crawling.")
    ns = parser.parse_args()

    vault = find_vault(ns.vault)
    room = run_step(vault, ["50_運用ツール/部屋別候補一覧HTML生成.py"])
    archive_args = ["50_運用ツール/不動産アーカイブ部屋候補HTML生成.py"]
    if not ns.area_crawl:
        archive_args.append("--skip-area-crawl")
    if ns.refresh:
        archive_args.append("--refresh")
    archive = run_step(vault, archive_args)

    summary = {
        "vault": str(vault),
        "room": room,
        "archive": archive,
    }
    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
