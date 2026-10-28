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

3. **Commit & Push Directly to GitHub**:
   Adhere to Conventional Commits:
   ```powershell
   Set-Location "$HOME\.agents\skills"
   git add -A
   git commit -m "feat(skills): add <skill-name> skill"
   git push origin main
   ```

## Best Practices
- **Single Responsibility**: Each skill should address a distinct operational domain (e.g., storage rules, orchestration, tooling).
- **No Hardcoded Secrets**: Never commit API keys, tokens, or personal credentials into `SKILL.md`.
- **Cross-Platform Awareness**: While this workstation is Windows 11 / PowerShell native, ensure prompt instructions specify the exact environment context.
