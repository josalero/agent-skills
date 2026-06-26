from __future__ import annotations

import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"


def skillctl_argv(*args: str) -> list[str]:
    """Return subprocess argv for skillctl on the current OS."""
    if os.name == "nt":
        return ["cmd", "/c", str(TOOLS / "skillctl.cmd"), *args]
    return [str(TOOLS / "skillctl"), *args]


def run_skillctl(
    *args: str,
    cwd: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    """Run skillctl and return the completed process."""
    return subprocess.run(
        skillctl_argv(*args),
        cwd=cwd or ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
