from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .catalog import load_repository
from .models import Repository

IGNORED_DIR_NAMES = frozenset(
    {
        ".git",
        ".hg",
        ".svn",
        "node_modules",
        "vendor",
        "target",
        "build",
        "dist",
        "out",
        ".gradle",
        ".idea",
        ".vscode",
        "__pycache__",
        ".cursor",
        ".claude",
        "coverage",
    }
)

SCAN_MAX_DEPTH = 5
READ_LIMIT_BYTES = 96_000

JAVA_MARKERS = (
    "spring-boot",
    "org.springframework.boot",
    "springframework",
)
KOTLIN_MARKERS = (
    "org.jetbrains.kotlin",
    "kotlin(\"jvm\")",
    "kotlin(\"android\")",
    "kotlin-gradle-plugin",
    "kotlin.version",
    "kotlin-maven-plugin",
)
AI_MARKERS = (
    "langchain",
    "langchain4j",
    "openai",
    "anthropic",
    "spring-ai",
    "llamaindex",
    "pgvector",
    "vectorstore",
    "embeddings",
)
DOCKER_MARKERS = ("dockerfile", "docker-compose", "compose.yaml", "compose.yml")
CI_MARKERS = (".github/workflows", ".gitlab-ci.yml", "Jenkinsfile", "azure-pipelines.yml")


@dataclass(frozen=True)
class RepoProfile:
    stacks: tuple[str, ...] = ()
    features: tuple[str, ...] = ()
    evidence: dict[str, tuple[str, ...]] = field(default_factory=dict)

    def has_stack(self, stack: str) -> bool:
        return stack in self.stacks

    def has_feature(self, feature: str) -> bool:
        return feature in self.features


@dataclass(frozen=True)
class PackRecommendation:
    pack_id: str
    display_name: str
    tier: str
    reason: str
    skill_count: int


@dataclass(frozen=True)
class SkillRecommendation:
    skill_id: str
    display_name: str
    reason: str


@dataclass(frozen=True)
class RecommendReport:
    project_root: Path
    profile: RepoProfile
    packs: tuple[PackRecommendation, ...]
    skills: tuple[SkillRecommendation, ...]
    warnings: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "project_root": str(self.project_root),
            "profile": {
                "stacks": list(self.profile.stacks),
                "features": list(self.profile.features),
                "evidence": {key: list(values) for key, values in self.profile.evidence.items()},
            },
            "packs": [
                {
                    "pack_id": item.pack_id,
                    "display_name": item.display_name,
                    "tier": item.tier,
                    "reason": item.reason,
                    "skill_count": item.skill_count,
                }
                for item in self.packs
            ],
            "skills": [
                {
                    "skill_id": item.skill_id,
                    "display_name": item.display_name,
                    "reason": item.reason,
                }
                for item in self.skills
            ],
            "install_commands": list(self.install_commands()),
            "warnings": list(self.warnings),
        }

    def install_commands(
        self,
        agent_skills_root: Path | None = None,
        *,
        target: str = "cursor",
    ) -> list[str]:
        root_hint = str(agent_skills_root) if agent_skills_root else "/path/to/agent-skills"
        commands: list[str] = []
        for pack in self.packs:
            if pack.tier != "recommended":
                continue
            commands.append(
                f"./scripts/install-from-clone.sh --dest {self.project_root} --pack {pack.pack_id} --target {target}"
            )
        if not commands and self.packs:
            pack_id = self.packs[0].pack_id
            commands.append(
                f"./scripts/install-from-clone.sh --dest {self.project_root} --pack {pack_id}"
            )
        if root_hint != "/path/to/agent-skills":
            commands = [cmd.replace("./scripts/", f"{root_hint}/scripts/") for cmd in commands]
        return commands


