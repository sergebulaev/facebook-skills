#!/usr/bin/env python3
"""Text I/O must state its encoding, so the bundle behaves the same on Windows.

Python's default text encoding is the locale's. On Linux and macOS that is
UTF-8, so a `read_text()` without `encoding=` works and nobody notices. On
Windows it is the ANSI code page, cp1252 on most installs: the same call
misreads the em dashes and curly quotes this bundle's markdown is full of, or
fails outright on a byte cp1252 does not define.

This check is static, so a Linux CI run catches a new unencoded call before a
Windows user does. Ported from the linkedin bundle, where the problem was
reported against a real Windows 11 install.

Run from the repo root:

    python3 scripts/check_text_encoding.py
"""
import ast
import os
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

#: Dot-directories (.git, the generated package), scratch and virtualenvs are
#: not this repo's source.
SKIP_DIRS = {"venv", "testing", "marketing", "node_modules"}
MODE_CHARS = set("rwxabt+")


def sources() -> list[pathlib.Path]:
    found = []
    for folder, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in SKIP_DIRS]
        found += [pathlib.Path(folder, name) for name in files if name.endswith(".py")]
    return sorted(found)


def unencoded_text_io(tree: ast.AST):
    """(line, call) for each text-mode open / read_text / write_text with no `encoding=`."""
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or any(k.arg == "encoding" for k in node.keywords):
            continue
        func = node.func
        name = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", None)
        if name in ("read_text", "write_text"):
            yield node.lineno, name
        elif name == "open":
            # open(path, mode) for the builtin, path.open(mode) for pathlib. An
            # attribute call whose first argument is not a mode (webbrowser.open,
            # Image.open) is something else and is left alone.
            builtin = isinstance(func, ast.Name)
            args = node.args[1:] if builtin else node.args
            mode = args[0] if args else next(
                (k.value for k in node.keywords if k.arg == "mode"), None)
            if mode is None:
                if builtin:
                    yield node.lineno, "open"
            elif isinstance(mode, ast.Constant) and isinstance(mode.value, str) \
                    and set(mode.value) <= MODE_CHARS and "b" not in mode.value:
                yield node.lineno, "open"


def main() -> int:
    problems = []
    scanned = 0
    for path in sources():
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except (SyntaxError, UnicodeDecodeError) as exc:
            problems.append(f"{path.relative_to(ROOT)}: will not parse: {exc}")
            continue
        scanned += 1
        for line, call in unencoded_text_io(tree):
            problems.append(
                f"{path.relative_to(ROOT)}:{line}: {call}() without `encoding=`. "
                f"Pass encoding=\"utf-8\"; the locale default is cp1252 on Windows.")

    if problems:
        print("Text I/O without an encoding:\n" + "\n".join("  " + p for p in problems))
        return 1

    print(f"OK: {scanned} Python files, every text-mode read and write names its encoding.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
