"""Runtime configuration flags shared across modules."""
import os


def _flag(name: str) -> bool:
    return os.environ.get(name, "").strip().lower() in ("1", "true", "yes", "on")


# Public, password-less demo instance: anyone can create projects, upload and
# comment without logging in. Intended for a throwaway instance that resets
# regularly. NEVER enable this on an instance with real client material.
DEMO_MODE = _flag("REAMARK_DEMO_MODE")

# Per-file upload cap (MB) enforced only in demo mode.
DEMO_MAX_UPLOAD_MB = int(os.environ.get("REAMARK_DEMO_MAX_UPLOAD_MB", "30"))

# Safety caps in demo mode to avoid filling the disk before the next reset.
DEMO_MAX_PROJECTS = int(os.environ.get("REAMARK_DEMO_MAX_PROJECTS", "100"))
