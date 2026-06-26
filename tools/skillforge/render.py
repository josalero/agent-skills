from __future__ import annotations

from pathlib import Path

from .adapters import codex, copilot, cursor
from .catalog import write_catalog
from .models import Repository


TARGET_BUILDERS = {
    "codex": codex.build,
    "cursor": cursor.build,
    "copilot": copilot.build,
}


def build_targets(repo: Repository, target: str) -> list[Path]:
    changed: list[Path] = []
    targets = list(TARGET_BUILDERS) if target == "all" else [target]
    for item in targets:
        if item not in TARGET_BUILDERS:
            raise ValueError(f"unsupported target: {item}")
        changed.extend(TARGET_BUILDERS[item](repo))
    changed.extend(write_catalog(repo))
    return changed