def analyze_project(project_root: Path) -> RepoProfile:
    """Inspect a project directory and return detected stacks and features."""
    project_root = project_root.resolve()
    if not project_root.is_dir():
        raise ValueError(f"Project path is not a directory: {project_root}")

    evidence: dict[str, list[str]] = {}
    stacks: set[str] = set()
    features: set[str] = set()

    def note(category: str, relative: str) -> None:
        evidence.setdefault(category, []).append(relative)

    pom_files = _find_named_files(project_root, {"pom.xml"})
    gradle_files = _find_named_files(project_root, {"build.gradle", "build.gradle.kts", "settings.gradle.kts"})
    if pom_files or gradle_files:
        stacks.add("java")
        for path in pom_files + gradle_files:
            note("java", _relative(project_root, path))
        combined = "\n".join(_read_text(path) for path in (pom_files + gradle_files)[:6])
        if _contains_any(combined, JAVA_MARKERS):
            features.add("spring-boot")
            note("spring-boot", _relative(project_root, pom_files[0] if pom_files else gradle_files[0]))
        boot_version = _detect_spring_boot_version(combined)
        if boot_version:
            features.add(boot_version)
            note(boot_version, _relative(project_root, pom_files[0] if pom_files else gradle_files[0]))
        if _contains_any(combined, AI_MARKERS):
            features.add("ai")
            note("ai", _relative(project_root, pom_files[0] if pom_files else gradle_files[0]))
        if _contains_any(combined, KOTLIN_MARKERS):
            stacks.add("kotlin")
            note("kotlin", _relative(project_root, pom_files[0] if pom_files else gradle_files[0]))

    cargo_files = _find_named_files(project_root, {"Cargo.toml"})
    for cargo_path in cargo_files:
        stacks.add("rust")
        note("rust", _relative(project_root, cargo_path))

    csproj_files = _find_glob(project_root, "*.csproj")
    sln_files = _find_glob(project_root, "*.sln")
    if csproj_files or sln_files:
        stacks.add("dotnet")
        for path in (csproj_files + sln_files)[:6]:
            note("dotnet", _relative(project_root, path))
        combined = "\n".join(_read_text(path) for path in csproj_files[:4])
        if "Microsoft.AspNetCore" in combined or "Sdk.Web" in combined:
            features.add("aspnet-core")
            note("aspnet-core", _relative(project_root, csproj_files[0]))

    composer_files = _find_named_files(project_root, {"composer.json"})
    for composer_path in composer_files:
        stacks.add("php")
        note("php", _relative(project_root, composer_path))
        content = _read_text(composer_path)
        if "laravel/framework" in content:
            features.add("laravel")
            note("laravel", _relative(project_root, composer_path))
        if "symfony/" in content:
            features.add("symfony")
            note("symfony", _relative(project_root, composer_path))

    package_files = _find_named_files(project_root, {"package.json"})
    for package_path in package_files:
        content = _read_text(package_path)
        if not content:
            continue
        rel = _relative(project_root, package_path)
        if re.search(r'"react"\s*:', content):
            stacks.add("react")
            note("react", rel)
        if "@angular/core" in content or '"@angular/core"' in content:
            stacks.add("angular")
            note("angular", rel)
        if re.search(r'"(vue|nuxt)"\s*:', content) or "@vitejs/plugin-vue" in content:
            stacks.add("vue")
            note("vue", rel)
        if _contains_any(content, AI_MARKERS):
            features.add("ai")
            note("ai", rel)

    angular_json = _find_named_files(project_root, {"angular.json"})
    if angular_json:
        stacks.add("angular")
        for path in angular_json:
            note("angular", _relative(project_root, path))

    for vue_config in ("nuxt.config.ts", "nuxt.config.js", "nuxt.config.mjs", "vite.config.ts", "vite.config.js"):
        for path in _find_named_files(project_root, {vue_config}):
            content = _read_text(path)
            if "vue" in content.lower() or vue_config.startswith("nuxt"):
                stacks.add("vue")
                note("vue", _relative(project_root, path))
                break

    tailwind_configs = _find_glob(project_root, "tailwind.config.*")
    postcss_configs = _find_named_files(project_root, {"postcss.config.js", "postcss.config.mjs", "postcss.config.cjs"})
    for package_path in package_files:
        content = _read_text(package_path)
        if "tailwindcss" in content or "@tailwindcss/" in content:
            features.add("tailwind")
            note("tailwind", _relative(project_root, package_path))
            break
    for path in tailwind_configs + postcss_configs:
        features.add("tailwind")
        note("tailwind", _relative(project_root, path))

    for docker_name in ("Dockerfile", "docker-compose.yml", "docker-compose.yaml", "compose.yaml", "compose.yml"):
        for path in _find_named_files(project_root, {docker_name}):
            features.add("docker")
            note("docker", _relative(project_root, path))

    for ci_marker in CI_MARKERS:
        if ci_marker.endswith(".yml") or ci_marker.endswith(".yaml"):
            for path in _find_named_files(project_root, {Path(ci_marker).name}):
                features.add("ci")
                note("ci", _relative(project_root, path))
        else:
            ci_dir = project_root / ci_marker
            if ci_dir.exists():
                features.add("ci")
                note("ci", ci_marker)
            for path in _find_named_files(project_root, {Path(ci_marker).name}):
                features.add("ci")
                note("ci", _relative(project_root, path))

    test_markers = (
        "jest.config",
        "vitest.config",
        "playwright.config",
        "phpunit.xml",
        "karma.conf",
    )
    for marker in test_markers:
        for path in _find_glob(project_root, f"{marker}*"):
            features.add("automated-tests")
            note("automated-tests", _relative(project_root, path))
            break

    normalized_evidence = {key: tuple(sorted(set(values))) for key, values in sorted(evidence.items())}
    return RepoProfile(
        stacks=tuple(sorted(stacks)),
        features=tuple(sorted(features)),
        evidence=normalized_evidence,
    )


