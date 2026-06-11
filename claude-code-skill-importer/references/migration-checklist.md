# Migration Checklist

Use this checklist when converting a Claude Code skill, Claude Project instruction set, or Claude knowledge pack into a Codex skill.

## Source Audit

- Identify whether the source is a Claude Code skill, Claude Project instruction, knowledge file, or pasted prompt.
- If the source is a collection, compare it with the current Codex skills before converting anything.
- Separate durable task knowledge from Claude-specific setup text.
- Note whether the source contains executable helpers, examples, templates, or reference material.
- Preserve any required validation, safety, privacy, or data-handling constraints.

## Sync Gate

- Show `claude-only`, `codex-only`, `both`, and `both-description-diff` groups to the user.
- Explain what each group means in one short sentence.
- Ask the user which skills to import, update, skip, or review.
- Do not modify Codex skills until the user explicitly chooses a sync action.
- Treat deletions and overwrites as separate explicit actions, not as implied sync behavior.

## Codex Structure

- `SKILL.md` exists and starts with YAML frontmatter.
- Frontmatter contains only `name` and `description`.
- The description says what the skill does and when to use it.
- The body starts with the workflow Codex should follow after the skill is triggered.
- Long or rarely needed details are moved to directly linked files under `references/`.
- Scripts are executable or clearly runnable with standard tooling.
- Assets are not duplicated in `references/`.
- `agents/openai.yaml` has `display_name`, `short_description`, and `default_prompt`.

## Rewrite Quality

- Instructions are written for Codex, not for a human using Claude's web UI.
- The skill avoids generic advice that Codex already knows.
- The workflow is specific enough to prevent repeated rediscovery.
- The skill tells Codex when to read references and when to run scripts.
- Examples are short and realistic.
- Provider-specific terms are kept only when they are part of the user's domain.

## Validation

- Run `quick_validate.py` on the skill folder.
- Open `SKILL.md` and verify the description is trigger-friendly.
- If scripts were added, run at least one representative command.
- For complex migrations, test the skill on one realistic source artifact and revise based on failure points.
