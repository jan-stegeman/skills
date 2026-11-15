"""Public-ready check for one of the user's app repos (skill html-app-house-style, rule 11).

Run it in every test run, also while the repo is still private, so the repo can go public at any time without a
clean-up round. It prints "OK public ready ..." or one "FAIL ..." line per problem (exit code 1).

Checks:
  1. Every commit on a branch, tag, remote branch or HEAD (also a detached HEAD) has a no-reply author and committer
     e-mail, and the repo's own git e-mail (for the next commits) is a no-reply address too.
  2. No private text in the files in git: the working copy, the staged version (the next commit), every older
     version (history), the file names, the commit messages and the built page(s) (--built). It looks for words
     from the private list, keys and tokens, Windows user folders, home-network addresses and e-mail addresses that
     are not no-reply. UTF-8 and UTF-16 text is read; other files with zero bytes count as binary (not scanned).
     The private list is a text file on this PC only, never in git: one word or text per line, # for a comment.
     Place: --private-list, else $PUBLIC_READY_PRIVATE_LIST, else ~/.config/public-ready/private.txt.
  3. Work notes (PROGRESS.md, research/, design/) are ignored by git and never were in git.
  4. The public files are there (README with a "no warranty" line, LICENSE, SECURITY, CONTRIBUTING, ACCESSIBILITY,
     THIRD-PARTY-NOTICES, the pull request template and the issue form settings).
  5. GitHub workflows (when there are any): every action pinned to a full commit SHA (also in the repo's own
     .github/actions), a "permissions:" block for the whole workflow or for every job, "persist-credentials: false"
     in every checkout step, and Dependabot watching the actions.

Usage:
  python -I -X utf8 check_public_ready.py <repo> [--built FILE ...] [--allow REGEX ...] [--private-list FILE]
         [--notes PATH ...] [--require FILE ...]
--allow REGEX: a hit that matches it is accepted (for example a third-party e-mail that a license requires).
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

NOREPLY = re.compile(
    r"^(?:\d+\+)?[A-Za-z0-9-]+(?:\[bot\])?@users\.noreply\.github\.com$"
    r"|^noreply@(?:github|anthropic)\.com$",
    re.I,
)
# E-mail addresses that are fine in text: no-reply, example domains, the git host address.
OK_EMAIL = re.compile(r"@(?:example\.(?:com|org|net)|[\w-]+\.invalid)$|^git@github\.com$", re.I)

SECRETS = [
    ("GitHub token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})")),
    ("Hugging Face token", re.compile(r"\bhf_[A-Za-z0-9]{30,}")),
    ("API key (sk-)", re.compile(r"\bsk-(?:ant-|proj-)?[A-Za-z0-9_-]{20,}")),
    ("AWS key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}")),
    ("Slack token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}")),
    ("private key", re.compile(r"-----BEGIN (?:[A-Z]+ )?PRIVATE KEY-----")),
]
GENERIC = [
    # A real user name after C:\Users\ (not Public, Default, or an example name such as "you" or "<name>").
    ("Windows user folder", re.compile(
        r"\b[A-Za-z]:[\\/]+Users[\\/]+"
        r"(?!(?:Public|Default|All Users|you|yourname|your-name|username|user|name)(?=[\\/\s\"'<>|`]|$)|[<%$])"
        r"[^\\/\s\"'<>|`]+", re.I)),
    ("home folder", re.compile(r"(?<![\w.~])/(?:Users|home)/(?!runner\b)[A-Za-z0-9._-]+")),
    ("home-network address", re.compile(r"\b(?:10\.\d{1,3}|192\.168|172\.(?:1[6-9]|2\d|3[01]))\.\d{1,3}\.\d{1,3}\b")),
]
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}\b")

DEFAULT_NOTES = ["PROGRESS.md", "research/", "design/"]
DEFAULT_REQUIRED = [
    "README.md", "LICENSE", "SECURITY.md", "CONTRIBUTING.md", "ACCESSIBILITY.md", "THIRD-PARTY-NOTICES.md",
    ".github/pull_request_template.md", ".github/ISSUE_TEMPLATE/config.yml",
]
REFS = ["--branches", "--tags", "--remotes", "HEAD"]  # what can be pushed; HEAD also when it is detached
MAX_BYTES = 20 * 1024 * 1024  # bigger files are reported, not scanned


def git(repo: Path, *args: str, check: bool = True) -> str:
    out = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, check=False)
    if check and out.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {out.stderr.decode('utf-8', 'replace').strip()}")
    return out.stdout.decode("utf-8", "replace")


def has_commits(repo: Path) -> bool:
    return subprocess.run(["git", "-C", str(repo), "rev-parse", "-q", "--verify", "HEAD"], capture_output=True).returncode == 0


def mask(text: str) -> str:
    """Never print a private value in full: at most a third of it (4 characters at most), and the length."""
    keep = min(4, len(text) // 3)
    return f"{text[:keep]}... ({len(text)} chars)"


def load_private(path_arg: str | None) -> tuple[list[str], str]:
    path = Path(path_arg or os.environ.get("PUBLIC_READY_PRIVATE_LIST") or Path.home() / ".config/public-ready/private.txt")
    if not path.is_file():
        if path_arg:
            raise SystemExit(f"FAIL private list not found: {path}")
        return [], f"WARNING no private list at {path}: only the general checks ran"
    words = []
    for n, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        line = line.strip()
        if line and not line.startswith("#"):
            if len(line) < 4:
                raise SystemExit(f"FAIL private list {path} line {n}: shorter than 4 characters (too many false hits)")
            words.append(line)
    return words, f"private list: {len(words)} entries"


class Scanner:
    def __init__(self, private: list[str], allow: list[re.Pattern]):
        self.private = [re.compile(re.escape(w), re.I) for w in private]
        self.allow = allow
        self.problems: set[str] = set()

    def allowed(self, hit: str) -> bool:
        return any(a.search(hit) for a in self.allow)

    def scan(self, where: str, text: str, lines: bool = True) -> None:
        def report(kind: str, m: re.Match) -> None:
            hit = m.group(0)
            if self.allowed(hit):
                return
            at = f"{where}:{text.count(chr(10), 0, m.start()) + 1}" if lines else where
            self.problems.add(f"FAIL {kind} in {at}: {mask(hit)}")

        for rx in self.private:
            for m in rx.finditer(text):
                report("private text", m)
        for kind, rx in SECRETS + GENERIC:
            for m in rx.finditer(text):
                report(kind, m)
        for m in EMAIL.finditer(text):
            if not (NOREPLY.search(m.group(0)) or OK_EMAIL.search(m.group(0))):
                report("e-mail address", m)


def decode(data: bytes) -> str | None:
    """UTF-8 or UTF-16 text (Windows PowerShell 5.1 writes UTF-16); None for a binary file (picture, PDF)."""
    if data[:2] in (b"\xff\xfe", b"\xfe\xff"):
        return data.decode("utf-16", "replace")
    head = data[:8192]
    if b"\0" not in head:
        return data.decode("utf-8", "replace")
    # UTF-16 without a byte order mark: nearly every second byte is zero.
    pairs = len(head) // 2
    if pairs:
        odd = head[1::2].count(0) / pairs
        even = head[0::2].count(0) / pairs
        if odd > 0.6 and even < 0.1:
            return data.decode("utf-16-le", "replace")
        if even > 0.6 and odd < 0.1:
            return data.decode("utf-16-be", "replace")
    return None


def scan_blobs(repo: Path, blobs: dict[str, str], sc: Scanner) -> int:
    """Read each blob (sha -> label) with one git cat-file process and scan it."""
    if not blobs:
        return 0
    proc = subprocess.Popen(["git", "-C", str(repo), "cat-file", "--batch"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    n = 0
    try:
        for sha, label in blobs.items():
            proc.stdin.write(sha.encode() + b"\n")
            proc.stdin.flush()
            head = proc.stdout.readline().split()
            if len(head) < 3:  # "<sha> missing"
                continue
            size = int(head[2])
            data = proc.stdout.read(size)
            proc.stdout.read(1)  # the newline after the content
            if head[1] != b"blob":
                continue
            if size > MAX_BYTES:
                sc.problems.add(f"FAIL {label} is bigger than {MAX_BYTES // 1048576} MB: check it by hand")
                continue
            text = decode(data)
            if text is not None:
                sc.scan(label, text)
                n += 1
    finally:
        proc.stdin.close()
        proc.wait()
    return n


def code_lines(text: str) -> list[str]:
    """YAML lines without their comments (a # at the start or after a space)."""
    return [re.sub(r"(^|\s)#.*$", "", line).rstrip() for line in text.splitlines()]


def indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def blocks(lines: list[str], start: int) -> list[list[str]]:
    """The children of the block that starts after line `start` (each child: its own line plus deeper lines)."""
    out: list[list[str]] = []
    child = None
    for line in lines[start + 1:]:
        if not line.strip():
            continue
        n = indent(line)
        if n <= indent(lines[start]):
            break
        if child is None:
            child = n
        if n == child:
            out.append([line])
        elif n > child and out:
            out[-1].append(line)
        else:
            break
    return out


def uses_refs(lines: list[str]) -> list[str]:
    """Every 'uses:' value, also in flow style such as '- {uses: owner/action@ref}'."""
    return re.findall(r"(?:^|[\s{,-])uses:\s*['\"]?([^\s'\"#,}]+)", "\n".join(lines), re.M)


def check_workflow(p: str, text: str, problems: set[str]) -> None:
    lines = code_lines(text)
    top_perm = any(re.match(r"permissions:", l) for l in lines)
    jobs_at = next((i for i, l in enumerate(lines) if re.match(r"jobs:\s*$", l)), None)
    jobs = blocks(lines, jobs_at) if jobs_at is not None else []
    if not top_perm:
        if not jobs:
            problems.add(f"FAIL {p}: no 'permissions:' block (the token gets too many rights)")
        for job in jobs:
            name = job[0].strip().rstrip(":")
            child = min((indent(l) for l in job[1:]), default=0)
            if not any(indent(l) == child and re.match(r"\s*permissions:", l) for l in job[1:]):
                problems.add(f"FAIL {p}: job '{name}' has no 'permissions:' block and the workflow has none")
    # Steps: a line '- ...' and its deeper lines. Each checkout step needs persist-credentials: false.
    for i, line in enumerate(lines):
        if not re.match(r"\s*-\s", line):
            continue
        step = [line]
        for nxt in lines[i + 1:]:
            if nxt.strip() and indent(nxt) <= indent(line):
                break
            step.append(nxt)
        body = "\n".join(step)
        if re.search(r"uses:\s*['\"]?actions/checkout@", body) and not re.search(r"persist-credentials:\s*['\"]?false", body):
            problems.add(f"FAIL {p}:{i + 1}: a checkout without 'persist-credentials: false'")


def main() -> int:
    ap = argparse.ArgumentParser(description="Check that a repo is ready to go public.")
    ap.add_argument("repo")
    ap.add_argument("--built", nargs="*", default=[], help="built files to scan too (the page in dist)")
    ap.add_argument("--allow", nargs="*", default=[], help="regex: hits that match it are accepted")
    ap.add_argument("--private-list")
    ap.add_argument("--notes", nargs="*", default=DEFAULT_NOTES)
    ap.add_argument("--require", nargs="*", default=[], help="extra files that must be in git")
    a = ap.parse_args()
    repo = Path(a.repo).resolve()
    try:
        git(repo, "rev-parse", "--git-dir")
    except RuntimeError:
        print(f"FAIL not a git repo: {repo}")
        return 1

    private, private_note = load_private(a.private_list)
    sc = Scanner(private, [re.compile(x) for x in a.allow])
    problems = sc.problems
    refs = REFS if has_commits(repo) else ["--branches", "--tags", "--remotes"]

    # 1. E-mail addresses in the commits, and the one for the next commits.
    log = git(repo, "log", *refs, "--format=%h%x00%ae%x00%ce").splitlines()
    for row in log:
        h, ae, ce = row.split("\0")
        for who, mail in (("author", ae), ("committer", ce)):
            if not NOREPLY.search(mail):
                problems.add(f"FAIL commit {h}: {who} e-mail is not a no-reply address: {mask(mail)}")
    next_mail = git(repo, "config", "user.email", check=False).strip()
    if not NOREPLY.search(next_mail):
        problems.add(f"FAIL git e-mail for the next commits is not a no-reply address: "
                     f"{mask(next_mail) if next_mail else '(empty)'}"
                     " - set it with: git config user.email <id>+<name>@users.noreply.github.com")

    # 2. Private text: working copy, staged version and file names of the files in git ...
    tracked = [p for p in git(repo, "ls-files", "-z").split("\0") if p]
    for p in tracked:
        sc.scan("file name", p, lines=False)
        f = repo / p
        if not f.is_file():
            continue
        if f.stat().st_size > MAX_BYTES:
            problems.add(f"FAIL {p} is bigger than {MAX_BYTES // 1048576} MB: check it by hand")
            continue
        text = decode(f.read_bytes())
        if text is not None:
            sc.scan(p, text)
    blobs: dict[str, str] = {}
    for row in git(repo, "ls-files", "-s", "-z").split("\0"):
        meta, _, path = row.partition("\t")
        if path:
            blobs[meta.split()[1]] = f"{path} (staged)"
    # ... every older version and its file name, the commit messages, the built pages.
    ever: set[str] = set()
    if log:
        for line in git(repo, "rev-list", "--objects", *refs).splitlines():
            sha, _, path = line.partition(" ")
            if path:
                blobs.setdefault(sha, f"{path} (history {sha[:7]})")
                ever.add(path)
        for m in git(repo, "log", *refs, "--format=%h%x00%B%x1e").split("\x1e"):
            if "\0" in m:
                h, body = m.strip("\n").split("\0", 1)
                sc.scan(f"commit message {h}", body)
    for path in ever:
        sc.scan("file name (history)", path, lines=False)
    versions = scan_blobs(repo, blobs, sc)
    for b in a.built:
        f = Path(b)
        if not f.is_file():
            problems.add(f"FAIL built file not found: {b}")
            continue
        text = decode(f.read_bytes())
        if text is not None:
            sc.scan(f.name, text)

    # 3. Work notes stay on the PC.
    for note in a.notes:
        is_dir = note.endswith("/")
        probe = note + "probe.txt" if is_dir else note
        if subprocess.run(["git", "-C", str(repo), "check-ignore", "-q", "--no-index", probe]).returncode != 0:
            problems.add(f"FAIL work notes '{note}' are not in .gitignore")
        match = (lambda p: p.startswith(note)) if is_dir else (lambda p: p == note)
        now = [p for p in tracked if match(p)]
        if now:
            problems.add(f"FAIL work notes in git now: {', '.join(now[:3])}")
        old = sorted(p for p in ever if match(p) and p not in now)
        if old:
            problems.add(f"FAIL work notes in the git history: {', '.join(old[:3])} (needs a history rewrite)")

    # 4. Public files.
    for req in DEFAULT_REQUIRED + a.require:
        if req not in tracked:
            problems.add(f"FAIL public file missing (not in git): {req}")
    readme = repo / "README.md"
    if readme.is_file() and not re.search(r"\bno warranty\b", readme.read_text(encoding="utf-8", errors="replace"), re.I):
        problems.add("FAIL README.md has no 'No warranty' line")

    # 5. GitHub workflows and the repo's own actions (.github/actions/*/action.yml).
    wfs = [p for p in tracked if re.match(r"\.github/workflows/[^/]+\.ya?ml$", p)]
    own_actions = [p for p in tracked if re.match(r"\.github/actions/.+/action\.ya?ml$", p)]
    for p in wfs + own_actions:
        text = (repo / p).read_text(encoding="utf-8", errors="replace")
        for ref in uses_refs(code_lines(text)):
            if ref.startswith(("./", "docker://")):
                continue
            if not re.search(r"@[0-9a-f]{40}$", ref):
                problems.add(f"FAIL {p}: '{ref}' is not pinned to a full commit SHA")
        if p in wfs:
            check_workflow(p, text, problems)
    if wfs:
        dep = repo / ".github/dependabot.yml"
        if ".github/dependabot.yml" not in tracked or "github-actions" not in dep.read_text(encoding="utf-8", errors="replace"):
            problems.add("FAIL .github/dependabot.yml does not watch 'github-actions' (needed when there are workflows)")

    print(private_note)
    for line in sorted(problems):
        print(line)
    if problems:
        print(f"FAIL public ready: {len(problems)} problem(s)")
        return 1
    print(f"OK public ready ({len(tracked)} files, {versions} file versions, {len(log)} commits, "
          f"{len(a.built)} built file(s), {len(wfs)} workflow(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
