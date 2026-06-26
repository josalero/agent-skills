from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .catalog import load_repository
from .paths import skill_eval_prompt_path
from .models import (
    SUPPORTED_AREAS,
    SUPPORTED_DOMAINS,
    SUPPORTED_KINDS,
    SUPPORTED_MODES,
    SUPPORTED_PRIORITIES,
    SUPPORTED_STABILITIES,
    SUPPORTED_STATUSES,
    SUPPORTED_TARGETS,
    Issue,
    Repository,
    Skill,
)
from .parse import ParseError, parse_skill_markdown, parse_yaml_file


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REFERENCE_RE = re.compile(r"`?(references/[A-Za-z0-9_.\-/]+\.md)`?")
TODO_RE = re.compile(r"\bTODO\b", re.IGNORECASE)
INSTALLABLE_STATUSES = {"active", "recommended"}


def validate_repository(root: Path, skill_id: str | None = None, include_backlog: bool = True) -> tuple[Repository, list[Issue]]:
    repo, load_warnings = load_repository(root)
    issues = [Issue("warning", root, warning) for warning in load_warnings]

    skills_dir = root / "skills"
    if not skills_dir.exists():
        issues.append(Issue("error", skills_dir, "skills directory is required"))
    else:
        skill_dirs = sorted(path for path in skills_dir.iterdir() if path.is_dir())
        if skill_id:
            skill_dirs = [skills_dir / skill_id]
            if not skill_dirs[0].exists():
                issues.append(Issue("error", skill_dirs[0], f"skill does not exist: {skill_id}"))
        for skill_dir in skill_dirs:
            issues.extend(validate_skill_dir(skill_dir, repo))

    if not skill_id:
        issues.extend(validate_collections(repo))
        issues.extend(validate_packs(repo))
        if include_backlog:
            issues.extend(validate_backlog(repo))
    return repo, issues


def validate_skill_dir(skill_dir: Path, repo: Repository) -> list[Issue]:
    issues: list[Issue] = []
    folder_name = skill_dir.name
    if not NAME_RE.match(folder_name):
        issues.append(Issue("error", skill_dir, "skill folder name must use lowercase letters, digits, and hyphens"))

    skill_md = skill_dir / "SKILL.md"
    metadata_path = skill_dir / "skill.yaml"
    if not skill_md.exists():
        issues.append(Issue("error", skill_md, "SKILL.md is required"))
        return issues
    if not metadata_path.exists():
        issues.append(Issue("error", metadata_path, "skill.yaml is required"))
        return issues

    try:
        frontmatter, body = parse_skill_markdown(skill_md)
    except ParseError as exc:
        issues.append(Issue("error", skill_md, str(exc)))
        return issues

    try:
        metadata = parse_yaml_file(metadata_path)
    except ParseError as exc:
        issues.append(Issue("error", metadata_path, str(exc)))
        return issues

    if not isinstance(metadata, dict):
        issues.append(Issue("error", metadata_path, "skill.yaml must contain a mapping"))
        return issues

    required_frontmatter = ("name", "description")
    for field in required_frontmatter:
        if not str(frontmatter.get(field, "")).strip():
            issues.append(Issue("error", skill_md, f"frontmatter.{field} is required"))
    if frontmatter.get("name") != folder_name:
        issues.append(Issue("error", skill_md, "frontmatter.name must match folder name"))
    if not body.strip():
        issues.append(Issue("error", skill_md, "body is required"))

    required_metadata = (
        "id",
        "display_name",
        "domain",
        "kind",
        "modes",
        "status",
        "summary",
        "areas",
        "tags",
        "collections",
        "packs",
        "targets",
        "stability",
    )
    for field in required_metadata:
        if field not in metadata:
            issues.append(Issue("error", metadata_path, f"{field} is required"))
    if metadata.get("id") != folder_name:
        issues.append(Issue("error", metadata_path, "id must match folder name"))

    issues.extend(validate_known_value(metadata_path, "domain", metadata.get("domain"), SUPPORTED_DOMAINS))
    issues.extend(validate_known_value(metadata_path, "kind", metadata.get("kind"), SUPPORTED_KINDS))
    issues.extend(validate_list_values(metadata_path, "modes", metadata.get("modes"), SUPPORTED_MODES))
    modes = metadata.get("modes")
    if isinstance(modes, list) and not modes:
        issues.append(Issue("error", metadata_path, "modes must contain at least one value"))
    issues.extend(validate_known_value(metadata_path, "status", metadata.get("status"), SUPPORTED_STATUSES))
    issues.extend(validate_known_value(metadata_path, "stability", metadata.get("stability"), SUPPORTED_STABILITIES))

    issues.extend(validate_list_values(metadata_path, "areas", metadata.get("areas"), SUPPORTED_AREAS))
    issues.extend(validate_string_list(metadata_path, "tags", metadata.get("tags")))
    issues.extend(validate_string_list(metadata_path, "collections", metadata.get("collections")))
    issues.extend(validate_string_list(metadata_path, "packs", metadata.get("packs")))

    collections = metadata.get("collections", [])
    if isinstance(collections, list):
        for collection_id in collections:
            if collection_id not in repo.collections:
                issues.append(Issue("error", metadata_path, f"unknown collection: {collection_id}"))

    packs = metadata.get("packs", [])
    if isinstance(packs, list):
        for pack_id in packs:
            if pack_id not in repo.packs:
                issues.append(Issue("error", metadata_path, f"unknown pack: {pack_id}"))

    targets = metadata.get("targets")
    if not isinstance(targets, dict):
        issues.append(Issue("error", metadata_path, "targets must be a mapping"))
    else:
        enabled = [target for target, value in targets.items() if value is True]
        if not enabled:
            issues.append(Issue("error", metadata_path, "at least one target must be enabled"))
        for target, value in targets.items():
            if target not in SUPPORTED_TARGETS:
                issues.append(Issue("error", metadata_path, f"unsupported target: {target}"))
            if not isinstance(value, bool):
                issues.append(Issue("error", metadata_path, f"target value must be boolean: {target}"))

    referenced = set(REFERENCE_RE.findall(body))
    for ref in referenced:
        if not (skill_dir / ref).exists():
            issues.append(Issue("error", skill_md, f"referenced file does not exist: {ref}"))

    references_dir = skill_dir / "references"
    if references_dir.exists():
        for ref_file in references_dir.rglob("*.md"):
            rel = ref_file.relative_to(skill_dir).as_posix()
            if rel not in referenced:
                issues.append(Issue("warning", ref_file, "reference file is not mentioned in SKILL.md"))

    issues.extend(validate_active_skill_quality(skill_dir, repo, metadata, skill_md, body))

    return issues