def recommend_for_project(
    repo: Repository,
    project_root: Path,
    *,
    include_consider: bool = True,
) -> RecommendReport:
    """Suggest install packs and optional skills for a target project."""
    profile = analyze_project(project_root)
    warnings: list[str] = []
    pack_candidates: list[tuple[str, str, str]] = []
    skill_candidates: list[tuple[str, str]] = []

    if profile.has_stack("java"):
        pack_candidates.append(("java-backend-pack", "recommended", "Java build files detected (Maven or Gradle)."))
    if profile.has_stack("dotnet"):
        pack_candidates.append(("dotnet-backend-pack", "recommended", ".NET project files detected."))
    if profile.has_stack("php"):
        pack_candidates.append(("php-backend-pack", "recommended", "PHP composer.json detected."))
    if profile.has_stack("kotlin"):
        pack_candidates.append(("kotlin-backend-pack", "recommended", "Kotlin build configuration detected."))
    if profile.has_stack("rust"):
        pack_candidates.append(("rust-backend-pack", "recommended", "Rust Cargo.toml detected."))
    if profile.has_stack("react"):
        pack_candidates.append(("frontend-react-pack", "recommended", "React dependency detected in package.json."))
    if profile.has_stack("angular"):
        pack_candidates.append(("frontend-angular-pack", "recommended", "Angular project detected."))
    if profile.has_stack("vue"):
        pack_candidates.append(("frontend-vue-pack", "recommended", "Vue dependency or config detected."))

    if profile.has_feature("ai"):
        pack_candidates.append(
            (
                "architecture-review-pack",
                "consider",
                "AI / LLM / RAG related dependencies detected — planning skills for architecture, eval, and orchestration.",
            )
        )
    if profile.has_feature("docker") and not profile.stacks:
        pack_candidates.append(
            (
                "architecture-review-pack",
                "consider",
                "Container or compose files detected — production readiness and delivery planning skills.",
            )
        )

    if include_consider:
        if profile.stacks or profile.has_feature("spring-boot"):
            pack_candidates.append(
                (
                    "architecture-review-pack",
                    "consider",
                    "Planning and review workflows for API design, readiness, and LLM architecture.",
                )
            )
        if profile.has_feature("automated-tests") or profile.has_feature("ci"):
            pack_candidates.append(
                (
                    "architecture-review-pack",
                    "consider",
                    "Test tooling or CI configuration detected — testing strategy and quality-gate planning.",
                )
            )
        if profile.stacks:
            pack_candidates.append(
                (
                    "architecture-review-pack",
                    "consider",
                    "Cross-stack security review complements stack-specific hardening in your technology pack.",
                )
            )
        if not profile.stacks and not profile.features:
            pack_candidates.append(
                (
                    "architecture-review-pack",
                    "consider",
                    "No stack auto-detected — start with cross-stack planning and review skills.",
                )
            )

    if profile.has_feature("spring-boot-4.1"):
        skill_candidates.append(("java-spring-boot-41", "Spring Boot 4.1 detected in build files."))
    elif profile.has_feature("spring-boot-4.0"):
        skill_candidates.append(("java-spring-boot-40", "Spring Boot 4.x detected in build files."))
    elif profile.has_feature("spring-boot-3.5"):
        skill_candidates.append(("java-spring-boot-35", "Spring Boot 3.5 detected in build files."))

    if profile.has_stack("java") and profile.has_feature("ai"):
        skill_candidates.append(("java-ai-backend-engineering", "Java backend with AI / LLM libraries detected."))
    if profile.has_stack("kotlin") and profile.has_feature("spring-boot"):
        skill_candidates.append(("kotlin-spring-boot-service", "Kotlin project with Spring Boot detected."))
    if profile.has_stack("react") and profile.has_feature("ai"):
        skill_candidates.append(("react-ai-product-engineering", "React app with AI-related dependencies detected."))
    if profile.has_stack("vue") and profile.has_feature("ai"):
        skill_candidates.append(("vue-ai-product-engineering", "Vue app with AI-related dependencies detected."))

    if profile.has_feature("ai"):
        for skill_id, reason in (
            ("llm-application-architecture", "Plan LLM patterns before implementation."),
            ("ai-evaluation-architecture", "Design eval datasets and quality gates for AI features."),
            ("agent-orchestration-design", "Design multi-step agent workflows and limits."),
        ):
            skill_candidates.append((skill_id, reason))

    packs = _finalize_pack_recommendations(repo, pack_candidates, warnings)
    skills = _finalize_skill_recommendations(repo, skill_candidates, warnings)

    return RecommendReport(
        project_root=project_root.resolve(),
        profile=profile,
        packs=packs,
        skills=skills,
        warnings=tuple(warnings),
    )


