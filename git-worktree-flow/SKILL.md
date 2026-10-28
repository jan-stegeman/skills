---
name: git-worktree-flow
description: Worktree management, safe branching, Conventional Commits, and parallel non-blocking development rules for Git repositories
---

# Git Worktree & Branching Workflow

## Overview
Git worktrees allow multiple working branches to be checked out simultaneously in different folders, preventing context switching or dirty working trees when orchestrating multiple AI agents or parallel tasks.

## Worktree Conventions
- **Main Checkout**: Keep the root repository clean and aligned with `main`.
- **Branch Naming**:
  - `feat/<short-description>`: New features or capabilities.
  - `fix/<short-description>`: Bug fixes or patches.
  - `refactor/<short-description>`: Code restructuring without behavior change.
  - `chore/<short-description>`: Dependency updates, skill maintenance, or configuration.

## Conventional Commits Standard
All commit messages must adhere to the Conventional Commits specification:
```
<type>(<optional scope>): <short description in imperative mood>

[optional body explaining the 'why' behind architectural choices]
```
Examples:
- `feat(skills): add local-model-runner for Threadripper acceleration`
- `fix(storage): correct Hugging Face cache path to D:\AI\huggingface`
- `docs(orchestration): document subagent delegation patterns`

## Safe Git Operations
- Never force-push (`git push --force`) to `main` or `master`.
- Always verify branch status (`git status`) before committing.
- Clean up deleted worktrees with `git worktree prune`.
