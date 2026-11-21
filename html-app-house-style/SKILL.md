---
name: html-app-house-style
description: House style and project setup for the user's standalone single-file HTML apps (TensorTailor, GlyphGarage and every new one), so they form one suite. Shared colours, fonts, top bar, logo, light/dark, version "vYYYY.MM.DD" or "dev build" plus commit, one accent colour per app, folders, repo, docs and checks, and a repo that is ready to go public from day one (public-ready check, going-public checklist). Use when you start, restyle, build or review such an app, choose the name or colour of a new one, or prepare its repo to go public.
---

# HTML App House Style

The user's standalone HTML apps form one suite: they look and work the same; only the accent colour and logo
icon differ. TensorTailor (`D:\AI\tools\llmfit-studio`) is the reference. Agreed with the user on 2026-11-15.

## 1. When This Applies
- Every app that is one HTML page, opened by a double-click in Chrome (file://), with no server.
- New apps, and every change to the look of an existing one. A desktop program (tkinter, WinForms) is not covered.

## 2. Source of Truth
- `references/house-style.css`: the shared tokens (light, dark when Windows is dark, dark when chosen) and base
  rules. Copy the three token blocks into the app's own `<style>` unchanged; the app adds only its accent tokens and
  app-only tokens (for example TensorTailor's `--seg-*`).
- `references/apps.md`: every app with its folder, repo, theme key, accent tokens and logo colours.
- To change the house style: change these files first (with the user's OK), then update and rebuild every app, then
  run the check (rule 10) on each. Never change shared tokens inside one app only.

## 3. Look
- Fonts: `--font` Segoe UI Variable Text, `--display` Segoe UI Variable Display (titles, app name), `--mono` Cascadia
  Mono (codes, numbers in tables, keys). Body `14px/1.45`.
- Surfaces: `--bg` page, `--panel` cards, `--side` sidebar, `--sunken` inputs and search. Cards: `--radius` 14px and
  `--elev` (a hairline ring, no heavy shadow); menus and dialogs: `--pop`.
- Status colours keep one meaning in every app: `--perfect` green = good, `--good` blue = info, `--marginal` amber =
  warning, `--tight` red = fault. Never use them as decoration.
- Focus ring `2px solid var(--accent)`; respect `prefers-reduced-motion`; contrast at least 4.5:1 (WCAG AA).
- `[hidden] { display: none !important; }` is a base rule: without it, an element with its own `display` (flex,
  grid) stays visible when hidden. Tests check real visibility (`el.checkVisibility()`), not the attribute.
- PC only: full keyboard use; no phone layout unless the user asks.
- Tool pages use the shared components in `references/components.md`: card up to 1480px, equal step boxes, real
  view tabs, tiles plus a table view, sticky table headers, Copy on hover/focus, chart panels, menu glyph tiles, a
  picture editor dialog, empty states and amber "not a real result" labels.

## 4. Top Bar
- Left, the brand: logo square (30px, radius 9px, radial gradient of the app's 3 logo colours, a white line icon,
  stroke 2.2), the name (`--display`, 700, 15px), and under it the version line (`.brand-sub`, 11px, `--faint`).
- Middle: search with a `/` key hint (`<kbd>/</kbd>`); `/` focuses it, `Esc` clears or leaves it.
- Right, icon buttons: Help (`?` opens it, `Esc` closes) and a Tools menu (☰) with "Light or dark" (key `T`, a
  half-filled circle icon) and "About and licenses"; an app may add its own items to that menu.
- Theme: follows Windows (`prefers-color-scheme`) until the user chooses "Light or dark"; the choice goes in
  `localStorage` under `<prefix>-theme` (see apps.md) as `data-theme` on `<html>`. Wrap storage in try/catch
  (`safeGet`/`safeSet`).

## 5. Accent Colour per App
- Each app has its own accent (`--accent`, `--accent-2`, `--accent-soft`, `--accent-text`, `--accent-ring`) in all three
  token blocks, and logo tokens `--logo-1/2/3`, `--logo-glow`. Taken: TensorTailor indigo, GlyphGarage teal, PromptPrism fuchsia.
- A new app: pick a free colour (rules in apps.md), show the user 2-3 choices as pictures in light and dark, let them
  choose, then add the app to apps.md.

## 6. Version
- The build writes a build-info object into the page: `built` (YYYY-MM-DD), `commit` (7 characters of
  `git rev-parse --short=7 HEAD`, or `local`), `version`.
- `version` is a release tag `vYYYY.MM.DD` (a second release that day: `vYYYY.MM.DD-2`), taken only from an
  environment variable `<PREFIX>_VERSION` that matches `^v\d{4}\.\d{2}\.\d{2}(-\d+)?$`; otherwise empty.
- The page shows `version`, or `dev build <commit>` when it is empty: under the name, in About (with build date and
  commit) and in the README's "how to check your version".

## 7. One Offline File
- `web\` holds the source; a build script writes `dist\<name>.html` with all CSS, JS, data and icons inside. No CDN,
  no web fonts, no external images.
- An app that needs no network gets a Content-Security-Policy `<meta>` that blocks it (`default-src 'none'` plus
  inline style and script); its test proves zero network requests. An app that must use the network (TensorTailor:
  Hugging Face) names every host in README and SECURITY.md.
- Data (codes, word lists, tables) is never typed by hand: compute it or take the official file, test it, and list
  each source with its license in THIRD-PARTY-NOTICES.md.

## 8. Project Setup
- Folder `D:\AI\tools\<folder>`; `web\` source, `dist\` output (ignored), `tools\` scripts and tests; `PROGRESS.md`,
  `research\`, `design\` stay on the PC only (in `.gitignore`).
- Files like TensorTailor: README.md (with a "No warranty" line), LICENSE (MIT), SECURITY.md, CONTRIBUTING.md,
  ACCESSIBILITY.md, THIRD-PARTY-NOTICES.md, `.github` PR template and issue forms (`ISSUE_TEMPLATE\*.yml`,
  `config.yml` with blank issues off), `.gitattributes`. Repo-local git e-mail: the GitHub no-reply address.
- Build script: `web\build.mjs` (Node) like TensorTailor; data generators may be Python (one environment per
  project under `D:\AI\envs`).
- GitHub repo `jan-stegeman/<name>`, private first. Before it goes public: full trademark check of the name (WIPO
  Global Brand Database + BOIP).
- Also: a T3 project, a Claude project memory, a handover `D:\AI\tools\<Name>-handover.md`, and the
  Obsidian entry (`chat_to_obsidian.py` REPOS, START_MESSAGES, PROJECT_REPORTS; Index.md section).
- Umbrel backup from the first commit: ask the user, add the repo to
  `D:\AI\tools\Dictate-Speak-work\scripts\backup-repos.json`, run `Start-ScheduledTask GitBundleBackup`, and check
  its OK line in `D:\AI\logs\git-backup.txt`.
- Commits follow rule 18 of `user-preferences` (model and effort level in subject and author).

## 9. Tests for Every Step
- Build, then open the page in headless Chrome by file://: pictures in light and dark, no console errors, the
  network check, and the data tests.
- Steps for the user always say Chrome, never Edge.

## 10. House Style Check
Run it on the source and the built file after every change to the look; it must print `OK`:
```powershell
& "D:\AI\envs\<project>\Scripts\python.exe" -I -X utf8 "$HOME\.agents\skills\html-app-house-style\scripts\check_house_style.py" "D:\AI\tools\<folder>\web\<page>.html"
```
It compares every shared token with `house-style.css`, checks the accent tokens in all three blocks, and checks
contrast (4.5:1). Add it to the app's own test list. After a change to the script itself, run
`scripts\test_check_house_style.py` (it must print "all ... tests passed").

## 11. Ready to Go Public From Day One
Every repo starts private but stays ready to go public, so going public needs no clean-up round. Add this check to
the app's test list from the first step; it must print `OK public ready`:
```powershell
& "D:\AI\envs\<project>\Scripts\python.exe" -I -X utf8 "$HOME\.agents\skills\html-app-house-style\scripts\check_public_ready.py" "D:\AI\tools\<folder>" --built "dist\<name>.html"
```
- It fails on: a commit e-mail that is not no-reply; private text, keys, tokens, user folder paths, home-network
  addresses or e-mail addresses in the files, their history, commit messages or the built page; work notes in git;
  a missing public file; a workflow action not pinned by SHA, without `permissions:` or `persist-credentials: false`.
- Private words: `~/.config/public-ready/private.txt`, on the PC only. Accept a third-party hit (an address a
  license requires) only with a narrow `--allow` regex and a comment in the test script.
- Never print a private value in chat or logs in full. Workflows: token with least rights, Dependabot for actions.
- Going public: follow `references/going-public.md`; every step only after the user's OK.
- After a change to the script, run `scripts\test_check_public_ready.py` ("all ... tests passed").
