# Components: the shared look of tool pages (skill html-app-house-style, rule 3)

Agreed with the user on 2026-11-15 (GlyphGarage design pass, mockup B: "the finesse within the house style").
Reference: GlyphGarage `web/app.html` (Alt codes and ASCII table). Use these in every app; values are for
14px body text.

## Page and card
- Content area: padding `24px 28px 48px`; store the top padding in `--content-pad-top` (sticky headers use it).
- Card: `--panel`, `--radius`, `--elev`, padding `22px 26px 26px`, `max-width: 1480px` (no empty band on wide
  screens, no endless lines). Title `h1` 22px weight 650 (`--display`), one `--muted` sub line of 14px.
- Scrollbars: the thin `::-webkit-scrollbar` block of `house-style.css` (8px, a `--line-2` thumb, `--faint` on hover,
  no track and no arrows), in lists, tables, dialogs and Help alike. Never set `scrollbar-width` or `scrollbar-color`
  on an element: Chrome 121+ then shows its own bar there and ignores the block (agreed 2026-11-21).

## Steps ("how to")
- Equal boxes in one row: `display: grid; grid-template-columns: repeat(N, minmax(0, 1fr)); gap: 10px`.
- Each box `--panel-2` + `--elev`, radius 10px, padding `10px 12px 10px 42px`; the number in a 20px accent circle,
  `position: absolute; left: 12px; top: 10px`. Never a wrapping flex row (uneven steps look homemade).
- A sub line under the step name gets at most 2 lines (`-webkit-line-clamp: 2`, `text-wrap: balance`, no single word
  alone) and the whole text as its `title`.

## Toolbar
- View switch = real tabs (`role="tablist"`, arrow keys, Home/End, only the chosen tab has `tabindex="0"`),
  buttons 32px high. Filter box 36px high, at most 460px wide. Group chips 30px high, 12.5px text.
- The chosen tab is `--panel` on a `--panel-2` track. In dark mode `--panel` is darker than the track (1.06:1), so
  there, in both dark paths, it is `color-mix(in srgb, var(--text) 9%, var(--panel-2))` (1.27:1). PromptPrism `.tabs`
  and GlyphGarage `.seg` (2026-11-21).
- Input fields, lists (`select`), number boxes and search boxes: a 1px `--field-line` border on a `--sunken` fill;
  on focus the border is `--accent`. `--field-line` stands out 3:1 or more from `--panel`, `--panel-2`, `--raised`, `--sunken`
  and `--bg` (3.4:1 light, 3.3:1 dark; WCAG 1.4.11 asks 3:1 for the edge that shows where a control is), and
  `check_house_style.py` checks it. Never `--line` or `--line-2` for a field's edge: 1.3:1 is too faint (owner's
  choice B, 2026-11-23; this replaces the dark-only `--line-2` border of the search box).
