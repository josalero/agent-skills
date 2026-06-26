from __future__ import annotations

import shutil
from pathlib import Path

from .models import Skill

RESOURCE_DIRS = ("references", "scripts", "assets")


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def reset_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def write_text_if_changed(path: Path, content: str) -> bool:
    ensure_dir(path.parent)
    normalized = content.replace("\r\n", "\n")
    if not normalized.endswith("\n"):
        normalized += "\n"
    if path.exists() and path.read_text(encoding="utf-8") == normalized:
        return False
    path.write_text(normalized, encoding="utf-8", newline="\n")
    return True


def copy_optional_resources(source: Path, destination: Path) -> None:
    for name in RESOURCE_DIRS:
        source_dir = source / name
        if not source_dir.exists():
            continue
        dest_dir = destination / name
        if dest_dir.exists():
            shutil.rmtree(dest_dir)
        shutil.copytree(source_dir, dest_dir)


def copy_skill_bundle(skill: Skill, destination: Path) -> list[Path]:
    ensure_dir(destination)
    changed: list[Path] = []
    skill_md = destination / "SKILL.md"
    shutil.copy2(skill.path / "SKILL.md", skill_md)
    changed.append(skill_md)
    copy_optional_resources(skill.path, destination)
    for resource_dir in RESOURCE_DIRS:
        resource_path = destination / resource_dir
        if resource_path.exists():
            changed.append(resource_path)
    return changed
