"""Check that a standalone HTML app follows the house style.

Usage:
    python -I -X utf8 check_house_style.py <app.html or app.css> [more files ...]

For each file it compares the shared tokens with references/house-style.css in three blocks:
  light  = ":root { ... }"
  dark   = ':root:not([data-theme="light"]) { ... }' inside @media (prefers-color-scheme: dark)
  chosen = ':root[data-theme="dark"] { ... }'
A token that is missing or has another value is a fault. Extra tokens of the app are fine.
It also checks the app's own accent tokens: present in all three blocks, the same in both dark blocks, and
contrast 4.5:1 or more (WCAG AA) for --accent on --panel and --bg, and --accent-text on --accent.
Exit code 0 = follows the house style, 1 = faults found (listed), 2 = cannot read a file.
Only the Python standard library is used.
"""
import re
import sys
from pathlib import Path

REFERENCE = Path(__file__).resolve().parent.parent / "references" / "house-style.css"
ACCENT_TOKENS = ["--accent", "--accent-2", "--accent-soft", "--accent-text", "--accent-ring"]
BLOCKS = {
    "light": re.compile(r":root\s*\{([^{}]*)\}"),
    "dark": re.compile(r""":root:not\(\[data-theme=["']light["']\]\)\s*\{([^{}]*)\}"""),
    "chosen": re.compile(r""":root\[data-theme=["']dark["']\]\s*\{([^{}]*)\}"""),
}
DARK_MEDIA = re.compile(r"@media\s*\(\s*prefers-color-scheme\s*:\s*dark\s*\)\s*\{")
DECL = re.compile(r"(--[\w-]+|color-scheme)\s*:\s*([^;]+)(?:;|$)")
NAMED = {"white": "#ffffff", "black": "#000000"}


def css_text(path):
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in (".html", ".htm"):
        text = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", text, flags=re.S | re.I))
    return re.sub(r"/\*.*?\*/", "", text, flags=re.S)


def short_number(m):
    t = ("%.6f" % float(m.group())).rstrip("0").rstrip(".")
    return t[1:] if t.startswith("0.") else t  # 0.5 = .5 = .50


def norm(value):
    v = re.sub(r"\s+", " ", value.strip().lower())
    v = re.sub(r"\s*([,()/])\s*", r"\1", v)
    v = re.sub(r"#([0-9a-f])([0-9a-f])([0-9a-f])\b", r"#\1\1\2\2\3\3", v)  # #fff = #ffffff
    v = re.sub(r"(?<![\w#])\d*\.\d+", short_number, v)
    return NAMED.get(v, v)


def dark_media_bodies(text):
    """The text inside every @media (prefers-color-scheme: dark) { ... } (braces counted)."""
    bodies = []
    for m in DARK_MEDIA.finditer(text):
        depth, i = 1, m.end()
        while i < len(text) and depth:
            depth += {"{": 1, "}": -1}.get(text[i], 0)
            i += 1
        bodies.append(text[m.end():i - 1])
    return bodies


def blocks(text):
    out = {}
    for name, rx in BLOCKS.items():
        # The "follows Windows" dark block only counts inside its @media; outside it, dark would always be on.
        sources = dark_media_bodies(text) if name == "dark" else [text]
        tokens = {}
        for source in sources:
            for body in rx.findall(source):
                for key, value in DECL.findall(body.strip()):
                    tokens[key] = norm(value)
        out[name] = tokens
    return out


def parse_colour(value, under=(1.0, 1.0, 1.0)):
    """Return (r, g, b) in 0..1; a colour with alpha is laid over `under`."""
    m = re.fullmatch(r"#([0-9a-f]{3}|[0-9a-f]{6})", value)
    if m:
        h = m.group(1)
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    m = re.fullmatch(r"rgba?\((.*)\)", value)
    if m:  # rgb(1,2,3) rgba(1,2,3,.5) rgb(1 2 3/.5) rgb(1 2 3/50%)
        parts = [p for p in re.split(r"[\s,/]+", m.group(1)) if p]
        try:
            rgb = [float(p) / 255 for p in parts[:3]]
            a = 1.0 if len(parts) < 4 else (float(parts[3][:-1]) / 100 if parts[3].endswith("%") else float(parts[3]))
        except ValueError:
            return None
        if len(parts) not in (3, 4):
            return None
        return tuple(a * c + (1 - a) * u for c, u in zip(rgb, under))
    return None


