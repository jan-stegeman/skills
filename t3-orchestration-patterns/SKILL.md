---
name: t3-orchestration-patterns
description: Guidelines and best practices for multi-agent workflows, subagent delegation, background task execution, and worktree isolation in T3 Code
---

# T3 Code Orchestration Patterns

## Architectural Philosophy
T3 Code manages agent execution across native subagents, external delegates, and background tasks. Maximize efficiency by choosing the right execution pattern for the task.

## Delegation Strategy

1. **Native Subagents (`invoke_subagent`)**:
   - **When to use**: Fast, focused, read-only research, documentation lookups, or bounded parallel tasks that finish in the current turn.
   - **Context**: Use `role: 'research'` for codebase exploration to keep the primary thread context clean.
   - **Execution**: Run concurrently; do NOT poll or sleep while waiting. The system wakes up reactively.

2. **Full Delegate Tasks (`delegate_task`)**:
   - **When to use**: Heavy refactoring, separate worktrees (`isolation: "worktree"`), running a different provider model (e.g., Claude 3.5 Sonnet / Opus, OpenAI o3/Codex), or tasks requiring user review cycles.
   - **Protocol**: Call `orchestrator_capabilities` once before the first delegate task.
   - **Review loops**: Treat every review or re-check as a fresh `delegate_task` brief. Cancel stale or redundant delegates with `task_cancel`.

3. **Background Commands & Tasks (`run_command`)**:
   - **Interactive / Long-running**: When executing compilation, testing, or server processes, run with appropriate timeouts.
   - **Strict Turn Ending**: Immediately after launching a background task, either proceed to independent work or report to the user and end the turn. Never loop `manage_task status`.

## Worktree Isolation
- Use isolated worktrees for risky, destructive, or experimental changes.
- Ensure the agent's work is linked to a Pull Request or clean feature branch before handoff.
