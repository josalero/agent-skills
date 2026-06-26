from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from .backlog_gen import load_waves
from .filesystem import write_text_if_changed
from .models import Backlog, Collection, Pack, Repository, Skill
from .parse import ParseError, parse_skill_markdown, parse_yaml_file
from .paths import backlog_path, collections_dir, packs_dir


def load_repository(root: Path) -> tuple[Repository, list[str]]:
    root = root.resolve()
    repo = Repository(root=root)
    warnings: list[str] = []

    skills_dir = root / "skills"
    if skills_dir.exists():
        for skill_dir in sorted(path for path in skills_dir.iterdir() if path.is_dir()):
            skill_md = skill_dir / "SKILL.md"
            metadata_path = skill_dir / "skill.yaml"
            if not skill_md.exists() or not metadata_path.exists():
                continue
            try:
                frontmatter, body = parse_skill_markdown(skill_md)
                metadata = parse_yaml_file(metadata_path)
                if not isinstance(metadata, dict):
                    warnings.append(f"{metadata_path}: expected mapping")
                    metadata = {}
                skill_id = str(metadata.get("id") or skill_dir.name)
                repo.skills[skill_id] = Skill(
                    id=skill_id,
                    path=skill_dir,
                    frontmatter=frontmatter,
                    body=body,
                    metadata=metadata,
                )
            except ParseError as exc:
                warnings.append(f"{skill_dir}: {exc}")

    collections_root = collections_dir(root)
    if collections_root.exists():
        for path in sorted(collections_root.glob("*.yaml")):
            try:
                data = parse_yaml_file(path)
                if isinstance(data, dict):
                    repo.collections[str(data.get("id") or path.stem)] = Collection(
                        id=str(data.get("id") or path.stem),
                        path=path,
                        data=data,
                    )
            except ParseError as exc:
                warnings.append(f"{path}: {exc}")

    packs_root = packs_dir(root)
    if packs_root.exists():
        for path in sorted(packs_root.glob("*.yaml")):
            try:
                data = parse_yaml_file(path)
                if isinstance(data, dict):
                    repo.packs[str(data.get("id") or path.stem)] = Pack(
                        id=str(data.get("id") or path.stem),
                        path=path,
                        data=data,
                    )
            except ParseError as exc:
                warnings.append(f"{path}: {exc}")

    backlog_file = backlog_path(root)
    if backlog_file.exists():
        try:
            data = parse_yaml_file(backlog_file)
            if isinstance(data, dict):
                repo.backlog = Backlog(path=backlog_file, data=data)
        except ParseError as exc:
            warnings.append(f"{backlog_file}: {exc}")

    return repo, warnings


def active_skill_catalog(repo: Repository) -> list[dict[str, Any]]:
    return [
        item
        for item in skill_catalog(repo)
        if item.get("status") in {"active", "recommended"}
    ]


def skill_catalog(repo: Repository) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for skill in sorted(repo.skills.values(), key=lambda item: item.id):
        items.append(
            {
                "id": skill.id,
                "display_name": skill.metadata.get("display_name"),
                "domain": skill.metadata.get("domain"),
                "kind": skill.metadata.get("kind"),
                "modes": skill.metadata.get("modes", []),
                "status": skill.metadata.get("status"),
                "stability": skill.metadata.get("stability"),
                "summary": skill.summary,
                "areas": skill.metadata.get("areas", []),
                "collections": skill.metadata.get("collections", []),
                "packs": skill.metadata.get("packs", []),
                "targets": sorted(skill.enabled_targets),
            }
        )
    return items


def backlog_catalog(repo: Repository) -> list[dict[str, Any]]:
    if repo.backlog is None:
        return []
    items: list[dict[str, Any]] = []
    for item in repo.backlog.data.get("skills", []):
        if isinstance(item, dict) and item.get("id"):
            items.append(item)
    return sorted(items, key=lambda item: str(item["id"]))


