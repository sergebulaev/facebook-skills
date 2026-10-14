#!/usr/bin/env python3
"""Three trust boundaries this bundle is not allowed to reopen.

Reported against the linkedin bundle (sergebulaev/linkedin-skills#68) and
present here in the same shape, because these clients share an ancestor.

1. **A project .env may not name an executable.** load_env() once copied every
   variable it found into the environment, and the DIY tier reads
   FB_SKILLS_CUSTOM_POSTER from there and runs it through subprocess. A .env
   that arrives with a clone, or lands in a parent directory, was therefore a
   command this bundle would execute. Only credentials load now.
2. **No module may load a .env behind load_env's back.** A direct load_dotenv()
   call reopens boundary 1 for whatever imports it.
3. **Authenticated requests may not follow redirects.** The Publora key rides a
   custom header and the Apify token rides a query parameter; requests strips
   Authorization across hosts but not either of those, so a redirect hands the
   credential, and on POST the body, to whoever answered.

Run from the repo root:

    python3 scripts/check_security_boundaries.py
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ENV = ROOT / "lib" / "_env.py"
POSTER = "FB_SKILLS_CUSTOM_POSTER"
CLIENTS = ("publora_client.py", "apify_client.py", "youtube_client.py", "pixfaro_client.py")
DOTENV_CALL = re.compile(r"load_dotenv\s*\(")
CALL = re.compile(r"((?:self\._session|requests)\.(?:get|post|put|delete)\()")


def call_bodies(source: str):
    """(offset, body) for every HTTP call, parens matched so multi-line is fine."""
    for match in CALL.finditer(source):
        depth, i = 1, match.end()
        while depth and i < len(source):
            if source[i] == "(":
                depth += 1
            elif source[i] == ")":
                depth -= 1
            i += 1
        yield match.start(), source[match.end():i - 1]


def main() -> int:
    problems = []

    env = ENV.read_text(encoding="utf-8")
    if "_DOTENV_VARIABLES" not in env:
        problems.append(
            "lib/_env.py has no _DOTENV_VARIABLES allowlist, so a project .env can set "
            "anything, including the command the DIY tier executes.")
    if DOTENV_CALL.search(env):
        problems.append(
            "lib/_env.py calls load_dotenv(), which loads every variable in the file. "
            "Read the allowlisted names with dotenv_values() instead.")
    if POSTER in env:
        problems.append(
            f"lib/_env.py names {POSTER}. The variable the bundle executes must come "
            f"from the launch environment, never from a file on disk.")

    for path in sorted((ROOT / "scripts").glob("*.py")) + sorted((ROOT / "lib").glob("*.py")):
        if path.name in ("_env.py", pathlib.Path(__file__).name):
            continue
        if DOTENV_CALL.search(path.read_text(encoding="utf-8")):
            problems.append(
                f"{path.relative_to(ROOT)} calls load_dotenv() directly, which bypasses the "
                f"allowlist in lib/_env.py. Import from lib instead.")

    for name in CLIENTS:
        path = ROOT / "lib" / name
        if not path.is_file():
            continue
        source = path.read_text(encoding="utf-8")
        for offset, body in call_bodies(source):
            if "allow_redirects" not in body:
                line = source[:offset].count("\n") + 1
                problems.append(
                    f"lib/{name}:{line}: an authenticated request without "
                    f"allow_redirects=False. A redirect would forward the credential.")

    if problems:
        print("Security boundaries:\n" + "\n".join("  " + p for p in problems))
        return 1

    print("OK: .env cannot name an executable, nothing loads it behind load_env, and no "
          "authenticated request follows redirects.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
