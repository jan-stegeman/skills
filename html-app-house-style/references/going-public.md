# Going public: the checklist (skill html-app-house-style, rule 11)

Learned with TensorTailor (public since 2026-11-14). The repo was public-ready all along (rule 11), so this list
only turns things on. Do every step **only after the user's OK**, one step at a time, and check the result.

## Before (repo still private)
1. **Name:** full trademark check of the app name: WIPO Global Brand Database and Benelux BOIP
   (boip.int, trademarks register); EUIPO TMview if it loads. Not legal advice; write the result in PROGRESS.md.
2. **Public-ready check** prints `OK public ready` on `main` and on the newest release file (download it; scan it with
   `--built`). Also look at every release and its notes, and at old Actions artifacts: delete what is not needed.
3. **Review** by two models of the code since the last review (global rule: review before a version goes out).
4. **Tokens:** every repo secret has the least rights it needs (for example a read-only Hugging Face token).
5. **Choices for the user:** Issues on (advice: on, with the issue forms), Discussions off, Wiki off.

## The switch
6. Visibility public: `gh repo edit jan-stegeman/<repo> --visibility public --accept-visibility-change-consequences`.
7. Then (these give 404 or stay off while the repo is private):
   - private vulnerability reporting: `gh api -X PUT repos/jan-stegeman/<repo>/private-vulnerability-reporting`;
   - secret scanning + push protection: `PATCH repos/jan-stegeman/<repo>` with `security_and_analysis`. In Windows
     PowerShell 5.1, send the JSON as a UTF-8 file with `--input file.json` (a piped string gives HTTP 400);
   - Dependabot alerts: `gh api -X PUT repos/jan-stegeman/<repo>/vulnerability-alerts`;
   - CodeQL default setup: `PATCH repos/jan-stegeman/<repo>/code-scanning/default-setup` with
     `{"state":"configured"}`. Fix a real alert; show a false one to the user before you dismiss it.
8. Rulesets (no pull-request rule, so the user and the workflows can still push): `protect-main` (default branch:
   block deletion and force-push) and `protect-release-tags` (`refs/tags/v*`: the same).
9. Check each setting with a GET call, then run the release workflow once as a dry run.

## After
10. The user opens the repo signed out (Chrome, Incognito window) and checks README, pictures, releases, Issues.
11. GitHub Actions are free for public repos: add the repo to `PUBLIC_SINCE` in `D:\AI\tools\actions_usage_all.py`
    and show the cost overview.
12. Update the project memory, PROGRESS.md, README (status), the start message and the Obsidian notes.
    Note: the "Contributors" box on the repo home page can lag behind; the Insights page and the API are right.
