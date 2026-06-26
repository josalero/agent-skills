from __future__ import annotations

import re

from .models import Skill

RESOURCE_PREFIXES = ("references", "scripts", "assets")


def rewrite_resource_paths(body: str, bundle_root: str) -> str:
    bundle_root = bundle_root.rstrip("/")
    rewritten = body
    for prefix in RESOURCE_PREFIXES:
        pattern = rf"`({prefix}/[^`]+)`"
        rewritten = re.sub(pattern, rf"`{bundle_root}/\1`", rewritten)
    return rewritten


def extract_resource_links(body: str) -> list[str]:
    links: list[str] = []
    for prefix in RESOURCE_PREFIXES:
        pattern = rf"`({prefix}/[^`]+)`"
        links.extend(re.findall(pattern, body))
    return links


def render_thin_routing_body(skill: Skill, bundle_root: str) -> str:
    bundle_root = bundle_root.rstrip("/")
    skill_md = f"{bundle_root}/SKILL.md"
    when_to_use = skill.description or skill.summary
    lines = [
        f"Skill bundle: `{bundle_root}/`",
        "",
        f"Primary workflow: `{skill_md}`",
        "",
        "When this guidance applies:",
        "",
        f"1. Read `{skill_md}`.",
        "2. Follow its workflow, checklist, and output format.",
        "3. Load linked files from the same skill bundle before making changes.",
        "",
        "When to use:",
        "",
        when_to_use,
    ]
    links = extract_resource_links(skill.body)
    if links:
        lines.extend(["", "Linked resources:", ""])
        for link in links:
            lines.append(f"- `{bundle_root}/{link}`")
    return "\n".join(lines)
