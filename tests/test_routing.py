from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from skillforge.models import Skill
from skillforge.routing import extract_resource_links, render_thin_routing_body, rewrite_resource_paths


class RoutingTests(unittest.TestCase):
    def test_rewrite_resource_paths_uses_bundle_root(self) -> None:
        body = "Read `references/api-design.md` and run `scripts/check.sh`."
        rewritten = rewrite_resource_paths(body, ".cursor/skills/java-spring-boot-service")
        self.assertIn("`.cursor/skills/java-spring-boot-service/references/api-design.md`", rewritten)
        self.assertIn("`.cursor/skills/java-spring-boot-service/scripts/check.sh`", rewritten)

    def test_extract_resource_links_finds_references_scripts_assets(self) -> None:
        body = "Read `references/a.md` and `scripts/run.sh` and `assets/diagram.png`."
        links = extract_resource_links(body)
        self.assertEqual(links, ["references/a.md", "scripts/run.sh", "assets/diagram.png"])

    def test_render_thin_routing_body_points_to_skill_bundle(self) -> None:
        skill = Skill(
            id="java-core-engineering",
            path=ROOT / "skills" / "java-core-engineering",
            frontmatter={"description": "Apply modern Java engineering practices."},
            body="Read `references/idioms.md`.\nRead `references/refactoring.md`.",
            metadata={"summary": "Apply modern Java engineering practices."},
        )
        rendered = render_thin_routing_body(skill, ".cursor/skills/java-core-engineering")
        self.assertIn("Primary workflow: `.cursor/skills/java-core-engineering/SKILL.md`", rendered)
        self.assertIn("`.cursor/skills/java-core-engineering/references/idioms.md`", rendered)
        self.assertIn("`.cursor/skills/java-core-engineering/references/refactoring.md`", rendered)
        self.assertNotIn("## Workflow", rendered)


if __name__ == "__main__":
    unittest.main()