def format_recommend_report(
    report: RecommendReport,
    *,
    agent_skills_root: Path | None = None,
    target: str = "cursor",
) -> str:
    lines = [f"Project: {report.project_root}", ""]

    lines.append("Detected")
    if report.profile.stacks:
        lines.append(f"  Stacks: {', '.join(report.profile.stacks)}")
    else:
        lines.append("  Stacks: (none auto-detected)")
    if report.profile.features:
        lines.append(f"  Features: {', '.join(report.profile.features)}")
    if report.profile.evidence:
        lines.append("  Evidence:")
        for category, paths in report.profile.evidence.items():
            sample = ", ".join(paths[:3])
            if len(paths) > 3:
                sample += f", +{len(paths) - 3} more"
            lines.append(f"    - {category}: {sample}")
    lines.append("")

    recommended = [pack for pack in report.packs if pack.tier == "recommended"]
    consider = [pack for pack in report.packs if pack.tier == "consider"]

    if recommended:
        lines.append("Recommended packs")
        for pack in recommended:
            lines.append(f"  {pack.pack_id} ({pack.skill_count} skills)")
            lines.append(f"    {pack.reason}")
        lines.append("")

    if consider:
        lines.append("Also consider")
        for pack in consider:
            lines.append(f"  {pack.pack_id} ({pack.skill_count} skills)")
            lines.append(f"    {pack.reason}")
        lines.append("")

    if report.skills:
        lines.append("Optional skills (already in suggested packs or planning-only)")
        for skill in report.skills:
            lines.append(f"  {skill.skill_id}")
            lines.append(f"    {skill.reason}")
        lines.append("")

    commands = report.install_commands(agent_skills_root, target=target)
    if commands:
        lines.append("Install (from agent-skills clone)")
        for command in commands:
            lines.append(f"  {command}")
        lines.append("")
        if recommended:
            lines.append("Combine packs by running install once per pack, or install everything:")
            lines.append(f"  ./scripts/install-from-clone.sh --dest {report.project_root}")
        lines.append("")

    if report.warnings:
        lines.append("Warnings")
        for warning in report.warnings:
            lines.append(f"  - {warning}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def _finalize_pack_recommendations(
    repo: Repository,
    candidates: list[tuple[str, str, str]],
    warnings: list[str],
) -> tuple[PackRecommendation, ...]:
    seen: set[str] = set()
    results: list[PackRecommendation] = []
    for pack_id, tier, reason in candidates:
        if pack_id in seen:
            continue
        pack = repo.packs.get(pack_id)
        if pack is None:
            warnings.append(f"Pack '{pack_id}' is not registered in this catalog.")
            continue
        seen.add(pack_id)
        skill_ids = pack.data.get("skills", [])
        skill_count = len(skill_ids) if isinstance(skill_ids, list) else 0
        results.append(
            PackRecommendation(
                pack_id=pack_id,
                display_name=str(pack.data.get("display_name") or pack_id),
                tier=tier,
                reason=reason,
                skill_count=skill_count,
            )
        )
    tier_order = {"recommended": 0, "consider": 1}
    return tuple(sorted(results, key=lambda item: (tier_order.get(item.tier, 9), item.pack_id)))