def write_catalog(repo: Repository, include_backlog: bool = True) -> list[Path]:
    dist_dir = repo.root / "dist" / "catalog"
    changed: list[Path] = []

    all_skills = skill_catalog(repo)
    active_skills = active_skill_catalog(repo)

    json_path = dist_dir / "skills.json"
    if write_text_if_changed(json_path, json.dumps(active_skills, indent=2, sort_keys=True)):
        changed.append(json_path)

    all_json_path = dist_dir / "skills-all.json"
    if write_text_if_changed(all_json_path, json.dumps(all_skills, indent=2, sort_keys=True)):
        changed.append(all_json_path)

    skills_md = _render_skill_markdown("# Skill Catalog (All Folders)", all_skills)
    md_path = dist_dir / "skills.md"
    if write_text_if_changed(md_path, skills_md):
        changed.append(md_path)

    active_md_path = dist_dir / "active-skills.md"
    if write_text_if_changed(active_md_path, _render_skill_markdown("# Active Skills", active_skills)):
        changed.append(active_md_path)

    if include_backlog and repo.backlog is not None:
        backlog_items = backlog_catalog(repo)
        backlog_md = _render_backlog_markdown(backlog_items)
        backlog_path = dist_dir / "backlog.md"
        if write_text_if_changed(backlog_path, backlog_md):
            changed.append(backlog_path)

        coverage_path = dist_dir / "coverage-by-domain.md"
        if write_text_if_changed(coverage_path, _render_coverage_markdown(repo, backlog_items)):
            changed.append(coverage_path)

        mode_coverage_path = dist_dir / "coverage-by-mode.md"
        if write_text_if_changed(mode_coverage_path, _render_coverage_by_mode_markdown(repo)):
            changed.append(mode_coverage_path)

    packs_md = _render_packs_markdown(repo)
    packs_path = dist_dir / "packs.md"
    if write_text_if_changed(packs_path, packs_md):
        changed.append(packs_path)

    collections_md = _render_collections_markdown(repo)
    collections_path = dist_dir / "collections.md"
    if write_text_if_changed(collections_path, collections_md):
        changed.append(collections_path)

    waves_md = _render_waves_markdown(repo)
    waves_path = dist_dir / "waves.md"
    if write_text_if_changed(waves_path, waves_md):
        changed.append(waves_path)

    return changed


def _render_skill_markdown(title: str, items: list[dict[str, Any]]) -> str:
    lines = [title, ""]
    if not items:
        lines.append("_No skills in this view._")
        lines.append("")
        return "\n".join(lines)
    for item in items:
        lines.append(f"## {item['display_name'] or item['id']}")
        lines.append("")
        lines.append(f"- ID: `{item['id']}`")
        lines.append(f"- Domain: `{item['domain']}`")
        lines.append(f"- Kind: `{item['kind']}`")
        modes = item.get("modes") or []
        lines.append(f"- Modes: {', '.join(f'`{mode}`' for mode in modes) if modes else '—'}")
        lines.append(f"- Status: `{item['status']}`")
        lines.append(f"- Targets: {', '.join(item['targets'])}")
        lines.append("")
        lines.append(str(item["summary"]))
        lines.append("")
    return "\n".join(lines)


def _render_backlog_markdown(items: list[dict[str, Any]]) -> str:
    lines = ["# Skill Backlog", ""]
    for item in items:
        lines.append(f"## {item.get('display_name', item['id'])}")
        lines.append("")
        lines.append(f"- ID: `{item['id']}`")
        lines.append(f"- Domain: `{item.get('domain')}`")
        lines.append(f"- Kind: `{item.get('kind')}`")
        lines.append(f"- Priority: `{item.get('priority')}`")
        lines.append(f"- Status: `{item.get('status')}`")
        lines.append("")
        lines.append(str(item.get("rationale", "")))
        lines.append("")
    return "\n".join(lines)


def _render_packs_markdown(repo: Repository) -> str:
    lines = ["# Packs", ""]
    for pack in sorted(repo.packs.values(), key=lambda item: item.id):
        lines.append(f"## {pack.data.get('display_name', pack.id)}")
        lines.append("")
        lines.append(f"- ID: `{pack.id}`")
        lines.append(f"- Description: {pack.data.get('description', '')}")
        lines.append("- Skills:")
        for skill_id in pack.data.get("skills", []):
            lines.append(f"  - `{skill_id}`")
        lines.append("")
    return "\n".join(lines)


