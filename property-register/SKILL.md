---
name: property-register
description: Register rental property candidates into the user's Obsidian house-hunting vault at C:\Users\nedie\Obsidian\■家関係. Use when the user asks to register, add, compare, classify, move, delete, or synchronize a property candidate; when they provide a listing URL, property name, room number, HOME'S archive URL, or housing note to add; or when they ask for the usual house-hunting property registration workflow.
---

# Property Register

## Overview

Use this skill to add or maintain property candidates in `C:\Users\nedie\Obsidian\■家関係`. Treat the vault's live files as the source of truth, create the actual candidate files by default, and finish by running the vault checker.

The user often enters requests by voice. Check for plausible transcription mistakes in property names, station names, room numbers, and category words before creating durable filenames or headings.

## Source Files

Read these files before changing the vault:

- `README.md` for the current folder layout and operating rules.
- `10_共通資料/10_方針・条件/物件追加ワークフロー.md` for the live registration sequence.
- `10_共通資料/10_方針・条件/現在の検索条件_恵比寿徒歩通勤.md` for current search constraints.
- `10_共通資料/10_方針・条件/評価基準_候補比較.md` for scoring and classification.
- `40_調査テンプレート/個別物件_条件照合テンプレート.md` for the individual note structure.
- `40_調査テンプレート/候補比較表_列定義.md` for comparison-table synchronization.
- `40_調査テンプレート/物件追加チェックリスト.md` for final coverage checks.

Do not rely on older paths or archived materials unless the user explicitly asks about history. Do not assume the vault is a Git repository.

## Registration Workflow

1. Extract the property name, room number, primary URL, desired category, and any HOME'S archive URL from the user's request.
2. Confirm spelling, duplicate registration, and address. If the request is URL-only, use the listing page and public sources to determine the property name, room number, and address.
3. Check public listing sources such as SUUMO, HOME'S, At Home, Yahoo! Real Estate, Canary, management-company pages, and broker pages when available. Prefer source-backed facts over guesses.
4. Collect every field required by `40_調査テンプレート/個別物件_条件照合テンプレート.md`. Use `-` for unavailable values.
5. Normalize yes/no style values to `○`, `×`, `△`, `-`, or `対象外`. Do not use `あり` or `なし` in comparison table fields.
6. Score the property with `10_共通資料/10_方針・条件/評価基準_候補比較.md`.
7. Classify the property:
   - `30_個別物件/10_本命物件` for priority candidates to check quickly when available.
   - `30_個別物件/20_比較物件` for candidates worth comparing.
   - `30_個別物件/30_参考物件` for lower-priority or policy-reference candidates.
8. Create the property folder under the chosen category. Add the condition note, `画像/` folder, representative images when available, and the vacancy-history HTML.
9. Create or update the condition note from the template. Keep the durable note clean: no discussion history, rejected names, temporary labels, or process narration.
10. Run `pwsh -File 50_運用ツール/物件整合性チェック.ps1 -Fix` from the vault root.
11. Re-read the relevant comparison table and condition note to check that the category, property name, score order, representative image section, and chart link are coherent.

## Individual Notes

Create notes as `<物件名><部屋番号>_条件照合.md` or the closest existing vault convention for that property. Put the note in:

- `30_個別物件/10_本命物件/<物件名>/`
- `30_個別物件/20_比較物件/<物件名>/`
- `30_個別物件/30_参考物件/<物件名>/`

Use stable property names for folders and filenames. Do not use raw conversational wording as official names. Preserve existing spelling if the property is already registered.

## Comparison Tables

Treat the individual property folders as the source of truth and synchronize with:

- `20_比較表/10_本命比較表.md`
- `20_比較表/20_候補比較表.md`
- `20_比較表/30_参考比較表.md`

Property columns in comparison tables use plain property names, not Obsidian links. Navigation links belong in the individual notes and other navigation files.

## Vacancy History

When a HOME'S archive or LIFULL source exists, generate a real populated chart:

```powershell
pwsh -File 50_運用ツール/HOMES空室履歴チャート生成.ps1 -PropertyName "物件名" -ArchiveUrl "HOME'SアーカイブURL" -OutputPath "30_個別物件/<区分>/<物件名>/<物件名>_空室履歴チャート.html"
```

Use `*_空室履歴未確認チャート.html` only when source data is genuinely unavailable. If active watch items lack chart HTML, run:

```powershell
pwsh -File 50_運用ツール/物件整合性チェック.ps1 -CreateMissingCharts
```

## Moving Or Deleting Properties

Move a property by moving its folder between `10_本命物件`, `20_比較物件`, and `30_参考物件`, then run:

```powershell
pwsh -File 50_運用ツール/物件整合性チェック.ps1 -Fix
```

When deleting or archiving a property folder, run the same checker so comparison tables stop showing removed items.

## Final Response

Report the created or updated property folder, condition note, comparison table, chart file, and checker result. Mention any important missing facts as concrete `要確認` items.
