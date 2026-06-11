---
name: room-dashboard
description: Update and operate the user's Obsidian house-hunting room dashboards. Use when the user asks to refresh, generate, inspect, or explain the room candidate dashboards, the 部屋別予算内候補一覧, the 不動産アーカイブ部屋候補一覧, saved property ratings, first-seen signals, or the Mac/Windows daily dashboard workflow for C:\Users\nedie\Obsidian\■家関係 or /Users/sugi/obsidian/■家関係.
---

# Room Dashboard

## Overview

Use this skill to operate the house-hunting dashboard tools through Codex instead of making the user run Python directly. Treat the vault scripts as the source of truth and keep web access conservative.

The user often enters requests by voice. Check for plausible transcription mistakes such as `価格` meaning `確認`, or vague references such as `ダッシュボード`, `部屋候補`, `アーカイブ`, `一覧`, and `評価`.

## Paths

Known vault roots:

- Windows: `C:\Users\nedie\Obsidian\■家関係`
- Mac: `/Users/sugi/obsidian/■家関係`

Work from the vault root. Do not assume the vault itself is a Git repository.

Key files:

- `50_運用ツール/部屋別候補一覧HTML生成.py`
- `50_運用ツール/不動産アーカイブ部屋候補HTML生成.py`
- `50_運用ツール/部屋候補設定.json`
- `50_運用ツール/物件評価.json`
- `20_比較表/生成結果/部屋別予算内候補一覧.html`
- `20_比較表/生成結果/部屋別予算内候補一覧_data.json`
- `20_比較表/生成結果/不動産アーカイブ部屋候補一覧.html`
- `20_比較表/生成結果/不動産アーカイブ部屋候補一覧_data.json`
- `20_比較表/生成結果/不動産アーカイブ部屋候補一覧_signal_snapshot.json`

## Update Workflow

For ordinary refresh requests, run the bundled helper:

```bash
python scripts/update_room_dashboard.py
```

The helper locates the vault, runs the部屋別 dashboard first, then runs the archive dashboard with `--skip-area-crawl`. This is the default because homes.co.jp can block repeated area crawling.

If the user explicitly asks for a full web refresh, run:

```bash
python scripts/update_room_dashboard.py --refresh
```

Only use full refresh when the user understands it may access lifullhomes-index.jp heavily. Do not run area crawling unless the user explicitly asks for a broad area reseed.

## Manual Commands

If the helper is unsuitable, run these commands from the vault root:

```bash
python3 50_運用ツール/部屋別候補一覧HTML生成.py
python3 50_運用ツール/不動産アーカイブ部屋候補HTML生成.py --skip-area-crawl
```

On Windows, use `python` if `python3` is unavailable.

## Validation

After updates, report the command outputs and the key counts:

- 部屋別: `rows`, `active`, `newToday`
- アーカイブ: `buildings`, `rows`, `representatives`, `detectedToday`

For same-day first-seen checks, run the archive update twice with `--skip-area-crawl` and confirm `detectedToday` is stable.

Do not modify `20_比較表/`, `30_個別物件/`, or other live vault files for dashboard refresh requests unless the user asks for registration or synchronization work.

## Ratings

Saved ratings live in `50_運用ツール/物件評価.json`.

When the user asks to save ratings from the dashboard:

1. Ask for the JSON copied by the dashboard's `評価をコピー` button if it is not already in the request.
2. Validate that it is JSON with a top-level `buildings` object.
3. Write it to `物件評価.json` with UTF-8 encoding and no extra commentary in the file.
4. Regenerate the archive dashboard so `vaultRating` is baked into the output.

Do not infer ratings from conversation unless the user states exact property names and ratings.

## Opening The Result

After generation, tell the user to open:

- Windows: `C:\Users\nedie\Obsidian\■家関係\20_比較表\生成結果\不動産アーカイブ部屋候補一覧.html`
- Mac: `/Users/sugi/obsidian/■家関係/20_比較表/生成結果/不動産アーカイブ部屋候補一覧.html`

If browser automation cannot open `file://`, report that limitation and provide the local path.

## Mac Automation

If the user asks to enable daily Mac refresh, use the plist in the vault:

```bash
mkdir -p ~/Library/LaunchAgents ~/Library/Logs
cp 50_運用ツール/com.sugi.archive-dashboard.plist ~/Library/LaunchAgents/com.sugi.archive-dashboard.plist
launchctl load ~/Library/LaunchAgents/com.sugi.archive-dashboard.plist
```

Log file: `~/Library/Logs/archive-dashboard.log`.

If `requests` is missing on Mac, install it for the user Python:

```bash
/usr/bin/python3 -m pip install --user requests
```

## Final Response

Keep the final response short. Include what was run, the output counts, whether generated files were updated, and any blockers such as missing `requests`, missing synced vault files, or unavailable `launchctl`.