def validate_active_skill_quality(
    skill_dir: Path,
    repo: Repository,
    metadata: dict[str, Any],
    skill_md: Path,
    body: str,
) -> list[Issue]:
    issues: list[Issue] = []
    status = metadata.get("status")
    if status not in INSTALLABLE_STATUSES:
        return issues

    skill_id = skill_dir.name
    combined = f"{body}\n{metadata.get('summary', '')}"
    if TODO_RE.search(combined):
        issues.append(
            Issue(
                "error",
                skill_md,
                f"status {status} skills must not contain TODO markers in SKILL.md",
            )
        )

    eval_path = skill_eval_prompt_path(repo.root, skill_id)
    if not eval_path.exists():
        issues.append(
            Issue(
                "warning",
                skill_md,
                f"missing eval prompt: skills/{skill_id}/eval/prompt.md",
            )
        )

    references_dir = skill_dir / "references"
    if references_dir.exists() and any(references_dir.rglob("*.md")):
        return issues

    if status == "active":
        issues.append(
            Issue(
                "warning",
                skill_md,
                "active skill has no references/*.md files; add references when code samples or checklists are needed",
            )
        )

    return issues


def validate_collections(repo: Repository) -> list[Issue]:
    issues: list[Issue] = []
    for collection in repo.collections.values():
        data = collection.data
        for field in ("id", "display_name", "description", "skills"):
            if field not in data:
                issues.append(Issue("error", collection.path, f"{field} is required"))
        if data.get("id") != collection.path.stem:
            issues.append(Issue("error", collection.path, "id must match file name"))
        skills = data.get("skills", [])
        if not isinstance(skills, list):
            issues.append(Issue("error", collection.path, "skills must be a list"))
            continue
        issues.extend(validate_unique_list(collection.path, "skills", skills))
        for item in skills:
            if item not in repo.skills:
                issues.append(Issue("error", collection.path, f"unknown skill: {item}"))
    return issues


