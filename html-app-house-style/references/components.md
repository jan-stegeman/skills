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

## Converters (two boxes that fill each other)
- `.conv`: two equal columns (`repeat(2, minmax(0, 1fr))`, gap 16px). Each box: a head row (label 600 on the left,
  a Copy button on the right, disabled while the box is empty), a textarea (min-height 150px, `--sunken`, 1px
  `--line`, radius 10px, padding `10px 12px`; on focus an `--accent` border and `--panel`; codes in `--mono` 15px)
  and a note line below it (12.5px `--muted`, min-height 20px, `aria-live="polite"`).
- Typing in one box fills the other. The page's filter and group buttons are hidden in this view (`data-views`).
- Never drop input silently: the note names every character or code that has no translation.

## Number boxes (several bases or units that fill each other)
- One row per box: `grid-template-columns: 150px minmax(0, 1fr) 70px` (name with a `--muted` 11.5px `--mono` sub
  line such as "base 16 · 0x", the box, Copy). Box: textarea `rows="1"`, `--mono` 15px, min-height 46px, no resize;
  it grows with its text (height = scrollHeight, also from a `ResizeObserver` via `requestAnimationFrame`), and
  Enter adds no line. One `aria-live` note under all boxes; a box with wrong input gets a `--tight` border and the
  note names every wrong character.
- A code in a table that copies itself: a `<button class="kb">` that looks like a code tag (`--sunken`, 1px `--line`,
  radius 6px, 12.5px `--mono`) and lights up like a tile on hover; it copies the text without spaces. Use it when a
  row has several codes, instead of one Copy per row.
- Small tables inside a panel use their own class (not `.tbl`): the page filter works on every `.tbl tbody tr`.
- Never name a class after a page part (`.wrap`, `.top`, `.side`, `.content`, `.card`): it takes that part's layout.
- A choice inside a tool view (for example the kind of unit) looks like the group chips but has its own class
  (`.kchip`, `aria-pressed`): `.chip` is wired to the page filter.
