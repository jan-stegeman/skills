---
name: skill-maintenance
description: Standards and automated workflow for creating, modifying, testing, and pushing AI skills across T3 Code, Claude, Antigravity, Gemini, and OpenAI (ChatGPT/Codex) directly to GitHub
---

# Skill Maintenance & Governance

This skill defines the canonical lifecycle for creating, updating, and synchronizing Agent Skills across all AI applications (T3 Code, Claude, Antigravity, Gemini, and OpenAI/ChatGPT/Codex) on this workstation.

## Central Source of Truth
- **Root Directory**: `C:\Users\Preferred Customer\.agents\skills\` (or `$HOME\.agents\skills`)
- **Remote Repository**: `https://github.com/jan-stegeman/skills` (`branch: main`)
- **Skill Format**: Each skill resides in its own folder named after the skill, containing a `SKILL.md` file with standard YAML frontmatter:
  ```yaml
  ---
  name: <kebab-case-name>
  description: <Concise, actionable explanation of what the skill does and when to activate it>
  ---
  ```

## Universal App Linking (Native Windows Junctions)
All AI applications on this workstation share this exact folder in real-time via native Windows NTFS junctions:
- **T3 Code / Universal**: `~/.agents/skills` (Direct Git repository)
- **Claude (Desktop & CLI)**: `~/.claude/skills`
- **Antigravity**: `~/.gemini/config/skills`
- **Gemini**: `~/.gemini/skills`
- **OpenAI / ChatGPT / Codex / Copilot**: `~/.codex/skills`, `~/.openai/skills`, `~/.chatgpt/skills`, `~/.copilot/skills`

**No third-party sync software or background daemon is required.** Any edit made in one place is immediately visible to all AI models.

## Mandatory Lifecycle for Changes

Whenever any AI agent creates, updates, or deprecates a skill:

1. **Write to Central Source**:
   Author or modify the skill directly inside `C:\Users\Preferred Customer\.agents\skills\<skill-name>\SKILL.md`.

2. **Verify Git Status**:
   ```powershell
   Set-Location "$HOME\.agents\skills"
   git status
   ```

3. **Validate Against Anthropic's Rules Before Every Commit**:
   Run Anthropic's own validator (from the `skill-creator` skill) on every skill folder you created or changed. It must print `Skill is valid!`; fix any error first and never commit a skill that fails. Also check by hand that the `name` field equals the folder name (the Agent Skills spec requires it; the validator does not check it). `-X utf8` matters: the validator reads files without an encoding, and Windows would read UTF-8 wrongly.
   ```powershell
   & "D:\AI\envs\skillspector\Scripts\python.exe" -I -X utf8 "$HOME\.agents\skills\skill-creator\scripts\quick_validate.py" "$HOME\.agents\skills\<skill-name>"
   ```
   Without that environment: `uv run --with pyyaml python -X utf8 "<same script>" "<same folder>"`.

4. **Commit, Then Push Only With Approval**:
   Stage only the skill folders you changed (and `README.md` when it changed), never `git add -A`: another file in the folder, or a credential, must not go along. Show what is staged, commit with Conventional Commits, and push to `main` only after the user's clear approval (rule 18 of `user-preferences`):
   ```powershell
   Set-Location "$HOME\.agents\skills"
   git add -- <skill-name>
   git diff --staged --stat
   git commit -m "feat(skills): add <skill-name> skill"
   git push origin main   # only after the user approved this push
   ```

5. **Size Check and Bloat Warning**:
   - Keep every SKILL.md file under 1,500 words (or under 20 bullet points).
   - If adding a rule causes a skill to exceed 20 points or 1,500 words, the model MUST warn the user before saving:
     *"Warning: This skill file is getting too long (more than 20 points). It is safer to split these rules into a new separate skill folder (e.g. database-rules, frontend-rules) or clean up older rules. Would you like me to split it or trim it?"*

## Best Practices
- **Single Responsibility**: Each skill should address a distinct operational domain (e.g., storage rules, orchestration, tooling).
- **No Hardcoded Secrets**: Never commit API keys, tokens, or personal credentials into `SKILL.md`.
- **Cross-Platform Awareness**: While this workstation is Windows 11 / PowerShell native, ensure prompt instructions specify the exact environment context.

