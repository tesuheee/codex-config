# codex-config

Codex のユーザー定義 skill を管理するリポジトリです。

このリポジトリでは user skill のみを同期対象にします。Codex が配布する標準 skill、設定、認証情報、セッション履歴、キャッシュ、プラグイン状態は管理対象外です。

## 管理対象

- `*/SKILL.md`: ユーザー定義 skill の本体
- `*/agents/openai.yaml`: skill の表示メタデータ
- `*/scripts/`: skill 用の補助スクリプト
- `*/references/`: skill 用の参照資料
- `*/assets/`: skill 用の再利用アセット

## 同期対象外

- `~/.codex/skills/.system/`
- `~/.codex/config.toml`
- `~/.codex/auth.json`
- `~/.codex/plugins/`
- `~/.codex/sessions/`
- `~/.codex/log/`
- `~/.codex/cache/`
- `~/.codex/*.sqlite`

詳細は `.gitignore` を参照してください。

## セットアップ

既存の Codex 環境を用意したうえで、`~/.codex/skills` を Git 管理下に置きます。`~/.codex/skills/.system/` は Codex が管理するため、このリポジトリでは管理しません。

初回同期は既存の `~/.codex/skills` ディレクトリ内で `git init` してから `pull` します。これにより、Codex が作成した `.system/` を残したまま user skill だけを取得できます。

macOS / Linux:

```bash
mkdir -p ~/.codex/skills
cd ~/.codex/skills
git init
git remote add origin https://github.com/tesuheee/codex-config.git
git pull origin master
git branch --set-upstream-to=origin/master master
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
Set-Location "$env:USERPROFILE\.codex\skills"
git init
git remote add origin https://github.com/tesuheee/codex-config.git
git pull origin master
git branch --set-upstream-to=origin/master master
```

## 日常運用

別端末の変更を取り込む場合:

```bash
cd ~/.codex/skills
git pull
```

変更を反映する場合:

```bash
cd ~/.codex/skills
git status
git add .
git commit -m "Update Codex skills"
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
