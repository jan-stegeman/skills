---
name: html-app-house-style
description: House style and project setup for the user's standalone single-file HTML apps (TensorTailor, GlyphGarage and every new one), so they form one suite. Shared colours, fonts, top bar, logo, light/dark, version "vYYYY.MM.DD" or "dev build" plus commit, one accent colour per app, folders, repo, docs and checks. Use when you start, restyle, build or review such an app, or choose the name or colour of a new one.
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
  token blocks, and logo tokens `--logo-1/2/3`, `--logo-glow`. Taken: TensorTailor indigo, GlyphGarage teal.
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
- Files like TensorTailor: README.md, LICENSE (MIT), SECURITY.md, CONTRIBUTING.md, ACCESSIBILITY.md,
  THIRD-PARTY-NOTICES.md, `.github` PR template, `.gitattributes`.
- Build script: `web\build.mjs` (Node) like TensorTailor; data generators may be Python (one environment per
  project under `D:\AI\envs`).
- GitHub repo `jan-stegeman/<name>`, private first. Before it goes public: full trademark check of the name (WIPO
  Global Brand Database + BOIP).
- Also: a T3 project, a Claude project memory, a start message `D:\AI\tools\<Name>-start-message.txt`, and the
  Obsidian entry (`chat_to_obsidian.py` REPOS, START_MESSAGES, PROJECT_REPORTS; Index.md section).
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
