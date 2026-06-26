from __future__ import annotations

from pathlib import Path


REGISTRY_DIR = "registry"
PACKS_SUBDIR = "packs"
COLLECTIONS_SUBDIR = "collections"


def registry_dir(root: Path) -> Path:
    return root / REGISTRY_DIR


def packs_dir(root: Path) -> Path:
    return registry_dir(root) / PACKS_SUBDIR


def collections_dir(root: Path) -> Path:
    return registry_dir(root) / COLLECTIONS_SUBDIR


def taxonomy_path(root: Path) -> Path:
    return registry_dir(root) / "taxonomy.yaml"


def waves_path(root: Path) -> Path:
    return registry_dir(root) / "waves.yaml"


def backlog_path(root: Path) -> Path:
    return registry_dir(root) / "skill-backlog.yaml"


def skill_eval_prompt_path(root: Path, skill_id: str) -> Path:
    return root / "skills" / skill_id / "eval" / "prompt.md"


def legacy_eval_prompt_path(root: Path, skill_id: str) -> Path:
    return root / "evals" / "prompts" / f"{skill_id}.md"
