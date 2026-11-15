"""Tests for check_public_ready.py. Run: python -I -X utf8 test_check_public_ready.py (prints "all N tests passed").

Each test makes a small git repo in a temporary folder. The repos get a fake remote (example.invalid), so the
user's global commit hook treats them as someone else's repo. Fake keys are built at run time, so this file itself
holds no string that looks like a real key.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECK = HERE / "check_public_ready.py"
OK_MAIL = "123+someone@users.noreply.github.com"
BAD_MAIL = "someone" + "@" + "mail-provider.test"
FAKE_GH = "gh" + "p_" + "A1b2C3d4" * 5
GOOD_SHA = "0123456789abcdef0123456789abcdef01234567"
PUBLIC = {
    "README.md": "# App\n\n- **No warranty.** Use it at your own risk.\n",
    "LICENSE": "MIT License\n",
    "SECURITY.md": "# Security\n",
    "CONTRIBUTING.md": "# Contributing\n",
    "ACCESSIBILITY.md": "# Accessibility\n",
    "THIRD-PARTY-NOTICES.md": "# Notices\n",
    ".github/pull_request_template.md": "## What changes\n",
    ".github/ISSUE_TEMPLATE/config.yml": "blank_issues_enabled: false\n",
    ".gitignore": "/PROGRESS.md\n/research/\n/design/\n/dist/\n",
}


def run(cwd: Path, *args: str) -> None:
    subprocess.run(args, cwd=cwd, check=True, capture_output=True)


def write(repo: Path, files: dict[str, str]) -> None:
    for name, text in files.items():
        f = repo / name
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(text, encoding="utf-8", newline="\n")


def commit(repo: Path, msg: str = "test commit", mail: str = OK_MAIL, add: str | None = ".") -> None:
    if add:
        run(repo, "git", "add", "-f", add)
    run(repo, "git", "-c", "user.name=Tester", "-c", f"user.email={mail}", "-c", "commit.gpgsign=false",
        "commit", "-q", "-m", msg)


def new_repo(tmp: Path, name: str, files: dict[str, str] | None = None) -> Path:
    repo = tmp / name
    repo.mkdir()
    run(repo, "git", "init", "-q", "-b", "main")
    run(repo, "git", "remote", "add", "origin", "https://example.invalid/test.git")
    run(repo, "git", "config", "user.email", OK_MAIL)
    run(repo, "git", "config", "core.autocrlf", "false")
    write(repo, dict(PUBLIC) if files is None else files)
    commit(repo)
    return repo


def check(repo: Path, *extra: str, private: Path | None = None) -> tuple[int, str]:
    args = [sys.executable, "-I", "-X", "utf8", str(CHECK), str(repo)]
    if private:
        args += ["--private-list", str(private)]
    out = subprocess.run(args + list(extra), capture_output=True, text=True, encoding="utf-8")
    return out.returncode, out.stdout + out.stderr


def main() -> int:
    passed = 0
    failed: list[str] = []
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        plist = tmp / "private.txt"
        plist.write_text("# my private words\nSecretName Person\n", encoding="utf-8")

        def case(name: str, repo: Path, want_ok: bool, want_text: str = "", *extra: str, private: Path | None = plist) -> None:
            nonlocal passed
            code, out = check(repo, *extra, private=private)
            good = (code == 0) == want_ok and want_text in out
            if good:
                passed += 1
            else:
                failed.append(f"{name}: exit {code}, wanted text '{want_text}'\n{out}")

        clean = new_repo(tmp, "clean")
        case("clean repo is OK", clean, True, "OK public ready")

        r = new_repo(tmp, "author")
        write(r, {"a.txt": "x\n"})
        commit(r, mail=BAD_MAIL)
        case("personal author e-mail fails", r, False, "author e-mail is not a no-reply address")

        r = new_repo(tmp, "nextmail")
        run(r, "git", "config", "user.email", BAD_MAIL)
        case("personal e-mail for next commits fails", r, False, "git e-mail for the next commits")

        r = new_repo(tmp, "private-history")
        write(r, {"notes.txt": "made by SecretName Person\n"})
        commit(r)
        write(r, {"notes.txt": "made by someone\n"})
        commit(r)
        case("private word only in an old version fails", r, False, "(history")
        _, out = check(r, private=plist)
        if "SecretName Person" in out:
            failed.append("private word is printed in full")
        else:
            passed += 1

        r = new_repo(tmp, "token-msg")
        write(r, {"b.txt": "y\n"})
        commit(r, msg=f"add key {FAKE_GH}")
        case("token in a commit message fails", r, False, "GitHub token in commit message")

        r = new_repo(tmp, "userpath")
        write(r, {"run.ps1": 'python "C:\\Users\\SomeOne\\x.py"\n'})
        commit(r)
        case("Windows user folder fails", r, False, "Windows user folder in run.ps1:1")
        case("--allow accepts that hit", r, True, "OK public ready", "--allow", r"Users\\SomeOne")

        r = new_repo(tmp, "example-paths")
        write(r, {"help.js": 'const a = "C:\\\\Users\\\\you\\\\.lmstudio"; // C:\\Users\\<name>\\x, C:\\Users\\Public\\y\n'})
        commit(r)
        case("example user folders are OK", r, True, "OK public ready")

        r = new_repo(tmp, "own-action")
        write(r, {".github/actions/build/action.yml": "runs:\n  using: composite\n  steps:\n    - uses: actions/setup-node@v4\n"})
        commit(r)
        case("own action with an unpinned step fails", r, False, "action.yml: 'actions/setup-node@v4' is not pinned")

        r = new_repo(tmp, "lan")
        write(r, {"cfg.txt": "server 192.168.1.20\n"})
        commit(r)
        case("home-network address fails", r, False, "home-network address")

        r = new_repo(tmp, "notes")
        write(r, {"PROGRESS.md": "notes\n"})
        commit(r, add="PROGRESS.md")
        run(r, "git", "rm", "-q", "--cached", "PROGRESS.md")
        commit(r, add=None)
        case("work notes in the history fail", r, False, "work notes in the git history: PROGRESS.md")

        files = dict(PUBLIC)
        files[".gitignore"] = "/dist/\n"
        r = new_repo(tmp, "noignore", files)
        case("notes not in .gitignore fail", r, False, "work notes 'research/' are not in .gitignore")

        files = dict(PUBLIC)
        del files["SECURITY.md"]
        r = new_repo(tmp, "nosecurity", files)
        case("missing SECURITY.md fails", r, False, "public file missing (not in git): SECURITY.md")

        files = dict(PUBLIC)
        files["README.md"] = "# App\n"
        r = new_repo(tmp, "nowarranty", files)
        case("README without 'No warranty' fails", r, False, "README.md has no 'No warranty' line")

        r = new_repo(tmp, "wf-bad")
        write(r, {".github/workflows/ci.yml": "on: push\njobs:\n  a:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n"})
        commit(r)
        code, out = check(r, private=plist)
        want = ["not pinned to a full commit SHA", "no 'permissions:' block", "without 'persist-credentials: false'",
                "dependabot.yml does not watch"]
        if code == 1 and all(w in out for w in want):
            passed += 1
        else:
            failed.append(f"bad workflow: exit {code}\n{out}")

        r = new_repo(tmp, "wf-good")
        write(r, {
            ".github/workflows/ci.yml": "on: push\npermissions:\n  contents: read\njobs:\n  a:\n    runs-on: ubuntu-latest\n"
                                        f"    steps:\n      - uses: actions/checkout@{GOOD_SHA} # v4\n        with:\n"
                                        "          persist-credentials: false\n      - uses: ./.github/actions/build\n",
            ".github/dependabot.yml": "version: 2\nupdates:\n  - package-ecosystem: github-actions\n    directory: /\n",
        })
        commit(r)
        case("good workflow is OK", r, True, "1 workflow(s)")

        # Review 2026-11-15 (GPT-6.1): each case below slipped through the first version.
        r = new_repo(tmp, "staged")
        write(r, {"config.txt": "owner SecretName Person\n"})
        run(r, "git", "add", "config.txt")
        write(r, {"config.txt": "owner someone\n"})
        case("private word only in the staged version fails", r, False, "config.txt (staged")

        r = new_repo(tmp, "utf16")
        (r / "config.ps1").write_bytes("\ufeff# by SecretName Person\r\n".encode("utf-16-le"))
        commit(r)
        case("private word in a UTF-16 file fails", r, False, "private text in config.ps1:1")

        r = new_repo(tmp, "detached")
        run(r, "git", "checkout", "-q", "--detach")
        write(r, {"c.txt": "z\n"})
        commit(r, mail=BAD_MAIL)
        case("commit on a detached HEAD is checked", r, False, "author e-mail is not a no-reply address")

        r = new_repo(tmp, "filename")
        write(r, {"SecretName Person notes.txt": "harmless\n"})
        commit(r)
        case("private word in a file name fails", r, False, "private text in file name")

        r = new_repo(tmp, "wf-scope")
        write(r, {
            ".github/workflows/ci.yml": "on: push\njobs:\n  a:\n    permissions:\n      contents: read\n    runs-on: x\n"
                                        f"    steps:\n      - uses: actions/checkout@{GOOD_SHA}\n        with:\n"
                                        "          persist-credentials: false\n  b:\n    runs-on: x\n    steps:\n"
                                        f"      - uses: actions/checkout@{GOOD_SHA} # persist-credentials: false\n",
            ".github/dependabot.yml": "version: 2\nupdates:\n  - package-ecosystem: github-actions\n    directory: /\n",
        })
        commit(r)
        code, out = check(r, private=plist)
        if code == 1 and "job 'b' has no 'permissions:'" in out and "checkout without 'persist-credentials: false'" in out:
            passed += 1
        else:
            failed.append(f"workflow scope per job: exit {code}\n{out}")

        r = new_repo(tmp, "wf-flow")
        write(r, {
            ".github/workflows/ci.yml": "on: push\npermissions: {contents: read}\njobs:\n  a:\n    runs-on: x\n"
                                        "    steps:\n      - {uses: actions/setup-node@v4}\n",
            ".github/dependabot.yml": "version: 2\nupdates:\n  - package-ecosystem: github-actions\n    directory: /\n",
        })
        commit(r)
        case("flow-style step with an unpinned action fails", r, False, "'actions/setup-node@v4' is not pinned")

        four = tmp / "four.txt"
        four.write_text("QZXY\n", encoding="utf-8")
        r = new_repo(tmp, "fourchar")
        write(r, {"d.txt": "code QZXY here\n"})
        commit(r)
        code, out = check(r, private=four)
        if code == 1 and "QZXY" not in out:
            passed += 1
        else:
            failed.append(f"a 4-character private word is printed in full or not found: exit {code}\n{out}")

        built = tmp / "page.html"
        built.write_text(f"<p>mail {BAD_MAIL}</p>", encoding="utf-8")
        case("e-mail in the built page fails", clean, False, "e-mail address in page.html:1", "--built", str(built))
        built.write_text(f"<p>mail {OK_MAIL} or git@github.com</p>", encoding="utf-8")
        case("no-reply e-mail in the built page is OK", clean, True, "1 built file(s)", "--built", str(built))

        short = tmp / "short.txt"
        short.write_text("abc\n", encoding="utf-8")
        case("too short private word is refused", clean, False, "shorter than 4 characters", private=short)
        case("missing private list given by hand fails", clean, False, "private list not found", private=tmp / "nope.txt")

    if failed:
        print("\n\n".join(failed))
        print(f"FAILED {len(failed)} of {passed + len(failed)} tests")
        return 1
    print(f"all {passed} tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
