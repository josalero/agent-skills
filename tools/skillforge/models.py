from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


SUPPORTED_TARGETS = {"codex", "cursor", "copilot", "claude"}
SUPPORTED_DOMAINS = {
    "java",
    "dotnet",
    "php",
    "react",
    "angular",
    "node",
    "python",
    "database",
    "cloud",
    "security",
    "testing",
    "architecture",
    "cross-stack",
}
SUPPORTED_KINDS = {
    "general",
    "framework",
    "version",
    "migration",
    "diagnostic",
    "testing",
    "security",
    "architecture",
    "delivery",
    "ai-engineering",
    "review",
}
SUPPORTED_STATUSES = {"proposed", "draft", "active", "recommended", "deprecated", "archived"}
SUPPORTED_STABILITIES = {"experimental", "stable", "recommended"}
SUPPORTED_PRIORITIES = {"P0", "P1", "P2", "P3"}
SUPPORTED_MODES = {"coding", "planning"}
SUPPORTED_AREAS = {
    "backend",
    "frontend",
    "full-stack",
    "api-design",
    "code-quality",
    "data-persistence",
    "observability",
    "performance",
    "concurrency",
    "security",
    "testing",
    "architecture",
    "cloud-delivery",
    "ai-engineering",
    "developer-experience",
    "versions",
    "migrations",
}


@dataclass(frozen=True)
class Issue:
    severity: str
    path: Path
    message: str


@dataclass
class Skill:
    id: str
    path: Path
    frontmatter: dict[str, Any]
    body: str
    metadata: dict[str, Any]

    @property
    def enabled_targets(self) -> set[str]:
        targets = self.metadata.get("targets", {})
        if not isinstance(targets, dict):
            return set()
        return {target for target, enabled in targets.items() if enabled is True}

    @property
    def description(self) -> str:
        return str(self.frontmatter.get("description", "")).strip()

    @property
    def summary(self) -> str:
        return str(self.metadata.get("summary") or self.description).strip()


@dataclass
class Collection:
    id: str
    path: Path
    data: dict[str, Any]


@dataclass
class Pack:
    id: str
    path: Path
    data: dict[str, Any]


@dataclass
class Backlog:
    path: Path
    data: dict[str, Any]


@dataclass
class Repository:
    root: Path
    skills: dict[str, Skill] = field(default_factory=dict)
    collections: dict[str, Collection] = field(default_factory=dict)
    packs: dict[str, Pack] = field(default_factory=dict)
    backlog: Backlog | None = None