- Controls that belong to some views only get `data-views="a b"` and are hidden in the other views.
- Many tabs in a narrow column (PromptPrism's result): short names on the buttons where needed; such a tab gets the
  full name as `title` and an `aria-label` that holds the visible name too (for example "JSON: Raw answer", plus
  ", 3 missing"). A row that still does not fit scrolls sideways instead of wrapping (`flex-wrap: nowrap;
  overflow-x: auto`, buttons `flex: none`, focus ring inside the button with `outline-offset: -2px`); the render
  code saves and restores `scrollLeft` when it draws the row again and scrolls the chosen tab into view.

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
- Toast and the screen-reader line inside dialogs (2026-11-23, PromptPrism): a modal `dialog` (`showModal()`) lies
  in the top layer, covers everything else and makes the rest of the page inert, so a `#toast` or `aria-live` line
  outside it is hidden under it and not read aloud. Move both into the dialog opened last (a MutationObserver on the
  `open` attribute of every dialog, a stack of open ones; back to `body` when none is open), before any text is set.
  In a dialog with a button bar (`.dlg-foot`) the toast sits 12px above that bar (`position: absolute`), never over
  its buttons. A fallback `<textarea>` for Copy goes into the same dialog. Test it: `document.elementFromPoint` at
  the toast's centre is the toast while a dialog is open. (GlyphGarage and TensorTailor still had the toast outside
  their dialogs on 2026-11-23: each app's own chat fixes it.)

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

## Calculator (like the Windows 11 calculator, Standard and Scientific)
Reference: GlyphGarage, Convert page (2026-11-26, checked against the real Windows 11 Calculator and its source).
- A panel with a head row (h2, real tabs **Standard | Scientific** (`.seg`, remembered), `--muted` sub line, a Deg /
  Rad / Grad segment of `aria-pressed` buttons when the page has trigonometry, and **Hide calculator** / **Show
  calculator** with `aria-expanded`, remembered), then a wrapping flex
  row: the device (`flex: none`, 360px) and a History | Memory side panel (`flex: 1 1 300px`, real tabs), so in a
  small window the side panel moves under the device instead of getting narrow.
- Device: padding 12px, radius 16px, its own app-only tokens `--cx-*` in all three token blocks (body, number keys,
  function keys, key ring, drop shadow, top highlight in dark, display background).
- Display: fixed height 118px (it never grows, so the keys never move), radius 11px, 1px `--field-line` border,
  `--accent` on focus. Two lines, right-aligned: the **small line** (13px `--muted`, one line, shrinks to 11px, then
  starts with …) holds the calculation so far (`0.3333333333333333 ×`); the **big line** (a read-only input, 600 36px
  `--display`, tabular figures, shrinks to 18px to fit) holds only the number typed now, the value of a function
  (√(9) → 3), the answer, or a short fault ("Cannot divide by zero"; the keys that need a number turn grey until C,
  CE or a digit). A Copy icon sits left of the big line; Copy gives the plain number without thousands commas.
- Keys: a 4-column grid, gap 5px, key 52px high, radius 8px. Three shades: digits `--cx-num` (600 19px `--display`),
  functions (% CE C ⌫ ¹/ₓ x² √x ±) `--cx-fn` (600 15px `--font`), operators `--cx-fn` in `--accent` (500 23px); `=`
  filled `--accent` / `--accent-text`. Pressed or keyboard-lit (`.down`, 120 ms): 1px down. Above the keys a memory
  row MC MR M+ M− MS (30px, transparent, MC and MR disabled while the memory is empty). `mousedown` is prevented so
  the display keeps its focus.
- Behaviour as in Windows: 16 significant digits shown and at most 16 typed; = again repeats the last operation;
  a new operator replaces the last one; ⌫ never removes an operator; MR or an answer is replaced by the next digit.
  Keyboard: digits, + - * / % ^, Enter or =, Backspace, Esc (C), Delete (CE), F9 (±), R, Q and @; Ctrl + V pastes a
  number or a calculation.
- Scientific: the device 452px, a 5-column grid, keys 46px, 35 keys in Windows' order (2nd π e C ⌫ / x² ¹/ₓ |x| exp mod
  / ²√x ( ) n! ÷ / xʸ 7 8 9 × / 10ˣ 4 5 6 − / log 1 2 3 + / ln ± 0 . =). **2nd** (`aria-pressed`, filled `--accent`
  while on) swaps the first column for x³, ³√x, ʸ√x, 2ˣ, logᵧx and eˣ; one clear key shows CE while a number is typed.
  Above the memory row two flat buttons: **DEG** (each click goes to RAD, GRAD, DEG; one angle setting with the head
  row's Deg / Rad / Grad) and **F-E** (`aria-pressed`). 32 digits; the big line may shrink to 13px. The small line marks
  the unit of a trig function as Windows does (sin₀ degrees, sinᵣ radians, sin₉ gradians), with a spoken copy ("sin
  degrees (30)") in an `.sr-only` live region. In a narrow window History | Memory moves under the device.
- Scientific menus (under the memory row): two flat disclosure buttons **Trigonometry** and **Function** (32px, icon,
  chevron that turns, `aria-expanded` + `aria-controls`). Each opens a panel over the top keys (`--panel`, `--pop`,
  radius 12px, padding 6px, keys 78 × 42px): Trigonometry `2nd sin cos tan / hyp sec csc cot` (its own 2nd and hyp,
  `aria-pressed`, keep the panel open; the keys change to sin⁻¹ …, sinh …), Function `|x| ⌊x⌋ ⌈x⌉ / rand →dms →deg`.
  One panel at a time; it closes after a function, with Esc, a click outside or when the focus leaves; opened with
  the keyboard the focus goes to its first key and Esc returns it to the button. Standard has no menus.
- Programmer (GG 37, like Windows 11 Programmer): the tab **Programmer** after Scientific; the same 452px device and
  5-column pad (46px keys, Windows' order `A « » C ⌫ / B ( ) % ÷ / C 7 8 9 × / D 4 5 6 − / E 1 2 3 + / F ± 0 . =`;
  digits outside the base and `.` grey). Under the display four rows HEX DEC OCT BIN (`role="radio"`, label 600 12px
  `--muted`, value 13.5px `--mono`; the chosen one has a 3px `--accent` bar and an accent label; a click chooses the
  base to type in; Copy icon on hover/focus); BIN keeps room for two lines so nothing moves. Then a row: real tabs
  **Keys | Bits** and a flat word-size button (QWORD → DWORD → WORD → BYTE). The menus row has **Bitwise** (panel of
  keys AND OR NOT / NAND NOR XOR) and **Bit shift** (a radio list of the four shift modes, drawn once so arrow keys
  keep the focus; « » become RoL RoR in the rotate modes). **Bits** replaces the pad by 64 bit buttons in 4 rows of 4
  groups (mono 600 19px, a 1 in `--accent`, bits above the word size grey and disabled, the bit number under every 4th
  bit, one tab stop with arrow keys), exactly as high as the pad. A 64-bit BIN answer shows on two lines over the
  (then transparent) input. The angle unit is hidden. Keys of Windows (`& | ^ ~ < > . \`, A–F, F9) but none of its
  F-keys for base and word size (the browser's). Engine: whole numbers in two's complement, every result wraps; Windows'
  rules (÷ and % toward 0, shift ≥ word size has no result, precedence × ÷ % Lsh Rsh > + − > AND NAND NOR > OR XOR;
  a word-size change keeps what was already worked out); tested against Python's integers and Windows' own answers.
- Rules taken from Windows' own engine (microsoft/calculator, MIT: rules only, no code): numbers written by its
  NumberToString (P = 16 or 32: below 1 the zeros after the point count, an exponent past two leading zeros, `1.e+400`);
  a digit after ) multiplies; equal precedence goes left to right; replacing an operator by a higher one keeps what was
  worked out, in brackets; = again repeats the operation worked out last; % is Y/100 after × ÷, else X × Y/100 (alone:
  0); x mod 0 = x; MS / M+ / M− finish the typed number. Keys that the browser uses itself (F3, F5, Ctrl + G/N/R/P/L)
  keep their job. An answer always matches the calculation that the small line shows.
- History and Memory: lists of right-aligned buttons (calculation 13px `--muted`, answer 600 20px `--display`),
  newest first, at most 20, max-height with its own scroll; a memory row shows MC / M+ / M− on hover or focus; an empty
  text says how to fill it; **Clear history** / **Clear memory** go with the tab. Kept in `localStorage` via safeGet /
  safeSet, read with try/catch and every entry checked (broken data = empty list).
- Calculations are read by the page's own parser, never `eval` / `new Function` (the house CSP blocks them anyway);
  exact apps calculate with BigInt fractions and test against a second implementation (Python `fractions`).

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

## Settings and the Internet switch (an offline app that may go online)
- Off by default, enforced by the page, not only by code: the CSP `<meta>` names the only hosts (`connect-src`), and
  a script in `<head>` right after it adds a second `<meta>` `connect-src 'none'` while the switch is off. Policies
  only add up, so "on" = remember it and reload without that tag; "off" = add the tag at once. The build checks both.
- The top-bar status pill is a button that opens Settings: **Offline** neutral grey with a lock; **Online** in
  `--marginal` on `--marginal-soft` with a globe, so it is never missed. Settings is a `dialog.dlg` (also in the ☰ menu).
- The switch is a `.toggle` with `role="switch"` and `aria-checked`, plus a small On/Off chip (`aria-hidden`); its
  state sentence beside it. Turning it on shows a warning panel first (`--marginal-soft`, 3px `--marginal` left
  border): a table of every host with what for, when and what it sees (IP address and time), then a filled
  **Allow** and a plain **Cancel**. The table is built from the same host list as the policy; a test compares them.
- Under it, "What the page uses the internet for": one `dl` row per job with the data's date, when it was fetched,
  the last check, a fault in words and the next try; a manual "Get … now" button only while on.
- Data from the internet shows its age where the answer is, not only in a grey note: a label right under the answer
  (`--panel-2`, 1px `--line-2` ring, text colour, clock icon in `--accent`, date and time 600) such as "ECB rates of
  2026-11-16 · fetched 2026-11-16 18:08 from …" (no "today" or "3 days ago": the user reads the date), also
  offline; built-in data says so. The grey note and the card heading then leave the date out: one place only.
- Favourites in a card grid: a small star button at the card's top right (☆ / ★ in `--marginal`, `aria-pressed`, its
  own label), outside the copy button; `.fchip` buttons "★ Favourites (n)" / "All n" above the grid (never `.kchip`,
  which the kind buttons use). A maximum is said in a toast; starring in "All" keeps "All" in view; the focus stays
  on the star after the grid is drawn again.
- Requests: credentials omitted, no referrer, no cache, no redirects, a time limit, short JSON read as numbers only,
  back-off after faults, nothing while the page is hidden. Tests never reach the internet: intercept every request
  (CDP Fetch), answer with fakes, count them, and count requests the policy blocked.

## Picture editor (one dialog for picture tools)
Agreed 2026-11-20/21 (PromptPrism, mockup approved, then a second-model UI review). Reference: PromptPrism
`web/app.html` (`dialog#dlgEdit`, `ed-*` CSS).
- One big `dialog.dlg.editor` (`min(1560px, 96vw)` × 92vh) instead of one dialog per tool. Grid: tool rail 84px |
  tool panel 380px | preview `minmax(0, 1fr)` | history 220px. At 1280px or less the history goes under the panel
  (panel 360px, history row 210px, its tip box hidden); when the window is ALSO low (max-width 1280px and
  max-height 820px) the dialog is 96vh and the history row 140px. A wide, low window keeps 92vh and the column.
- Tool rail = a vertical `role="tablist"` (ArrowUp / ArrowDown, Home / End): tiles 72px high and `flex: none` (a 2-line name
  fits, every tile the same, the rail scrolls), a 22px line icon above an 11.5px name; a small `--marginal` dot on
  a tool with changes not applied yet. The card that opens the editor keeps quick buttons with the SAME icons.
- Preview: Before / Split / After (`aria-pressed`), a split line with a round grip (also arrow keys), Fit, 100%
  (one picture pixel on one screen pixel), − / + and the wheel, and a typed zoom percentage box.
- History column: Undo / Redo (icons), Original, a bin icon for Clear history… (a short question), the steps as a
  list (click = go back), a tip box that names Ctrl + Z / Ctrl + Y (wide windows only). The card's history uses the
  same icons with words and a hint line under its list ("No edits yet. …" and the keys).
- Footer: a state line (`aria-live`; "Not applied yet: …"), honest step progress for full-size work ("Step 2 of 3 …"
  plus seconds, never a fake percentage), Download "Download the …" (download icon), a filled Apply, Close `Esc`.
- Short button rows in a narrow panel never leave one button alone: a grid (ratios 3 per row; 2 + 1 full width).
  Presets too: a 2-column grid of equal cells, names centred (never one preset alone on a row).
Added 2026-11-23 (PromptPrism reviews of 2026-11-22/23, the owner's OK):
- Opening: the rail scrolls the chosen tool's tile into sight (only the rail, never the dialog) and the keyboard
  starts on that tile. Rail and panel show soft scroll shadows at an edge with more content.
- Split waits for a change: with nothing changed, the split line, its grip and the Before/After labels stay hidden
  (two equal halves say nothing); they appear at the first change. Tools with one view (Crop, Rotate, Four corners)
  show only the result and hide Before / Split / After.
- The checkerboard sits only behind the picture (where it is see-through), never over the whole stage.
- Sub-tabs inside a panel (Light & tone / Colour / Effects) fill their row (`flex: 1 0 auto`).
- A number box keeps Apply ready while you type in it: a grey Apply under the mouse would lose the click; the
  typed number counts on Enter, on leaving the box, or when Apply is clicked.
- Every tool panel ends with a Reset row (`.snd`, small secondary buttons): "Reset" puts that tool's settings back
  to the values the editor opens with; "Reset all" on a panel with tabs or groups, next to "Reset this channel" /
  "Reset this group". The picture and the history never change. Each Reset says what it did in one short toast
  ("Crop box reset.", "Rotation reset. New size: …") and clears the footer message; when there is nothing to reset
  it says so.
- Footer: the message has its own space (`flex: 1 1 260px`, it wraps to two lines) so the buttons stay on one row
  at 1100px. A hint in the footer (a practice hint, a reset note) goes at the first change, as every footer message.

## Empty states and caution labels
- An area with nothing yet (no result, a stage not built yet): GlyphGarage's `.empty-state`, a 1px dashed
  `--line-2` box, radius 10px, padding 16px, muted 13px centred text. Say what will be there and how to get it (with
  the key, `<kbd>`), and offer one way on: a button (Load an example, only when there are examples) or a "Go to …"
  link (`a.sbtn`, no underline) whose click opens that stage and moves the focus to it in the side bar.
- A drop zone is NOT an empty-state box: a 2px dashed `--line-2` border, radius 12px, `--sunken`, min-height 240px,
  centred text, and a 36px picture line icon (stroke 1.5) in `--faint` above it.
- A side-bar item that is not built yet: a small "soon" tag (`--sunken`, `--faint`, 10.5px) with a screen-reader comma.
- A grey (disabled) main button gets a line under it that says why and what to do; that line is its
  `aria-describedby`.
- "Not a real result" (a test engine, an example): an amber label (`--marginal` on `--marginal-soft`), never red:
  red only means a fault.

## Check
- Look at every test picture in light and dark, at 1600 px and at a small window (1100 px): no horizontal scroll,
  no cut text, equal boxes, equal rows. Then a page-only picture of the user's Chrome (after their OK).
