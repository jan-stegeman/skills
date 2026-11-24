---
name: ship-check
description: Fixed checklist before every git commit or push in the user's own repos, for all six tools (T3 Code, Claude, Gemini, Antigravity, ChatGPT, Codex). Level "small" for every commit, level "version" before a release, build tag or a build that leaves the PC. Use before you run git commit or git push, and when the user says "ship-check" or "oplevering", or asks whether something was forgotten.
---

# Ship Check

The local version of the Claude Ship idea (Anthropic, 2026-11-23): every change follows the same path, so nothing is
forgotten. Claude Ship itself needs a Team or Enterprise plan, and its watch does not start on native Windows. The
git hooks (`~/.githooks`: commit-msg, pre-push) stay the hard safety net; this list is the soft one.

## 1. When
- Before every `git commit` and `git push` in the user's own repos. One run per commit, not per file edit.
- Level **small**: every commit. Level **version**: a release, a `build-*` tag, a version bump, or a build that leaves
  the PC (USB, public).
- Project rules (handover file, start message) add to this list. If they differ, the project rule wins.

## 2. Level small (every commit)
1. **Scope.** Run `git status` and `git diff --stat`. Only files of this task. No secrets, `.env` files or private
   words. Stage named paths; never `git add -A`.
2. **Tests.** Run the project's test script; it must pass. App repos include `check_public_ready.py`. Say what passed
   and what was not tested.
3. **Review.** One review of only this change: in Claude `/code-review high`, in another tool a review subagent.
   Check every point yourself. Only confirmed faults count. A fix gets a test that failed first, where possible.
4. **Docs.** Search README, Help, CHANGELOG, ROADMAP, skill lists and screenshots for what changed, and update them in
   the same commit. Name the checked files in one line.
5. **Commit.** Message by the commit rule in `CLAUDE.md` and rule 18 of `user-preferences` (subject
   `Implemented by <model> <effort level>: type(scope): ...`; a Claude model is also the author). Write the message
   file as UTF-8 without BOM and use `git commit -F`. Never `--no-verify`.
6. **Undo line.** Tell the user how to undo it: `git revert <short sha>`.
7. **Push.** Only after the user's OK (rule 18); push finished work in one go. If the pre-push hook refuses: stop and
   tell the user. After a push to a repo with GitHub Actions: wait for the run, report its result, then show the cost
   overview (`D:\AI\uv\python\cpython-3.13.18-windows-x86_64-none\python.exe -I D:\AI\tools\actions_usage_all.py`).
8. **Log.** One row in `D:\AI\tools\Dictate-Speak-work\research\log\YYYY-MM-DD.md` (time from `Get-Date`), then
   this must report 0 invalid (the script needs `yaml` and the vault folder):
   `& "D:\AI\envs\skillspector\Scripts\python.exe" -I -X utf8 "D:\AI\tools\Dictate-Speak-work\scripts\check_vault_yaml.py" "D:\AI\tools\Dictate-Speak-work\research"`.
   Say it in one line.

## 3. Level version (adds to small)
9. Read the whole README before the push.
10. Two reviews by two different models of all code since the last public version (`delegate_task`); three after a
    big rebuild. Note per review how many points came in and how many were right.
11. Run the real build, not only read it. After fixes, run the real test round again.
12. Obsidian: review report and chat note as the project asks.
13. Big GitHub actions (release, new repo, rename, visibility): at most one a day, only with the user's OK.

## 4. Report
End with one block, in the user's language:

```text
Ship-check (klein): tests ✅ | review ✅ (4 punten, 1 terecht, opgelost) | docs ✅ README, Help | commit abc1234
terugdraaien: git revert abc1234 | push ⏳ wacht op je OK | log ✅
```

A skipped step shows ⏭ and the reason. Never ✅ for a step that did not run.

## 5. New checks start in observe mode
A new automatic check first only warns, for about one week. It blocks only after that, with the user's OK. The
pre-push hook was introduced the same way.
