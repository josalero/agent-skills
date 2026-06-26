from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from skillforge.catalog import load_repository
from skillforge.recommend import (
    analyze_project,
    format_recommend_report,
    recommend_for_project,
    recommend_project,
)


class RecommendTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo, _ = load_repository(ROOT)

    def test_java_spring_boot_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "service"
            project.mkdir()
            (project / "pom.xml").write_text(
                """
                <project>
                  <parent>
                    <groupId>org.springframework.boot</groupId>
                    <artifactId>spring-boot-starter-parent</artifactId>
                    <version>4.0.1</version>
                  </parent>
                </project>
                """,
                encoding="utf-8",
            )
            (project / "Dockerfile").write_text("FROM eclipse-temurin:25", encoding="utf-8")

            profile = analyze_project(project)
            self.assertIn("java", profile.stacks)
            self.assertIn("spring-boot", profile.features)
            self.assertIn("spring-boot-4.0", profile.features)
            self.assertIn("docker", profile.features)

            report = recommend_for_project(self.repo, project)
            pack_ids = [item.pack_id for item in report.packs if item.tier == "recommended"]
            self.assertIn("java-backend-pack", pack_ids)
            self.assertIn("production-readiness-pack", pack_ids)

            skill_ids = [item.skill_id for item in report.skills]
            self.assertIn("java-spring-boot-40", skill_ids)

    def test_react_project_with_ai_dependencies(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "web"
            project.mkdir()
            (project / "package.json").write_text(
                json.dumps(
                    {
                        "dependencies": {
                            "react": "^19.0.0",
                            "openai": "^4.0.0",
                        }
                    }
                ),
                encoding="utf-8",
            )

            report = recommend_for_project(self.repo, project)
            recommended = {item.pack_id for item in report.packs if item.tier == "recommended"}
            self.assertIn("frontend-react-pack", recommended)
            self.assertIn("ai-engineering-pack", recommended)

            skill_ids = [item.skill_id for item in report.skills]
            self.assertIn("react-ai-product-engineering", skill_ids)
            self.assertIn("llm-application-architecture", skill_ids)

    def test_vue_project_with_ai_dependencies(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "web"
            project.mkdir()
            (project / "package.json").write_text(
                json.dumps(
                    {
                        "dependencies": {
                            "vue": "^3.5.0",
                            "openai": "^4.0.0",
                        },
                        "devDependencies": {
                            "@vitejs/plugin-vue": "^5.0.0",
                        },
                    }
                ),
                encoding="utf-8",
            )

            report = recommend_for_project(self.repo, project)
            recommended = {item.pack_id for item in report.packs if item.tier == "recommended"}
            self.assertIn("frontend-vue-pack", recommended)
            self.assertIn("ai-engineering-pack", recommended)

            skill_ids = [item.skill_id for item in report.skills]
            self.assertIn("vue-ai-product-engineering", skill_ids)

    def test_kotlin_spring_boot_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "service"
            project.mkdir()
            (project / "build.gradle.kts").write_text(
                """
                plugins {
                    kotlin("jvm") version "2.0.0"
                    id("org.springframework.boot") version "3.5.0"
                }
                """,
                encoding="utf-8",
            )

            profile = analyze_project(project)
            self.assertIn("kotlin", profile.stacks)
            self.assertIn("java", profile.stacks)
            self.assertIn("spring-boot", profile.features)

            report = recommend_for_project(self.repo, project)
            recommended = {item.pack_id for item in report.packs if item.tier == "recommended"}
            self.assertIn("kotlin-backend-pack", recommended)
            self.assertIn("java-backend-pack", recommended)

            skill_ids = [item.skill_id for item in report.skills]
            self.assertIn("kotlin-spring-boot-service", skill_ids)

    def test_rust_cargo_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "service"
            project.mkdir()
            (project / "Cargo.toml").write_text(
                """
                [package]
                name = "demo"
                version = "0.1.0"
                edition = "2024"
                """,
                encoding="utf-8",
            )

            profile = analyze_project(project)
            self.assertIn("rust", profile.stacks)

            report = recommend_for_project(self.repo, project)
            recommended = {item.pack_id for item in report.packs if item.tier == "recommended"}
            self.assertIn("rust-backend-pack", recommended)

    def test_primary_only_omits_consider_packs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "service"
            project.mkdir()
            (project / "build.gradle.kts").write_text(
                'plugins { id("org.springframework.boot") version "3.5.0" }',
                encoding="utf-8",
            )

            full = recommend_for_project(self.repo, project, include_consider=True)
            primary = recommend_for_project(self.repo, project, include_consider=False)

            self.assertTrue(any(item.tier == "consider" for item in full.packs))
            self.assertFalse(any(item.tier == "consider" for item in primary.packs))
            self.assertTrue(any(item.pack_id == "java-backend-pack" for item in primary.packs))

    def test_empty_project_suggests_architecture_pack(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "empty"
            project.mkdir()

            report = recommend_for_project(self.repo, project)
            consider = [item.pack_id for item in report.packs if item.tier == "consider"]
            self.assertIn("architecture-review-pack", consider)
            self.assertFalse(any(item.tier == "recommended" for item in report.packs))

    def test_format_includes_install_commands(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "service"
            project.mkdir()
            (project / "composer.json").write_text('{"require":{"php":"^8.3"}}', encoding="utf-8")

            report = recommend_project(ROOT, project)
            rendered = format_recommend_report(report, agent_skills_root=ROOT)
            self.assertIn("php-backend-pack", rendered)
            self.assertIn("install-from-clone.sh", rendered)

    def test_cli_recommend_json(self) -> None:
        import subprocess

        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "service"
            project.mkdir()
            (project / "pom.xml").write_text("<project></project>", encoding="utf-8")

            result = subprocess.run(
                [
                    str(ROOT / "tools" / "skillctl"),
                    "recommend",
                    "--dest",
                    str(project),
                    "--format",
                    "json",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertIn("java", payload["profile"]["stacks"])
            self.assertTrue(any(item["pack_id"] == "java-backend-pack" for item in payload["packs"]))


if __name__ == "__main__":
    unittest.main()
