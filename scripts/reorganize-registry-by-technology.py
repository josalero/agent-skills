#!/usr/bin/env python3
"""One-shot migration: group collections and packs by technology."""

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from skillforge.parse import parse_yaml_file
from skillforge.promote import _dump_mapping

TECH_DOMAINS = {"java", "kotlin", "rust", "dotnet", "php", "react", "angular", "vue"}
TECH_PACKS = {
    "java": "java-backend-pack",
    "kotlin": "kotlin-backend-pack",
    "rust": "rust-backend-pack",
    "dotnet": "dotnet-backend-pack",
    "php": "php-backend-pack",
    "react": "frontend-react-pack",
    "angular": "frontend-angular-pack",
    "vue": "frontend-vue-pack",
}

REMOVED_COLLECTIONS = {"frontend", "backend", "testing", "code-quality", "migrations"}
REMOVED_PACKS = {
    "quality-gates-pack",
    "security-review-pack",
    "testing-verification-pack",
    "production-readiness-pack",
    "ai-engineering-pack",
    "frontend-ux-ui-pack",
}

WRITING_SKILLS = {
    "technical-article-authoring",
    "technical-documentation-authoring",
    "software-design-analysis",
}

FRONTEND_IMPLEMENTATION_SKILLS = {"frontend-ui-engineering"}


def primary_collection(skill_id: str, domain: str) -> str:
    if domain in TECH_DOMAINS:
        return domain
    if skill_id in WRITING_SKILLS:
        return "technical-writing"
    return "architecture"


def collections_for_skill(skill_id: str, domain: str) -> list[str]:
    if skill_id in FRONTEND_IMPLEMENTATION_SKILLS:
        return ["react", "angular", "vue"]
    return [primary_collection(skill_id, domain)]


def packs_for_skill(skill_id: str, domain: str, existing: list[str]) -> list[str]:
    packs: set[str] = set(existing) - REMOVED_PACKS

    if domain in TECH_DOMAINS:
        packs.add(TECH_PACKS[domain])
    elif skill_id in WRITING_SKILLS:
        packs.add("technical-writing-pack")
    else:
        packs.add("architecture-review-pack")

    if skill_id in FRONTEND_IMPLEMENTATION_SKILLS:
        packs.update(
            {
                "frontend-react-pack",
                "frontend-angular-pack",
                "frontend-vue-pack",
            }
        )
        packs.discard("architecture-review-pack")

    return sorted(packs)


def render_registry_mapping(data: dict[str, Any]) -> str:
    lines: list[str] = []
    for key, value in data.items():
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - {item}")
        else:
            lines.append(f"{key}: {value}")
    return "\n".join(lines) + "\n"


def rebuild_collection_files(skills: dict[str, dict]) -> None:
    membership: dict[str, set[str]] = defaultdict(set)
    for skill_id, metadata in skills.items():
        for collection_id in metadata.get("collections", []):
            membership[collection_id].add(skill_id)

    collections_dir = ROOT / "registry" / "collections"
    for path in sorted(collections_dir.glob("*.yaml")):
        if path.stem in REMOVED_COLLECTIONS:
            path.unlink()
            continue
        data = parse_yaml_file(path)
        if not isinstance(data, dict):
            continue
        collection_id = str(data.get("id") or path.stem)
        data["skills"] = sorted(membership.get(collection_id, set()))
        path.write_text(render_registry_mapping(data), encoding="utf-8")


def rebuild_pack_files(skills: dict[str, dict]) -> None:
    membership: dict[str, set[str]] = defaultdict(set)
    for skill_id, metadata in skills.items():
        for pack_id in metadata.get("packs", []):
            membership[pack_id].add(skill_id)

    packs_dir = ROOT / "registry" / "packs"
    for path in sorted(packs_dir.glob("*.yaml")):
        if path.stem in REMOVED_PACKS:
            path.unlink()
            continue
        data = parse_yaml_file(path)
        if not isinstance(data, dict):
            continue
        pack_id = str(data.get("id") or path.stem)
        data["skills"] = sorted(membership.get(pack_id, set()))
        path.write_text(render_registry_mapping(data), encoding="utf-8")


def main() -> None:
    skills_dir = ROOT / "skills"
    skills: dict[str, dict] = {}

    for skill_yaml in sorted(skills_dir.glob("*/skill.yaml")):
        metadata = parse_yaml_file(skill_yaml)
        if not isinstance(metadata, dict):
            raise SystemExit(f"invalid skill metadata: {skill_yaml}")
        skill_id = str(metadata.get("id") or skill_yaml.parent.name)
        domain = str(metadata.get("domain", ""))

        metadata["collections"] = collections_for_skill(skill_id, domain)
        metadata["packs"] = packs_for_skill(skill_id, domain, list(metadata.get("packs") or []))
        skill_yaml.write_text(_dump_mapping(metadata), encoding="utf-8")
        skills[skill_id] = metadata

    rebuild_collection_files(skills)
    rebuild_pack_files(skills)
    print("Reorganized registry by technology.")


if __name__ == "__main__":
    main()
