from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from skillforge.parse import parse_yaml


class ParseYamlTests(unittest.TestCase):
    def test_nested_list_of_mappings(self) -> None:
        data = parse_yaml(
            """
version: 1
skills:
  - id: java-core-engineering
    areas:
      - backend
      - code-quality
    targets:
      codex: true
      cursor: false
"""
        )

        self.assertEqual(data["version"], 1)
        self.assertEqual(data["skills"][0]["id"], "java-core-engineering")
        self.assertEqual(data["skills"][0]["areas"], ["backend", "code-quality"])
        self.assertTrue(data["skills"][0]["targets"]["codex"])
        self.assertFalse(data["skills"][0]["targets"]["cursor"])


if __name__ == "__main__":
    unittest.main()