def _render_collections_markdown(repo: Repository) -> str:
    lines = ["# Collections", ""]
    for collection in sorted(repo.collections.values(), key=lambda item: item.id):
        lines.append(f"## {collection.data.get('display_name', collection.id)}")
        lines.append("")
        lines.append(f"- ID: `{collection.id}`")
        lines.append(f"- Description: {collection.data.get('description', '')}")
        lines.append("- Skills:")
        for skill_id in collection.data.get("skills", []):
            lines.append(f"  - `{skill_id}`")
        lines.append("")
    return "\n".join(lines)


def _render_waves_markdown(repo: Repository) -> str:
    lines = ["# Promotion Waves", ""]
    try:
        waves = load_waves(repo.root).get("waves", [])
    except ParseError:
        waves = []
    for wave in waves:
        if not isinstance(wave, dict):
            continue
        lines.append(f"## {wave.get('display_name', wave.get('id'))}")
        lines.append("")
        lines.append(f"- ID: `{wave.get('id')}`")
        lines.append("- Skills:")
        for skill_id in wave.get("skills", []):
            lines.append(f"  - `{skill_id}`")
        lines.append("")
    return "\n".join(lines)


def _render_coverage_markdown(repo: Repository, backlog_items: list[dict[str, Any]]) -> str:
    folder_status = Counter(str(skill.metadata.get("status", "draft")) for skill in repo.skills.values())
    backlog_status = Counter(str(item.get("status", "proposed")) for item in backlog_items)
    domain_counter: Counter[str] = Counter()
    for skill in repo.skills.values():
        domain_counter[str(skill.metadata.get("domain", "unknown"))] += 1
    for item in backlog_items:
        if item.get("status") == "proposed":
            domain_counter[str(item.get("domain", "unknown"))] += 0

    lines = ["# Coverage By Domain", "", "## Skill Folders By Status", ""]
    for status, count in sorted(folder_status.items()):
        lines.append(f"- `{status}`: {count}")
    lines.append("")
    lines.append("## Backlog By Status")
    lines.append("")
    for status, count in sorted(backlog_status.items()):
        lines.append(f"- `{status}`: {count}")
    lines.append("")
    lines.append("## Skill Folders By Domain")
    lines.append("")
    for domain, count in sorted(domain_counter.items()):
        lines.append(f"- `{domain}`: {count}")
    lines.append("")
    return "\n".join(lines)


def _render_coverage_by_mode_markdown(repo: Repository) -> str:
    mode_counter: Counter[str] = Counter()
    dual_count = 0
    for skill in repo.skills.values():
        modes = skill.metadata.get("modes", [])
        if not isinstance(modes, list):
            continue
        normalized = sorted({str(mode) for mode in modes if isinstance(mode, str) and mode in {"coding", "planning"}})
        if len(normalized) == 2:
            dual_count += 1
        for mode in normalized:
            mode_counter[mode] += 1

    lines = ["# Coverage By Mode", "", "Agent modes describe when to use a skill:", ""]
    lines.append("- `planning` — design, review, strategy, migration planning, go/no-go")
    lines.append("- `coding` — implement, refactor, write tests, apply fixes")
    lines.append("")
    lines.append("## Skills By Mode")
    lines.append("")
    for mode, count in sorted(mode_counter.items()):
        lines.append(f"- `{mode}`: {count}")
    lines.append("")
    lines.append(f"- `planning+coding` (both): {dual_count}")
    lines.append("")
    lines.append("## Skills By Mode And Domain")
    lines.append("")
    for mode in ("planning", "coding"):
        lines.append(f"### {mode.title()}")
        lines.append("")
        for skill in sorted(repo.skills.values(), key=lambda item: item.id):
            skill_modes = skill.metadata.get("modes", [])
            if not isinstance(skill_modes, list) or mode not in skill_modes:
                continue
            domain = skill.metadata.get("domain", "unknown")
            lines.append(f"- `{skill.id}` ({domain})")
        lines.append("")
    return "\n".join(lines)

