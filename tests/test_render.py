from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from skillforge.render import build_targets
from skillforge.validate import has_errors, validate_repository


class RenderTests(unittest.TestCase):
    def test_build_all_matches_representative_golden_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for folder in ("skills", "registry"):
                shutil.copytree(ROOT / folder, root / folder)

            repo, issues = validate_repository(root)
            self.assertFalse(has_errors(issues), [issue.message for issue in issues])
            build_targets(repo, "all")

            comparisons = [
                (
                    root / "dist" / "codex" / "skills" / "java-core-engineering" / "SKILL.md",
                    ROOT / "tests" / "golden" / "codex" / "java-core-engineering.SKILL.md",
                ),
                (
                    root / "dist" / "cursor" / ".cursor" / "rules" / "java-core-engineering.mdc",
                    ROOT / "tests" / "golden" / "cursor" / "java-core-engineering.mdc",
                ),
                (
                    root / "dist" / "cursor" / ".cursor" / "skills" / "java-core-engineering" / "SKILL.md",
                    ROOT / "tests" / "golden" / "codex" / "java-core-engineering.SKILL.md",
                ),
                (
                    root / "dist" / "copilot" / ".github" / "instructions" / "java-core-engineering.instructions.md",
                    ROOT / "tests" / "golden" / "copilot" / "java-core-engineering.instructions.md",
                ),
            ]
            for actual, expected in comparisons:
                self.assertEqual(
                    normalize(actual.read_text(encoding="utf-8")),
                    normalize(expected.read_text(encoding="utf-8")),
                    f"{actual} did not match {expected}",
                )

            reference = (
                root
                / "dist"
                / "cursor"
                / ".cursor"
                / "skills"
                / "java-core-engineering"
                / "references"
                / "idioms.md"
            )
            self.assertTrue(reference.exists(), f"missing cursor skill reference bundle: {reference}")

            copilot_reference = (
                root
                / "dist"
                / "copilot"
                / ".github"
                / "skills"
                / "java-core-engineering"
                / "references"
                / "idioms.md"
            )
            self.assertTrue(
                copilot_reference.exists(),
                f"missing copilot skill reference bundle: {copilot_reference}",
            )

            cursor_rule = root / "dist" / "cursor" / ".cursor" / "rules" / "java-core-engineering.mdc"
            copilot_instruction = (
                root
                / "dist"
                / "copilot"
                / ".github"
                / "instructions"
                / "java-core-engineering.instructions.md"
            )
            self.assertNotIn("## Workflow", cursor_rule.read_text(encoding="utf-8"))
            self.assertNotIn("## Workflow", copilot_instruction.read_text(encoding="utf-8"))


def normalize(value: str) -> str:
    return value.replace("\r\n", "\n").rstrip() + "\n"


if __name__ == "__main__":
    unittest.main()