def validate_packs(repo: Repository) -> list[Issue]:
    issues: list[Issue] = []
    for pack in repo.packs.values():
        data = pack.data
        for field in ("id", "display_name", "description", "skills", "targets"):
            if field not in data:
                issues.append(Issue("error", pack.path, f"{field} is required"))
        if data.get("id") != pack.path.stem:
            issues.append(Issue("error", pack.path, "id must match file name"))
        skills = data.get("skills", [])
        if not isinstance(skills, list):
            issues.append(Issue("error", pack.path, "skills must be a list"))
        else:
            issues.extend(validate_unique_list(pack.path, "skills", skills))
            for item in skills:
                if item not in repo.skills:
                    issues.append(Issue("error", pack.path, f"unknown skill: {item}"))
        targets = data.get("targets", [])
        issues.extend(validate_list_values(pack.path, "targets", targets, SUPPORTED_TARGETS))
    return issues


def validate_backlog(repo: Repository) -> list[Issue]:
    issues: list[Issue] = []
    if repo.backlog is None:
        issues.append(Issue("error", repo.root / "registry" / "skill-backlog.yaml", "backlog file is required"))
        return issues
    data = repo.backlog.data
    skills = data.get("skills")
    if not isinstance(skills, list):
        issues.append(Issue("error", repo.backlog.path, "skills must be a list"))
        return issues
    seen: set[str] = set()
    for index, item in enumerate(skills):
        if not isinstance(item, dict):
            issues.append(Issue("error", repo.backlog.path, f"skills[{index}] must be a mapping"))
            continue
        skill_id = str(item.get("id", ""))
        if not NAME_RE.match(skill_id):
            issues.append(Issue("error", repo.backlog.path, f"invalid backlog skill id: {skill_id}"))
        if skill_id in seen:
            issues.append(Issue("error", repo.backlog.path, f"duplicate backlog skill id: {skill_id}"))
        seen.add(skill_id)
        for field in (
            "id",
            "display_name",
            "domain",
            "kind",
            "priority",
            "status",
            "areas",
            "rationale",
            "promotion_criteria",
        ):
            if field not in item:
                issues.append(Issue("error", repo.backlog.path, f"{skill_id}: {field} is required"))
        issues.extend(validate_known_value(repo.backlog.path, f"{skill_id}.domain", item.get("domain"), SUPPORTED_DOMAINS))
        issues.extend(validate_known_value(repo.backlog.path, f"{skill_id}.kind", item.get("kind"), SUPPORTED_KINDS))
        issues.extend(validate_known_value(repo.backlog.path, f"{skill_id}.priority", item.get("priority"), SUPPORTED_PRIORITIES))
        issues.extend(validate_known_value(repo.backlog.path, f"{skill_id}.status", item.get("status"), SUPPORTED_STATUSES))
        issues.extend(validate_list_values(repo.backlog.path, f"{skill_id}.areas", item.get("areas"), SUPPORTED_AREAS))
        status = item.get("status")
        if status in {"draft", "active", "recommended"} and skill_id not in repo.skills:
            issues.append(Issue("error", repo.backlog.path, f"{skill_id}: status {status} requires an active skill folder"))
        if status == "proposed" and skill_id in repo.skills:
            issues.append(Issue("warning", repo.backlog.path, f"{skill_id}: proposed backlog item already has a skill folder"))
    return issues


def validate_known_value(path: Path, field: str, value: Any, allowed: set[str]) -> list[Issue]:
    if value not in allowed:
        return [Issue("error", path, f"{field} has unsupported value: {value}")]
    return []


def validate_list_values(path: Path, field: str, values: Any, allowed: set[str]) -> list[Issue]:
    issues = validate_string_list(path, field, values)
    if issues:
        return issues
    for value in values:
        if value not in allowed:
            issues.append(Issue("error", path, f"{field} has unsupported value: {value}"))
    return issues


def validate_string_list(path: Path, field: str, values: Any) -> list[Issue]:
    if not isinstance(values, list):
        return [Issue("error", path, f"{field} must be a list")]
    return [Issue("error", path, f"{field} must contain only strings") for value in values if not isinstance(value, str)]


def validate_unique_list(path: Path, field: str, values: list[Any]) -> list[Issue]:
    issues: list[Issue] = []
    seen: set[Any] = set()
    for value in values:
        if value in seen:
            issues.append(Issue("error", path, f"{field} contains duplicate value: {value}"))
        seen.add(value)
    return issues


def has_errors(issues: list[Issue]) -> bool:
    return any(issue.severity == "error" for issue in issues)

