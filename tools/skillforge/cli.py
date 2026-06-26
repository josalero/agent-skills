from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .backlog_gen import generate_backlog_file
from .catalog import active_skill_catalog, load_repository, write_catalog
from .install import install_pack
from .models import Issue
from .promote import promote_all_waves, promote_skill, promote_wave
from .recommend import format_recommend_report, recommend_project, render_recommend_json
from .render import build_targets
from .validate import has_errors, validate_repository


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="skillctl", description="Cross-agent skill library tooling")
    parser.add_argument("--root", default=".", help="Repository root")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate", help="Validate skills, collections, packs, and backlog")
    validate_parser.add_argument("skill_id", nargs="?", help="Skill ID to validate")
    validate_parser.add_argument("--all", action="store_true", help="Validate the full repository")

    build_parser = subparsers.add_parser("build", help="Build generated vendor output")
    build_parser.add_argument("--target", choices=["all", "claude", "codex", "cursor", "copilot", "opencode"], required=True)

    list_parser = subparsers.add_parser("list", help="List repository objects")
    list_group = list_parser.add_mutually_exclusive_group(required=True)
    list_group.add_argument("--skills", action="store_true")
    list_group.add_argument("--collections", action="store_true")
    list_group.add_argument("--packs", action="store_true")

    backlog_parser = subparsers.add_parser("backlog", help="Backlog commands")
    backlog_subparsers = backlog_parser.add_subparsers(dest="backlog_command", required=True)
    backlog_subparsers.add_parser("validate", help="Validate backlog")
    backlog_list_parser = backlog_subparsers.add_parser("list", help="List backlog items")
    backlog_list_parser.add_argument("--priority", choices=["P0", "P1", "P2", "P3"])
    backlog_list_parser.add_argument("--domain")
    backlog_generate_parser = backlog_subparsers.add_parser("generate", help="Generate backlog from taxonomy")
    backlog_generate_parser.add_argument("--from", dest="from_path", default="registry/taxonomy.yaml")
    backlog_generate_parser.add_argument("--out", dest="out_path", default="registry/skill-backlog.yaml")
    backlog_generate_parser.add_argument("--merge", action="store_true", default=True)
    backlog_promote_parser = backlog_subparsers.add_parser("promote", help="Promote backlog items to draft skill folders")
    backlog_promote_parser.add_argument("skill_id", nargs="?", help="Single backlog skill ID")
    backlog_promote_parser.add_argument("--wave", help="Promote all skills in a wave")
    backlog_promote_parser.add_argument("--all-waves", action="store_true", help="Promote all configured waves")

    subparsers.add_parser("doctor", help="Check local environment")

    catalog_parser = subparsers.add_parser("catalog", help="Build or print catalog data")
    catalog_parser.add_argument("--format", choices=["text", "json"], default="text")
    catalog_subparsers = catalog_parser.add_subparsers(dest="catalog_command")
    catalog_build_parser = catalog_subparsers.add_parser("build", help="Write dist/catalog reports")
    catalog_build_parser.add_argument("--include-backlog", action=argparse.BooleanOptionalAction, default=True)

    recommend_parser = subparsers.add_parser(
        "recommend",
        help="Analyze a project and suggest skills or packs to install",
    )
    recommend_parser.add_argument(
        "--dest",
        required=True,
        help="Path to the target project to analyze",
    )
    recommend_parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )
    recommend_parser.add_argument(
        "--primary-only",
        action="store_true",
        help="Omit 'also consider' cross-cutting packs",
    )
    recommend_parser.add_argument(
        "--target",
        choices=["cursor", "copilot", "codex", "claude", "opencode"],
        default="cursor",
        help="Agent target for generated install commands (default: cursor)",
    )

    install_parser = subparsers.add_parser("install", help="Install generated skills from a pack into a project")
    install_parser.add_argument("--pack", required=True, help="Pack ID (see skillctl list --packs)")
    install_parser.add_argument(
        "--target",
        choices=["cursor", "copilot", "codex", "claude", "opencode"],
        default="cursor",
        help="Vendor target output to install",
    )
    install_parser.add_argument(
        "--dest",
        required=True,
        help="Destination project root (skills copy into .cursor/, .github/, .claude/, or skills/)",
    )
    install_parser.add_argument(
        "--include-draft",
        action="store_true",
        help="Also install draft skills from the pack (default: active/recommended only)",
    )
    install_parser.add_argument(
        "--modes",
        nargs="+",
        choices=["coding", "planning"],
        help="Install only skills that support all listed modes (e.g. --modes planning)",
    )

    args = parser.parse_args(argv)
    root = Path(args.root).resolve()

    if args.command == "validate":
        skill_id = args.skill_id
        if not args.all and not skill_id:
            parser.error("validate requires --all or a skill_id")
        _, issues = validate_repository(root, skill_id=skill_id)
        print_issues(issues)
        if has_errors(issues):
            print("Validation failed.")
            return 1
        print("Validation passed.")
        return 0

    if args.command == "build":
        repo, issues = validate_repository(root)
        print_issues(issues)
        if has_errors(issues):
            print("Build stopped because validation failed.")
            return 1
        changed = build_targets(repo, args.target)
        print("Build completed.")
        for path in changed:
            print(f"  generated {path.relative_to(root)}")
        return 0

    if args.command == "list":
        repo, warnings = load_repository(root)
        for warning in warnings:
            print(f"warning: {warning}", file=sys.stderr)
        if args.skills:
            for skill_id in sorted(repo.skills):
                print(skill_id)
        elif args.collections:
            for collection_id in sorted(repo.collections):
                print(collection_id)
        elif args.packs:
            for pack_id in sorted(repo.packs):
                print(pack_id)
        return 0

    if args.command == "backlog":
        if args.backlog_command == "validate":
            _, issues = validate_repository(root, include_backlog=True)
            backlog_issues = [issue for issue in issues if "skill-backlog.yaml" in issue.path.as_posix()]
            print_issues(backlog_issues)
            if has_errors(backlog_issues):
                print("Backlog validation failed.")
                return 1
            print("Backlog validation passed.")
            return 0
        if args.backlog_command == "list":
            repo, _ = load_repository(root)
            if repo.backlog is None:
                print("No backlog found.")
                return 1
            for item in repo.backlog.data.get("skills", []):
                if args.priority and item.get("priority") != args.priority:
                    continue
                if args.domain and item.get("domain") != args.domain:
                    continue
                print(f"{item.get('id')} [{item.get('priority')}] {item.get('status')}")
            return 0
        if args.backlog_command == "generate":
            path, count = generate_backlog_file(root, merge_existing=args.merge)
            print(f"Generated {count} backlog entries at {path.relative_to(root)}")
            return 0
        if args.backlog_command == "promote":
            try:
                if args.all_waves:
                    promoted = promote_all_waves(root)
                elif args.wave:
                    promoted = promote_wave(root, args.wave)
                elif args.skill_id:
                    promoted = [promote_skill(root, args.skill_id)]
                else:
                    print("promote requires skill_id, --wave, or --all-waves")
                    return 2
            except ValueError as exc:
                print(str(exc))
                return 1
            print(f"Promoted {len(promoted)} skill folder(s).")
            for path in promoted:
                print(f"  {path.relative_to(root)}")
            return 0

    if args.command == "doctor":
        return doctor(root)

    if args.command == "catalog":
        if args.catalog_command == "build":
            repo, issues = validate_repository(root)
            if has_errors(issues):
                print_issues(issues)
                return 1
            changed = write_catalog(repo, include_backlog=args.include_backlog)
            print("Catalog build completed.")
            for path in changed:
                print(f"  generated {path.relative_to(root)}")
            return 0
        repo, issues = validate_repository(root)
        if has_errors(issues):
            print_issues(issues)
            return 1
        if args.format == "json":
            import json

            print(json.dumps(active_skill_catalog(repo), indent=2, sort_keys=True))
        else:
            for item in active_skill_catalog(repo):
                print(f"{item['id']}: {item['summary']}")
        return 0

    if args.command == "recommend":
        project_root = Path(args.dest).resolve()
        if not project_root.is_dir():
            print(f"Project path is not a directory: {project_root}")
            return 1
        try:
            report = recommend_project(
                root,
                project_root,
                include_consider=not args.primary_only,
            )
        except ValueError as exc:
            print(str(exc))
            return 1
        if args.format == "json":
            print(render_recommend_json(report, agent_skills_root=root, target=args.target))
        else:
            print(format_recommend_report(report, agent_skills_root=root, target=args.target), end="")
        return 0

    if args.command == "install":
        requested_modes: set[str] | None = None
        if args.modes:
            requested_modes = set(args.modes)
        try:
            result = install_pack(
                root,
                args.pack,
                args.target,
                Path(args.dest),
                active_only=not args.include_draft,
                modes=requested_modes,
            )
        except ValueError as exc:
            print(str(exc))
            return 1
        print(f"Installed {len(result.installed)} skill(s) from pack '{result.pack_id}' to {result.destination}")
        for skill_id in result.installed:
            print(f"  installed {skill_id}")
        for skill_id in result.skipped_draft:
            print(f"  skipped draft {skill_id}")
        for skill_id in result.skipped_missing:
            print(f"  skipped missing {skill_id}")
        for skill_id in result.skipped_target:
            print(f"  skipped unsupported target {skill_id}")
        for skill_id in result.skipped_modes:
            print(f"  skipped mode filter {skill_id}")
        if not result.installed:
            print("No skills installed.")
            return 1
        return 0

    parser.error("unknown command")
    return 2


def print_issues(issues: list[Issue]) -> None:
    if not issues:
        return
    for issue in issues:
        print(f"{issue.severity.upper()} {issue.path}: {issue.message}")


def doctor(root: Path) -> int:
    print(f"Repository root: {root}")
    print(f"Python: {sys.version.split()[0]}")
    for required in ("skills", "registry", "dist"):
        path = root / required
        status = "OK" if path.exists() else "MISSING"
        print(f"{status} {required}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
