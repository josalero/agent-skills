from __future__ import annotations

import shutil
from dataclasses import dataclass, field
from pathlib import Path

from .catalog import load_repository
from .modes import skill_supports_modes
from .models import Repository

INSTALLABLE_STATUSES = {"active", "recommended"}


@dataclass
class InstallResult:
    pack_id: str
    target: str
    destination: Path
    installed: list[str] = field(default_factory=list)
    skipped_draft: list[str] = field(default_factory=list)
    skipped_missing: list[str] = field(default_factory=list)
    skipped_target: list[str] = field(default_factory=list)
    skipped_modes: list[str] = field(default_factory=list)


def resolve_pack_skill_ids(repo: Repository, pack_id: str) -> list[str]:
    pack = repo.packs.get(pack_id)
    if pack is None:
        known = ", ".join(sorted(repo.packs))
        raise ValueError(f"Unknown pack '{pack_id}'. Known packs: {known}")
    skills = pack.data.get("skills", [])
    if not isinstance(skills, list):
        return []
    return [str(skill_id) for skill_id in skills]


def _skill_is_installable(repo: Repository, skill_id: str, active_only: bool) -> bool:
    skill = repo.skills.get(skill_id)
    if skill is None:
        return False
    status = str(skill.metadata.get("status", "draft"))
    if active_only:
        return status in INSTALLABLE_STATUSES
    return status not in {"deprecated", "archived"}


def _dist_paths(root: Path, target: str, skill_id: str) -> tuple[Path, Path | None]:
    if target == "cursor":
        base = root / "dist" / "cursor" / ".cursor"
        return base / "skills" / skill_id, base / "rules" / f"{skill_id}.mdc"
    if target == "copilot":
        base = root / "dist" / "copilot" / ".github"
        return base / "skills" / skill_id, base / "instructions" / f"{skill_id}.instructions.md"
    if target == "codex":
        base = root / "dist" / "codex" / "skills"
        return base / skill_id, None
    if target == "claude":
        base = root / "dist" / "claude" / ".claude"
        return base / "skills" / skill_id, None
    raise ValueError(f"Unsupported target '{target}'. Use cursor, copilot, codex, or claude.")


def _dest_paths(dest_root: Path, target: str, skill_id: str) -> tuple[Path, Path | None]:
    dest_root = dest_root.resolve()
    if target == "cursor":
        base = dest_root / ".cursor"
        return base / "skills" / skill_id, base / "rules" / f"{skill_id}.mdc"
    if target == "copilot":
        base = dest_root / ".github"
        return base / "skills" / skill_id, base / "instructions" / f"{skill_id}.instructions.md"
    if target == "codex":
        return dest_root / "skills" / skill_id, None
    if target == "claude":
        base = dest_root / ".claude"
        return base / "skills" / skill_id, None
    raise ValueError(f"Unsupported target '{target}'. Use cursor, copilot, codex, or claude.")


def _copy_tree(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination)


def _copy_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def install_pack(
    root: Path,
    pack_id: str,
    target: str,
    dest: Path,
    *,
    active_only: bool = True,
    modes: set[str] | None = None,
) -> InstallResult:
    repo, _ = load_repository(root)
    skill_ids = resolve_pack_skill_ids(repo, pack_id)
    result = InstallResult(pack_id=pack_id, target=target, destination=dest.resolve())

    dist_root = root / "dist"
    if not dist_root.exists():
        raise ValueError("dist/ output not found. Run `skillctl build --target all` first.")

    for skill_id in skill_ids:
        skill = repo.skills.get(skill_id)
        if skill is None:
            result.skipped_missing.append(skill_id)
            continue

        if target not in skill.enabled_targets:
            result.skipped_target.append(skill_id)
            continue

        status = str(skill.metadata.get("status", "draft"))
        if active_only and status not in INSTALLABLE_STATUSES:
            result.skipped_draft.append(skill_id)
            continue
        if not active_only and status in {"deprecated", "archived"}:
            result.skipped_draft.append(skill_id)
            continue

        if modes and not skill_supports_modes(skill.metadata.get("modes"), modes):
            result.skipped_modes.append(skill_id)
            continue

        source_bundle, source_router = _dist_paths(root, target, skill_id)
        if not source_bundle.exists():
            result.skipped_missing.append(skill_id)
            continue

        dest_bundle, dest_router = _dest_paths(dest, target, skill_id)
        _copy_tree(source_bundle, dest_bundle)
        if source_router is not None and dest_router is not None:
            if source_router.exists():
                _copy_file(source_router, dest_router)
        result.installed.append(skill_id)

    return result
