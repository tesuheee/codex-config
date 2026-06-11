---
name: welbox-claim
description: WELBOX申請の準備を行う。会社ルールPDFから申請メモを作成し、そのメモを前提にAmazon領収書を取得する。
---

# WELBOX Claim Prep

引数: `$ARGUMENTS`

## 目的

1. 会社ルールPDFから申請メモを作る（更新時に実行）
2. 申請対象（書籍・在宅勤務関連）に該当するAmazon領収書を年度単位で保存する
3. 取得後に整合チェック（件数/金額/重複/返金混在/一覧ノート整合）を実行する

## 標準実行

```powershell
python "C:\Users\nedie\.codex\skills\welbox-claim\scripts\run_welbox_prep.py" `
  --base-dir "C:\Users\nedie\Obsidian\■リファレンス\Welbox申請" `
  --fiscal-year 2025 `
  --auth-mode manual-cdp `
  --launch-chrome
```

## ルールメモ更新

```powershell
python "C:\Users\nedie\.codex\skills\welbox-claim\scripts\run_welbox_prep.py" `
  --base-dir "C:\Users\nedie\Obsidian\■リファレンス\Welbox申請" `
  --fiscal-year 2025 `
  --refresh-rule-memo `
  --skip-amazon
```

- 既定の保存先: `■リファレンス\Welbox申請\ドキュメント\rule_memo.md`

## 年度と出力

- 対象期間（既定）: `fiscal-year/04/01` 〜 `fiscal-year+1/03/31`
- 出力フォルダ（既定）: `■リファレンス\Welbox申請\<年度>年度_申請領収書`
- manifest（既定）: `amazon_manifest_<年度>fy.json`
- 一覧ノート（既定）: `申請領収書一覧_amazon_manifest_<年度>fy.md`
  - 通常表と `返品済み` 表に分けて出力
- 取得後チェック（既定）:
  - `取得後チェック_amazon_manifest_<年度>fy.md`
  - `取得後チェック_amazon_manifest_<年度>fy.json`

## Amazon取得の仕様

- 対象条件:
  - 期間内注文
  - 対象キーワードに一致（Kindle/書籍/在宅機器）
  - 除外キーワードに非一致（Kindle Unlimited/読み放題/返品・食品・PC本体など）
- 保存条件:
  - 領収書ページ本文に `領収書` と `注文番号` があること
  - 条件を満たした場合のみPDF保存
  - 返品/返金ステータスがある注文は `返品済み` フォルダへ保存

## 主なオプション

- 期間を明示: `--date-from 2025-04-01 --date-to 2026-03-31`
- 年フィルタを明示: `--years 2025,2026`
- キーワード調整: `--keywords ... --exclude-keywords ...`
- 候補確認のみ: `--dry-run-amazon`
- Chrome接続先変更: `--cdp-url http://127.0.0.1:9222`
- 取得後チェック無効化: `--skip-post-check`
- 取得後チェックの閾値: `--post-check-strict-level none|error|warn`

## 参照ファイル

- `scripts/extract_welbox_rules.py`
- `scripts/download_amazon_receipts.py`
- `scripts/organize_returned_receipts.py`
- `scripts/run_welbox_prep.py`
- `scripts/audit_receipt_manifest.py`
- `references/claim_scope.md`

