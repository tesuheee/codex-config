# codex-config

Codex のユーザー定義 skill を管理するリポジトリです。

このリポジトリを正本として扱い、各端末の `~/.codex/skills` はここから取得したコピーとして運用します。Codex 本体の設定、セッション履歴、キャッシュ、システム標準 skill は管理対象外です。

## 管理対象

- `*/SKILL.md`: ユーザー定義 skill の本体
- `*/agents/openai.yaml`: skill の表示メタデータ
- `*/scripts/`: skill 用の補助スクリプト
- `*/references/`: skill 用の参照資料
- `*/assets/`: skill 用の再利用アセット

## 同期対象外

端末固有の設定、機密情報、実行履歴、キャッシュ、Codex が配布する標準 skill は Git 管理しません。

- `~/.codex/config.toml`
- `~/.codex/auth.json`
- `~/.codex/sessions/`
- `~/.codex/log/`
- `~/.codex/plugins/`
- `~/.codex/skills/.system/`

詳細は `.gitignore` を参照してください。

## セットアップ

新しい端末では、既存の `~/.codex/skills` がある場合は退避してから clone します。

macOS / Linux:

```bash
mv ~/.codex/skills ~/.codex/skills.backup-$(date +%Y%m%d-%H%M%S)
git clone https://github.com/tesuheee/codex-config.git ~/.codex/skills
```

Windows PowerShell:

```powershell
Rename-Item "$env:USERPROFILE\.codex\skills" "skills.backup-$(Get-Date -Format yyyyMMdd-HHmmss)"
git clone https://github.com/tesuheee/codex-config.git "$env:USERPROFILE\.codex\skills"
```

## 日常運用

別端末の変更を取り込む場合:

```bash
cd ~/.codex/skills
git pull
```

Windows PowerShell:

```powershell
Set-Location "$env:USERPROFILE\.codex\skills"
git pull
```

この端末で変更を反映する場合:

```bash
cd ~/.codex/skills
git status
git add <変更したファイル>
git commit -m "変更内容"
git push
```

Windows PowerShell:

```powershell
Set-Location "$env:USERPROFILE\.codex\skills"
git status
git add <変更したファイル>
git commit -m "変更内容"
git push
```

## Claude Code skill との比較

Claude Code 側の `~/.claude/skills` と Codex 側の `~/.codex/skills` を比較する場合:

```bash
python ~/.codex/skills/claude-code-skill-importer/scripts/compare_skill_sets.py
```

Claude Code skill を Codex skill に変換する場合:

```bash
python ~/.codex/skills/claude-code-skill-importer/scripts/convert_claude_skill.py ~/.claude/skills/<skill-name> --out ~/.codex/skills
```

変換後は内容を確認し、必要に応じて検証します。

```bash
python ~/.codex/skills/claude-code-skill-importer/scripts/validate_codex_skill.py ~/.codex/skills/<skill-name>
```
