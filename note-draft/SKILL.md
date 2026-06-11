---
name: note-draft
description: note.com投稿用の下書きを作成し、コピペ用HTMLをブラウザで開く。
---
# note.com 下書き作成ツール

トピック: $ARGUMENTS

## 共通情報

- 保存先: `C:\Users\nedie\Obsidian\■記事\note-draft\`
- アーカイブ先: `C:\Users\nedie\Obsidian\■記事\note-draft\published\`
- ファイル名: `YYYY-MM-DD_タイトル.md`（今日の日付を使用）
- HTML出力: 同フォルダに同名で `.html` として保存

## frontmatter形式

```yaml
---
title: タイトル
date: YYYY-MM-DD
published: false
---
```

`published: true` に変更するとアーカイブ対象になる。

## 文体ルール

note.com向けの文体で書くこと：

- **です・ます調**が基本
- 個人的な体験・気づきを軸にした読みやすいエッセイスタイル
- 段落は短め、テンポよく
- 専門用語は使う場合に軽く説明を添える
- 「まとめ」は不要。余韻のある締め方でOK
- 絵文字は使わない
- 画像は必ずインライン形式 `![alt](url)` で書く。参照形式 `![alt][ref]` ＋ `[ref]: url` は使わない（後から画像を消すとき2箇所消す手間がかかるため）

## 手順

### Phase 0: アーカイブ処理（起動時に毎回実行）

`note-draft\` フォルダ内のMDファイルを走査し、frontmatterに `published: true` が含まれるファイルを `published\` フォルダへ移動する。対応するHTMLファイルも同様に移動する。移動したファイルがあればユーザーに通知する。

### Phase 1: 記事作成

1. トピックについて必要であればWebSearchで調べる
2. 文体ルールに従って本文を下書きする
3. frontmatterを先頭に付けてMarkdownファイルとして保存先に保存する（`published: false` で開始）

### Phase 2: HTML変換・ブラウザ表示

4. 保存先フォルダにある `convert.py` で Markdown→HTML に変換する。引数に保存したMDファイルのパスを渡す。

   **重要**: Pythonは必ず `py -3`（Windowsランチャー）で実行すること。`python` だと `.browser-use-env` の仮想環境が掴まれ、`markdown` も `pip` も無くて失敗する。`py -3`（Python 3.14系）には `markdown` が入っている。

   ```
   py -3 "C:\Users\nedie\Obsidian\■記事\note-draft\convert.py" "保存したMDファイルのパス"
   ```

   `convert.py` がスタイル・frontmatter除去・HTML書き出しまで全部やる。引数なしで実行すると `note-draft\` 配下（`published\` 除く）の全MDを変換する。

5. 変換後、以下のコマンドでブラウザを開く：
   ```
   start "" "HTMLファイルのパス"
   ```

### Phase 3: ユーザー操作（手動）

6. ユーザーにブラウザで以下の操作を案内する：
   - `Ctrl+A` で全選択
   - `Ctrl+C` でコピー
   - note.com の新規投稿エディタを開いて `Ctrl+V` でペースト
   - タイトルを設定して公開 or 下書き保存

7. HTMLのパスとnote.comの新規投稿URLをユーザーに伝えて完了
