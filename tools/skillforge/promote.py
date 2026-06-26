from __future__ import annotations

from pathlib import Path
from typing import Any

from .backlog_gen import dump_backlog, load_waves
from .filesystem import ensure_dir, write_text_if_changed
from .modes import resolve_modes
from .parse import parse_yaml_file
from .paths import backlog_path, collections_dir, packs_dir, skill_eval_prompt_path


DRAFT_SKILL_MD = """---
name: {skill_id}
description: {description}
---

# {display_name}

## Workflow

TODO: Replace this generated draft with a concrete workflow.

1. Inspect the repository, toolchain, tests, and existing conventions for this domain.
2. Identify the requested task type and the smallest safe change.
3. Apply guidance using local patterns before introducing new abstractions.
4. Verify with focused tests or commands.

## References

TODO: Add `references/*.md` files when detailed guidance or code samples are needed.

## Output

TODO: Define the summary format the agent should produce after completing the task.
"""

DRAFT_EVAL_PROMPT = """# {display_name} — eval prompt

## User prompt

TODO: Add a realistic user request that should trigger this skill.

## Expected behavior

TODO: Describe what the agent should do when this skill applies.
"""


def _dump_mapping(data: dict[str, Any]) -> str:
    lines: list[str] = []
    for key, value in data.items():
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - {item}")
        elif isinstance(value, dict):
            lines.append(f"{key}:")
            for sub_key, sub_value in value.items():
                lines.append(f"  {sub_key}: {sub_value}")
        else:
            lines.append(f"{key}: {value}")
    return "\n".join(lines) + "\n"


def render_draft_skill_yaml(entry: dict[str, Any]) -> str:
    tags = [str(entry["domain"])] + [
        str(part)
        for part in str(entry["id"]).split("-")
        if part not in {str(entry["domain"]), "any", "version"}
    ][:3]
    payload: dict[str, Any] = {
        "id": entry["id"],
        "display_name": entry["display_name"],
        "domain": entry["domain"],
        "kind": entry["kind"],
        "modes": resolve_modes(str(entry["id"])),
        "status": "draft",
        "summary": entry.get("rationale") or entry["display_name"],
        "areas": entry.get("areas") or ["code-quality"],
        "tags": tags,
        "collections": entry.get("collections") or [entry["domain"]],
        "packs": entry.get("packs") or [],
        "targets": {"codex": True, "cursor": True, "copilot": True},
        "owners": ["josalero"],
        "stability": "experimental",
    }
    return _dump_mapping(payload)


def promote_backlog_entry(root: Path, entry: dict[str, Any]) -> Path:
    skill_id = str(entry["id"])
    skill_dir = root / "skills" / skill_id
    if skill_dir.exists():
        return skill_dir

    ensure_dir(skill_dir)
    description = str(entry.get("rationale") or entry.get("display_name") or skill_id)
    skill_md = DRAFT_SKILL_MD.format(
        skill_id=skill_id,
        display_name=entry["display_name"],
        description=description,
    )
    write_text_if_changed(skill_dir / "SKILL.md", skill_md)
    write_text_if_changed(skill_dir / "skill.yaml", render_draft_skill_yaml(entry))
    ensure_dir(skill_dir / "eval")
    write_text_if_changed(
        skill_eval_prompt_path(root, skill_id),
        DRAFT_EVAL_PROMPT.format(display_name=entry["display_name"]),
    )
    _register_skill_in_collections(root, entry)
    _register_skill_in_packs(root, entry)
    return skill_dir


def _register_skill_in_collections(root: Path, entry: dict[str, Any]) -> None:
    skill_id = str(entry["id"])
    for collection_id in entry.get("collections") or [entry["domain"]]:
        path = collections_dir(root) / f"{collection_id}.yaml"
        if not path.exists():
            continue
        data = parse_yaml_file(path)
        if not isinstance(data, dict):
            continue
        skills = data.setdefault("skills", [])
        if skill_id not in skills:
            skills.append(skill_id)
            skills.sort()
            path.write_text(_dump_mapping(data), encoding="utf-8")


def _register_skill_in_packs(root: Path, entry: dict[str, Any]) -> None:
    skill_id = str(entry["id"])
    for pack_id in entry.get("packs") or []:
        path = packs_dir(root) / f"{pack_id}.yaml"
        if not path.exists():
            continue
        data = parse_yaml_file(path)
        if not isinstance(data, dict):
            continue
        skills = data.setdefault("skills", [])
        if skill_id not in skills:
            skills.append(skill_id)
            skills.sort()
            path.write_text(_dump_mapping(data), encoding="utf-8")


def _backlog_entries(root: Path) -> list[dict[str, Any]]:
    backlog_file = backlog_path(root)
    data = parse_yaml_file(backlog_file)
    if not isinstance(data, dict):
        return []
    skills = data.get("skills", [])
    return [item for item in skills if isinstance(item, dict)]


def _update_backlog_status(root: Path, skill_id: str, status: str) -> None:
    entries = _backlog_entries(root)
    if not entries:
        return
    for item in entries:
        if item.get("id") == skill_id:
            item["status"] = status
            break
    dump_backlog(backlog_path(root), entries)


def promote_skill(root: Path, skill_id: str) -> Path:
    entry = next((item for item in _backlog_entries(root) if item.get("id") == skill_id), None)
    if entry is None:
        raise ValueError(f"backlog skill not found: {skill_id}")
    skill_dir = promote_backlog_entry(root, entry)
    _update_backlog_status(root, skill_id, "draft")
    return skill_dir


def promote_wave(root: Path, wave_id: str) -> list[Path]:
    waves = load_waves(root).get("waves", [])
    wave = next((item for item in waves if isinstance(item, dict) and item.get("id") == wave_id), None)
    if wave is None:
        raise ValueError(f"wave not found: {wave_id}")
    promoted: list[Path] = []
    for skill_id in wave.get("skills", []):
        if (root / "skills" / skill_id).exists():
            continue
        try:
            promoted.append(promote_skill(root, str(skill_id)))
        except ValueError:
            continue
    return promoted


def promote_all_waves(root: Path) -> list[Path]:
    promoted: list[Path] = []
    for wave in load_waves(root).get("waves", []):
        if isinstance(wave, dict) and wave.get("id"):
            promoted.extend(promote_wave(root, str(wave["id"])))
    return promoted