- Unit converter: From and To each have a number box above a `<select>` of units (US and UK named once: "Pint (UK)
  (pt)"), `=` between them, and below them a list of the value in every unit of that kind, with From and To marked.

## Drawn codes (Morse)
- Dots and dashes as round marks in `--accent`: dot 6×6px, dash 16×6px, radius 3px, gap 3px; the text form (`.-`)
  below them in `--mono` 12px with letter-spacing .12em; tile grid `minmax(104px, 1fr)`. The marks are
  `aria-hidden`; the tile's label says the code as text.

## Sound controls
- A row (`.snd`, flex, gap `10px 16px`): a filled **Play** button (`--accent`, `--accent-text`, 34px high, radius 9px),
  plain buttons (`--panel-2` + `--elev`: Stop, Save as …), range sliders with their label and an `<output>` that
  shows the value (`accent-color: var(--accent)`), and the item that plays now in `--accent` (aria-hidden).
- Never a surprise sound: sound starts only on a click; a "Sound on click" option is a toggle button
  (`aria-pressed`, off at the start). Play moves focus to Stop; at the end focus goes back to Play.
- Make sound in the page (Web Audio, 5 ms fade in and out per tone); a saved sound file is built in memory and
  downloaded with a `blob:` link. Test the real download (cdp_test `"download"` step).

## Colours
- Colour tiles: grid `minmax(150px, 1fr)`, tile 104px high; on top a colour field (46px, radius 7px, inset `--line`
  ring so white shows on a white tile), the name 12.5px `--text`, the hex code like a main code. Inline
  `style="background:#…"` is fine under the house CSP (`style-src 'unsafe-inline'`).
- Several codes in one table cell (`display: flex; flex-wrap: wrap; gap: 4px 6px`) instead of one column each, so the
  table fits 960 px; each code is a self-copying `.kb` that keeps its spaces (`rgb(0, 128, 128)`).
- Colour converter: a wide preview with white and black text on the colour and `<input type="color">` beside it
  (Chrome's picker), then number-box rows with single-line inputs; a refused box gets `aria-invalid="true"`.
- Contrast results: Pass / Fail as a word with ✓ / ✗ in `--perfect` / `--tight` (never colour alone); a ratio is cut
  off at 2 decimals, never rounded up to a pass. Short column heads (AA, AA large …) with `white-space: nowrap`.

## Calculator keys and history
- A panel with a head row (h2, `--muted` sub line, a **Hide keys** / **Show keys** button with `aria-expanded`,
  remembered), then a wrapping flex row: the keys (`flex: none`) and the history (`flex: 1 1 300px`), so in a small
  window the history moves under the keys instead of getting narrow.
- Keys: grids of 52px columns, gap 6px, key 38px high, radius 9px, `--panel` + `--elev`, `--mono` 600 15px;
  operators in `--accent`; `=` filled (`--accent`, `--accent-text`), wide keys `span 2`. A key types at the cursor of
  the typing line; `mousedown` is prevented so the line keeps its focus and cursor. A two-way choice (Deg / Rad) is a
  small segment of `aria-pressed` buttons, the pressed one filled with `--accent`.
- History: a list of buttons (line on the left, answer in `--accent` on the right, `overflow-wrap: anywhere`), newest
  first, a fixed maximum, max-height with its own scroll; an empty text says how to fill it; **Clear history**. Kept in
  `localStorage` via safeGet / safeSet, read with try/catch and every entry checked (broken data = empty list).
- Sums are read by the page's own parser, never `eval` / `new Function` (the house CSP blocks them anyway).

## Clocks (time zones)
- A card per city (grid `minmax(210px, 1fr)`): name 13px 600 with a × remove button (`aria-label` "Remove …"), the
  time `--mono` 600 26px in `--accent`, under it the same time on the 12-hour clock (`--mono` 600 13px `--text-2`,
  "9:07 PM"), then date, the zone's own name from `Intl` ("Central European Standard Time") and offset lines 12px
  `--muted`; the user's own zone is marked like a current card (`--accent-soft` + `--accent-ring`), not removable, and
  has no "Here:" in its title (a `.sr-only` ", your own zone" for screen readers). Cards go in time order by their UTC
  offset now: behind the user on the left, their own zone, ahead on the right (same offset: order added); redraw when
  it changes.
- A converted time uses the same cards, static and as buttons (a click copies "2026-11-16 03:07"): In = To side by
  side (a small uppercase tag "In" / "To", To marked), and the same moment in every city below, in time order.
- Explain the clock words once on the page: UTC never changes; the user's zone in winter and summer (computed);
  24-hour and AM / PM (AM before noon, 00:30 = 12:30 AM, 12:00 = 12:00 PM); times come from the PC's clock.
- A running clock changes just after each whole second of the PC (`setTimeout` to the next second, not a plain
  1000 ms interval) and only while its page is shown. Times come from `Intl` only, never a typed offset rule.

## World map (time zones)
- One box with a fixed shape (`aspect-ratio`, here 3600 / 1640 = 84° N … 80° S, equirectangular), radius 10px,
  `--elev`. Inside: an SVG for what may scale (land, lines with `vector-effect: non-scaling-stroke`, night) and
  HTML on top, placed in %, for what keeps its pixel size (dots 5px, the sun, labels, the chosen ring).
- Colours are app tokens in all three token blocks (`--map-sea`, `--map-land`, `--map-night`, `--map-grid`,
  `--map-dot`, `--map-sun`); night is one semi-transparent layer per sun height (0°, -6°, -12°, -18°), so twilight
  darkens step by step. Check in dark that the night still shows.
- Many small dots are not tab stops: a click picks the nearest one within 16px. The user's own items are real
  buttons with a label (name + time, `--glass`) and an `aria-label`; the chosen one gets a `--panel` label with an
  `--accent` ring. A label goes left of its dot only when its measured box would stick out on the right (again on
  every resize, `ResizeObserver`), never by a fixed longitude. A label may cover other dots: a mouse click within
  6px of a dot picks that dot, elsewhere the label's own item; Enter/Space (click `detail` 0) picks the label's item.
  Test clicks through `elementFromPoint` (what really lies on top), not by dispatching on the map. Update label text
  in place (keep the focus).
- Under the map: the chosen item's running clock (like a clock card), one line of facts, and action buttons; a
  caption says what the shading means. Shapes from public-domain data, simplified at build time; sky positions from
  published formulas, tested against known moments (equinoxes, solstices, equation of time).

## Date rows (dates, weeks, Unix time)
- A row of labelled boxes is a wrapping flex row (`align-items: end`, gap 10px) with fixed label widths (date 190px,
  time 150px, list 150px, number 120px, wide `min(360px, 100%)`), so a small window moves boxes to the next line
  instead of squeezing them. Boxes 40px high, 15px; a **Today** / **Now** button at the end of the row.
- Dates are written `YYYY-MM-DD`; a card with seconds leaves out the weekday so the date stays on one line, and keeps
  milliseconds (`.123`) in its text and its Copy. A table row of the chosen item (the week of the chosen date) gets
  `--accent-soft`, its first cell in `--accent` 600.
- Calendar rules come from the browser's own `Date` in UTC (leap years, days of a month), never a typed table; an
  input the date box lets through (year 10000) is named, never a page error.

## Check
- Look at every test picture in light and dark, at 1600 px and at a small window (1100 px): no horizontal scroll,
  no cut text, equal boxes, equal rows. Then a page-only picture of the user's Chrome (after their OK).
