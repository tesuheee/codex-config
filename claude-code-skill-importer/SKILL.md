---
name: claude-code-skill-importer
description: Compare, convert, rewrite, sync-plan, and import Claude Code skills from ~/.claude/skills into Codex skill folders. Use when the user asks to compare Claude Code skills with Codex skills, decide what to sync, bring Claude skills into Codex, migrate, port, import, copy, transform, or adapt Claude Code skills into Codex's SKILL.md format with optional scripts, references, assets, agents/openai.yaml metadata, and validation.
---

# Claude Code Skill Importer

## Workflow

1. Identify the source: a Claude Code skill folder, `~/.claude/skills`, Claude Project instruction, Claude knowledge file, pasted prompt, exported archive, or related Claude-side material. If the user has not provided any source material or path, check `~/.claude/skills` first, then ask if it is missing.
2. When the source is a collection or the user mentions compare, sync, import all, update, or reconcile, run the comparison step first and stop for user approval before changing Codex skills.
3. Decide whether this is a direct conversion or a rewrite:
   - Direct conversion: preserve most instructions when the source is already concise and agent-facing.
   - Rewrite: reorganize verbose, UI-facing, or provider-specific material into Codex's progressive-disclosure format.
4. Create or update the Codex skill under `$CODEX_HOME/skills` when available, otherwise `~/.codex/skills`, unless the user specified another destination.
5. Keep `SKILL.md` lean and procedural. Move long examples, provider-specific notes, schemas, policies, and detailed references into `references/`.
6. Put deterministic helper code in `scripts/`; put reusable templates, icons, sample files, and other copied output resources in `assets/`.
7. Create or update `agents/openai.yaml` with human-facing UI metadata.
8. Validate the result with the skill-creator `quick_validate.py` script when available.

## Compare Before Sync

Use `scripts/compare_skill_sets.py` to inventory Claude Code skills and Codex skills before bulk migration or sync:

```bash
python <this-skill>/scripts/compare_skill_sets.py
```

By default, the script compares `~/.claude/skills` with `$CODEX_HOME/skills` or `~/.codex/skills`. Pass `--claude` or `--codex` only when using nonstandard locations.

Show the comparison to the user before making changes. Include:

- `claude-only`: Claude Code skills that are candidates to import into Codex.
- `codex-only`: existing Codex skills with no matching Claude source.
- `both`: matching skill names on both sides.
- `both-description-diff`: matching skill names where the frontmatter descriptions differ.

After showing the table, ask the user what to sync. When `request_user_input` is available in the current mode, use it to present 2-3 concrete choices, such as importing Claude-only skills, updating selected matched skills, or reviewing one skill in detail. If `request_user_input` is unavailable, ask the same question as a concise plain-text prompt. Do not create, overwrite, delete, rename, or merge any skill until the user explicitly answers.

## Quick Conversion

Use `scripts/convert_claude_skill.py` for a first-pass conversion from a Claude Code skill file or folder:

```bash
python <this-skill>/scripts/convert_claude_skill.py <source> [--out <skills-dir>] [--name skill-name] [--overwrite]
```

If `--out` is omitted, the script writes to `$CODEX_HOME/skills` or `~/.codex/skills`.

After running it, manually review the generated skill. The script intentionally favors a safe draft over aggressive interpretation.

## Rewrite Rules

- Use lowercase hyphenated skill names under 64 characters.
- Make frontmatter contain only `name` and `description`.
- Put trigger conditions in the frontmatter `description`, because Codex sees that before loading the body.
- Remove Claude-specific UI wording that does not apply to Codex, such as project setup clicks, upload steps, artifact-only instructions, or chat-platform-only controls.
- Preserve operational constraints, safety rules, file conventions, command sequences, and validation steps.
- Convert long background explanations into concise imperative instructions.
- Replace "you are..." persona blocks with task-specific behavior only when it materially changes execution.
- Avoid creating extra README, changelog, installation guide, or tutorial files.

## Resource Mapping

- Source prompt, operating instructions, and short examples: fold into `SKILL.md`.
- Long examples, policies, schemas, API notes, and detailed playbooks: move to `references/`.
- Python, shell, JavaScript, or PowerShell helpers: move to `scripts/` and test representative scripts.
- Templates, images, sample documents, fonts, and reusable binary files: move to `assets/`.
- UI metadata: write `agents/openai.yaml`; keep it short and quote all string values.

For detailed review criteria, read `references/migration-checklist.md` only when converting a non-trivial skill or auditing an existing conversion.

## Validation

Run:

```bash
python <this-skill>/scripts/validate_codex_skill.py <path-to-skill>
```

The wrapper locates `quick_validate.py` under `$CODEX_HOME/skills` or `~/.codex/skills`. Fix validation errors before reporting completion.
