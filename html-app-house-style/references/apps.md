# Apps in the suite and their accent colours

Each app has its own accent, so the user sees at once which app is open. Everything else is shared
(`house-style.css`). Add a new app here before you build it; `scripts/check_house_style.py` checks the contrast.

| App | Folder | GitHub repo | Theme key | Accent | Logo icon |
|---|---|---|---|---|---|
| TensorTailor | `D:\AI\tools\llmfit-studio` | jan-stegeman/tensortailor | `tt-theme` | indigo | "T" line icon |
| GlyphGarage | `D:\AI\tools\glyph-garage` | jan-stegeman/glyphgarage (private) | `gg-theme` | teal | "G" with a spark |

## Accent tokens

Put them in the same three blocks as the shared tokens: `:root`, the dark `@media` block and
`:root[data-theme="dark"]`. The `--logo-*` tokens can stay in `:root` only (the logo looks the same in both themes).

### TensorTailor: indigo (the reference; its .logo has the gradient written in)

| Token | Light | Dark |
|---|---|---|
| `--accent` | `#4f46e5` | `#8a8cff` |
| `--accent-2` | `#4338ca` | `#6d6ff5` |
| `--accent-soft` | `rgba(79, 70, 229, .09)` | `rgba(138, 140, 255, .13)` |
| `--accent-text` | `#ffffff` | `#0b0d14` |
| `--accent-ring` | `rgba(79, 70, 229, .3)` | `rgba(138, 140, 255, .35)` |
| logo 1 / 2 / 3 / glow | `#a8aaff` / `#6d6ff5` / `#3b2fc9` / `rgba(109, 111, 245, .42)` | same |

### GlyphGarage: teal

| Token | Light | Dark |
|---|---|---|
| `--accent` | `#0f766e` | `#2dd4bf` |
| `--accent-2` | `#115e59` | `#14b8a6` |
| `--accent-soft` | `rgba(15, 118, 110, .09)` | `rgba(45, 212, 191, .12)` |
| `--accent-text` | `#ffffff` | `#04201d` |
| `--accent-ring` | `rgba(15, 118, 110, .3)` | `rgba(45, 212, 191, .35)` |
| logo 1 / 2 / 3 / glow | `#8af0e2` / `#14b8a6` / `#0f5f58` / `rgba(20, 184, 166, .42)` | same |

Note: teal is close to the green status colour (`--perfect`), so GlyphGarage's "Offline" badge is neutral grey.

## Picking a colour for a new app

- Not used by another app above, and clearly different from the status colours: green `--perfect` (good),
  blue `--good` (info), amber `--marginal` (warning), red `--tight` (fault). Those keep their meaning in every app.
- Free examples: fuchsia (light `#a21caf`, dark `#e879f9`), rose (light `#be123c`, dark `#fb7185`). Rose is near red:
  only for an app without fault messages.
- Contrast (WCAG AA, 4.5:1 or more), checked by the script: `--accent` on `--panel` and on `--bg`, and
  `--accent-text` on `--accent`, in light and in dark.
- Show the user 2-3 accent choices as pictures (light and dark) and let them choose.
