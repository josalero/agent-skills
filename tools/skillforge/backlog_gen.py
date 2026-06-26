from __future__ import annotations

from pathlib import Path
from typing import Any

from .parse import ParseError, parse_yaml_file
from .paths import backlog_path, taxonomy_path, waves_path


DEFAULT_PROMOTION_CRITERIA = [
    "Has a distinct workflow in SKILL.md.",
    "Has at least one realistic eval prompt.",
    "Has references when code samples or version tables are needed.",
    "Validates and renders for Codex, Cursor, and Copilot.",
]


def load_taxonomy(root: Path) -> dict[str, Any]:
    path = taxonomy_path(root)
    data = parse_yaml_file(path)
    if not isinstance(data, dict):
        raise ParseError(f"{path}: expected mapping")
    return data


def load_waves(root: Path) -> dict[str, Any]:
    path = waves_path(root)
    data = parse_yaml_file(path)
    if not isinstance(data, dict):
        raise ParseError(f"{path}: expected mapping")
    return data


def _domain_map(taxonomy: dict[str, Any]) -> dict[str, dict[str, Any]]:
    domains = taxonomy.get("domains", [])
    return {str(item["id"]): item for item in domains if isinstance(item, dict) and item.get("id")}


def _promotion_criteria(taxonomy: dict[str, Any]) -> list[str]:
    defaults = taxonomy.get("promotion_criteria_defaults")
    if isinstance(defaults, list) and defaults:
        return [str(item) for item in defaults]
    return DEFAULT_PROMOTION_CRITERIA


def _entry_from_shape(domain: dict[str, Any], shape: dict[str, Any], taxonomy: dict[str, Any]) -> dict[str, Any]:
    domain_id = str(domain["id"])
    domain_title = str(domain.get("title") or domain_id.title())
    skill_id = f"{domain_id}-{shape['skill_suffix']}"
    display_name = f"{domain_title} {shape.get('display_suffix', shape['skill_suffix']).replace('-', ' ').title()}"
    if "display_suffix" in shape:
        display_name = f"{domain_title} {shape['display_suffix']}"

    areas = shape.get("areas") or domain.get("default_areas") or ["code-quality"]
    packs = shape.get("default_packs") or domain.get("default_packs") or []
    rationale_template = str(shape.get("rationale") or "Engineering workflow for {domain_title}.")
    rationale = rationale_template.format(domain_title=domain_title, domain=domain_id)

    return {
        "id": skill_id,
        "display_name": display_name,
        "domain": domain_id,
        "kind": shape.get("kind", "general"),
        "priority": shape.get("priority", "P2"),
        "status": "proposed",
        "areas": list(areas),
        "packs": list(packs),
        "collections": list(domain.get("collections") or []),
        "rationale": rationale,
        "promotion_criteria": _promotion_criteria(taxonomy),
    }


def _entry_from_explicit(item: dict[str, Any], taxonomy: dict[str, Any]) -> dict[str, Any]:
    domain_map = _domain_map(taxonomy)
    domain_id = str(item["domain"])
    domain = domain_map.get(domain_id, {})
    entry = {
        "id": str(item["id"]),
        "display_name": str(item["display_name"]),
        "domain": domain_id,
        "kind": str(item.get("kind", "general")),
        "priority": str(item.get("priority", "P2")),
        "status": str(item.get("status", "proposed")),
        "areas": list(item.get("areas") or domain.get("default_areas") or ["code-quality"]),
        "packs": list(item.get("packs") or domain.get("default_packs") or []),
        "collections": list(item.get("collections") or domain.get("collections") or []),
        "rationale": str(item.get("rationale") or ""),
        "promotion_criteria": list(item.get("promotion_criteria") or _promotion_criteria(taxonomy)),
    }
    return entry


def generate_backlog_entries(taxonomy: dict[str, Any]) -> list[dict[str, Any]]:
    domain_map = _domain_map(taxonomy)
    entries: dict[str, dict[str, Any]] = {}

    for shape in taxonomy.get("capability_shapes", []):
        if not isinstance(shape, dict):
            continue
        for domain_id in shape.get("applies_to", []):
            domain = domain_map.get(str(domain_id))
            if domain is None:
                continue
            entry = _entry_from_shape(domain, shape, taxonomy)
            entries[entry["id"]] = entry

    for item in taxonomy.get("explicit_skills", []):
        if isinstance(item, dict) and item.get("id"):
            entry = _entry_from_explicit(item, taxonomy)
            entries[entry["id"]] = entry

    return [entries[key] for key in sorted(entries)]


def load_skill_folder_statuses(root: Path) -> dict[str, str]:
    statuses: dict[str, str] = {}
    for path in (root / "skills").glob("*"):
        if not path.is_dir():
            continue
        yaml_path = path / "skill.yaml"
        if not yaml_path.exists():
            continue
        data = parse_yaml_file(yaml_path)
        if isinstance(data, dict) and data.get("status"):
            statuses[path.name] = str(data["status"])
    return statuses


def merge_backlog_entries(
    generated: list[dict[str, Any]],
    existing: list[dict[str, Any]],
    skill_statuses: dict[str, str],
) -> list[dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {entry["id"]: entry for entry in generated}
    for item in existing:
        if not isinstance(item, dict) or not item.get("id"):
            continue
        skill_id = str(item["id"])
        current = merged.get(skill_id, {})
        preserved = {**current, **item}
        merged[skill_id] = preserved
    for skill_id, folder_status in skill_statuses.items():
        if skill_id in merged:
            merged[skill_id]["status"] = folder_status
    return [merged[key] for key in sorted(merged)]


def dump_backlog(path: Path, entries: list[dict[str, Any]]) -> None:
    lines = ["version: 1", "skills:"]
    for entry in entries:
        lines.append(f"  - id: {entry['id']}")
        lines.append(f"    display_name: {entry['display_name']}")
        lines.append(f"    domain: {entry['domain']}")
        lines.append(f"    kind: {entry['kind']}")
        lines.append(f"    priority: {entry['priority']}")
        lines.append(f"    status: {entry['status']}")
        lines.append("    areas:")
        for area in entry.get("areas", []):
            lines.append(f"      - {area}")
        if entry.get("packs"):
            lines.append("    packs:")
            for pack in entry["packs"]:
                lines.append(f"      - {pack}")
        if entry.get("collections"):
            lines.append("    collections:")
            for collection in entry["collections"]:
                lines.append(f"      - {collection}")
        lines.append(f"    rationale: {entry['rationale']}")
        lines.append("    promotion_criteria:")
        for criterion in entry.get("promotion_criteria", DEFAULT_PROMOTION_CRITERIA):
            lines.append(f"      - {criterion}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def generate_backlog_file(root: Path, merge_existing: bool = True) -> tuple[Path, int]:
    taxonomy = load_taxonomy(root)
    generated = generate_backlog_entries(taxonomy)
    backlog_file = backlog_path(root)

    existing: list[dict[str, Any]] = []
    if merge_existing and backlog_file.exists():
        existing_data = parse_yaml_file(backlog_file)
        if isinstance(existing_data, dict):
            raw = existing_data.get("skills", [])
            existing = [item for item in raw if isinstance(item, dict)]

    skill_statuses = load_skill_folder_statuses(root)
    entries = merge_backlog_entries(generated, existing, skill_statuses)
    dump_backlog(backlog_file, entries)
    return backlog_file, len(entries)