def _finalize_skill_recommendations(
    repo: Repository,
    candidates: list[tuple[str, str]],
    warnings: list[str],
) -> tuple[SkillRecommendation, ...]:
    seen: set[str] = set()
    results: list[SkillRecommendation] = []
    for skill_id, reason in candidates:
        if skill_id in seen:
            continue
        skill = repo.skills.get(skill_id)
        if skill is None:
            warnings.append(f"Skill '{skill_id}' is not in the catalog.")
            continue
        if str(skill.metadata.get("status")) not in {"active", "recommended"}:
            continue
        seen.add(skill_id)
        results.append(
            SkillRecommendation(
                skill_id=skill_id,
                display_name=str(skill.metadata.get("display_name") or skill_id),
                reason=reason,
            )
        )
    return tuple(results)


def _find_named_files(root: Path, names: set[str]) -> list[Path]:
    matches: list[Path] = []
    for path in _walk_files(root):
        if path.name in names:
            matches.append(path)
    return sorted(matches)


def _find_glob(root: Path, pattern: str) -> list[Path]:
    matches: list[Path] = []
    for path in _walk_files(root):
        if path.match(pattern):
            matches.append(path)
    return sorted(matches)


def _walk_files(root: Path) -> list[Path]:
    results: list[Path] = []

    def walk(current: Path, depth: int) -> None:
        if depth > SCAN_MAX_DEPTH:
            return
        try:
            entries = sorted(current.iterdir(), key=lambda item: item.name)
        except OSError:
            return
        for entry in entries:
            if entry.is_dir():
                if entry.name in IGNORED_DIR_NAMES:
                    continue
                walk(entry, depth + 1)
            elif entry.is_file():
                results.append(entry)

    walk(root, 0)
    return results


def _read_text(path: Path) -> str:
    try:
        data = path.read_bytes()[:READ_LIMIT_BYTES]
        return data.decode("utf-8", errors="ignore")
    except OSError:
        return ""


def _relative(root: Path, path: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _contains_any(content: str, markers: tuple[str, ...]) -> bool:
    lowered = content.lower()
    return any(marker in lowered for marker in markers)


def _detect_spring_boot_version(content: str) -> str | None:
    patterns = (
        (r"spring-boot-starter-parent[\s\S]{0,400}?<version>\s*(4\.1\.[\d.A-Za-z-]+)", "spring-boot-4.1"),
        (r"spring-boot-starter-parent[\s\S]{0,400}?<version>\s*(4\.0\.[\d.A-Za-z-]+)", "spring-boot-4.0"),
        (r"spring-boot-starter-parent[\s\S]{0,400}?<version>\s*(3\.5\.[\d.A-Za-z-]+)", "spring-boot-3.5"),
        (r"org\.springframework\.boot[\s\S]{0,200}?version\s*[=:]\s*['\"]?(\d+\.\d+\.\d+)", None),
        (r"id\s*['\"]org\.springframework\.boot['\"][\s\S]{0,200}?version\s*['\"](\d+\.\d+\.\d+)['\"]", None),
    )
    for pattern, feature in patterns:
        match = re.search(pattern, content, flags=re.IGNORECASE)
        if not match:
            continue
        if feature:
            return feature
        version = match.group(1)
        if version.startswith("4.1."):
            return "spring-boot-4.1"
        if version.startswith("4.0."):
            return "spring-boot-4.0"
        if version.startswith("3.5."):
            return "spring-boot-3.5"
    if "spring-boot" in content.lower():
        return "spring-boot"
    return None


def recommend_project(
    agent_skills_root: Path,
    project_root: Path,
    *,
    include_consider: bool = True,
) -> RecommendReport:
    repo, warnings = load_repository(agent_skills_root)
    report = recommend_for_project(repo, project_root, include_consider=include_consider)
    if warnings:
        merged = list(report.warnings) + [f"catalog load: {item}" for item in warnings]
        return RecommendReport(
            project_root=report.project_root,
            profile=report.profile,
            packs=report.packs,
            skills=report.skills,
            warnings=tuple(merged),
        )
    return report


def render_recommend_json(
    report: RecommendReport,
    *,
    agent_skills_root: Path | None = None,
    target: str = "cursor",
) -> str:
    payload = report.to_dict()
    payload["install_commands"] = report.install_commands(agent_skills_root, target=target)
    payload["install_target"] = target
    return json.dumps(payload, indent=2, sort_keys=True)