def contrast(fg, bg):
    def lum(c):
        lin = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
        return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]
    a, b = sorted((lum(fg), lum(bg)), reverse=True)
    return (a + 0.05) / (b + 0.05)


HIDDEN_RULE = re.compile(r"(^|[\s}])\[hidden\]\s*\{\s*display\s*:\s*none\s*!\s*important")


def check(path, ref):
    text = css_text(path)
    app = blocks(text)
    faults, notes = [], []
    if not HIDDEN_RULE.search(text):
        # A warning, not a fault: apps made before 2026-11-15 (TensorTailor) hide element by element.
        notes.append("WARNING: no general rule [hidden] { display: none !important; } (house-style.css base rules)")
    shared = 0
    for name, ref_tokens in ref.items():
        for key, value in ref_tokens.items():
            shared += 1
            got = app[name].get(key)
            if got is None:
                faults.append(f"{name}: {key} is missing (house style: {value})")
            elif got != value:
                faults.append(f"{name}: {key} is {got}, house style says {value}")
    for name in BLOCKS:
        for key in ACCENT_TOKENS:
            if key not in app[name]:
                faults.append(f"{name}: accent token {key} is missing")
    for key in ACCENT_TOKENS:
        if key in app["dark"] and key in app["chosen"] and app["dark"][key] != app["chosen"][key]:
            faults.append(f"{key} differs between the two dark blocks")
    for theme, tokens in (("light", app["light"]), ("dark", {**app["light"], **app["chosen"]})):
        panel = parse_colour(tokens.get("--panel", ""))
        bg = parse_colour(tokens.get("--bg", ""))
        accent = parse_colour(tokens.get("--accent", ""), panel or (1, 1, 1))
        text = parse_colour(tokens.get("--accent-text", ""), accent or (1, 1, 1))
        pairs = [("--accent on --panel", accent, panel), ("--accent on --bg", accent, bg),
                 ("--accent-text on --accent", text, accent)]
        for label, fg, bgc in pairs:
            if fg is None or bgc is None:
                faults.append(f"{theme}: cannot read the colours for {label}")
                continue
            ratio = contrast(fg, bgc)
            (faults if ratio < 4.5 else notes).append(f"{theme}: {label} = {ratio:.2f}:1" + (" (below 4.5)" if ratio < 4.5 else ""))
        # The border of an input field must stand out from the field and from what is around it: 3:1 (WCAG 1.4.11).
        field = parse_colour(tokens.get("--field-line", ""), panel or (1, 1, 1))
        for under in ("--panel", "--panel-2", "--raised", "--sunken", "--bg"):  # every surface a field sits on
            bgc = parse_colour(tokens.get(under, ""))
            if field is None or bgc is None:
                faults.append(f"{theme}: cannot read the colours for --field-line on {under}")
                continue
            ratio = contrast(field, bgc)
            (faults if ratio < 3 else notes).append(f"{theme}: --field-line on {under} = {ratio:.2f}:1" + (" (below 3)" if ratio < 3 else ""))
    return shared, faults, notes


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    try:
        ref = blocks(css_text(REFERENCE))
    except (OSError, UnicodeDecodeError) as e:
        print(f"cannot read the house style {REFERENCE}: {e}")
        return 2
    worst = 0
    for arg in argv[1:]:
        path = Path(arg)
        try:
            shared, faults, notes = check(path, ref)
        except (OSError, UnicodeDecodeError) as e:
            print(f"{path}: cannot read it: {e}")
            worst = 2
            continue
        if faults:
            print(f"FAULT {path}: {len(faults)} problem(s)")
            for f in faults:
                print(f"  - {f}")
            worst = max(worst, 1)
        else:
            print(f"OK {path}: {shared} shared tokens match the house style")
        for n in notes:
            print(f"  {n}" if n.startswith("WARNING") else f"  contrast {n}")
    return worst


if __name__ == "__main__":
    sys.exit(main(sys.argv))
