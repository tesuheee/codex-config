---
name: read-later
description: Vault直下のWeb Clip・■クリッピング/フォルダー・既存リンク集ファイルを📎Webクリップにカテゴリ別にまとめて元ファイルを削除する。`/read-later` で起動。
---

# Web Clip 整理ワークフロー

## 概要

Obsidian Vault内のWeb Clipを収集し、リンクを `■メモ/📎Webクリップ.md` にカテゴリ別にまとめた後、元ファイルを削除する。

## 対象ソース（優先順に処理）

### ソース1: Vault直下の単発Web Clipファイル
- パス: `C:\Users\nedie\Obsidian\*.md`（直下のみ）
- `■` で始まるフォルダ内のファイルは対象外
- 1ファイル = 1リンクの形式が多い（iOSのShare Sheet経由など）

### ソース2: ■クリッピング/ フォルダー
- パス: `C:\Users\nedie\Obsidian\■クリッピング\*.md`
- Obsidian Web Clipper（ブラウザ拡張機能）が保存したフルコンテンツファイル
- frontmatter から `title`（タイトル）と `source`（URL）を抽出する
- `author` フィールドがあれば投稿者名として使用する
- 本文内容はカテゴリ判定の参考に使うが、📎Webクリップ.md には登録しない

### ソース3: 既存のリンク集ファイル
- `■メモ/Safariリーディングリスト.md` など、複数リンクがまとまったファイル
- ユーザーから指定があった場合に処理する
- 箇条書き形式 `- [タイトル](URL)` やプレーンURL行を抽出

## 手順

### 1. 対象ファイルの収集とリンク抽出

- 各ファイルを読み取り、URL を抽出する
- Markdownリンク `[タイトル](URL)` やプレーンURLを取得
- 重複URLを除去（同一URLは1つだけ残す）

### 2. ツイート内容の取得（X/Twitter リンクの場合）

Chrome MCP を使う（WebFetchはXでブロックされる）。

**セットアップ:**
1. `tabs_context_mcp`（`createIfEmpty: true`）でタブ取得
2. 1つのタブを使い回してナビゲート→抽出を繰り返す

**高速抽出パターン（推奨）:**
```
navigate → URL に遷移
javascript_tool → 以下のJSで本文を一括取得（2秒待機で十分）
```

```javascript
new Promise(r=>{setTimeout(()=>{
  const a=document.querySelector('article');
  r(a?a.innerText.substring(0,300):'no article')
},2000)})
```

**フォールバック（JSでテキスト取れない場合）:**
- `read_page` で main → region → article の順に掘る
- `[data-testid="tweetText"]` が空の場合は `article.innerText` を使う

**スキップ対象:**
- 「凍結されたアカウント」→ 除外し、完了報告で件数を報告
- 「このポストは表示できません」→ 除外
- 引用元と同じURLが別エントリにある場合 → 重複除去

### 3. 非Xリンクの処理

- zenn.dev / note.com / 一般サイト → ファイル内のタイトルテキストをそのまま使用
- タイトルがない場合は WebFetch で取得を試みる

### 4. カテゴリ分け

ツイート内容・タイトル・ユーザー名から推定して分類する。

**既存カテゴリ（優先的に使用）:**
- AI — LLM、エージェント、AI全般
- Claude Code — Claude Code、Antigravity、Skills、MCP、ハーネス
- OpenClaw — OpenClaw固有の話題
- 投資/金融 — 株、金、暗号資産、Polymarket
- 映画/エンタメ — 映画、読み物、ネタ
- ビジネス/副業 — 稼ぐ系、SEO、マーケティング、セールス
- 自己啓発/学習 — 勉強法、思考術、ライフハック
- 開発ツール — 汎用ツール（tmux、Syncthing等）
- デザイン/映像 — デザイン、映像制作、資料作成
- 生活 — 行政、日常

**カテゴリ判断の指針:**
- Claude Code / Antigravity / Skills / MCP の話 → 「Claude Code」（「AI」ではない）
- AI + 副業の組み合わせ → 副業が主旨なら「ビジネス/副業」
- 既存カテゴリに合わない場合は新規カテゴリを作成
- 判断がつかない場合 →「その他」

### 5. 📎Webクリップ.md への書き込み

- パス: `■メモ/📎Webクリップ.md`
- フォーマット:

```markdown
# カテゴリ名

[タイトル - 投稿者名](URL)
```

- **1行につき1リンクのみ**
- URLのトラッキングパラメータ除去: `?s=12`, `?utm_*` 等を削除
- 既にファイルが存在する場合は、既存カテゴリ構造を維持して追記
- 同じURLが既に存在する場合はスキップ（重複防止）

### 6. 元ファイルの削除

- まとめ終わったファイルを削除する
- `📎Webクリップ.md` 自体は削除しない

### 7. 完了報告

以下を簡潔に報告:
- 追加したリンク数
- カテゴリ別内訳（テーブル形式）
- 除外した件数と理由（凍結、重複、表示不可等）
