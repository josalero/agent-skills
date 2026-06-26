from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from skillforge.modes import CODING_ONLY_SKILLS, PLANNING_ONLY_SKILLS, resolve_modes, skill_supports_modes
from skillforge.parse import parse_yaml_file


class ModesTests(unittest.TestCase):
    def test_all_skills_have_canonical_modes(self) -> None:
        skills_dir = ROOT / "skills"
        for path in sorted(skills_dir.glob("*/skill.yaml")):
            metadata = parse_yaml_file(path)
            skill_id = path.parent.name
            expected = resolve_modes(skill_id)
            self.assertEqual(metadata.get("modes"), expected, skill_id)

    def test_mode_counts(self) -> None:
        self.assertEqual(len(PLANNING_ONLY_SKILLS), 12)
        self.assertEqual(len(CODING_ONLY_SKILLS), 16)
        self.assertEqual(len(PLANNING_ONLY_SKILLS | CODING_ONLY_SKILLS), 28)

    def test_skill_supports_modes_requires_subset(self) -> None:
        self.assertTrue(skill_supports_modes(["planning", "coding"], {"planning"}))
        self.assertFalse(skill_supports_modes(["coding"], {"planning"}))
        self.assertTrue(skill_supports_modes(["planning", "coding"], {"planning", "coding"}))


if __name__ == "__main__":
    unittest.main()
