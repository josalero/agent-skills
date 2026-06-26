from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from skillforge.validate import has_errors, validate_repository


class ValidationTests(unittest.TestCase):
    def test_current_repository_validates(self) -> None:
        _, issues = validate_repository(ROOT)
        self.assertFalse(has_errors(issues), [issue.message for issue in issues])

    def test_missing_frontmatter_description_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill = root / "skills" / "bad-skill"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text(
                "---\nname: bad-skill\n---\n\n# Bad Skill\n\nBody.\n",
                encoding="utf-8",
            )
            (skill / "skill.yaml").write_text(
                """
id: bad-skill
display_name: Bad Skill
domain: java
kind: general
modes:
  - coding
status: draft
summary: Bad skill.
areas:
  - backend
tags:
  - java
collections: []
packs: []
targets:
  codex: true
stability: experimental
""",
                encoding="utf-8",
            )

            _, issues = validate_repository(root, skill_id="bad-skill", include_backlog=False)

        self.assertTrue(has_errors(issues))
        self.assertTrue(any("frontmatter.description is required" in issue.message for issue in issues))

    def test_active_skill_with_todo_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill = root / "skills" / "todo-skill"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text(
                "---\nname: todo-skill\ndescription: Do something when needed.\n---\n\n# Todo Skill\n\nTODO: finish workflow.\n",
                encoding="utf-8",
            )
            (skill / "skill.yaml").write_text(
                """
id: todo-skill
display_name: Todo Skill
domain: java
kind: general
modes:
  - coding
status: active
summary: Todo skill.
areas:
  - backend
tags:
  - java
collections: []
packs: []
targets:
  codex: true
  cursor: true
  copilot: true
stability: stable
""",
                encoding="utf-8",
            )

            _, issues = validate_repository(root, skill_id="todo-skill", include_backlog=False)

        self.assertTrue(has_errors(issues))
        self.assertTrue(any("TODO markers" in issue.message for issue in issues))


if __name__ == "__main__":
    unittest.main()

