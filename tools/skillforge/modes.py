from __future__ import annotations

SUPPORTED_MODES = frozenset({"coding", "planning"})

PLANNING_ONLY_SKILLS = frozenset(
    {
        "agent-orchestration-design",
        "ai-evaluation-architecture",
        "api-design-review",
        "cloud-native-delivery",
        "llm-application-architecture",
        "migration-planning",
        "observability-review",
        "production-readiness-review",
        "rag-architecture-review",
        "security-review",
        "system-architecture-review",
        "software-design-analysis",
        "technical-article-authoring",
        "technical-documentation-authoring",
        "testing-strategy",
        "tool-calling-design-review",
        "ui-design-system-review",
        "ux-design-review",
    }
)

CODING_ONLY_SKILLS = frozenset(
    {
        "angular-application-engineering",
        "angular-rxjs-patterns",
        "angular-state-management",
        "dotnet-aspnet-service",
        "dotnet-core-engineering",
        "frontend-ui-engineering",
        "java-21-lts",
        "java-25-lts",
        "java-core-engineering",
        "java-spring-boot-35",
        "java-spring-boot-41",
        "java-spring-boot-service",
        "kotlin-core-engineering",
        "kotlin-coroutines-patterns",
        "kotlin-spring-boot-service",
        "php-core-engineering",
        "php-laravel-service",
        "php-symfony-service",
        "react-component-engineering",
        "react-state-management",
        "rust-api-service",
        "rust-async-patterns",
        "rust-core-engineering",
        "vue-application-engineering",
        "vue-composables-patterns",
        "vue-state-management",
    }
)


def resolve_modes(skill_id: str) -> list[str]:
    """Return canonical agent modes for a skill id."""
    if skill_id in PLANNING_ONLY_SKILLS:
        return ["planning"]
    if skill_id in CODING_ONLY_SKILLS:
        return ["coding"]
    return ["planning", "coding"]


def skill_supports_modes(metadata_modes: object, requested: set[str]) -> bool:
    if not requested:
        return True
    if not isinstance(metadata_modes, list):
        return False
    skill_modes = {str(mode) for mode in metadata_modes if isinstance(mode, str)}
    return requested.issubset(skill_modes)
