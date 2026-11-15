# Components: the shared look of tool pages (skill html-app-house-style, rule 3)

Agreed with the user on 2026-11-15 (GlyphGarage design pass, mockup B: "the finesse within the house style").
Reference: GlyphGarage `web/app.html` (Alt codes and ASCII table). Use these in every app; values are for
14px body text.

## Page and card
- Content area: padding `24px 28px 48px`; store the top padding in `--content-pad-top` (sticky headers use it).
- Card: `--panel`, `--radius`, `--elev`, padding `22px 26px 26px`, `max-width: 1480px` (no empty band on wide
  screens, no endless lines). Title `h1` 22px weight 650 (`--display`), one `--muted` sub line of 14px.

## Steps ("how to")
- Equal boxes in one row: `display: grid; grid-template-columns: repeat(N, minmax(0, 1fr)); gap: 10px`.
- Each box `--panel-2` + `--elev`, radius 10px, padding `10px 12px 10px 42px`; the number in a 20px accent circle,
  `position: absolute; left: 12px; top: 10px`. Never a wrapping flex row (uneven steps look homemade).

## Toolbar
- View switch = real tabs (`role="tablist"`, arrow keys, Home/End, only the chosen tab has `tabindex="0"`),
  buttons 32px high. Filter box 36px high, at most 460px wide. Group chips 30px high, 12.5px text.
- Controls that belong to some views only get `data-views="a b"` and are hidden in the other views.

## Tiles (cheat-sheet view)
- Grid `repeat(auto-fill, minmax(86px, 1fr))`, gap 8px; tile 94px high, `--panel-2` + `--elev`, radius 10px.
- Big glyph 27px; the main code 600 12px `--mono` in `--accent`; the second code 11px `--mono` `--muted`;
  missing code = a `--faint` dash. Hover: `--accent-soft` + inset ring `--accent-ring`.
- A tile is a `<button>`: `aria-label` = character, name and every code; `title` = the name. Groups get an `h2`
  with a live count (the number of tiles that match the filter); a group without matches is hidden.
- Always offer a table view of the same data (names, for search and screen readers); one filter drives both.
- Word tiles (word lists, for example BIP39): grid `minmax(118px, 1fr)`, tile 62px high; the word 15px `--muted`
  with the part that matters (the first 4 letters) 650 `--text`; the number below like the main code. Their filter
  matches from the start of a word, and a typed number is that exact item number (`data-match="start"`).

## Tables
- Header: `position: sticky; top: calc(-1 * var(--content-pad-top))`, `--panel` background, inset bottom line,
  11px uppercase, letter-spacing .05em, `white-space: nowrap` (one fixed height). Cells padding `7px 12px`.
- The scrolling content area gets `scroll-padding-top` a bit more than the header height (48px): a control that
  gets keyboard focus then scrolls below the header, never behind it. Test it: focus a Copy button that sits under
  the header and check that `elementFromPoint` on its centre returns the button.
- Row actions (Copy): `opacity: 0`, shown on row hover and on `:focus-visible` (keyboard users see them).
- Equal row heights: a big glyph cell gets `line-height: 1`; cells with a glyph or a button get no vertical
  padding, so plain text sets the row height. Test it (row heights within 2px).

## Charts and grids of codes
- Each chart is its own panel: `--panel-2` + `--elev`, radius 12px, padding `14px 16px 16px`; `h2` 14px plus a
  `--muted` 12.5px sub line. Table `border-spacing: 4px`.
- Cells: `--panel` + `--elev`, radius 8px, 54px high; glyph `400 19px/1 var(--mono)` (box-drawing characters join
  up), code 10.5px `--mono` `--muted`; empty cell transparent with an inset `--line` ring.
- Invisible characters (space, nbsp, soft hyphen, empty) show a tag: `600 9px`, uppercase, letter-spacing .06em,
  `--sunken` background, `--muted` text.

## Menu and tips
- Menu glyphs: 26px tiles, radius 7px, `--panel-2` + `--elev`, `600 11.5px var(--mono)`; the open tool's tile is
  `--accent` with `--accent-text`.
- Tips ("Good to know"): `--panel-2` + `--elev`, radius 10px, padding `14px 18px`, a 3px `--accent` left edge.

## Check
- Look at every test picture in light and dark, at 1600 px and at a small window (1100 px): no horizontal scroll,
  no cut text, equal boxes, equal rows. Then a page-only picture of the user's Chrome (after their OK).
