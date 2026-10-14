"""Internal helper to load .env when python-dotenv is available."""
from __future__ import annotations

import os
from pathlib import Path

_ENV_LOADED = False
#: The only variables a project .env may set. Anything the bundle *executes*
#: or routes traffic through has to come from the launch environment: a .env
#: that arrives with a clone, or that lands in a parent directory, is not a
#: trusted source for the name of a command to run.
_DOTENV_VARIABLES = (
    "APIFY_TOKEN", "PUBLORA_API_KEY", "FACEBOOK_PLATFORM_ID", "PIXFARO_TOKEN", "PIXFARO_API_KEY",
)


def env_candidates() -> list[Path]:
    """Where `load_env` looks, in order: upward from the cwd, then the repo root
    (this file's parent's parent)."""
    out: list[Path] = []
    try:
        from dotenv import find_dotenv

        found = find_dotenv(usecwd=True)
        if found:
            out.append(Path(found))
    except ImportError:
        cur = Path.cwd()
        for d in [cur, *cur.parents]:
            if (d / ".env").is_file():
                out.append(d / ".env")
                break
    root = Path(__file__).resolve().parents[1] / ".env"
    if root not in out:
        out.append(root)
    return out


def load_env(force: bool = False) -> None:
    """Load environment variables from .env if python-dotenv is installed.

    Safe no-op if python-dotenv is missing, preserving Tier 0 (manual)
    zero-dependency operation. Searches upwards from the current working
    directory and checks the repository root. Only bundle API credentials and
    the platform id are loaded. Executables and transport settings must come
    from the launch environment. Existing environment variables are preserved.
    """
    global _ENV_LOADED
    if _ENV_LOADED and not force:
        return

    try:
        from dotenv import dotenv_values

        for path in env_candidates():
            if not path.is_file():
                continue
            values = dotenv_values(path)
            for name in _DOTENV_VARIABLES:
                value = values.get(name)
                if value is not None:
                    os.environ.setdefault(name, value)
    except ImportError:
        pass

    _ENV_LOADED = True
