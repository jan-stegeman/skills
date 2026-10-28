---
name: skill-maintenance
description: Standards and automated workflow for creating, modifying, testing, syncing, and pushing AI skills across tools and GitHub using Skillshare
---

# Skill Maintenance & Governance

This skill defines the canonical lifecycle for creating, updating, and distributing Agent Skills across AI CLI environments and T3 Code on this workstation.

## Central Source of Truth
- **Root Directory**: `C:\Users\Preferred Customer\AppData\Roaming\skillshare\skills\` (or `$env:APPDATA\skillshare\skills`)
- **Remote Repository**: `https://github.com/jan-stegeman/skills` (`branch: main`)
- **Skill Format**: Each skill must reside in its own folder named after the skill, containing a `SKILL.md` file with standard YAML frontmatter:
  ```yaml
  ---
  name: <kebab-case-name>
  description: <Concise, actionable explanation of what the skill does and when to activate it>
  ---
  ```

## Mandatory 4-Step Lifecycle for Changes

Whenever any AI agent creates, updates, or deprecates a skill:

1. **Write to Central Source**:
   Always author or modify the skill directly inside `$env:APPDATA\skillshare\skills\<skill-name>\SKILL.md`.

2. **Sync Locally Across All Targets**:
   Run the Skillshare synchronization command:
   ```powershell
   skillshare sync
   ```
   This ensures symlinks in `~/.agents/skills` (Universal / T3 Code), `~/.gemini/config/skills`, `~/.claude/skills`, and other targets are immediately updated.

3. **Verify Git Status**:
   Ensure no unwanted temporary files or binary artifacts are tracked:
   ```powershell
   Set-Location "$env:APPDATA\skillshare\skills"
   git status
   ```

4. **Commit & Push to GitHub**:
   Adhere to Conventional Commits:
   ```powershell
   skillshare push -m "feat(skills): add <skill-name> skill"
   ```
   or
   ```powershell
   skillshare push -m "docs(skills): update guidelines in <skill-name>"
   ```

## Best Practices
- **Single Responsibility**: Each skill should address a distinct operational domain (e.g., storage rules, orchestration, tooling).
- **No Hardcoded Secrets**: Never commit API keys, tokens, or personal credentials into `SKILL.md`.
- **Cross-Platform Awareness**: While this system is Windows 11 / PowerShell native, ensure prompt instructions specify the exact environment context.
