"""Tests for check_house_style.py. Run: python -I -X utf8 test_check_house_style.py  (prints "all N tests passed").

Each case builds a page from references/house-style.css plus GlyphGarage's teal accent, changes one thing, and
checks the exit code: 0 = follows the house style, 1 = fault found, 2 = cannot read.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECK = HERE / "check_house_style.py"
CSS = (HERE.parent / "references" / "house-style.css").read_text(encoding="utf-8")
LIGHT = "--accent: #0f766e; --accent-2: #115e59; --accent-soft: rgba(15, 118, 110, .09); --accent-text: #ffffff; --accent-ring: rgba(15, 118, 110, .3);"
DARK = "--accent: #2dd4bf; --accent-2: #14b8a6; --accent-soft: rgba(45, 212, 191, .12); --accent-text: #04201d; --accent-ring: rgba(45, 212, 191, .35);"


def page(css=CSS, light=LIGHT, dark=DARK, chosen=DARK, media=True):
    auto = f':root:not([data-theme="light"]) {{ {dark} }}'
    auto = f"@media (prefers-color-scheme: dark) {{ {auto} }}" if media else auto
    return f'<style>{css}\n:root {{ {light} }}\n{auto}\n:root[data-theme="dark"] {{ {chosen} }}</style>'


CASES = [
    ("teal page follows the house style", page(), 0),
    ("3-digit hex, 0.09 and .090 are the same", page(css=CSS.replace("--panel: #ffffff;", "--panel: #FFF;")
                                                     .replace("rgba(16, 24, 40, .09)", "rgba(16, 24, 40, 0.090)")), 0),
    ("last value without a semicolon", page(css=CSS.replace("--data: #6b7789;\n}\n}", "--data: #6b7789\n}\n}")), 0),
    ("white and the space form of rgb()", page(light=LIGHT.replace("#ffffff", "white").replace("rgba(15, 118, 110, .3)", "rgb(15 118 110 / 30%)")), 0),
    ("changed shared token", page(css=CSS.replace("--bg: #f5f6f8;", "--bg: #f5f6f9;")), 1),
    ("missing shared token", page(css=CSS.replace("  --radius: 14px;\n", "")), 1),
    ("missing accent token in a dark block", page(chosen=DARK.replace("--accent-ring: rgba(45, 212, 191, .35);", "")), 1),
    ("accent differs between the dark blocks", page(chosen=DARK.replace("#2dd4bf", "#5eead4")), 1),
    ("accent with low contrast", page(light=LIGHT.replace("#0f766e", "#5eead4")), 1),
    ("dark block outside its @media", page(css=CSS.replace("@media (prefers-color-scheme: dark) {", "/* no media */", 1)
                                           .replace("--data: #6b7789;\n}\n}", "--data: #6b7789;\n}"), media=False), 1),
]


def run(path):
    return subprocess.run([sys.executable, "-I", "-X", "utf8", str(CHECK), str(path)],
                          capture_output=True, text=True, encoding="utf-8").returncode


def main():
    failed = 0
    with tempfile.TemporaryDirectory() as tmp:
        for i, (name, html, want) in enumerate(CASES):
            path = Path(tmp) / f"case{i}.html"
            path.write_text(html, encoding="utf-8")
            got = run(path)
            if got != want:
                failed += 1
                print(f"FAIL {name}: exit {got}, expected {want}")
        bad = Path(tmp) / "not-utf8.html"
        bad.write_bytes(b"<style>\xff\xfe:root{}</style>")
        if run(bad) != 2:
            failed += 1
            print("FAIL a file that is not UTF-8 must give exit 2")
        if run(Path(tmp) / "missing.html") != 2:
            failed += 1
            print("FAIL a missing file must give exit 2")
    total = len(CASES) + 2
    print(f"{total - failed} of {total} tests passed" if failed else f"all {total} tests passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
